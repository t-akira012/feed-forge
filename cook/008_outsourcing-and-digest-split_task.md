# outsourcing-and-digest-split 実装タスクリスト

## 背景

digestパイプラインのトークン消費が大きすぎる。データ取得をCodex CLIにアウトソースし、Claude側は加工のみ行う分離アーキテクチャを構築する。

## タスク一覧

- [x] outsourcing skill 作成（TDD）
  - [x] tests/test_outsourcing.py — テスト先行
  - [x] skills/outsourcing/scripts/dispatch.py — codex exec発行 → parcel保存
  - [x] skills/outsourcing/SKILL.md
- [x] digest-fetch 作成（TDD）
  - [x] tests/test_digest_fetch.py — テスト先行
  - [x] skills/digest-fetch/scripts/fetch_all.py — input_list解析+全ソースfetch+JSON統合
  - [x] skills/digest-fetch/SKILL.md
- [x] digest.md を更新（fetch phaseをparcel経由に変更）
- [x] codex exec でデータ取得アウトソースのE2Eテスト
- [x] cook log 作成

## 補足

- parcel構造: `./parcel/{timestamp}/{task-name}.md`
- Codexへの指示: 厳密なデータ取得のみ。自己判断で加工・削減しない
- コンテナ環境: approvals bypass可
