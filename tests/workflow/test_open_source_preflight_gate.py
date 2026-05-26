from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MCP = ROOT / ".mcp.example.json"
REQUIRED_ROUND_DOCS = [
    ROOT / "docs" / "open-source-rename-scope.md",
    ROOT / "docs" / "turingresearch-public-naming-policy.md",
    ROOT / "docs" / "public-naming-sweep-report.md",
    ROOT / "docs" / "readme-first-public-version-report.md",
    ROOT / "docs" / "open-source-license-decision.md",
    ROOT / "docs" / "open-source-compliance-checklist.md",
    ROOT / "docs" / "mcp-public-config-guide.md",
    ROOT / "docs" / "open-source-hygiene-gate-report.md",
]
REQUIRED_GITHUB_READY_DOCS = [
    ROOT / "docs" / "github-repo-description.md",
    ROOT / "docs" / "github-profile-readme-snippet.md",
    ROOT / "docs" / "main-repo-public-launch-plan.md",
    ROOT / "docs" / "github-pages-safety-checklist.md",
]
REQUIRED_ROOT_FILES = [
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "CITATION.cff",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
    ROOT / "SECURITY.md",
    MCP,
]
PUBLIC_SURFACES = [
    ROOT / "README.md",
    ROOT / ".env.example",
    MCP,
    ROOT / "LICENSE",
    ROOT / "CITATION.cff",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
    ROOT / "SECURITY.md",
    *REQUIRED_ROUND_DOCS,
    *REQUIRED_GITHUB_READY_DOCS,
    ROOT / "docs" / "open-source-preflight-gate-report.md",
    ROOT / "docs" / "open-source-go-no-go.md",
    ROOT / "docs" / "open-source-next-actions.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def test_open_source_preflight_required_round_outputs_exist() -> None:
    required = [
        *REQUIRED_ROUND_DOCS,
        *REQUIRED_GITHUB_READY_DOCS,
        *REQUIRED_ROOT_FILES,
        ROOT / "lanes" / "360_1_open_source_rename_scope.md",
        ROOT / "lanes" / "360_2_public_naming_sweep.md",
        ROOT / "lanes" / "360_3_readme_first_public_version.md",
        ROOT / "lanes" / "360_4_license_citation_conduct.md",
        ROOT / "lanes" / "360_5_mcp_env_public_hygiene.md",
        ROOT / "lanes" / "360_6_open_source_hygiene_gate.md",
    ]

    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.exists()]
    assert missing == []


def test_open_source_preflight_go_no_go_status_is_honest() -> None:
    report = _read(ROOT / "docs" / "open-source-preflight-gate-report.md")
    go_no_go = _read(ROOT / "docs" / "open-source-go-no-go.md")
    next_actions = _read(ROOT / "docs" / "open-source-next-actions.md")

    assert "Status: go for v1.6 public release execution line with human blockers" in report
    assert "GO for v1.6 public release execution line" in go_no_go
    assert "NO-GO for automatic publication" in go_no_go
    assert "Final license selection and approval" in next_actions
    assert "GitHub repo readiness docs present" in report
    assert "Round 360.7" in report
    assert "not found as an independent lane" in report


def test_open_source_preflight_public_surfaces_have_no_release_blocker_markers() -> None:
    combined = "\n".join(_read(path) for path in PUBLIC_SURFACES if path.exists())
    prior_public_name = "Tul" + "ingResearch"
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    fake_urls = [
        "github.com/" + "OWNER/",
        "github.com/" + "example/",
        "github.com/" + "meamaturinlove221/TuringResearch",
        "https://github.com/" + "turingresearch/",
    ]

    assert prior_public_name not in combined
    plus_display = "TuringResearch" + " Plus"
    plus_path = "TuringResearch" + "_plus"

    assert plus_display not in combined
    assert plus_path not in combined
    assert not token_like.search(combined)
    assert all(url not in combined for url in fake_urls)
    assert "D:" + "/vggt" not in combined
    assert "D:" + "\\vggt" not in combined
    assert "SMPL" + "-X" not in combined
    assert "SMPLX" + "_" not in combined


def test_open_source_preflight_mcp_and_live_defaults_are_safe() -> None:
    config = json.loads(MCP.read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_WEB_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_APIFY_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_SFTP_LIVE"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"

    for key, value in env.items():
        if key.startswith("TURINGRESEARCH_ENABLE_"):
            assert value == "0"
        elif key == "TURINGRESEARCH_MODE":
            assert value == "fake"
        else:
            assert value == ""


def test_open_source_preflight_readme_and_aris_boundary() -> None:
    readme = _read(ROOT / "README.md")

    assert readme.splitlines()[0] == "# TuringResearch"
    assert "TuringResearch helps researchers" in readme
    assert "Default tests use fake services" in readme
    assert "They do not require real API keys or live network access" in readme
    assert "ARIS remains deferred" in readme
    assert "ARIS is implemented" not in readme
