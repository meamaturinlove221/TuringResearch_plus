"""Problem reformulation for Deep Insight workflows."""

from __future__ import annotations

from tuling_research_plus.insight.models import (
    GapValidationReport,
    ReformulatedProblem,
    ReformulatedProblemSet,
)


def reformulate_problems(
    gap_report: GapValidationReport,
    set_id: str = "problem-set-1",
) -> ReformulatedProblemSet:
    """Create evidence-backed problem reformulations."""

    problems = [
        ReformulatedProblem(
            problem_id=f"problem-{index}",
            original_problem=gap.description,
            reformulated_problem=(
                "What evidence-bounded intervention would reduce uncertainty around "
                f"{gap.description}"
            ),
            changes=[
                "Moves from a broad gap statement to an intervention-oriented question.",
                "Requires explicit uncertainty reduction criteria.",
            ],
            invariants=[
                "Keeps the original evidence base.",
                "Keeps the original research topic.",
            ],
            evidence=gap.evidence,
        )
        for index, gap in enumerate(gap_report.gaps, start=1)
    ]
    return ReformulatedProblemSet(
        set_id=set_id,
        topic=gap_report.topic,
        problems=problems,
    )

