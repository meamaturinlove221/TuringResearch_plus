from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.archive_writer import sha256_file
from turing_research_plus.session_runtime.unpack_safety import (
    ArchiveMember,
    archive_members_from_directory,
    validate_archive_members,
    validate_return_archive_directory,
)


def test_unpack_safety_blocks_traversal_dotfile_and_symlink() -> None:
    report = validate_archive_members(
        [
            ArchiveMember(path="../secret.txt"),
            ArchiveMember(path=".env"),
            ArchiveMember(path="link", member_type="symlink", link_target="../target"),
        ]
    )
    finding_ids = {finding.finding_id for finding in report.findings}

    assert report.release_blocker is True
    assert "path-traversal" in finding_ids
    assert "dotfile-denylist" in finding_ids
    assert "symlink-blocked" in finding_ids
    assert "unsafe-symlink-target" in finding_ids


def test_unpack_safety_requires_checksums_before_ingest() -> None:
    report = validate_archive_members(
        [
            ArchiveMember(
                path="FINAL_STATUS.json",
                expected_sha256="a" * 64,
                actual_sha256="b" * 64,
            )
        ],
        require_checksums=True,
    )

    assert "checksum-mismatch" in {finding.finding_id for finding in report.findings}


def test_archive_members_from_directory_reports_files(tmp_path: Path) -> None:
    (tmp_path / "RUN_STATUS.json").write_text("{}\n", encoding="utf-8")

    members = archive_members_from_directory(tmp_path)

    assert [member.path for member in members] == ["RUN_STATUS.json"]


def test_validate_return_archive_directory_passes_complete_return(tmp_path: Path) -> None:
    _write_required_return(tmp_path)

    report = validate_return_archive_directory(tmp_path)

    assert report.release_blocker is False
    assert report.return_archive_validation is True


def test_validate_return_archive_directory_blocks_missing_file(tmp_path: Path) -> None:
    _write_required_return(tmp_path)
    (tmp_path / "FAILURE_REPORT.md").unlink()

    report = validate_return_archive_directory(tmp_path)

    assert "missing-return-file" in {finding.finding_id for finding in report.findings}


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
