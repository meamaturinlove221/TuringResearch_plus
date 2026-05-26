"""Human import decision models for verified return packages."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.session_runtime.return_verifier import (
    ReturnVerifierReport,
    ReturnVerifierStatus,
)


class ImportDecisionStatus(StrEnum):
    """Allowed human import decision states."""

    ACCEPT = "accept"
    REJECT = "reject"
    PARTIAL_ACCEPT = "partial_accept"
    REQUIRES_MORE_REVIEW = "requires_more_review"
    UNSAFE_BLOCKED = "unsafe_blocked"


class ImportDecision(BaseModel):
    """Human decision over a return verifier report."""

    model_config = ConfigDict(extra="forbid")

    return_id: str = Field(min_length=1)
    status: ImportDecisionStatus = ImportDecisionStatus.REQUIRES_MORE_REVIEW
    accepted_update_ids: list[str] = Field(default_factory=list)
    rejected_update_ids: list[str] = Field(default_factory=list)
    rationale: str = "Human review required before import."
    decided_by: str = "human-reviewer"
    remote_claims_trusted: bool = False
    auto_write_evidence_ledger: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_human_import_boundary(self) -> Self:
        if self.remote_claims_trusted:
            raise ValueError("return import cannot trust remote claims directly")
        if self.auto_write_evidence_ledger:
            raise ValueError("return import cannot auto-write the evidence ledger")
        if not self.requires_human_review:
            raise ValueError("return import decision requires human review")
        if self.status == ImportDecisionStatus.ACCEPT and self.rejected_update_ids:
            raise ValueError("accept decision cannot include rejected updates")
        if self.status == ImportDecisionStatus.REJECT and self.accepted_update_ids:
            raise ValueError("reject decision cannot include accepted updates")
        if self.status == ImportDecisionStatus.PARTIAL_ACCEPT and not self.accepted_update_ids:
            raise ValueError("partial_accept requires at least one accepted update")
        return self

    @property
    def blocks_import(self) -> bool:
        """Return whether this decision blocks import proposal review."""

        return self.status in {
            ImportDecisionStatus.REJECT,
            ImportDecisionStatus.REQUIRES_MORE_REVIEW,
            ImportDecisionStatus.UNSAFE_BLOCKED,
        }


def default_import_decision_from_verifier(report: ReturnVerifierReport) -> ImportDecision:
    """Build the safest default decision from a verifier report."""

    if report.status == ReturnVerifierStatus.BLOCKED:
        return ImportDecision(
            return_id=report.return_id,
            status=ImportDecisionStatus.UNSAFE_BLOCKED,
            rejected_update_ids=[update.update_id for update in report.proposed_updates.updates],
            rationale="Return verifier blocked this package; do not import.",
        )
    return ImportDecision(
        return_id=report.return_id,
        status=ImportDecisionStatus.REQUIRES_MORE_REVIEW,
        rationale="Verifier passed, but a human must accept or reject proposed updates.",
    )


def render_import_decision(decision: ImportDecision) -> str:
    """Render an import decision as Markdown."""

    lines = [
        f"## Import Decision: {decision.return_id}",
        "",
        f"- Status: `{decision.status}`",
        f"- Decided by: `{decision.decided_by}`",
        f"- Blocks import: `{str(decision.blocks_import).lower()}`",
        "- Remote claims trusted: `false`",
        "- Auto-write Evidence Ledger: `false`",
        "- Requires human review: `true`",
        f"- Rationale: {decision.rationale}",
        "",
        "Accepted update ids:",
    ]
    lines.extend([f"- `{item}`" for item in decision.accepted_update_ids] or ["- None."])
    lines.append("")
    lines.append("Rejected update ids:")
    lines.extend([f"- `{item}`" for item in decision.rejected_update_ids] or ["- None."])
    return "\n".join(lines) + "\n"
