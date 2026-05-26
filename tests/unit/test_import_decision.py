from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from turing_research_plus.handoff.manifest import sha256_file
from turing_research_plus.session_runtime.import_decision import (
    ImportDecision,
    ImportDecisionStatus,
    default_import_decision_from_verifier,
    render_import_decision,
)
from turing_research_plus.session_runtime.return_verifier import verify_return_package


def test_default_import_decision_requires_more_review_for_pass(tmp_path: Path) -> None:
    _write_return(tmp_path)
    verifier = verify_return_package(tmp_path, return_id="return-demo")

    decision = default_import_decision_from_verifier(verifier)

    assert decision.status == ImportDecisionStatus.REQUIRES_MORE_REVIEW
    assert decision.blocks_import is True
    assert decision.auto_write_evidence_ledger is False
    assert decision.remote_claims_trusted is False


def test_default_import_decision_blocks_unsafe_verifier(tmp_path: Path) -> None:
    _write_return(tmp_path, include_all=False)
    verifier = verify_return_package(tmp_path, return_id="return-demo")

    decision = default_import_decision_from_verifier(verifier)

    assert decision.status == ImportDecisionStatus.UNSAFE_BLOCKED
    assert decision.rejected_update_ids == ["u1"]


def test_import_decision_supports_all_statuses() -> None:
    statuses = {
        ImportDecisionStatus.ACCEPT,
        ImportDecisionStatus.REJECT,
        ImportDecisionStatus.PARTIAL_ACCEPT,
        ImportDecisionStatus.REQUIRES_MORE_REVIEW,
        ImportDecisionStatus.UNSAFE_BLOCKED,
    }

    assert {item.value for item in statuses} == {
        "accept",
        "reject",
        "partial_accept",
        "requires_more_review",
        "unsafe_blocked",
    }


def test_import_decision_rejects_auto_write() -> None:
    with pytest.raises(ValidationError):
        ImportDecision(
            return_id="return-demo",
            status=ImportDecisionStatus.ACCEPT,
            auto_write_evidence_ledger=True,
        )


def test_render_import_decision_states_boundaries() -> None:
    text = render_import_decision(
        ImportDecision(return_id="return-demo", status=ImportDecisionStatus.REJECT)
    )

    assert "Auto-write Evidence Ledger: `false`" in text
    assert "Remote claims trusted: `false`" in text


def _write_return(root: Path, *, include_all: bool = True) -> None:
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
        if include_all or name != "ARTIFACT_INDEX.md":
            (root / name).write_text(text, encoding="utf-8")
    sums = [
        f"{sha256_file(root / name)}  {name}"
        for name in payloads
        if (root / name).exists()
    ]
    (root / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
