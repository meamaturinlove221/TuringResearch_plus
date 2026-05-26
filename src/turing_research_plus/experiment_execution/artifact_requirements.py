"""Artifact requirement helpers for safe experiment execution planning."""

from __future__ import annotations

from turing_research_plus.experiment_execution.models import ArtifactRequirement
from turing_research_plus.experiment_route.models import ExperimentRouteSpec

DEFAULT_ACCEPTANCE_CRITERIA = [
    "artifact exists in a reviewable local or exported bundle",
    "artifact has source metadata",
    "artifact is not private raw data",
    "artifact is not promoted to observed evidence automatically",
]


def build_artifact_requirements(route: ExperimentRouteSpec) -> list[ArtifactRequirement]:
    """Build artifact requirements from route-level and stage-level outputs."""

    requirements: list[ArtifactRequirement] = []
    for index, item in enumerate(route.artifact_requirements, start=1):
        requirements.append(
            ArtifactRequirement(
                artifact_id=f"{route.route_id}-artifact-{index}",
                description=item,
                acceptance_criteria=list(DEFAULT_ACCEPTANCE_CRITERIA),
            )
        )

    existing_descriptions = {item.description for item in requirements}
    for stage in route.stages:
        for output in stage.outputs:
            if output not in existing_descriptions:
                existing_descriptions.add(output)
                requirements.append(
                    ArtifactRequirement(
                        artifact_id=f"{route.route_id}-{stage.id}-{_slug(output)}",
                        description=output,
                        source_stage_id=stage.id,
                        acceptance_criteria=list(DEFAULT_ACCEPTANCE_CRITERIA),
                    )
                )
    return requirements


def _slug(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("/", "-")
        .replace(" ", "-")
        .replace("_", "-")
    )
