"""Structured return manifests for pod lifecycle review."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.pod_lifecycle.models import PodContextLifecycle


class StructuredReturnFile(BaseModel):
    """One file declared in a structured pod return."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    role: str = Field(min_length=1)
    required: bool = True
    sha256: str | None = None
    status: str = "present"


class StructuredReturnManifest(BaseModel):
    """Review-only return manifest for pod output."""

    model_config = ConfigDict(extra="forbid")

    return_package_id: str = Field(min_length=1)
    context_package_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    target_environment_label: str = Field(min_length=1)
    files: list[StructuredReturnFile] = Field(default_factory=list)
    sha256_manifest: dict[str, str] = Field(default_factory=dict)
    proposed_evidence_updates_only: bool = True
    auto_apply_evidence_updates: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_review_only_return(self) -> Self:
        if not self.proposed_evidence_updates_only:
            raise ValueError("return manifest must keep evidence updates proposed-only")
        if self.auto_apply_evidence_updates:
            raise ValueError("return manifest cannot auto-apply evidence updates")
        if not self.requires_human_review:
            raise ValueError("return manifest requires human review")
        return self

    @property
    def missing_required_files(self) -> list[str]:
        """Return required files missing from the return manifest."""

        present = {item.path for item in self.files if item.status == "present"}
        required = {item.path for item in self.files if item.required}
        return sorted(required - present)

    def to_metadata(self) -> dict[str, object]:
        """Return metadata compatible with the existing return verifier."""

        return {
            "context_package_id": self.context_package_id,
            "route_id": self.route_id,
            "target_environment_label": self.target_environment_label,
            "return_package_id": self.return_package_id,
            "sha256_manifest": self.sha256_manifest,
        }


def build_structured_return_manifest(
    lifecycle: PodContextLifecycle,
    returned_files: Iterable[str],
    *,
    return_package_id: str,
    sha256_manifest: dict[str, str] | None = None,
) -> StructuredReturnManifest:
    """Build a structured return manifest from returned file paths."""

    returned = set(returned_files)
    hashes = sha256_manifest or {}
    files = [
        StructuredReturnFile(
            path=path,
            role=_return_role(path),
            required=True,
            sha256=hashes.get(path),
            status="present" if path in returned else "missing",
        )
        for path in lifecycle.return_verification.required_files
    ]
    extra_files = sorted(returned - set(lifecycle.return_verification.required_files))
    files.extend(
        StructuredReturnFile(
            path=path,
            role="extra_review_file",
            required=False,
            sha256=hashes.get(path),
            status="present",
        )
        for path in extra_files
    )
    return StructuredReturnManifest(
        return_package_id=return_package_id,
        context_package_id=lifecycle.context_package_id,
        route_id=lifecycle.route_id,
        target_environment_label=lifecycle.target_environment_label,
        files=files,
        sha256_manifest=hashes,
    )


def render_structured_return_manifest(manifest: StructuredReturnManifest) -> str:
    """Render a deterministic YAML-like return manifest."""

    lines = [
        f"return_package_id: {manifest.return_package_id}",
        f"context_package_id: {manifest.context_package_id}",
        f"route_id: {manifest.route_id}",
        f"target_environment_label: {manifest.target_environment_label}",
        f"proposed_evidence_updates_only: {str(manifest.proposed_evidence_updates_only).lower()}",
        f"auto_apply_evidence_updates: {str(manifest.auto_apply_evidence_updates).lower()}",
        f"requires_human_review: {str(manifest.requires_human_review).lower()}",
        "files:",
    ]
    for item in manifest.files:
        lines.extend(
            [
                f"  - path: {item.path}",
                f"    role: {item.role}",
                f"    required: {str(item.required).lower()}",
                f"    status: {item.status}",
            ]
        )
        if item.sha256:
            lines.append(f"    sha256: {item.sha256}")
    return "\n".join(lines) + "\n"


def _return_role(path: str) -> str:
    if path == "PROPOSED_EVIDENCE_UPDATES.json":
        return "proposed_evidence_updates"
    if path == "SHA256SUMS.txt":
        return "hash_manifest"
    if path.endswith(".json"):
        return "status_metadata"
    if path.endswith(".md"):
        return "review_markdown"
    if path.endswith(".yaml"):
        return "return_manifest"
    return "return_artifact"
