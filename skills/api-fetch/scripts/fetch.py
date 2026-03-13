import sys, json, requests


ZENN_BASE = "https://zenn.dev"


def main():
    url = sys.argv[1]
    resp = requests.get(url, timeout=30)
    data = resp.json()
    articles = data.get("articles", [])[:30]
    items = [
        {
            "title": a.get("title", ""),
            "url": ZENN_BASE + a.get("path", ""),
            "published": a.get("published_at", ""),
        }
        for a in articles
    ]
    json.dump(items, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
