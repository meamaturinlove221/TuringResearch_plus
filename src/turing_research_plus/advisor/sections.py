"""Section rendering helpers for advisor packs."""

from __future__ import annotations

from turing_research_plus.advisor.models import AdvisorPack, AdvisorReadinessStatus


def render_current_status(pack: AdvisorPack) -> str:
    """Render current route and status for advisor review."""

    lines = [
        "# Current Status",
        "",
        pack.current_route_summary,
        "",
        "## What Changed Since Last Update",
        "",
    ]
    lines.extend(f"- {item}" for item in pack.what_changed_since_last_update)
    lines.extend(
        [
            "",
            "## Current Readiness",
            "",
            f"- Visual readiness: {pack.visual_readiness.value}",
        ]
    )
    return "\n".join(lines) + "\n"


def render_evidence_summary(pack: AdvisorPack) -> str:
    """Render evidence, limitations, and missing inputs."""

    lines = ["# Evidence Summary", "", "## Observed Evidence", ""]
    lines.extend(_bullets(pack.observed_evidence, "No observed evidence is available."))
    lines.extend(["", "## Limitations", ""])
    lines.extend(_bullets(pack.limitations, "No limitations recorded."))
    if pack.missing_inputs:
        lines.extend(["", "## Missing Inputs", ""])
        lines.extend(f"- `{item}`" for item in pack.missing_inputs)
    return "\n".join(lines) + "\n"


def render_visual_readiness(pack: AdvisorPack) -> str:
    """Render visual readiness gate details."""

    lines = [
        "# Visual Readiness",
        "",
        f"- Status: {pack.visual_readiness.value}",
        "",
        "## Required Human Review",
        "",
    ]
    lines.extend(_bullets(pack.required_human_review, "No human review item recorded."))
    lines.extend(["", "## Not-Ready Visual Claims", ""])
    lines.extend(_bullets(pack.not_ready_claims, "No not-ready claim recorded."))
    return "\n".join(lines) + "\n"


def render_failure_analysis(pack: AdvisorPack) -> str:
    """Render internal failure analysis."""

    lines = ["# Failure Analysis", "", "## Blockers", ""]
    lines.extend(_bullets(pack.blockers, "No blockers recorded."))
    lines.extend(["", "## Not-Ready Claims", ""])
    lines.extend(_bullets(pack.not_ready_claims, "No not-ready claims recorded."))
    lines.extend(["", "## Review Boundary", ""])
    lines.append("- Review-ready is not promotion and is not final advisor acceptance.")
    lines.append("- Planned work is not written as observed evidence.")
    return "\n".join(lines) + "\n"


def render_next_actions(pack: AdvisorPack) -> str:
    """Render actionable next steps."""

    lines = ["# Next Actions", ""]
    lines.extend(f"- {item}" for item in pack.next_actions)
    return "\n".join(lines) + "\n"


def readiness_from_visual_block(blocked: bool) -> AdvisorReadinessStatus:
    """Return visual readiness from a conservative visual gate."""

    return AdvisorReadinessStatus.BLOCKED if blocked else AdvisorReadinessStatus.READY_FOR_REVIEW


def _bullets(items: list[str], placeholder: str) -> list[str]:
    if not items:
        return [f"- {placeholder}"]
    return [f"- {item}" for item in items]
