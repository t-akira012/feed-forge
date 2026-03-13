---
name: api-fetch
description: JSON APIから記事一覧を取得する。input_list.txtでconecter_type: api-fetchが指定された場合に使用。現在Zenn APIに対応。
allowed-tools: Bash(python:*)
---

scripts/fetch.py を実行し、引数にURLを渡す。
出力はJSON（stdout）で、各要素は {title, url, published} を含む。
