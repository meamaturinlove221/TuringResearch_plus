from __future__ import annotations

import pytest

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)

REQUIRED_FILES = [
    "advisor_report_source.md",
    "slides_outline.md",
    "figure_list.md",
    "table_list.md",
    "evidence_refs.md",
    "limitations.md",
    "next_actions.md",
    "manifest.yaml",
]


def test_advisor_markdown_bundle_serializes() -> None:
    bundle = AdvisorMarkdownBundle(
        bundle_id="bundle-1",
        topic="VGGT",
        output_dir="out",
        files=[
            AdvisorBundleFile(path=f"out/{filename}", role=filename)
            for filename in REQUIRED_FILES
        ],
    )

    payload = bundle.model_dump(mode="json")

    assert payload["requires_human_review"] is True
    assert payload["generated_pdf"] is False
    assert payload["generated_pptx"] is False


def test_advisor_markdown_bundle_rejects_pdf_claim() -> None:
    with pytest.raises(ValueError, match="must not claim PDF/PPTX generation"):
        AdvisorMarkdownBundle(
            bundle_id="bundle-1",
            topic="VGGT",
            output_dir="out",
            files=[
                AdvisorBundleFile(path=f"out/{filename}", role=filename)
                for filename in REQUIRED_FILES
            ],
            generated_pdf=True,
        )


def test_advisor_markdown_bundle_requires_all_files() -> None:
    with pytest.raises(ValueError, match="missing files"):
        AdvisorMarkdownBundle(
            bundle_id="bundle-1",
            topic="VGGT",
            output_dir="out",
            files=[AdvisorBundleFile(path="out/manifest.yaml", role="manifest")],
        )
