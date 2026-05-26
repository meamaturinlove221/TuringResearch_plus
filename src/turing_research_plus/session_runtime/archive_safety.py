"""Runtime archive safety checks for local context pack builder."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.pod_lifecycle.transfer_policy import (
    transfer_warnings_for_path,
)

TEXT_CONTEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}
GENERATED_PACK_FILES = {"HANDOFF_MANIFEST.yaml", "SHA256SUMS.txt"}
DEFAULT_CONTEXT_PACK_ALLOWLIST = {
    "PROJECT_CONTEXT.md",
    "MEMORY.md",
    "ROUTE_SPEC.yaml",
    "HARD_GATES.md",
    "ARTIFACT_REQUIREMENTS.md",
    "FAILURE_TAXONOMY.md",
}
DEFAULT_CONTEXT_PACK_FILES = [
    "PROJECT_CONTEXT.md",
    "MEMORY.md",
    "ROUTE_SPEC.yaml",
    "HARD_GATES.md",
    "ARTIFACT_REQUIREMENTS.md",
    "FAILURE_TAXONOMY.md",
    "HANDOFF_MANIFEST.yaml",
    "SHA256SUMS.txt",
]


class ArchiveCandidateCheck(BaseModel):
    """Safety decision for one source file candidate."""

    model_config = ConfigDict(extra="forbid")

    source_path: str = Field(min_length=1)
    archive_path: str = Field(min_length=1)
    included: bool
    reasons: list[str] = Field(default_factory=list)
    file_size: int = 0


class ArchiveSafetyRuntimeReport(BaseModel):
    """Safety report for runtime context pack candidates."""

    model_config = ConfigDict(extra="forbid")

    checks: list[ArchiveCandidateCheck] = Field(default_factory=list)
    allow_hidden_dotfiles: bool = False
    allow_raw_data: bool = False
    dotfile_policy: str = "hidden dotfiles excluded unless explicitly allowlisted"
    path_policy: str = "relative POSIX paths only; no absolute paths or traversal"
    private_data_policy: str = (
        "secrets, raw data, private paths, model payloads, and huge npz are excluded"
    )

    @property
    def included_paths(self) -> list[str]:
        """Return paths selected for the package."""

        return [check.archive_path for check in self.checks if check.included]

    @property
    def excluded_paths(self) -> list[str]:
        """Return source paths excluded by safety policy."""

        return [check.source_path for check in self.checks if not check.included]

    @property
    def release_blocker(self) -> bool:
        """Context pack builder excludes unsafe files instead of blocking safe packages."""

        return False


def normalize_pack_entry(path: str | Path) -> str:
    """Normalize a context pack entry to relative POSIX form."""

    normalized = str(path).replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def is_safe_pack_entry(
    archive_path: str,
    *,
    file_size: int = 0,
    allow_hidden_dotfiles: bool = False,
    allow_raw_data: bool = False,
    allowlist: set[str] | None = None,
) -> ArchiveCandidateCheck:
    """Return a safety decision for one archive entry."""

    normalized = normalize_pack_entry(archive_path)
    path = Path(normalized)
    allowed = allowlist or DEFAULT_CONTEXT_PACK_ALLOWLIST
    reasons: list[str] = []

    if normalized not in allowed and normalized not in GENERATED_PACK_FILES:
        reasons.append("not-in-context-pack-allowlist")
    if path.suffix.lower() not in TEXT_CONTEXT_SUFFIXES and normalized not in GENERATED_PACK_FILES:
        reasons.append("non-text-context-file")
    if any(part.startswith(".") for part in path.parts) and not allow_hidden_dotfiles:
        reasons.append("hidden-dotfile-excluded")

    warnings = transfer_warnings_for_path(normalized, file_size=file_size)
    if allow_hidden_dotfiles:
        warnings = [
            warning
            for warning in warnings
            if warning not in {"forbidden-dotfile", "forbidden-env-file"}
        ]
    if allow_raw_data:
        warnings = [
            warning
            for warning in warnings
            if warning != "forbidden-private-or-raw-path"
        ]
    reasons.extend(warnings)

    return ArchiveCandidateCheck(
        source_path=normalized,
        archive_path=normalized,
        included=not reasons,
        reasons=list(dict.fromkeys(reasons)),
        file_size=file_size,
    )


def audit_context_pack_candidates(
    source_root: Path,
    *,
    allow_hidden_dotfiles: bool = False,
    allow_raw_data: bool = False,
    allowlist: set[str] | None = None,
) -> ArchiveSafetyRuntimeReport:
    """Audit direct files under source root for context pack inclusion."""

    checks: list[ArchiveCandidateCheck] = []
    for path in sorted(source_root.iterdir()) if source_root.exists() else []:
        if not path.is_file():
            continue
        archive_path = normalize_pack_entry(path.relative_to(source_root))
        check = is_safe_pack_entry(
            archive_path,
            file_size=path.stat().st_size,
            allow_hidden_dotfiles=allow_hidden_dotfiles,
            allow_raw_data=allow_raw_data,
            allowlist=allowlist,
        )
        checks.append(
            check.model_copy(
                update={
                    "source_path": path.as_posix(),
                    "archive_path": archive_path,
                }
            )
        )
    return ArchiveSafetyRuntimeReport(
        checks=checks,
        allow_hidden_dotfiles=allow_hidden_dotfiles,
        allow_raw_data=allow_raw_data,
    )
