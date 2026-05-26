from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)
from turing_research_plus.advisor_export.pdf_exporter import (
    build_advisor_pdf_export_plan,
    export_advisor_pdf_optional,
)
from turing_research_plus.advisor_export.pptx_exporter import (
    build_advisor_pptx_export_plan,
    export_advisor_pptx_optional,
)
from turing_research_plus.advisor_export.quality_gate import (
    ExportQualityGateRequest,
    ExportQualityStatus,
    run_export_quality_gate,
)
from turing_research_plus.benchmark.replay_runner import run_benchmark_suite
from turing_research_plus.benchmark.scenarios import built_in_scenarios
from turing_research_plus.plugins.compat_report import PluginCompatibilityStatus
from turing_research_plus.plugins.compat_test_runner import run_demo_plugin_compatibility
from turing_research_plus.plugins.loader import load_trusted_local_plugin
from turing_research_plus.plugins.permission_gate import evaluate_sandbox_permission
from turing_research_plus.plugins.sandbox_policy import (
    SandboxDecisionStatus,
    SandboxPermission,
)
from turing_research_plus.plugins.trust_policy import PluginTrustSource
from turing_research_plus.privacy.scanner import scan_privacy_paths
from turing_research_plus.quality.metrics import build_quality_report
from turing_research_plus.quality.regression_gate import run_regression_gate

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
ADVISOR_EXPORT = VGGT / "advisor_export"
TRUSTED_DEMO_PLUGIN = (
    ROOT / "examples" / "plugins" / "trusted_local_demo_plugin" / "plugin.yaml"
)


def _advisor_bundle() -> AdvisorMarkdownBundle:
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
        bundle_id="v0_7_full_replay_advisor_bundle",
        topic="VGGT public review bundle",
        output_dir=str(ADVISOR_EXPORT),
        files=[
            AdvisorBundleFile(path=str(ADVISOR_EXPORT / filename), role=filename)
            for filename in required
        ],
    )


def test_v0_7_full_fake_replay_covers_requested_surfaces(tmp_path: Path) -> None:
    plugin_loading = load_trusted_local_plugin(
        TRUSTED_DEMO_PLUGIN,
        source=PluginTrustSource.BUILT_IN_DEMO,
    )
    sandbox_execute = evaluate_sandbox_permission(SandboxPermission.EXECUTE_CODE)
    sandbox_secrets_access = evaluate_sandbox_permission(
        SandboxPermission.SECRETS_ACCESS
    )
    compatibility = run_demo_plugin_compatibility(ROOT)

    bundle = _advisor_bundle()
    pdf_plan = build_advisor_pdf_export_plan(bundle, tmp_path / "pdf")
    pptx_plan = build_advisor_pptx_export_plan(bundle, tmp_path / "pptx")
    pdf_result = export_advisor_pdf_optional(bundle, tmp_path / "pdf", force_skip=True)
    pptx_result = export_advisor_pptx_optional(
        bundle,
        tmp_path / "pptx",
        force_skip=True,
    )
    export_quality = run_export_quality_gate(
        ExportQualityGateRequest(
            advisor_export_dir=ADVISOR_EXPORT,
            dashboard_paths=[
                VGGT / "dashboard_html" / "refined_dashboard.html",
                PUBLIC_DEMO / "dashboard" / "index.html",
            ],
        )
    )

    public_demo_privacy = scan_privacy_paths([PUBLIC_DEMO])
    benchmark_reports = run_benchmark_suite(built_in_scenarios(ROOT))
    quality = build_quality_report(ROOT)
    regression = run_regression_gate(ROOT)

    compliance = (VGGT / "compliance" / "compliance_report.md").read_text(
        encoding="utf-8"
    )
    vault_ui = (VGGT / "vault_ui" / "index.html").read_text(encoding="utf-8")
    deep_review = (
        VGGT / "paper_deep_review" / "neuralbody_review_checklist.md"
    ).read_text(encoding="utf-8")
    case_study = (
        VGGT / "public_case_study" / "case_study_draft.md"
    ).read_text(encoding="utf-8")

    assert plugin_loading.loaded is True
    assert plugin_loading.executes_code is False
    assert plugin_loading.loads_entrypoint is False
    assert plugin_loading.exposed_capabilities[0].disabled_by_default is True
    assert sandbox_execute.status == SandboxDecisionStatus.DENIED
    assert sandbox_secrets_access.status == SandboxDecisionStatus.DENIED
    assert compatibility.status == PluginCompatibilityStatus.COMPATIBLE_WITH_REVIEW
    assert compatibility.executes_plugin_code is False
    assert compatibility.enables_plugin is False

    assert pdf_plan.optional_backend is True
    assert pptx_plan.optional_backend is True
    assert pdf_result.status == "skipped"
    assert pptx_result.status == "skipped"
    assert pdf_result.skipped_reason
    assert pptx_result.skipped_reason
    assert export_quality.status == ExportQualityStatus.PASS_WITH_WARNINGS
    assert export_quality.findings == []

    assert public_demo_privacy.release_blocker is False
    assert public_demo_privacy.findings == []
    assert "not legal advice" in compliance.lower()
    assert "Graph is not truth" in vault_ui
    assert "No network" in vault_ui
    assert "Reading status: `needs-real-paper`" in deep_review
    assert "No final paper conclusion is generated" in deep_review
    assert "Do not claim SparseConv3D success" in case_study
    assert "It does not claim experiment success." in case_study

    assert {report.scenario_id for report in benchmark_reports} == {
        "public_demo_replay",
        "vggt_fake_replay",
        "demo_workspace_replay",
        "paper_assembly_replay",
    }
    assert all(report.status == "pass" for report in benchmark_reports)
    assert all(report.demo_only for report in benchmark_reports)
    assert all(report.no_real_experiment for report in benchmark_reports)
    assert quality.status == "pass"
    assert regression.status == "pass"


def test_v0_7_full_fake_replay_keeps_public_demo_expansion_safe() -> None:
    for ledger in (PUBLIC_DEMO / "projects").glob("*/evidence_ledger.json"):
        payload = json.loads(ledger.read_text(encoding="utf-8"))
        statuses = {entry["status"] for entry in payload["entries"]}

        assert payload["status"] == "demo-only"
        assert payload["requires_human_review"] is True
        assert "observed" not in statuses

    dashboard = (PUBLIC_DEMO / "dashboard" / "index.html").read_text(
        encoding="utf-8"
    )
    assert "safe demo mode" in dashboard
    assert "not an experiment result" in dashboard
    assert "<script" not in dashboard.lower()
    assert "http://" not in dashboard
    assert "https://" not in dashboard


def test_v0_7_full_fake_replay_preserves_existing_v0_6_boundaries() -> None:
    v0_6_report = (ROOT / "docs" / "v0.6.0-full-replay-report.md").read_text(
        encoding="utf-8"
    )
    paper_gate = (
        VGGT / "paper_scaffold" / "paper_assembly_report.md"
    ).read_text(encoding="utf-8")

    assert "No network access." in v0_6_report
    assert "No Modal or VGGT execution." in v0_6_report
    assert "SparseConv3D success is not established." in v0_6_report
    assert "Gate status: `blocked`" in paper_gate
    assert "No final paper text is generated." in paper_gate
