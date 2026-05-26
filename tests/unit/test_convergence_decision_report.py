from __future__ import annotations

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.convergence.decision_report import (
    build_convergence_decision_report,
    render_convergence_decision_report,
)
from turing_research_plus.convergence.models import CandidateKind, ConvergenceCandidate


def evidence(source_id: str) -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-1",
        quote="Fake evidence for convergence decision report.",
    )


def candidate(
    candidate_id: str,
    feasibility: float,
    novelty: float,
    resources: list[str] | None = None,
) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.RELEASE_FEATURE,
        title=f"Route {candidate_id}",
        mechanism="review route",
        expected_gain="Improve release implementation quality.",
        feasibility=feasibility,
        novelty=novelty,
        risk="medium",
        required_resources=resources or ["review table"],
        evidence_refs=[evidence(candidate_id)],
    )


def test_build_convergence_decision_report_selects_feasible_best_route() -> None:
    report = build_convergence_decision_report(
        [
            candidate("route-a", 0.9, 0.85),
            candidate("route-b", 0.45, 0.95, resources=["a", "b", "c", "d", "e"]),
        ],
        report_id="demo-report",
    )

    assert report.report_id == "demo-report"
    assert report.final_recommendation == "route-a"
    assert report.ranked_candidates[0].candidate_id == "route-a"
    assert report.rejected_candidates[0].candidate_id == "route-b"
    assert report.steelman_for_rejected["route-b"]
    assert report.pairwise_matrix
    assert report.confidence > 0
    assert "Run stress-test review before implementation." in report.next_actions


def test_render_convergence_decision_report_explains_selection() -> None:
    report = build_convergence_decision_report(
        [candidate("route-a", 0.9, 0.85), candidate("route-b", 0.7, 0.7)]
    )
    rendered = render_convergence_decision_report(report)

    assert "# Convergence Decision Report" in rendered
    assert "Final recommendation: `route-a`" in rendered
    assert "Why This Route" in rendered
    assert "Does not execute route: `true`" in rendered
    assert "Run stress-test review before implementation." in rendered
