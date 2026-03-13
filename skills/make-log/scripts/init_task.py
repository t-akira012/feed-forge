import os, re, sys

TEMPLATE = """# {name} 実装タスクリスト

## 背景


## タスク一覧

- [ ] TODO

## 補足

"""


def next_number(make_log_dir):
    if not os.path.exists(make_log_dir):
        return 1
    nums = []
    for f in os.listdir(make_log_dir):
        m = re.match(r"^(\d{3})_", f)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1


def create_task(make_log_dir, name):
    num = next_number(make_log_dir)
    filename = f"{num:03d}_{name}_task.md"
    path = os.path.join(make_log_dir, filename)
    os.makedirs(make_log_dir, exist_ok=True)
    with open(path, "w") as f:
        f.write(TEMPLATE.format(name=name))
    return path


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 2 else "make_log"
    name = sys.argv[-1]
    print(create_task(d, name))
