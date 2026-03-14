---
name: digest-fetch
description: input_list.txtの全ソースからデータを取得し、統合JSONを出力する
allowed-tools: Bash(python:*)
---

## 概要

input_list.txt を解析し、各エントリのconnecter_typeに対応するfetchスキルを実行。結果を1つのJSON配列に統合して標準出力に出力する。

## 使い方

```
python3 skills/digest-fetch/scripts/fetch_all.py [input_list.txt]
```

## 出力

```json
[{"title": "...", "url": "...", "published": "...", "category": "IT", "lang": "en"}, ...]
```
