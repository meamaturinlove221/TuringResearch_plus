from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"
REQUIRED_WORKFLOWS = [
    "ci.yml",
    "docs-check.yml",
    "privacy-gate.yml",
    "release-artifact-dry-run.yml",
]


def read_workflow(name: str) -> str:
    return (WORKFLOWS / name).read_text(encoding="utf-8")


def test_release_candidate_workflows_exist() -> None:
    for workflow in REQUIRED_WORKFLOWS:
        assert (WORKFLOWS / workflow).exists(), workflow


def test_release_candidate_workflows_disable_live_by_default() -> None:
    combined = "\n".join(read_workflow(workflow) for workflow in REQUIRED_WORKFLOWS)

    required_env = [
        'TURINGRESEARCH_MODE: "fake"',
        'TURINGRESEARCH_ENABLE_LIVE_TESTS: "0"',
        'TURINGRESEARCH_ENABLE_WEB_LIVE: "0"',
        'TURINGRESEARCH_ENABLE_APIFY_LIVE: "0"',
        'TURINGRESEARCH_ENABLE_SFTP_LIVE: "0"',
    ]
    for env_line in required_env:
        assert env_line in combined

    assert "tests/live" not in combined
    assert "-m live" not in combined


def test_ci_workflow_runs_v1_6_release_candidate_checks() -> None:
    workflow = read_workflow("ci.yml")

    required = [
        'python -m pip install -e ".[dev,pdf,mcp]"',
        "python -m ruff check src tests",
        "tests/contract/test_package_metadata_v1_6.py",
        "tests/workflow/test_install_smoke_fake.py",
        "python -m pytest tests/unit -m \"not live and not manual\"",
        "python -m pytest tests/contract -m \"not live and not manual\"",
        "tests/workflow/test_release_artifact_manifest.py",
        "tests/contract/test_name_integrity.py",
        "tests/workflow/test_public_demo_privacy_gate.py",
        "python -m mypy src",
    ]
    for term in required:
        assert term in workflow


def test_docs_workflow_is_docs_build_dry_run_only() -> None:
    workflow = read_workflow("docs-check.yml")

    required = [
        "tests/workflow/test_docs_site_build_hardening.py",
        "tests/workflow/test_docs_deployment_preflight.py",
        "tests/workflow/test_docs_deployment_dry_run.py",
        "tests/workflow/test_docs_release_bundle.py",
        "tests/contract/test_public_release_hygiene.py",
        "tests/workflow/test_public_demo_walkthrough_files.py",
    ]
    for term in required:
        assert term in workflow

    forbidden = [
        "actions/deploy-pages",
        "pages: write",
        "id-token: write",
        "environment:",
    ]
    for term in forbidden:
        assert term not in workflow


def test_privacy_gate_workflow_runs_public_safety_checks() -> None:
    workflow = read_workflow("privacy-gate.yml")

    required = [
        "tests/workflow/test_public_demo_privacy_gate.py",
        "tests/contract/test_v1_5_security_privacy_gate.py",
        "tests/workflow/test_v1_1_split_ready_bundles.py",
        "tests/contract/test_public_release_hygiene.py",
        "tests/workflow/test_release_artifact_manifest.py",
    ]
    for term in required:
        assert term in workflow


def test_release_artifact_workflow_is_dry_run_only() -> None:
    workflow = read_workflow("release-artifact-dry-run.yml")

    required = [
        "python -m pip wheel --no-deps --no-build-isolation -w dist .",
        "python -m build --version",
        "python -m build --sdist --no-isolation --outdir dist",
        "sdist skipped: python -m build unavailable",
        "tests/workflow/test_release_artifact_manifest.py",
        "tests/workflow/test_install_smoke_fake.py",
    ]
    for term in required:
        assert term in workflow

    forbidden = [
        "actions/upload-artifact",
        "pypa/gh-action-pypi-publish",
        "gh release",
        "git tag",
        "twine upload",
        "pypi-token",
        "PYPI_API_TOKEN",
    ]
    for term in forbidden:
        assert term not in workflow


def test_release_candidate_workflows_do_not_reference_secrets_or_private_paths() -> None:
    combined = "\n".join(read_workflow(workflow) for workflow in REQUIRED_WORKFLOWS)

    forbidden_patterns = [
        re.compile(r"secrets\."),
        re.compile(r"api[_-]?key", re.IGNORECASE),
        re.compile(r"token:", re.IGNORECASE),
        re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
        re.compile(r"ghp_[A-Za-z0-9_]{12,}"),
        re.compile(r"[A-Za-z]:\\vggt", re.IGNORECASE),
        re.compile(r"/home/[^/\s]+/"),
        re.compile(r"local_project_links\.yaml"),
    ]

    for pattern in forbidden_patterns:
        assert pattern.search(combined) is None


def test_release_candidate_docs_record_no_publish_boundary() -> None:
    docs = (ROOT / "docs" / "github-actions-release-candidate-v1.6.md").read_text(
        encoding="utf-8"
    )

    required = [
        "No PyPI publish",
        "No GitHub release publish",
        "No release artifact upload",
        "No workflow secrets",
        "No live tests",
        "Docs build dry-run only",
        "release-candidate checks, not release automation",
    ]
    for term in required:
        assert term in docs

    legacy_misspelling = "Tuling" + "Research"
    assert legacy_misspelling not in docs
