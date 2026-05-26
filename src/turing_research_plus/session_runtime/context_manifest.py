"""Manifest models for generated local context packs."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.session_runtime.archive_safety import (
    DEFAULT_CONTEXT_PACK_FILES,
    ArchiveSafetyRuntimeReport,
)


class ContextPackBuildStatus(StrEnum):
    """Status for a generated context pack."""

    BUILT = "built"
    BUILT_WITH_EXCLUSIONS = "built-with-exclusions"
    BLOCKED = "blocked"


class ContextPackManifestFile(BaseModel):
    """One file included in the generated context pack."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    sha256: str = Field(min_length=64, max_length=64)
    role: str = Field(min_length=1)
    required: bool = True
    generated: bool = False
    source_path: str | None = None
    size_bytes: int = 0


class ContextPackOmittedFile(BaseModel):
    """One file omitted by runtime safety rules."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    reasons: list[str] = Field(default_factory=list)


class ContextPackManifest(BaseModel):
    """Review-only manifest for a generated context pack."""

    model_config = ConfigDict(extra="forbid")

    package_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    project_name: str = "TuringResearch Plus"
    status: ContextPackBuildStatus
    output_dir: str = Field(min_length=1)
    files: list[ContextPackManifestFile] = Field(default_factory=list)
    omitted_files: list[ContextPackOmittedFile] = Field(default_factory=list)
    required_files: list[str] = Field(default_factory=lambda: list(DEFAULT_CONTEXT_PACK_FILES))
    archive_safety: ArchiveSafetyRuntimeReport = Field(
        default_factory=ArchiveSafetyRuntimeReport
    )
    remote_execution_allowed: bool = False
    live_network_allowed: bool = False
    contains_secrets: bool = False
    contains_raw_data: bool = False
    contains_model_payloads: bool = False
    proposed_updates_only: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_safe_pack_boundary(self) -> Self:
        if self.remote_execution_allowed:
            raise ValueError("context pack cannot allow remote execution")
        if self.live_network_allowed:
            raise ValueError("context pack cannot allow live networking")
        if self.contains_secrets:
            raise ValueError("context pack cannot contain secrets")
        if self.contains_raw_data:
            raise ValueError("context pack cannot contain raw data")
        if self.contains_model_payloads:
            raise ValueError("context pack cannot contain model payloads")
        if not self.proposed_updates_only:
            raise ValueError("context pack must keep proposed updates only")
        if not self.requires_human_review:
            raise ValueError("context pack requires human review")
        return self

    @property
    def included_paths(self) -> list[str]:
        """Return included context pack paths."""

        return [item.path for item in self.files]

    @property
    def missing_required_files(self) -> list[str]:
        """Return required files not included in the pack."""

        present = set(self.included_paths)
        return [path for path in self.required_files if path not in present]

    @property
    def release_blocker(self) -> bool:
        """Return whether missing required generated files block the pack."""

        return bool(self.missing_required_files)


def role_for_context_file(path: str) -> str:
    """Return a stable role label for a context pack file."""

    if path in {"PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml"}:
        return "durable_context"
    if path in {
        "HARD_GATES.md",
        "ARTIFACT_REQUIREMENTS.md",
        "FAILURE_TAXONOMY.md",
    }:
        return "handoff_context"
    if path == "HANDOFF_MANIFEST.yaml":
        return "generated_manifest"
    if path == "SHA256SUMS.txt":
        return "checksum_manifest"
    return "supporting_context"


def render_handoff_manifest(manifest: ContextPackManifest) -> str:
    """Render the generated handoff manifest in a deterministic YAML-like format."""

    lines = [
        f"package_id: {manifest.package_id}",
        f"route_id: {manifest.route_id}",
        f"project_name: {manifest.project_name}",
        "status: planned",
        "execution_status: not_executed_by_turingresearch",
        "remote_execution_allowed: false",
        "live_network_allowed: false",
        "proposed_updates_only: true",
        "requires_human_review: true",
        "files:",
    ]
    for item in manifest.files:
        if item.path == "SHA256SUMS.txt":
            continue
        lines.extend(
            [
                f"  - path: {item.path}",
                f"    role: {item.role}",
                f"    sha256: {item.sha256}",
            ]
        )
    lines.append("omitted_files:")
    for omitted in manifest.omitted_files:
        reasons = ", ".join(omitted.reasons) if omitted.reasons else "unspecified"
        lines.extend([f"  - path: {omitted.path}", f"    reasons: {reasons}"])
    if not manifest.omitted_files:
        lines.append("  - none")
    return "\n".join(lines) + "\n"


def render_context_pack_manifest_markdown(manifest: ContextPackManifest) -> str:
    """Render a review-oriented manifest report."""

    lines = [
        f"# Context Pack Manifest: {manifest.package_id}",
        "",
        f"- Route: `{manifest.route_id}`",
        f"- Status: `{manifest.status}`",
        f"- Release blocker: `{str(manifest.release_blocker).lower()}`",
        "- Remote execution allowed: `false`",
        "- Live network allowed: `false`",
        "- Proposed updates only: `true`",
        "- Requires human review: `true`",
        "",
        "## Included Files",
        "",
    ]
    lines.extend(
        [
            f"- `{item.path}` `{item.role}` sha256 `{item.sha256}`"
            for item in manifest.files
        ]
        or ["- None."]
    )
    lines.extend(["", "## Omitted Files", ""])
    lines.extend(
        [
            f"- `{item.path}`: {', '.join(item.reasons) if item.reasons else 'unspecified'}"
            for item in manifest.omitted_files
        ]
        or ["- None."]
    )
    lines.extend(["", "## Missing Required Files", ""])
    lines.extend([f"- `{item}`" for item in manifest.missing_required_files] or ["- None."])
    return "\n".join(lines) + "\n"
