"""Models for privacy and data policy scanning."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SafetyLevel(StrEnum):
    """Research data safety levels."""

    PUBLIC_DEMO = "public-demo"
    INTERNAL_RESEARCH = "internal-research"
    PRIVATE_RESEARCH = "private-research"
    RESTRICTED_DATA = "restricted-data"
    SECRET_FORBIDDEN = "secret-forbidden"


class PrivacySeverity(StrEnum):
    """Finding severity."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PrivacyFindingType(StrEnum):
    """Supported privacy finding types."""

    ENV_FILE = "env_file"
    API_KEY_PATTERN = "api_key_pattern"
    TOKEN_PATTERN = "token_pattern"
    PRIVATE_DATA_PATH = "private_data_path"
    LOCAL_PROJECT_LINKS = "local_project_links"
    RAW_DATA = "raw_data"
    SMPLX_MODEL_FILE = "smplx_model_file"
    HUGE_NPZ = "huge_npz"
    PERSONAL_PATH = "personal_path"
    PRIVATE_ADVISOR_FEEDBACK = "private_advisor_feedback"
    LICENSED_MODEL_FILE = "licensed_model_file"


class PrivacyPolicyRule(BaseModel):
    """One scanner rule."""

    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1)
    finding_type: PrivacyFindingType
    description: str = Field(min_length=1)
    safety_level: SafetyLevel
    severity: PrivacySeverity
    recommended_action: str = Field(min_length=1)
    redaction_possible: bool = False
    release_blocker: bool = False
    path_patterns: list[str] = Field(default_factory=list)
    content_patterns: list[str] = Field(default_factory=list)
    max_size_bytes: int | None = Field(default=None, gt=0)


class RedactionProposal(BaseModel):
    """A non-destructive proposed redaction."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    finding_type: PrivacyFindingType
    replacement: str = Field(default="[REDACTED]", min_length=1)
    proposed_text: str | None = None
    destructive: bool = False

    @model_validator(mode="after")
    def redaction_is_non_destructive(self) -> Self:
        if self.destructive:
            raise ValueError("redaction proposals must be non-destructive")
        return self


class PrivacyFinding(BaseModel):
    """One privacy scan finding."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    finding_type: PrivacyFindingType
    safety_level: SafetyLevel
    severity: PrivacySeverity
    matched_rule: str = Field(min_length=1)
    message: str = Field(min_length=1)
    recommended_action: str = Field(min_length=1)
    redaction_possible: bool = False
    release_blocker: bool = False
    line_number: int | None = Field(default=None, ge=1)
    proposed_redaction: RedactionProposal | None = None


class PrivacyScanReport(BaseModel):
    """Report emitted by privacy and data policy scans."""

    model_config = ConfigDict(extra="forbid")

    scanned_paths: list[str] = Field(default_factory=list)
    findings: list[PrivacyFinding] = Field(default_factory=list)
    severity: PrivacySeverity = PrivacySeverity.INFO
    recommended_action: str = "No findings."
    redaction_possible: bool = False
    release_blocker: bool = False
    requires_human_review: bool = True
    proposed_redactions: list[RedactionProposal] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def report_requires_review_and_summarizes(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("privacy scan reports require human review")
        self.severity = _max_severity([finding.severity for finding in self.findings])
        self.redaction_possible = any(finding.redaction_possible for finding in self.findings)
        self.release_blocker = any(finding.release_blocker for finding in self.findings)
        self.proposed_redactions = [
            finding.proposed_redaction
            for finding in self.findings
            if finding.proposed_redaction is not None
        ]
        if self.release_blocker:
            self.recommended_action = "Block release until findings are removed or reviewed."
        elif self.findings:
            self.recommended_action = "Review findings before export or release."
        return self


def _max_severity(severities: list[PrivacySeverity]) -> PrivacySeverity:
    if not severities:
        return PrivacySeverity.INFO
    order = {
        PrivacySeverity.INFO: 0,
        PrivacySeverity.LOW: 1,
        PrivacySeverity.MEDIUM: 2,
        PrivacySeverity.HIGH: 3,
        PrivacySeverity.CRITICAL: 4,
    }
    return max(severities, key=lambda item: order[item])


def path_to_scan_label(path: Path) -> str:
    """Return a stable path label for reports."""

    return path.as_posix()
