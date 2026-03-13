# PROMPTS.md — Claude Code型 自動情報収集・配信システム設計書

## 1. システム概要

`input_list.txt` に宣言的にソース定義を書き、Claude Codeが読み取り、Agent Skills標準のスキルをコネクタとして起動し、自動収集・要約・配信するローカル完結型パイプライン。コネクタは `skills/` 配下にAgent Skills形式（`SKILL.md` + `scripts/`）で配置し、`input_list.txt` の `conecter_type` でスキル名を指定する。

### アーキテクチャ全体像

```
Trigger(launchd/cron)
  → Claude Code起動（カスタムコマンド）
    → input_list.txt読み込み（ソース定義）
    → エントリごとにconecter_typeで対応スキルを特定
    → スキルのscripts/を実行 or Claude Code組み込みツールで取得
    → get_data/block_dataに基づくフィルタリング
    → Dedup: State Storeと照合し既出除外
    → Generate: Claude自身が要約・分類・Markdown/HTML生成
    → Deliver: ローカルファイル / Slack Webhook / メール
    → State更新
```

---

## 2. ディレクトリ構成

```
project-root/
├── .claude/
│   └── commands/
│       └── digest.md              # パイプライン起動カスタムコマンド
├── skills/
│   ├── rss-fetch/                 # RSSフィード取得スキル
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── fetch.py
│   ├── api-fetch/                 # 公式API取得スキル
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── fetch.py
│   ├── scrape-fetch/              # スクレイピング取得スキル
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── fetch.py
│   ├── web-fetch/                 # WebFetch取得スキル（Claude Code組み込み）
│   │   └── SKILL.md
│   ├── web-search/                # WebSearch取得スキル（Claude Code組み込み）
│   │   └── SKILL.md
│   ├── dedup/                     # 重複排除スキル
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── dedup.py
│   └── deliver/                   # 配信スキル
│       ├── SKILL.md
│       └── scripts/
│           └── deliver.py
├── state/
│   └── state.json                 # 既出管理・最終実行時刻
├── output/
│   └── (生成されたMarkdown/HTML)
├── input_list.txt                 # ソース定義
└── PROMPTS.md                     # 本ファイル
```

### ディレクトリ設計方針

