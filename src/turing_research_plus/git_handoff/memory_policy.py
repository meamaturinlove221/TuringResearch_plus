"""Memory policy validation for context handoff."""

from __future__ import annotations

from turing_research_plus.git_handoff.models import MemoryPolicy
from turing_research_plus.git_handoff.safety import safety_warnings_for_text


def validate_memory_text(text: str, policy: MemoryPolicy | None = None) -> list[str]:
    """Validate MEMORY.md text and return policy warnings."""

    active_policy = policy or MemoryPolicy()
    warnings = safety_warnings_for_text(text)
    lowered = text.lower()
    if "memory is the only source of truth" in lowered:
        warnings.append("memory-cannot-be-only-source-of-truth")
    if "observed" in lowered and "evidence" not in lowered:
        warnings.append("observed-status-needs-evidence-reference")
    if active_policy.bidirectional_sync:
        warnings.append("bidirectional-memory-sync-disabled-by-policy")
    return list(dict.fromkeys(warnings))


def render_memory_policy(policy: MemoryPolicy | None = None) -> str:
    """Render the memory policy as Markdown."""

    active_policy = policy or MemoryPolicy()
    lines = [
        "# Memory Policy",
        "",
        "`MEMORY.md` is a handoff-safe summary, not the only source of truth.",
        "",
        "## Allowed Content",
        "",
        *[f"- {item}" for item in active_policy.allowed_content],
        "",
        "## Forbidden Content",
        "",
        *[f"- {item}" for item in active_policy.forbidden_content],
        "",
        "## Source of Truth",
        "",
        active_policy.source_of_truth,
        "",
        f"- Bidirectional sync: `{str(active_policy.bidirectional_sync).lower()}`",
        f"- Review required: `{str(active_policy.review_required).lower()}`",
    ]
    return "\n".join(lines) + "\n"
