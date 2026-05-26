from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_V1_3_DOCS = [
    "docs/v1.3.0-full-original-parity-scope.md",
    "docs/v1.3.0-original-parity-implementation-order.md",
    "docs/runtime-gap-audit.md",
    "docs/original-reference-tool-surface-audit.md",
    "docs/v1.3.0-aris-deferral-reconfirm.md",
    "docs/aris-implementation-blocklist-v1.3.md",
    "docs/session-runtime-gate-report.md",
    "docs/scholar-web-parity-gate-report.md",
    "docs/yogsoth-full-parity-gate-report.md",
    "docs/v1.3.0-full-original-parity-replay-report.md",
    "docs/original-reference-parity-summary.md",
    "docs/reference-parity-dashboard.md",
    "docs/v1.3.0-security-audit.md",
    "docs/v1.3.0-privacy-audit.md",
    "docs/v1.3.0-secret-scan-report.md",
    "docs/v1.3.0-full-regression-report.md",
    "docs/v1.3.0-regression-failures.md",
    "docs/v1.3.0-release-notes.md",
    "docs/v1.3.0-feature-list.md",
    "docs/v1.3.0-known-limitations.md",
    "docs/v1.3.0-test-summary.md",
    "docs/v1.3.0-upgrade-guide.md",
    "docs/github-release-draft-v1.3.0.md",
]

REQUIRED_V1_3_TESTS = [
    "tests/workflow/test_session_runtime_gate.py",
    "tests/workflow/test_scholar_web_parity_gate.py",
    "tests/workflow/test_yogsoth_full_parity_gate.py",
    "tests/workflow/test_v1_3_full_original_parity_replay.py",
    "tests/workflow/test_v1_3_original_parity_public_demo.py",
    "tests/contract/test_v1_3_security_privacy_gate.py",
    "tests/contract/test_aris_deferred_in_v1_3.py",
    "tests/contract/test_v1_3_release_contracts.py",
]

REQUIRED_V1_3_CONTRACTS = [
    "contracts/session_preflight_runner.yaml",
    "contracts/context_pack_builder_runtime.yaml",
    "contracts/optional_sftp_transfer_runner.yaml",
    "contracts/remote_return_verifier_runtime.yaml",
    "contracts/scholar_full_tool_surface.yaml",
    "contracts/web_full_tool_surface.yaml",
    "contracts/campaign_execution_trace.yaml",
    "contracts/convergence_decision_report.yaml",
]

REQUIRED_V1_2_REGRESSION_SURFACES = [
    "tests/workflow/test_v1_2_full_fake_replay.py",
    "tests/workflow/test_v1_2_public_demo.py",
    "tests/contract/test_v1_2_security_privacy_gate.py",
    "tests/contract/test_v1_2_release_contracts.py",
    "docs/v1.2.0-full-regression-report.md",
    "docs/v1.2.0-regression-failures.md",
]


def test_v1_3_release_docs_exist() -> None:
    missing = [path for path in REQUIRED_V1_3_DOCS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_3_release_tests_exist() -> None:
    required = [*REQUIRED_V1_3_TESTS, *REQUIRED_V1_2_REGRESSION_SURFACES]
    missing = [path for path in required if not (ROOT / path).exists()]

    assert missing == []


def test_v1_3_original_parity_contracts_exist() -> None:
    missing = [path for path in REQUIRED_V1_3_CONTRACTS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_3_regression_report_covers_required_surfaces() -> None:
    report = (ROOT / "docs" / "v1.3.0-full-regression-report.md").read_text(
        encoding="utf-8"
    )
    required_terms = [
        "v1.2 workflows",
        "session runtime parity",
        "scholar/web parity",
        "yogsoth parity",
        "original parity demo",
        "security/privacy",
        "ARIS deferred",
        "PASS WITH REVIEW",
    ]

    for term in required_terms:
        assert term in report


def test_v1_3_regression_failures_record_no_unresolved_failures() -> None:
    failures = (ROOT / "docs" / "v1.3.0-regression-failures.md").read_text(
        encoding="utf-8"
    )

    assert "Status: no unresolved failures" in failures
    assert "none" in failures.lower()
    assert "introduce new features" in failures
    assert "enable live tests by default" in failures
    assert "enable ARIS runtime" in failures


def test_v1_3_release_boundary_does_not_claim_release_or_aris_adoption() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/v1.3.0-full-regression-report.md",
            "docs/v1.3.0-regression-failures.md",
            "docs/v1.3.0-aris-deferral-reconfirm.md",
            "docs/v1.3.0-security-audit.md",
            "docs/v1.3.0-privacy-audit.md",
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
        "aris adopted" + " in v1.3",
        "automatic experiment execution" + " enabled",
        "remote command execution" + " enabled",
        "fake/demo result promotion enabled",
        "live ssh enabled by default",
    ]
    for claim in forbidden_claims:
        assert claim not in combined


def test_v1_3_release_prep_docs_cover_feature_list_and_manual_release_boundary() -> None:
    release_docs = [
        "docs/v1.3.0-release-notes.md",
        "docs/v1.3.0-feature-list.md",
        "docs/v1.3.0-known-limitations.md",
        "docs/v1.3.0-test-summary.md",
        "docs/v1.3.0-upgrade-guide.md",
        "docs/github-release-draft-v1.3.0.md",
    ]
    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in release_docs)

    required_features = [
        "Full original reference parity scope",
        "Session runtime parity",
        "Context pack runtime",
        "Optional SFTP transfer fake-first",
        "Remote return verifier",
        "Scholar full tool surface",
        "Web full tool surface",
        "MCP tool parity",
        "Campaign execution trace",
        "Research Catalog dashboard",
        "Vault wiki demo",
        "Ontology runbook demo",
        "Stress scenario library",
        "Convergence decision report",
        "Original parity public demo",
        "ARIS still deferred",
    ]
    for feature in required_features:
        assert feature in combined

    assert "1.3.0rc0" in combined
    assert "Do not publish this draft automatically" in combined
    assert "No automatic GitHub release" in combined
    assert "No automatic experiment execution" in combined
    assert "ARIS features are still deferred" in combined
