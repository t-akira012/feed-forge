import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from skills.digest_fetch_helper import parse_input_list, fetch_all_sources


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input_list.txt"
    with open(input_file, "r") as f:
        text = f.read()

    entries = parse_input_list(text)
    articles = fetch_all_sources(entries)
    json.dump(articles, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
