from __future__ import annotations

from turing_research_plus.privacy.models import PrivacyFindingType
from turing_research_plus.privacy.policy import default_privacy_policy
from turing_research_plus.privacy.redaction import propose_redaction, redact_text


def test_redaction_proposal_is_preview_only() -> None:
    token_rule = next(
        rule
        for rule in default_privacy_policy()
        if rule.finding_type == PrivacyFindingType.TOKEN_PATTERN
    )
    proposal = propose_redaction("notes.md", "access_token=abcdefghi123", token_rule)

    assert proposal is not None
    assert proposal.destructive is False
    assert "[REDACTED]" in (proposal.proposed_text or "")


def test_redact_text_redacts_personal_path_preview() -> None:
    redacted = redact_text(
        "path C:\\Users\\researcher\\project",
        default_privacy_policy(),
    )

    assert "[REDACTED]" in redacted
