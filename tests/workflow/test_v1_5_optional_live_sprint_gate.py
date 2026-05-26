from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs" / "v1.5.0-optional-live-sprint-gate-report.md"
LANE = ROOT / "lanes" / "327_optional_live_sprint_gate.md"
MCP = ROOT / ".mcp.example.json"
PYPROJECT = ROOT / "pyproject.toml"

DOCS = [
    ROOT / "docs" / "optional-live-polish-scope.md",
    ROOT / "docs" / "optional-live-safety-policy.md",
    ROOT / "docs" / "optional-live-test-policy-v1.5.md",
    ROOT / "docs" / "scholar-live-optional-guide.md",
    ROOT / "docs" / "web-apify-live-optional-guide.md",
    ROOT / "docs" / "sftp-live-optional-guide.md",
    ROOT / "docs" / "optional-live-safety-gate.md",
    REPORT,
    LANE,
]

EXAMPLE_DIRS = [
    ROOT / "examples" / "scholar_demo" / "live_optional",
    ROOT / "examples" / "apify_workflows" / "live_optional",
    ROOT / "examples" / "session_runtime" / "sftp_live_optional",
]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined(paths: list[Path]) -> str:
    return "\n".join(_text(path) for path in paths)


def _mcp_env() -> dict[str, str]:
    config = json.loads(MCP.read_text(encoding="utf-8"))
    return config["mcpServers"]["turingresearch-plus"]["env"]


def test_optional_live_sprint_gate_docs_exist() -> None:
    assert REPORT.exists()
    assert LANE.exists()
    for path in DOCS[:-2]:
        assert path.exists()


def test_optional_live_sprint_gate_records_required_surfaces() -> None:
    text = _combined([REPORT, LANE])

    assert "GO FOR OPTIONAL LIVE POLISH / NO-GO FOR DEFAULT LIVE" in text
    assert "Scholar live optional" in text
    assert "Web / Apify live optional" in text
    assert "SFTP live optional" in text
    assert "MCP env block" in text
    assert "live tests skipped by default" in text
    assert "no secrets" in text
    assert "no remote command" in text
    assert "no private scraping" in text
    assert "no old naming" in text


def test_optional_live_sprint_gate_defaults_are_disabled() -> None:
    env = _mcp_env()
    pyproject = _text(PYPROJECT)

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_APIFY_LIVE"] == "0"
    assert env["SEMANTIC_SCHOLAR_API_KEY"] == ""
    assert env["APIFY_TOKEN"] == ""
    assert "-m 'not live and not manual'" in pyproject


def test_optional_live_sprint_gate_examples_use_placeholders_only() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for directory in EXAMPLE_DIRS
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    )

    assert "SEMANTIC_SCHOLAR_API_KEY=" in combined
    assert "APIFY_TOKEN=" in combined
    assert "TURINGRESEARCH_SFTP_CREDENTIAL=" in combined
    assert "<private local value>" in combined
    assert "<private local key path placeholder>" in combined
    assert "BEGIN OPENSSH PRIVATE KEY" not in combined
    assert "password=" not in combined.lower()


def test_optional_live_sprint_gate_has_no_sensitive_material_or_old_name() -> None:
    combined = _combined(DOCS)
    old_name = "Tuling" + "Research"

    forbidden = [
        old_name,
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "github_pat_",
        "sk-",
        "https://github.com/",
        "status" + ": observed",
    ]
    for marker in forbidden:
        assert marker not in combined


def test_optional_live_sprint_gate_does_not_claim_live_success() -> None:
    text = _combined([REPORT, LANE])

    assert "does not run live providers" in text
    assert "not proof that any provider call" in text
    assert "live output treated as observed evidence without human review" in text
    assert "automatic Evidence Ledger write" in text
