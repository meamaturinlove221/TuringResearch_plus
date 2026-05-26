from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.manifest import sha256_file
from turing_research_plus.session_runtime.return_verifier import (
    ReturnVerifierStatus,
    render_return_verifier_report,
    verify_return_package,
)


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


def test_return_verifier_passes_complete_fake_return(tmp_path: Path) -> None:
    _write_return(tmp_path)

    report = verify_return_package(tmp_path, return_id="return-demo")

    assert report.status == ReturnVerifierStatus.PASS
    assert report.auto_write_evidence_ledger is False
    assert report.proposed_updates_only is True
    assert report.requires_human_review is True
    assert report.proposed_updates.updates[0].status == "proposed"


def test_return_verifier_blocks_missing_artifact(tmp_path: Path) -> None:
    _write_return(tmp_path, include_all=False)

    report = verify_return_package(tmp_path)

    assert report.status == ReturnVerifierStatus.BLOCKED
    assert "ARTIFACT_INDEX.md" in report.missing_artifacts


def test_render_return_verifier_report_states_review_boundary(tmp_path: Path) -> None:
    _write_return(tmp_path)
    text = render_return_verifier_report(verify_return_package(tmp_path))

    assert "Auto-write Evidence Ledger: `false`" in text
    assert "Proposed updates only: `true`" in text
    assert "Requires human review: `true`" in text
