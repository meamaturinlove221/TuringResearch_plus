"""Models for the static docs site builder."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DocsSiteNavItem(BaseModel):
    """One static docs navigation item."""

    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    page: str = Field(min_length=1)
    source_docs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def page_must_be_markdown(self) -> Self:
        if not self.page.endswith(".md"):
            raise ValueError("docs site nav page must be markdown")
        return self


class DocsSiteNav(BaseModel):
    """Parsed docs-site navigation."""

    model_config = ConfigDict(extra="forbid")

    site_title: str = Field(min_length=1)
    status: str = Field(min_length=1)
    items: list[DocsSiteNavItem] = Field(min_length=1)

    @model_validator(mode="after")
    def item_ids_must_be_unique(self) -> Self:
        item_ids = [item.item_id for item in self.items]
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("docs site nav item ids must be unique")
        return self


class DocsSiteManifest(BaseModel):
    """Parsed docs-site manifest."""

    model_config = ConfigDict(extra="forbid")

    site_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    source_of_truth: str = Field(min_length=1)
    local_first: bool = True
    deployment: str = "none"
    cloud_dependency: bool = False
    large_frontend_framework: bool = False
    private_data_required: bool = False
    fake_links_allowed: bool = False
    required_sections: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def safety_boundary_must_hold(self) -> Self:
        if not self.local_first:
            raise ValueError("docs site must be local-first")
        if self.cloud_dependency or self.large_frontend_framework or self.private_data_required:
            raise ValueError("docs site must not require cloud, large frontend, or private data")
        if self.fake_links_allowed:
            raise ValueError("docs site must not allow fake links")
        return self


class DocsSiteBuildRequest(BaseModel):
    """Input for a static docs site build."""

    model_config = ConfigDict(extra="forbid")

    repo_root: Path
    docs_site_root: Path
    output_root: Path
    nav_path: Path
    manifest_path: Path
    copy_assets: bool = True


class DocsSiteBuildResult(BaseModel):
    """Result from a static docs site build."""

    model_config = ConfigDict(extra="forbid")

    site_id: str = Field(min_length=1)
    output_root: Path
    generated_files: list[Path] = Field(default_factory=list)
    copied_assets: list[Path] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def generated_site_requires_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("docs site build requires human review")
        return self
