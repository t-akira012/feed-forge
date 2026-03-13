import json
from unittest.mock import patch, MagicMock
from skills.scrape_fetch_helper import fetch


SAMPLE_HTML = """
<html><body>
<a href="/article/123">This is a long enough article title</a>
<a href="/article/456">Another article with a decent title here</a>
<a href="/short">Too short</a>
<a href="/article/123">This is a long enough article title</a>
</body></html>
"""


def test_fetch_extracts_articles():
    mock_resp = MagicMock()
    mock_resp.text = SAMPLE_HTML
    mock_resp.raise_for_status = MagicMock()

    with patch("skills.scrape_fetch_helper.requests.get", return_value=mock_resp):
        items = fetch("https://example.com")

    assert len(items) == 2
    assert items[0]["title"] == "This is a long enough article title"
    assert items[0]["url"] == "https://example.com/article/123"
    assert items[1]["url"] == "https://example.com/article/456"


def test_fetch_skips_short_titles():
    mock_resp = MagicMock()
    mock_resp.text = '<html><body><a href="/x">Short</a></body></html>'
    mock_resp.raise_for_status = MagicMock()

    with patch("skills.scrape_fetch_helper.requests.get", return_value=mock_resp):
        items = fetch("https://example.com")

    assert len(items) == 0


def test_fetch_limits_to_30():
    links = "".join(f'<a href="/a/{i}">Article title number {i} is long enough</a>' for i in range(50))
    mock_resp = MagicMock()
    mock_resp.text = f"<html><body>{links}</body></html>"
    mock_resp.raise_for_status = MagicMock()

    with patch("skills.scrape_fetch_helper.requests.get", return_value=mock_resp):
        items = fetch("https://example.com")

    assert len(items) == 30
