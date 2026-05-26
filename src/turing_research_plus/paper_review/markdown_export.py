"""Markdown export for paper deep review reports."""

from __future__ import annotations

from turing_research_plus.paper_review.models import DeepReviewItem, DeepReviewReport


def render_deep_review_report_markdown(report: DeepReviewReport) -> str:
    """Render a deep review report as Markdown."""

    lines = [
        f"# Paper Deep Review: {report.title}",
        "",
        "## Paper Identity",
        "",
        f"- Paper ID: `{report.paper_id}`",
        f"- Source status: `{report.source_status}`",
        f"- Reading status: `{report.reading_status}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Figures To Inspect",
        "",
        *_render_items(report.figures_to_inspect),
        "",
        "## Equations To Inspect",
        "",
        *_render_items(report.equations_to_inspect),
        "",
        "## Tables To Inspect",
        "",
        *_render_items(report.tables_to_inspect),
        "",
        "## Implementation Questions",
        "",
        *_render_items(report.implementation_questions),
        "",
        "## Reproduction Blockers",
        "",
        *_render_items(report.reproduction_blockers),
        "",
        "## Relation To Our Project",
        "",
        *_bullets(report.relation_to_our_project),
        "",
        "## Claims Requiring Verification",
        "",
        *_render_items(report.claims_requiring_verification),
        "",
        "## Notes For Advisor",
        "",
        *_render_items(report.notes_for_advisor),
        "",
        "## Limitations",
        "",
        *_bullets(report.limitations),
        "",
        "## Boundary",
        "",
        "- This is not a claim of completed real deep reading.",
        "- No long paper text is copied.",
        "- No equation is fabricated.",
        "- No PDF is downloaded.",
        "- No final paper conclusion is generated.",
        "",
    ]
    return "\n".join(lines)


def _render_items(items: list[DeepReviewItem]) -> list[str]:
    if not items:
        return ["- none"]
    return [
        "- "
        f"`{item.item_id}` {item.description} "
        f"(kind: `{item.kind}`, source_status: `{item.source_status}`, "
        f"status: `{item.status}`, "
        f"requires_human_review: `{str(item.requires_human_review).lower()}`)"
        for item in items
    ]


def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] or ["- none"]
