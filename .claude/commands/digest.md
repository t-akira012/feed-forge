以下のパイプラインを順番に実行せよ。

## 1. Parse — input_list.txt解析

`input_list.txt` を読み込み、`---` でエントリを分割する。各エントリから list, conecter_type, get_data, block_data, lang を抽出する。

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

## 5. OGP Fetch — OGP画像URL取得

dedup後の記事一覧に対しogp-fetchスキルを起動:
```
echo '<JSON>' | python skills/ogp-fetch/scripts/fetch.py
```
各記事にog_imageフィールドが追加される。画像はローカル保存しない。

## 6. Translate — 翻訳（外国語ソースのみ）

エントリに `lang` フィールドが指定されている場合（`lang: en` 等）、そのエントリ由来の記事に対し `skills/translate/SKILL.md` の指示に従い日本語翻訳を実行する。

- 原文を *_original フィールドに保持したまま、title / text / summary を日本語に置換
- `lang` が未指定または `ja` の記事はスキップ

## 7. Ideological Re-education — RLHF歪み検出

ステップ6で翻訳された記事に対し、`skills/ideological-re-education/SKILL.md` の指示に従い原文と翻訳を比較する。

- RLHF安全チューニングによる意味変容の可能性を検出
- `rlhf_warning`（歪み検出時）または `rlhf_caution`（感応トピック時）フィールドを付与
- 翻訳文の修正は行わない。注釈の付与のみ

## 8. Generate — 要約・Markdown生成

新着記事を以下の形式でMarkdownにまとめる。タイトルにリンクを埋め込み、OGP画像があれば表示する:

```markdown
# Daily Digest — YYYY-MM-DD

## カテゴリ名

### [記事タイトル](URL)

![OGP](og_image_url)

要約文（2-3文）

⚠️ RLHF Warning: （rlhf_warningがある場合のみ表示）
ℹ️ RLHF Caution: （rlhf_cautionがある場合のみ表示）

---
```

- **画像行は必ず空行で囲む**（pandocがfigure要素として認識するため）
- **alt textに "OGP" を指定する**（pandocがimg要素として出力するため必須）
- og_imageが空の記事はプレースホルダ画像を使用: `![OGP](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)`
- 記事が0件の場合は「新着記事はありません」と出力する

## 9. Deliver — 配信

生成したMarkdownを以下で配信:
```
echo '<Markdown>' | python skills/deliver/scripts/deliver.py file output/digest-YYYY-MM-DD.md
```

## 10. Render — HTML変換

pandoc-renderスキルを起動し、MarkdownをHTML化する:
```
python skills/pandoc-render/scripts/render.py output/digest-YYYY-MM-DD.md dist/digest-YYYY-MM-DD.html
```
