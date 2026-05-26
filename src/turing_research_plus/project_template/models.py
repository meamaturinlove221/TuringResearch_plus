"""Models for research project template generation."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProjectTemplateFile(BaseModel):
    """One generated project template file."""

    model_config = ConfigDict(extra="forbid")

    relative_path: str = Field(min_length=1)
    role: str = Field(min_length=1)
    generated: bool = True
    overwrite: bool = False


class ProjectTemplateRequest(BaseModel):
    """Input for generating a new research project skeleton."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    output_dir: Path
    north_star: str = Field(default="Define the research north star.", min_length=1)
    owner: str = Field(default="researcher", min_length=1)
    overwrite: bool = False

    @model_validator(mode="after")
    def project_id_is_path_safe(self) -> Self:
        if any(part in self.project_id for part in ["..", "/", "\\", ":"]):
            raise ValueError("project_id must be a simple path-safe slug")
        return self


class ProjectTemplateResult(BaseModel):
    """Result of a local project template generation run."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    output_dir: str = Field(min_length=1)
    generated_files: list[ProjectTemplateFile] = Field(default_factory=list)
    created_directories: list[str] = Field(default_factory=list)
    omitted_items: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    read_private_vggt: bool = False
    network_used: bool = False

    @model_validator(mode="after")
    def template_result_preserves_boundaries(self) -> Self:
        if self.read_private_vggt:
            raise ValueError("project template generator must not read private VGGT paths")
        if self.network_used:
            raise ValueError("project template generator must not use network")
        if not self.requires_human_review:
            raise ValueError("generated project templates require human review")
        return self
