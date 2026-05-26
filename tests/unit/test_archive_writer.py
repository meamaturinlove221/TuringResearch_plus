from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.archive_writer import (
    sha256_file,
    write_context_pack_files,
)


def test_sha256_file_computes_digest(tmp_path: Path) -> None:
    path = tmp_path / "file.txt"
    path.write_text("abc", encoding="utf-8")

    assert sha256_file(path) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_write_context_pack_files_copies_and_writes_checksum(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    project = source / "PROJECT_CONTEXT.md"
    project.write_text("project\n", encoding="utf-8")

    report = write_context_pack_files(
        output,
        {"PROJECT_CONTEXT.md": project},
        generated_text_files={"HANDOFF_MANIFEST.yaml": "package_id: ctx\n"},
    )

    assert (output / "PROJECT_CONTEXT.md").exists()
    assert (output / "HANDOFF_MANIFEST.yaml").exists()
    assert (output / "SHA256SUMS.txt").exists()
    assert report.remote_execution_allowed is False
    paths = {item.path for item in report.written_files}
    assert {"PROJECT_CONTEXT.md", "HANDOFF_MANIFEST.yaml", "SHA256SUMS.txt"} <= paths
    checksums = (output / "SHA256SUMS.txt").read_text(encoding="utf-8")
    assert "PROJECT_CONTEXT.md" in checksums
    assert "HANDOFF_MANIFEST.yaml" in checksums
