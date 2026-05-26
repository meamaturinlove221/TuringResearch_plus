"""Thin research.stress_* tool wrappers."""

from __future__ import annotations

from typing import Any

from tuling_research_plus.artifacts.models import ResearchArtifact
from tuling_research_plus.hypothesis.models import Hypothesis
from tuling_research_plus.stress.models import Claim, ExperimentPlan, FailureMode
from tuling_research_plus.stress.service import StressTestService


def research_artifact_stress_test(
    artifact: ResearchArtifact,
    service: StressTestService,
) -> dict[str, Any]:
    return service.artifact_stress_test(artifact).model_dump(mode="json")


def research_claim_red_team(
    claim: Claim,
    service: StressTestService,
) -> dict[str, Any]:
    return service.claim_red_team(claim).model_dump(mode="json")


def research_hypothesis_debate(
    hypothesis: Hypothesis,
    service: StressTestService,
) -> dict[str, Any]:
    return service.hypothesis_debate(hypothesis).model_dump(mode="json")


def research_experiment_premortem(
    plan: ExperimentPlan,
    service: StressTestService,
) -> dict[str, Any]:
    return service.experiment_premortem(plan).model_dump(mode="json")


def research_counterfactual_probe(
    artifact_id: str,
    claim: str,
    evidence_count: int,
    service: StressTestService,
    mitigated: bool = False,
) -> dict[str, Any]:
    return service.counterfactual_probe(
        artifact_id=artifact_id,
        claim=claim,
        evidence_count=evidence_count,
        mitigated=mitigated,
    ).model_dump(mode="json")


def research_failure_mode_analyze(
    artifact_id: str,
    failure_modes: list[FailureMode],
    service: StressTestService,
    mitigations: list[str] | None = None,
) -> dict[str, Any]:
    return service.failure_mode_analyze(
        artifact_id=artifact_id,
        failure_modes=failure_modes,
        mitigations=mitigations,
    ).model_dump(mode="json")

