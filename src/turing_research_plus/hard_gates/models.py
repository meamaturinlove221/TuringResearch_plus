"""Models for reusable hard gates."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import EvidenceRef


class GateOutcome(StrEnum):
    """Allowed hard gate outcomes."""

    PASS = "pass"
    BLOCK = "block"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"
    NOT_ENOUGH_EVIDENCE = "not-enough-evidence"


class GateInputRef(BaseModel):
    """Reference to an input used by a gate."""

    model_config = ConfigDict(extra="forbid")

    ref_id: str = Field(min_length=1)
    ref_type: str = Field(min_length=1)
    status: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)


class GateCondition(BaseModel):
    """One condition inside a hard gate."""

    model_config = ConfigDict(extra="forbid")

    condition_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    required_statuses: list[str] = Field(default_factory=list)
    forbidden_statuses: list[str] = Field(default_factory=list)
    required_evidence: bool = True


class GateSpec(BaseModel):
    """Reusable hard gate definition."""

    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    severity: str = Field(default="high", min_length=1)
    conditions: list[GateCondition] = Field(min_length=1)
    default_block_reason: str = Field(min_length=1)


class GateResult(BaseModel):
    """Validation result for one gate."""

    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(min_length=1)
    outcome: GateOutcome
    reasons: list[str] = Field(default_factory=list)
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def non_pass_outcome_has_reason(self) -> Self:
        if self.outcome != GateOutcome.PASS and not (self.reasons or self.missing_inputs):
            raise ValueError("non-pass gate result requires reasons or missing_inputs")
        return self


class HardGateValidationInput(BaseModel):
    """Input for validating one or more hard gates."""

    model_config = ConfigDict(extra="forbid")

    route_id: str | None = None
    stage_id: str | None = None
    gate_ids: list[str] = Field(min_length=1)
    inputs: list[GateInputRef] = Field(default_factory=list)
    allow_human_review: bool = True


class HardGateValidationReport(BaseModel):
    """Validation report for a hard-gate pass."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    route_id: str | None = None
    stage_id: str | None = None
    results: list[GateResult] = Field(min_length=1)
    summary: str = Field(min_length=1)

    @property
    def passed(self) -> bool:
        """Return whether every gate passed."""

        return all(result.outcome == GateOutcome.PASS for result in self.results)

    def to_markdown(self) -> str:
        """Render a compact Markdown report."""

        lines = [
            f"# Hard Gate Validation: {self.report_id}",
            "",
            f"- Route: {self.route_id or 'n/a'}",
            f"- Stage: {self.stage_id or 'n/a'}",
            f"- Passed: {str(self.passed).lower()}",
            "",
            "| Gate | Outcome | Reasons | Missing inputs |",
            "| --- | --- | --- | --- |",
        ]
        for result in self.results:
            lines.append(
                "| "
                + " | ".join(
                    [
                        result.gate_id,
                        result.outcome.value,
                        "; ".join(result.reasons).replace("|", "/"),
                        "; ".join(result.missing_inputs).replace("|", "/"),
                    ]
                )
                + " |"
            )
        return "\n".join(lines) + "\n"
