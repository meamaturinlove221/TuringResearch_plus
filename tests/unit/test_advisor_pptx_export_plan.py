from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)
from turing_research_plus.advisor_export.pptx_exporter import (
    build_advisor_pptx_export_plan,
    export_advisor_pptx_optional,
)
from turing_research_plus.advisor_export.pptx_models import AdvisorPptxExportStatus


def _bundle(tmp_path: Path) -> AdvisorMarkdownBundle:
    files = {
        "advisor_report_source.md": "# Advisor Report\n\n## Current Status\n\nnot-ready review.\n",
        "slides_outline.md": "# Slides Outline\n\n1. North Star\n",
        "figure_list.md": "# Figure List\n\nNo generated figures are included.\n",
        "table_list.md": "# Table List\n\nNo synthetic result table was generated.\n",
        "evidence_refs.md": "# Evidence Refs\n\nEvidence summary remains source-linked.\n",
        "limitations.md": "# Limitations\n\nRequires human review.\n",
        "next_actions.md": "# Next Actions\n\nCollect missing artifacts.\n",
        "manifest.yaml": "requires_human_review: true\n",
    }
    for filename, text in files.items():
        (tmp_path / filename).write_text(text, encoding="utf-8")
    return AdvisorMarkdownBundle(
        bundle_id="bundle-1",
        topic="VGGT Advisor",
        output_dir=str(tmp_path),
        files=[
            AdvisorBundleFile(path=str(tmp_path / filename), role=filename)
            for filename in files
        ],
    )


def test_build_real_pptx_export_plan_is_optional(tmp_path: Path) -> None:
    plan = build_advisor_pptx_export_plan(_bundle(tmp_path), tmp_path / "pptx")

    assert plan.source_bundle_id == "bundle-1"
    assert plan.output_filename == "advisor_deck.pptx"
    assert plan.optional_backend is True
    assert len(plan.slides) == 8
    assert "No fake charts" in " ".join(plan.safety_warnings)


def test_pptx_export_gracefully_skips_when_forced(tmp_path: Path) -> None:
    result = export_advisor_pptx_optional(_bundle(tmp_path), tmp_path / "pptx", force_skip=True)

    assert result.status == AdvisorPptxExportStatus.SKIPPED
    assert result.output_pptx is None
    assert result.skipped_reason == "PPTX backend intentionally skipped"
    assert (tmp_path / "pptx" / "advisor_pptx_review_source.md").exists()
