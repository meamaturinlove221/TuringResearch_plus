"""Convergence decision report builder and renderer."""

from __future__ import annotations

from turing_research_plus.convergence.feasibility import assess_feasibilities
from turing_research_plus.convergence.models import ConvergenceCandidate, DecisionReport
from turing_research_plus.convergence.pairwise import pairwise_rank
from turing_research_plus.convergence.portfolio import steelman_for_rejected
from turing_research_plus.convergence.scoring import score_candidates, scoring_matrix


def build_convergence_decision_report(
    candidates: list[ConvergenceCandidate],
    *,
    report_id: str = "convergence-decision-report",
    include_pairwise: bool = True,
) -> DecisionReport:
    """Build a deterministic decision report for route comparison."""

    if not candidates:
        raise ValueError("at least one convergence candidate is required")

    scores = score_candidates(candidates)
    feasibility_notes = assess_feasibilities(candidates)
    feasible_ids = {
        note.candidate_id for note in feasibility_notes if note.feasible
    }
    ranked = [score for score in scores if score.candidate_id in feasible_ids]
    rejected = [score for score in scores if score.candidate_id not in feasible_ids]
    if not ranked:
        ranked = scores[:1]
        rejected = scores[1:]

    final = ranked[0]
    return DecisionReport(
        report_id=report_id,
        ranked_candidates=ranked,
        scoring_matrix=scoring_matrix(scores),
        pairwise_matrix=pairwise_rank(scores) if include_pairwise else None,
        sensitivity_analysis=_sensitivity_notes(final.candidate_id),
        feasibility_notes=feasibility_notes,
        rejected_candidates=rejected,
        steelman_for_rejected=steelman_for_rejected(rejected),
        final_recommendation=final.candidate_id,
        confidence=_confidence(final.total_score, final.criteria),
        next_actions=[
            f"Review why `{final.candidate_id}` is preferred.",
            "Run stress-test review before implementation.",
            "Record human approval before promoting the route.",
        ],
    )


def render_convergence_decision_report(report: DecisionReport) -> str:
    """Render a convergence decision report as Markdown."""

    ranked_lines = [
        f"| `{score.candidate_id}` | `{score.total_score:.3f}` | "
        f"`{score.criteria['feasibility']:.3f}` | "
        f"`{score.criteria['evidence_strength']:.3f}` |"
        for score in report.ranked_candidates
    ]
    rejected_lines = [
        f"- `{score.candidate_id}`: {report.steelman_for_rejected.get(score.candidate_id, '')}"
        for score in report.rejected_candidates
    ] or ["- none"]
    feasibility_lines = [
        f"- `{note.candidate_id}`: feasible=`{str(note.feasible).lower()}`, "
        f"score=`{note.score:.3f}`, blockers=`{', '.join(note.blockers) or 'none'}`"
        for note in report.feasibility_notes
    ]
    pairwise_lines = []
    for item in report.pairwise_matrix or []:
        loser_id = item.right_id if item.winner_id == item.left_id else item.left_id
        pairwise_lines.append(
            f"- `{item.winner_id}` over `{loser_id}` by `{item.margin:.3f}`"
        )
    if not pairwise_lines:
        pairwise_lines = ["- none"]
    lines = [
        f"# Convergence Decision Report: {report.report_id}",
        "",
        f"- Final recommendation: `{report.final_recommendation}`",
        f"- Confidence: `{report.confidence:.3f}`",
        "- Requires human review: `true`",
        "- Does not execute route: `true`",
        "",
        "## Ranked Candidates",
        "",
        "| Candidate | Total | Feasibility | Evidence |",
        "| --- | --- | --- | --- |",
        *ranked_lines,
        "",
        "## Why This Route",
        "",
        f"- `{report.final_recommendation}` has the highest feasible weighted score.",
        "- Feasibility and evidence strength are explicit scoring criteria.",
        "- Rejected or held routes keep steelman notes for future review.",
        "",
        "## Pairwise Comparison",
        "",
        *pairwise_lines,
        "",
        "## Feasibility Notes",
        "",
        *feasibility_lines,
        "",
        "## Rejected / Held Candidates",
        "",
        *rejected_lines,
        "",
        "## Sensitivity",
        "",
        *[f"- {item}" for item in report.sensitivity_analysis],
        "",
        "## Next Actions",
        "",
        *[f"- {item}" for item in report.next_actions],
    ]
    return "\n".join(lines) + "\n"


def _sensitivity_notes(final_candidate_id: str) -> list[str]:
    return [
        f"`{final_candidate_id}` remains preferred while feasibility and evidence stay high.",
        "A lower feasibility score can move a candidate from preferred to held.",
        "Missing evidence should block promotion even when novelty is high.",
    ]


def _confidence(total_score: float, criteria: dict[str, float]) -> float:
    return round(
        (
            total_score
            + criteria["feasibility"]
            + criteria["evidence_strength"]
        )
        / 3,
        3,
    )
