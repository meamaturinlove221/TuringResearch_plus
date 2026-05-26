from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_V1_1_DOCS = [
    "docs/v1.1.0-baseline-verification.md",
    "docs/v1.1.0-final-scope.md",
    "docs/v1.1.0-main-repo-stabilization-report.md",
    "docs/v1.1.0-sprint-1-gate-report.md",
    "docs/v1.1.0-split-execution-gate.md",
    "docs/v1.1.0-docs-dashboard-integration-report.md",
    "docs/v1.1.0-paper-demo-integration-report.md",
    "docs/v1.1.0-github-actions-hardening.md",
    "docs/v1.1.0-full-regression-report.md",
    "docs/v1.1.0-regression-failures.md",
]

REQUIRED_V1_1_CONTRACTS = [
    "contracts/v1_public_api.yaml",
    "contracts/docs_site_builder.yaml",
    "contracts/local_server_dashboard.yaml",
    "contracts/dashboard_data_api.yaml",
    "contracts/paper_draft_assembly_beta.yaml",
    "contracts/plugin_sandbox_policy.yaml",
]

REQUIRED_V1_1_TESTS = [
    "tests/workflow/test_v1_1_full_fake_replay.py",
    "tests/contract/test_v1_1_release_contracts.py",
    "tests/contract/test_github_actions_workflows.py",
    "tests/workflow/test_v1_1_docs_dashboard_integration.py",
    "tests/workflow/test_v1_1_paper_demo_integration.py",
    "tests/workflow/test_v1_1_split_ready_bundles.py",
]


def test_v1_1_release_docs_exist() -> None:
    missing = [path for path in REQUIRED_V1_1_DOCS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_1_release_contracts_exist() -> None:
    missing = [path for path in REQUIRED_V1_1_CONTRACTS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_1_release_tests_exist() -> None:
    missing = [path for path in REQUIRED_V1_1_TESTS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_1_release_docs_preserve_public_boundaries() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in REQUIRED_V1_1_DOCS
    )
    required_terms = [
        "fake",
        "privacy",
        "human review",
        "no automatic",
        "split",
        "dashboard",
        "paper",
        "github actions",
    ]

    for term in required_terms:
        assert term in combined


def test_v1_1_release_does_not_claim_automatic_publication() -> None:
    report = (ROOT / "docs" / "v1.1.0-full-regression-report.md").read_text(
        encoding="utf-8"
    )
    failures = (ROOT / "docs" / "v1.1.0-regression-failures.md").read_text(
        encoding="utf-8"
    )
    combined = f"{report}\n{failures}".lower()

    assert "pass with review" in combined
    assert "not released" in combined
    assert "no automatic github release" in combined
    assert "no automatic pypi publish" in combined
    assert "no automatic child repository creation" in combined
