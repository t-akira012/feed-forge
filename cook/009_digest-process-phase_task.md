# digest-process-phase 実装タスクリスト

## 背景

outsourcingで取得したデータの加工フェーズを整備し、実際に処理を実行する。

## タスク一覧

- [x] dispatch.py を .json 拡張子対応に修正
- [x] digest.md 更新（fetch phaseをoutsourcing対応に変更済み）
- [x] 加工実行（parcel/2026-03-14-17-32-56/digest-fetch.md → Steps 3-10）
- [x] cook log 作成

## 補足

- 機械的ステップ (4: dedup, 5: OGP, 9: deliver, 10: render) はスクリプト実行
- NLUステップ (3: filter, 6: translate, 7: RLHF, 8: generate) はClaude直接実行
- digest-processスキルは不要と判断（NLUステップが多くスクリプト化の利点が薄い）
