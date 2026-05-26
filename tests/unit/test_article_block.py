from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.paper.models import (
    ArticleBlock,
    ArticleBlockKind,
    ArticleBlockState,
    ArticleBlockStatus,
    ArticleSection,
    DraftStatus,
    ExperimentReport,
    PaperDraftRequest,
)


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="experiment-1", locator="table-1", quote="Metric improved.")


def test_article_block_requires_evidence() -> None:
    block = ArticleBlock(
        block_id="block-1",
        section=ArticleSection.RESULTS,
        text="The treatment improved the measured outcome.",
        evidence=[evidence()],
    )

    assert block.section == ArticleSection.RESULTS
    assert block.evidence[0].locator == "table-1"


def test_paper_draft_request_blocks_without_experiment_report() -> None:
    request = PaperDraftRequest(draft_id="draft-1", experiment_report=None)

    assert request.status == DraftStatus.BLOCKED
    assert request.blocked_reason == "ExperimentReport is required before Paper Draft"


def test_paper_draft_request_accepts_experiment_report() -> None:
    report = ExperimentReport(
        report_id="report-1",
        title="Experiment Report",
        evidence=[evidence()],
    )
    request = PaperDraftRequest(draft_id="draft-1", experiment_report=report)

    assert request.status == DraftStatus.PLANNED
    assert request.blocked_reason is None


def test_article_block_state_readiness_property() -> None:
    state = ArticleBlockState(
        block_kind=ArticleBlockKind.RESEARCH_BRIEF,
        title="Research Brief",
        path="paper/blocks/01_research_brief.md",
        required_artifacts=["ResearchBrief"],
        present_artifacts=["ResearchBrief"],
        evidence_refs=[evidence()],
        status=ArticleBlockStatus.READY,
    )

    assert state.ready is True
