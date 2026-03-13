import sys, os


def deliver_file(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def main():
    method = sys.argv[1]  # file / slack / email
    target = sys.argv[2]  # パス or URL
    content = sys.stdin.read()

    if method == "file":
        deliver_file(content, target)


if __name__ == "__main__":
    main()
