import json
import os
import tempfile
import subprocess
import sys
import io

import pytest

NEXT_NUMBER = "skills/make-log/scripts/next_number.py"
INIT_TASK = "skills/make-log/scripts/init_task.py"
WRITE_LOG = "skills/make-log/scripts/write_log.py"


def load_module(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestNextNumber:
    def test_empty_dir(self):
        with tempfile.TemporaryDirectory() as d:
            mod = load_module(NEXT_NUMBER)
            assert mod.next_number(d) == 1

    def test_with_existing_files(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "001_foo_task.md"), "w").close()
            open(os.path.join(d, "001_foo_log.md"), "w").close()
            open(os.path.join(d, "002_bar_task.md"), "w").close()
            mod = load_module(NEXT_NUMBER)
            assert mod.next_number(d) == 3

    def test_ignores_non_numbered_files(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "README.md"), "w").close()
            open(os.path.join(d, "001_foo_task.md"), "w").close()
            mod = load_module(NEXT_NUMBER)
            assert mod.next_number(d) == 2

    def test_nonexistent_dir_returns_1(self):
        mod = load_module(NEXT_NUMBER)
        assert mod.next_number("/tmp/nonexistent_make_log_dir_xyz") == 1


class TestInitTask:
    def test_creates_task_file(self):
        with tempfile.TemporaryDirectory() as d:
            mod = load_module(INIT_TASK)
            path = mod.create_task(d, "test-feature")
            assert os.path.exists(path)
            assert "001_test-feature_task.md" in path

    def test_task_file_has_template(self):
        with tempfile.TemporaryDirectory() as d:
            mod = load_module(INIT_TASK)
            path = mod.create_task(d, "test-feature")
            with open(path) as f:
                content = f.read()
            assert "# test-feature" in content
            assert "タスク一覧" in content
            assert "[ ]" in content

    def test_increments_number(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "001_old_task.md"), "w").close()
            mod = load_module(INIT_TASK)
            path = mod.create_task(d, "new")
            assert "002_new_task.md" in path


class TestWriteLog:
    def test_creates_log_file(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "001_feat_task.md"), "w").close()
            mod = load_module(WRITE_LOG)
            path = mod.create_log(d, "feat")
            assert os.path.exists(path)
            assert "001_feat_log.md" in path

    def test_log_file_has_template(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "001_feat_task.md"), "w").close()
            mod = load_module(WRITE_LOG)
            path = mod.create_log(d, "feat")
            with open(path) as f:
                content = f.read()
            assert "# MAKE_LOG: feat" in content
            assert "実装の流れ" in content

    def test_matches_existing_task_number(self):
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "003_feat_task.md"), "w").close()
            mod = load_module(WRITE_LOG)
            path = mod.create_log(d, "feat")
            assert "003_feat_log.md" in path

    def test_error_if_no_matching_task(self):
        with tempfile.TemporaryDirectory() as d:
            mod = load_module(WRITE_LOG)
            with pytest.raises(FileNotFoundError):
                mod.create_log(d, "nonexistent")
