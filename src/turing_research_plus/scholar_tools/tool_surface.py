"""Scholar full tool surface catalog."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ScholarToolSurfaceEntry(BaseModel):
    """One Scholar tool-surface entry."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = Field(min_length=1)
    module: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    default_mode: str = "fake/default"
    live_optional: bool = False
    requires_api_key: bool = False
    requires_human_review: bool = True
    automatic_full_paper_download: bool = False
    mineru_enabled: bool = False
    paywall_bypass_allowed: bool = False
    final_conclusion_generated: bool = False

    @property
    def release_blocker(self) -> bool:
        """Return whether this entry enables unsafe defaults."""

        return (
            self.requires_api_key
            or self.automatic_full_paper_download
            or self.mineru_enabled
            or self.paywall_bypass_allowed
            or self.final_conclusion_generated
            or not self.requires_human_review
        )


class ScholarFullToolSurface(BaseModel):
    """Review-only catalog for the Scholar full tool surface."""

    model_config = ConfigDict(extra="forbid")

    surface_id: str = "scholar-full-tool-surface-v1.3"
    status: str = "implemented"
    tools: list[ScholarToolSurfaceEntry] = Field(default_factory=list)
    fake_mode_default: bool = True
    live_tests_skipped_by_default: bool = True
    mineru_enabled: bool = False
    automatic_full_paper_download: bool = False
    paywall_bypass_allowed: bool = False
    final_paper_conclusion_allowed: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether the full surface violates safe defaults."""

        return (
            not self.fake_mode_default
            or not self.live_tests_skipped_by_default
            or self.mineru_enabled
            or self.automatic_full_paper_download
            or self.paywall_bypass_allowed
            or self.final_paper_conclusion_allowed
            or not self.requires_human_review
            or any(tool.release_blocker for tool in self.tools)
        )


def build_scholar_full_tool_surface() -> ScholarFullToolSurface:
    """Build the v1.3 Scholar tool-surface catalog."""

    return ScholarFullToolSurface(
        tools=[
            ScholarToolSurfaceEntry(
                tool_name="scholar.paper_searching",
                module="turing_research_plus.scholar_tools.paper_searching",
                purpose="Cache-first fake/default paper lookup.",
            ),
            ScholarToolSurfaceEntry(
                tool_name="scholar.paper_content",
                module="turing_research_plus.scholar_tools.paper_content",
                purpose="Read already cached local Markdown paper content.",
            ),
            ScholarToolSurfaceEntry(
                tool_name="scholar.paper_reference",
                module="turing_research_plus.scholar_tools.paper_reference",
                purpose="Resolve references through fake/default, cached, or manual fallback.",
            ),
            ScholarToolSurfaceEntry(
                tool_name="scholar.paper_reading",
                module="turing_research_plus.scholar_tools.paper_reading",
                purpose="Build a three-pass paper reading plan for human review.",
            ),
        ]
    )


def render_scholar_full_tool_surface(surface: ScholarFullToolSurface) -> str:
    """Render the Scholar tool surface as Markdown."""

    lines = [
        "# Scholar Full Tool Surface",
        "",
        f"- Surface ID: `{surface.surface_id}`",
        f"- Status: `{surface.status}`",
        f"- Fake mode default: `{str(surface.fake_mode_default).lower()}`",
        "- Live tests skipped by default: "
        f"`{str(surface.live_tests_skipped_by_default).lower()}`",
        f"- MinerU enabled: `{str(surface.mineru_enabled).lower()}`",
        "- Automatic full paper download: "
        f"`{str(surface.automatic_full_paper_download).lower()}`",
        f"- Paywall bypass allowed: `{str(surface.paywall_bypass_allowed).lower()}`",
        "- Final paper conclusion allowed: "
        f"`{str(surface.final_paper_conclusion_allowed).lower()}`",
        f"- Requires human review: `{str(surface.requires_human_review).lower()}`",
        "",
        "| Tool | Module | Purpose | Mode | Human review |",
        "| --- | --- | --- | --- | --- |",
    ]
    for tool in surface.tools:
        lines.append(
            f"| `{tool.tool_name}` | `{tool.module}` | {tool.purpose} | "
            f"{tool.default_mode} | `{str(tool.requires_human_review).lower()}` |"
        )
    return "\n".join(lines) + "\n"
