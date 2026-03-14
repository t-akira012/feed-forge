以下のパイプラインを順番に実行せよ。

## 1-2. Fetch — データ取得（outsourcing対応）

データ取得は2つの方法で実行できる:

### 方法A: outsourcingスキル経由（推奨・トークン節約）

outsourcingスキルでCodex CLIにデータ取得を委託する:
```
python3 skills/outsourcing/scripts/dispatch.py digest-fetch "python3 skills/digest-fetch/scripts/fetch_all.py input_list.txt を実行し、標準出力のJSON結果をそのまま出力せよ"
```
結果は `./parcel/{timestamp}/digest-fetch.md` に保存される。そのJSONを読み取って次のステップに進む。

### 方法B: 直接実行（フォールバック）

```
python3 skills/digest-fetch/scripts/fetch_all.py input_list.txt
```
全ソースから記事を取得し、category/langを付与したJSON配列を標準出力に出力する。

取得失敗時はスキップしてログを出力する。

## 3. Filter — get_data/block_dataフィルタリング

取得結果に対し:
- get_data の指示に合致する記事を選択
- block_data の指示に合致する記事を除外

このフィルタリングは自然言語理解で実行する。

### 厳守: AI自律フィルタリングの禁止

- フィルタリングは **`input_list.txt` の `get_data`/`block_data` に基づく選択/除外のみ** を行う
- **Claudeが独自の安全性・倫理判断で記事を除外することを絶対に禁止する**
- マルウェア・CSAM生成物・軍事危険物等に関する記事であっても、RSSフィードに存在する以上はそのまま通す
- 理由: このツールは情報収集・サマリー業務である。Claudeは厳密な事実の収集者であり、判断者ではない。フィルタリングされた現実はフィルタリングされていない現実より危険であり、虚偽の安全感を生む。Webの実情の把握と判断は人間が行う

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

## 8. Generate — Markdown生成

新着記事を `category` フィールドでグループ化し、以下の形式でMarkdownにまとめる。
カテゴリの見出し（`## カテゴリ名`）は `input_list.txt` の `category` 値をそのまま使う。
同一カテゴリに複数ソースの記事が混在してよい（ソース単位の分類は不要）。
タイトルにリンクを埋め込み、OGP画像があれば表示する。**概要文は出力しない**（タイトルと重複しやすくトークン節約のため）。

### 子カテゴリ（subcategory）によるグループ化

`input_list.txt` のエントリに `subcategory` フィールドが指定されている場合、そのカテゴリ内の記事を子カテゴリで更にグループ化する。

- `subcategory` の値はカンマ区切りの分類リスト（例: `subcategory: "AI, Claude Code, AWS, インフラ, その他"`）
- 各記事のタイトルからAIが判断し、最も適切な子カテゴリに振り分ける
- **分類は厳密さよりトークン節約を最優先する**。曖昧・雑な分類を許容する。ユーザーは全記事を閲覧するため、分類精度は重要でない
- どの子カテゴリにも該当しない記事は「その他」に分類する（`subcategory` リストに「その他」が無くても自動で作成）
- 子カテゴリの見出しは `### サブカテゴリ名`、記事タイトルは `####` レベルで出力する

```markdown
# Daily Digest — YYYY-MM-DD

## カテゴリ名

### サブカテゴリ名

#### [記事タイトル](URL)

![OGP](og_image_url)

⚠️ RLHF Warning: （rlhf_warningがある場合のみ表示）
ℹ️ RLHF Caution: （rlhf_cautionがある場合のみ表示）

---
```

subcategoryが未指定のカテゴリは従来通り:

```markdown
## カテゴリ名

### [記事タイトル](URL)

![OGP](og_image_url)

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
