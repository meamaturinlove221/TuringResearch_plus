"""Build safe local context packs for session runtime parity."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.session_runtime.archive_safety import (
    DEFAULT_CONTEXT_PACK_ALLOWLIST,
    audit_context_pack_candidates,
)
from turing_research_plus.session_runtime.archive_writer import write_context_pack_files
from turing_research_plus.session_runtime.context_manifest import (
    ContextPackBuildStatus,
    ContextPackManifest,
    ContextPackManifestFile,
    ContextPackOmittedFile,
    render_context_pack_manifest_markdown,
    render_handoff_manifest,
    role_for_context_file,
)


class ContextPackBuildRequest(BaseModel):
    """Request for the local context pack builder."""

    model_config = ConfigDict(extra="forbid")

    package_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    source_dir: Path
    output_dir: Path
    project_name: str = "TuringResearch Plus"
    allow_hidden_dotfiles: bool = False
    allow_raw_data: bool = False
    allowlist: list[str] = Field(
        default_factory=lambda: sorted(DEFAULT_CONTEXT_PACK_ALLOWLIST)
    )
    remote_execution_enabled: bool = False
    live_network_enabled: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_safe_defaults(self) -> Self:
        if self.remote_execution_enabled:
            raise ValueError("context pack builder cannot enable remote execution")
        if self.live_network_enabled:
            raise ValueError("context pack builder cannot enable live networking")
        if not self.requires_human_review:
            raise ValueError("context pack builder requires human review")
        return self


def build_context_pack(request: ContextPackBuildRequest) -> ContextPackManifest:
    """Build a safe local context pack directory."""

    safety = audit_context_pack_candidates(
        request.source_dir,
        allow_hidden_dotfiles=request.allow_hidden_dotfiles,
        allow_raw_data=request.allow_raw_data,
        allowlist=set(request.allowlist),
    )
    selected_sources = {
        check.archive_path: Path(check.source_path)
        for check in safety.checks
        if check.included
    }
    omitted = [
        ContextPackOmittedFile(path=check.archive_path, reasons=check.reasons)
        for check in safety.checks
        if not check.included
    ]

    seed_manifest = ContextPackManifest(
        package_id=request.package_id,
        route_id=request.route_id,
        project_name=request.project_name,
        status=ContextPackBuildStatus.BUILT_WITH_EXCLUSIONS
        if omitted
        else ContextPackBuildStatus.BUILT,
        output_dir=request.output_dir.as_posix(),
        files=[],
        omitted_files=omitted,
        archive_safety=safety,
    )
    generated = {
        "HANDOFF_MANIFEST.yaml": render_handoff_manifest(seed_manifest),
    }
    write_report = write_context_pack_files(
        request.output_dir,
        selected_sources,
        generated_text_files=generated,
    )
    manifest = ContextPackManifest(
        package_id=request.package_id,
        route_id=request.route_id,
        project_name=request.project_name,
        status=ContextPackBuildStatus.BUILT_WITH_EXCLUSIONS
        if omitted
        else ContextPackBuildStatus.BUILT,
        output_dir=request.output_dir.as_posix(),
        files=[
            ContextPackManifestFile(
                path=item.path,
                sha256=item.sha256,
                role=role_for_context_file(item.path),
                required=True,
                generated=item.generated,
                source_path=item.source_path,
                size_bytes=item.size_bytes,
            )
            for item in write_report.written_files
        ],
        omitted_files=omitted,
        archive_safety=safety,
        remote_execution_allowed=False,
        live_network_allowed=False,
        proposed_updates_only=True,
        requires_human_review=True,
    )
    manifest_text = render_context_pack_manifest_markdown(manifest)
    (request.output_dir / "CONTEXT_PACK_MANIFEST.md").write_text(
        manifest_text,
        encoding="utf-8",
    )
    return manifest
