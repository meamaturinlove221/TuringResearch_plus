from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_V1_5_DOCS = [
    "docs/v1.5.0-final-scope.md",
    "docs/v1.5.0-docs-sprint-gate-report.md",
    "docs/v1.5.0-split-sprint-gate-report.md",
    "docs/v1.5.0-optional-live-sprint-gate-report.md",
    "docs/v1.5.0-dashboard-ux-gate-report.md",
    "docs/v1.5.0-full-replay-report.md",
    "docs/v1.5.0-security-audit.md",
    "docs/v1.5.0-privacy-audit.md",
    "docs/v1.5.0-secret-scan-report.md",
    "docs/v1.5.0-release-notes.md",
    "docs/v1.5.0-feature-list.md",
    "docs/v1.5.0-known-limitations.md",
    "docs/v1.5.0-test-summary.md",
    "docs/v1.5.0-upgrade-guide.md",
    "docs/github-release-draft-v1.5.0.md",
]

REQUIRED_V1_5_TESTS = [
    "tests/workflow/test_v1_5_docs_sprint_gate.py",
    "tests/workflow/test_v1_5_split_sprint_gate.py",
    "tests/workflow/test_v1_5_optional_live_sprint_gate.py",
    "tests/workflow/test_v1_5_dashboard_ux_gate.py",
    "tests/workflow/test_v1_5_full_replay.py",
    "tests/contract/test_v1_5_security_privacy_gate.py",
    "tests/contract/test_v1_5_release_contracts.py",
]

REQUIRED_V1_5_ARTIFACTS = [
    "docs-site/dist_manifest.yaml",
    "docs-site/deployment_dry_run_report.md",
    "split_manual/turingresearch-vggt-case/manifest.yaml",
    "split_manual/turingresearch-examples/manifest.yaml",
    "examples/public_demo/dashboard_showcase/landing.html",
    "examples/public_demo/dashboard_showcase/parity.html",
    "examples/public_demo/dashboard_showcase/interview.html",
]


def test_v1_5_release_docs_exist() -> None:
    missing = [path for path in REQUIRED_V1_5_DOCS if not (ROOT / path).exists()]

    assert missing == []


def test_v1_5_release_tests_and_artifacts_exist() -> None:
    required = [*REQUIRED_V1_5_TESTS, *REQUIRED_V1_5_ARTIFACTS]
    missing = [path for path in required if not (ROOT / path).exists()]

    assert missing == []


def test_v1_5_full_replay_report_covers_required_surfaces() -> None:
    report = (ROOT / "docs" / "v1.5.0-full-replay-report.md").read_text(
        encoding="utf-8"
    )
    required_terms = [
        "docs deployment dry-run",
        "split manual packs",
        "optional live safety",
        "dashboard showcase",
        "v1.4 production parity",
        "ARIS remains deferred",
        "PASS WITH REVIEW",
    ]

    for term in required_terms:
        assert term in report


def test_v1_5_release_docs_cover_feature_list_and_manual_release_boundary() -> None:
    release_docs = [
        "docs/v1.5.0-release-notes.md",
        "docs/v1.5.0-feature-list.md",
        "docs/v1.5.0-known-limitations.md",
        "docs/v1.5.0-test-summary.md",
        "docs/v1.5.0-upgrade-guide.md",
        "docs/github-release-draft-v1.5.0.md",
    ]
    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in release_docs)

    required_features = [
        "Docs deployment dry-run",
        "Docs navigation polish",
        "Split repo manual packs",
        "Optional live Scholar/Web/SFTP polish",
        "Live safety gate",
        "Dashboard landing page",
        "Parity showcase view",
        "Interview demo view",
    ]
    for feature in required_features:
        assert feature in combined

    assert "1.5.0rc0" in combined
    assert "Do not publish this draft automatically" in combined
    assert "No automatic public deployment" in combined
    assert "No automatic child repository creation" in combined
    assert "No automatic experiment execution" in combined
    assert "ARIS remains intentionally deferred" in combined


def test_v1_5_release_boundary_does_not_claim_release_or_live_success() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/v1.5.0-release-notes.md",
            "docs/v1.5.0-known-limitations.md",
            "docs/v1.5.0-full-replay-report.md",
            "docs/v1.5.0-security-audit.md",
            "docs/v1.5.0-privacy-audit.md",
            "docs/github-release-draft-v1.5.0.md",
        ]
    ).lower()

    required_boundaries = [
        "not publish",
        "no automatic public deployment",
        "no automatic child repository creation",
        "no live provider call",
        "human review",
        "aris remains deferred",
    ]
    for boundary in required_boundaries:
        assert boundary in combined

    forbidden_claims = [
        "public site is live",
        "child repositories created",
        "live provider succeeded",
        "remote command execution enabled",
        "fake/demo result promotion enabled",
        "aris implemented",
    ]
    for claim in forbidden_claims:
        assert claim not in combined
