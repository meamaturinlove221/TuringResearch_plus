from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.hypothesis.falsifiability import build_hypothesis, is_falsifiable
from turing_research_plus.hypothesis.models import GapPriority
from turing_research_plus.hypothesis.scoring import score_hypothesis
from turing_research_plus.hypothesis.service import HypothesisFormationService
from turing_research_plus.hypothesis.tools import (
    research_hypothesis_generate,
    research_hypothesis_operationalize,
)
from turing_research_plus.insight.models import GapValidation, GapValidationReport


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def priority() -> GapPriority:
    return GapPriority(
        gap_id="gap-1",
        description="Few studies validate workflow gates.",
        score=0.9,
        rationale="High confidence and enough evidence.",
        evidence=[evidence()],
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
                evidence=[evidence()],
            )
        ],
    )


def test_generated_hypothesis_is_falsifiable() -> None:
    hypothesis = build_hypothesis(priority())

    assert is_falsifiable(hypothesis) is True


def test_score_hypothesis_preserves_bounds() -> None:
    scored = score_hypothesis(build_hypothesis(priority()), priority())

    assert 0 <= scored.score <= 1


def test_hypothesis_generate_and_operationalize_tools() -> None:
    service = HypothesisFormationService()
    priorities = service.gap_prioritize(gap_report())
    generated_payload = research_hypothesis_generate(priorities, service)
    hypothesis = service.hypothesis_generate(priorities).hypotheses[0]
    operationalized = research_hypothesis_operationalize(hypothesis, service)

    assert generated_payload["hypotheses"][0]["falsifiability_criteria"]
    assert operationalized["variables"]["independent"]
    assert operationalized["experiment_readiness"] == "dry_run_ready"

