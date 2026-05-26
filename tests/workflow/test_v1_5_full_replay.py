from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs" / "v1.5.0-full-replay-report.md"
LANE = ROOT / "lanes" / "333_v1.5_full_replay.md"

DOCS_GATE = ROOT / "docs" / "v1.5.0-docs-sprint-gate-report.md"
SPLIT_GATE = ROOT / "docs" / "v1.5.0-split-sprint-gate-report.md"
LIVE_GATE = ROOT / "docs" / "v1.5.0-optional-live-sprint-gate-report.md"
DASHBOARD_GATE = ROOT / "docs" / "v1.5.0-dashboard-ux-gate-report.md"
V14_REPLAY = ROOT / "docs" / "v1.4.0-full-production-replay-report.md"
ARIS_DEFERRED = ROOT / "docs" / "v1.5.0-aris-still-deferred.md"

DIST_MANIFEST = ROOT / "docs-site" / "dist_manifest.yaml"
SPLIT_PACKS = [
    ROOT / "split_manual" / "turingresearch-vggt-case",
    ROOT / "split_manual" / "turingresearch-examples",
]
SHOWCASE_PAGES = [
    ROOT / "examples" / "public_demo" / "dashboard_showcase" / "landing.html",
    ROOT / "examples" / "public_demo" / "dashboard_showcase" / "parity.html",
    ROOT / "examples" / "public_demo" / "dashboard_showcase" / "interview.html",
]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined(paths: list[Path]) -> str:
    return "\n".join(_text(path) for path in paths)


def test_v1_5_full_replay_required_artifacts_exist() -> None:
    required = [
        REPORT,
        LANE,
        DOCS_GATE,
        SPLIT_GATE,
        LIVE_GATE,
        DASHBOARD_GATE,
        V14_REPLAY,
        ARIS_DEFERRED,
        DIST_MANIFEST,
        *SHOWCASE_PAGES,
    ]
    for path in required:
        assert path.exists()

    for pack in SPLIT_PACKS:
        assert (pack / "README.md").exists()
        assert (pack / "CREATE_REPO_MANUALLY.md").exists()
        assert (pack / "PUSH_COMMANDS.md").exists()
        assert (pack / "SAFETY_CHECKLIST.md").exists()
        assert (pack / "GIT_INIT_DRY_RUN.md").exists()
        assert (pack / "RELEASE_CHECKLIST.md").exists()
        assert (pack / "manifest.yaml").exists()


def test_v1_5_full_replay_records_all_required_scopes() -> None:
    text = _combined([REPORT, LANE])

    required = [
        "docs deployment dry-run",
        "split manual packs",
        "optional live safety",
        "dashboard showcase",
        "v1.4 production parity",
        "ARIS remains deferred",
        "PASS WITH REVIEW",
    ]
    for term in required:
        assert term in text


def test_v1_5_full_replay_gate_decisions_are_consistent() -> None:
    combined = _combined(
        [DOCS_GATE, SPLIT_GATE, LIVE_GATE, DASHBOARD_GATE, V14_REPLAY, ARIS_DEFERRED]
    )

    required = [
        "GO for docs deployment prep",
        "NO-GO for automatic public deployment",
        "GO FOR HUMAN REVIEW / NO-GO FOR AUTOMATIC SPLIT EXECUTION",
        "GO FOR OPTIONAL LIVE POLISH / NO-GO FOR DEFAULT LIVE",
        "GO FOR DASHBOARD SHOWCASE / NO-GO FOR DEPLOYMENT OR LIVE UI",
        "PASS WITH REVIEW",
        "ARIS remains a future reference",
    ]
    for term in required:
        assert term in combined


def test_v1_5_full_replay_dry_run_and_showcase_are_static() -> None:
    manifest = _text(DIST_MANIFEST)
    showcase = _combined(SHOWCASE_PAGES)

    assert "deployment_performed: false" in manifest
    assert "public_url: none" in manifest
    assert "static-local-first" in showcase
    assert "<script" not in showcase.lower()
    assert "http://" not in showcase
    assert "https://" not in showcase


def test_v1_5_full_replay_blocks_automation_and_live_claims() -> None:
    combined = _combined([REPORT, LANE, DOCS_GATE, SPLIT_GATE, LIVE_GATE, DASHBOARD_GATE])

    required = [
        "No public deployment",
        "No real public URL",
        "No analytics",
        "No external repository creation",
        "No external push",
        "No live provider call",
        "No SSH or SFTP connection",
        "No remote command execution",
        "No experiment execution",
        "No Evidence Ledger mutation",
        "No ARIS implementation",
    ]
    for term in required:
        assert term in combined


def test_v1_5_full_replay_has_no_sensitive_material_or_old_name() -> None:
    combined = _combined(
        [
            REPORT,
            LANE,
            DOCS_GATE,
            SPLIT_GATE,
            LIVE_GATE,
            DASHBOARD_GATE,
            V14_REPLAY,
            ARIS_DEFERRED,
            DIST_MANIFEST,
            *SHOWCASE_PAGES,
        ]
    )
    old_name = "Tuling" + "Research"

    forbidden = [
        old_name,
        "D:" + "/vggt",
        "D:" + "\\vggt",
        "local_project_links" + ".yaml",
        "ghp_",
        "github_pat_",
        "sk-",
        "BEGIN OPENSSH PRIVATE KEY",
        "status" + ": observed",
        "deployed at",
        "live URL:",
    ]
    for marker in forbidden:
        assert marker not in combined
