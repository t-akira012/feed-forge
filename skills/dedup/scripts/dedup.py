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
