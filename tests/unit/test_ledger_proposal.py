from __future__ import annotations

from turing_research_plus.session_runtime.import_decision import (
    ImportDecision,
    ImportDecisionStatus,
)
from turing_research_plus.session_runtime.ledger_proposal import (
    build_ledger_proposal_packet,
    render_ledger_proposal_packet,
)
from turing_research_plus.session_runtime.proposed_updates import ProposedEvidenceUpdate


def test_ledger_proposal_is_empty_until_human_accepts() -> None:
    packet = build_ledger_proposal_packet(
        decision=ImportDecision(
            return_id="return-demo",
            status=ImportDecisionStatus.REQUIRES_MORE_REVIEW,
        ),
        proposed_updates=[_update("u1")],
    )

    assert packet.entries == []
    assert packet.ready_for_manual_import is False
    assert packet.auto_write_evidence_ledger is False
    assert packet.proposed_only is True


def test_ledger_proposal_accepts_only_selected_updates() -> None:
    packet = build_ledger_proposal_packet(
        decision=ImportDecision(
            return_id="return-demo",
            status=ImportDecisionStatus.PARTIAL_ACCEPT,
            accepted_update_ids=["u2"],
        ),
        proposed_updates=[_update("u1"), _update("u2")],
    )

    assert [entry.update_id for entry in packet.entries] == ["u2"]
    assert packet.entries[0].observed_result is False
    assert packet.ready_for_manual_import is True


def test_render_ledger_proposal_packet_states_manual_boundary() -> None:
    packet = build_ledger_proposal_packet(
        decision=ImportDecision(
            return_id="return-demo",
            status=ImportDecisionStatus.ACCEPT,
            accepted_update_ids=["u1"],
        ),
        proposed_updates=[_update("u1")],
    )
    text = render_ledger_proposal_packet(packet)

    assert "Auto-write Evidence Ledger: `false`" in text
    assert "Proposed only: `true`" in text


def _update(update_id: str) -> ProposedEvidenceUpdate:
    return ProposedEvidenceUpdate(
        update_id=update_id,
        claim=f"Review-only claim {update_id}",
        status="proposed",
        evidence_refs=["ARTIFACT_INDEX.md"],
    )
