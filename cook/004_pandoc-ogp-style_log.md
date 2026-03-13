# COOK: pandoc出力 + OGP画像 + スタイル改善

## 日付
2026-03-13

## 目的
ダイジェストHTMLにOGP画像を表示し、新聞風スタイルでレンダリングする。画像はローカル保存せずリモートURL直接参照。

---

## 実装の流れ

### 1. OGPフェッチスキル（TDD）

#### ogp-fetch/scripts/fetch.py
- 7テストGREEN: og:image抽出（property→content順/content→property順）/画像なし/取得失敗/複数記事処理/stdin入出力
- regex 2パターンで `<meta property="og:image" content="...">` と属性逆順の両方に対応
- requests.get + タイムアウト10秒、失敗時は空文字

### 2. pandoc-renderスキル

#### render.py
- 初回: `--embed-resources` でリモート画像がローカルにダウンロード・埋め込まれる問題発生
- 修正: `--include-in-header` + 一時ファイルでCSS埋め込み、`--embed-resources` 削除
- 6テストGREEN: HTML生成/CSS埋め込み/出力ディレクトリ自動作成/CLI実行/存在しないファイルエラー/pandocコマンド引数検証

### 3. Markdown出力形式

- `![OGP](url)` 形式で画像行を追加（alt text "OGP" 必須: pandocがimg要素として出力するため）
- 画像行は必ず空行で囲む（pandocがfigure要素として認識するため）
- OGP画像なしの記事は1x1透明GIF data URIをプレースホルダとして使用

### 4. CSSスタイル（newspaper_style.css）

- figure: float:right, 140x90px, min-height設定（プレースホルダ用）, background:#eee
- object-fit:cover で画像サイズ統一
- figcaption非表示
- hr clear:both でフロート解除

---

## 成果物

| ファイル | 内容 |
|---|---|
| `skills/ogp-fetch/SKILL.md` | OGPフェッチスキル定義 |
| `skills/ogp-fetch/scripts/fetch.py` | OGP画像URL抽出 |
| `skills/pandoc-render/SKILL.md` | pandocレンダースキル定義 |
| `skills/pandoc-render/scripts/render.py` | pandoc HTML変換 |
| `styles/newspaper_style.css` | 新聞風CSSスタイル |
| `tests/test_ogp_fetch.py` | 7テスト |
| `tests/test_pandoc_render.py` | 6テスト |
| `adr/002_pandoc_html_render.md` | ADR-002 |

## 判断メモ
- --embed-resources廃止: リモート画像のローカルダウンロードはユーザー要件「画像はローカル保存しない」に反するため
- --include-in-headerでCSS埋め込み: --cssだと外部ファイル参照になり配信時にCSS別送が必要になるため
- プレースホルダはdata URI: 1x1透明GIFでCSSのmin-heightとbackgroundで視覚的に空白領域を確保
- float:rightレイアウト: 画像横に概要テキストを流し込むため（下に折り返さない）
