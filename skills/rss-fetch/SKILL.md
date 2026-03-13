---
name: rss-fetch
description: RSSフィードを解析し記事一覧をJSON形式で出力する。input_list.txtでconecter_type: rss-fetchが指定された場合に使用。
allowed-tools: Bash(python:*)
---

scripts/fetch.py を実行し、引数にURLを渡す。
出力はJSON（stdout）で、各要素は {title, url, published} を含む。
