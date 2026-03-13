---
name: pandoc-render
description: MarkdownファイルをpandocでHTML化する。styles/newspaper_style.cssを埋め込んだスタンドアロンHTMLを出力。
allowed-tools: Bash(python:*)
---

scripts/render.py を実行する。
引数: 入力Markdownパス、出力HTMLパス
CSSは styles/newspaper_style.css をインライン埋め込みする。
