"""Citation status guards for paper draft beta packages."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

NON_FINAL_SOURCE_STATUSES = {
    "fake-or-manual-note",
    "fixture",
    "requires-real-paper-review",
}


class PaperCitationStatus(BaseModel):
    """One citation candidate status for beta paper assembly."""

    model_config = ConfigDict(extra="forbid")

    citation_id: str = Field(min_length=1)
    source_status: str = Field(min_length=1)
    citation_grade: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def non_final_sources_cannot_be_citation_grade(self) -> Self:
        if self.source_status in NON_FINAL_SOURCE_STATUSES and self.citation_grade:
            raise ValueError("non-final citation source cannot be citation-grade")
        if self.source_status in NON_FINAL_SOURCE_STATUSES and not self.requires_human_review:
            raise ValueError("non-final citation source requires human review")
        return self


class PaperCitationStatusReport(BaseModel):
    """Citation status report for beta paper assembly."""

    model_config = ConfigDict(extra="forbid")

    citations: list[PaperCitationStatus] = Field(default_factory=list)
    blocked_citations: list[str] = Field(default_factory=list)
    fabricated_citation_blocked: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def citation_report_must_stay_review_only(self) -> Self:
        if not self.fabricated_citation_blocked:
            raise ValueError("fabricated citation blocking must stay enabled")
        if not self.requires_human_review:
            raise ValueError("citation status guard requires human review")
        return self


def parse_citation_status_report(markdown: str) -> PaperCitationStatusReport:
    """Parse the existing citation safety Markdown table into a beta report."""

    citations: list[PaperCitationStatus] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped.startswith("| `") or "---" in stripped:
            continue
        parts = [part.strip().strip("`") for part in stripped.strip("|").split("|")]
        if len(parts) != 4:
            continue
        citation_id, source_status, citation_grade, requires_review = parts
        citations.append(
            PaperCitationStatus(
                citation_id=citation_id,
                source_status=source_status,
                citation_grade=citation_grade.lower() == "true",
                requires_human_review=requires_review.lower() != "false",
            )
        )

    blocked = [
        f"`{citation.citation_id}` remains `{citation.source_status}` and is "
        "not final citation support."
        for citation in citations
        if citation.source_status in NON_FINAL_SOURCE_STATUSES or citation.requires_human_review
    ]
    return PaperCitationStatusReport(citations=citations, blocked_citations=blocked)


def render_paper_citation_status_report(report: PaperCitationStatusReport) -> str:
    """Render citation status guard output as Markdown."""

    lines = [
        "# Citation Status Report",
        "",
        f"- Fabricated citation blocked: `{str(report.fabricated_citation_blocked).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
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
            "## Blocked Citation Uses",
            "",
            *[f"- {item}" for item in report.blocked_citations],
            "",
            "## Boundary",
            "",
            "- Fixture citations are not final paper citations.",
            "- Missing review remains visible.",
            "- Human review is required before paper prose.",
            "",
        ]
    )
    return "\n".join(lines)
