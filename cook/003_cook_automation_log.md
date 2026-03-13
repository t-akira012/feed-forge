# COOK: cook スキル + hook 自動化

## 日付
2026-03-13

## 目的
ADR-001の記録方式をskills+hookで自動化。実装変更があるのにcook/未更新の場合、Claudeにリマインドする。taskに対応するlogが未作成の場合も警告する。

---

## 実装の流れ

### 1. スキル scripts（TDD）

#### next_number.py
- 4テスト一発GREEN: 空ディレクトリ/既存ファイル/非番号ファイル無視/存在しないディレクトリ
- `cook/` 内の `{NNN}_` プレフィックスから最大番号を検出、+1を返す

#### init_task.py
- 初回RED: `from next_number import next_number` がテスト時にモジュール解決不可
- 修正: next_number関数をインライン化（スクリプト間の相対importを排除）
- GREEN: 3テスト通過（ファイル作成/テンプレート内容/番号インクリメント）

#### write_log.py
- 4テスト一発GREEN: ファイル作成/テンプレート内容/タスク番号と一致/タスク未存在エラー
- タスクファイルの番号を検索して同番号でログファイルを作成

### 2. hook

#### check-cook.sh
- UserPromptSubmitイベントで実行
- git diff/ls-filesで変更検出 → skills/tests/.claude/等の変更ありかつcook/変更なしなら警告
- cook/内のtaskファイルを走査し、対応するlogファイルが存在しない場合に警告
- stdout出力がClaudeのコンテキストに注入される（exit 0）
- 7テストGREEN: 変更なし/変更あり警告/cook同時変更で無警告/cookのみ無警告/非gitリポ/log欠落警告/ペア揃い無警告

#### .claude/settings.json
- UserPromptSubmitフックとして登録

---

## 成果物

| ファイル | 内容 |
|---|---|
| `skills/cook/SKILL.md` | cookスキル定義 |
| `skills/cook/scripts/next_number.py` | 次番号算出 |
| `skills/cook/scripts/init_task.py` | タスクファイル作成 |
| `skills/cook/scripts/write_log.py` | ログファイル作成 |
| `.claude/hooks/check-cook.sh` | 記録漏れ検出 + logファイル欠落検出hookスクリプト |
| `.claude/settings.json` | hook設定（UserPromptSubmit） |
| `tests/test_cook.py` | 11テスト |
| `tests/test_check_cook_hook.py` | 7テスト |

## 判断メモ
- init_task.pyでの相対import排除: テスト時のimportlib動的ロードと相性が悪いため、next_number関数をインライン化
- hookイベントはUserPromptSubmitを選択: stdoutがClaudeコンテキストに注入される唯一のタイミング（Stop等では無視される）
- hookはexit 0（ブロックではなくリマインド）: 強制ブロックは作業フローを阻害するリスクがあるため
- Stopイベントhookは見送り: stdoutがClaudeに届かないため実効性が薄い
