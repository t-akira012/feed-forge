import os
import tempfile
import io
import sys

import pytest

SCRIPT = "skills/deliver/scripts/deliver.py"


def load_deliver_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("deliver", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestDeliver:
    def test_deliver_file(self):
        mod = load_deliver_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out", "digest.md")
            content = "# Today's Digest\n\n- Article 1\n- Article 2"

            old_stdin, old_argv = sys.stdin, sys.argv
            try:
                sys.stdin = io.StringIO(content)
                sys.argv = ["deliver.py", "file", path]
                mod.main()
            finally:
                sys.stdin = old_stdin
                sys.argv = old_argv

            assert os.path.exists(path)
            with open(path) as f:
                assert f.read() == content

    def test_deliver_file_creates_parent_dirs(self):
        mod = load_deliver_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "a", "b", "c", "digest.md")

            old_stdin, old_argv = sys.stdin, sys.argv
            try:
                sys.stdin = io.StringIO("test")
                sys.argv = ["deliver.py", "file", path]
                mod.main()
            finally:
                sys.stdin = old_stdin
                sys.argv = old_argv

            assert os.path.exists(path)
