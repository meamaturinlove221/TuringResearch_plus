"""Models for Markdown-only advisor packs."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import EvidenceRef


class AdvisorReadinessStatus(StrEnum):
    """Readiness labels used in advisor-facing summaries."""

    READY_FOR_REVIEW = "ready-for-review"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"
    NOT_READY = "not-ready"
    BLOCKED = "blocked"


class AdvisorMissingEvidenceItem(BaseModel):
    """One missing evidence item that blocks a stronger claim."""

    model_config = ConfigDict(extra="forbid")

    item: str = Field(min_length=1)
    status: AdvisorReadinessStatus
    reason: str = Field(min_length=1)
    next_action: str = Field(min_length=1)


class AdvisorPackSection(BaseModel):
    """A rendered advisor pack section."""

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: AdvisorReadinessStatus
    body: str = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)


class AdvisorPack(BaseModel):
    """Advisor-facing VGGT / SMPL-X status package."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(min_length=1)
    advisor_goal: str = Field(min_length=1)
    current_route_summary: str = Field(min_length=1)
    what_changed_since_last_update: list[str] = Field(min_length=1)
    observed_evidence: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    visual_readiness: AdvisorReadinessStatus
    not_ready_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(min_length=1)
    suggested_advisor_message: str = Field(min_length=1)
    required_human_review: list[str] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)
    sections: list[AdvisorPackSection] = Field(default_factory=list)

    @model_validator(mode="after")
    def blocked_pack_requires_not_ready_claims(self) -> Self:
        if self.visual_readiness in {
            AdvisorReadinessStatus.NOT_READY,
            AdvisorReadinessStatus.BLOCKED,
        } and not self.not_ready_claims:
            raise ValueError("blocked advisor pack requires not_ready_claims")
        return self

    def section(self, section_id: str) -> AdvisorPackSection:
        """Return a section by id."""

        for section in self.sections:
            if section.section_id == section_id:
                return section
        raise KeyError(section_id)

    def to_markdown(self) -> str:
        """Render a concise advisor summary in Markdown."""

        lines = [
            "# Advisor Summary",
            "",
            f"Goal: {self.advisor_goal}",
            "",
            "## Current Route",
            "",
            self.current_route_summary,
            "",
            "## What Changed",
            "",
        ]
        lines.extend(f"- {item}" for item in self.what_changed_since_last_update)
        lines.extend(["", "## Observed Evidence", ""])
        lines.extend(
            _list_or_placeholder(
                self.observed_evidence,
                "No observed evidence is available.",
            )
        )
        lines.extend(["", "## Limitations", ""])
        lines.extend(_list_or_placeholder(self.limitations, "No limitations recorded."))
        lines.extend(["", "## Blockers", ""])
        lines.extend(_list_or_placeholder(self.blockers, "No blockers recorded."))
        lines.extend(["", "## Visual Readiness", "", f"- Status: {self.visual_readiness.value}"])
        lines.extend(["", "## Not-Ready Claims", ""])
        lines.extend(_list_or_placeholder(self.not_ready_claims, "No not-ready claims recorded."))
        lines.extend(["", "## Next Actions", ""])
        lines.extend(f"- {item}" for item in self.next_actions)
        lines.extend(["", "## Suggested Advisor Message", "", self.suggested_advisor_message])
        if self.required_human_review:
            lines.extend(["", "## Required Human Review", ""])
            lines.extend(f"- {item}" for item in self.required_human_review)
        if self.missing_inputs:
            lines.extend(["", "## Missing Inputs", ""])
            lines.extend(f"- `{item}`" for item in self.missing_inputs)
        return "\n".join(lines) + "\n"


class AdvisorPackBuildInput(BaseModel):
    """Input paths for building a Markdown-only advisor pack."""

    model_config = ConfigDict(extra="forbid")

    pack_id: str = "vggt-sprint1-advisor-pack"
    advisor_goal: str = "Summarize VGGT / SMPL-X dogfooding status without overclaiming."
    output_dir: Path | None = None
    dogfooding_doc_path: Path
    vggt_evidence_doc_path: Path
    artifact_auditor_doc_path: Path
    visual_evidence_doc_path: Path
    sprint_plan_path: Path
    risk_register_path: Path
    local_scan_summary_path: Path
    local_scan_artifact_index_path: Path
    local_scan_evidence_ledger_path: Path | None = None
    visual_evidence_audit_report_path: Path | None = None
    visual_evidence_missing_items_path: Path | None = None
    visual_evidence_scorecard_path: Path | None = None


def _list_or_placeholder(items: list[str], placeholder: str) -> list[str]:
    if not items:
        return [f"- {placeholder}"]
    return [f"- {item}" for item in items]
