"""Write local context pack directories with checksum manifests."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class WrittenArchiveFile(BaseModel):
    """One file written to the local context pack output directory."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    sha256: str = Field(min_length=64, max_length=64)
    size_bytes: int = 0
    source_path: str | None = None
    generated: bool = False


class ArchiveWriteReport(BaseModel):
    """Report returned after writing a context pack directory."""

    model_config = ConfigDict(extra="forbid")

    output_dir: str = Field(min_length=1)
    written_files: list[WrittenArchiveFile] = Field(default_factory=list)
    archive_format: str = "directory"
    remote_execution_allowed: bool = False
    requires_human_review: bool = True


def write_context_pack_files(
    output_dir: Path,
    files: dict[str, Path],
    *,
    generated_text_files: dict[str, str] | None = None,
) -> ArchiveWriteReport:
    """Copy selected files and write generated files into output dir."""

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[WrittenArchiveFile] = []

    for relative_path, source_path in sorted(files.items()):
        target = output_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target)
        written.append(
            WrittenArchiveFile(
                path=relative_path,
                sha256=sha256_file(target),
                size_bytes=target.stat().st_size,
                source_path=source_path.as_posix(),
                generated=False,
            )
        )

    for relative_path, content in sorted((generated_text_files or {}).items()):
        target = output_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(
            WrittenArchiveFile(
                path=relative_path,
                sha256=sha256_file(target),
                size_bytes=target.stat().st_size,
                generated=True,
            )
        )

    sha_lines = [
        f"{item.sha256}  {item.path}"
        for item in sorted(written, key=lambda item: item.path)
        if item.path != "SHA256SUMS.txt"
    ]
    sha_path = output_dir / "SHA256SUMS.txt"
    sha_path.write_text("\n".join(sha_lines) + "\n", encoding="utf-8")
    checksum_item = WrittenArchiveFile(
        path="SHA256SUMS.txt",
        sha256=sha256_file(sha_path),
        size_bytes=sha_path.stat().st_size,
        generated=True,
    )
    written = [item for item in written if item.path != "SHA256SUMS.txt"]
    written.append(checksum_item)

    return ArchiveWriteReport(
        output_dir=output_dir.as_posix(),
        written_files=sorted(written, key=lambda item: item.path),
        remote_execution_allowed=False,
        requires_human_review=True,
    )


def sha256_file(path: Path) -> str:
    """Compute sha256 for one local file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
