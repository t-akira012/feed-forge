# COOK: はてなブックマーク実装ログ

## 日付
2026-03-13

## 対象
https://b.hatena.ne.jp/hotentry/it.rss（ITカテゴリのホットエントリRSS）

---

## 実装の流れ

### 1. 初期状態の確認
- リポジトリにはPROMPTS.md（設計書）のみ存在
- .gitignore、ディレクトリ構成、スキル、テストすべて未作成

### 2. タスクリスト作成 → hatebu_task.md
- はてブはRSSフィードを提供しているため `rss-fetch` コネクタを採用
- 必要スキルを rss-fetch / dedup / deliver の3つに絞り込み
- deliver は file 方式（ローカルMarkdown出力）のみに限定

### 3. プロジェクト基盤
- `.gitignore` 作成（state/, output/, __pycache__/, .pytest_cache/）
- ディレクトリ構成作成: skills/, state/, output/, .claude/commands/, tests/

### 4. スキル実装（TDD）

#### 4-1. rss-fetch
- **RED**: テスト作成 → `importlib.util` でfetch.pyを動的ロードし feedparser をモック
- **つまずき**: `if __name__ == "__main__"` ガードにより `main()` が呼ばれない問題
  - exec_module時の `__name__` は "fetch"（"__main__" ではない）
  - → テスト側で `mod.main()` を明示呼び出しに修正
- **GREEN**: 3テスト通過（空フィード / 単一エントリ / 30件上限）
- 実装: PROMPTS.md仕様通り feedparser.parse → entries[:30] → JSON出力

#### 4-2. dedup
- **RED→GREEN**: 5テスト一発通過
  - 全新規 / 2回目重複排除 / 新旧混在 / 空URL除外 / state.json生成確認
- 実装: SHA256ハッシュ + 7日TTL + state.json永続化

#### 4-3. deliver
- **RED→GREEN**: 2テスト一発通過
  - ファイル出力 / 親ディレクトリ自動作成
- 実装: file方式のみ（YAGNI: slack/emailは未実装）

### 5. パイプライン定義
- `input_list.txt`: はてブITホットエントリRSSを記述
- `.claude/commands/digest.md`: Parse→Fetch→Filter→Dedup→Generate→Deliverの6段パイプライン

### 6. 全テスト実行
- 10テスト全GREEN確認

---

## 成果物

| ファイル | 内容 |
|---|---|
| `.gitignore` | state/, output/, __pycache__/ 等 |
| `skills/rss-fetch/SKILL.md` | RSSフィードスキル定義 |
| `skills/rss-fetch/scripts/fetch.py` | feedparserでRSS取得→JSON出力 |
| `skills/dedup/SKILL.md` | 重複排除スキル定義 |
| `skills/dedup/scripts/dedup.py` | SHA256ベース重複排除（7日TTL） |
| `skills/deliver/SKILL.md` | 配信スキル定義 |
| `skills/deliver/scripts/deliver.py` | ファイル出力 |
| `tests/test_rss_fetch.py` | 3テスト |
| `tests/test_dedup.py` | 5テスト |
| `tests/test_deliver.py` | 2テスト |
| `input_list.txt` | はてブRSSエントリ定義 |
| `.claude/commands/digest.md` | パイプライン起動カスタムコマンド |
| `hatebu_task.md` | タスクリスト（全完了） |

## 依存パッケージ
- feedparser
- pytest（テスト用）

## 判断メモ
- はてブはRSS提供済み → web-fetch/scrape-fetchは不要
- deliver は file のみ → slack/email は必要になってから実装（YAGNI）
- web-fetch, web-search, api-fetch, scrape-fetch スキルは未実装（今回不要）
