from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime import (
    ArchiveMember,
    build_context_pack,
    normalize_archive_member_path,
    validate_archive_members,
    validate_return_archive_directory,
)
from turing_research_plus.session_runtime.archive_writer import sha256_file
from turing_research_plus.session_runtime.context_pack_builder import (
    ContextPackBuildRequest,
)


def test_cross_platform_archive_hardening_context_and_return_flow(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    for name in [
        "PROJECT_CONTEXT.md",
        "MEMORY.md",
        "ROUTE_SPEC.yaml",
        "HARD_GATES.md",
        "ARTIFACT_REQUIREMENTS.md",
        "FAILURE_TAXONOMY.md",
    ]:
        (source / name).write_text(f"{name}\n", encoding="utf-8")
    (source / ".env").write_text("not exported\n", encoding="utf-8")

    manifest = build_context_pack(
        ContextPackBuildRequest(
            package_id="ctx-cross-platform",
            route_id="route-cross-platform",
            source_dir=source,
            output_dir=tmp_path / "pack",
        )
    )

    assert ".env" not in {file.path for file in manifest.files}
    assert any(item.path == ".env" for item in manifest.omitted_files)
    assert normalize_archive_member_path(r"nested\ROUTE_SPEC.yaml").normalized_path == (
        "nested/ROUTE_SPEC.yaml"
    )


def test_cross_platform_unpack_validation_blocks_unsafe_members() -> None:
    report = validate_archive_members(
        [
            ArchiveMember(path=r"safe\PROJECT_CONTEXT.md"),
            ArchiveMember(path="../escape.md"),
            ArchiveMember(path=".ssh/config"),
            ArchiveMember(path="link", member_type="symlink", link_target="target"),
        ]
    )
    finding_ids = {finding.finding_id for finding in report.findings}

    assert "path-traversal" in finding_ids
    assert "dotfile-denylist" in finding_ids
    assert "symlink-blocked" in finding_ids
    assert "safe/PROJECT_CONTEXT.md" in report.safe_paths


def test_return_archive_validation_requires_checksums(tmp_path: Path) -> None:
    _write_required_return(tmp_path)
    (tmp_path / "FINAL_STATUS.json").write_text('{"tampered": true}\n', encoding="utf-8")

    report = validate_return_archive_directory(tmp_path)

    assert "checksum-mismatch" in {finding.finding_id for finding in report.findings}
    assert report.release_blocker is True


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
