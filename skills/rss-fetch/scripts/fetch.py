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
