"""Figure asset registry for TuringResearch Plus paper outputs."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FigureAssetKind(StrEnum):
    """Supported paper asset kinds."""

    MERMAID = "mermaid"
    SVG = "svg"
    PNG = "png"
    CSV_TABLE = "csv_table"
    PDF_EXTRACTED_FIGURE = "pdf_extracted_figure"
    PDF_EXTRACTED_TABLE = "pdf_extracted_table"
    EXPERIMENT_RESULT_JSON = "experiment_result_json"
    ARCHITECTURE_DOC = "architecture_doc"
    SOP_GRAPH = "sop_graph"


class FigureAssetStatus(StrEnum):
    """Figure asset readiness status."""

    REGISTERED = "registered"
    READY = "ready"
    BLOCKED = "blocked"


class FigureAsset(BaseModel):
    """One figure, table, or paper asset tracked for paper use."""

    model_config = ConfigDict(extra="forbid")

    figure_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_file: Path
    output_svg: Path | None = None
    output_png: Path | None = None
    caption: str | None = None
    used_in_blocks: list[str] = Field(default_factory=list)
    status: FigureAssetStatus = FigureAssetStatus.REGISTERED
    asset_kind: FigureAssetKind = FigureAssetKind.PNG
    original_pdf_source: Path | None = None

    @model_validator(mode="after")
    def validate_asset(self) -> Self:
        if not self.used_in_blocks:
            object.__setattr__(self, "status", FigureAssetStatus.BLOCKED)
            return self
        if self.caption is None or not self.caption.strip():
            object.__setattr__(self, "status", FigureAssetStatus.BLOCKED)
            return self
        if self.asset_kind in {
            FigureAssetKind.PDF_EXTRACTED_FIGURE,
            FigureAssetKind.PDF_EXTRACTED_TABLE,
        } and self.original_pdf_source is None:
            msg = "PDF extracted assets must record original_pdf_source"
            raise ValueError(msg)
        object.__setattr__(self, "status", FigureAssetStatus.READY)
        return self


class FigureRegistryIssue(BaseModel):
    """One figure registry lint issue."""

    model_config = ConfigDict(extra="forbid")

    figure_id: str = Field(min_length=1)
    issue_type: str = Field(min_length=1)
    message: str = Field(min_length=1)


class FigureAssetRegistry(BaseModel):
    """Registry of all paper figure and table assets."""

    model_config = ConfigDict(extra="forbid")

    assets: list[FigureAsset] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_ids(self) -> Self:
        figure_ids = [asset.figure_id for asset in self.assets]
        if len(figure_ids) != len(set(figure_ids)):
            msg = "figure_id values must be unique"
            raise ValueError(msg)
        return self


class FigureRegisterInput(BaseModel):
    """Input for paper.figure_register."""

    model_config = ConfigDict(extra="forbid")

    figure_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_file: Path
    output_svg: Path | None = None
    output_png: Path | None = None
    caption: str | None = None
    used_in_blocks: list[str] = Field(default_factory=list)
    asset_kind: FigureAssetKind = FigureAssetKind.PNG
    original_pdf_source: Path | None = None


class FigureRegisterOutput(BaseModel):
    """Output for paper.figure_register."""

    model_config = ConfigDict(extra="forbid")

    asset: FigureAsset
    registry: FigureAssetRegistry
    issues: list[FigureRegistryIssue] = Field(default_factory=list)


def register_figure(
    input_data: FigureRegisterInput,
    registry: FigureAssetRegistry | None = None,
) -> FigureRegisterOutput:
    """Register one paper figure asset without performing conversion."""

    asset = FigureAsset(
        figure_id=input_data.figure_id,
        title=input_data.title,
        source_file=input_data.source_file,
        output_svg=input_data.output_svg or _stable_output(input_data.figure_id, "svg"),
        output_png=input_data.output_png or _stable_output(input_data.figure_id, "png"),
        caption=input_data.caption,
        used_in_blocks=input_data.used_in_blocks,
        asset_kind=input_data.asset_kind,
        original_pdf_source=input_data.original_pdf_source,
    )
    current_registry = registry or FigureAssetRegistry()
    updated_registry = FigureAssetRegistry(assets=[*current_registry.assets, asset])
    return FigureRegisterOutput(
        asset=asset,
        registry=updated_registry,
        issues=lint_figure_registry(updated_registry),
    )


def lint_figure_registry(registry: FigureAssetRegistry) -> list[FigureRegistryIssue]:
    """Detect orphan figures and missing captions."""

    issues: list[FigureRegistryIssue] = []
    for asset in registry.assets:
        if not asset.used_in_blocks:
            issues.append(
                FigureRegistryIssue(
                    figure_id=asset.figure_id,
                    issue_type="orphan_figure",
                    message="Figure must link to at least one ArticleBlock.",
                )
            )
        if asset.caption is None or not asset.caption.strip():
            issues.append(
                FigureRegistryIssue(
                    figure_id=asset.figure_id,
                    issue_type="caption_missing",
                    message="Every paper figure must have a caption.",
                )
            )
    return issues


def paper_figure_register(input_data: FigureRegisterInput) -> dict[str, object]:
    """Thin paper.figure_register wrapper."""

    return register_figure(input_data).model_dump(mode="json")


def _stable_output(figure_id: str, suffix: str) -> Path:
    safe_id = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in figure_id)
    return Path("paper") / "figures" / f"{safe_id}.{suffix}"
