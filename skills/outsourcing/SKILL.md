---
name: outsourcing
description: Codex CLIにタスクをアウトソースし、結果をparcelディレクトリで受け取る
allowed-tools: Bash(codex:*), Bash(python:*)
---

## 概要

codex exec を使ってタスクを外部エージェントに委託する。結果は `./parcel/{timestamp}/{task-name}.md` に保存される。

## 使い方

```
python3 skills/outsourcing/scripts/dispatch.py <task-name> "<prompt>"
```

## 原則

- Codexには厳密なデータ取得のみを指示する
- 加工・データ削減・フィルタリングはCodexに行わせない
- 加工は次のステップで別エージェント（Claude）が行う
