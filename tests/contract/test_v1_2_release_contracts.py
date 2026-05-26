from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_V1_2_DOCS = [
    "docs/v1.2.0-final-scope.md",
    "docs/v1.2.0-original-reference-parity-first.md",
    "docs/original-reference-parity-matrix.md",
    "docs/aris-deferral-decision.md",
    "docs/" + "neo" + "cortica-reference-parity-integration-report.md",
    "docs/" + "neo" + "cortica-parity-gate-report.md",
    "docs/" + "yogsoth" + "-parity-gate-report.md",
    "docs/reference-parity-dashboard.md",
    "docs/v1.2.0-full-workflow-replay-report.md",
    "docs/v1.2.0-public-demo-refresh.md",
    "docs/v1.2.0-security-audit.md",
    "docs/v1.2.0-privacy-audit.md",
    "docs/v1.2.0-secret-scan-report.md",
    "docs/v1.2.0-interview-pack.md",
    "docs/v1.2.0-full-regression-report.md",
    "docs/v1.2.0-regression-failures.md",
]

REQUIRED_V1_2_TESTS = [
    "tests/workflow/test_v1_2_full_fake_replay.py",
    "tests/workflow/test_reference_parity_dashboard.py",
    "tests/workflow/test_v1_2_public_demo.py",
    "tests/contract/test_v1_2_security_privacy_gate.py",
    "tests/contract/test_v1_2_release_contracts.py",
]

REQUIRED_V1_2_CONTRACTS = [
    "contracts/neocortica_session_parity.yaml",
    "contracts/neocortica_scholar_parity.yaml",
    "contracts/neocortica_web_parity.yaml",
    "contracts/yogsoth_campaign_parity.yaml",
    "contracts/yogsoth_vault_parity.yaml",
    "contracts/yogsoth_ontology_parity.yaml",
    "contracts/yogsoth_stress_test_parity.yaml",
    "contracts/yogsoth_experiment_execution_parity.yaml",
]

REQUIRED_V1_1_WORKFLOW_TESTS = [
    "tests/workflow/test_v1_1_full_fake_replay.py",
    "tests/workflow/test_v1_1_docs_dashboard_integration.py",
    "tests/workflow/test_v1_1_paper_demo_integration.py",
    "tests/workflow/test_v1_1_split_ready_bundles.py",
    "tests/contract/test_v1_1_release_contracts.py",
]


def test_v1_2_release_docs_exist() -> None:
    missing = [path for path in REQUIRED_V1_2_DOCS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_2_release_tests_exist() -> None:
    required = [*REQUIRED_V1_2_TESTS, *REQUIRED_V1_1_WORKFLOW_TESTS]
    missing = [path for path in required if not (ROOT / path).exists()]

    assert missing == []


def test_v1_2_reference_parity_contracts_exist() -> None:
    missing = [path for path in REQUIRED_V1_2_CONTRACTS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_2_regression_report_covers_required_surfaces() -> None:
    report = (ROOT / "docs" / "v1.2.0-full-regression-report.md").read_text(
        encoding="utf-8"
    )
    required_terms = [
        "v1.1 existing workflows",
        "Neocortica parity",
        "yogsoth parity",
        "Reference Parity Dashboard",
        "public demo v1.2",
        "security/privacy",
        "ARIS deferred",
        "PASS WITH REVIEW",
    ]

    for term in required_terms:
        assert term in report


def test_v1_2_regression_failures_record_no_unresolved_failures() -> None:
    failures = (ROOT / "docs" / "v1.2.0-regression-failures.md").read_text(
        encoding="utf-8"
    )

    assert "Status: no unresolved failures" in failures
    assert "none" in failures.lower()
    assert "introduce new features" in failures
    assert "enable live tests by default" in failures


def test_v1_2_release_boundary_does_not_claim_release_or_aris_adoption() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/v1.2.0-full-regression-report.md",
            "docs/v1.2.0-regression-failures.md",
            "docs/aris-deferral-decision.md",
            "docs/v1.2.0-security-audit.md",
            "docs/v1.2.0-privacy-audit.md",
        ]
    ).lower()

    required_boundaries = [
        "not released",
        "not tagged",
        "no automatic github release",
        "no automatic pypi publish",
        "no automatic experiment execution",
        "human review",
        "aris deferred",
    ]
    for boundary in required_boundaries:
        assert boundary in combined

    forbidden_claims = [
        "aris adopted" + " in v1.2",
        "automatic experiment execution" + " enabled",
        "remote execution" + " enabled",
        "fake/demo result promotion enabled",
    ]
    for claim in forbidden_claims:
        assert claim not in combined
