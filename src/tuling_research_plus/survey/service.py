"""Literature survey service with Protocol dependencies."""

from __future__ import annotations

from typing import Protocol

from tuling_research_plus.survey.depth_gate import evaluate_depth_gates
from tuling_research_plus.survey.evidence_matrix import build_evidence_matrix
from tuling_research_plus.survey.gap_extractor import extract_gaps
from tuling_research_plus.survey.models import (
    CitationLineage,
    LiteratureSurveyArtifact,
    PaperRecord,
    PRISMAFlow,
    SurveyInput,
    SurveyPlan,
    SurveyResult,
    SurveyStatus,
    SurveyStrategy,
)
from tuling_research_plus.survey.screening import screen_papers
from tuling_research_plus.survey.strategies import create_survey_plan


class PaperService(Protocol):
    """Protocol for paper search/content services."""

    def search(self, survey_input: SurveyInput, limit: int) -> list[PaperRecord]: ...


class WebService(Protocol):
    """Protocol for web source services."""


class PDFMarkdownService(Protocol):
    """Protocol for PDF Markdown conversion services."""

    def to_markdown(self, paper: PaperRecord) -> PaperRecord: ...


class SemanticGraphService(Protocol):
    """Protocol for citation graph services."""

    def expand_seed_papers(self, seed_papers: list[str], budget: int) -> list[PaperRecord]: ...


class VaultService(Protocol):
    """Protocol for survey artifact persistence."""

    def store(self, artifact: LiteratureSurveyArtifact) -> None: ...


class ContextService(Protocol):
    """Protocol for workflow context checkpoints."""

    def checkpoint(self, label: str, payload: object) -> None: ...


class LiteratureSurveyService:
    """Depth-gated literature survey workflow."""

    def __init__(
        self,
        paper_service: PaperService,
        pdf_service: PDFMarkdownService | None = None,
        graph_service: SemanticGraphService | None = None,
        vault_service: VaultService | None = None,
        context_service: ContextService | None = None,
    ) -> None:
        self.paper_service = paper_service
        self.pdf_service = pdf_service
        self.graph_service = graph_service
        self.vault_service = vault_service
        self.context_service = context_service

    def plan(self, survey_input: SurveyInput, survey_id: str = "survey-1") -> SurveyPlan:
        """Create a strategy-routed survey plan."""

        return create_survey_plan(survey_input, survey_id)

    def run(
        self,
        survey_input: SurveyInput,
        survey_id: str = "survey-1",
        dry_run: bool = True,
    ) -> SurveyResult:
        """Run a fake-service literature survey workflow."""

        plan = self.plan(survey_input, survey_id)
        papers = self.paper_service.search(plan.survey_input, plan.search_budget)
        if plan.survey_input.strategy == SurveyStrategy.SNOWBALL and self.graph_service is not None:
            expanded = self.graph_service.expand_seed_papers(
                plan.survey_input.seed_papers,
                plan.search_budget,
            )
            papers = self._merge_papers([*papers, *expanded])
        if self.pdf_service is not None:
            papers = [self.pdf_service.to_markdown(paper) for paper in papers]

        screening = screen_papers(papers, plan.survey_input)
        blockers = evaluate_depth_gates(plan.survey_input, screening)
        matrix = build_evidence_matrix(papers, screening)
        gap_list = extract_gaps(matrix) if matrix.rows else None
        if gap_list is None or not gap_list.gaps:
            blockers.append("no evidence-backed final gaps")

        artifact = LiteratureSurveyArtifact(
            survey_id=plan.survey_id,
            topic=plan.survey_input.topic,
            strategy=plan.survey_input.strategy,
            status=SurveyStatus.BLOCKED if blockers else SurveyStatus.COMPLETED,
            screening_table=screening,
            method_taxonomy=self._method_taxonomy(papers),
            evidence_matrix=matrix,
            gap_list=gap_list or extract_gaps(matrix),
            prisma_flow=PRISMAFlow(
                identified=len(papers),
                screened=len(screening.rows),
                included=screening.included_count,
            ),
            citation_lineage=self._citation_lineage(plan, papers),
            warnings=blockers,
        )
        if self.vault_service is not None and not blockers:
            self.vault_service.store(artifact)
        if self.context_service is not None:
            self.context_service.checkpoint("survey_run", artifact)
        return SurveyResult(
            status=artifact.status,
            plan=plan,
            artifact=artifact,
            blocked_reason="; ".join(blockers) if blockers else None,
        )

    def export_markdown(self, result: SurveyResult) -> str:
        """Export a survey result as Markdown."""

        return result.to_markdown()

    def _merge_papers(self, papers: list[PaperRecord]) -> list[PaperRecord]:
        merged: dict[str, PaperRecord] = {}
        for paper in papers:
            merged[paper.paper_id] = paper
        return list(merged.values())

    def _method_taxonomy(self, papers: list[PaperRecord]) -> object:
        from tuling_research_plus.survey.models import MethodTaxonomy

        methods: dict[str, list[str]] = {}
        for paper in papers:
            for tag in paper.tags:
                methods.setdefault(tag, []).append(paper.paper_id)
        return MethodTaxonomy(methods=methods)

    def _citation_lineage(
        self,
        plan: SurveyPlan,
        papers: list[PaperRecord],
    ) -> CitationLineage | None:
        if plan.survey_input.strategy != SurveyStrategy.SNOWBALL:
            return None
        paper_ids = [paper.paper_id for paper in papers]
        expanded = [
            paper_id
            for paper_id in paper_ids
            if paper_id not in plan.survey_input.seed_papers
        ]
        return CitationLineage(
            seed_papers=plan.survey_input.seed_papers,
            expanded_papers=expanded,
            saturation_reached=len(expanded) < plan.search_budget,
        )
