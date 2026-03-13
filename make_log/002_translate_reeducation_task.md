# translate / ideological-re-education スキル実装タスクリスト

## 背景
海外情報源を日本語で消費する際、2つの問題がある:
1. 言語の壁 → translate で解決
2. 生成AIのRLHF安全チューニングによる翻訳歪み → ideological-re-education で検出・注釈

## スキル設計

### translate
- Claude自然言語処理で翻訳（scripts/なし、SKILL.mdのみ）
- パイプライン上の位置: Filter後、Generate前
- 入力: 記事JSON（title, url, text/summary等）
- 出力: 原文フィールド保持 + 日本語翻訳フィールド追加

### ideological-re-education
- Claude自然言語処理で原文と翻訳を比較（scripts/なし、SKILL.mdのみ）
- パイプライン上の位置: translate後、Generate前
- 原文と翻訳文を比較し、RLHF的安全制約による意味変容の可能性を検出
- 翻訳文は修正しない。注釈を付与するのみ

## タスク一覧

### 1. スキル定義
- [x] 1-1. `skills/translate/SKILL.md` 作成
- [x] 1-2. `skills/ideological-re-education/SKILL.md` 作成

### 2. パイプライン更新
- [x] 2-1. `.claude/commands/digest.md` にTranslate・Re-educationステップ追加（6→8ステップ）
- [x] 2-2. `input_list.txt` にlang フィールド対応（Hacker Newsをen例として追加）

### 3. 動作確認用テスト
- [x] 3-1. translate指示の検証テスト（8テスト）
- [x] 3-2. ideological-re-education指示の検証テスト（9テスト）

## 補足
- 両スキルともClaude自然言語処理（SKILL.mdのみ、scripts/なし）
- input_list.txt に `lang` フィールド追加で翻訳要否を判定
