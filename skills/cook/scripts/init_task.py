import os, re, sys

TEMPLATE = """# {name} 実装タスクリスト

## 背景


## タスク一覧

- [ ] TODO

## 補足

"""


def next_number(cook_dir):
    if not os.path.exists(cook_dir):
        return 1
    nums = []
    for f in os.listdir(cook_dir):
        m = re.match(r"^(\d{3})_", f)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1


def create_task(cook_dir, name):
    num = next_number(cook_dir)
    filename = f"{num:03d}_{name}_task.md"
    path = os.path.join(cook_dir, filename)
    os.makedirs(cook_dir, exist_ok=True)
    with open(path, "w") as f:
        f.write(TEMPLATE.format(name=name))
    return path


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 2 else "cook"
    name = sys.argv[-1]
    print(create_task(d, name))
