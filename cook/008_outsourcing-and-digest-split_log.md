# COOK: outsourcing-and-digest-split

## 日付

2026-03-14

## 目的

digestパイプラインのトークン消費削減。データ取得をCodex CLIにアウトソースし、Claude側は加工のみ行う分離アーキテクチャを構築。

---

## 実装の流れ

1. outsourcing skill（TDD: 3テスト → GREEN）
   - dispatch.py: codex exec呼び出し → parcel保存
   - build_prompt: 加工禁止指示を自動付与
   - make_parcel_dir: {base}/{timestamp}/ 構造
2. digest-fetch skill（TDD: 3テスト → GREEN）
   - digest_fetch_helper.py: input_list解析 + 全ソースfetch + category/lang付与
   - fetch_all.py: CLIエントリポイント
3. digest.md更新: Steps 1-2をoutsourcing対応（方法A: codex委託、方法B: 直接実行）
4. E2Eテスト: codex exec → 192記事（4カテゴリ）を55KB JSONで取得成功

---

## 成果物

| ファイル | 内容 |
|---|---|
| skills/outsourcing/scripts/dispatch.py | codex exec発行・parcel保存 |
| skills/outsourcing/SKILL.md | スキル定義 |
| skills/digest_fetch_helper.py | input_list解析・全ソースfetch統合 |
| skills/digest-fetch/scripts/fetch_all.py | CLIエントリポイント |
| skills/digest-fetch/SKILL.md | スキル定義 |
| tests/test_outsourcing.py | 3テスト |
| tests/test_digest_fetch.py | 3テスト |
| .claude/commands/digest.md | fetch phaseをoutsourcing対応に更新 |

## 判断メモ

- codex execのデフォルトtimeout 300sでは14ソース取得に不足。600sに延長
- parcel出力形式はJSON（.md拡張子だが中身はJSON）。codex -oの制約
- 加工フェーズ（Steps 3-10）は未分離。今回はfetchのみ
