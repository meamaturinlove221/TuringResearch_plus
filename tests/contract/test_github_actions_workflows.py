from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"

REQUIRED_WORKFLOWS = [
    "ci.yml",
    "docs-check.yml",
    "privacy-gate.yml",
    "release-artifact-dry-run.yml",
]


def test_required_github_actions_workflows_exist() -> None:
    for workflow in REQUIRED_WORKFLOWS:
        assert (WORKFLOWS / workflow).exists(), workflow


def test_ci_workflow_contains_required_checks() -> None:
    text = (WORKFLOWS / "ci.yml").read_text(encoding="utf-8")

    required = [
        "actions/checkout",
        "actions/setup-python",
        'python -m pip install -e ".[dev,pdf,mcp]"',
        "python -m ruff check src tests",
        "python -m pytest tests/unit",
        "python -m pytest tests/contract",
        "test_package_metadata_v1_6.py",
        "test_install_smoke_fake.py",
        "test_release_artifact_manifest.py",
        "test_name_integrity.py",
        "test_public_demo_privacy_gate.py",
        "python -m mypy src",
    ]

    for item in required:
        assert item in text


def test_docs_and_privacy_workflows_are_fake_default() -> None:
    combined = "\n".join(
        (WORKFLOWS / workflow).read_text(encoding="utf-8")
        for workflow in ["docs-check.yml", "privacy-gate.yml"]
    )

    assert "test_docs_site_build_hardening.py" in combined
    assert "test_docs_deployment_preflight.py" in combined
    assert "test_docs_deployment_dry_run.py" in combined
    assert "test_docs_release_bundle.py" in combined
    assert "test_public_release_hygiene.py" in combined
    assert "test_v1_5_security_privacy_gate.py" in combined
    assert "test_release_artifact_manifest.py" in combined
    assert 'TURINGRESEARCH_ENABLE_LIVE_TESTS: "0"' in combined


def test_github_actions_do_not_publish_or_upload_private_data() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in WORKFLOWS.glob("*.yml")
        if path.name in REQUIRED_WORKFLOWS
    ).lower()

    forbidden = [
        "pypi",
        "gh release",
        "git tag",
        "actions/upload-artifact",
        "pypa/gh-action-pypi-publish",
        "twine upload",
        "secrets.",
        "api_key",
        "token:",
        "d:/vggt",
        "local_project_links.yaml",
    ]

    for item in forbidden:
        assert item not in combined


def test_github_actions_skip_live_tests_by_default() -> None:
    combined = "\n".join(
        (WORKFLOWS / workflow).read_text(encoding="utf-8")
        for workflow in REQUIRED_WORKFLOWS
    )

    assert 'TURINGRESEARCH_ENABLE_LIVE_TESTS: "0"' in combined
    assert "tests/live" not in combined
    assert "-m live" not in combined
