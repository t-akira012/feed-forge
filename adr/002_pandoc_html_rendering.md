# ADR-002: pandocによるHTML出力とスタイル定義

## ステータス
承認済み (2026-03-13)

## コンテキスト
Markdownダイジェストを人間が快適に読める形式で提供する必要がある。ブラウザで閲覧可能なHTML出力が望ましい。

## 決定

### 出力パイプライン
```
output/*.md → pandoc → dist/*.html
```

### Markdown出力形式
- 記事タイトルにリンクを埋め込む: `### [タイトル](URL)`
- 旧形式の `🔗 [元記事](URL)` 行は廃止

### HTML変換
- pandoc `--standalone --embed-resources` でCSS埋め込みのスタンドアロンHTML生成
- スタイルは `styles/newspaper_style.css`（新聞風明朝体デザイン）
- `skills/pandoc-render/` スキルとして実装、`scripts/render.py` でワンライナーCLI実行

### ディレクトリ
| パス | 内容 | git |
|---|---|---|
| `styles/newspaper_style.css` | CSSスタイル定義 | tracked |
| `output/*.md` | Markdownダイジェスト | ignored |
| `dist/*.html` | HTML出力 | ignored |

## 結果
- ブラウザで即座に閲覧可能なスタンドアロンHTML
- CSS変更でスタイル調整が容易
- パイプラインのステップ9として自動実行
