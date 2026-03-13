---
name: cook
description: 実装タスクと結果をcook/に記録する。ADR-001準拠。タスクファイルとログファイルを対で管理する。
allowed-tools: Bash(python:*)
---

## 使い方

### タスクファイル作成（実装開始前）
```
python skills/cook/scripts/init_task.py cook <name>
```
`cook/{NNN}_{name}_task.md` が作成される。内容を編集してタスク一覧を記入する。

### ログファイル作成（実装完了後）
```
python skills/cook/scripts/write_log.py cook <name>
```
対応するタスクファイルの番号を検出し、`cook/{NNN}_{name}_log.md` が作成される。内容を編集して実装ログを記入する。

### 次の番号確認
```
python skills/cook/scripts/next_number.py cook
```
