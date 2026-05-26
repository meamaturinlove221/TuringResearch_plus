"""Models for dataset and license compliance review."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ComplianceAssetType(StrEnum):
    """Asset categories covered by the compliance assistant."""

    DATASET = "dataset"
    MODEL = "model"
    PAPER = "paper"
    CODE_REPO = "code_repo"


class LicenseStatus(StrEnum):
    """Known license state for an asset."""

    KNOWN = "known"
    UNKNOWN = "unknown"
    RESTRICTED = "restricted"
    PROPRIETARY = "proprietary"
    REVIEW_REQUIRED = "review-required"


class ComplianceRiskLevel(StrEnum):
    """Conservative compliance risk levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKER = "blocker"


class ComplianceAsset(BaseModel):
    """One dataset, model, paper, or code asset to review."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    asset_type: ComplianceAssetType
    license_name: str = Field(default="unknown", min_length=1)
    license_status: LicenseStatus = LicenseStatus.UNKNOWN
    usage_restrictions: list[str] = Field(default_factory=list)
    source: str | None = None
    bundled: bool = False
    public_release_allowed: bool | None = None
    requires_human_review: bool = True

    @model_validator(mode="after")
    def restricted_assets_require_review(self) -> Self:
        if self.license_status in {
            LicenseStatus.UNKNOWN,
            LicenseStatus.RESTRICTED,
            LicenseStatus.PROPRIETARY,
            LicenseStatus.REVIEW_REQUIRED,
        } and not self.requires_human_review:
            raise ValueError("restricted or unknown assets require human review")
        return self


class ComplianceFinding(BaseModel):
    """One risk finding from the compliance checker."""

    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(min_length=1)
    asset_type: ComplianceAssetType
    risk_level: ComplianceRiskLevel
    message: str = Field(min_length=1)
    recommended_action: str = Field(min_length=1)
    release_blocker: bool = False
    requires_human_review: bool = True


class ComplianceReport(BaseModel):
    """Dataset / model / paper / code compliance report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    datasets: list[ComplianceAsset] = Field(default_factory=list)
    models: list[ComplianceAsset] = Field(default_factory=list)
    papers: list[ComplianceAsset] = Field(default_factory=list)
    code_repos: list[ComplianceAsset] = Field(default_factory=list)
    licenses: list[str] = Field(default_factory=list)
    usage_restrictions: list[str] = Field(default_factory=list)
    redistribution_risk: ComplianceRiskLevel = ComplianceRiskLevel.LOW
    publication_risk: ComplianceRiskLevel = ComplianceRiskLevel.LOW
    missing_license_info: list[str] = Field(default_factory=list)
    findings: list[ComplianceFinding] = Field(default_factory=list)
    disclaimer: str = Field(
        default="This compliance report is a research checklist and is not legal advice."
    )
    requires_human_review: bool = True

    @model_validator(mode="after")
    def report_must_not_claim_legal_advice(self) -> Self:
        if "not legal advice" not in self.disclaimer.lower():
            raise ValueError("compliance report must state that it is not legal advice")
        if not self.requires_human_review:
            raise ValueError("compliance report requires human review")
        return self
