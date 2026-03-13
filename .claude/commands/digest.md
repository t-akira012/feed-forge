以下のパイプラインを順番に実行せよ。

## 1. Parse — input_list.txt解析

`input_list.txt` を読み込み、`---` でエントリを分割する。各エントリから list, conecter_type, get_data, block_data を抽出する。

## 2. Fetch — スキル起動による取得

各エントリについて conecter_type に対応するスキルを起動する:
- `rss-fetch`: `python skills/rss-fetch/scripts/fetch.py <URL>` を実行しJSON取得
- `api-fetch`: `python skills/api-fetch/scripts/fetch.py <URL>` を実行しJSON取得
- `scrape-fetch`: `python skills/scrape-fetch/scripts/fetch.py <URL>` を実行しJSON取得
- `web-fetch`: WebFetchツールでURLのコンテンツを取得し、記事情報をJSON形式に整形
- `web-search`: WebSearchツールでURLを起点に検索し、記事情報をJSON形式に整形

取得失敗時はスキップしてログを出力する。

## 3. Filter — get_data/block_dataフィルタリング

取得結果に対し:
- get_data の指示に合致する記事を選択
- block_data の指示に合致する記事を除外

このフィルタリングは自然言語理解で実行する。

## 4. Dedup — 重複排除

フィルタ後の全記事をJSON形式にまとめ、以下を実行:
```
echo '<JSON>' | python skills/dedup/scripts/dedup.py
```
既出除外済みの記事一覧を受け取る。

## 5. Generate — 要約・Markdown生成

新着記事を以下の形式でMarkdownにまとめる:

```markdown
# Daily Digest — YYYY-MM-DD

## カテゴリ名

### 記事タイトル
要約文（2-3文）
🔗 [元記事](URL)

---
```

記事が0件の場合は「新着記事はありません」と出力する。

## 6. Deliver — 配信

生成したMarkdownを以下で配信:
```
echo '<Markdown>' | python skills/deliver/scripts/deliver.py file output/digest-YYYY-MM-DD.md
```
