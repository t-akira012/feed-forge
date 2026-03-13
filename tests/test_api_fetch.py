import json
import io
import sys
from unittest.mock import patch, MagicMock

import pytest

SCRIPT = "skills/api-fetch/scripts/fetch.py"


def run_fetch(url, response_json, status_code=200):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = response_json

    buf = io.StringIO()
    original_stdout = sys.stdout
    original_argv = sys.argv

    try:
        sys.stdout = buf
        sys.argv = ["fetch.py", url]

        import importlib.util
        spec = importlib.util.spec_from_file_location("fetch", SCRIPT)
        mod = importlib.util.module_from_spec(spec)

        with patch("requests.get", return_value=mock_response) as mock_get:
            spec.loader.exec_module(mod)
            mod.main()
            mock_get.assert_called_once_with(url, timeout=30)

        return json.loads(buf.getvalue())
    finally:
        sys.stdout = original_stdout
        sys.argv = original_argv


class TestApiFetchZenn:
    def test_empty_articles(self):
        result = run_fetch(
            "https://zenn.dev/api/articles?order=daily",
            {"articles": []},
        )
        assert result == []

    def test_single_article(self):
        response = {
            "articles": [
                {
                    "title": "テスト記事",
                    "path": "/user/articles/abc123",
                    "published_at": "2026-03-13T10:00:00.000+09:00",
                }
            ]
        }
        result = run_fetch("https://zenn.dev/api/articles?order=daily", response)
        assert len(result) == 1
        assert result[0]["title"] == "テスト記事"
        assert result[0]["url"] == "https://zenn.dev/user/articles/abc123"
        assert result[0]["published"] == "2026-03-13T10:00:00.000+09:00"

    def test_max_30_articles(self):
        articles = [
            {"title": f"T{i}", "path": f"/u/articles/{i}", "published_at": ""}
            for i in range(50)
        ]
        result = run_fetch(
            "https://zenn.dev/api/articles?order=daily",
            {"articles": articles},
        )
        assert len(result) == 30
