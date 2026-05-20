import pytest
from pydantic import ValidationError

from tuling_research_plus.paper.figure_registry import (
    FigureAsset,
    FigureAssetKind,
    FigureAssetRegistry,
    FigureAssetStatus,
    FigureRegisterInput,
    lint_figure_registry,
    register_figure,
)


def test_registry_validates() -> None:
    asset = FigureAsset(
        figure_id="fig-1",
        title="Architecture Diagram",
        source_file="docs/architecture_16box.mmd",
        caption="TulingResearch Plus 16-box architecture.",
        used_in_blocks=["method_design"],
        asset_kind=FigureAssetKind.MERMAID,
    )
    registry = FigureAssetRegistry(assets=[asset])

    assert registry.assets[0].status == FigureAssetStatus.READY
    assert lint_figure_registry(registry) == []


def test_orphan_figure_detected() -> None:
    asset = FigureAsset(
        figure_id="fig-orphan",
        title="Orphan Figure",
        source_file="paper/figures/orphan.png",
        caption="Unused figure.",
        used_in_blocks=[],
    )

    issues = lint_figure_registry(FigureAssetRegistry(assets=[asset]))

    assert asset.status == FigureAssetStatus.BLOCKED
    assert issues[0].issue_type == "orphan_figure"


def test_caption_missing_detected() -> None:
    asset = FigureAsset(
        figure_id="fig-caption",
        title="Missing Caption",
        source_file="paper/figures/missing_caption.png",
        used_in_blocks=["experiments"],
    )

    issues = lint_figure_registry(FigureAssetRegistry(assets=[asset]))

    assert asset.status == FigureAssetStatus.BLOCKED
    assert any(issue.issue_type == "caption_missing" for issue in issues)


def test_figure_linked_to_article_block() -> None:
    result = register_figure(
        FigureRegisterInput(
            figure_id="fig-linked",
            title="Linked Figure",
            source_file="sop_graphs/paper_graphs/paper_default.mmd",
            caption="Paper DocFlow SOP graph.",
            used_in_blocks=["paper_draft"],
            asset_kind=FigureAssetKind.SOP_GRAPH,
        )
    )

    assert result.asset.used_in_blocks == ["paper_draft"]
    assert result.asset.status == FigureAssetStatus.READY
    assert result.asset.output_png.as_posix() == "paper/figures/fig-linked.png"


def test_pdf_extracted_figure_can_be_registered() -> None:
    result = register_figure(
        FigureRegisterInput(
            figure_id="fig-pdf-1",
            title="Extracted PDF Figure",
            source_file="paper/figures/pdf_fig_1.png",
            caption="Extracted figure from local PDF.",
            used_in_blocks=["related_work"],
            asset_kind=FigureAssetKind.PDF_EXTRACTED_FIGURE,
            original_pdf_source="fixtures/sample.pdf",
        )
    )

    assert result.asset.original_pdf_source is not None
    assert result.asset.status == FigureAssetStatus.READY


def test_pdf_extracted_figure_requires_original_pdf_source() -> None:
    with pytest.raises(ValidationError):
        FigureAsset(
            figure_id="fig-pdf-2",
            title="Extracted PDF Figure",
            source_file="paper/figures/pdf_fig_2.png",
            caption="Extracted figure from local PDF.",
            used_in_blocks=["related_work"],
            asset_kind=FigureAssetKind.PDF_EXTRACTED_FIGURE,
        )