- **skills/**: Agent Skills標準準拠。各スキルは独立したディレクトリで、`SKILL.md`（メタデータ+指示）と`scripts/`（実行コード）で構成
- **scripts/を持つスキル（rss-fetch, api-fetch, scrape-fetch, dedup, deliver）**: Pythonスクリプトで確定的に実行。Claude Codeがスキルを起動し、scripts/内のコードをBashで呼び出す
- **scripts/を持たないスキル（web-fetch, web-search）**: SKILL.mdの指示に従い、Claude Code組み込みツール（WebFetch/WebSearch）で実行
- **state/**: 実行状態の永続化。gitignore対象
- **output/**: 生成物の出力先。gitignore対象

---

## 3. input_list.txt 仕様

人間が手書きしやすいテキスト形式。`---` で各エントリを区切る。

### フォーマット

```
---
list: <URL>
conecter_type: <スキル名>
get_data: "<取得したいデータの自然言語指示>"
block_data: "<除外したいデータの自然言語指示>"
---
```

### conecter_type 一覧

| スキル名 | 方式 | 用途 | 実行手段 |
|---|---|---|---|
| web-fetch | Webページ直接取得 | ブロックされにくいサイト | Claude Code WebFetch（SKILL.mdの指示） |
| web-search | キーワード検索で記事発見 | トレンド・話題発見 | Claude Code WebSearch（SKILL.mdの指示） |
| rss-fetch | RSSフィード解析 | 定期更新サイト | scripts/fetch.py（feedparser） |
| api-fetch | 公式API呼び出し | 構造化データ提供サイト | scripts/fetch.py（requests） |
| scrape-fetch | 本文抽出 | RSS要約では不足するサイト | scripts/fetch.py（trafilatura） |

### 記述例

```
---
list: https://news.example.com/rss
conecter_type: rss-fetch
get_data: "投資の記事を取得する"
block_data: "炎上商法の記事は除外する"
---
list: https://arxiv.org/list/cs.AI/recent
conecter_type: web-fetch
get_data: "LLMエージェントに関する新着論文を取得する"
block_data: "画像生成のみの論文は除外する"
---
list: https://example.com/api/v1/articles
conecter_type: api-fetch
get_data: "経済ニュースのヘッドラインを取得する"
block_data: "広告記事は除外する"
---
```

### フィールド補足

- **list**: 取得対象URL。RSSならフィードURL、APIならエンドポイント、WebFetch/WebSearchなら対象ページまたは検索起点URL
- **conecter_type**: スキル名。`skills/` 配下のディレクトリ名と一致する
- **get_data**: Claude Codeへの取得指示。自然言語で「何が欲しいか」を書く
- **block_data**: Claude Codeへの除外指示。自然言語で「何を除くか」を書く。不要なら空文字 `""`

---

## 4. スキル定義

### 4.1 rss-fetch

```markdown
# skills/rss-fetch/SKILL.md
---
name: rss-fetch
description: RSSフィードを解析し記事一覧をJSON形式で出力する。input_list.txtでconecter_type: rss-fetchが指定された場合に使用。
allowed-tools: Bash(python:*)
---

scripts/fetch.py を実行し、引数にURLを渡す。
出力はJSON（stdout）で、各要素は {title, url, published} を含む。
```

```python
# skills/rss-fetch/scripts/fetch.py
import sys, json, feedparser

def main():
    url = sys.argv[1]
    d = feedparser.parse(url)
    items = [
        {"title": e.get("title", ""), "url": e.get("link", ""), "published": e.get("published", "")}
        for e in d.entries[:30]
    ]
    json.dump(items, sys.stdout, ensure_ascii=False)

if __name__ == "__main__":
    main()
```

### 4.2 api-fetch

```markdown
# skills/api-fetch/SKILL.md
---
name: api-fetch
description: 公式APIエンドポイントからJSONデータを取得する。input_list.txtでconecter_type: api-fetchが指定された場合に使用。
allowed-tools: Bash(python:*)
---

scripts/fetch.py を実行し、引数にURLを渡す。
出力はJSON（stdout）。
```

```python
# skills/api-fetch/scripts/fetch.py
import sys, json, requests

def main():
    url = sys.argv[1]
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    # リスト形式でなければラップ
    if not isinstance(data, list):
        data = [data]
    json.dump(data, sys.stdout, ensure_ascii=False)

if __name__ == "__main__":
    main()
```

### 4.3 scrape-fetch

```markdown
# skills/scrape-fetch/SKILL.md
---
name: scrape-fetch
description: Webページから本文を抽出しJSON形式で出力する。input_list.txtでconecter_type: scrape-fetchが指定された場合に使用。
allowed-tools: Bash(python:*)
---

scripts/fetch.py を実行し、引数にURLを渡す。
出力はJSON（stdout）で、各要素は {url, text} を含む。
```

```python
# skills/scrape-fetch/scripts/fetch.py
import sys, json, trafilatura

def main():
    url = sys.argv[1]
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded) or ""
    json.dump([{"url": url, "text": text}], sys.stdout, ensure_ascii=False)

if __name__ == "__main__":
    main()
```

### 4.4 web-fetch（Claude Code組み込み）

```markdown
# skills/web-fetch/SKILL.md
---
name: web-fetch
description: Claude CodeのWebFetchツールでWebページを直接取得する。input_list.txtでconecter_type: web-fetchが指定された場合に使用。
allowed-tools: WebFetch
---

WebFetchツールを使い、指定URLのコンテンツを取得する。
取得したコンテンツからget_dataの指示に従い記事情報を抽出する。
```

### 4.5 web-search（Claude Code組み込み）

```markdown
# skills/web-search/SKILL.md
---
name: web-search
description: Claude CodeのWebSearchツールでキーワード検索し記事を発見する。input_list.txtでconecter_type: web-searchが指定された場合に使用。
allowed-tools: WebSearch
---

WebSearchツールを使い、指定URLを起点にキーワード検索する。
検索結果からget_dataの指示に従い関連記事を抽出する。
```

### 4.6 dedup

```markdown
# skills/dedup/SKILL.md
---
name: dedup
description: 取得済み記事の重複排除を行う。state/state.jsonと照合し既出URLを除外する。
allowed-tools: Bash(python:*)
---

scripts/dedup.py を実行する。
stdin: 記事一覧JSON
stdout: 既出除外済み記事一覧JSON
副作用: state/state.json を更新
```

```python
# skills/dedup/scripts/dedup.py
import sys, json, hashlib, os, time

STATE_PATH = "state/state.json"

def stable_id(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {"seen": {}, "last_run": 0}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def main():
    items = json.load(sys.stdin)
    state = load_state()
    seen = state.get("seen", {})
    ttl = 7 * 86400  # 7日
    now = int(time.time())

    # TTL切れを除去
    seen = {k: v for k, v in seen.items() if now - v < ttl}

    new_items = []
    for item in items:
        url = item.get("url", "")
        if not url:
            continue
        sid = stable_id(url)
        if sid not in seen:
            new_items.append(item)
            seen[sid] = now

    state["seen"] = seen
    state["last_run"] = now
    save_state(state)
    json.dump(new_items, sys.stdout, ensure_ascii=False)

if __name__ == "__main__":
    main()
```

### 4.7 deliver

```markdown
# skills/deliver/SKILL.md
---
name: deliver
description: 生成されたMarkdown/HTMLを配信する。Slack Webhook、メール、ローカルファイル出力に対応。
allowed-tools: Bash(python:*)
---

scripts/deliver.py を実行する。
引数: 配信方式（file / slack / email）、出力ファイルパス or Webhook URL
stdin: 配信するコンテンツ
```

```python
# skills/deliver/scripts/deliver.py
import sys, json, os, requests
from datetime import datetime

def deliver_file(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def deliver_slack(content, webhook_url):
    r = requests.post(webhook_url, json={"text": content}, timeout=20)
    r.raise_for_status()

def main():
    method = sys.argv[1]  # file / slack / email
    target = sys.argv[2]  # パス or URL
    content = sys.stdin.read()

    if method == "file":
        deliver_file(content, target)
    elif method == "slack":
        deliver_slack(content, target)

if __name__ == "__main__":
    main()
```

---

## 5. パイプライン設計

### 5.1 Parse（input_list.txt解析）

- `---` でエントリを分割
- 各エントリからlist, conecter_type, get_data, block_dataを抽出
- conecter_typeでスキルを特定

### 5.2 Fetch（スキル起動による取得）

- conecter_typeがスキル名に対応
- **scripts/を持つスキル**: Claude Codeが `python skills/<name>/scripts/fetch.py <url>` を実行、JSON出力を受け取る
- **scripts/を持たないスキル**: SKILL.mdの指示に従いClaude Code組み込みツールで実行
- 取得失敗時はスキップしてログ記録

### 5.3 Filter（get_data/block_dataによるフィルタリング）

- 取得結果に対し、get_dataの指示に合致する記事を選択
- block_dataの指示に合致する記事を除外
- このフィルタリングはClaude自身が自然言語理解で実行する

### 5.4 Dedup（重複排除）

- dedupスキルを起動: 全取得結果をstdinに流し、既出除外済みをstdoutで受け取る
- state/state.jsonが自動更新される

### 5.5 Generate（要約・分類）

- フィルタ後の記事をClaude自身が要約・分類・Markdown/HTML生成
- 要約文ごとに根拠URLを付与

### 5.6 Deliver（配信）

- deliverスキルを起動: 生成物をstdinに流し、配信方式と宛先を引数で指定

---

## 6. Claude Codeエージェント行動定義

```
launchd/cron → Claude Code起動（.claude/commands/digest.md）
  → input_list.txt読み込み・パース
  → エントリごとにconecter_typeで対応スキルを特定
  → scripts/ありスキル: Bash実行 → JSON取得
  → scripts/なしスキル: WebFetch/WebSearchで取得
  → 全結果マージ
  → get_data指示で選択フィルタ（Claude自然言語処理）
  → block_data指示で除外フィルタ（Claude自然言語処理）
  → dedupスキル起動 → 既出除外
  → Claude自身が要約・分類・Markdown/HTML生成
  → deliverスキル起動 → 配信
```

### 行動定義の原則

- コネクタはAgent Skills標準のスキルとして `skills/` 配下に配置。新しいソース種別はスキル追加で対応
- `input_list.txt` の `conecter_type` がスキル名と1:1対応し、人間は番号ではなく名前で指定する
- scripts/を持つスキルは確定的に実行、Claude組み込みツール系スキルはSKILL.mdの指示で実行
- スキルの追加・削除でパイプライン本体を変更する必要がない

---

## 7. 状態管理

### 段階的拡張

| 段階 | 方式 | 用途 | 移行トリガー |
|---:|---|---|---|
| 1 | JSON | 既出URL、処理済み状態、最終実行時刻 | 起動時の読み込みが遅くなった |
| 2 | SQLite | 既出管理 + TTL(例:7日) + 失敗ログ + スコア履歴 | — |

### state.json構造

```json
{
  "seen": {
    "<SHA256>": 1710288000
  },
  "last_run": 1710288000
}
```

---

## 8. 技術スタック

| 領域 | 推奨 | 備考 |
|---|---|---|
| エージェント | Claude Code | カスタムコマンド + スキル起動 |
| スキル標準 | Agent Skills (agentskills.io) | SKILL.md + scripts/ |
| 入力定義 | input_list.txt | 宣言的テキスト |
| 言語 | Python | scripts/内のコネクタ・ユーティリティ |
| スケジューラ | launchd(macOS) / cron(Linux) | GitHub Actionsも可 |
| 状態管理 | JSON → SQLite | 既出除外・再実行耐性 |
| 配信 | Slack Webhook / SMTP / ローカルMarkdown | deliverスキルで抽象化 |
| LLM | Claude（Claude Code内蔵） | 追加のAPIキー不要 |

---

## 9. 実装ステップ

1. **ディレクトリ構成を作る** — `skills/`, `state/`, `output/`, `.claude/commands/` を配置
2. **スキルを実装する** — 各conecter_typeに対応するSKILL.md + scripts/を作成（本ドキュメントのセクション4を参照）
3. **input_list.txtを書く** — 対象ソース・conecter_type・get_data・block_dataを宣言
4. **カスタムコマンド作成** — `.claude/commands/digest.md` にパイプライン起動指示を記述
5. **テスト整備** — 各スキルのscripts/の単体テスト + dedupの重複排除テスト
6. **スケジューラ設定** — launchd/cronでClaude Codeを定期起動

---

## 10. 品質評価指標

| 指標 | 測定対象 | 用途 |
|---|---|---|
| ROUGE | 参照要約との重なり | 要約の網羅性 |
| BERTScore | 埋め込みベースの類似度 | 意味的な要約品質 |
| QAGS | 生成要約の事実不整合 | 誤情報検出 |
| 根拠URL一致率 | 要約文vs元記事 | 幻覚率の簡易測定 |
| 収集遅延 | Trigger→Deliver間 | パイプライン性能 |
| 失敗率・リトライ回数 | Fetch段 | ソース健全性 |

### コスト見積り近似式

```
コスト ≈ 収集件数 × 平均本文長 × 要約粒度 × LLM単価(入力+出力)
```

---

## 11. 参考実例（Claude Code型）

| 名称 | 構成 | 特徴 |
|---|---|---|
| Claude Codeで朝刊Markdown生成 | launchd + Claude Code + Python | ローカル完結、WebFetch/WebSearch活用、取得手段でグループ分け |
| Claude Code Release Radar | GitHub Actions + Claude/Gemini + Slack | JSON状態管理、日次リリース監視、処理済み状態永続化 |
| claude-rss-news-digest | Python + TF-IDF + Claude + SQLite + Resend | SQLite既出管理(7日TTL)、段階的キュレーション |

---

## 12. スキル拡張ガイド

新しいソース種別を追加する手順:

1. `skills/<new-name>/SKILL.md` を作成（Agent Skills仕様に準拠）
2. 必要に応じて `skills/<new-name>/scripts/` に実行コードを配置
3. `input_list.txt` で `conecter_type: <new-name>` を指定

パイプライン本体（`.claude/commands/digest.md`）の変更は不要。
