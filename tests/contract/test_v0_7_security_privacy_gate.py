from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.plugins.permission_gate import evaluate_sandbox_permission
from turing_research_plus.plugins.sandbox_policy import (
    SandboxDecisionStatus,
    SandboxPermission,
)
from turing_research_plus.privacy.models import PrivacyFindingType
from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
CURRENT_PUBLIC_DOCS = [
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "docs-index.md",
    ROOT / "docs" / "quickstart.md",
    ROOT / "docs" / "install.md",
    ROOT / "docs" / "examples.md",
    ROOT / "docs" / "limitations.md",
    ROOT / "docs" / "public-demo-guide.md",
    ROOT / "docs" / "vggt-case-study-public.md",
    ROOT / "docs" / "plugin-guide.md",
    ROOT / "docs" / "advisor-export-guide.md",
    ROOT / "docs" / "dashboard-guide.md",
    ROOT / "docs" / "v0.7.0-public-rc-report.md",
    ROOT / "docs" / "v0.7.0-go-no-go.md",
    ROOT / "docs" / "v0.7.0-release-blockers.md",
    ROOT / "docs" / "v0.7.0-public-known-limitations.md",
    ROOT / "docs" / "v0.7.0-security-audit.md",
    ROOT / "docs" / "v0.7.0-privacy-audit.md",
    ROOT / "docs" / "v0.7.0-compliance-audit.md",
    ROOT / "docs" / "v0.7.0-secret-scan-report.md",
]
PUBLIC_SURFACES = [
    ROOT / "README.md",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
    *CURRENT_PUBLIC_DOCS,
    ROOT / "examples" / "public_demo",
    ROOT / "examples" / "vggt-human-prior-survey" / "public_case_study",
]
ALLOWED_SECURITY_FIXTURES = {
    "examples/vggt-human-prior-survey/shared_store_fixture/.env",
    "examples/vggt-human-prior-survey/shared_store_fixture/large/predictions.npz",
    "examples/vggt-human-prior-survey/shared_store_fixture/private/"
    + "SMPLX"
    + "_model.pkl",
}


def _repo_text_files() -> list[Path]:
    suffixes = {".md", ".yaml", ".yml", ".json", ".toml", ".py", ".html", ".txt"}
    ignored = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__"}
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in suffixes
        and not (set(path.parts) & ignored)
    )


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def test_v0_7_public_surfaces_have_no_privacy_release_blockers() -> None:
    report = scan_privacy_paths(PUBLIC_SURFACES)
    allowed_policy_mentions = {PrivacyFindingType.PRIVATE_ADVISOR_FEEDBACK}

    assert report.release_blocker is False
    assert all(finding.release_blocker is False for finding in report.findings)
    assert {finding.finding_type for finding in report.findings} <= allowed_policy_mentions
    assert report.requires_human_review is True


def test_v0_7_no_unapproved_env_or_local_project_links() -> None:
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        if path.name in {".env", "local_project_links" + ".yaml"}:
            offenders.append(relative)

    assert offenders == []


def test_v0_7_no_real_token_or_api_key_values_in_text_surface() -> None:
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assignment_like = re.compile(
        r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9][A-Za-z0-9_-]{11,}"
    )
    offenders = []
    files = [
        ROOT / ".env.example",
        ROOT / ".mcp.example.json",
        ROOT / "README.md",
        ROOT / "SECURITY.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CODE_OF_CONDUCT.md",
        *CURRENT_PUBLIC_DOCS,
        *[
            path
            for path in (ROOT / "examples" / "public_demo").rglob("*")
            if path.is_file()
        ],
    ]
    for path in files:
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        assignment_match = any(
            assignment_like.search(line) for line in text.splitlines()
        )
        if token_like.search(text) or assignment_match:
            offenders.append(relative)

    assert offenders == []


def test_v0_7_no_private_payload_files_outside_allowed_fixtures() -> None:
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        if path.name.startswith("SMPLX" + "_") and path.suffix.lower() in {
            ".npz",
            ".pkl",
        }:
            offenders.append(relative)
        if path.name == "predictions.npz":
            offenders.append(relative)
        if "private_data" in path.parts or "secrets" in path.parts:
            offenders.append(relative)

    assert offenders == []


def test_v0_7_no_huge_npz_payloads_outside_allowed_fixtures() -> None:
    offenders = []
    for path in ROOT.rglob("*.npz"):
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        if path.stat().st_size > 5_000_000:
            offenders.append(relative)

    assert offenders == []


def test_v0_7_public_outputs_do_not_contain_private_local_paths() -> None:
    private_drive_path = "D:" + "/vggt"
    private_win_path = "D:" + "\\\\vggt"
    path_like = re.compile(
        rf"([A-Za-z]:\\Users\\[^\\\s]+|/home/[^/\s]+|{re.escape(private_drive_path)}|{re.escape(private_win_path)})"
    )
    offenders = []
    for path in [
        ROOT / "README.md",
        *CURRENT_PUBLIC_DOCS,
        *sorted((ROOT / "examples" / "public_demo").rglob("*")),
        *sorted((ROOT / "examples" / "vggt-human-prior-survey" / "public_case_study").rglob("*")),
    ]:
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".yaml", ".html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if path_like.search(text):
            offenders.append(_relative(path))

    assert offenders == []


def test_v0_7_license_and_compliance_docs_do_not_overclaim() -> None:
    compliance = (
        ROOT / "examples" / "vggt-human-prior-survey" / "compliance" / "compliance_report.md"
    ).read_text(encoding="utf-8")
    disclaimer = (ROOT / "docs" / "compliance-disclaimer.md").read_text(
        encoding="utf-8"
    )
    public_limitations = (ROOT / "docs" / "v0.7.0-public-known-limitations.md").read_text(
        encoding="utf-8"
    )

    assert "not legal advice" in compliance.lower()
    assert "not legal advice" in disclaimer.lower()
    assert "not legal advice" in public_limitations.lower()
    assert "license approved" not in compliance.lower()
    assert "legally cleared" not in compliance.lower()


def test_v0_7_unsafe_plugin_permissions_are_blocked() -> None:
    blocked_permissions = [
        SandboxPermission.EXECUTE_CODE,
        SandboxPermission.SHELL_ACCESS,
        SandboxPermission.SECRETS_ACCESS,
        SandboxPermission.REMOTE_WRITE,
    ]

    for permission in blocked_permissions:
        decision = evaluate_sandbox_permission(permission)
        assert decision.status == SandboxDecisionStatus.DENIED
        assert decision.release_blocker is True
