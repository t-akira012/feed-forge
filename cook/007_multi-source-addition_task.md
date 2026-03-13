# multi-source-addition 実装タスクリスト

## 背景

非リベラル・非西側の情報源を追加し、日本/中国/米国/中東の現地情報を収集する。

## タスク一覧

- [x] input_list.txt にヘッダー（編集方針）を追記
- [x] 産経新聞・Global Times・米国4紙・中東4紙のエントリを追加
- [x] RSS URL疎通確認
- [x] scrape-fetchスキル新規作成（TDD: 3テスト通過）
- [x] 産経→scrape-fetch、Press TV→scrape-fetch、Arab News→Middle East Eye(RSS代替)、TRT→URL修正
- [ ] /digest 実行で全ソース取得を検証

## 補足

- RSS取得不可: 産経（ブロック）、Arab News（403）、Press TV（タイムアウト）
- Arab News → Middle East Eye に差し替え（同じく非西側中東メディア）
