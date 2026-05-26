"""Static export manifest for docs-site builds."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.docs_site.builder import build_docs_site_from_repo

ExportFileKind = Literal["html", "css", "asset", "manifest"]


class DocsSiteStaticExportFile(BaseModel):
    """One generated static docs-site export file."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    kind: ExportFileKind
    size_bytes: int = Field(ge=0)
    sha256: str = Field(min_length=64, max_length=64)


class DocsSiteStaticExportManifest(BaseModel):
    """Manifest for a local static docs-site export."""

    model_config = ConfigDict(extra="forbid")

    site_id: str = Field(min_length=1)
    output_root: Path
    files: list[DocsSiteStaticExportFile] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    deployment_performed: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def export_must_remain_reviewed_and_local(self) -> DocsSiteStaticExportManifest:
        if self.deployment_performed:
            raise ValueError("docs-site static export must not deploy")
        if not self.requires_human_review:
            raise ValueError("docs-site static export requires human review")
        return self


def export_static_docs_site(
    repo_root: Path,
    *,
    output_root: Path | None = None,
    write_manifest: bool = True,
) -> DocsSiteStaticExportManifest:
    """Build local static docs and write a deterministic export manifest."""

    output = output_root or repo_root / "docs-site" / "output"
    build_result = build_docs_site_from_repo(repo_root, output_root=output)
    files = [
        _file_entry(path, output)
        for path in [*build_result.generated_files, *build_result.copied_assets]
        if path.exists() and path.is_file()
    ]
    manifest = DocsSiteStaticExportManifest(
        site_id=build_result.site_id,
        output_root=output,
        files=files,
        warnings=build_result.warnings,
    )
    if write_manifest:
        manifest_path = output / "static_export_manifest.json"
        payload = manifest.model_dump(mode="json")
        manifest_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return manifest


def render_static_export_manifest_markdown(manifest: DocsSiteStaticExportManifest) -> str:
    """Render the static export manifest as Markdown."""

    lines = [
        "# Docs Site Static Export Manifest",
        "",
        f"Site ID: `{manifest.site_id}`",
        f"Deployment performed: `{str(manifest.deployment_performed).lower()}`",
        f"Requires human review: `{str(manifest.requires_human_review).lower()}`",
        "",
        "## Files",
        "",
    ]
    for file in manifest.files:
        lines.append(f"- `{file.path}` ({file.kind}, {file.size_bytes} bytes, `{file.sha256}`)")
    if not manifest.files:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    if manifest.warnings:
        lines.extend(f"- {warning}" for warning in manifest.warnings)
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def _file_entry(path: Path, output_root: Path) -> DocsSiteStaticExportFile:
    suffix = path.suffix.lower()
    if suffix == ".html":
        kind: ExportFileKind = "html"
    elif suffix == ".css":
        kind = "css"
    else:
        kind = "asset"
    return DocsSiteStaticExportFile(
        path=path.resolve().relative_to(output_root.resolve()).as_posix(),
        kind=kind,
        size_bytes=path.stat().st_size,
        sha256=_sha256(path),
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
