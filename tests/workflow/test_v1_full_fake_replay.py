from __future__ import annotations

import importlib
import json
from pathlib import Path

from tests.workflow.test_v1_benchmark_replay import load_v1_public_demo_scenario

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
from turing_research_plus.benchmark.replay_runner import run_benchmark_scenario
from turing_research_plus.plugins.permission_gate import evaluate_sandbox_permission
from turing_research_plus.plugins.sandbox_policy import (
    SandboxDecisionStatus,
    SandboxPermission,
)
from turing_research_plus.privacy.scanner import scan_privacy_paths

ROOT = Path(__file__).resolve().parents[2]
PUBLIC_DEMO = ROOT / "examples" / "public_demo"
VGGT = ROOT / "examples" / "vggt-human-prior-survey"
ADVISOR_EXPORT = VGGT / "advisor_export"
SPLIT_READY = ROOT / "split_ready"

NAMESPACES = [
    "turing_research_plus",
    "turing_research_core",
    "turing_research_paper",
    "turing_research_artifact",
    "turing_research_experiment",
    "turing_research_dashboard",
    "turing_research_plugins",
    "turing_research_cases",
]


def _advisor_bundle() -> AdvisorMarkdownBundle:
    files = [
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
        bundle_id="v1_full_fake_replay_advisor_bundle",
        topic="VGGT public review bundle",
        output_dir=str(ADVISOR_EXPORT),
        files=[
            AdvisorBundleFile(path=str(ADVISOR_EXPORT / filename), role=filename)
            for filename in files
        ],
    )


def test_v1_full_fake_replay_covers_api_namespace_cli_and_demo() -> None:
    for namespace in NAMESPACES:
        module = importlib.import_module(namespace)
        assert module is not None

    for namespace in NAMESPACES[1:]:
        public_api = importlib.import_module(f"{namespace}.public_api")
        assert public_api.COMPATIBILITY_NAMESPACE == "turing_research_plus"

    config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["turingresearch-plus"]["env"]
    benchmark_report = run_benchmark_scenario(load_v1_public_demo_scenario())

    assert env["TURINGRESEARCH_MODE"] == "fake"
    assert env["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert env["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert benchmark_report.status == "pass"
    assert benchmark_report.demo_only is True
    assert benchmark_report.no_real_experiment is True


def test_v1_full_fake_replay_covers_dashboard_export_and_quality_gate(
    tmp_path: Path,
) -> None:
    bundle = _advisor_bundle()
    pdf_plan = build_advisor_pdf_export_plan(bundle, tmp_path / "pdf")
    pptx_plan = build_advisor_pptx_export_plan(bundle, tmp_path / "pptx")
    pdf_result = export_advisor_pdf_optional(bundle, tmp_path / "pdf", force_skip=True)
    pptx_result = export_advisor_pptx_optional(
        bundle,
        tmp_path / "pptx",
        force_skip=True,
    )
    quality = run_export_quality_gate(
        ExportQualityGateRequest(
            advisor_export_dir=ADVISOR_EXPORT,
            dashboard_paths=[
                VGGT / "dashboard_html" / "refined_dashboard.html",
                PUBLIC_DEMO / "dashboard" / "index.html",
            ],
        )
    )

    assert pdf_plan.optional_backend is True
    assert pptx_plan.optional_backend is True
    assert pdf_result.status == "skipped"
    assert pptx_result.status == "skipped"
    assert quality.status == ExportQualityStatus.PASS_WITH_WARNINGS
    assert quality.findings == []


def test_v1_full_fake_replay_covers_privacy_plugin_and_split_readiness() -> None:
    privacy = scan_privacy_paths([PUBLIC_DEMO])
    execute_code = evaluate_sandbox_permission(SandboxPermission.EXECUTE_CODE)
    secrets_access = evaluate_sandbox_permission(SandboxPermission.SECRETS_ACCESS)

    required_split_dirs = [
        SPLIT_READY / "turingresearch-vggt-case",
        SPLIT_READY / "turingresearch-examples",
        SPLIT_READY / "turingresearch-plugins",
    ]

    assert privacy.release_blocker is False
    assert execute_code.status == SandboxDecisionStatus.DENIED
    assert secrets_access.status == SandboxDecisionStatus.DENIED
    for path in required_split_dirs:
        assert path.exists()
        safety_report = (path / "safety_report.md").read_text(encoding="utf-8")
        assert "safe_to_export" in safety_report
        assert "release_blocker" in safety_report
        assert "false" in safety_report.lower()


def test_v1_full_fake_replay_covers_public_launch_rc_docs() -> None:
    required_docs = [
        ROOT / "docs" / "v1.0.0-public-launch-rc-report.md",
        ROOT / "docs" / "v1.0.0-public-launch-go-no-go.md",
        ROOT / "docs" / "v1.0.0-public-launch-blockers.md",
        ROOT / "docs" / "v1.0.0-split-execution-go-no-go.md",
    ]

    for path in required_docs:
        text = path.read_text(encoding="utf-8").lower()
        assert "go" in text or "no-go" in text
        assert "human review" in text or "review" in text
