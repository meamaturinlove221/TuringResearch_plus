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
    ROOT / "README.md",
    ROOT / "docs" / "v1.0.0-quickstart.md",
    ROOT / "docs" / "v1.0.0-public-api.md",
    ROOT / "docs" / "v1.0.0-import-guide.md",
    ROOT / "docs" / "v1.0.0-api-install-integration-report.md",
    ROOT / "docs" / "v1.0.0-api-install-known-limitations.md",
    ROOT / "docs" / "v1.0.0-public-demo-walkthrough.md",
    ROOT / "docs" / "v1.0.0-demo-script.md",
    ROOT / "docs" / "v1.0.0-readme-finalization-report.md",
    ROOT / "docs" / "v1.0.0-interview-pack-final.md",
    ROOT / "docs" / "v1.0.0-interview-30s-pitch.md",
    ROOT / "docs" / "v1.0.0-interview-3min-pitch.md",
    ROOT / "docs" / "v1.0.0-interview-10min-demo.md",
    ROOT / "docs" / "v1.0.0-interview-faq-final.md",
    ROOT / "docs" / "v1.0.0-engineering-highlights.md",
]

PUBLIC_SURFACES = [
    *CURRENT_PUBLIC_DOCS,
    ROOT / ".env.example",
    ROOT / ".mcp.example.json",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
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


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _text_files_under(paths: list[Path]) -> list[Path]:
    suffixes = {".md", ".yaml", ".yml", ".json", ".toml", ".py", ".html", ".txt"}
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in suffixes:
            files.append(path)
        elif path.is_dir():
            files.extend(
                item
                for item in path.rglob("*")
                if item.is_file() and item.suffix.lower() in suffixes
            )
    return sorted(set(files))


def test_v1_public_launch_surfaces_have_no_privacy_release_blockers() -> None:
    report = scan_privacy_paths(PUBLIC_SURFACES)
    allowed_policy_mentions = {
        "private advisor feedback markers",
        "private advisor feedback.",
    }
    unexpected = [
        finding
        for finding in report.findings
        if finding.finding_type != PrivacyFindingType.PRIVATE_ADVISOR_FEEDBACK
        or finding.proposed_redaction is None
        or (
            finding.proposed_redaction.proposed_text
            and "[REDACTED]" not in finding.proposed_redaction.proposed_text
            and not any(
                mention.replace("private advisor feedback", "[REDACTED]")
                in finding.proposed_redaction.proposed_text
                for mention in allowed_policy_mentions
            )
        )
    ]

    assert report.release_blocker is False
    assert unexpected == []
    assert report.requires_human_review is True


def test_v1_no_unapproved_env_or_local_project_links() -> None:
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


def test_v1_no_real_token_or_api_key_values_in_launch_surface() -> None:
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    assignment_like = re.compile(
        r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret)\s*[:=]\s*"
        r"['\"]?[A-Za-z0-9][A-Za-z0-9_-]{11,}"
    )
    offenders = []

    for path in _text_files_under(PUBLIC_SURFACES):
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if token_like.search(text) or any(
            assignment_like.search(line) for line in text.splitlines()
        ):
            offenders.append(relative)

    assert offenders == []


def test_v1_no_private_payload_files_outside_allowed_fixtures() -> None:
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


def test_v1_no_huge_npz_payloads_outside_allowed_fixtures() -> None:
    offenders = []
    for path in ROOT.rglob("*.npz"):
        relative = _relative(path)
        if relative in ALLOWED_SECURITY_FIXTURES:
            continue
        if path.stat().st_size > 5_000_000:
            offenders.append(relative)

    assert offenders == []


def test_v1_public_launch_text_has_no_private_paths_or_old_name() -> None:
    private_drive_path = "D:" + "/vggt"
    private_win_path = "D:" + "\\\\vggt"
    private_path_like = re.compile(
        rf"([A-Za-z]:\\Users\\[^\\\s]+|/home/[^/\s]+|{re.escape(private_drive_path)}|"
        rf"{re.escape(private_win_path)})"
    )
    old_name = "Tuling" + "Research"
    offenders = []

    for path in _text_files_under(PUBLIC_SURFACES):
        text = path.read_text(encoding="utf-8", errors="replace")
        if private_path_like.search(text) or old_name in text:
            offenders.append(_relative(path))

    assert offenders == []


def test_v1_public_demo_has_no_unsupported_observed_claims() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace").lower()
        for path in _text_files_under([ROOT / "examples" / "public_demo"])
    )

    assert '"status": "observed"' not in combined
    assert "experiment success" not in combined
    assert "claim benchmark improvement" not in combined.replace(
        "do not claim benchmark improvement", ""
    )
    assert "final paper conclusion" not in combined.replace("no final paper conclusion", "")


def test_v1_unsafe_plugin_permissions_are_blocked() -> None:
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
        assert decision.allowed is False


def test_v1_launch_audit_reports_exist_and_record_review_boundary() -> None:
    required = [
        ROOT / "docs" / "v1.0.0-security-audit.md",
        ROOT / "docs" / "v1.0.0-privacy-audit.md",
        ROOT / "docs" / "v1.0.0-secret-scan-report.md",
        ROOT / "docs" / "v1.0.0-public-data-audit.md",
    ]

    for path in required:
        assert path.exists()
        text = path.read_text(encoding="utf-8").lower()
        assert "pass with review" in text
        assert "human review" in text
        assert "not a certification" in text or "not legal advice" in text
