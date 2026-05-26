from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REPORT = ROOT / "docs" / "v1.6.0-full-regression-report.md"
FAILURES = ROOT / "docs" / "v1.6.0-regression-failures.md"
LANE = ROOT / "lanes" / "364_v1.6_full_regression.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined(paths: list[Path]) -> str:
    return "\n".join(_text(path) for path in paths)


def test_v1_6_full_replay_required_reports_exist() -> None:
    required = [
        REPORT,
        FAILURES,
        LANE,
        ROOT / "docs" / "v1.6.0-docs-deployment-gate-report.md",
        ROOT / "docs" / "docs-release-bundle.md",
        ROOT / "docs" / "split-final-safety-refresh-v1.6.md",
        ROOT / "docs" / "optional-live-safety-gate.md",
        ROOT / "docs" / "local-install-smoke.md",
        ROOT / "docs" / "open-source-hygiene-gate-report.md",
        ROOT / "docs" / "v1.6.0-aris-still-deferred.md",
        ROOT / "docs" / "public-launch-checklist-v1.6.md",
    ]

    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]

    assert missing == []


def test_v1_6_full_replay_covers_required_scopes() -> None:
    text = _combined([REPORT, LANE])

    required = [
        "docs deployment",
        "split manual pack",
        "optional live smoke",
        "package readiness",
        "dashboard showcase",
        "release artifact",
        "privacy/security",
        "ARIS remains deferred",
        "PASS WITH REVIEW",
    ]
    for term in required:
        assert term in text


def test_v1_6_full_replay_evidence_surfaces_are_present_and_review_only() -> None:
    release_manifest = ROOT / "docs-site" / "release_bundle_manifest.yaml"
    screenshot_manifest = ROOT / "assets" / "screenshots" / "SCREENSHOT_MANIFEST.yaml"
    dashboard_pages = [
        ROOT / "examples" / "public_demo" / "dashboard_showcase" / "landing.html",
        ROOT / "examples" / "public_demo" / "dashboard_showcase" / "parity.html",
        ROOT / "examples" / "public_demo" / "dashboard_showcase" / "interview.html",
    ]
    split_packs = [
        ROOT / "split_manual" / "turingresearch-vggt-case" / "manifest.yaml",
        ROOT / "split_manual" / "turingresearch-examples" / "manifest.yaml",
    ]

    required_files = [release_manifest, screenshot_manifest, *dashboard_pages, *split_packs]
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.exists()]

    assert missing == []
    assert "public_url: none" in _text(release_manifest)
    assert "placeholder_pending_capture" in _text(screenshot_manifest)

    dashboard = _combined(dashboard_pages)
    assert "static-local-first" in dashboard
    assert "<script" not in dashboard.lower()


def test_v1_6_full_replay_blocks_live_publication_and_remote_execution() -> None:
    combined = _combined(
        [
            REPORT,
            FAILURES,
            ROOT / "docs" / "optional-live-safety-gate.md",
            ROOT / "docs" / "public-launch-go-no-go-v1.6.md",
            ROOT / "docs" / "v1.6.0-what-is-not-ready.md",
        ]
    ).lower()

    required = [
        "no automatic publication",
        "no github pages deployment",
        "no split repository creation",
        "no live provider",
        "no ssh/sftp",
        "no remote command execution",
        "no aris implementation",
    ]
    for term in required:
        assert term in combined


def test_v1_6_full_replay_failures_report_has_no_open_code_blocker() -> None:
    text = _text(FAILURES)

    assert "No Round 386 implementation blocker is recorded." in text
    assert "no open failure" in text
    assert "no PyPI publication" in text
    assert "no GitHub Pages deployment" in text


def test_v1_6_full_replay_public_surfaces_have_no_sensitive_markers() -> None:
    combined = _combined(
        [
            REPORT,
            FAILURES,
            ROOT / "docs" / "public-launch-checklist-v1.6.md",
            ROOT / "docs" / "public-launch-go-no-go-v1.6.md",
            ROOT / "docs" / "public-launch-human-actions-v1.6.md",
            ROOT / "assets" / "screenshots" / "SCREENSHOT_MANIFEST.yaml",
        ]
    )

    old_name = "Tul" + "ingResearch"
    forbidden = [
        old_name,
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "ghp_",
        "github_pat_",
        "BEGIN OPENSSH PRIVATE KEY",
        "status" + ": observed",
        "deployed at",
        "live URL:",
    ]
    for marker in forbidden:
        assert marker not in combined
