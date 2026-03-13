import os, re, sys


def next_number(cook_dir):
    if not os.path.exists(cook_dir):
        return 1
    nums = []
    for f in os.listdir(cook_dir):
        m = re.match(r"^(\d{3})_", f)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "cook"
    print(next_number(d))
