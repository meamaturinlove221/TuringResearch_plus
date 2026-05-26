from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.hypothesis.scoring import prioritize_gaps
from turing_research_plus.hypothesis.service import HypothesisFormationService
from turing_research_plus.hypothesis.tools import research_gap_prioritize
from turing_research_plus.insight.models import GapValidation, GapValidationReport


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
                gap_id="gap-low",
                description="Low confidence gap.",
                confidence=0.55,
                evidence=[evidence("paper-low")],
            ),
            GapValidation(
                gap_id="gap-high",
                description="High confidence gap.",
                confidence=0.85,
                evidence=[evidence("paper-high"), evidence("paper-high-2")],
            ),
        ],
    )


def test_gap_prioritization_sorts_by_score() -> None:
    priorities = prioritize_gaps(gap_report())

    assert priorities.priorities[0].gap_id == "gap-high"
    assert priorities.priorities[0].score > priorities.priorities[1].score


def test_gap_prioritize_tool_returns_json_payload() -> None:
    payload = research_gap_prioritize(gap_report(), HypothesisFormationService())

    assert payload["priorities"][0]["gap_id"] == "gap-high"
    assert payload["priorities"][0]["evidence"]
