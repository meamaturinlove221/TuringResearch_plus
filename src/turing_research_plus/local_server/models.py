"""Models for the read-only local server dashboard."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LocalDashboardContentType(StrEnum):
    """Supported local dashboard response content types."""

    HTML = "text/html; charset=utf-8"
    JSON = "application/json; charset=utf-8"
    TEXT = "text/plain; charset=utf-8"


class LocalDashboardSafety(BaseModel):
    """Safety boundary for the local server dashboard."""

    model_config = ConfigDict(extra="forbid")

    localhost_only: bool = True
    read_only: bool = True
    login_required: bool = False
    public_network: bool = False
    uploads_data: bool = False
    default_networking: bool = False
    executes_commands: bool = False
    reads_private_vggt_path: bool = False
    displays_secrets: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_local_read_only_boundary(self) -> Self:
        if not self.localhost_only or not self.read_only:
            raise ValueError("local server dashboard must be localhost-only and read-only")
        if (
            self.login_required
            or self.public_network
            or self.uploads_data
            or self.default_networking
            or self.executes_commands
            or self.reads_private_vggt_path
            or self.displays_secrets
        ):
            raise ValueError("local server dashboard safety boundary was violated")
        if not self.requires_human_review:
            raise ValueError("local server dashboard requires human review")
        return self


class LocalDashboardRoute(BaseModel):
    """One read-only local dashboard route."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    source_path: Path | None = None
    content_type: LocalDashboardContentType = LocalDashboardContentType.HTML
    requires_human_review: bool = True

    @model_validator(mode="after")
    def route_path_must_be_absolute_http_path(self) -> Self:
        if not self.path.startswith("/"):
            raise ValueError("local dashboard route path must start with /")
        if "\\" in self.path or ".." in self.path:
            raise ValueError("local dashboard route path must be normalized")
        return self


class LocalDashboardRequest(BaseModel):
    """Request configuration for the local dashboard server."""

    model_config = ConfigDict(extra="forbid")

    repo_root: Path
    public_demo_dir: Path
    host: str = "127.0.0.1"
    port: int = Field(default=8765, ge=0, le=65535)
    safety: LocalDashboardSafety = Field(default_factory=LocalDashboardSafety)

    @model_validator(mode="after")
    def host_must_be_localhost(self) -> Self:
        if self.host not in {"127.0.0.1", "localhost"}:
            raise ValueError("local dashboard server must bind localhost only")
        return self


class LocalDashboardResponse(BaseModel):
    """One generated local dashboard response."""

    model_config = ConfigDict(extra="forbid")

    status_code: int = Field(ge=100, le=599)
    content_type: LocalDashboardContentType
    body: str
    route_path: str = Field(min_length=1)
    served_from: str | None = None
