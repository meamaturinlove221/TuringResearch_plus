from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def pyproject() -> dict[str, object]:
    return tomllib.loads(read_text("pyproject.toml"))


def run_mcp_module(*args: str) -> dict[str, object]:
    env = os.environ.copy()
    env["TURINGRESEARCH_MODE"] = "fake"
    env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] = "0"
    env["TURINGRESEARCH_ENABLE_PLUGINS"] = "0"
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [sys.executable, "-m", "turing_research.mcp_server", *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.strip()
    payload = json.loads(result.stdout)
    assert isinstance(payload, dict)
    return payload


def test_install_guides_document_local_pipx_and_uv_paths() -> None:
    docs = "\n".join(
        [
            read_text("docs/pipx-install-guide.md"),
            read_text("docs/uv-install-guide.md"),
            read_text("docs/install-smoke-test.md"),
        ]
    )

    assert "No PyPI package is required" in docs
    assert "No PyPI publication is performed" in docs
    assert "local editable" in docs.lower()
    assert "wheel artifact" in docs.lower()
    assert "turingresearch_plus-1.5.0rc0-py3-none-any.whl" in docs
    assert "No API key" in docs
    assert "No VGGT" in docs
    assert "Live adapters remain disabled by default" in docs
    assert "do not use a package-index install command" in docs.lower()


def test_install_guides_avoid_private_or_secret_material() -> None:
    docs = "\n".join(
        [
            read_text("docs/pipx-install-guide.md"),
            read_text("docs/uv-install-guide.md"),
            read_text("docs/install-smoke-test.md"),
        ]
    )

    legacy_misspelling = "Tuling" + "Research"
    forbidden_patterns = [
        re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
        re.compile(r"ghp_[A-Za-z0-9_]{12,}"),
        re.compile(r"APIFY_TOKEN\s*=\s*['\"][^'\"]+['\"]"),
        re.compile(r"[A-Za-z]:\\vggt", re.IGNORECASE),
        re.compile(r"/home/[^/\s]+/"),
    ]

    assert legacy_misspelling not in docs
    assert "SparseConv3D success" not in docs
    assert "https://github.com/" not in docs
    for pattern in forbidden_patterns:
        assert not pattern.search(docs)


def test_fake_health_check_command_runs_without_live_dependencies() -> None:
    project = pyproject()["project"]
    assert isinstance(project, dict)

    payload = run_mcp_module("--health-check")

    assert payload["status"] == "ok"
    assert payload["package"] == "turing_research"
    assert payload["version"] == project["version"]
    assert isinstance(payload["tools"], list)
    assert "core.health_check" in payload["tools"]


def test_fake_manifest_command_runs_and_matches_entrypoint_metadata() -> None:
    project = pyproject()["project"]
    assert isinstance(project, dict)
    scripts = project["scripts"]
    assert isinstance(scripts, dict)

    payload = run_mcp_module("--manifest")
    tool_names = {tool["name"] for tool in payload["tools"]}

    assert scripts["turingresearch-plus-mcp"] == "turing_research.mcp_server:main"
    assert payload["server_name"] == "turingresearch-plus"
    assert payload["package"] == "turing_research"
    assert payload["version"] == project["version"]
    assert payload["transport"] == "stdio"
    assert "core.health_check" in tool_names
    assert "core.paper_content" in tool_names
    assert "core.web_content" in tool_names


def test_install_guide_links_round_379_guides() -> None:
    install = read_text("docs/install.md")

    assert "[pipx Install Guide](pipx-install-guide.md)" in install
    assert "[uv Install Guide](uv-install-guide.md)" in install
    assert "[Install Smoke Test](install-smoke-test.md)" in install
    assert "local wheel artifact installs" in install
