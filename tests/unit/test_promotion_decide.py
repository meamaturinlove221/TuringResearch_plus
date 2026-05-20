from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.convergence.models import CandidateScore, PromotionDecision
from tuling_research_plus.convergence.portfolio import decide_promotion
from tuling_research_plus.convergence.service import ConvergenceService
from tuling_research_plus.convergence.tools import research_promotion_decide


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def score(candidate_id: str, total_score: float) -> CandidateScore:
    return CandidateScore(
        candidate_id=candidate_id,
        total_score=total_score,
        criteria={
            "evidence_strength": 0.8,
            "feasibility": 0.8,
            "novelty": 0.8,
            "expected_gain": 0.8,
            "risk_adjustment": 0.7,
        },
        rationale="Weighted deterministic convergence score.",
        evidence_refs=[evidence()],
    )


def test_promotion_decide_promotes_high_score() -> None:
    decision = decide_promotion(score("candidate-1", 0.8), feasible=True)

    assert decision.decision == PromotionDecision.PROMOTE


def test_promotion_decide_rejects_infeasible_candidate() -> None:
    decision = decide_promotion(score("candidate-1", 0.9), feasible=False)

    assert decision.decision == PromotionDecision.REJECT


def test_promotion_decide_holds_mid_score() -> None:
    decision = decide_promotion(score("candidate-1", 0.7), feasible=True)

    assert decision.decision == PromotionDecision.HOLD


def test_promotion_decide_tool_returns_json_payload() -> None:
    payload = research_promotion_decide(
        score("candidate-1", 0.8),
        ConvergenceService(),
        feasible=True,
    )

    assert payload["decision"] == "promote"
    assert payload["confidence"] == 0.8

