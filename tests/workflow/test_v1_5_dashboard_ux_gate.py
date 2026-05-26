from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs" / "v1.5.0-dashboard-ux-gate-report.md"
LANE = ROOT / "lanes" / "332_dashboard_ux_gate.md"

DOCS = [
    ROOT / "docs" / "dashboard-ux-showcase-scope.md",
    ROOT / "docs" / "dashboard-showcase-navigation.md",
    ROOT / "docs" / "dashboard-showcase-non-goals.md",
    ROOT / "docs" / "dashboard-landing-page.md",
    ROOT / "docs" / "parity-showcase-view.md",
    ROOT / "docs" / "interview-demo-dashboard-view.md",
    REPORT,
    LANE,
]

HTML_PAGES = [
    ROOT / "examples" / "public_demo" / "dashboard_showcase" / "landing.html",
    ROOT / "examples" / "public_demo" / "dashboard_showcase" / "parity.html",
    ROOT / "examples" / "public_demo" / "dashboard_showcase" / "interview.html",
]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined(paths: list[Path]) -> str:
    return "\n".join(_text(path) for path in paths)


def test_dashboard_ux_gate_artifacts_exist() -> None:
    for path in [*DOCS, *HTML_PAGES]:
        assert path.exists()


def test_dashboard_ux_gate_records_sprint_inputs_and_decision() -> None:
    text = _combined([REPORT, LANE])

    assert "GO FOR DASHBOARD SHOWCASE / NO-GO FOR DEPLOYMENT OR LIVE UI" in text
    assert "Dashboard UX scope" in text
    assert "Dashboard landing page" in text
    assert "Parity showcase view" in text
    assert "Interview demo view" in text


def test_dashboard_ux_gate_showcase_pages_are_static_local_first() -> None:
    combined = _combined(HTML_PAGES)

    assert "<!doctype html>" in combined
    assert "static-local-first" in combined
    assert "<script" not in combined.lower()
    assert "http://" not in combined
    assert "https://" not in combined
    assert "analytics" in combined
    assert "no public deployment" in combined.lower()


def test_dashboard_ux_gate_required_content_is_visible() -> None:
    combined = _combined([*HTML_PAGES, REPORT])

    required = [
        "Project Pitch",
        "Quickstart",
        "Original Parity Status",
        "Public Demo",
        "Docs Site",
        "Split Repo Readiness",
        "Safety Boundary",
        "upstream capability",
        "our equivalent",
        "safety enhancement",
        "deferred items",
        "Architecture",
        "Modules",
        "Tests / Contracts",
        "Why ARIS Deferred",
        "ARIS deferred",
    ]
    for term in required:
        assert term in combined


def test_dashboard_ux_gate_blocks_runtime_and_deployment_claims() -> None:
    combined = _combined([REPORT, LANE, *HTML_PAGES])
    combined_lower = combined.lower()

    required_boundaries = [
        "No live provider call",
        "No remote command execution",
        "No Evidence Ledger mutation",
        "No fake/demo result promotion",
    ]
    for item in required_boundaries:
        assert item in combined

    for item in ["no javascript", "no analytics", "no external assets"]:
        assert item in combined_lower

    assert "deployed product" in combined
    assert "site" in combined
    assert "autonomous research runtime" in combined


def test_dashboard_ux_gate_has_no_sensitive_material_or_old_name() -> None:
    combined = _combined([*DOCS, *HTML_PAGES])
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
