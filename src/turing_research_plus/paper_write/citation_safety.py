"""Citation safety helpers for related-work draft scaffolds."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

FIXTURE_SOURCE_STATUSES = {
    "fake-or-manual-note",
    "fixture",
    "requires-real-paper-review",
}


class RelatedWorkCitation(BaseModel):
    """A citation candidate with explicit source status."""

    model_config = ConfigDict(extra="forbid")

    citation_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_status: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    citation_grade: bool = False

    @model_validator(mode="after")
    def fixture_citations_are_not_citation_grade(self) -> Self:
        if self.source_status in FIXTURE_SOURCE_STATUSES and self.citation_grade:
            raise ValueError("fixture citation cannot be citation-grade")
        if self.source_status in FIXTURE_SOURCE_STATUSES and not self.requires_human_review:
            raise ValueError("fixture citation requires human review")
        return self


class CitationSafetyReport(BaseModel):
    """Safety report for related-work citation candidates."""

    model_config = ConfigDict(extra="forbid")

    citations: list[RelatedWorkCitation] = Field(default_factory=list)
    unsafe_citations: list[str] = Field(default_factory=list)
    missing_review: list[str] = Field(default_factory=list)
    fabricated_citation_blocked: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def report_stays_review_only(self) -> Self:
        if not self.fabricated_citation_blocked:
            raise ValueError("fabricated citation blocking must stay enabled")
        if not self.requires_human_review:
            raise ValueError("citation safety report requires human review")
        return self


def evaluate_citation_safety(
    citations: list[RelatedWorkCitation],
) -> CitationSafetyReport:
    """Evaluate local citation candidates without promoting fixture evidence."""

    unsafe: list[str] = []
    missing_review: list[str] = []
    for citation in citations:
        if citation.source_status in FIXTURE_SOURCE_STATUSES:
            unsafe.append(
                f"`{citation.citation_id}` is `{citation.source_status}` and "
                "cannot be used as a final citation."
            )
        if citation.requires_human_review:
            missing_review.append(
                f"`{citation.citation_id}` requires human review before paper text."
            )
    return CitationSafetyReport(
        citations=citations,
        unsafe_citations=unsafe,
        missing_review=missing_review,
    )


def citation_from_digest_fixture(path: Path) -> RelatedWorkCitation:
    """Create a citation candidate from a local paper digest fixture."""

    text = path.read_text(encoding="utf-8")
    title = _extract_title(text) or path.stem.replace("_", " ").title()
    paper_id = _extract_field(text, "Paper ID") or path.stem
    source_status = _extract_field(text, "Source status") or "requires-real-paper-review"
    requires_review = (_extract_field(text, "Requires human review") or "true").lower()
    return RelatedWorkCitation(
        citation_id=paper_id,
        title=title,
        source_status=source_status,
        evidence_refs=[path.as_posix()],
        requires_human_review=requires_review != "false",
        citation_grade=False,
    )


def render_citation_safety_report(report: CitationSafetyReport) -> str:
    """Render citation safety as Markdown."""

    lines = [
        "# Citation Safety Report",
        "",
        "| Citation | Source status | Citation grade | Requires review |",
        "| --- | --- | --- | --- |",
    ]
    for citation in report.citations:
        lines.append(
            "| "
            f"`{citation.citation_id}` | `{citation.source_status}` | "
            f"`{str(citation.citation_grade).lower()}` | "
            f"`{str(citation.requires_human_review).lower()}` |"
        )
    lines.extend(
        [
            "",
            "## Unsafe Citation Uses",
            "",
            *[f"- {item}" for item in report.unsafe_citations],
            "",
            "## Missing Review",
            "",
            *[f"- {item}" for item in report.missing_review],
            "",
            "## Boundary",
            "",
            "- Fake fixtures are not final citations.",
            "- No citation is fabricated.",
            "- Human review is required before camera-ready paper text.",
            "",
        ]
    )
    return "\n".join(lines)


def _extract_title(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            title = line.removeprefix("# ").strip()
            return title.removeprefix("Paper Digest: ").strip()
    return None


def _extract_field(text: str, field: str) -> str | None:
    prefix = f"- {field}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip().strip("`")
    return None
