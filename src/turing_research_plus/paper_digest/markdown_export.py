"""Markdown export for PaperDigest objects."""

from __future__ import annotations

from turing_research_plus.paper_digest.models import PaperDigest


def export_paper_digest_markdown(digest: PaperDigest) -> str:
    """Render a PaperDigest as Markdown."""

    lines = [
        f"# Paper Digest: {digest.title}",
        "",
        f"- Paper ID: `{digest.paper_id}`",
        f"- Source status: `{digest.source_status.value}`",
        f"- Requires human review: `{str(digest.requires_human_review).lower()}`",
        f"- Requires real paper: `{str(digest.requires_real_paper).lower()}`",
        "",
        "## Pass 1 Summary",
        "",
        digest.pass1_summary,
        "",
        "## Pass 2 Notes",
        "",
        *_items(digest.pass2_notes),
        "",
        "## Pass 3 Deep Notes",
        "",
        *_items(digest.pass3_deep_notes),
        "",
        "## Method Contribution",
        "",
        digest.method_contribution,
        "",
        "## Figures To Inspect",
        "",
        *_items(digest.figures_to_inspect),
        "",
        "## Equations To Inspect",
        "",
        *_items(digest.equations_to_inspect),
        "",
        "## Experiment Table Notes",
        "",
        *_items(digest.experiment_table_notes),
        "",
        "## What To Borrow",
        "",
        *_items(digest.what_to_borrow),
        "",
        "## What Not To Copy",
        "",
        *_items(digest.what_not_to_copy),
        "",
        "## Collision Notes",
        "",
        *_items(digest.collision_notes),
        "",
        "## Related Work Positioning",
        "",
        *_items(digest.related_work_positioning),
        "",
        "## Limitations",
        "",
        *_items(digest.limitations),
        "",
        "## Boundary",
        "",
        "- Fixture digest is not a complete paper review.",
        "- No citation is fabricated by this digest.",
        "- Human review is required before paper claims.",
        "",
    ]
    return "\n".join(lines)


def _items(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- none recorded"]
