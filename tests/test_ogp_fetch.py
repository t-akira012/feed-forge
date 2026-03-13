import json
import io
import sys
from unittest.mock import patch, MagicMock
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

import pytest

SCRIPT = "skills/ogp-fetch/scripts/fetch.py"


def load_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ogp_fetch", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestExtractOgImage:
    def test_extracts_og_image(self):
        mod = load_module()
        html = '<html><head><meta property="og:image" content="https://example.com/img.jpg"></head></html>'
        assert mod.extract_og_image(html) == "https://example.com/img.jpg"

    def test_returns_empty_when_no_og_image(self):
        mod = load_module()
        html = "<html><head><title>Test</title></head></html>"
        assert mod.extract_og_image(html) == ""

    def test_handles_single_quotes(self):
        mod = load_module()
        html = "<html><head><meta property='og:image' content='https://example.com/img.png'></head></html>"
        assert mod.extract_og_image(html) == "https://example.com/img.png"

    def test_handles_malformed_html(self):
        mod = load_module()
        assert mod.extract_og_image("") == ""
        assert mod.extract_og_image("not html at all") == ""


class TestFetchOgImages:
    def test_adds_og_image_field(self):
        mod = load_module()
        html = '<html><head><meta property="og:image" content="https://example.com/og.jpg"></head></html>'

        def mock_get(url, timeout=10):
            resp = MagicMock()
            resp.text = html
            resp.status_code = 200
            resp.raise_for_status = lambda: None
            return resp

        items = [{"title": "Test", "url": "https://example.com/article"}]
        with patch.object(mod.requests, "get", side_effect=mock_get):
            result = mod.fetch_og_images(items)
        assert result[0]["og_image"] == "https://example.com/og.jpg"

    def test_fetch_failure_sets_empty(self):
        mod = load_module()

        def mock_get(url, timeout=10):
            raise Exception("connection error")

        items = [{"title": "Test", "url": "https://example.com/fail"}]
        with patch.object(mod.requests, "get", side_effect=mock_get):
            result = mod.fetch_og_images(items)
        assert result[0]["og_image"] == ""

    def test_preserves_existing_fields(self):
        mod = load_module()
        html = '<html><head><meta property="og:image" content="https://example.com/og.jpg"></head></html>'

        def mock_get(url, timeout=10):
            resp = MagicMock()
            resp.text = html
            resp.raise_for_status = lambda: None
            return resp

        items = [{"title": "Test", "url": "https://example.com/a", "published": "2026-03-13"}]
        with patch.object(mod.requests, "get", side_effect=mock_get):
            result = mod.fetch_og_images(items)
        assert result[0]["title"] == "Test"
        assert result[0]["published"] == "2026-03-13"
        assert result[0]["og_image"] == "https://example.com/og.jpg"
