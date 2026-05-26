"""Models for Git-based context handoff packages."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContextPackageFileName(StrEnum):
    """Required context package file names."""

    PROJECT_CONTEXT = "PROJECT_CONTEXT.md"
    MEMORY = "MEMORY.md"
    ROUTE_SPEC = "ROUTE_SPEC.yaml"
    HARD_GATES = "HARD_GATES.md"
    ARTIFACT_REQUIREMENTS = "ARTIFACT_REQUIREMENTS.md"
    FAILURE_TAXONOMY = "FAILURE_TAXONOMY.md"
    ADVISOR_INTENT = "ADVISOR_INTENT.md"
    HANDOFF_MANIFEST = "HANDOFF_MANIFEST.yaml"
    README = "README.md"


class StructuredOutputFileName(StrEnum):
    """Required structured output template file names."""

    RUN_STATUS = "RUN_STATUS.json"
    FINAL_STATUS = "FINAL_STATUS.json"
    ARTIFACT_INDEX = "ARTIFACT_INDEX.md"
    FAILURE_REPORT = "FAILURE_REPORT.md"
    PROPOSED_EVIDENCE_UPDATES = "PROPOSED_EVIDENCE_UPDATES.json"
    ADVISOR_SUMMARY_DRAFT = "ADVISOR_SUMMARY_DRAFT.md"
    SHA256SUMS = "SHA256SUMS.txt"


class ContextFile(BaseModel):
    """One context file emitted into a context package."""

    model_config = ConfigDict(extra="forbid")

    relative_path: str = Field(min_length=1)
    sha256: str = Field(min_length=64, max_length=64)
    source_ref: str | None = None
    generated: bool = True


class OmittedContextItem(BaseModel):
    """One item omitted by context handoff safety rules."""

    model_config = ConfigDict(extra="forbid")

    item: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    safety_warnings: list[str] = Field(default_factory=list)


class MemoryPolicy(BaseModel):
    """Memory policy for context handoff."""

    model_config = ConfigDict(extra="forbid")

    allowed_content: list[str] = Field(
        default_factory=lambda: [
            "project summary",
            "route summary",
            "evidence-backed status",
            "known blockers",
            "handoff-safe next actions",
        ]
    )
    forbidden_content: list[str] = Field(
        default_factory=lambda: [
            "API key",
            ".env",
            "raw data path with secret",
            "SMPL-X body model files",
            "private data",
            "unreviewed session transcript",
        ]
    )
    bidirectional_sync: bool = False
    source_of_truth: str = "Evidence Ledger, Artifact Audit, Run Ingest, and Handoff Manifest"
    review_required: bool = True

    @model_validator(mode="after")
    def memory_cannot_be_only_truth(self) -> Self:
        if "memory" == self.source_of_truth.strip().lower():
            raise ValueError("MEMORY.md cannot be the only source of truth")
        return self


class HandoffSafetyPolicy(BaseModel):
    """Safety policy for context package contents."""

    model_config = ConfigDict(extra="forbid")

    forbidden_patterns: list[str] = Field(
        default_factory=lambda: [
            ".env",
            "API_KEY",
            "TOKEN",
            "SECRET",
            "private_data",
            "raw_data",
            "SMPLX_",
            "SMPL-X",
        ]
    )
    large_file_policy: str = "manifest_and_sha256_only"
    allow_raw_data: bool = False
    allow_secrets: bool = False
    allow_body_model_files: bool = False


class GitTransportPolicy(BaseModel):
    """Git transport policy for handoff packages."""

    model_config = ConfigDict(extra="forbid")

    transport: str = "git"
    remote_execution_allowed: bool = False
    dotfile_policy: str = "exclude secret dotfiles; allow generated package files only"
    branch_or_bundle_ref: str | None = None
    allowed_files: list[str] = Field(
        default_factory=lambda: [item.value for item in ContextPackageFileName]
    )
    forbidden_files: list[str] = Field(default_factory=lambda: [".env", ".codex", "secrets"])


class ContextPackage(BaseModel):
    """Generated context package metadata."""

    model_config = ConfigDict(extra="forbid")

    package_id: str = Field(min_length=1)
    project_name: str = "TuringResearch Plus"
    route_id: str = Field(min_length=1)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    context_files: list[ContextFile] = Field(min_length=1)
    safety_warnings: list[str] = Field(default_factory=list)
    omitted_items: list[OmittedContextItem] = Field(default_factory=list)
    sha256_manifest: dict[str, str] = Field(default_factory=dict)
    memory_policy: MemoryPolicy = Field(default_factory=MemoryPolicy)
    safety_policy: HandoffSafetyPolicy = Field(default_factory=HandoffSafetyPolicy)
    git_transport_policy: GitTransportPolicy = Field(default_factory=GitTransportPolicy)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def context_package_is_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("context package requires human review")
        if self.git_transport_policy.remote_execution_allowed:
            raise ValueError("Git handoff transport cannot allow remote execution")
        return self

    def to_markdown(self) -> str:
        """Render package metadata to Markdown."""

        lines = [
            f"# Context Package: {self.package_id}",
            "",
            f"- Project: {self.project_name}",
            f"- Route: `{self.route_id}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            "- Execution: not executed by TuringResearch",
            "",
            "## Context Files",
            "",
            *[f"- `{item.relative_path}` sha256 `{item.sha256}`" for item in self.context_files],
            "",
            "## Omitted Items",
            "",
        ]
        lines.extend(
            [f"- `{item.item}`: {item.reason}" for item in self.omitted_items]
            or ["- No omitted items recorded."]
        )
        lines.extend(["", "## Safety Warnings", ""])
        lines.extend([f"- {item}" for item in self.safety_warnings] or ["- None."])
        return "\n".join(lines) + "\n"


class ContextPackageBuildInput(BaseModel):
    """Input for building a context package."""

    model_config = ConfigDict(extra="forbid")

    package_id: str = Field(default="vggt-modal-sparseconv-context", min_length=1)
    project_name: str = "TuringResearch Plus"
    route_id: str = Field(default="modal_sparseconv_real_v0", min_length=1)
    output_dir: Path
    project_context: str = Field(min_length=1)
    memory_summary: str = Field(min_length=1)
    route_spec_text: str = Field(min_length=1)
    hard_gates_text: str = Field(min_length=1)
    artifact_requirements_text: str = Field(min_length=1)
    failure_taxonomy_text: str = Field(min_length=1)
    advisor_intent: str = Field(min_length=1)
    readme_text: str | None = None
    source_refs: dict[str, str] = Field(default_factory=dict)


class StructuredOutputTemplate(BaseModel):
    """Structured output template metadata."""

    model_config = ConfigDict(extra="forbid")

    template_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    output_files: list[str] = Field(
        default_factory=lambda: [item.value for item in StructuredOutputFileName]
    )
    sha256_manifest_file: str = StructuredOutputFileName.SHA256SUMS.value
    instructions: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    def to_markdown(self) -> str:
        """Render output template metadata to Markdown."""

        lines = [
            f"# Structured Output Template: {self.template_id}",
            "",
            f"- Route: `{self.route_id}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            "",
            "## Files",
            "",
            *[f"- `{item}`" for item in self.output_files],
            "",
            "## Instructions",
            "",
            *[f"- {item}" for item in self.instructions],
        ]
        return "\n".join(lines) + "\n"


def json_stub(run_id: str, route_id: str, **extra: Any) -> dict[str, Any]:
    """Build a deterministic JSON stub for output templates."""

    payload: dict[str, Any] = {
        "run_id": run_id,
        "route_id": route_id,
        "status": "planned",
        "execution_status": "not_executed_by_turingresearch",
        "requires_human_review": True,
    }
    payload.update(extra)
    return payload
