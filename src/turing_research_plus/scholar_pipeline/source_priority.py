"""Source-priority helpers for the Scholar parity layer."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.scholar_pipeline.models import ScholarSourcePriority

DEFAULT_SOURCE_PRIORITY = [
    ScholarSourcePriority.CACHED_MARKDOWN,
    ScholarSourcePriority.ARXIV,
    ScholarSourcePriority.SEMANTIC_SCHOLAR,
    ScholarSourcePriority.UNPAYWALL_PLACEHOLDER,
    ScholarSourcePriority.MANUAL,
]


class ScholarSourcePriorityPlan(BaseModel):
    """Review-only source priority plan for paper lookup."""

    model_config = ConfigDict(extra="forbid")

    priority: list[ScholarSourcePriority] = Field(
        default_factory=lambda: list(DEFAULT_SOURCE_PRIORITY)
    )
    cached_markdown_policy: str = (
        "Use local cached Markdown first; it is not human-verified by default."
    )
    live_enabled_by_default: bool = False
    automatic_full_paper_download: bool = False
    paywall_bypass_allowed: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether the plan violates public-safe defaults."""

        return (
            self.live_enabled_by_default
            or self.automatic_full_paper_download
            or self.paywall_bypass_allowed
            or not self.requires_human_review
        )


def build_scholar_source_priority_plan() -> ScholarSourcePriorityPlan:
    """Return the default Scholar source priority plan."""

    return ScholarSourcePriorityPlan()


def render_scholar_source_priority_plan(plan: ScholarSourcePriorityPlan) -> str:
    """Render a Markdown source priority summary."""

    lines = [
        "# Scholar Source Priority",
        "",
        f"- Live enabled by default: `{str(plan.live_enabled_by_default).lower()}`",
        f"- Automatic full paper download: `{str(plan.automatic_full_paper_download).lower()}`",
        f"- Paywall bypass allowed: `{str(plan.paywall_bypass_allowed).lower()}`",
        f"- Requires human review: `{str(plan.requires_human_review).lower()}`",
        "",
        "## Priority",
        "",
    ]
    lines.extend([f"{index}. `{source.value}`" for index, source in enumerate(plan.priority, 1)])
    lines.extend(["", "## Cached Markdown Policy", "", plan.cached_markdown_policy])
    return "\n".join(lines) + "\n"
