"""Provider-neutral cloud object artifact index models."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ObjectStoreProvider(StrEnum):
    """Provider-neutral object store provider labels."""

    S3 = "s3"
    R2 = "r2"
    OSS = "oss"
    GCS = "gcs"
    GENERIC = "generic"


class ObjectArtifactStatus(StrEnum):
    """Object artifact index statuses."""

    INDEXED = "indexed"
    SELECTED = "selected"
    OMITTED = "omitted"
    LARGE_METADATA_ONLY = "large-metadata-only"
    UNSAFE = "unsafe"
    ERROR = "error"


class ObjectArtifactRef(BaseModel):
    """One object-store artifact reference."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1)
    size: int = Field(default=0, ge=0)
    hash: str | None = Field(default=None, min_length=8)
    content_type: str | None = None
    status: ObjectArtifactStatus = ObjectArtifactStatus.INDEXED
    omitted_reason: str | None = None
    evidence_tags: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)


class ObjectArtifactIndexRequest(BaseModel):
    """Input for provider-neutral object artifact indexing."""

    model_config = ConfigDict(extra="forbid")

    provider: ObjectStoreProvider = ObjectStoreProvider.GENERIC
    bucket_or_container: str = Field(min_length=1)
    prefix: str = ""
    selected_patterns: list[str] = Field(default_factory=list)
    max_object_size_bytes: int = Field(default=2_000_000, ge=1)
    fake_mode: bool = True


class ObjectArtifactIndex(BaseModel):
    """Provider-neutral object artifact index."""

    model_config = ConfigDict(extra="forbid")

    provider: ObjectStoreProvider
    bucket_or_container: str = Field(min_length=1)
    prefix: str = ""
    objects: list[ObjectArtifactRef] = Field(default_factory=list)
    size: dict[str, int] = Field(default_factory=dict)
    hash: dict[str, str] = Field(default_factory=dict)
    content_type: dict[str, str] = Field(default_factory=dict)
    status: ObjectArtifactStatus = ObjectArtifactStatus.INDEXED
    omitted_reason: dict[str, str] = Field(default_factory=dict)
    evidence_tags: list[str] = Field(default_factory=list)
    proposed_imports: list[dict[str, object]] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    indexed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    requires_human_review: bool = True
    human_verified: bool = False
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def index_requires_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("object artifact indexes require human review")
        if self.human_verified:
            raise ValueError("object artifact indexes are indexed, not verified")
        return self

    def to_markdown(self) -> str:
        """Render a concise Markdown index."""

        lines = [
            f"# Object Artifact Index: {self.provider}/{self.bucket_or_container}",
            "",
            f"- Prefix: `{self.prefix}`",
            f"- Status: `{self.status}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            f"- Human verified: `{str(self.human_verified).lower()}`",
            "",
            "## Objects",
            "",
            *[
                f"- `{item.key}`: `{item.status}` ({item.size} bytes)"
                for item in self.objects
            ],
            "",
            "## Proposed Imports",
            "",
            *[f"- {item}" for item in self.proposed_imports],
            "",
        ]
        return "\n".join(lines)
