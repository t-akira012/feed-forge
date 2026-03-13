---
name: ogp-fetch
description: 記事URLからOGP画像URLを抽出し、og_imageフィールドを追加する。画像のローカル保存は行わない。
allowed-tools: Bash(python:*)
---

scripts/fetch.py を実行する。
stdin: 記事一覧JSON
stdout: og_imageフィールド追加済み記事一覧JSON
