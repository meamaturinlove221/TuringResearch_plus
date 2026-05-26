"""Web content models."""

from pydantic import BaseModel, ConfigDict, Field

from turing_research.errors import CoreError


class WebContentRequest(BaseModel):
    """Request for locally cached web Markdown."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1)


class WebContentResult(BaseModel):
    """Result for locally cached web Markdown."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1)
    found: bool
    markdown: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    error: CoreError | None = None
