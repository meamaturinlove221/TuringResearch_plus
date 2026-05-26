"""Human confirmation packet for return import review."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.session_runtime.import_decision import (
    ImportDecision,
    default_import_decision_from_verifier,
    render_import_decision,
)
from turing_research_plus.session_runtime.ledger_proposal import (
    LedgerProposalPacket,
    build_ledger_proposal_packet,
    render_ledger_proposal_packet,
)
from turing_research_plus.session_runtime.return_verifier import (
    ReturnVerifierReport,
    render_return_verifier_report,
)


class HumanConfirmationChecklist(BaseModel):
    """Checklist required before any manual ledger import."""

    model_config = ConfigDict(extra="forbid")

    items: list[str] = Field(default_factory=list)
    all_required: bool = True


class HumanConfirmationPacket(BaseModel):
    """Review packet produced after return verification."""

    model_config = ConfigDict(extra="forbid")

    confirmation_id: str = Field(min_length=1)
    verifier_report: ReturnVerifierReport
    decision: ImportDecision
    ledger_proposal: LedgerProposalPacket
    checklist: HumanConfirmationChecklist = Field(
        default_factory=lambda: HumanConfirmationChecklist(
            items=[
                "Return verifier report has been reviewed.",
                "Remote claims are not trusted as observed evidence.",
                "Unsafe files and checksum mismatches are absent or blocked.",
                "Accepted updates are still proposed-only.",
                "Evidence Ledger write is manual and separate.",
            ]
        )
    )
    auto_write_evidence_ledger: bool = False
    remote_claims_trusted: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_confirmation_boundary(self) -> Self:
        if self.auto_write_evidence_ledger:
            raise ValueError("human confirmation packet cannot auto-write evidence")
        if self.remote_claims_trusted:
            raise ValueError("human confirmation packet cannot trust remote claims")
        if not self.requires_human_review:
            raise ValueError("human confirmation packet requires human review")
        if self.decision.return_id != self.verifier_report.return_id:
            raise ValueError("decision return_id must match verifier report")
        if self.ledger_proposal.return_id != self.verifier_report.return_id:
            raise ValueError("ledger proposal return_id must match verifier report")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether the packet blocks manual import review."""

        return self.verifier_report.release_blocker or self.decision.blocks_import


def build_human_confirmation_packet(
    verifier_report: ReturnVerifierReport,
    *,
    confirmation_id: str | None = None,
    decision: ImportDecision | None = None,
) -> HumanConfirmationPacket:
    """Build a human confirmation packet without writing the Evidence Ledger."""

    import_decision = decision or default_import_decision_from_verifier(verifier_report)
    proposal = build_ledger_proposal_packet(
        decision=import_decision,
        proposed_updates=verifier_report.proposed_updates.updates,
    )
    return HumanConfirmationPacket(
        confirmation_id=confirmation_id or f"{verifier_report.return_id}-confirmation",
        verifier_report=verifier_report,
        decision=import_decision,
        ledger_proposal=proposal,
    )


def render_human_confirmation_packet(packet: HumanConfirmationPacket) -> str:
    """Render a human confirmation packet as Markdown."""

    lines = [
        f"# Human Confirmation Packet: {packet.confirmation_id}",
        "",
        f"- Return id: `{packet.verifier_report.return_id}`",
        f"- Release blocker: `{str(packet.release_blocker).lower()}`",
        "- Auto-write Evidence Ledger: `false`",
        "- Remote claims trusted: `false`",
        "- Requires human review: `true`",
        "",
        render_return_verifier_report(packet.verifier_report).rstrip(),
        "",
        render_import_decision(packet.decision).rstrip(),
        "",
        render_ledger_proposal_packet(packet.ledger_proposal).rstrip(),
        "",
        "## Confirmation Checklist",
        "",
    ]
    lines.extend([f"- [ ] {item}" for item in packet.checklist.items])
    return "\n".join(lines) + "\n"


def write_human_confirmation_packet(packet: HumanConfirmationPacket, output_path: Path) -> Path:
    """Write a human confirmation packet Markdown file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_human_confirmation_packet(packet), encoding="utf-8")
    return output_path
