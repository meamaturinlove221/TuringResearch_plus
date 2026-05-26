"""Models for local-first research vault UI."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.vault_graph.models import VaultGraphNodeType


class VaultUIStatus(StrEnum):
    """Static vault UI status labels."""

    READY = "ready"
    PARTIAL = "partial"
    MISSING = "missing"
    REQUIRES_REVIEW = "requires-review"


class VaultUISection(BaseModel):
    """One section of a static vault UI."""

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: VaultUIStatus = VaultUIStatus.REQUIRES_REVIEW
    node_types: list[VaultGraphNodeType] = Field(default_factory=list)
    markdown: str = Field(default="", min_length=1)


class VaultSearchEntry(BaseModel):
    """One static search index entry for the vault UI."""

    model_config = ConfigDict(extra="forbid")

    entry_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    node_type: VaultGraphNodeType
    text: str = Field(min_length=1)
    href: str = Field(min_length=1)
    requires_human_review: bool = True


class VaultUISafetyReport(BaseModel):
    """Safety report for a generated static vault UI."""

    model_config = ConfigDict(extra="forbid")

    no_server: bool = True
    no_login: bool = True
    no_network: bool = True
    no_graph_database: bool = True
    graph_not_truth: bool = True
    no_private_path_read: bool = True
    requires_human_review: bool = True
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def safety_boundary_is_preserved(self) -> Self:
        if not all(
            [
                self.no_server,
                self.no_login,
                self.no_network,
                self.no_graph_database,
                self.graph_not_truth,
                self.no_private_path_read,
                self.requires_human_review,
            ]
        ):
            raise ValueError("vault UI must remain local/static/review-only")
        return self


class ResearchVaultUIBundle(BaseModel):
    """A generated local-first research vault UI bundle."""

    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    graph_id: str = Field(min_length=1)
    sections: list[VaultUISection] = Field(default_factory=list)
    search_index: list[VaultSearchEntry] = Field(default_factory=list)
    missing_edges: list[str] = Field(default_factory=list)
    requires_review_nodes: list[str] = Field(default_factory=list)
    generated_files: list[str] = Field(default_factory=list)
    safety_report: VaultUISafetyReport = Field(default_factory=VaultUISafetyReport)
    wikilinks_optional: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def bundle_requires_review_and_sections(self) -> Self:
        if not self.sections:
            raise ValueError("vault UI bundle requires at least one section")
        if not self.requires_human_review:
            raise ValueError("vault UI bundle requires human review")
        return self
