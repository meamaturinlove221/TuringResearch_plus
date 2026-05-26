"""Template helpers for optional Advisor PDF export."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import AdvisorMarkdownBundle

PDF_REQUIRED_SECTIONS = [
    "title",
    "current status",
    "evidence summary",
    "artifact readiness",
    "visual readiness",
    "failure summary",
    "next actions",
    "limitations",
    "requires human review",
]


def build_pdf_section_text(bundle: AdvisorMarkdownBundle) -> dict[str, str]:
    """Build review-safe PDF sections from a Markdown bundle."""

    files = _bundle_file_text(bundle)
    report = files.get("advisor_report_source.md", "")
    evidence = files.get("evidence_refs.md", "")
    figures = files.get("figure_list.md", "")
    tables = files.get("table_list.md", "")
    limitations = files.get("limitations.md", "")
    next_actions = files.get("next_actions.md", "")

    return {
        "title": bundle.topic,
        "current status": _extract_section(report, "Current Status") or report,
        "evidence summary": evidence,
        "artifact readiness": _join_nonempty([figures, tables]),
        "visual readiness": _visual_boundary(figures),
        "failure summary": _failure_boundary(report, limitations),
        "next actions": next_actions,
        "limitations": limitations,
        "requires human review": _human_review_boundary(bundle),
    }


def render_pdf_review_markdown(bundle: AdvisorMarkdownBundle) -> str:
    """Render the PDF source text as Markdown for audit and fallback output."""

    sections = build_pdf_section_text(bundle)
    lines = [
        "# Advisor PDF Review Source",
        "",
        "- Status: optional PDF export source.",
        "- This Markdown source remains authoritative for review.",
        "- No figures, result values, or experiment claims are fabricated.",
        "- Requires human review before advisor delivery.",
        "",
    ]
    for section in PDF_REQUIRED_SECTIONS:
        title = section.title()
        section_text = sections[section].strip() or "No source text provided."
        lines.extend([f"## {title}", "", section_text, ""])
    return "\n".join(lines)


def _bundle_file_text(bundle: AdvisorMarkdownBundle) -> dict[str, str]:
    texts: dict[str, str] = {}
    for item in bundle.files:
        path = Path(item.path)
        if path.exists() and path.is_file():
            texts[path.name] = path.read_text(encoding="utf-8")
    return texts


def _extract_section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    start: int | None = None
    collected: list[str] = []
    target = f"## {heading}".lower()
    for index, line in enumerate(lines):
        if line.strip().lower() == target:
            start = index + 1
            continue
        if start is not None and line.startswith("## "):
            break
        if start is not None:
            collected.append(line)
    return "\n".join(collected).strip()


def _join_nonempty(parts: list[str]) -> str:
    return "\n\n".join(part.strip() for part in parts if part.strip())


def _visual_boundary(figures: str) -> str:
    return "\n".join(
        [
            figures.strip() or "No generated figures are included.",
            "",
            "Visual readiness must be backed by existing reviewed artifacts.",
            "This PDF export does not create visual evidence.",
        ]
    )


def _failure_boundary(report: str, limitations: str) -> str:
    text = _join_nonempty([_extract_section(report, "Boundary"), limitations])
    if text:
        return text
    return "Failure summary is limited to existing advisor source material."


def _human_review_boundary(bundle: AdvisorMarkdownBundle) -> str:
    marker = "required" if bundle.requires_human_review else "not recorded"
    return "\n".join(
        [
            f"Human review: {marker}.",
            "The PDF is an export artifact, not new evidence.",
            "Planned work remains planned and must not be written as observed.",
        ]
    )
