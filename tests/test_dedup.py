import json
import os
import tempfile
import time

import pytest

SCRIPT = "skills/dedup/scripts/dedup.py"


def load_dedup_module(state_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("dedup", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.STATE_PATH = state_path
    return mod


class TestDedup:
    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.state_path = os.path.join(self.tmpdir, "state.json")

    def _run(self, items, state_path=None):
        import io, sys
        path = state_path or self.state_path
        mod = load_dedup_module(path)

        stdin_buf = io.StringIO(json.dumps(items))
        stdout_buf = io.StringIO()
        old_stdin, old_stdout = sys.stdin, sys.stdout
        try:
            sys.stdin = stdin_buf
            sys.stdout = stdout_buf
            mod.main()
            return json.loads(stdout_buf.getvalue())
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout

    def test_all_new(self):
        items = [{"url": "https://example.com/1"}, {"url": "https://example.com/2"}]
        result = self._run(items)
        assert len(result) == 2

    def test_dedup_second_run(self):
        items = [{"url": "https://example.com/1"}]
        self._run(items)
        result = self._run(items)
        assert result == []

    def test_mixed_new_and_seen(self):
        self._run([{"url": "https://example.com/1"}])
        items = [{"url": "https://example.com/1"}, {"url": "https://example.com/2"}]
        result = self._run(items)
        assert len(result) == 1
        assert result[0]["url"] == "https://example.com/2"

    def test_empty_url_skipped(self):
        items = [{"url": ""}, {"title": "no url"}]
        result = self._run(items)
        assert result == []

    def test_state_file_created(self):
        self._run([{"url": "https://example.com/1"}])
        assert os.path.exists(self.state_path)
        with open(self.state_path) as f:
            state = json.load(f)
        assert "seen" in state
        assert "last_run" in state
