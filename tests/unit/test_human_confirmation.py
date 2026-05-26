from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.manifest import sha256_file
from turing_research_plus.session_runtime.human_confirmation import (
    build_human_confirmation_packet,
    render_human_confirmation_packet,
    write_human_confirmation_packet,
)
from turing_research_plus.session_runtime.import_decision import (
    ImportDecision,
    ImportDecisionStatus,
)
from turing_research_plus.session_runtime.return_verifier import verify_return_package


def test_human_confirmation_defaults_to_more_review(tmp_path: Path) -> None:
    _write_return(tmp_path)
    verifier = verify_return_package(tmp_path, return_id="return-demo")

    packet = build_human_confirmation_packet(verifier)

    assert packet.decision.status == ImportDecisionStatus.REQUIRES_MORE_REVIEW
    assert packet.ledger_proposal.entries == []
    assert packet.auto_write_evidence_ledger is False
    assert packet.remote_claims_trusted is False
    assert packet.release_blocker is True


def test_human_confirmation_can_package_manual_accept_without_auto_write(
    tmp_path: Path,
) -> None:
    _write_return(tmp_path)
    verifier = verify_return_package(tmp_path, return_id="return-demo")
    decision = ImportDecision(
        return_id="return-demo",
        status=ImportDecisionStatus.ACCEPT,
        accepted_update_ids=["u1"],
        rationale="Human accepted this proposed update for manual import review.",
    )

    packet = build_human_confirmation_packet(verifier, decision=decision)

    assert packet.release_blocker is False
    assert [entry.update_id for entry in packet.ledger_proposal.entries] == ["u1"]
    assert packet.ledger_proposal.entries[0].observed_result is False
    assert packet.ledger_proposal.auto_write_evidence_ledger is False


def test_render_and_write_human_confirmation_packet(tmp_path: Path) -> None:
    _write_return(tmp_path)
    verifier = verify_return_package(tmp_path, return_id="return-demo")
    packet = build_human_confirmation_packet(verifier)

    text = render_human_confirmation_packet(packet)
    output = write_human_confirmation_packet(packet, tmp_path / "CONFIRMATION.md")

    assert "Human Confirmation Packet" in text
    assert "Auto-write Evidence Ledger: `false`" in text
    assert output.read_text(encoding="utf-8") == text


def _write_return(root: Path) -> None:
    payloads = {
        "RUN_STATUS.json": '{"status": "completed", "mode": "fake"}\n',
        "FINAL_STATUS.json": '{"status": "requires-human-review"}\n',
        "ARTIFACT_INDEX.md": "# Artifact Index\n\n- review outputs only\n",
        "FAILURE_REPORT.md": "# Failure Report\n\nNo blocker in fake fixture.\n",
        "PROPOSED_EVIDENCE_UPDATES.json": (
            '{"updates": [{"update_id": "u1", "claim": "Review-only update", '
            '"status": "proposed"}]}\n'
        ),
    }
    for name, text in payloads.items():
        (root / name).write_text(text, encoding="utf-8")
    sums = [f"{sha256_file(root / name)}  {name}" for name in payloads]
    (root / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
