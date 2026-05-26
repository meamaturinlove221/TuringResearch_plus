from turing_research_plus.paper.latex_export import (
    LatexExportInput,
    export_latex,
    paper_latex_export,
)


def markdown() -> str:
    return """# TuringResearch Plus Paper Draft

## Abstract
Evidence-backed summary.

## Method
Architecture figure fig_1 is referenced.
"""


def test_latex_export_sections() -> None:
    result = export_latex(LatexExportInput(draft_markdown=markdown(), title="Draft_1"))

    assert "\\title{Draft\\_1}" in result.latex_text
    assert "\\section{Abstract}" in result.latex_text
    assert "\\section{Method}" in result.latex_text


def test_paper_latex_export_tool_returns_json_payload() -> None:
    payload = paper_latex_export(LatexExportInput(draft_markdown=markdown()))

    assert payload["latex_text"].startswith("\\documentclass{article}")
    assert "\\end{document}" in payload["latex_text"]
