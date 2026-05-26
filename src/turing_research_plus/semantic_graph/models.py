"""Semantic graph models for TuringResearch Plus."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class GraphStatus(StrEnum):
    """Semantic graph operation status."""

    OK = "ok"
    ERROR = "error"


class GraphErrorCode(StrEnum):
    """Typed semantic graph errors."""

    ADAPTER_FAILURE = "adapter_failure"
    NOT_FOUND = "not_found"


class GraphError(BaseModel):
    """Typed semantic graph error."""

    model_config = ConfigDict(extra="forbid")

    code: GraphErrorCode
    message: str = Field(min_length=1)


class GraphDirection(StrEnum):
    """Citation graph expansion direction."""

    BACKWARD = "backward"
    FORWARD = "forward"
    BOTH = "both"


class PaperNode(BaseModel):
    """Paper node in the semantic graph."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    year: int | None = None
    citation_count: int = Field(default=0, ge=0)
    is_open_access: bool = False
    authors: list[str] = Field(default_factory=list)
    abstract: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuthorNode(BaseModel):
    """Author node in the semantic graph."""

    model_config = ConfigDict(extra="forbid")

    author_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    paper_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class CitationEdge(BaseModel):
    """Directed citation edge from source to target."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    relation: GraphDirection


class AuthorEdge(BaseModel):
    """Undirected co-author edge represented canonically."""

    model_config = ConfigDict(extra="forbid")

    source_author_id: str = Field(min_length=1)
    target_author_id: str = Field(min_length=1)
    shared_paper_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def canonicalize_author_pair(self) -> "AuthorEdge":
        if self.source_author_id > self.target_author_id:
            source = self.target_author_id
            target = self.source_author_id
            self.source_author_id = source
            self.target_author_id = target
        return self


class PaperLookupInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)


class PaperLookupOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GraphStatus
    paper: PaperNode | None = None
    error: GraphError | None = None


class PaperBatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paper_ids: list[str] = Field(min_length=1)


class PaperBatchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GraphStatus
    papers: list[PaperNode] = Field(default_factory=list)
    errors: list[GraphError] = Field(default_factory=list)


class PaperListInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    limit: int = Field(default=20, gt=0)


class PaperListOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GraphStatus
    papers: list[PaperNode] = Field(default_factory=list)
    error: GraphError | None = None


class RecommendationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paper_ids: list[str] = Field(min_length=1)
    limit: int = Field(default=10, gt=0)


class RecommendationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GraphStatus
    papers: list[PaperNode] = Field(default_factory=list)
    error: GraphError | None = None


class AuthorInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    author_id: str = Field(min_length=1)


class AuthorOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GraphStatus
    author: AuthorNode | None = None
    error: GraphError | None = None


class AuthorPapersOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GraphStatus
    papers: list[PaperNode] = Field(default_factory=list)
    error: GraphError | None = None


class CitationGraphExpandInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seed_paper_ids: list[str] = Field(min_length=1)
    direction: GraphDirection = GraphDirection.BOTH
    depth_limit: int = Field(default=1, ge=0)
    max_nodes: int = Field(default=50, gt=0)
    min_year: int | None = None
    max_year: int | None = None
    min_citation_count: int | None = Field(default=None, ge=0)
    open_access_only: bool = False
    recommendation_limit: int = Field(default=5, ge=0)


class CitationGraphOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GraphStatus
    nodes: list[PaperNode] = Field(default_factory=list)
    edges: list[CitationEdge] = Field(default_factory=list)
    frontier_nodes: list[PaperNode] = Field(default_factory=list)
    recommended_next_reads: list[PaperNode] = Field(default_factory=list)
    error: GraphError | None = None


class AuthorNetworkInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    seed_author_ids: list[str] = Field(min_length=1)
    max_depth: int = Field(default=1, ge=0)
    max_authors: int = Field(default=50, gt=0)


class AuthorNetworkOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: GraphStatus
    authors: list[AuthorNode] = Field(default_factory=list)
    edges: list[AuthorEdge] = Field(default_factory=list)
    frontier_authors: list[AuthorNode] = Field(default_factory=list)
    error: GraphError | None = None
