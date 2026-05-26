"""Markdown exports for paper writing scaffolds."""

from __future__ import annotations

from turing_research_plus.paper_write.evidence_linker import missing_evidence_report
from turing_research_plus.paper_write.models import PaperScaffold, PaperSectionPlan
from turing_research_plus.paper_write.section_status import summarize_section_status


def render_paper_outline(scaffold: PaperScaffold) -> str:
    """Render a safe paper outline."""

    sections = [
        scaffold.introduction_plan,
        scaffold.related_work_plan,
        scaffold.method_plan,
        scaffold.experiment_plan,
        scaffold.limitation_plan,
    ]
    lines = [
        f"# Paper Outline: {scaffold.topic}",
        "",
        "## Title Candidates",
        "",
        *[f"- {title}" for title in scaffold.title_candidates],
        "",
        "## Sections",
        "",
    ]
    for section in sections:
        lines.extend(_render_section(section))
    lines.extend(
        [
            "## Safety Boundary",
            "",
            "- This is a scaffold, not final paper prose.",
            "- No final abstract is generated.",
            "- No final results are generated.",
            "- Planned experiments stay in the experiment plan.",
            "",
        ]
    )
    return "\n".join(lines)


def render_section_status(scaffold: PaperScaffold) -> str:
    """Render section readiness status."""

    sections = [
        scaffold.introduction_plan,
        scaffold.related_work_plan,
        scaffold.method_plan,
        scaffold.experiment_plan,
        scaffold.limitation_plan,
    ]
    lines = [
        "# Paper Section Status",
        "",
        f"- Abstract status: `{scaffold.abstract_status}`",
        f"- Results status: `{scaffold.results_status}`",
        f"- Requires human review: `{str(scaffold.requires_human_review).lower()}`",
        "",
        "## Sections",
        "",
        *summarize_section_status(sections),
        "",
    ]
    return "\n".join(lines)


def render_evidence_gap_report(scaffold: PaperScaffold) -> str:
    """Render missing evidence and unsafe claims."""

    lines = [
        "# Evidence Gap Report",
        "",
        "## Evidence Requirements",
        "",
        *missing_evidence_report(scaffold.evidence_requirements),
        "",
        "## Missing Experiments",
        "",
        *[f"- {item}" for item in scaffold.missing_experiments],
        "",
        "## Unsafe Claims",
        "",
        *[f"- {item}" for item in scaffold.unsafe_claims],
        "",
    ]
    return "\n".join(lines)


def _render_section(section: PaperSectionPlan) -> list[str]:
    lines = [
        f"### {section.title}",
        "",
        f"- Status: `{section.status}`",
        "",
    ]
    lines.extend([f"- {bullet}" for bullet in section.bullets] or ["- No bullets yet."])
    if section.missing_evidence:
        lines.extend(["", "Missing evidence:"])
        lines.extend([f"- {item}" for item in section.missing_evidence])
    if section.unsafe_claims:
        lines.extend(["", "Unsafe claims:"])
        lines.extend([f"- {item}" for item in section.unsafe_claims])
    lines.append("")
    return lines
