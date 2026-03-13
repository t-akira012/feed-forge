import os, re, sys

TEMPLATE = """# MAKE_LOG: {name}

## 日付


## 目的


---

## 実装の流れ


---

## 成果物

| ファイル | 内容 |
|---|---|

## 判断メモ

"""


def find_task_number(make_log_dir, name):
    for f in sorted(os.listdir(make_log_dir), reverse=True):
        m = re.match(r"^(\d{3})_" + re.escape(name) + r"_task\.md$", f)
        if m:
            return int(m.group(1))
    raise FileNotFoundError(f"No task file found for '{name}' in {make_log_dir}")


def create_log(make_log_dir, name):
    num = find_task_number(make_log_dir, name)
    filename = f"{num:03d}_{name}_log.md"
    path = os.path.join(make_log_dir, filename)
    with open(path, "w") as f:
        f.write(TEMPLATE.format(name=name))
    return path


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 2 else "make_log"
    name = sys.argv[-1]
    print(create_log(d, name))
