# COOK: categoryフィールド追加・カテゴリ別出力

## 日付
2026-03-13

## 目的
input_list.txtにcategoryフィールドを追加し、出力をカテゴリ単位でグループ化する。Claude推測ではなくユーザー宣言によるカテゴリ体系。

---

## 実装の流れ

### 1. input_list.txt 変更
- `category: IT` を はてブ/HN 両エントリに追加
- 既存フィールド（list, conecter_type, get_data, block_data, lang）に並列して配置

### 2. digest.md パイプライン更新
- Parseステップ: category抽出を明記
- Fetchステップ: 取得した各記事JSONにcategoryフィールドを付与
- Generateステップ: categoryフィールドでグループ化、`## カテゴリ名` はユーザー宣言値をそのまま使用、ソース単位の分類は不要

### 3. ADR-003 作成
- categoryフィールドの仕様・グループ化ルール・背景を記録

---

## 成果物

| ファイル | 内容 |
|---|---|
| `input_list.txt` | categoryフィールド追加 |
| `.claude/commands/digest.md` | Parse/Fetch/Generate更新 |
| `adr/003_category_field.md` | ADR-003 |

## 判断メモ
- コード変更なし（スキル/テスト追加不要）: categoryはパイプライン仕様の変更であり、実装はClaude自身の振る舞い変更のみ
- 全59テストGREEN: 既存機能への影響なし
