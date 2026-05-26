"""Non-destructive redaction proposal helpers."""

from __future__ import annotations

import re

from turing_research_plus.privacy.models import (
    PrivacyFindingType,
    PrivacyPolicyRule,
    RedactionProposal,
)


def propose_redaction(
    path: str,
    text: str,
    rule: PrivacyPolicyRule,
) -> RedactionProposal | None:
    """Return a redaction proposal without modifying the source text."""

    if not rule.redaction_possible:
        return None

    redacted = text
    for pattern in rule.content_patterns:
        redacted = re.sub(pattern, "[REDACTED]", redacted)

    if redacted == text:
        redacted = _fallback_redaction(text, rule.finding_type)

    return RedactionProposal(
        path=path,
        finding_type=rule.finding_type,
        replacement="[REDACTED]",
        proposed_text=redacted,
        destructive=False,
    )


def redact_text(text: str, rules: list[PrivacyPolicyRule]) -> str:
    """Return redacted text for preview only."""

    redacted = text
    for rule in rules:
        if not rule.redaction_possible:
            continue
        for pattern in rule.content_patterns:
            redacted = re.sub(pattern, "[REDACTED]", redacted)
    return redacted


def _fallback_redaction(text: str, finding_type: PrivacyFindingType) -> str:
    if finding_type == PrivacyFindingType.PERSONAL_PATH:
        return "[REDACTED_PATH]"
    return text.replace(text.strip(), "[REDACTED]", 1)
