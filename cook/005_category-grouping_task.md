# category フィールド追加・カテゴリ別出力タスクリスト

## 背景
現状のGenerateステップではClaude が記事内容からカテゴリを推測して分類している。
ユーザーが `input_list.txt` で明示的にカテゴリを宣言し、出力をカテゴリ単位でグループ化する。

## タスク一覧

### 1. 仕様変更
- [x] 1-1. `input_list.txt` に category フィールド追加（はてブ/HN共にIT）
- [x] 1-2. `digest.md` Parse/Fetch/Generate ステップ更新
- [x] 1-3. ADR-003 作成

### 2. 動作確認
- [x] 2-1. 全59テスト GREEN
