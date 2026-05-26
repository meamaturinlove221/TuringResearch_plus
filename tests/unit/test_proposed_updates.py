from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from turing_research_plus.session_runtime.proposed_updates import (
    ProposedEvidenceUpdate,
    load_proposed_updates,
)


def test_proposed_update_rejects_observed_status() -> None:
    with pytest.raises(ValidationError):
        ProposedEvidenceUpdate(
            update_id="u1",
            claim="demo claim",
            status="observed",
        )


def test_load_proposed_updates_keeps_updates_proposed_only(tmp_path: Path) -> None:
    path = tmp_path / "PROPOSED_EVIDENCE_UPDATES.json"
    path.write_text(
        '{"updates": [{"update_id": "u1", "claim": "Review this", "status": "proposed"}]}',
        encoding="utf-8",
    )

    report = load_proposed_updates(path)

    assert report.release_blocker is False
    assert report.updates[0].status == "proposed"
    assert report.auto_apply_evidence_updates is False


def test_load_proposed_updates_reports_unsafe_observed_update(tmp_path: Path) -> None:
    path = tmp_path / "PROPOSED_EVIDENCE_UPDATES.json"
    path.write_text(
        '{"updates": [{"update_id": "u1", "claim": "Fake claim", "status": "observed"}]}',
        encoding="utf-8",
    )

    report = load_proposed_updates(path)

    assert report.release_blocker is True
    assert report.errors
