"""Session registry models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SessionInfo(BaseModel):
    """A locally registered research session."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    created_at: datetime | None = None
    metadata: dict[str, str] = Field(default_factory=dict)


class SessionListResult(BaseModel):
    """Result for local session listing."""

    model_config = ConfigDict(extra="forbid")

    sessions: list[SessionInfo] = Field(default_factory=list)
