"""DocFlow Article Blocks for TuringResearch Plus."""

from __future__ import annotations

from dataclasses import dataclass

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.paper.models import (
    ArticleBlockKind,
    ArticleBlockRegistry,
    ArticleBlockState,
    ArticleBlockStatus,
    ArticleBlockUpdateInput,
    ArticleBlockUpdateOutput,
    DocflowStatusInput,
    DocflowStatusOutput,
    MissingEvidenceItem,
    MissingItemReport,
    PaperReadinessReport,
)


@dataclass(frozen=True)
class ArticleBlockSpec:
    """Static DocFlow block specification."""

    block_kind: ArticleBlockKind
    title: str
    path: str
    required_artifacts: tuple[str, ...]


ARTICLE_BLOCK_SPECS: tuple[ArticleBlockSpec, ...] = (
    ArticleBlockSpec(
        block_kind=ArticleBlockKind.RESEARCH_BRIEF,
        title="Research Brief",
        path="paper/blocks/01_research_brief.md",
        required_artifacts=("ResearchBrief",),
    ),
    ArticleBlockSpec(
        block_kind=ArticleBlockKind.RELATED_WORK,
        title="Related Work",
        path="paper/blocks/02_related_work.md",
        required_artifacts=("LiteratureSurveyArtifact", "PDFMarkdownOutput"),
    ),
    ArticleBlockSpec(
        block_kind=ArticleBlockKind.METHOD_DESIGN,
        title="Method Design",
        path="paper/blocks/03_method_design.md",
        required_artifacts=(
            "ResearchBrief",
            "GapReport",
            "HypothesisPortfolio",
            "IdeaPortfolio",
            "DecisionReport",
        ),
    ),
    ArticleBlockSpec(
        block_kind=ArticleBlockKind.EXPERIMENTS,
        title="Experiments",
        path="paper/blocks/04_experiments.md",
        required_artifacts=("ExperimentPlan", "StressTestReport"),
    ),
    ArticleBlockSpec(
        block_kind=ArticleBlockKind.PAPER_DRAFT,
        title="Paper Draft",
        path="paper/blocks/05_paper_draft.md",
        required_artifacts=("ExperimentReport",),
    ),
)


def docflow_status(input_data: DocflowStatusInput) -> DocflowStatusOutput:
    """Compute article-block readiness from local artifacts."""

    graph = build_docflow_graph()
    blocks = [_build_block_state(spec, input_data) for spec in ARTICLE_BLOCK_SPECS]
    registry = ArticleBlockRegistry(blocks=blocks, continuity_graph=graph)
    missing_report = build_missing_item_report(blocks)
    readiness = PaperReadinessReport(
        ready=all(block.ready for block in blocks),
        draft_blocked=not registry.get_block(ArticleBlockKind.PAPER_DRAFT).ready,
        ready_blocks=[block.block_kind.value for block in blocks if block.ready],
        blocked_blocks=[block.block_kind.value for block in blocks if not block.ready],
        missing_item_report=missing_report,
    )
    return DocflowStatusOutput(
        registry=registry,
        continuity_graph=graph,
        missing_item_report=missing_report,
        readiness_report=readiness,
    )


def article_block_update(input_data: ArticleBlockUpdateInput) -> ArticleBlockUpdateOutput:
    """Compute readiness for one updated article block."""

    evidence_by_block = {input_data.block_kind.value: input_data.evidence_refs}
    if input_data.block_kind == ArticleBlockKind.PAPER_DRAFT and not input_data.evidence_refs:
        evidence_by_block[input_data.block_kind.value] = (
            input_data.experiment_report.evidence if input_data.experiment_report else []
        )
    status_input = DocflowStatusInput(
        available_artifacts=input_data.available_artifacts,
        evidence_by_block=evidence_by_block,
        required_figures={input_data.block_kind.value: input_data.required_figures},
        available_figures=input_data.available_figures,
        block_text={input_data.block_kind.value: input_data.text},
        experiment_report=input_data.experiment_report,
    )
    status = docflow_status(status_input)
    block = status.registry.get_block(input_data.block_kind)
    missing_evidence = [
        item
        for item in status.missing_item_report.missing_evidence
        if item.block_kind == input_data.block_kind
    ]
    return ArticleBlockUpdateOutput(
        block=block,
        accepted=block.ready,
        missing_evidence=missing_evidence,
    )


def missing_evidence(input_data: DocflowStatusInput) -> MissingItemReport:
    """Return the missing evidence and blocker report for the current DocFlow state."""

    return docflow_status(input_data).missing_item_report


def paper_docflow_status(input_data: DocflowStatusInput) -> dict[str, object]:
    """Thin paper.docflow_status wrapper."""

    return docflow_status(input_data).model_dump(mode="json")


def paper_article_block_update(input_data: ArticleBlockUpdateInput) -> dict[str, object]:
    """Thin paper.article_block_update wrapper."""

    return article_block_update(input_data).model_dump(mode="json")


