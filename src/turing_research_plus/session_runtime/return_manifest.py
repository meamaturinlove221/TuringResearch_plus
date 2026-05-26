"""Runtime structured return manifest loading."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

REQUIRED_RETURN_FILES = [
    "RUN_STATUS.json",
    "FINAL_STATUS.json",
    "ARTIFACT_INDEX.md",
    "FAILURE_REPORT.md",
    "PROPOSED_EVIDENCE_UPDATES.json",
    "SHA256SUMS.txt",
]


class ReturnFileRecord(BaseModel):
    """One file expected or found in a structured return directory."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    required: bool = True
    present: bool = False
    size_bytes: int = 0
    expected_sha256: str | None = Field(default=None, min_length=64, max_length=64)
    actual_sha256: str | None = Field(default=None, min_length=64, max_length=64)


class ReturnManifestRuntime(BaseModel):
    """Runtime manifest derived from a local return directory."""

    model_config = ConfigDict(extra="forbid")

    return_dir: str = Field(min_length=1)
    files: list[ReturnFileRecord] = Field(default_factory=list)
    sha256_manifest: dict[str, str] = Field(default_factory=dict)
    required_files: list[str] = Field(default_factory=lambda: list(REQUIRED_RETURN_FILES))

    @property
    def present_files(self) -> list[str]:
        """Return present file paths."""

        return [item.path for item in self.files if item.present]

    @property
    def missing_required_files(self) -> list[str]:
        """Return missing required return files."""

        present = set(self.present_files)
        return [path for path in self.required_files if path not in present]


def load_return_manifest(return_dir: Path) -> ReturnManifestRuntime:
    """Load a structured return directory without trusting its claims."""

    checksums = load_sha256sums(return_dir / "SHA256SUMS.txt")
    records = [
        ReturnFileRecord(
            path=path,
            required=True,
            present=(return_dir / path).is_file(),
            size_bytes=(return_dir / path).stat().st_size if (return_dir / path).is_file() else 0,
            expected_sha256=checksums.get(path),
        )
        for path in REQUIRED_RETURN_FILES
    ]
    extra_files = sorted(
        path.name
        for path in return_dir.iterdir()
        if path.is_file() and path.name not in REQUIRED_RETURN_FILES
    ) if return_dir.exists() else []
    records.extend(
        ReturnFileRecord(
            path=path,
            required=False,
            present=True,
            size_bytes=(return_dir / path).stat().st_size,
            expected_sha256=checksums.get(path),
        )
        for path in extra_files
    )
    return ReturnManifestRuntime(
        return_dir=return_dir.as_posix(),
        files=records,
        sha256_manifest=checksums,
    )


def load_sha256sums(path: Path) -> dict[str, str]:
    """Parse SHA256SUMS.txt lines as '<digest>  <path>'."""

    if not path.exists():
        return {}
    checksums: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split(maxsplit=1)
        if len(parts) != 2:
            continue
        digest, file_path = parts
        digest = digest.lstrip("\ufeff")
        checksums[file_path.strip()] = digest.strip()
    return checksums
