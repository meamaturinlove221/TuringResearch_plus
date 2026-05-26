"""Schema models for reusable research project templates."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.project_template.research_types import ResearchProjectType


class ResearchTemplateSection(BaseModel):
    """One required generated section."""

    model_config = ConfigDict(extra="forbid")

    relative_path: str = Field(min_length=1)
    title: str = Field(min_length=1)
    role: str = Field(min_length=1)
    required: bool = True


class ResearchProjectTemplate(BaseModel):
    """Reusable research project template definition."""

    model_config = ConfigDict(extra="forbid")

    template_id: ResearchProjectType
    display_name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    recommended_for: list[str] = Field(default_factory=list)
    sections: list[ResearchTemplateSection] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def template_requires_review_and_sections(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("research project templates require human review")
        paths = [section.relative_path for section in self.sections]
        if len(paths) != len(set(paths)):
            raise ValueError("template section paths must be unique")
        if "README.md" not in paths:
            raise ValueError("template must include README.md")
        return self


class ResearchProjectTemplateRequest(BaseModel):
    """Input for generating a typed reusable research project template."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    output_dir: Path
    template_type: ResearchProjectType = ResearchProjectType.MIXED_RESEARCH_PROJECT
    north_star: str = Field(default="Define the research north star.", min_length=1)
    research_questions: list[str] = Field(default_factory=list)
    owner: str = Field(default="researcher", min_length=1)
    overwrite: bool = False

    @model_validator(mode="after")
    def project_id_is_path_safe(self) -> Self:
        if any(part in self.project_id for part in ["..", "/", "\\", ":"]):
            raise ValueError("project_id must be a simple path-safe slug")
        return self


class GeneratedResearchProjectFile(BaseModel):
    """One generated file in a typed template result."""

    model_config = ConfigDict(extra="forbid")

    relative_path: str = Field(min_length=1)
    role: str = Field(min_length=1)
    generated: bool = True
    overwrite: bool = False


class ResearchProjectTemplateManifest(BaseModel):
    """Result manifest for typed reusable research project generation."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    template_type: ResearchProjectType
    output_dir: str = Field(min_length=1)
    generated_files: list[GeneratedResearchProjectFile] = Field(default_factory=list)
    created_directories: list[str] = Field(default_factory=list)
    omitted_items: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    network_used: bool = False
    read_private_vggt: bool = False
    observed_evidence_generated: bool = False

    @model_validator(mode="after")
    def manifest_preserves_template_boundaries(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("generated research project templates require human review")
        if self.network_used:
            raise ValueError("template generation must not use network")
        if self.read_private_vggt:
            raise ValueError("template generation must not read private VGGT paths")
        if self.observed_evidence_generated:
            raise ValueError("templates must not generate observed evidence")
        return self
