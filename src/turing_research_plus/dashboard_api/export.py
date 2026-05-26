"""JSON export helpers for the read-only dashboard data API."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard_api.artifact_summary import build_artifact_summary
from turing_research_plus.dashboard_api.evidence_summary import build_evidence_summary
from turing_research_plus.dashboard_api.models import DashboardDataBundle
from turing_research_plus.dashboard_api.paper_summary import build_paper_summary
from turing_research_plus.dashboard_api.project_summary import build_project_summary


def build_public_demo_dashboard_data(public_demo_dir: Path) -> DashboardDataBundle:
    """Build a unified dashboard data bundle from public demo files."""

    source_paths = [
        public_demo_dir / "demo_research_intent.md",
        public_demo_dir / "demo_evidence_ledger.json",
        public_demo_dir / "demo_artifact_index.md",
        public_demo_dir / "demo_related_work.md",
        public_demo_dir / "demo_advisor_pack.md",
    ]
    return DashboardDataBundle(
        bundle_id="public_demo_dashboard_data",
        project=build_project_summary(source_paths[0]),
        evidence=build_evidence_summary(source_paths[1]),
        artifacts=build_artifact_summary(source_paths[2]),
        paper=build_paper_summary(source_paths[3], source_paths[4]),
        source_paths=[str(path) for path in source_paths],
    )


def export_json(bundle: DashboardDataBundle) -> str:
    """Export a dashboard data bundle as JSON."""

    return bundle.model_dump_json(indent=2)
