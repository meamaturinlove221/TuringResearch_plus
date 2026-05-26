"""Markdown exports for public case study drafts."""

from __future__ import annotations

from turing_research_plus.case_study.models import (
    CaseStudyClaimSafetyReport,
    CaseStudyDraft,
    CaseStudyRedactionReport,
    CaseStudySection,
)


def render_case_study_draft_markdown(draft: CaseStudyDraft) -> str:
    """Render a sanitized public case study draft."""

    lines = [
        f"# {draft.title}",
        "",
        "- Status: public draft / requires human review",
        "- Published: false",
        "- Public demo only: true",
        "",
    ]
    for section in draft.sections:
        lines.extend(_render_section(section))
    lines.extend(
        [
            "## Safety Boundary",
            "",
            "- This case study is not a publication.",
            "- It does not claim experiment success.",
            "- It does not claim SparseConv3D success.",
            "- It does not include private local paths, restricted datasets, "
            "model files, or non-public advisor notes.",
            "- Human review is required before release.",
            "",
        ]
    )
    return "\n".join(lines)


def render_case_study_redaction_markdown(report: CaseStudyRedactionReport) -> str:
    """Render redaction report Markdown."""

    lines = [
        "# Case Study Redaction Report",
        "",
        f"- Sanitized: `{str(report.sanitized).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Redactions",
        "",
    ]
    if report.redactions:
        for item in report.redactions:
            lines.append(
                "- "
                f"`{item.finding_type}` -> `{item.replacement}` "
                f"(applied: `{str(item.applied).lower()}`)"
            )
    else:
        lines.append("- none")
    lines.extend(["", "## Release Blockers", ""])
    lines.extend([f"- {item}" for item in report.release_blockers] or ["- none"])
    lines.append("")
    return "\n".join(lines)


def render_case_study_claim_safety_markdown(
    report: CaseStudyClaimSafetyReport,
) -> str:
    """Render claim safety report Markdown."""

    lines = [
        "# Case Study Claim Safety Report",
        "",
        f"- Safe to publish: `{str(report.safe_to_publish).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Findings",
        "",
    ]
    if report.findings:
        for finding in report.findings:
            lines.append(
                "- "
                f"`{finding.severity}` {finding.reason} "
                f"Replacement: {finding.replacement}"
            )
    else:
        lines.append("- none")
    lines.extend(["", "## Unsupported Experiment Claims", ""])
    lines.extend(
        [f"- {item}" for item in report.unsupported_experiment_claims] or ["- none"]
    )
    lines.append("")
    return "\n".join(lines)


def _render_section(section: CaseStudySection) -> list[str]:
    lines = [
        f"## {section.title}",
        "",
        *[f"- {item}" for item in section.bullets],
        "",
        "Evidence refs:",
        *[f"- `{ref}`" for ref in section.evidence_refs],
        "",
    ]
    return lines
