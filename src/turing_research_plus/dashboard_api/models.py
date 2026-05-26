"""Models for the read-only dashboard data API."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DashboardProjectSummary(BaseModel):
    """Project overview for dashboard rendering."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: str = Field(min_length=1)
    topic: str = Field(default="", min_length=1)
    north_star: str = Field(default="", min_length=1)
    demo_only: bool = True
    read_only: bool = True
    requires_human_review: bool = True


class DashboardEvidenceEntry(BaseModel):
    """One evidence entry for dashboard summaries."""

    model_config = ConfigDict(extra="forbid")

    evidence_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    claim: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    notes: str = ""


class DashboardEvidenceSummary(BaseModel):
    """Evidence summary for dashboard rendering."""

    model_config = ConfigDict(extra="forbid")

    ledger_id: str = Field(min_length=1)
    status: str = Field(min_length=1)
    entries: list[DashboardEvidenceEntry] = Field(default_factory=list)
    status_counts: dict[str, int] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)
    read_only: bool = True
    no_observed_fake_result: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def fake_demo_must_not_be_observed(self) -> Self:
        if any(entry.status == "observed" for entry in self.entries):
            raise ValueError("dashboard data API must not promote fake/demo evidence to observed")
        if not self.read_only or not self.no_observed_fake_result:
            raise ValueError("dashboard evidence summary must remain read-only and fake-safe")
        return self


class DashboardArtifactRecord(BaseModel):
    """One artifact table row."""

    model_config = ConfigDict(extra="forbid")

    artifact: str = Field(min_length=1)
    status: str = Field(min_length=1)
    size: str = ""
    safety: str = ""
    notes: str = ""


class DashboardArtifactSummary(BaseModel):
    """Artifact summary for dashboard rendering."""

    model_config = ConfigDict(extra="forbid")

    title: str = "Artifact Summary"
    records: list[DashboardArtifactRecord] = Field(default_factory=list)
    selected_count: int = 0
    omitted_count: int = 0
    missing_count: int = 0
    read_only: bool = True
    no_raw_data: bool = True
    no_private_path: bool = True
    requires_human_review: bool = True


class DashboardPaperSummary(BaseModel):
    """Paper and advisor summary for dashboard rendering."""

    model_config = ConfigDict(extra="forbid")

    title: str = "Paper Summary"
    method_notes: list[str] = Field(default_factory=list)
    related_work_groups: list[str] = Field(default_factory=list)
    safe_claims: list[str] = Field(default_factory=list)
    unsafe_claims: list[str] = Field(default_factory=list)
    advisor_next_actions: list[str] = Field(default_factory=list)
    read_only: bool = True
    requires_human_review: bool = True


class DashboardDataBundle(BaseModel):
    """Unified read-only dashboard data bundle."""

    model_config = ConfigDict(extra="forbid")

    bundle_id: str = Field(min_length=1)
    project: DashboardProjectSummary
    evidence: DashboardEvidenceSummary
    artifacts: DashboardArtifactSummary
    paper: DashboardPaperSummary
    source_paths: list[str] = Field(default_factory=list)
    supports_json_export: bool = True
    supports_dashboard_rendering: bool = True
    read_only: bool = True
    no_secrets: bool = True
    no_raw_data: bool = True
    no_private_path: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def dashboard_bundle_must_be_safe(self) -> Self:
        if not all(
            [
                self.supports_json_export,
                self.supports_dashboard_rendering,
                self.read_only,
                self.no_secrets,
                self.no_raw_data,
                self.no_private_path,
                self.requires_human_review,
            ]
        ):
            raise ValueError("dashboard data bundle safety boundary was violated")
        return self
