import os, re, sys


def next_number(make_log_dir):
    if not os.path.exists(make_log_dir):
        return 1
    nums = []
    for f in os.listdir(make_log_dir):
        m = re.match(r"^(\d{3})_", f)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "make_log"
    print(next_number(d))
