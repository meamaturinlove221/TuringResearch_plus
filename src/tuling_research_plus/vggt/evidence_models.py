"""VGGT / SMPL-X evidence ledger models."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tuling_research_plus.artifacts.models import EvidenceRef


class VGGTEvidenceStatus(StrEnum):
    """Status labels allowed in the VGGT dogfooding evidence ledger."""

    OBSERVED = "observed"
    LOCAL_OBSERVED = "local-observed"
    PLANNED = "planned"
    FAKE_DATA = "fake-data"
    FAILED = "failed"
    HARD_BLOCKED = "hard-blocked"
    REQUIRES_REAL_PAPER = "requires-real-paper"
    REQUIRES_REAL_EXPERIMENT = "requires-real-experiment"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"
    NOT_ENOUGH_EVIDENCE = "not-enough-evidence"


class VGGTEvidenceRow(BaseModel):
    """One evidence row for a VGGT / SMPL-X milestone or claim."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    version_label: str = Field(min_length=1)
    claim: str = Field(min_length=1)
    status: VGGTEvidenceStatus
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    source_files: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_evidence_boundary(self) -> Self:
        evidence_required = {
            VGGTEvidenceStatus.OBSERVED,
            VGGTEvidenceStatus.LOCAL_OBSERVED,
            VGGTEvidenceStatus.FAILED,
            VGGTEvidenceStatus.HARD_BLOCKED,
        }
        if self.status in evidence_required and not self.evidence_refs:
            msg = f"{self.status.value} evidence row requires evidence_refs"
            raise ValueError(msg)
        if self.status == VGGTEvidenceStatus.LOCAL_OBSERVED and not self.source_files:
            msg = "local-observed evidence row requires source_files"
            raise ValueError(msg)
        if (
            self.status
            in {
                VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW,
                VGGTEvidenceStatus.NOT_ENOUGH_EVIDENCE,
                VGGTEvidenceStatus.HARD_BLOCKED,
            }
            and not (self.blockers or self.next_actions)
        ):
            msg = f"{self.status.value} evidence row requires blockers or next_actions"
            raise ValueError(msg)
        return self

    @property
    def is_success_claim(self) -> bool:
        """Return whether this row is strong enough to support a success claim."""

        return self.status in {
            VGGTEvidenceStatus.OBSERVED,
            VGGTEvidenceStatus.LOCAL_OBSERVED,
        }


class VGGTEvidenceLedger(BaseModel):
    """Evidence ledger for VGGT / SMPL-X dogfooding milestones."""

    model_config = ConfigDict(extra="forbid")

    ledger_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    project: str = "VGGT / SMPL-X Human Prior"
    rows: list[VGGTEvidenceRow] = Field(min_length=1)
    generated_from: list[str] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def row_for(self, version_label: str) -> VGGTEvidenceRow:
        """Return a row by version label."""

        for row in self.rows:
            if row.version_label == version_label:
                return row
        raise KeyError(version_label)

    def rows_with_status(self, status: VGGTEvidenceStatus) -> list[VGGTEvidenceRow]:
        """Return rows that match a status."""

        return [row for row in self.rows if row.status == status]

    def to_markdown(self) -> str:
        """Serialize the ledger to a compact Markdown table."""

        lines = [
            f"# TulingResearch Plus VGGT Evidence Ledger: {self.run_id}",
            "",
            "| Version | Status | Claim | Limitations | Blockers | Next actions |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for row in self.rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        row.version_label,
                        row.status.value,
                        row.claim.replace("|", "/"),
                        "; ".join(row.limitations).replace("|", "/"),
                        "; ".join(row.blockers).replace("|", "/"),
                        "; ".join(row.next_actions).replace("|", "/"),
                    ]
                )
                + " |"
            )
        if self.missing_inputs:
            lines.extend(["", "## Missing Inputs"])
            lines.extend(f"- `{item}`" for item in self.missing_inputs)
        return "\n".join(lines) + "\n"


class VGGTEvidenceLedgerBuildInput(BaseModel):
    """Input for building the VGGT evidence ledger from local scan summaries."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = "vggt-local-scan"
    local_scan_summary_path: Path
    local_scan_artifact_index_path: Path
    local_scan_evidence_ledger_path: Path | None = None

