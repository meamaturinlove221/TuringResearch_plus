"""Session context pack manifests for review-only pod handoff."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.pod_lifecycle.context_archive_safety import (
    ContextArchiveSafetyReport,
    validate_context_archive_entries,
)
from turing_research_plus.pod_lifecycle.models import PodContextLifecycle

REQUIRED_CONTEXT_FILES = [
    "PROJECT_CONTEXT.md",
    "MEMORY.md",
    "ROUTE_SPEC.yaml",
]
OPTIONAL_CONTEXT_FILES = [
    "HARD_GATES.md",
    "ARTIFACT_REQUIREMENTS.md",
    "FAILURE_TAXONOMY.md",
    "ADVISOR_INTENT.md",
    "HANDOFF_MANIFEST.yaml",
    "README.md",
]


class SessionContextPackFile(BaseModel):
    """One file in a session context pack."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    role: str = Field(min_length=1)
    required: bool = False
    sha256: str | None = None
    omitted: bool = False
    omitted_reason: str | None = None


class SessionContextPackManifest(BaseModel):
    """Review-only manifest for a session context pack."""

    model_config = ConfigDict(extra="forbid")

    context_package_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    source_machine_label: str = Field(min_length=1)
    target_environment_label: str = Field(min_length=1)
    files: list[SessionContextPackFile] = Field(default_factory=list)
    memory_bidirectional_sync: bool = False
    proposed_updates_only: bool = True
    requires_human_review: bool = True
    remote_execution_allowed: bool = False
    automatic_git_push_allowed: bool = False
    archive_safety: ContextArchiveSafetyReport = Field(
        default_factory=ContextArchiveSafetyReport
    )

    @model_validator(mode="after")
    def enforce_review_only_pack(self) -> Self:
        if self.memory_bidirectional_sync:
            raise ValueError("session context pack cannot enable bidirectional sync")
        if not self.proposed_updates_only:
            raise ValueError("session context pack must keep updates proposed-only")
        if not self.requires_human_review:
            raise ValueError("session context pack requires human review")
        if self.remote_execution_allowed:
            raise ValueError("session context pack cannot enable remote execution")
        if self.automatic_git_push_allowed:
            raise ValueError("session context pack cannot enable automatic git push")
        return self

    @property
    def missing_required_files(self) -> list[str]:
        """Return required context files missing from the manifest."""

        present = {item.path for item in self.files if not item.omitted}
        return [path for path in REQUIRED_CONTEXT_FILES if path not in present]

    @property
    def release_blocker(self) -> bool:
        """Return whether the pack has release-blocking issues."""

        return bool(self.missing_required_files) or self.archive_safety.release_blocker


def build_session_context_pack_manifest(
    lifecycle: PodContextLifecycle,
    files: Iterable[str],
    *,
    hashes: dict[str, str] | None = None,
) -> SessionContextPackManifest:
    """Build a session context pack manifest from candidate relative file paths."""

    file_paths = list(files)
    archive_safety = validate_context_archive_entries(file_paths)
    hash_map = hashes or {}
    manifest_files = [
        SessionContextPackFile(
            path=path,
            role=_role_for_file(path),
            required=path in REQUIRED_CONTEXT_FILES,
            sha256=hash_map.get(path),
            omitted=path in archive_safety.blocked_paths,
            omitted_reason="blocked-by-archive-safety"
            if path in archive_safety.blocked_paths
            else None,
        )
        for path in file_paths
    ]

    return SessionContextPackManifest(
        context_package_id=lifecycle.context_package_id,
        route_id=lifecycle.route_id,
        source_machine_label=lifecycle.source_machine_label,
        target_environment_label=lifecycle.target_environment_label,
        files=manifest_files,
        archive_safety=archive_safety,
    )


def render_session_context_pack_manifest(manifest: SessionContextPackManifest) -> str:
    """Render a deterministic YAML-like manifest."""

    lines = [
        f"context_package_id: {manifest.context_package_id}",
        f"route_id: {manifest.route_id}",
        f"source_machine_label: {manifest.source_machine_label}",
        f"target_environment_label: {manifest.target_environment_label}",
        f"memory_bidirectional_sync: {str(manifest.memory_bidirectional_sync).lower()}",
        f"proposed_updates_only: {str(manifest.proposed_updates_only).lower()}",
        f"requires_human_review: {str(manifest.requires_human_review).lower()}",
        f"release_blocker: {str(manifest.release_blocker).lower()}",
        "files:",
    ]
    for item in manifest.files:
        lines.extend(
            [
                f"  - path: {item.path}",
                f"    role: {item.role}",
                f"    required: {str(item.required).lower()}",
                f"    omitted: {str(item.omitted).lower()}",
            ]
        )
        if item.sha256:
            lines.append(f"    sha256: {item.sha256}")
        if item.omitted_reason:
            lines.append(f"    omitted_reason: {item.omitted_reason}")
    lines.extend(
        [
            "archive_safety:",
            f"  release_blocker: {str(manifest.archive_safety.release_blocker).lower()}",
            "  blocked_paths:",
        ]
    )
    lines.extend(
        [f"    - {path}" for path in manifest.archive_safety.blocked_paths] or ["    - none"]
    )
    return "\n".join(lines) + "\n"


def _role_for_file(path: str) -> str:
    if path in REQUIRED_CONTEXT_FILES:
        return "durable_context"
    if path in OPTIONAL_CONTEXT_FILES:
        return "handoff_context"
    return "supporting_context"
