from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ISSUE_TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"

TEMPLATES = {
    "bug": ISSUE_TEMPLATE_DIR / "bug_report.md",
    "feature": ISSUE_TEMPLATE_DIR / "feature_request.md",
    "research_case": ISSUE_TEMPLATE_DIR / "research_case_request.md",
    "plugin": ISSUE_TEMPLATE_DIR / "plugin_proposal.md",
    "security_privacy": ISSUE_TEMPLATE_DIR / "security_privacy_report.md",
    "pull_request": ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_v1_1_issue_templates_exist() -> None:
    missing = [name for name, path in TEMPLATES.items() if not path.exists()]

    assert missing == []


def test_v1_1_templates_collect_required_debug_context() -> None:
    required = [
        "Expected",
        "Actual",
        "Reproduction",
        "Environment",
        "Live mode",
        "Safety",
        "Do not upload",
    ]

    for name, path in TEMPLATES.items():
        text = _read(path)
        missing = [item for item in required if item not in text]
        assert missing == [], f"{name} missing {missing}"


def test_v1_1_templates_warn_against_sensitive_uploads() -> None:
    required = [
        "API keys",
        "raw data",
        "SMPL-X model files",
        "private local paths",
    ]

    for name, path in TEMPLATES.items():
        text = _read(path)
        missing = [item for item in required if item not in text]
        assert missing == [], f"{name} missing {missing}"


def test_v1_1_plugin_proposal_requires_permissions() -> None:
    text = _read(TEMPLATES["plugin"])
    required = [
        "Requested Permissions",
        "Network access",
        "Execute code",
        "Shell access",
        "Secrets access",
        "Permission Justification",
    ]

    for item in required:
        assert item in text
    assert "Unknown third-party plugins must stay disabled by default" in text


def test_v1_1_research_case_request_declares_data_sensitivity() -> None:
    text = _read(TEMPLATES["research_case"])
    required = [
        "Data Sensitivity",
        "public demo",
        "private research",
        "restricted data",
        "Does it require raw data?",
        "Does it require restricted model files?",
    ]

    for item in required:
        assert item in text


def test_v1_1_templates_have_no_secret_or_old_name_payloads() -> None:
    combined = "\n".join(_read(path) for path in TEMPLATES.values())
    forbidden = [
        "Tuling" + "Research",
        "D:" + "/vggt",
        "D:\\vggt",
        "SMPLX" + "_",
    ]
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )

    for item in forbidden:
        assert item not in combined
    assert not token_like.search(combined)
