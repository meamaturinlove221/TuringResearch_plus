"""Models for the Experiment Route DSL."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RouteStatus(StrEnum):
    """Route planning status."""

    PLANNED = "planned"
    REQUIRES_REAL_EXPERIMENT = "requires-real-experiment"
    BLOCKED = "blocked"
    COMPILED = "compiled"


class ExperimentRouteStage(BaseModel):
    """One route stage."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    hard_gates: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
    fallback: str | None = None
    done_criteria: list[str] = Field(default_factory=list)


class ExperimentRouteSpec(BaseModel):
    """Structured route specification."""

    model_config = ConfigDict(extra="forbid")

    route_id: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    context: str = Field(min_length=1)
    status: RouteStatus = RouteStatus.PLANNED
    allowed_inputs: list[str] = Field(default_factory=list)
    forbidden_actions: list[str] = Field(default_factory=list)
    stages: list[ExperimentRouteStage] = Field(min_length=1)
    hard_gates: list[str] = Field(default_factory=list)
    fallback_routes: list[str] = Field(default_factory=list)
    final_states: list[str] = Field(default_factory=list)
    artifact_requirements: list[str] = Field(default_factory=list)
    cleanup_requirements: list[str] = Field(default_factory=list)
    advisor_outputs: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def route_must_forbid_execution_claims(self) -> Self:
        combined = " ".join(self.forbidden_actions).lower()
        if "claim experiment completion" not in combined:
            raise ValueError("route must forbid claiming experiment completion")
        return self

    def to_markdown(self) -> str:
        """Render the route as Markdown without claiming execution."""

        lines = [
            f"# Experiment Route: {self.route_id}",
            "",
            f"- Status: {self.status.value}",
            "- Execution: not executed by TuringResearch",
            f"- Goal: {self.goal}",
            "",
            "## Context",
            "",
            self.context,
            "",
            "## Stages",
        ]
        for stage in self.stages:
            lines.extend(
                [
                    "",
                    f"### {stage.id}: {stage.name}",
                    "",
                    f"- Purpose: {stage.purpose}",
                    f"- Inputs: {', '.join(stage.inputs) or 'none'}",
                    f"- Outputs: {', '.join(stage.outputs) or 'none'}",
                    f"- Hard gates: {', '.join(stage.hard_gates) or 'none'}",
                    f"- Failure modes: {', '.join(stage.failure_modes) or 'none'}",
                    f"- Fallback: {stage.fallback or 'none'}",
                    f"- Done criteria: {'; '.join(stage.done_criteria) or 'none'}",
                ]
            )
        lines.extend(
            [
                "",
                "## Forbidden Actions",
                "",
                *[f"- {item}" for item in self.forbidden_actions],
                "",
                "## Final States",
                "",
                *[f"- {item}" for item in self.final_states],
            ]
        )
        return "\n".join(lines) + "\n"


class ControllerPromptDraft(BaseModel):
    """Prompt draft generated from a route spec."""

    model_config = ConfigDict(extra="forbid")

    route_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: RouteStatus
    body: str = Field(min_length=1)
    warnings: list[str] = Field(default_factory=list)


class ExperimentRouteCompileInput(BaseModel):
    """Compile request for an experiment route."""

    model_config = ConfigDict(extra="forbid")

    route_path: Path | None = None
    route_data: dict[str, Any] | None = None

    @model_validator(mode="after")
    def exactly_one_route_source(self) -> Self:
        if (self.route_path is None) == (self.route_data is None):
            raise ValueError("provide exactly one of route_path or route_data")
        return self
