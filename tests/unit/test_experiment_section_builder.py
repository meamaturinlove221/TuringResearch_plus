from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.paper_write.experiment_builder import (
    ExperimentSectionSkeleton,
    build_vggt_experiment_section_skeleton,
    render_experiment_result_table_missing_items,
    render_experiment_section_skeleton,
)

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"


def _skeleton() -> ExperimentSectionSkeleton:
    return build_vggt_experiment_section_skeleton(
        VGGT / "run_ingest_report.md",
        VGGT / "dashboard",
        VGGT / "route_specs" / "modal_sparseconv_v0.yaml",
    )


def test_experiment_section_skeleton_contains_required_sections() -> None:
    skeleton = _skeleton()

    assert skeleton.dataset_setup_placeholder
    assert skeleton.baselines
    assert skeleton.ablations
    assert skeleton.metrics
    assert skeleton.route_status == "requires-real-experiment"
    assert skeleton.run_status == "ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS"
    assert skeleton.backend_status == "real_backend_missing"
    assert skeleton.missing_result_tables
    assert skeleton.failure_cases
    assert skeleton.planned_experiments
    assert skeleton.not_ready_claims
    assert skeleton.requires_human_review is True


def test_experiment_section_skeleton_blocks_dashboard_as_result() -> None:
    skeleton = _skeleton()
    not_ready = "\n".join(skeleton.not_ready_claims)

    assert "Dashboard is not a paper result." in not_ready
    assert "SparseConv3D success is not established." in not_ready
    assert skeleton.generated_result_values is False
    assert skeleton.fabricated_tables is False
    assert skeleton.dashboard_treated_as_result is False


def test_experiment_section_skeleton_rejects_generated_values() -> None:
    payload = _skeleton().model_dump(mode="python")
    payload["generated_result_values"] = True

    with pytest.raises(ValueError, match="must not generate result values"):
        ExperimentSectionSkeleton(**payload)


def test_experiment_section_markdown_exports_boundaries() -> None:
    skeleton = _skeleton()

    section = render_experiment_section_skeleton(skeleton)
    missing = render_experiment_result_table_missing_items(skeleton)

    assert "## Dataset / Setup Placeholder" in section
    assert "## Missing Result Tables" in section
    assert "Planned is not executed." in section
    assert "Dashboard is not a paper result." in section
    assert "Result tables allowed: `false`" in missing
    assert "No result value is generated." in missing
