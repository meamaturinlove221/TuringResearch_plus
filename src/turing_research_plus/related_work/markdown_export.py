"""Markdown export for related-work positioning reports."""

from __future__ import annotations

from turing_research_plus.related_work.models import RelatedWorkPositioningReport


def export_related_work_positioning_markdown(report: RelatedWorkPositioningReport) -> str:
    """Export a report as review Markdown, not final paper prose."""

    lines = [
        "# Related Work Positioning Report",
        "",
        f"Project topic: `{report.project_topic}`",
        f"Requires human review: `{report.requires_human_review}`",
        "",
        "## Recommended Structure",
    ]
    lines.extend(f"- {item}" for item in report.recommended_related_work_structure)
    lines.extend(["", "## Paper Groups"])
    lines.extend(
        f"- `{entry.group}` {entry.title}: {entry.rationale}"
        for entry in report.paper_groups
    )
    lines.extend(["", "## Overlap Summary"])
    lines.extend(f"- {item}" for item in report.overlap_summary)
    lines.extend(["", "## Differentiation Points"])
    lines.extend(f"- {item}" for item in report.differentiation_points)
    lines.extend(["", "## Safe Claims"])
    lines.extend(f"- {claim.text} Caveat: {claim.caveat}" for claim in report.safe_claims)
    lines.extend(["", "## Unsafe Claims"])
    lines.extend(f"- {claim.text} Reason: {claim.basis}" for claim in report.unsafe_claims)
    lines.extend(["", "## Missing Evidence"])
    lines.extend(
        f"- {item.item}: {item.reason} Action: {item.required_action}"
        for item in report.missing_evidence
    )
    lines.append("")
    return "\n".join(lines)
