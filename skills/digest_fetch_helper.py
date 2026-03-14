import json
import subprocess
import sys
import re


FETCH_SCRIPTS = {
    "rss-fetch": "skills/rss-fetch/scripts/fetch.py",
    "api-fetch": "skills/api-fetch/scripts/fetch.py",
    "scrape-fetch": "skills/scrape-fetch/scripts/fetch.py",
}


def parse_input_list(text):
    blocks = text.split("---")
    entries = []
    for block in blocks:
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        entry = {}
        for line in block.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r'^(\w+):\s*"?(.+?)"?\s*$', line)
            if m:
                entry[m.group(1)] = m.group(2)
        if "list" in entry and "conecter_type" in entry:
            entries.append(entry)
    return entries


def fetch_all_sources(entries):
    all_articles = []
    for entry in entries:
        url = entry["list"]
        ctype = entry["conecter_type"]
        category = entry.get("category", "")
        lang = entry.get("lang", "")

        script = FETCH_SCRIPTS.get(ctype)
        if not script:
            print(f"[SKIP] unknown conecter_type: {ctype}", file=sys.stderr)
            continue

        try:
            result = subprocess.run(
                [sys.executable, script, url],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode != 0:
                print(f"[FAIL] {ctype} {url}: {result.stderr[:200]}", file=sys.stderr)
                continue
            articles = json.loads(result.stdout)
        except Exception as e:
            print(f"[ERROR] {ctype} {url}: {e}", file=sys.stderr)
            continue

        for a in articles:
            a["category"] = category
            if lang:
                a["lang"] = lang
        all_articles.extend(articles)

    return all_articles
