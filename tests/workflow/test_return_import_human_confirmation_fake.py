from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.human_confirmation import (
    build_human_confirmation_packet,
    write_human_confirmation_packet,
)
from turing_research_plus.session_runtime.import_decision import (
    ImportDecision,
    ImportDecisionStatus,
)
from turing_research_plus.session_runtime.return_verifier import verify_return_package

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "session_runtime" / "return_fixture"


def test_return_import_human_confirmation_fake_fixture(tmp_path: Path) -> None:
    verifier = verify_return_package(FIXTURE, return_id="return-fixture")
    packet = build_human_confirmation_packet(verifier)
    output = write_human_confirmation_packet(packet, tmp_path / "CONFIRMATION_PACKET.md")
    text = output.read_text(encoding="utf-8")

    assert packet.decision.status == ImportDecisionStatus.REQUIRES_MORE_REVIEW
    assert packet.ledger_proposal.entries == []
    assert packet.auto_write_evidence_ledger is False
    assert packet.remote_claims_trusted is False
    assert "Remote claims are not trusted" in text
    assert "Auto-write Evidence Ledger: `false`" in text


def test_return_import_human_confirmation_accepts_manual_proposal(tmp_path: Path) -> None:
    verifier = verify_return_package(FIXTURE, return_id="return-fixture")
    decision = ImportDecision(
        return_id="return-fixture",
        status=ImportDecisionStatus.PARTIAL_ACCEPT,
        accepted_update_ids=["fake-return-proposed-update"],
        rationale="Human accepts one proposed update for manual ledger review.",
    )

    packet = build_human_confirmation_packet(verifier, decision=decision)

    assert packet.ledger_proposal.ready_for_manual_import is True
    assert packet.ledger_proposal.entries[0].write_mode == "manual-review-only"
    assert packet.ledger_proposal.entries[0].observed_result is False


def test_checked_in_return_confirmation_demo_is_public_safe() -> None:
    demo = Path("examples/session_runtime/return_confirmation")

    assert (demo / "README.md").is_file()
    assert (demo / "CONFIRMATION_PACKET.md").is_file()

    text = "\n".join(path.read_text(encoding="utf-8") for path in demo.glob("*.md"))
    assert "fake/demo only" in text
    assert "Auto-write Evidence Ledger: `false`" in text
    assert "Remote claims trusted: `false`" in text
    assert "D:/vggt" not in text
    assert "API_KEY=" not in text
    assert "TOKEN=" not in text
