from __future__ import annotations

from turing_research_plus.privacy.models import PrivacyFindingType, SafetyLevel
from turing_research_plus.privacy.policy import default_privacy_policy


def test_default_privacy_policy_covers_required_findings() -> None:
    rules = default_privacy_policy()
    finding_types = {rule.finding_type for rule in rules}

    assert PrivacyFindingType.ENV_FILE in finding_types
    assert PrivacyFindingType.API_KEY_PATTERN in finding_types
    assert PrivacyFindingType.TOKEN_PATTERN in finding_types
    assert PrivacyFindingType.PRIVATE_DATA_PATH in finding_types
    assert PrivacyFindingType.LOCAL_PROJECT_LINKS in finding_types
    assert PrivacyFindingType.RAW_DATA in finding_types
    assert PrivacyFindingType.SMPLX_MODEL_FILE in finding_types
    assert PrivacyFindingType.HUGE_NPZ in finding_types
    assert PrivacyFindingType.PERSONAL_PATH in finding_types
    assert PrivacyFindingType.PRIVATE_ADVISOR_FEEDBACK in finding_types
    assert PrivacyFindingType.LICENSED_MODEL_FILE in finding_types
    assert any(rule.safety_level == SafetyLevel.SECRET_FORBIDDEN for rule in rules)


def test_secret_policy_rules_are_release_blockers() -> None:
    rules = default_privacy_policy()
    secret_rules = [rule for rule in rules if rule.safety_level == SafetyLevel.SECRET_FORBIDDEN]

    assert secret_rules
    assert all(rule.release_blocker for rule in secret_rules)
