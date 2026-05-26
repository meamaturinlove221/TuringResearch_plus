"""Default privacy and data policy rules."""

from __future__ import annotations

from turing_research_plus.privacy.models import (
    PrivacyFindingType,
    PrivacyPolicyRule,
    PrivacySeverity,
    SafetyLevel,
)

DEFAULT_HUGE_NPZ_BYTES = 5_000_000


def default_privacy_policy() -> list[PrivacyPolicyRule]:
    """Return conservative default privacy rules."""

    return [
        PrivacyPolicyRule(
            rule_id="env-file",
            finding_type=PrivacyFindingType.ENV_FILE,
            description="Environment files can contain secrets.",
            safety_level=SafetyLevel.SECRET_FORBIDDEN,
            severity=PrivacySeverity.CRITICAL,
            recommended_action="Remove .env files from shareable outputs.",
            release_blocker=True,
            path_patterns=[r"(^|/)\.env$"],
        ),
        PrivacyPolicyRule(
            rule_id="api-key-pattern",
            finding_type=PrivacyFindingType.API_KEY_PATTERN,
            description="Provider API key-like text.",
            safety_level=SafetyLevel.SECRET_FORBIDDEN,
            severity=PrivacySeverity.CRITICAL,
            recommended_action="Remove or redact API keys before export.",
            redaction_possible=True,
            release_blocker=True,
            content_patterns=[
                r"sk-[A-Za-z0-9_-]{8,}",
                r"ghp_[A-Za-z0-9_]{8,}",
            ],
        ),
        PrivacyPolicyRule(
            rule_id="token-pattern",
            finding_type=PrivacyFindingType.TOKEN_PATTERN,
            description="Token-like text or token variable assignment.",
            safety_level=SafetyLevel.SECRET_FORBIDDEN,
            severity=PrivacySeverity.HIGH,
            recommended_action="Review and redact token-like values.",
            redaction_possible=True,
            release_blocker=True,
            content_patterns=[
                r"xox[baprs]-[A-Za-z0-9-]+",
                r"(?i)[A-Z0-9_]*TOKEN\s*[:=]\s*[A-Za-z0-9_-]{8,}",
                r"(?i)(api[_-]?token|access[_-]?token)\s*[:=]\s*[A-Za-z0-9_-]{8,}",
            ],
        ),
        PrivacyPolicyRule(
            rule_id="private-data-path",
            finding_type=PrivacyFindingType.PRIVATE_DATA_PATH,
            description="Path suggests private data.",
            safety_level=SafetyLevel.PRIVATE_RESEARCH,
            severity=PrivacySeverity.HIGH,
            recommended_action="Omit private_data paths from public or handoff bundles.",
            release_blocker=True,
            path_patterns=[r"(^|/)private_data(/|$)", r"(^|/)secrets(/|$)"],
        ),
        PrivacyPolicyRule(
            rule_id="local-project-links",
            finding_type=PrivacyFindingType.LOCAL_PROJECT_LINKS,
            description="Local project link files can reveal private paths.",
            safety_level=SafetyLevel.PRIVATE_RESEARCH,
            severity=PrivacySeverity.HIGH,
            recommended_action="Do not include local_project_links.yaml in exports.",
            release_blocker=True,
            path_patterns=[r"(^|/)local_project_links\.yaml$"],
        ),
        PrivacyPolicyRule(
            rule_id="raw-data",
            finding_type=PrivacyFindingType.RAW_DATA,
            description="Raw data should not be included by default.",
            safety_level=SafetyLevel.RESTRICTED_DATA,
            severity=PrivacySeverity.HIGH,
            recommended_action="Omit raw data and include metadata-only references.",
            release_blocker=True,
            path_patterns=[r"(^|/)raw[_-]?data(/|$)", r"(^|/)raw(/|$)"],
            content_patterns=[
                r"(?i)\braw data\s*[:=]",
                r"(?i)\braw dataset\s*[:=]",
                r"(?i)\braw data path\b",
                r"(?i)\braw dataset path\b",
            ],
        ),
        PrivacyPolicyRule(
            rule_id="smplx-model-file",
            finding_type=PrivacyFindingType.SMPLX_MODEL_FILE,
            description="SMPL-X body model files are licensed/private model files.",
            safety_level=SafetyLevel.RESTRICTED_DATA,
            severity=PrivacySeverity.CRITICAL,
            recommended_action="Do not include SMPL-X model files.",
            release_blocker=True,
            path_patterns=[r"(^|/)SMPLX_[^/]+\.(npz|pkl)$"],
        ),
        PrivacyPolicyRule(
            rule_id="huge-npz",
            finding_type=PrivacyFindingType.HUGE_NPZ,
            description="Large npz payloads should be metadata-only.",
            safety_level=SafetyLevel.PRIVATE_RESEARCH,
            severity=PrivacySeverity.MEDIUM,
            recommended_action="Replace huge npz payloads with metadata and sha256.",
            release_blocker=True,
            path_patterns=[r"\.npz$"],
            max_size_bytes=DEFAULT_HUGE_NPZ_BYTES,
        ),
        PrivacyPolicyRule(
            rule_id="personal-path",
            finding_type=PrivacyFindingType.PERSONAL_PATH,
            description="Personal local path detected.",
            safety_level=SafetyLevel.PRIVATE_RESEARCH,
            severity=PrivacySeverity.MEDIUM,
            recommended_action="Replace personal paths with relative or workspace-safe refs.",
            redaction_possible=True,
            content_patterns=[r"[A-Za-z]:\\Users\\[^\\\s]+", r"/home/[^/\s]+"],
        ),
        PrivacyPolicyRule(
            rule_id="private-advisor-feedback",
            finding_type=PrivacyFindingType.PRIVATE_ADVISOR_FEEDBACK,
            description="Private advisor feedback should not be public by default.",
            safety_level=SafetyLevel.PRIVATE_RESEARCH,
            severity=PrivacySeverity.MEDIUM,
            recommended_action="Move private advisor feedback to reviewed internal notes.",
            redaction_possible=True,
            content_patterns=[r"(?i)private advisor feedback", r"(?i)advisor confidential"],
        ),
        PrivacyPolicyRule(
            rule_id="licensed-model-file",
            finding_type=PrivacyFindingType.LICENSED_MODEL_FILE,
            description="Licensed model payload file.",
            safety_level=SafetyLevel.RESTRICTED_DATA,
            severity=PrivacySeverity.HIGH,
            recommended_action="Omit licensed model files from export.",
            release_blocker=True,
            path_patterns=[
                r"(?i)(licensed|body_model|model_files?)/",
                r"(?i)\.(ckpt|safetensors|onnx|pt|pth)$",
            ],
        ),
    ]
