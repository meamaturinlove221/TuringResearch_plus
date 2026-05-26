from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard.run_dashboard import build_run_dashboard
from turing_research_plus.run_compare.board_index import board_ref_from_path
from turing_research_plus.run_compare.comparator import compare_runs, input_from_dashboard
from turing_research_plus.run_compare.markdown_export import (
    render_run_comparison_markdown,
)
from turing_research_plus.run_compare.models import (
    RunComparisonInput,
    RunComparisonStatus,
)
from turing_research_plus.run_ingest.modal_ingestor import ingest_modal_run
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType

ROOT = Path(__file__).resolve().parents[2]
MODAL_FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "run_ingest_fixtures"
    / "modal_run_fixture"
)
EXAMPLE_REPORT = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "run_comparison"
    / "vggt_run_comparison.md"
)


def test_vggt_run_comparison_fixture_is_conservative() -> None:
    modal_run = ingest_modal_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=MODAL_FIXTURE)
    )
    modal_dashboard = build_run_dashboard(modal_run)
    runs = [
        RunComparisonInput(
            run_id="V770",
            status=RunComparisonStatus.REQUIRES_HUMAN_REVIEW,
            boards=[board_ref_from_path("V770", "boards/v770_proxy_mask.png")],
            claimed_improvements=["full human completion"],
        ),
        RunComparisonInput(
            run_id="V129",
            status=RunComparisonStatus.LOCAL_OBSERVED,
            boards=[board_ref_from_path("V129", "boards/v129_hairline_delta.png")],
            notes=["local positive; regression warning retained"],
        ),
        RunComparisonInput(
            run_id="V260",
            status=RunComparisonStatus.HARD_BLOCKED,
            artifacts_missing=["adjacent_predictions.npz", "semantic_assets.json"],
        ),
        RunComparisonInput(
            run_id="V999",
            status=RunComparisonStatus.NOT_ENOUGH_EVIDENCE,
            claimed_improvements=["SparseConv3D promotion"],
        ),
        input_from_dashboard(modal_dashboard),
    ]

    report = compare_runs(runs)
    markdown = render_run_comparison_markdown(report)

    assert "V260 is hard-blocked" in markdown
    assert "V999 long-run does not equal promotion" in markdown
    assert "SparseConv3D success requires real backend evidence" in markdown
    assert "Planned routes are not observed results" in markdown
    assert "SparseConv3D success claim" not in markdown


def test_vggt_run_comparison_example_exists_and_keeps_boundary() -> None:
    text = EXAMPLE_REPORT.read_text(encoding="utf-8")

    assert "No Modal or VGGT execution was performed" in text
    assert "SparseConv3D success requires real backend evidence" in text
    assert "V260 is hard-blocked" in text
    assert "full human completion" in text
