---
name: deliver
description: 生成されたMarkdown/HTMLを配信する。Slack Webhook、メール、ローカルファイル出力に対応。
allowed-tools: Bash(python:*)
---

scripts/deliver.py を実行する。
引数: 配信方式（file / slack / email）、出力ファイルパス or Webhook URL
stdin: 配信するコンテンツ
