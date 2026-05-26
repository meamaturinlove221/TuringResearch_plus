"""Thin tool wrappers for collision risk detection."""

from __future__ import annotations

from turing_research_plus.collision.models import CollisionRiskReport, PaperComparisonInput
from turing_research_plus.collision.overlap import build_overlap_matrix
from turing_research_plus.collision.positioning import build_positioning_notes
from turing_research_plus.collision.risk_scoring import score_collision_risk
from turing_research_plus.collision.safe_claims import build_safe_claims, build_unsafe_claims


def collision_risk_detect(request: PaperComparisonInput) -> CollisionRiskReport:
    """Build a conservative collision risk report."""

    matrix = build_overlap_matrix(request.compared_papers)
    risk_scores = score_collision_risk(request.compared_papers, matrix)
    missing_evidence = _missing_evidence(request.compared_papers)
    return CollisionRiskReport(
        target_project=request.target_project,
        compared_papers=request.compared_papers,
        overlap_matrix=matrix,
        risk_scores=risk_scores,
        safe_claims=build_safe_claims(risk_scores),
        unsafe_claims=build_unsafe_claims(risk_scores),
        positioning_notes=build_positioning_notes(risk_scores),
        missing_evidence=missing_evidence,
        requires_human_review=True,
    )


def _missing_evidence(compared_papers: list[dict[str, object]]) -> list[str]:
    missing: list[str] = []
    for paper in compared_papers:
        title = str(paper.get("title") or paper.get("paper_id") or "unknown paper")
        text = " ".join(str(value) for value in paper.values()).lower()
        if "requires-real-paper-review" in text or not paper.get("evidence_refs"):
            missing.append(f"{title}: requires real paper review and citation-grade EvidenceRef.")
    if not compared_papers:
        missing.append("No compared papers were provided.")
    return list(dict.fromkeys(missing))
