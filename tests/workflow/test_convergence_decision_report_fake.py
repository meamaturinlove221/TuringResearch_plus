from __future__ import annotations

from pathlib import Path

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.convergence import (
    CandidateKind,
    ConvergenceCandidate,
    build_convergence_decision_report,
    render_convergence_decision_report,
)

ROOT = Path(__file__).resolve().parents[2]


def evidence(source_id: str) -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-1",
        quote="Fake evidence for convergence demo.",
    )


def candidate(candidate_id: str, feasibility: float, novelty: float) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.IMPLEMENTATION_VARIANT,
        title=f"Route {candidate_id}",
        mechanism="local route comparison",
        expected_gain="Improve release implementation quality.",
        feasibility=feasibility,
        novelty=novelty,
        risk="medium",
        required_resources=["review table"],
        evidence_refs=[evidence(candidate_id)],
    )


def test_convergence_decision_report_fake_workflow() -> None:
    report = build_convergence_decision_report(
        [
            candidate("route-session-first", 0.9, 0.75),
            candidate("route-dashboard-first", 0.7, 0.8),
        ],
        report_id="convergence-demo",
    )
    rendered = render_convergence_decision_report(report)

    assert report.final_recommendation == "route-session-first"
    assert "Why This Route" in rendered
    assert "Does not execute route: `true`" in rendered
    assert report.to_research_artifact().artifact_id == "decision-convergence-demo"


def test_convergence_decision_report_docs_and_demo_are_public_safe() -> None:
    paths = [
        ROOT / "docs" / "convergence-decision-report.md",
        ROOT / "examples" / "convergence_demo" / "README.md",
        ROOT / "examples" / "convergence_demo" / "decision_report.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "route comparison" in combined
    assert "why this route" in combined.lower()
    assert "does not execute routes" in combined
    assert "human review required" in combined

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_", "sk-"]
    for marker in forbidden:
        assert marker not in combined
