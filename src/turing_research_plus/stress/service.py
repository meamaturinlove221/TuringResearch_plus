"""Stress Test workflow service."""

from __future__ import annotations

from turing_research_plus.artifacts.models import ResearchArtifact
from turing_research_plus.hypothesis.models import Hypothesis
from turing_research_plus.stress.claim_red_team import red_team_claim
from turing_research_plus.stress.counterfactual import counterfactual_probe, failure_mode_analyze
from turing_research_plus.stress.hypothesis_debate import debate_hypothesis
from turing_research_plus.stress.models import (
    Claim,
    ExperimentPlan,
    FailureMode,
    StressTestReport,
)
from turing_research_plus.stress.premortem import experiment_premortem


class StressTestService:
    """Run deterministic stress-test workflows."""

    def artifact_stress_test(self, artifact: ResearchArtifact) -> StressTestReport:
        """Stress-test a ResearchArtifact as a claim."""

        claim = Claim(
            claim_id=artifact.artifact_id,
            statement=artifact.title,
            evidence_refs=artifact.evidence,
        )
        return red_team_claim(claim)

    def claim_red_team(self, claim: Claim) -> StressTestReport:
        """Red-team a claim."""

        return red_team_claim(claim)

    def hypothesis_debate(self, hypothesis: Hypothesis) -> StressTestReport:
        """Debate a hypothesis."""

        return debate_hypothesis(hypothesis)

    def experiment_premortem(self, plan: ExperimentPlan) -> StressTestReport:
        """Run experiment premortem."""

        return experiment_premortem(plan)

    def counterfactual_probe(
        self,
        artifact_id: str,
        claim: str,
        evidence_count: int,
        mitigated: bool = False,
    ) -> StressTestReport:
        """Run a counterfactual probe."""

        return counterfactual_probe(
            artifact_id=artifact_id,
            claim=claim,
            evidence_count=evidence_count,
            mitigated=mitigated,
        )

    def failure_mode_analyze(
        self,
        artifact_id: str,
        failure_modes: list[FailureMode],
        mitigations: list[str] | None = None,
    ) -> StressTestReport:
        """Aggregate failure modes."""

        return failure_mode_analyze(
            artifact_id=artifact_id,
            failure_modes=failure_modes,
            mitigations=mitigations,
        )

