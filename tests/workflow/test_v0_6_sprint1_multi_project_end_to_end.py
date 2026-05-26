from __future__ import annotations

from pathlib import Path

from turing_research_plus.cross_project.tools import (
    workspace_cross_project_graph,
    workspace_cross_project_markdown,
)
from turing_research_plus.privacy.models import PrivacyFindingType
from turing_research_plus.privacy.scanner import scan_privacy_paths
from turing_research_plus.project_template.generator import generate_research_project_template
from turing_research_plus.project_template.research_types import ResearchProjectType
from turing_research_plus.project_template.schema import ResearchProjectTemplateRequest
from turing_research_plus.workspace.tools import workspace_overview_markdown

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"
PUBLIC_DEMO = ROOT / "examples" / "public_demo"


def test_v0_6_sprint1_template_to_workspace_graph_privacy_overview(tmp_path: Path) -> None:
    generated = generate_research_project_template(
        ResearchProjectTemplateRequest(
            project_id="integration_demo_project",
            project_name="Integration Demo Project",
            topic="Fake v0.6 Sprint 1 integration",
            output_dir=tmp_path / "integration_demo_project",
            template_type=ResearchProjectType.MIXED_RESEARCH_PROJECT,
            overwrite=True,
        )
    )
    graph = workspace_cross_project_graph(WORKSPACE)
    graph_markdown = workspace_cross_project_markdown(WORKSPACE)
    privacy = scan_privacy_paths([PUBLIC_DEMO])
    overview = workspace_overview_markdown(WORKSPACE)

    assert generated.requires_human_review is True
    assert generated.network_used is False
    assert generated.observed_evidence_generated is False
    assert graph.requires_human_review is True
    assert graph.evidence_source is False
    assert graph.cross_project_edges
    assert all(edge.evidence_transfer is False for edge in graph.cross_project_edges)
    assert "not a source of evidence" in graph_markdown
    assert privacy.release_blocker is False
    assert privacy.findings == []
    assert "Workspace index is not an evidence source" in overview
    assert "D:/vggt" not in overview


def test_v0_6_sprint1_privacy_gate_flags_unsafe_without_deleting(tmp_path: Path) -> None:
    unsafe = tmp_path / "unsafe_export"
    unsafe.mkdir()
    env_file = unsafe / ".env"
    links = unsafe / "local_project_links.yaml"
    env_file.write_text("APIFY_TOKEN=abc123456789\n", encoding="utf-8")
    links.write_text("project: private\n", encoding="utf-8")
    private_data = unsafe / "private_data"
    private_data.mkdir()
    raw_file = private_data / "raw_notes.md"
    raw_file.write_text("raw data path: private_data/run001\n", encoding="utf-8")

    report = scan_privacy_paths([unsafe])
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.release_blocker is True
    assert PrivacyFindingType.ENV_FILE in finding_types
    assert PrivacyFindingType.TOKEN_PATTERN in finding_types
    assert PrivacyFindingType.LOCAL_PROJECT_LINKS in finding_types
    assert PrivacyFindingType.PRIVATE_DATA_PATH in finding_types
    assert PrivacyFindingType.RAW_DATA in finding_types
    assert env_file.exists()
    assert links.exists()
    assert raw_file.exists()
