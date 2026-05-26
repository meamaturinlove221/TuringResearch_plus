from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_SAFETY_FIXTURES = {
    "examples/vggt-human-prior-survey/shared_store_fixture/.env",
    "examples/vggt-human-prior-survey/shared_store_fixture/large/predictions.npz",
    "examples/vggt-human-prior-survey/shared_store_fixture/private/"
    + "SMPLX"
    + "_model.pkl",
}


def test_public_release_docs_and_templates_exist() -> None:
    required = [
        "docs/public-release-hardening.md",
        "docs/security-checklist.md",
        "docs/license-review.md",
        "docs/secret-scan-policy.md",
        "docs/public-example-policy.md",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/ISSUE_TEMPLATE/research_workflow_request.md",
    ]

    for relative_path in required:
        assert (ROOT / relative_path).exists()


def test_no_env_file_or_private_project_link_is_present() -> None:
    forbidden_names = {
        ".env",
        "local_project_links.yaml",
    }
    offenders = [
        relative
        for path in ROOT.rglob("*")
        if (relative := path.relative_to(ROOT).as_posix())
        not in ALLOWED_SAFETY_FIXTURES
        if path.is_file() and path.name in forbidden_names
    ]

    assert offenders == []


def test_no_token_like_values_in_public_release_surface() -> None:
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|xox[baprs]-[A-Za-z0-9-]+)"
    )
    files = [
        ROOT / ".env.example",
        ROOT / ".mcp.example.json",
        ROOT / "README.md",
        ROOT / "SECURITY.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CODE_OF_CONDUCT.md",
        *sorted((ROOT / "docs").glob("public-*.md")),
        *sorted((ROOT / "docs").glob("*policy.md")),
        *sorted((ROOT / ".github").rglob("*.md")),
    ]

    offenders = [
        path.relative_to(ROOT).as_posix()
        for path in files
        if path.exists() and token_like.search(path.read_text(encoding="utf-8"))
    ]

    assert offenders == []


def test_no_raw_data_or_private_model_payloads_are_in_public_examples() -> None:
    forbidden_suffixes = {".pkl"}
    forbidden_names = {
        "predictions.npz",
        "local_project_links.yaml",
    }
    private_model_prefix = "SMPLX_"
    offenders: list[str] = []

    for path in (ROOT / "examples").rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in ALLOWED_SAFETY_FIXTURES:
            continue
        if path.suffix.lower() in forbidden_suffixes:
            offenders.append(relative)
        if path.name in forbidden_names:
            offenders.append(relative)
        if path.name.startswith(private_model_prefix):
            offenders.append(relative)

    assert offenders == []


def test_public_demo_contains_no_forbidden_payload_names() -> None:
    public_demo = ROOT / "examples" / "public_demo"
    offenders: list[str] = []
    for path in public_demo.rglob("*"):
        if not path.is_file():
            continue
        if path.name in {".env", "local_project_links.yaml", "predictions.npz"}:
            offenders.append(path.relative_to(ROOT).as_posix())
        if path.suffix.lower() == ".pkl":
            offenders.append(path.relative_to(ROOT).as_posix())
        if path.name.startswith("SMPLX_"):
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def test_public_demo_examples_are_marked_demo_safe() -> None:
    public_demo = ROOT / "examples" / "public_demo"
    readme = (public_demo / "README.md").read_text(encoding="utf-8").lower()
    dashboard = (public_demo / "demo_dashboard.html").read_text(encoding="utf-8").lower()
    evidence = (public_demo / "demo_evidence_ledger.json").read_text(encoding="utf-8")

    assert "demo only" in readme
    assert "all data is fake/demo" in readme
    assert "not an experiment result" in dashboard
    assert '"status": "observed"' not in evidence


def test_readme_is_honest_about_default_fake_mode_and_limitations() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "Default tests use fake services" in readme
    assert "They do not require real API keys or live network access" in readme
    assert "Source Hygiene blocks unsafe or unauthorized source material" in readme


def test_license_status_is_clear_and_consistent() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    license_review = (ROOT / "docs" / "license-review.md").read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "Proprietary License" in license_text
    assert "current license is proprietary" in license_review
    assert 'license = { text = "Proprietary" }' in pyproject


def test_security_and_pr_templates_warn_against_sensitive_material() -> None:
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    pr_template = (ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(
        encoding="utf-8"
    )

    assert "Use `.env.example` for variable names only" in security
    assert "Public Release Hygiene" in contributing
    assert "Does not include `.env`" in pr_template
    assert "fake/demo/planned output as observed evidence" in pr_template
