from __future__ import annotations

import json
import re
from pathlib import Path

from turing_research_plus.plugins.permission_gate import evaluate_sandbox_permission
from turing_research_plus.plugins.sandbox_policy import (
    SandboxDecisionStatus,
    SandboxPermission,
)

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
PROJECTS = ["vggt_like_demo", "paper_survey_demo", "software_tooling_demo"]


def test_v1_public_launch_readme_is_final_and_honest() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required_sections = [
        "Local-first Research OS",
        "## Architecture",
        "## Problem",
        "## Core Capabilities",
        "## Quickstart",
        "## Public Demo",
        "## VGGT Case Study",
        "## Fake / Live Boundary",
        "## Privacy-first",
        "## Plugin Safety",
        "## Roadmap",
        "## Limitations",
    ]

    for section in required_sections:
        assert section in readme

    forbidden_claims = [
        "automatically completes research",
        "automatically writes final papers",
        "SparseConv3D succeeded",
    ]
    for claim in forbidden_claims:
        assert claim not in readme
    assert "not proof that any VGGT experiment succeeded" in readme


def test_v1_public_launch_quickstart_and_demo_workflow_files_exist() -> None:
    required = [
        ROOT / "docs" / "v1.0.0-quickstart.md",
        ROOT / "docs" / "v1.0.0-public-demo-walkthrough.md",
        PUBLIC_DEMO / "QUICKSTART.md",
        PUBLIC_DEMO / "WALKTHROUGH.md",
        PUBLIC_DEMO / "EXPECTED_OUTPUTS.md",
        PUBLIC_DEMO / "demo_manifest.yaml",
        PUBLIC_DEMO / "dashboard" / "index.html",
        ROOT / "examples" / "benchmarks" / "v1_public_demo_replay.yaml",
    ]
    for project in PROJECTS:
        required.extend(
            [
                PUBLIC_DEMO / "projects" / project / "evidence_ledger.json",
                PUBLIC_DEMO / "projects" / project / "advisor_pack.md",
                PUBLIC_DEMO / "projects" / project / "dashboard.html",
            ]
        )

    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]

    assert missing == []


def test_v1_public_launch_demo_ledgers_do_not_mark_fake_observed() -> None:
    ledgers = [PUBLIC_DEMO / "demo_evidence_ledger.json"]
    ledgers.extend(
        PUBLIC_DEMO / "projects" / project / "evidence_ledger.json"
        for project in PROJECTS
    )

    for path in ledgers:
        payload = json.loads(path.read_text(encoding="utf-8"))
        statuses = {entry["status"] for entry in payload["entries"]}
        assert payload["status"] == "demo-only"
        assert payload["requires_human_review"] is True
        assert "observed" not in statuses
        assert statuses <= {"planned", "fake-data", "not-enough-evidence"}


def test_v1_public_launch_security_privacy_audits_pass_with_review() -> None:
    audit_docs = [
        ROOT / "docs" / "v1.0.0-security-audit.md",
        ROOT / "docs" / "v1.0.0-privacy-audit.md",
        ROOT / "docs" / "v1.0.0-secret-scan-report.md",
        ROOT / "docs" / "v1.0.0-public-data-audit.md",
    ]
    for path in audit_docs:
        text = path.read_text(encoding="utf-8").lower()
        assert "pass with review" in text
        assert "human review" in text


def test_v1_public_launch_has_no_secret_raw_local_or_model_payloads() -> None:
    files = [
        ROOT / "README.md",
        ROOT / ".mcp.example.json",
        ROOT / ".env.example",
        *[
            path
            for path in PUBLIC_DEMO.rglob("*")
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".html"}
        ],
    ]
    combined = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in files)
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    forbidden = [
        "D:" + "/vggt",
        "D:\\vggt",
        "local_project_links" + ".yaml",
        "SMPL" + "-X",
        "SMPLX" + "_",
        '"status": "observed"',
    ]

    for item in forbidden:
        assert item not in combined
    assert not token_like.search(combined)


def test_v1_public_launch_plugin_safety_and_live_mode_defaults() -> None:
    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]
    blocked_permissions = [
        SandboxPermission.EXECUTE_CODE,
        SandboxPermission.SHELL_ACCESS,
        SandboxPermission.SECRETS_ACCESS,
        SandboxPermission.REMOTE_WRITE,
    ]

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"

    for permission in blocked_permissions:
        decision = evaluate_sandbox_permission(permission)
        assert decision.status == SandboxDecisionStatus.DENIED
        assert decision.allowed is False
        assert decision.release_blocker is True


def test_v1_public_launch_go_no_go_docs_exist() -> None:
    required = [
        ROOT / "docs" / "v1.0.0-public-launch-rc-report.md",
        ROOT / "docs" / "v1.0.0-public-launch-go-no-go.md",
        ROOT / "docs" / "v1.0.0-public-launch-blockers.md",
    ]

    for path in required:
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "go with review" in text or "no-go" in text
