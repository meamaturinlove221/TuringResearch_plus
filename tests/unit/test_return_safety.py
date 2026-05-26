from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.manifest import sha256_file
from turing_research_plus.session_runtime.return_manifest import load_return_manifest
from turing_research_plus.session_runtime.return_safety import run_return_safety_checks


def _write_required_return(root: Path) -> None:
    for name in [
        "RUN_STATUS.json",
        "FINAL_STATUS.json",
        "ARTIFACT_INDEX.md",
        "FAILURE_REPORT.md",
        "PROPOSED_EVIDENCE_UPDATES.json",
    ]:
        (root / name).write_text("{}\n" if name.endswith(".json") else "review\n", encoding="utf-8")
    sums = []
    for name in [
        "RUN_STATUS.json",
        "FINAL_STATUS.json",
        "ARTIFACT_INDEX.md",
        "FAILURE_REPORT.md",
        "PROPOSED_EVIDENCE_UPDATES.json",
    ]:
        sums.append(f"{sha256_file(root / name)}  {name}")
    (root / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")


def test_return_safety_passes_complete_checksummed_return(tmp_path: Path) -> None:
    _write_required_return(tmp_path)
    manifest = load_return_manifest(tmp_path)

    report = run_return_safety_checks(tmp_path, manifest)

    assert report.release_blocker is False


def test_return_safety_blocks_checksum_mismatch(tmp_path: Path) -> None:
    _write_required_return(tmp_path)
    (tmp_path / "FINAL_STATUS.json").write_text('{"tampered": true}\n', encoding="utf-8")

    report = run_return_safety_checks(tmp_path, load_return_manifest(tmp_path))

    assert "checksum-mismatch" in {item.finding_id for item in report.findings}


def test_return_safety_blocks_unsafe_extra_file(tmp_path: Path) -> None:
    _write_required_return(tmp_path)
    (tmp_path / "predictions.npz").write_bytes(b"fake")

    report = run_return_safety_checks(tmp_path, load_return_manifest(tmp_path))

    assert any(item.path == "predictions.npz" for item in report.findings)


def test_return_safety_blocks_fake_observed_claim(tmp_path: Path) -> None:
    _write_required_return(tmp_path)
    (tmp_path / "FAILURE_REPORT.md").write_text(
        "Fake demo output is observed and verified.\n",
        encoding="utf-8",
    )

    report = run_return_safety_checks(tmp_path, load_return_manifest(tmp_path))

    assert "fake-result-observed-claim" in {item.finding_id for item in report.findings}
