"""Minimal LaTeX export for TulingResearch Plus paper drafts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LatexExportInput(BaseModel):
    """Input for paper.latex_export."""

    model_config = ConfigDict(extra="forbid")

    draft_markdown: str = Field(min_length=1)
    title: str = "TulingResearch Plus Paper Draft"


class LatexExportOutput(BaseModel):
    """Output for paper.latex_export."""

    model_config = ConfigDict(extra="forbid")

    latex_text: str = Field(min_length=1)


def export_latex(input_data: LatexExportInput) -> LatexExportOutput:
    """Export a minimal LaTeX document from Markdown headings."""

    lines = [
        "\\documentclass{article}",
        "\\title{" + _escape_latex(input_data.title) + "}",
        "\\begin{document}",
        "\\maketitle",
    ]
    for raw_line in input_data.draft_markdown.splitlines():
        if raw_line.startswith("# "):
            continue
        if raw_line.startswith("## "):
            lines.append("\\section{" + _escape_latex(raw_line[3:]) + "}")
        elif raw_line:
            lines.append(_escape_latex(raw_line))
    lines.append("\\end{document}")
    return LatexExportOutput(latex_text="\n".join(lines) + "\n")


def paper_latex_export(input_data: LatexExportInput) -> dict[str, object]:
    """Thin paper.latex_export wrapper."""

    return export_latex(input_data).model_dump(mode="json")


def _escape_latex(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    escaped = value
    for source, target in replacements.items():
        escaped = escaped.replace(source, target)
    return escaped
