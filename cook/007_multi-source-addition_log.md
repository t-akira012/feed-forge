# COOK: multi-source-addition

## 日付

2026-03-14

## 目的

非リベラル・非西側の情報源を追加し、日本/中国/米国/中東の現地情報を収集する。

---

## 実装の流れ

1. input_list.txt に編集方針ヘッダー追記
2. 産経新聞・Global Times・米国4紙・中東4紙のエントリ追加
3. RSS URL疎通確認 → 産経/Arab News/Press TVがブロック・タイムアウト
4. scrape-fetchスキル新規作成（TDD: 3テスト通過）
5. RSS不可ソースの代替対応: 産経→scrape-fetch、Press TV→scrape-fetch、Arab News→Middle East Eye(RSS)、TRT→URL修正

---

## 成果物

| ファイル | 内容 |
|---|---|
| input_list.txt | 14ソース（+10）、編集方針ヘッダー |
| skills/scrape-fetch/SKILL.md | HTMLスクレイピングスキル |
| skills/scrape-fetch/scripts/fetch.py | CLIエントリポイント |
| skills/scrape_fetch_helper.py | スクレイピングロジック |
| tests/test_scrape_fetch.py | 3テスト |

## 判断メモ

- Arab News → Middle East Eye に差し替え（同じく非西側中東メディア、RSSあり）
- 産経・Press TVはRSSブロックのためscrape-fetchで対応
