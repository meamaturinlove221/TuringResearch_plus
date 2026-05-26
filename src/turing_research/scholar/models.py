"""Scholar content models."""

from pydantic import BaseModel, ConfigDict, Field

from tuling_research.errors import CoreError


class PaperContentRequest(BaseModel):
    """Request for locally cached paper Markdown."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)


class PaperContentResult(BaseModel):
    """Result for locally cached paper Markdown."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    found: bool
    markdown: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    error: CoreError | None = None
