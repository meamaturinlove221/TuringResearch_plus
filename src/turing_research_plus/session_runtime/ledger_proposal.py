"""Evidence Ledger proposal packet for human-confirmed return imports."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.session_runtime.import_decision import (
    ImportDecision,
    ImportDecisionStatus,
)
from turing_research_plus.session_runtime.proposed_updates import ProposedEvidenceUpdate


class LedgerProposalEntry(BaseModel):
    """One proposed ledger entry derived from a reviewed return update."""

    model_config = ConfigDict(extra="forbid")

    update_id: str = Field(min_length=1)
    claim: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    proposed_status: str = "proposed"
    write_mode: str = "manual-review-only"
    observed_result: bool = False
    requires_human_review: bool = True


class LedgerProposalPacket(BaseModel):
    """Review-only Evidence Ledger proposal packet."""

    model_config = ConfigDict(extra="forbid")

    return_id: str = Field(min_length=1)
    decision_status: ImportDecisionStatus
    entries: list[LedgerProposalEntry] = Field(default_factory=list)
    auto_write_evidence_ledger: bool = False
    proposed_only: bool = True
    requires_human_review: bool = True

    @property
    def ready_for_manual_import(self) -> bool:
        """Return whether a human accepted entries for manual import review."""

        return self.decision_status in {
            ImportDecisionStatus.ACCEPT,
            ImportDecisionStatus.PARTIAL_ACCEPT,
        } and bool(self.entries)


def build_ledger_proposal_packet(
    *,
    decision: ImportDecision,
    proposed_updates: list[ProposedEvidenceUpdate],
) -> LedgerProposalPacket:
    """Build a proposed-only ledger packet from a human decision."""

    accepted = set(decision.accepted_update_ids)
    include_all = decision.status == ImportDecisionStatus.ACCEPT
    entries: list[LedgerProposalEntry] = []
    if decision.status in {
        ImportDecisionStatus.ACCEPT,
        ImportDecisionStatus.PARTIAL_ACCEPT,
    }:
        for update in proposed_updates:
            if include_all or update.update_id in accepted:
                entries.append(
                    LedgerProposalEntry(
                        update_id=update.update_id,
                        claim=update.claim,
                        evidence_refs=list(update.evidence_refs),
                    )
                )

    return LedgerProposalPacket(
        return_id=decision.return_id,
        decision_status=decision.status,
        entries=entries,
    )


def render_ledger_proposal_packet(packet: LedgerProposalPacket) -> str:
    """Render ledger proposals as review-only Markdown."""

    lines = [
        f"## Ledger Proposal Packet: {packet.return_id}",
        "",
        f"- Decision status: `{packet.decision_status}`",
        f"- Ready for manual import: `{str(packet.ready_for_manual_import).lower()}`",
        "- Auto-write Evidence Ledger: `false`",
        "- Proposed only: `true`",
        "- Requires human review: `true`",
        "",
        "Entries:",
    ]
    lines.extend(
        [
            f"- `{item.update_id}` `{item.proposed_status}`: {item.claim}"
            for item in packet.entries
        ]
        or ["- None."]
    )
    return "\n".join(lines) + "\n"
