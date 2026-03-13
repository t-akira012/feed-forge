---
name: scrape-fetch
description: HTMLページをスクレイピングし記事一覧をJSON取得する。RSSが利用できないサイト向け。
allowed-tools: Bash(python:*)
---

scripts/fetch.py を実行し、引数にURLを渡す。
出力はJSON（stdout）で、各要素は {title, url, published} を含む。
