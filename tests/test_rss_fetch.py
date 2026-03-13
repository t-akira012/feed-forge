import json
import io
import sys
from unittest.mock import MagicMock

import pytest

SCRIPT = "skills/rss-fetch/scripts/fetch.py"


def make_entry(title, link, published):
    return {"title": title, "link": link, "published": published}


def run_fetch(url, entries):
    mock_fp = MagicMock()
    mock_result = MagicMock()
    mock_result.entries = entries
    mock_fp.parse.return_value = mock_result

    original_feedparser = sys.modules.get("feedparser")
    sys.modules["feedparser"] = mock_fp

    buf = io.StringIO()
    original_stdout = sys.stdout
    original_argv = sys.argv

    try:
        sys.stdout = buf
        sys.argv = ["fetch.py", url]

        import importlib.util
        spec = importlib.util.spec_from_file_location("fetch", SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()

        mock_fp.parse.assert_called_once_with(url)
        return json.loads(buf.getvalue())
    finally:
        sys.stdout = original_stdout
        sys.argv = original_argv
        if original_feedparser is not None:
            sys.modules["feedparser"] = original_feedparser
        else:
            sys.modules.pop("feedparser", None)


class TestRssFetch:
    def test_empty_feed(self):
        result = run_fetch("https://example.com/rss", [])
        assert result == []

    def test_single_entry(self):
        entries = [make_entry("Test Title", "https://example.com/1", "2026-03-13")]
        result = run_fetch("https://example.com/rss", entries)
        assert len(result) == 1
        assert result[0]["title"] == "Test Title"
        assert result[0]["url"] == "https://example.com/1"
        assert result[0]["published"] == "2026-03-13"

    def test_max_30_entries(self):
        entries = [make_entry(f"T{i}", f"https://example.com/{i}", "") for i in range(50)]
        result = run_fetch("https://example.com/rss", entries)
        assert len(result) == 30
