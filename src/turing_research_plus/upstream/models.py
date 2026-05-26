"""Models for public upstream watch baselines."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class ChangeCategory(StrEnum):
    """Change categories tracked by the upstream watch baseline."""

    NEW_REPO = "new_repo"
    REMOVED_REPO = "removed_repo"
    UNRESOLVED_REPO = "unresolved_repo"
    NEW_FILE = "new_file"
    REMOVED_FILE = "removed_file"
    CHANGED_FILE = "changed_file"
    RENAMED_PATH = "renamed_path"
    README_CHANGE = "readme_change"
    ENTRY_CHANGE = "entry_change"
    SKILL_CHANGE = "skill_change"
    MCP_TOOL_CHANGE = "mcp_tool_change"
    PACKAGE_RELEASE_CHANGE = "package_release_change"
    DOCS_CHANGE = "docs_change"
    TEST_CHANGE = "test_change"
    SOURCE_MODULE_CHANGE = "source_module_change"


class RepoTarget(BaseModel):
    """One configured public upstream repository target."""

    model_config = ConfigDict(extra="forbid")

    repository_full_name: str = Field(min_length=1)
    url: HttpUrl
    group: str = Field(min_length=1)
    required: bool = False
    notes: str = ""


class RepoBaseline(BaseModel):
    """Public metadata snapshot for one upstream repository."""

    model_config = ConfigDict(extra="forbid")

    repository_full_name: str = Field(min_length=1)
    url: HttpUrl
    default_branch: str = ""
    latest_commit_sha: str = ""
    latest_commit_message: str = ""
    latest_commit_time: str = ""
    root_files: list[str] = Field(default_factory=list)
    markdown_files: list[str] = Field(default_factory=list)
    skill_files: list[str] = Field(default_factory=list)
    docs_files: list[str] = Field(default_factory=list)
    package_files: list[str] = Field(default_factory=list)
    mcp_config_files: list[str] = Field(default_factory=list)
    src_files: list[str] = Field(default_factory=list)
    test_files: list[str] = Field(default_factory=list)
    file_hashes: dict[str, str] = Field(default_factory=dict)
    unresolved_reason: str | None = None

    @model_validator(mode="after")
    def require_unresolved_or_commit(self) -> RepoBaseline:
        if self.unresolved_reason is None and not self.latest_commit_sha:
            raise ValueError("resolved repository baseline requires latest_commit_sha")
        return self

    @property
    def resolved(self) -> bool:
        """Return whether the upstream repository was accessible."""

        return self.unresolved_reason is None


class UpstreamBaselineSet(BaseModel):
    """Baseline set for all configured public upstream targets."""

    model_config = ConfigDict(extra="forbid")

    baseline_id: str = Field(min_length=1)
    generated_at: str = Field(min_length=1)
    source: str = Field(default="public-github", min_length=1)
    repositories: list[RepoBaseline] = Field(default_factory=list)

    def by_repo(self) -> dict[str, RepoBaseline]:
        """Return baselines keyed by full repository name."""

        return {repo.repository_full_name: repo for repo in self.repositories}


class UpstreamChange(BaseModel):
    """One detected upstream baseline change."""

    model_config = ConfigDict(extra="forbid")

    repository_full_name: str = Field(min_length=1)
    category: ChangeCategory
    path: str | None = None
    summary: str = Field(min_length=1)


class UpstreamDiffReport(BaseModel):
    """Diff report between two upstream baselines."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    old_baseline_id: str | None = None
    new_baseline_id: str = Field(min_length=1)
    changes: list[UpstreamChange] = Field(default_factory=list)
    is_initial_baseline: bool = False
