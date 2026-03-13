# COOK: translate / ideological-re-education 実装ログ

## 日付
2026-03-13

## 目的
海外情報源を日本語で正確に消費するための2スキル追加。
生成AIのRLHFチューニングによる翻訳歪みを検出・注釈する仕組みの導入。

---

## 実装の流れ

### 1. 設計判断

#### translate
- Claude自然言語処理スキル（SKILL.mdのみ、scripts/なし）に決定
- 理由: 翻訳品質はLLM能力に依存、Pythonスクリプトで外部翻訳APIを使う必要がない
- 原文を `*_original` フィールドに保持し、翻訳後も原文参照可能にする
- 直訳基本。意訳・要約禁止。内容の改変・省略・追加を禁止

#### ideological-re-education
- 同じくClaude自然言語処理スキル（SKILL.mdのみ）
- 翻訳文の修正は行わない。注釈付与のみ（ユーザーが自分で判断する材料を提供）
- 2段階の注釈レベル:
  - `rlhf_warning`: 実際に歪みを検出した場合
  - `rlhf_caution`: 感応トピックだが歪み未検出の場合
- 検出基準: 意味の追加/省略/トーンの変化/トピックの敏感性

### 2. input_list.txt 拡張
- `lang` フィールドを新設。未指定 or `ja` なら翻訳スキップ
- Hacker News RSS (`lang: en`) を実例として追加

### 3. パイプライン拡張
- digest.md を 6ステップ → 8ステップに拡張
- ステップ5: Translate（lang指定ありの記事のみ）
- ステップ6: Ideological Re-education（翻訳済み記事のみ）
- ステップ7: Generate（rlhf_warning/rlhf_caution をMarkdownに表示）
- ステップ8: Deliver

### 4. テスト
- SKILL.mdの構造検証テスト（scripts/がないスキルのTDD手法）
- translate: 8テスト（ファイル存在、frontmatter、入出力セクション、原文保持、改変禁止ポリシー、scripts/不在）
- ideological-re-education: 9テスト（ファイル存在、frontmatter、warning/cautionフィールド、修正禁止、検出基準3項目、JSON例、scripts/不在）
- 全27テスト GREEN（既存10 + 新規17）

---

## 成果物

| ファイル | 内容 |
|---|---|
| `skills/translate/SKILL.md` | 翻訳スキル定義（直訳方針、原文保持） |
| `skills/ideological-re-education/SKILL.md` | RLHF歪み検出・注釈スキル定義 |
| `.claude/commands/digest.md` | パイプライン更新（6→8ステップ） |
| `input_list.txt` | Hacker News追加、langフィールド対応 |
| `tests/test_translate_skill.py` | 8テスト |
| `tests/test_reeducation_skill.py` | 9テスト |

## 判断メモ
- 両スキルともscripts/なし: 翻訳もRLHF検出もClaude自身の言語能力で実行するため、Pythonスクリプトは不要
- SKILL.mdのみスキルのTDD手法: 構造・必須セクション・ポリシー文言の存在を自動検証
- ideological-re-educationは翻訳修正しない設計: ユーザーの判断を尊重し、情報を歪めず注釈で補助
- rlhf_warning vs rlhf_caution の2段階: 確度の違いをユーザーに伝えるため
