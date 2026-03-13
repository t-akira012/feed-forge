import sys, json, re
import requests


def extract_og_image(html):
    m = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:image["\']', html, re.IGNORECASE)
    if m:
        return m.group(1)
    return ""


def fetch_og_images(items):
    for item in items:
        url = item.get("url", "")
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            item["og_image"] = extract_og_image(resp.text)
        except Exception:
            item["og_image"] = ""
    return items


def main():
    items = json.load(sys.stdin)
    results = fetch_og_images(items)
    json.dump(results, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
