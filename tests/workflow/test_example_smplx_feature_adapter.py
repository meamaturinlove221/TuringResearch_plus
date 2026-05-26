from __future__ import annotations

from tests.workflow.example_helpers import (
    assert_example_contract,
    example_evidence,
    read_json,
    to_pretty_json,
)

from turing_research_plus.convergence.models import CandidateKind, ConvergenceCandidate
from turing_research_plus.convergence.service import ConvergenceService
from turing_research_plus.hypothesis.models import GapPriorityReport
from turing_research_plus.hypothesis.service import HypothesisFormationService
from turing_research_plus.ideation.service import CreativeIdeationService
from turing_research_plus.stress.models import (
    FailureMode,
    PassFail,
    Severity,
    StressTestReport,
    StressWeakness,
)


def test_smplx_feature_adapter_example_dry_run_outputs_required_artifacts() -> None:
    required = {"HypothesisPortfolio", "IdeaPortfolio", "DecisionReport", "StressTestReport"}
    assert_example_contract("smplx-feature-adapter-hypothesis", required)
    request = read_json("smplx-feature-adapter-hypothesis/input/request.json")
    evidence = example_evidence("smplx-public-note")

    hypothesis_service = HypothesisFormationService()
    priorities = GapPriorityReport(
        report_id="smplx-priority",
        topic=request["topic"],
        priorities=[
            {
                "gap_id": "gap-smplx-adapter",
                "description": request["hypothesis_prompt"],
                "score": 0.87,
                "rationale": "Public or user-owned notes support clean-room exploration.",
                "evidence": [evidence.model_dump(mode="json")],
            }
        ],
    )
    hypotheses = hypothesis_service.hypothesis_generate(priorities)
    hypothesis_portfolio = hypothesis_service.hypothesis_portfolio_build(hypotheses, max_items=1)
    idea_portfolio = CreativeIdeationService().build_portfolio(hypotheses)
    candidates = [
        ConvergenceCandidate(
            candidate_id=idea.idea_id,
            kind=CandidateKind.IDEA,
            title=idea.title,
            mechanism=idea.mechanism,
            expected_gain=idea.expected_gain,
            feasibility=idea.feasibility,
            novelty=idea.novelty,
            risk=idea.risk,
            required_resources=idea.required_resources,
            evidence_refs=idea.evidence_refs,
        )
        for idea in idea_portfolio.ideas
    ]
    decision_report = ConvergenceService().portfolio_optimize(candidates)
    stress_report = StressTestReport(
        artifact_id=decision_report.report_id,
        weaknesses=[
            StressWeakness(
                weakness_id="weakness-source-boundary",
                description="Must preserve source hygiene and clean-room boundary.",
                severity=Severity.MEDIUM,
                evidence_refs=[evidence],
            )
        ],
        severity=Severity.MEDIUM,
        attack_paths=["Inject private implementation detail."],
        counterarguments=["The fixture uses only public or user-owned notes."],
        failure_modes=[
            FailureMode(
                mode_id="failure-source",
                description="Feature work blocked if source hygiene fails.",
                severity=Severity.MEDIUM,
                mitigation="Keep implementation concept-level and clean-room.",
            )
        ],
        mitigations=["Run Source Hygiene Gate before implementation."],
        residual_risk=Severity.LOW,
        pass_fail=PassFail.PASS,
        rerun_recommendations=["Rerun after source list changes."],
    )

    outputs = {
        "HypothesisPortfolio": hypothesis_portfolio.model_dump(mode="json"),
        "IdeaPortfolio": idea_portfolio.model_dump(mode="json"),
        "DecisionReport": decision_report.model_dump(mode="json"),
        "StressTestReport": stress_report.model_dump(mode="json"),
    }
    markdown = "\n".join(
        [
            "# SMPL-X Feature Adapter Hypothesis Dry Run",
            f"- DecisionReport: `{decision_report.report_id}`",
            f"- StressTestReport: `{stress_report.artifact_id}`",
        ]
    )

    assert set(outputs) == required
    assert decision_report.ranked_candidates
    assert stress_report.pass_fail == PassFail.PASS
    assert "DecisionReport" in markdown
    assert "StressTestReport" in to_pretty_json(outputs)
