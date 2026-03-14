# COOK: digest-process-phase

## 日付

2026-03-14

## 目的

outsourcingで取得したparcelデータの加工フェーズ実行。dispatch.pyの.json拡張子対応。

---

## 実装の流れ

1. dispatch.py に ext パラメータ追加（TDD: 2テスト追加 → GREEN）
2. parcel/2026-03-14-17-32-56/digest-fetch.md (192記事) を読み込み
3. Step 3 Filter: 192→187 (5件除外: 広告PR, ゲーム, スポーツ)
4. Step 4 Dedup: 187→126 (61件既出)
5. Step 5 OGP: 71/126にOGP画像取得
6. Step 6 Translate: 99件EN→JA翻訳完了（Unicode正規化で全件マッチ）
7. Step 7 RLHF: 58件にcaution付与
8. Step 8 Generate: 892行のMarkdown生成（ITはsubcategory分類）
9. Step 9 Deliver: output/digest-2026-03-14.md (67KB)
10. Step 10 Render: dist/digest-2026-03-14.html (99KB)

---

## 成果物

| ファイル | 内容 |
|---|---|
| output/digest-2026-03-14.md | Markdown digest (126記事) |
| dist/digest-2026-03-14.html | HTML版 |
| skills/outsourcing/scripts/dispatch.py | ext パラメータ追加 |
| tests/test_outsourcing.py | 2テスト追加（計5件） |

## 判断メモ

- digest-processスキルのスクリプト化は見送り。NLUステップが大半でスクリプト化の利点が薄い
- Unicode smart quotes ('') と \xa0 がRSSタイトルに混入。正規化で解決
- 加工フェーズのトークン消費は依然大きい（翻訳99件）が、fetchのoutsourcingで改善
