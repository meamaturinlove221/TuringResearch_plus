"""Models for the Paper Digest Engine."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PaperDigestSourceStatus(StrEnum):
    """Source status for digest inputs."""

    CACHED_MARKDOWN = "cached-markdown"
    PDF_MARKDOWN = "pdf-markdown"
    HTML_SUMMARY = "html-summary"
    MANUAL_NOTE = "manual-note"
    FAKE_OR_MANUAL_NOTE = "fake-or-manual-note"
    REQUIRES_REAL_PAPER = "requires-real-paper"


class ThreePassReadingNotes(BaseModel):
    """Notes collected by a conservative three-pass reading workflow."""

    model_config = ConfigDict(extra="forbid")

    pass1_summary: str = Field(min_length=1)
    pass2_notes: list[str] = Field(default_factory=list)
    pass3_deep_notes: list[str] = Field(default_factory=list)
    requires_real_paper_review: bool = True


class PaperDigestInput(BaseModel):
    """Input for building a PaperDigest from local text or notes."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_status: PaperDigestSourceStatus
    source_text: str | None = None
    pass_notes: ThreePassReadingNotes | None = None
    citation: str | None = None
    human_verified: bool = False

    @model_validator(mode="after")
    def input_is_not_fake_verified(self) -> Self:
        if self.human_verified and self.source_status in {
            PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            PaperDigestSourceStatus.REQUIRES_REAL_PAPER,
        }:
            raise ValueError("fake or missing paper inputs cannot be human verified")
        if self.source_text is None and self.pass_notes is None:
            raise ValueError("provide source_text or pass_notes")
        return self


class PaperDigest(BaseModel):
    """Reusable conservative paper digest."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_status: PaperDigestSourceStatus
    pass1_summary: str = Field(min_length=1)
    pass2_notes: list[str] = Field(default_factory=list)
    pass3_deep_notes: list[str] = Field(default_factory=list)
    method_contribution: str = Field(min_length=1)
    figures_to_inspect: list[str] = Field(default_factory=list)
    equations_to_inspect: list[str] = Field(default_factory=list)
    experiment_table_notes: list[str] = Field(default_factory=list)
    what_to_borrow: list[str] = Field(default_factory=list)
    what_not_to_copy: list[str] = Field(default_factory=list)
    collision_notes: list[str] = Field(default_factory=list)
    related_work_positioning: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    requires_real_paper: bool = True
    human_verified: bool = False
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def digest_is_not_complete_review_claim(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("paper digests require human review")
        if self.human_verified and self.source_status in {
            PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            PaperDigestSourceStatus.REQUIRES_REAL_PAPER,
        }:
            raise ValueError("fixture digests cannot be human verified")
        lowered = " ".join(
            [
                self.pass1_summary,
                self.method_contribution,
                *self.pass2_notes,
                *self.pass3_deep_notes,
            ]
        ).lower()
        if "complete paper review" in lowered or "fully read" in lowered:
            raise ValueError("paper digest cannot claim complete paper review")
        return self
