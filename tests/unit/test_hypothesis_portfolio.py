from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.hypothesis.portfolio import build_portfolio
from tuling_research_plus.hypothesis.service import HypothesisFormationService
from tuling_research_plus.hypothesis.tools import research_hypothesis_portfolio_build
from tuling_research_plus.insight.models import (
    GapValidation,
    GapValidationReport,
    InsightItem,
    InsightReport,
)


def evidence(source_id: str = "paper-1") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def gap_report() -> GapValidationReport:
    return GapValidationReport(
        report_id="gap-report-1",
        topic="research workflow quality gates",
        gaps=[
            GapValidation(
                gap_id="gap-1",
                description="Few studies validate workflow gates.",
                confidence=0.85,
                evidence=[evidence("paper-1")],
            ),
            GapValidation(
                gap_id="gap-2",
                description="Few studies compare evidence gate thresholds.",
                confidence=0.8,
                evidence=[evidence("paper-2")],
            ),
        ],
    )


def insight_report() -> InsightReport:
    return InsightReport(
        report_id="insight-report-1",
        topic="research workflow quality gates",
        insights=[
            InsightItem(
                insight_id="insight-1",
                statement="Boundary checks should happen before implementation planning.",
                supporting_evidence=[evidence("paper-1")],
                contradicting_evidence=[evidence("paper-2")],
                implication="Prefer falsifiable boundary tests.",
            )
        ],
    )


def test_hypothesis_portfolio_selects_ranked_items_and_questions() -> None:
    service = HypothesisFormationService()
    priorities = service.gap_prioritize(gap_report())
    hypotheses = service.hypothesis_generate(priorities, insight_report())
    portfolio = build_portfolio(hypotheses, max_items=1)

    assert len(portfolio.selected) == 1
    assert portfolio.research_questions[0].hypothesis_id == portfolio.selected[0].hypothesis_id
    assert portfolio.to_research_artifact().evidence


def test_hypothesis_portfolio_tool_returns_json_payload() -> None:
    service = HypothesisFormationService()
    priorities = service.gap_prioritize(gap_report())
    hypotheses = service.hypothesis_generate(priorities)
    payload = research_hypothesis_portfolio_build(hypotheses, service, max_items=2)

    assert len(payload["selected"]) == 2
    assert payload["research_questions"]
    assert payload["rationale"]

