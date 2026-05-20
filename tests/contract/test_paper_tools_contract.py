from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.paper.caption_generator import (
    CaptionGenerateInput,
    paper_caption_generate,
)
from tuling_research_plus.paper.docflow import paper_docflow_status
from tuling_research_plus.paper.figure_registry import (
    FigureAsset,
    FigureAssetKind,
    FigureRegisterInput,
    paper_figure_register,
)
from tuling_research_plus.paper.latex_export import LatexExportInput, paper_latex_export
from tuling_research_plus.paper.models import DocflowStatusInput, ExperimentReport
from tuling_research_plus.paper.paper_writer import PaperDraftInput, paper_draft_generate
from tuling_research_plus.sop.models import SOPGenerationRequest, SOPGraphType
from tuling_research_plus.sop.sop_graph import paper_sop_graph_generate


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="experiment-report-1", locator="table-1", quote="Metric.")


def test_paper_public_tools_contract_payloads() -> None:
    report = ExperimentReport(
        report_id="experiment-report-1",
        title="Experiment Report",
        metrics={"accuracy": 0.8},
        evidence=[evidence()],
    )
    docflow = paper_docflow_status(
        DocflowStatusInput(
            available_artifacts=["ResearchBrief"],
            evidence_by_block={"research_brief": [evidence()]},
            experiment_report=report,
        )
    )
    sop = paper_sop_graph_generate(
        SOPGenerationRequest(graph_type=SOPGraphType.PAPER, title="Paper SOP")
    )
    figure = paper_figure_register(
        FigureRegisterInput(
            figure_id="fig-1",
            title="Architecture Figure",
            source_file="docs/architecture_16box.mmd",
            caption="Architecture.",
            used_in_blocks=["method_design"],
            asset_kind=FigureAssetKind.MERMAID,
        )
    )
    caption = paper_caption_generate(
        CaptionGenerateInput(
            asset=FigureAsset(**figure["asset"]),
            evidence_refs=[evidence()],
        )
    )
    draft = paper_draft_generate(PaperDraftInput(experiment_report=None))
    latex = paper_latex_export(
        LatexExportInput(draft_markdown="# Draft\n\n## Abstract\nEvidence-backed.")
    )

    assert "registry" in docflow
    assert sop["mermaid_text"].startswith("flowchart TD")
    assert figure["asset"]["status"] == "ready"
    assert caption["caption"] == "Architecture."
    assert draft["blocked"] is True
    assert latex["latex_text"].startswith("\\documentclass{article}")
