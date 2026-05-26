from __future__ import annotations

from pathlib import Path

from turing_research_plus.ui.models import StaticDashboardRequest
from turing_research_plus.ui.static_dashboard import build_static_dashboard

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey"
DASHBOARD_HTML = EXAMPLE / "dashboard_html"


def test_vggt_dashboard_html_fixture_exists_and_keeps_boundaries() -> None:
    html = (DASHBOARD_HTML / "index.html").read_text(encoding="utf-8")
    markdown = (DASHBOARD_HTML / "dashboard.md").read_text(encoding="utf-8")

    assert "VGGT Research Dashboard" in html
    assert "No Modal execution" in html
    assert "No VGGT execution" in html
    assert "Not an experiment result" in html
    assert "SparseConv3D success is not claimed" in html
    assert "## Run Dashboard" in markdown
    assert "## Advisor Next Actions" in markdown


def test_vggt_dashboard_html_runtime_matches_fixture_shape(tmp_path: Path) -> None:
    spec = build_static_dashboard(
        StaticDashboardRequest(
            output_dir=tmp_path,
            knowledge_pack_dir=EXAMPLE / "research_knowledge_pack",
            advisor_pack_dir=EXAMPLE / "advisor_pack",
            run_dashboard_dir=EXAMPLE / "dashboard",
        )
    )

    assert [section.kind.value for section in spec.sections] == [
        "project_overview",
        "evidence_status",
        "artifact_completeness",
        "visual_readiness",
        "run_dashboard",
        "related_work",
        "failure_taxonomy",
        "advisor_next_actions",
    ]
    assert (tmp_path / "index.html").exists()
    assert spec.ui_executed_experiment is False
