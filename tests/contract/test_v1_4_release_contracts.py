from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_V1_4_DOCS = [
    "docs/v1.4.0-original-repo-production-parity.md",
    "docs/v1.4.0-plan-adjustment-from-upstream.md",
    "docs/v1.4.0-implementation-order.md",
    "docs/v1.4.0-aris-still-deferred.md",
    "docs/session-production-parity-gate-report.md",
    "docs/scholar-production-parity-gate-report.md",
    "docs/web-production-parity-gate-report.md",
    "docs/yogsoth-production-parity-gate-report.md",
    "docs/v1.4.0-full-production-replay-report.md",
    "docs/original-repo-parity-dashboard-v2.md",
    "docs/original-repo-production-parity-summary.md",
    "docs/aris-still-deferred-v1.4.md",
    "docs/v1.4.0-security-audit.md",
    "docs/v1.4.0-privacy-audit.md",
    "docs/v1.4.0-secret-scan-report.md",
    "docs/v1.4.0-full-regression-report.md",
    "docs/v1.4.0-regression-failures.md",
    "docs/v1.4.0-release-notes.md",
    "docs/v1.4.0-feature-list.md",
    "docs/v1.4.0-known-limitations.md",
    "docs/v1.4.0-test-summary.md",
    "docs/v1.4.0-upgrade-guide.md",
    "docs/github-release-draft-v1.4.0.md",
]

REQUIRED_V1_4_TESTS = [
    "tests/workflow/test_session_production_parity_gate.py",
    "tests/workflow/test_scholar_production_parity_gate.py",
    "tests/workflow/test_web_production_parity_gate.py",
    "tests/workflow/test_yogsoth_production_parity_gate.py",
    "tests/workflow/test_v1_4_full_production_replay.py",
    "tests/workflow/test_original_repo_parity_dashboard_v2.py",
    "tests/workflow/test_v1_4_docs_production_polish.py",
    "tests/contract/test_v1_4_security_privacy_gate.py",
    "tests/contract/test_v1_4_release_contracts.py",
]

REQUIRED_V1_4_CONTRACTS = [
    "contracts/session_cli_surface.yaml",
    "contracts/session_script_export.yaml",
    "contracts/cross_platform_archive_hardening.yaml",
    "contracts/optional_remote_dry_run_plan.yaml",
    "contracts/return_import_human_confirmation.yaml",
    "contracts/heavy_pdf_backend_slot.yaml",
    "contracts/convergence_decision_report.yaml",
]

REQUIRED_V1_3_REGRESSION_SURFACES = [
    "tests/workflow/test_v1_3_full_original_parity_replay.py",
    "tests/workflow/test_v1_3_original_parity_public_demo.py",
    "tests/contract/test_v1_3_security_privacy_gate.py",
    "tests/contract/test_v1_3_release_contracts.py",
    "docs/v1.3.0-full-regression-report.md",
    "docs/v1.3.0-regression-failures.md",
]


def test_v1_4_release_docs_exist() -> None:
    missing = [path for path in REQUIRED_V1_4_DOCS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_4_release_tests_exist() -> None:
    required = [*REQUIRED_V1_4_TESTS, *REQUIRED_V1_3_REGRESSION_SURFACES]
    missing = [path for path in required if not (ROOT / path).exists()]

    assert missing == []


def test_v1_4_production_contracts_exist() -> None:
    missing = [path for path in REQUIRED_V1_4_CONTRACTS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_4_regression_report_covers_required_surfaces() -> None:
    report = (ROOT / "docs" / "v1.4.0-full-regression-report.md").read_text(
        encoding="utf-8"
    )
    required_terms = [
        "v1.3 workflows",
        "Session production parity",
        "Scholar production parity",
        "Web production parity",
        "yogsoth production parity",
        "production dashboard/docs",
        "security/privacy",
        "ARIS deferred",
        "PASS WITH REVIEW",
    ]

    for term in required_terms:
        assert term in report


def test_v1_4_regression_failures_record_no_unresolved_failures() -> None:
    failures = (ROOT / "docs" / "v1.4.0-regression-failures.md").read_text(
        encoding="utf-8"
    )

    assert "Status: no unresolved failures" in failures
    assert "none" in failures.lower()
    assert "introduce new features" in failures
    assert "enable live tests by default" in failures
    assert "enable ARIS runtime" in failures


def test_v1_4_release_boundary_does_not_claim_release_or_aris_adoption() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/v1.4.0-full-regression-report.md",
            "docs/v1.4.0-regression-failures.md",
            "docs/v1.4.0-aris-still-deferred.md",
            "docs/aris-still-deferred-v1.4.md",
            "docs/v1.4.0-security-audit.md",
            "docs/v1.4.0-privacy-audit.md",
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
        "aris adopted" + " in v1.4",
        "automatic experiment execution" + " enabled",
        "remote command execution" + " enabled",
        "fake/demo result promotion enabled",
        "live ssh enabled by default",
        "live sftp enabled by default",
    ]
    for claim in forbidden_claims:
        assert claim not in combined


def test_v1_4_release_prep_docs_cover_feature_list_and_manual_release_boundary() -> None:
    release_docs = [
        "docs/v1.4.0-release-notes.md",
        "docs/v1.4.0-feature-list.md",
        "docs/v1.4.0-known-limitations.md",
        "docs/v1.4.0-test-summary.md",
        "docs/v1.4.0-upgrade-guide.md",
        "docs/github-release-draft-v1.4.0.md",
    ]
    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in release_docs)

    required_features = [
        "Session production parity",
        "Session CLI surface",
        "Shell script equivalent export",
        "Cross-platform archive hardening",
        "Remote dry-run plan",
        "Return import human confirmation",
        "Scholar production parity",
        "Paper content/reference/reading E2E",
        "Web production parity",
        "URL normalization/cache/content fixtures",
        "Apify fake/live report",
        "yogsoth production parity",
        "Campaign/catalog/vault/ontology/stress/convergence/experiment E2E",
        "Parity dashboard v2",
    ]
    for feature in required_features:
        assert feature in combined

    assert "1.4.0rc0" in combined
    assert "Do not publish this draft automatically" in combined
    assert "No automatic GitHub release" in combined
    assert "No automatic experiment execution" in combined
    assert "ARIS features are still deferred" in combined
