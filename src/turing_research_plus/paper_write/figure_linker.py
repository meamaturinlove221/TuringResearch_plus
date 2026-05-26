"""Figure placeholder linking for method section skeletons."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class MethodFigureLink(BaseModel):
    """A review-only figure placeholder for the method section."""

    model_config = ConfigDict(extra="forbid")

    figure_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    path: str = Field(min_length=1)
    source_status: str = "derived-from-fixture"
    evidence_refs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


def collect_mermaid_figure_links(diagram_dir: Path) -> list[MethodFigureLink]:
    """Collect local Mermaid diagrams as review-only figure placeholders."""

    links: list[MethodFigureLink] = []
    for path in sorted(diagram_dir.glob("*.mmd")):
        figure_id = path.stem
        links.append(
            MethodFigureLink(
                figure_id=figure_id,
                title=_title_from_stem(figure_id),
                path=path.as_posix(),
                evidence_refs=[path.as_posix()],
            )
        )
    return links


def render_figure_links_markdown(links: list[MethodFigureLink]) -> str:
    """Render figure placeholders as a Markdown table."""

    lines = [
        "# Method Figure Links",
        "",
        "| Figure | Title | Source status | Human review | Evidence ref |",
        "| --- | --- | --- | --- | --- |",
    ]
    for link in links:
        refs = ", ".join(f"`{ref}`" for ref in link.evidence_refs)
        lines.append(
            "| "
            f"`{link.figure_id}` | {link.title} | `{link.source_status}` | "
            f"`{str(link.requires_human_review).lower()}` | {refs} |"
        )
    lines.extend(
        [
            "",
            "These are figure placeholders, not fabricated paper figures.",
            "Every linked diagram remains requires-human-review.",
            "",
        ]
    )
    return "\n".join(lines)


def _title_from_stem(stem: str) -> str:
    return stem.replace("_", " ").replace("-", " ").title()
