import json, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from skills.scrape_fetch_helper import fetch


def main():
    url = sys.argv[1]
    items = fetch(url)
    json.dump(items, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
