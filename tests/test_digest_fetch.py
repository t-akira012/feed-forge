import json
import os
from unittest.mock import patch, MagicMock
from skills.digest_fetch_helper import parse_input_list, fetch_all_sources


SAMPLE_INPUT = """# comment
---
list: https://example.com/rss
conecter_type: rss-fetch
category: IT
get_data: "tech articles"
block_data: "ads"
---
list: https://example.com/api
conecter_type: api-fetch
category: 中国
lang: en
get_data: "politics"
block_data: "sports"
"""


def test_parse_input_list_extracts_entries():
    entries = parse_input_list(SAMPLE_INPUT)
    assert len(entries) == 2
    assert entries[0]["list"] == "https://example.com/rss"
    assert entries[0]["conecter_type"] == "rss-fetch"
    assert entries[0]["category"] == "IT"
    assert entries[1]["lang"] == "en"


def test_parse_input_list_skips_comments():
    entries = parse_input_list(SAMPLE_INPUT)
    for e in entries:
        assert not e["list"].startswith("#")


def test_fetch_all_sources_adds_category_and_lang():
    fake_articles = json.dumps([
        {"title": "Test Article", "url": "https://example.com/1", "published": ""}
    ])
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = fake_articles

    with patch("skills.digest_fetch_helper.subprocess.run", return_value=mock_result):
        entries = parse_input_list(SAMPLE_INPUT)
        result = fetch_all_sources(entries)

    assert len(result) >= 1
    # Check category is attached
    it_articles = [a for a in result if a["category"] == "IT"]
    assert len(it_articles) >= 1
    # Check lang is attached for entries that have it
    cn_articles = [a for a in result if a["category"] == "中国"]
    assert cn_articles[0]["lang"] == "en"
    # IT entry has no lang, should default to empty
    assert it_articles[0].get("lang", "") == ""
