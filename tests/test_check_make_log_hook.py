import os
import subprocess
import tempfile

import pytest

HOOK = os.path.abspath(".claude/hooks/check-make-log.sh")


def run_hook(project_dir):
    env = os.environ.copy()
    env["CLAUDE_PROJECT_DIR"] = project_dir
    r = subprocess.run(
        ["bash", HOOK],
        capture_output=True, text=True, env=env, cwd=project_dir
    )
    return r


def init_git_repo(d):
    subprocess.run(["git", "init"], cwd=d, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=d, capture_output=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=d, capture_output=True)
    # Initial commit so HEAD exists
    open(os.path.join(d, ".gitkeep"), "w").close()
    subprocess.run(["git", "add", "."], cwd=d, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=d, capture_output=True)


class TestCheckMakeLogHook:
    def test_no_changes_no_output(self):
        with tempfile.TemporaryDirectory() as d:
            init_git_repo(d)
            r = run_hook(d)
            assert r.returncode == 0
            assert r.stdout == ""

    def test_work_changes_without_make_log_warns(self):
        with tempfile.TemporaryDirectory() as d:
            init_git_repo(d)
            os.makedirs(os.path.join(d, "skills", "foo"))
            open(os.path.join(d, "skills", "foo", "test.py"), "w").close()
            r = run_hook(d)
            assert r.returncode == 0
            assert "make-log リマインダー" in r.stdout

    def test_work_changes_with_make_log_no_warn(self):
        with tempfile.TemporaryDirectory() as d:
            init_git_repo(d)
            os.makedirs(os.path.join(d, "skills", "foo"))
            open(os.path.join(d, "skills", "foo", "test.py"), "w").close()
            os.makedirs(os.path.join(d, "make_log"))
            open(os.path.join(d, "make_log", "001_foo_task.md"), "w").close()
            r = run_hook(d)
            assert r.returncode == 0
            assert "make-log リマインダー" not in r.stdout

    def test_only_make_log_changes_no_warn(self):
        with tempfile.TemporaryDirectory() as d:
            init_git_repo(d)
            os.makedirs(os.path.join(d, "make_log"))
            open(os.path.join(d, "make_log", "001_foo_task.md"), "w").close()
            r = run_hook(d)
            assert r.returncode == 0
            assert "make-log リマインダー" not in r.stdout

    def test_not_git_repo_no_output(self):
        with tempfile.TemporaryDirectory() as d:
            r = run_hook(d)
            assert r.returncode == 0
            assert r.stdout == ""
