import json
import os
import re
from unittest.mock import patch, MagicMock
from skills.outsourcing.scripts.dispatch import dispatch, build_prompt, make_parcel_dir


def test_make_parcel_dir_creates_timestamped_dir(tmp_path):
    parcel_dir = make_parcel_dir(str(tmp_path), "test-task")
    assert os.path.isdir(parcel_dir)
    # structure: {base}/{timestamp}/
    dirname = os.path.basename(parcel_dir)
    # timestamp format: YYYY-MM-DD-HH-MM-SS
    assert re.match(r"\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}", dirname)


def test_build_prompt_includes_no_modification_instruction():
    prompt = build_prompt("fetch some data")
    assert "加工" in prompt or "modify" in prompt.lower() or "削減" in prompt
    assert "fetch some data" in prompt


def test_dispatch_runs_codex_and_saves_parcel(tmp_path):
    mock_result = MagicMock()
    mock_result.returncode = 0

    with patch("skills.outsourcing.scripts.dispatch.subprocess.run", return_value=mock_result) as mock_run:
        result = dispatch(
            task_name="digest-fetch",
            prompt="fetch all sources",
            parcel_base=str(tmp_path),
        )

    assert mock_run.called
    cmd = mock_run.call_args[0][0]
    # codex exec should be invoked
    assert "codex" in cmd[0]
    assert "exec" in cmd
    # -o flag should point to parcel file
    assert "-o" in cmd
    # parcel dir should have been created
    assert result["parcel_dir"] is not None
    assert "digest-fetch" in result["parcel_file"]
