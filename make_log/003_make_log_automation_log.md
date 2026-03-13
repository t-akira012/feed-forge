# MAKE_LOG: make-log スキル + hook 自動化

## 日付
2026-03-13

## 目的
ADR-001の記録方式をskills+hookで自動化。実装変更があるのにmake_log/未更新の場合、Claudeにリマインドする。

---

## 実装の流れ

### 1. スキル scripts（TDD）

#### next_number.py
- 4テスト一発GREEN: 空ディレクトリ/既存ファイル/非番号ファイル無視/存在しないディレクトリ
- `make_log/` 内の `{NNN}_` プレフィックスから最大番号を検出、+1を返す

#### init_task.py
- 初回RED: `from next_number import next_number` がテスト時にモジュール解決不可
- 修正: next_number関数をインライン化（スクリプト間の相対importを排除）
- GREEN: 3テスト通過（ファイル作成/テンプレート内容/番号インクリメント）

#### write_log.py
- 4テスト一発GREEN: ファイル作成/テンプレート内容/タスク番号と一致/タスク未存在エラー
- タスクファイルの番号を検索して同番号でログファイルを作成

### 2. hook

#### check-make-log.sh
- UserPromptSubmitイベントで実行
- git diff/ls-filesで変更検出 → skills/tests/.claude/等の変更ありかつmake_log/変更なしなら警告
- stdout出力がClaudeのコンテキストに注入される（exit 0）
- 5テスト一発GREEN: 変更なし/変更あり警告/make_log同時変更で無警告/make_logのみ無警告/非gitリポ

#### .claude/settings.json
- UserPromptSubmitフックとして登録

---

## 成果物

| ファイル | 内容 |
|---|---|
| `skills/make-log/SKILL.md` | make-logスキル定義 |
| `skills/make-log/scripts/next_number.py` | 次番号算出 |
| `skills/make-log/scripts/init_task.py` | タスクファイル作成 |
| `skills/make-log/scripts/write_log.py` | ログファイル作成 |
| `.claude/hooks/check-make-log.sh` | 記録漏れ検出hookスクリプト |
| `.claude/settings.json` | hook設定（UserPromptSubmit） |
| `tests/test_make_log.py` | 11テスト |
| `tests/test_check_make_log_hook.py` | 5テスト |

## 判断メモ
- init_task.pyでの相対import排除: テスト時のimportlib動的ロードと相性が悪いため、next_number関数をインライン化
- hookイベントはUserPromptSubmitを選択: stdoutがClaudeコンテキストに注入される唯一のタイミング（Stop等では無視される）
- hookはexit 0（ブロックではなくリマインド）: 強制ブロックは作業フローを阻害するリスクがあるため
- Stopイベントhookは見送り: stdoutがClaudeに届かないため実効性が薄い
