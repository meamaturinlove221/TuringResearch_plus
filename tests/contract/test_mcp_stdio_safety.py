from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_mcp_module(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    src_path = str(ROOT / "src")
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        src_path if not existing_pythonpath else os.pathsep.join([src_path, existing_pythonpath])
    )
    return subprocess.run(
        [sys.executable, "-m", "turing_research.mcp_server", *args],
        check=False,
        capture_output=True,
        cwd=ROOT,
        env=env,
        text=True,
    )


def test_default_stdio_entrypoint_does_not_write_stdout_logs() -> None:
    result = run_mcp_module()

    assert result.returncode == 0
    assert result.stdout == ""
    assert "turingresearch-plus" in result.stderr


def test_manifest_output_is_explicit_protocol_payload() -> None:
    result = run_mcp_module("--manifest")

    assert result.returncode == 0
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["server_name"] == "turingresearch-plus"
    assert payload["transport"] == "stdio"
    assert "core.health_check" in {tool["name"] for tool in payload["tools"]}


def test_health_check_output_is_explicit_protocol_payload() -> None:
    result = run_mcp_module("--health-check")

    assert result.returncode == 0
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["package"] == "turing_research"
