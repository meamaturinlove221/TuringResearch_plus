from __future__ import annotations

from pathlib import Path

from turing_research_plus.ui.showcase_landing import (
    build_showcase_landing_page,
    render_showcase_landing_html,
    write_showcase_landing,
)

ROOT = Path(__file__).resolve().parents[2]
LANDING = ROOT / "examples" / "public_demo" / "dashboard_showcase" / "landing.html"
DOC = ROOT / "docs" / "dashboard-landing-page.md"
LANE = ROOT / "lanes" / "329_dashboard_landing_page.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_dashboard_landing_page_model_contains_required_sections() -> None:
    page = build_showcase_landing_page()

    assert page.status == "static-local-first-demo"
    assert [section.title for section in page.sections] == [
        "Project Pitch",
        "Quickstart",
        "Original Parity Status",
        "Public Demo",
        "Docs Site",
        "Split Repo Readiness",
        "Safety Boundary",
    ]
    assert "No default network access." in page.safety_boundaries
    assert "No automatic Evidence Ledger write." in page.safety_boundaries


def test_dashboard_landing_page_example_matches_renderer() -> None:
    expected = render_showcase_landing_html()

    assert LANDING.exists()
    assert _text(LANDING) == expected
    assert "<script" not in expected.lower()
    assert "http://" not in expected
    assert "https://" not in expected
    assert "analytics" in expected


def test_dashboard_landing_page_contains_requested_content() -> None:
    html = _text(LANDING)
    docs = _text(DOC)
    lane = _text(LANE)
    combined = "\n".join([html, docs, lane])

    required = [
        "Project Pitch",
        "Quickstart",
        "Original Parity Status",
        "Public Demo",
        "Docs Site",
        "Split Repo Readiness",
        "Safety Boundary",
        "static-local-first",
        "human review required",
    ]
    for term in required:
        assert term in combined


def test_dashboard_landing_page_write_helper(tmp_path: Path) -> None:
    output = write_showcase_landing(tmp_path / "landing.html")

    assert output.exists()
    assert output.read_text(encoding="utf-8") == render_showcase_landing_html()


def test_dashboard_landing_page_public_safety() -> None:
    combined = "\n".join([_text(LANDING), _text(DOC), _text(LANE)])
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

    assert "No live provider call" in combined
    assert "No remote command execution" in combined
    assert "No planned or demo output promoted to observed evidence" in combined
