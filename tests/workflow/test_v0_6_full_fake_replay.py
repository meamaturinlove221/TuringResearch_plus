from __future__ import annotations

from pathlib import Path

from turing_research_plus.benchmark.replay_runner import run_benchmark_suite
from turing_research_plus.benchmark.scenarios import built_in_scenarios
from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.cross_project.tools import workspace_cross_project_graph
from turing_research_plus.extension_safety.models import (
    ExtensionKind,
    ExtensionManifestRef,
    ExtensionPermission,
)
from turing_research_plus.extension_safety.validator import validate_extension_safety
from turing_research_plus.mcp_plugins.registry import load_mcp_plugin_registry
from turing_research_plus.mcp_plugins.validator import validate_mcp_plugin_registry
from turing_research_plus.plugins.registry import load_plugin_registry
from turing_research_plus.privacy.scanner import scan_privacy_paths
from turing_research_plus.project_template.generator import generate_research_project_template
from turing_research_plus.project_template.research_types import ResearchProjectType
from turing_research_plus.project_template.schema import ResearchProjectTemplateRequest
from turing_research_plus.quality.metrics import build_quality_report
from turing_research_plus.quality.regression_gate import run_regression_gate
from turing_research_plus.skill_market.catalog import (
    build_skill_marketplace_index,
    review_skill_marketplace,
)
from turing_research_plus.workspace.tools import workspace_overview

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
PAPER_SCAFFOLD = ROOT / "examples" / "vggt-human-prior-survey" / "paper_scaffold"


def test_v0_6_full_fake_replay_covers_major_surfaces(tmp_path: Path) -> None:
    generated = generate_research_project_template(
        ResearchProjectTemplateRequest(
            project_id="v0_6_full_fake_replay",
            project_name="v0.6 Full Fake Replay",
            topic="Fake/default replay coverage check",
            output_dir=tmp_path / "v0_6_full_fake_replay",
            template_type=ResearchProjectType.MIXED_RESEARCH_PROJECT,
            overwrite=True,
        )
    )
    workspace = workspace_overview(WORKSPACE)
    graph = workspace_cross_project_graph(WORKSPACE)
    privacy = scan_privacy_paths([PUBLIC_DEMO])
    plugins = load_plugin_registry(ROOT / "examples" / "plugins")
    mcp_registry = load_mcp_plugin_registry(
        ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml"
    )
    mcp_report = validate_mcp_plugin_registry(mcp_registry)
    capability_manifest = collect_capability_manifest()
    skill_market = build_skill_marketplace_index(ROOT / ".agents" / "skills")
    skill_report = review_skill_marketplace(skill_market, ROOT / ".agents" / "skills")
    extension_report = validate_extension_safety(
        ExtensionManifestRef(
            extension_id="v0_6_full_fake_replay_extension",
            kind=ExtensionKind.PLUGIN,
            third_party=True,
            default_enabled=False,
            requested_permissions=[
                ExtensionPermission.READ_LOCAL_FILES,
                ExtensionPermission.EXPORT_ARTIFACTS,
            ],
            declared_safety_level="public-demo",
            has_manifest=True,
            has_safety_report=True,
        )
    )
    benchmark_reports = run_benchmark_suite(built_in_scenarios(ROOT))
    quality = build_quality_report(ROOT)
    regression = run_regression_gate(ROOT)

    assert generated.requires_human_review is True
    assert generated.observed_evidence_generated is False
    assert workspace.requires_human_review is True
    assert workspace.evidence_source is False
    assert graph.requires_human_review is True
    assert all(edge.evidence_transfer is False for edge in graph.cross_project_edges)
    assert privacy.release_blocker is False
    assert all(plugin.status == "disabled" for plugin in plugins.plugins)
    assert mcp_report.valid is True
    assert mcp_report.starts_mcp_server is False
    assert mcp_report.loads_plugin_code is False
    assert capability_manifest.executes_tools is False
    assert capability_manifest.starts_mcp_server is False
    assert skill_report.valid is True
    assert skill_market.remote_publish is False
    assert extension_report.executes_extension_code is False
    assert extension_report.loads_third_party_code is False
    assert {report.scenario_id for report in benchmark_reports} == {
        "public_demo_replay",
        "vggt_fake_replay",
        "demo_workspace_replay",
        "paper_assembly_replay",
    }
    assert all(report.status == "pass" for report in benchmark_reports)
    assert all(report.no_real_experiment for report in benchmark_reports)
    assert quality.status == "pass"
    assert regression.status == "pass"


def test_v0_6_full_fake_replay_keeps_paper_assembly_blocked() -> None:
    report = (PAPER_SCAFFOLD / "paper_assembly_report.md").read_text(encoding="utf-8")
    blocked = (PAPER_SCAFFOLD / "blocked_sections.md").read_text(encoding="utf-8")

    assert "Gate status: `blocked`" in report
    assert "No final paper text is generated." in report
    assert "SparseConv3D success is not established." in blocked
    assert "No planned item is promoted to observed." in blocked