def paper_missing_evidence(input_data: DocflowStatusInput) -> dict[str, object]:
    """Thin paper.missing_evidence wrapper."""

    return missing_evidence(input_data).model_dump(mode="json")


def build_docflow_graph() -> str:
    """Generate the document continuity Mermaid graph."""

    return (
        "flowchart TD\n"
        "    research_brief[Research Brief]\n"
        "    related_work[Related Work]\n"
        "    method_design[Method Design]\n"
        "    experiments[Experiments]\n"
        "    paper_draft[Paper Draft]\n"
        "    research_brief --> related_work\n"
        "    research_brief --> method_design\n"
        "    related_work --> method_design\n"
        "    method_design --> experiments\n"
        "    experiments --> paper_draft\n"
        "    ExperimentReport{{ExperimentReport Gate}} --> paper_draft\n"
    )


def build_missing_item_report(blocks: list[ArticleBlockState]) -> MissingItemReport:
    """Build a missing item report from block states."""

    missing_artifacts = {
        block.block_kind.value: block.missing_artifacts
        for block in blocks
        if block.missing_artifacts
    }
    missing_figures = {
        block.block_kind.value: block.missing_figures
        for block in blocks
        if block.missing_figures
    }
    missing_evidence = [
        MissingEvidenceItem(
            block_kind=block.block_kind,
            requirement="EvidenceRef",
            reason=f"{block.title} requires evidence refs.",
        )
        for block in blocks
        if not block.evidence_refs
    ]
    blockers = {
        block.block_kind.value: block.blocked_reason
        for block in blocks
        if block.blocked_reason is not None
    }
    return MissingItemReport(
        missing_artifacts=missing_artifacts,
        missing_figures=missing_figures,
        missing_evidence=missing_evidence,
        blockers=blockers,
    )


def _build_block_state(
    spec: ArticleBlockSpec,
    input_data: DocflowStatusInput,
) -> ArticleBlockState:
    present_artifacts = _present_artifacts(input_data)
    required_artifacts = list(spec.required_artifacts)
    missing_artifacts = [
        artifact for artifact in required_artifacts if artifact not in present_artifacts
    ]
    required_figures = _string_list_for_block(input_data.required_figures, spec.block_kind)
    missing_figures = [
        figure for figure in required_figures if figure not in input_data.available_figures
    ]
    evidence_refs = _evidence_for_block(input_data, spec.block_kind)
    blocked_reasons = []
    if missing_artifacts:
        blocked_reasons.append(f"missing artifacts: {', '.join(missing_artifacts)}")
    if missing_figures:
        blocked_reasons.append(f"missing figures: {', '.join(missing_figures)}")
    if not evidence_refs:
        blocked_reasons.append("missing evidence refs")
    if spec.block_kind == ArticleBlockKind.PAPER_DRAFT and input_data.experiment_report is None:
        blocked_reasons.append("ExperimentReport is required before Paper Draft")
    return ArticleBlockState(
        block_kind=spec.block_kind,
        title=spec.title,
        path=spec.path,
        required_artifacts=required_artifacts,
        present_artifacts=[
            artifact for artifact in required_artifacts if artifact in present_artifacts
        ],
        missing_artifacts=missing_artifacts,
        required_figures=required_figures,
        available_figures=[
            figure for figure in required_figures if figure in input_data.available_figures
        ],
        missing_figures=missing_figures,
        evidence_refs=evidence_refs,
        text=input_data.block_text.get(spec.block_kind.value, ""),
        status=ArticleBlockStatus.BLOCKED if blocked_reasons else ArticleBlockStatus.READY,
        blocked_reason="; ".join(blocked_reasons) if blocked_reasons else None,
    )


def _present_artifacts(input_data: DocflowStatusInput) -> set[str]:
    artifacts = set(input_data.available_artifacts)
    if input_data.experiment_report is not None:
        artifacts.add("ExperimentReport")
    return artifacts


def _evidence_for_block(
    input_data: DocflowStatusInput,
    block_kind: ArticleBlockKind,
) -> list[EvidenceRef]:
    evidence = _evidence_list_for_block(input_data.evidence_by_block, block_kind)
    if block_kind == ArticleBlockKind.PAPER_DRAFT and not evidence:
        return input_data.experiment_report.evidence if input_data.experiment_report else []
    return evidence


def _evidence_list_for_block(
    mapping: dict[str, list[EvidenceRef]],
    block_kind: ArticleBlockKind,
) -> list[EvidenceRef]:
    return mapping.get(block_kind.value, mapping.get(block_kind.name, []))


def _string_list_for_block(
    mapping: dict[str, list[str]],
    block_kind: ArticleBlockKind,
) -> list[str]:
    return mapping.get(block_kind.value, mapping.get(block_kind.name, []))
