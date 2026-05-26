"""Models and Markdown export for paper draft beta packages."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PaperDraftPackage(BaseModel):
    """Evidence-linked beta paper draft package.

    This package is deliberately review-only. It does not represent a finished
    paper, final abstract, final conclusion, or result section.
    """

    model_config = ConfigDict(extra="forbid")

    package_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    title_candidates: list[str] = Field(min_length=1)
    abstract_placeholder: str = Field(min_length=1)
    introduction_skeleton: str = Field(min_length=1)
    related_work_skeleton: str = Field(min_length=1)
    method_skeleton: str = Field(min_length=1)
    experiment_skeleton: str = Field(min_length=1)
    results_blocked_section: str = Field(min_length=1)
    limitations: str = Field(min_length=1)
    missing_evidence_report: str = Field(min_length=1)
    unsafe_claim_report: str = Field(min_length=1)
    citation_status_report: str = Field(min_length=1)
    requires_human_review: bool = True
    generated_final_paper: bool = False
    generated_final_abstract: bool = False
    generated_final_results: bool = False
    camera_ready_text: bool = False

    @model_validator(mode="after")
    def beta_package_must_not_be_final_paper(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("paper draft beta package requires human review")
        if self.generated_final_paper:
            raise ValueError("paper draft beta must not generate a final paper")
        if self.generated_final_abstract:
            raise ValueError("paper draft beta must not generate a final abstract")
        if self.generated_final_results:
            raise ValueError("paper draft beta must not generate final results")
        if self.camera_ready_text:
            raise ValueError("paper draft beta must not claim camera-ready text")
        if "placeholder" not in self.abstract_placeholder.lower():
            raise ValueError("abstract must remain a placeholder")
        if "Result tables allowed: `false`" not in self.results_blocked_section:
            raise ValueError("results section must remain blocked")
        return self


def render_paper_draft_package(package: PaperDraftPackage) -> str:
    """Render the beta draft package as Markdown."""

    lines = [
        f"# Paper Draft Beta Package: {package.topic}",
        "",
        f"- Package ID: `{package.package_id}`",
        f"- Requires human review: `{str(package.requires_human_review).lower()}`",
        "- Status: `review-only-beta`",
        "",
        "## Title Candidates",
        "",
        *[f"- {title}" for title in package.title_candidates],
        "",
        "## Abstract Placeholder",
        "",
        package.abstract_placeholder,
        "",
        "## Introduction Skeleton",
        "",
        package.introduction_skeleton,
        "",
        "## Related Work Skeleton",
        "",
        package.related_work_skeleton,
        "",
        "## Method Skeleton",
        "",
        package.method_skeleton,
        "",
        "## Experiment Skeleton",
        "",
        package.experiment_skeleton,
        "",
        "## Results Blocked Section",
        "",
        package.results_blocked_section,
        "",
        "## Limitations",
        "",
        package.limitations,
        "",
        "## Safety Boundary",
        "",
        "- This is not a final paper.",
        "- No final abstract is generated.",
        "- No final result section is generated.",
        "- No result value, table, figure, metric, or ablation is fabricated.",
        "- Human review is required before any paper prose can be promoted.",
        "",
    ]
    return "\n".join(lines)


def export_paper_draft_package(
    package: PaperDraftPackage,
    output_dir: Path,
) -> list[Path]:
    """Export a paper draft beta package to Markdown files."""

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        (output_dir / "paper_draft_beta.md", render_paper_draft_package(package)),
        (output_dir / "missing_evidence_report.md", package.missing_evidence_report),
        (output_dir / "unsafe_claim_report.md", package.unsafe_claim_report),
        (output_dir / "citation_status_report.md", package.citation_status_report),
    ]
    for path, text in outputs:
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return [path for path, _ in outputs]
