"""Minimal evidence-edge audit helpers for VGGT ledgers."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vggt.evidence_models import (
    VGGTEvidenceLedger,
    VGGTEvidenceStatus,
)


class VGGTEvidenceEdgeIssue(BaseModel):
    """One conservative issue found in an evidence ledger row."""

    model_config = ConfigDict(extra="forbid")

    version_label: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    message: str = Field(min_length=1)


class VGGTEvidenceEdgeAuditReport(BaseModel):
    """Small audit report for claim-to-evidence traceability."""

    model_config = ConfigDict(extra="forbid")

    ledger_id: str = Field(min_length=1)
    checked_rows: int = Field(ge=0)
    issues: list[VGGTEvidenceEdgeIssue] = Field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Return whether the ledger has no high-severity traceability issues."""

        return not any(issue.severity in {"high", "critical"} for issue in self.issues)


def audit_vggt_evidence_edges(ledger: VGGTEvidenceLedger) -> VGGTEvidenceEdgeAuditReport:
    """Audit existing ledger rows without reading external VGGT paths."""

    issues: list[VGGTEvidenceEdgeIssue] = []
    evidence_required = {
        VGGTEvidenceStatus.OBSERVED,
        VGGTEvidenceStatus.LOCAL_OBSERVED,
        VGGTEvidenceStatus.FAILED,
        VGGTEvidenceStatus.HARD_BLOCKED,
    }

    for row in ledger.rows:
        if row.status in evidence_required and not row.evidence_refs:
            issues.append(
                VGGTEvidenceEdgeIssue(
                    version_label=row.version_label,
                    severity="high",
                    message=f"{row.status.value} row has no evidence_refs",
                )
            )
        if row.status == VGGTEvidenceStatus.LOCAL_OBSERVED and not row.source_files:
            issues.append(
                VGGTEvidenceEdgeIssue(
                    version_label=row.version_label,
                    severity="high",
                    message="local-observed row has no source_files",
                )
            )
        if row.status == VGGTEvidenceStatus.NOT_ENOUGH_EVIDENCE and row.is_success_claim:
            issues.append(
                VGGTEvidenceEdgeIssue(
                    version_label=row.version_label,
                    severity="critical",
                    message="not-enough-evidence row cannot support a success claim",
                )
            )

    return VGGTEvidenceEdgeAuditReport(
        ledger_id=ledger.ledger_id,
        checked_rows=len(ledger.rows),
        issues=issues,
    )
