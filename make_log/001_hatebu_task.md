# はてなブックマーク実装タスクリスト

## 対象URL
- https://b.hatena.ne.jp/hotentry/it.rss （ITカテゴリのホットエントリRSS）

## 使用コネクタ
- `rss-fetch` — はてブはRSSフィードを提供しているため

## タスク一覧

### 1. プロジェクト基盤
- [x] 1-1. `.gitignore` 作成（state/, output/）
- [x] 1-2. ディレクトリ構成作成（skills/, state/, output/, .claude/commands/）

### 2. スキル実装（TDD）
- [x] 2-1. `skills/rss-fetch/` — SKILL.md + scripts/fetch.py + テスト
- [x] 2-2. `skills/dedup/` — SKILL.md + scripts/dedup.py + テスト
- [x] 2-3. `skills/deliver/` — SKILL.md + scripts/deliver.py + テスト

### 3. パイプライン定義
- [x] 3-1. `input_list.txt` — はてブRSSエントリを記述
- [x] 3-2. `.claude/commands/digest.md` — パイプライン起動カスタムコマンド

### 4. 動作確認
- [x] 4-1. 全テスト実行・GREEN確認

## 補足
- web-fetch, web-search, api-fetch, scrape-fetch は今回不要（はてブはRSSで十分）
- deliver は `file` 方式（ローカルMarkdown出力）のみ実装
- Python依存: feedparser
