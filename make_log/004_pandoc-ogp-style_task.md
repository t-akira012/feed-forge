# pandoc出力 + OGP画像 + スタイル改善タスクリスト

## 背景
ダイジェストHTMLにOGP画像を表示し、ビジュアルで記事を識別しやすくする。
画像はローカル保存せず、リモートURLを直接参照する。

## タスク一覧

### 1. OGPフェッチスキル（TDD）
- [x] 1-1. `skills/ogp-fetch/scripts/fetch.py` + テスト（7テスト）
- [x] 1-2. `skills/ogp-fetch/SKILL.md`

### 2. 出力形式更新
- [x] 2-1. Markdown出力にOGP画像参照追加（`![](og_image_url)`）
- [x] 2-2. `styles/newspaper_style.css` 画像サイズ統一（120x80px, object-fit: cover, float:right）
- [x] 2-3. `digest.md` パイプライン更新（9→10ステップ、OGP Fetchステップ5追加）
- [x] 2-4. pandoc render.py変更: --embed-resources廃止→--include-in-headerでCSS埋め込み（画像リモート参照維持）

### 3. テストラン
- [x] 3-1. digest-2026-03-13.md / HTML再生成・ブラウザ確認済み

## 制約
- 画像のローカル保存は一切しない（リモートURL直接参照）
