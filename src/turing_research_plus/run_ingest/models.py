"""Models for Modal / experiment run ingestion."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.failure.models import FailureCategory


class RunSourceType(StrEnum):
    """Supported run source types."""

    MODAL_FIXTURE = "modal_fixture"
    MODAL_EXPORT = "modal_export"
    LOCAL_VGGT_BUNDLE = "local_vggt_bundle"
    THIN_REVIEW_BUNDLE = "thin_review_bundle"
    MANUAL_SUMMARY = "manual_summary"


class RunStatus(StrEnum):
    """Recognized experiment run statuses."""

    REVIEW_READY_NOT_PROMOTED = "REVIEW_READY_NOT_PROMOTED"
    ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS = "ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS"
    HARD_BLOCKED = "HARD_BLOCKED"
    RUN_FAILED = "RUN_FAILED"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


class BackendStatus(StrEnum):
    """Sparse backend status from run metadata."""

    REAL_BACKEND_CONFIRMED = "real_backend_confirmed"
    REAL_BACKEND_MISSING = "real_backend_missing"
    FALLBACK_USED = "fallback_used"
    UNKNOWN = "unknown"


class CandidateResult(BaseModel):
    """Candidate result summary from a run."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    score: float | None = None
    status: str = Field(default="unknown", min_length=1)
    notes: list[str] = Field(default_factory=list)


class RunArtifact(BaseModel):
    """One expected or observed run artifact."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1)
    present: bool = False
    required: bool = True
    notes: list[str] = Field(default_factory=list)


class HardGateResult(BaseModel):
    """Hard gate result from an ingested run."""

    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(min_length=1)
    passed: bool = False
    reason: str = Field(min_length=1)


class RunIngestRequest(BaseModel):
    """Input for local experiment run ingestion."""

    model_config = ConfigDict(extra="forbid")

    source_type: RunSourceType
    source_path: Path
    route_id: str = Field(default="modal_sparseconv_v0", min_length=1)
    run_id: str | None = None


class RunIngestReport(BaseModel):
    """Structured report for ingested Modal/local/thin run bundles."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    source_type: RunSourceType
    source_path: str = Field(min_length=1)
    status: RunStatus
    duration: str | None = None
    backend_status: BackendStatus = BackendStatus.UNKNOWN
    candidates: list[CandidateResult] = Field(default_factory=list)
    best_candidate: CandidateResult | None = None
    artifacts: list[RunArtifact] = Field(default_factory=list)
    missing_artifacts: list[str] = Field(default_factory=list)
    hard_gate_results: list[HardGateResult] = Field(default_factory=list)
    failure_categories: list[FailureCategory] = Field(default_factory=list)
    evidence_updates: list[dict[str, Any]] = Field(default_factory=list)
    advisor_pack_inputs: dict[str, Any] = Field(default_factory=dict)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def prevent_sparseconv_success_without_real_backend(self) -> Self:
        success_like = self.status == RunStatus.REVIEW_READY_NOT_PROMOTED
        if success_like and self.backend_status != BackendStatus.REAL_BACKEND_CONFIRMED:
            if FailureCategory.NOT_ENOUGH_EVIDENCE not in self.failure_categories:
                self.failure_categories.append(FailureCategory.NOT_ENOUGH_EVIDENCE)
        return self

    def to_markdown(self) -> str:
        """Render a concise Markdown report."""

        lines = [
            f"# Run Ingest Report: {self.run_id}",
            "",
            f"- Route: `{self.route_id}`",
            f"- Source type: `{self.source_type}`",
            f"- Status: `{self.status}`",
            f"- Backend status: `{self.backend_status}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            "",
            "## Missing Artifacts",
            "",
            *[f"- {item}" for item in self.missing_artifacts],
            "",
            "## Failure Categories",
            "",
            *[f"- `{item}`" for item in self.failure_categories],
            "",
            "## Proposed Evidence Updates",
            "",
            *[
                f"- {item.get('version_label')}: {item.get('status')}"
                for item in self.evidence_updates
            ],
        ]
        return "\n".join(lines) + "\n"


def run_evidence_ref(run_id: str, locator: str, quote: str) -> EvidenceRef:
    """Create an EvidenceRef for local run fixture metadata."""

    return EvidenceRef(
        source_id=run_id,
        locator=locator,
        quote=quote,
        confidence=0.6,
    )
