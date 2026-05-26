"""Template helpers for optional Advisor PPTX export."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import AdvisorMarkdownBundle
from turing_research_plus.advisor_export.pptx_models import AdvisorPptxSlide

DECK_SECTION_TITLES = [
    "Research North Star",
    "Current Engineering State",
    "Evidence Summary",
    "Visual Readiness",
    "Failure / Blockers",
    "Related Work Position",
    "Next Experiment Route",
    "Advisor Ask / Decision Needed",
]


def build_advisor_pptx_slides(bundle: AdvisorMarkdownBundle) -> list[AdvisorPptxSlide]:
    """Build review-safe slide content from an Advisor Markdown Bundle."""

    files = _bundle_file_text(bundle)
    report = files.get("advisor_report_source.md", "")
    evidence = files.get("evidence_refs.md", "")
    figures = files.get("figure_list.md", "")
    limitations = files.get("limitations.md", "")
    next_actions = files.get("next_actions.md", "")
    outline = files.get("slides_outline.md", "")

    return [
        AdvisorPptxSlide(
            slide_id="slide-01",
            title="Research North Star",
            bullets=[
                _first_content_line(outline, default=bundle.topic),
                "Frame direction without claiming final experiment success.",
                "requires-human-review",
            ],
            source_refs=["slides_outline.md", "advisor_report_source.md"],
        ),
        AdvisorPptxSlide(
            slide_id="slide-02",
            title="Current Engineering State",
            bullets=[
                _not_ready(
                    _extract_section(report, "Current Status")
                    or "Current status requires review."
                ),
                "Separate observed, planned, blocked, and not-enough-evidence states.",
                "requires-human-review",
            ],
            source_refs=["advisor_report_source.md"],
            not_ready=True,
        ),
        AdvisorPptxSlide(
            slide_id="slide-03",
            title="Evidence Summary",
            bullets=[
                _not_ready(
                    _compact_text(evidence) or "Evidence summary is missing from the bundle."
                ),
                "Do not promote fixture notes to verified evidence.",
                "requires-human-review",
            ],
            source_refs=["evidence_refs.md"],
            not_ready=True,
        ),
        AdvisorPptxSlide(
            slide_id="slide-04",
            title="Visual Readiness",
            bullets=[
                _compact_text(figures) or "No generated figures are included.",
                "not-ready: visual evidence must come from reviewed artifacts.",
                "requires-human-review",
            ],
            source_refs=["figure_list.md"],
            not_ready=True,
        ),
        AdvisorPptxSlide(
            slide_id="slide-05",
            title="Failure / Blockers",
            bullets=[
                _extract_section(report, "Boundary") or _compact_text(limitations),
                "not-ready claims must remain marked until evidence exists.",
                "requires-human-review",
            ],
            source_refs=["advisor_report_source.md", "limitations.md"],
            not_ready=True,
        ),
        AdvisorPptxSlide(
            slide_id="slide-06",
            title="Related Work Position",
            bullets=[
                "not-ready: keep related-work positioning conservative.",
                "Do not claim complete paper review from fixtures.",
                "requires-human-review",
            ],
            source_refs=["advisor_report_source.md"],
            not_ready=True,
        ),
        AdvisorPptxSlide(
            slide_id="slide-07",
            title="Next Experiment Route",
            bullets=[
                _not_ready(
                    _compact_text(next_actions) or "Next actions are missing from the bundle."
                ),
                "Planned experiment routes are not executed results.",
                "requires-human-review",
            ],
            source_refs=["next_actions.md"],
            not_ready=True,
        ),
        AdvisorPptxSlide(
            slide_id="slide-08",
            title="Advisor Ask / Decision Needed",
            bullets=[
                "Ask advisor to review evidence gaps and next route priority.",
                "not-ready: do not treat this deck as final results.",
                "requires-human-review",
            ],
            source_refs=["limitations.md", "next_actions.md"],
            not_ready=True,
        ),
    ]


def render_pptx_review_markdown(bundle: AdvisorMarkdownBundle) -> str:
    """Render deck content as Markdown for audit and fallback output."""

    lines = [
        "# Advisor PPTX Review Source",
        "",
        "- Status: optional PPTX export source.",
        "- The Markdown bundle remains authoritative.",
        "- No fake figures, charts, or experiment values are generated.",
        "- Not-ready claims remain explicitly marked.",
        "- Requires human review before advisor delivery.",
        "",
    ]
    for slide in build_advisor_pptx_slides(bundle):
        lines.extend([f"## {slide.slide_id}: {slide.title}", ""])
        lines.extend([f"- {bullet}" for bullet in slide.bullets])
        lines.extend(["", "Source refs:"])
        lines.extend([f"- `{item}`" for item in slide.source_refs])
        lines.append("")
    return "\n".join(lines)


def _bundle_file_text(bundle: AdvisorMarkdownBundle) -> dict[str, str]:
    texts: dict[str, str] = {}
    for item in bundle.files:
        path = Path(item.path)
        if path.exists() and path.is_file():
            texts[path.name] = path.read_text(encoding="utf-8")
    return texts


def _first_content_line(markdown: str, *, default: str) -> str:
    for line in markdown.splitlines():
        clean = line.strip().lstrip("#").strip()
        if clean and not clean.startswith("Note:"):
            return clean
    return default


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
    return _compact_text("\n".join(collected))


def _compact_text(text: str, *, limit: int = 180) -> str:
    cleaned = " ".join(
        line.strip().lstrip("-").strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def _not_ready(text: str) -> str:
    if "not-ready" in text.lower():
        return text
    return f"not-ready: {text}"
