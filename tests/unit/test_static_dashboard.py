from __future__ import annotations

from pathlib import Path

from turing_research_plus.ui.models import StaticDashboardRequest
from turing_research_plus.ui.static_dashboard import build_static_dashboard

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey"


def test_build_static_dashboard_writes_html_and_markdown(tmp_path: Path) -> None:
    spec = build_static_dashboard(
        StaticDashboardRequest(
            output_dir=tmp_path,
            knowledge_pack_dir=EXAMPLE / "research_knowledge_pack",
            advisor_pack_dir=EXAMPLE / "advisor_pack",
            run_dashboard_dir=EXAMPLE / "dashboard",
        )
    )

    assert len(spec.sections) == 8
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "dashboard.md").exists()
    assert spec.server_required is False
    assert spec.login_required is False
    assert spec.cloud_deployed is False


def test_build_static_dashboard_can_plan_without_writing(tmp_path: Path) -> None:
    spec = build_static_dashboard(
        StaticDashboardRequest(
            output_dir=tmp_path,
            knowledge_pack_dir=EXAMPLE / "research_knowledge_pack",
            advisor_pack_dir=EXAMPLE / "advisor_pack",
            run_dashboard_dir=EXAMPLE / "dashboard",
        ),
        write_files=False,
    )

    assert len(spec.generated_files) == 2
    assert not (tmp_path / "index.html").exists()
