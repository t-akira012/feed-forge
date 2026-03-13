---
name: dedup
description: 取得済み記事の重複排除を行う。state/state.jsonと照合し既出URLを除外する。
allowed-tools: Bash(python:*)
---

scripts/dedup.py を実行する。
stdin: 記事一覧JSON
stdout: 既出除外済み記事一覧JSON
副作用: state/state.json を更新
