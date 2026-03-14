import subprocess
import os
from datetime import datetime


def make_parcel_dir(parcel_base, task_name):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    parcel_dir = os.path.join(parcel_base, timestamp)
    os.makedirs(parcel_dir, exist_ok=True)
    return parcel_dir


def build_prompt(user_prompt):
    system_instruction = (
        "あなたは厳密なデータ取得プロセスを実行する。"
        "取得したデータに対して自己判断での加工・データ削減・フィルタリングは一切行わない。"
        "取得結果をそのまま出力せよ。加工・削減は次のステップで別のエージェントが行う。"
    )
    return f"{system_instruction}\n\n{user_prompt}"


def dispatch(task_name, prompt, parcel_base="./parcel", timeout=600, ext="md"):
    parcel_dir = make_parcel_dir(parcel_base, task_name)
    parcel_file = os.path.join(parcel_dir, f"{task_name}.{ext}")
    full_prompt = build_prompt(prompt)

    cmd = [
        "codex", "exec",
        "--dangerously-bypass-approvals-and-sandbox",
        "-o", parcel_file,
        full_prompt,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

    return {
        "returncode": result.returncode,
        "parcel_dir": parcel_dir,
        "parcel_file": parcel_file,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: dispatch.py <task-name> <prompt>")
        sys.exit(1)
    r = dispatch(sys.argv[1], sys.argv[2])
    print(f"parcel: {r['parcel_file']}")
    print(f"returncode: {r['returncode']}")
