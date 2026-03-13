# cook スキル + hook 自動化タスクリスト

## 目的
ADR-001（実装タスクと結果の記録方式）をskills+hookで自動化し、記録漏れを防止する。

## 設計

### skill: cook
- `scripts/next_number.py` — cook/の最大番号+1を返す
- `scripts/init_task.py <name>` — テンプレート付きタスクファイル作成
- `scripts/write_log.py <name>` — テンプレート付きログファイル作成

### hook: UserPromptSubmit
- 毎プロンプト送信時に `git status` で変更を検出
- cook/ 以外のファイルが変更されているのに cook/ の変更がない場合、Claudeのコンテキストにリマインダーを注入
- taskファイルに対応するlogファイルが未作成の場合、警告を注入
- stdout出力 → Claudeが認識

## タスク一覧

### 1. スキル実装（TDD）
- [x] 1-1. `scripts/next_number.py` + テスト（4テスト）
- [x] 1-2. `scripts/init_task.py` + テスト（3テスト）
- [x] 1-3. `scripts/write_log.py` + テスト（4テスト）
- [x] 1-4. `skills/cook/SKILL.md` 作成

### 2. hook実装
- [x] 2-1. `.claude/hooks/check-cook.sh` 作成 + テスト（7テスト）
- [x] 2-2. `.claude/settings.json` にhook設定追加（UserPromptSubmit）

### 3. 動作確認
- [x] 3-1. 全テスト GREEN
