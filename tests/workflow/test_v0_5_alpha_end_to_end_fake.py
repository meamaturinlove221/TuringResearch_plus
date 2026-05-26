from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.export_manifest import (
    build_advisor_export_manifest,
)
from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)
from turing_research_plus.project_template.generator import generate_project_template
from turing_research_plus.project_template.models import ProjectTemplateRequest
from turing_research_plus.ui.models import StaticDashboardRequest
from turing_research_plus.ui.static_dashboard import build_static_dashboard

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"
PUBLIC_DEMO = ROOT / "examples" / "public_demo"


def _advisor_bundle() -> AdvisorMarkdownBundle:
    root = VGGT / "advisor_export"
    required = [
        "advisor_report_source.md",
        "slides_outline.md",
        "figure_list.md",
        "table_list.md",
        "evidence_refs.md",
        "limitations.md",
        "next_actions.md",
        "manifest.yaml",
    ]
    return AdvisorMarkdownBundle(
        bundle_id="v0_5_alpha_advisor_bundle",
        topic="VGGT / SMPL-X Human Prior",
        output_dir=str(root),
        files=[
            AdvisorBundleFile(path=str(root / filename), role=filename)
            for filename in required
        ],
    )


def test_v0_5_alpha_fake_end_to_end_generates_local_outputs(tmp_path: Path) -> None:
    dashboard = build_static_dashboard(
        StaticDashboardRequest(
            output_dir=tmp_path / "dashboard",
            knowledge_pack_dir=VGGT / "research_knowledge_pack",
            advisor_pack_dir=VGGT / "advisor_pack",
            run_dashboard_dir=VGGT / "dashboard",
        )
    )
    export_manifest = build_advisor_export_manifest(
        _advisor_bundle(),
        tmp_path / "advisor_export_plan",
    )
    template = generate_project_template(
        ProjectTemplateRequest(
            project_id="v0_5_alpha_demo_project",
            project_name="v0.5 Alpha Demo Project",
            topic="Fake integration project",
            output_dir=tmp_path / "project_template",
        )
    )

    assert (tmp_path / "dashboard" / "index.html").exists()
    assert (tmp_path / "advisor_export_plan" / "export_manifest.yaml").exists()
    assert (tmp_path / "project_template" / "README.md").exists()
    assert dashboard.requires_human_review is True
    assert export_manifest.generated_binary_exports is False
    assert template.requires_human_review is True


def test_v0_5_alpha_public_demo_and_replay_boundaries_exist() -> None:
    demo_readme = (PUBLIC_DEMO / "README.md").read_text(encoding="utf-8")
    replay_manifest = (
        VGGT / "dogfooding_replay" / "replay_manifest.yaml"
    ).read_text(encoding="utf-8")

    assert "All data is fake/demo" in demo_readme
    assert "vggt_experiment_run: false" in replay_manifest
    assert "modal_run: false" in replay_manifest
    assert "sparseconv3d_success_claimed: false" in replay_manifest


def test_v0_5_alpha_no_fake_result_marked_observed_in_demo_suite() -> None:
    evidence = (PUBLIC_DEMO / "demo_evidence_ledger.json").read_text(encoding="utf-8")

    assert '"status": "demo-only"' in evidence
    assert '"status": "fake-data"' in evidence
    assert '"status": "observed"' not in evidence
