"""Tool list export for Scholar parity docs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ScholarToolEntry(BaseModel):
    """One public Scholar pipeline tool entry."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    mode: str = "fake/default"
    live_optional: bool = False
    requires_api_key: bool = False
    requires_human_review: bool = True


class ScholarToolList(BaseModel):
    """Public tool list for the Scholar pipeline."""

    model_config = ConfigDict(extra="forbid")

    tools: list[ScholarToolEntry] = Field(default_factory=list)
    live_tests_skipped_by_default: bool = True
    no_real_api_key_required: bool = True


def build_scholar_tool_list() -> ScholarToolList:
    """Build the public Scholar tool list."""

    return ScholarToolList(
        tools=[
            ScholarToolEntry(
                name="paper.search_pipeline",
                purpose=(
                    "Cache-first paper lookup using cached Markdown, known arXiv metadata, "
                    "fake adapters, or manual fallback."
                ),
            ),
            ScholarToolEntry(
                name="paper.reference_pipeline",
                purpose=(
                    "Resolve references from fake Semantic Scholar, cached Markdown, "
                    "or manual lists."
                ),
            ),
            ScholarToolEntry(
                name="paper.three_pass_reading_plan",
                purpose="Create a review checklist for first, second, and third reading passes.",
            ),
            ScholarToolEntry(
                name="paper.digest",
                purpose="Convert fixture or cached notes into a review-only paper digest.",
            ),
        ]
    )


def render_scholar_tool_list(tool_list: ScholarToolList) -> str:
    """Render the Scholar tool list as Markdown."""

    lines = [
        "# Scholar Tool List",
        "",
        "- Live tests skipped by default: "
        f"`{str(tool_list.live_tests_skipped_by_default).lower()}`",
        f"- No real API key required: `{str(tool_list.no_real_api_key_required).lower()}`",
        "",
        "| Tool | Purpose | Mode | API key | Human review |",
        "| --- | --- | --- | --- | --- |",
    ]
    for tool in tool_list.tools:
        lines.append(
            f"| `{tool.name}` | {tool.purpose} | {tool.mode} | "
            f"`{str(tool.requires_api_key).lower()}` | "
            f"`{str(tool.requires_human_review).lower()}` |"
        )
    return "\n".join(lines) + "\n"
