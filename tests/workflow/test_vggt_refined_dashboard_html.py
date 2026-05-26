from __future__ import annotations

from pathlib import Path

from turing_research_plus.ui.models import StaticDashboardRequest
from turing_research_plus.ui.project_dashboard import (
    build_refined_project_dashboard,
    write_public_demo_refined_dashboard,
)

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey"
DASHBOARD_HTML = EXAMPLE / "dashboard_html"


def test_vggt_refined_dashboard_fixture_keeps_static_boundaries() -> None:
    html = (DASHBOARD_HTML / "refined_dashboard.html").read_text(encoding="utf-8")
    public_demo = (ROOT / "examples" / "public_demo" / "demo_dashboard_refined.html").read_text(
        encoding="utf-8"
    )

    assert "SAFE DEMO MODE" in html
    assert "Project Overview Cards" in html
    assert "Simple Static Search Index" in html
    assert "dashboard-search-index" in html
    assert "No login" in html
    assert "No server" in html
    assert "No network" in html
    assert "Not an experiment result" in html
    assert "VGGT" in html
    assert "SAFE DEMO MODE" in public_demo
    assert "not an experiment result" in public_demo


def test_vggt_refined_dashboard_runtime_matches_fixture_shape(tmp_path: Path) -> None:
    bundle = build_refined_project_dashboard(
        StaticDashboardRequest(
            output_dir=tmp_path,
            knowledge_pack_dir=EXAMPLE / "research_knowledge_pack",
            advisor_pack_dir=EXAMPLE / "advisor_pack",
            run_dashboard_dir=EXAMPLE / "dashboard",
        )
    )

    assert len(bundle.navigation) == 8
    assert len(bundle.cards) == 8
    assert len(bundle.search_index) == 16
    assert bundle.safe_demo_mode is True
    assert bundle.server_required is False
    assert bundle.login_required is False
    assert bundle.network_required is False
    assert bundle.ui_executed_experiment is False
    assert (tmp_path / "refined_dashboard.html").exists()


def test_public_demo_refined_dashboard_writer(tmp_path: Path) -> None:
    output = write_public_demo_refined_dashboard(tmp_path / "demo_dashboard_refined.html")
    html = output.read_text(encoding="utf-8")

    assert output.exists()
    assert "TuringResearch Public Demo Refined Dashboard" in html
    assert "SAFE DEMO MODE" in html
    assert "No login, no server, no network" in html
