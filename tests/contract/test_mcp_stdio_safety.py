from __future__ import annotations

import json
import subprocess
import sys


def run_mcp_module(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "tuling_research.mcp_server", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_default_stdio_entrypoint_does_not_write_stdout_logs() -> None:
    result = run_mcp_module()

    assert result.returncode == 0
    assert result.stdout == ""
    assert "tulingresearch-plus" in result.stderr


def test_manifest_output_is_explicit_protocol_payload() -> None:
    result = run_mcp_module("--manifest")

    assert result.returncode == 0
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["server_name"] == "tulingresearch-plus"
    assert payload["transport"] == "stdio"
    assert "core.health_check" in {tool["name"] for tool in payload["tools"]}


def test_health_check_output_is_explicit_protocol_payload() -> None:
    result = run_mcp_module("--health-check")

    assert result.returncode == 0
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["package"] == "tuling_research"
