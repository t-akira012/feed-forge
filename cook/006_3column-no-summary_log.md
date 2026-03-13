# COOK: スタイル変更（3カラム・概要削除）

## 日付
2026-03-13

## 目的
概要文を削除してトークン節約。3カラムグリッドで一覧性向上。

---

## 実装の流れ

### 1. digest.md 更新
- Generateステップから「要約文（2-3文）」を削除
- 「要約・Markdown生成」→「Markdown生成」にステップ名変更

### 2. CSS 3カラムグリッド化
- `section.level2` にCSS Grid適用（`grid-template-columns: repeat(3, 1fr)`）
- `section.level3` を個別カードとしてスタイリング（白背景、ボーダー、角丸）
- カード内hrを非表示、OGP画像を幅100%に変更
- レスポンシブ対応: 700px以下で2カラム、480px以下で1カラム
- pandocのtitle-block-headerを非表示

### 3. pandoc render.py
- `--section-divs` オプション追加: pandocがh2/h3をsection要素で囲むようになり、CSSグリッドのコンテナ/アイテム構造が成立

### 4. digest-2026-03-13.md
- 全20記事から概要文を削除

---

## 成果物

| ファイル | 内容 |
|---|---|
| `.claude/commands/digest.md` | Generateステップから概要削除 |
| `styles/newspaper_style.css` | 3カラムグリッドレイアウト |
| `skills/pandoc-render/scripts/render.py` | --section-divs追加 |
| `output/digest-2026-03-13.md` | 概要削除版 |
| `dist/digest-2026-03-13.html` | 再レンダリング済み |

## 判断メモ
- --section-divs必須: pandocデフォルトではh2/h3がフラットにbody直下に出力され、CSSグリッドのコンテナ構造が作れないため
- section.level2をグリッドコンテナ、section.level3をグリッドアイテムとして利用
- h2はgrid-column: 1/-1で全幅表示
