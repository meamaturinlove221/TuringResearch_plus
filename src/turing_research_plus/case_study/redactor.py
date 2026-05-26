"""Redaction helpers for public case study drafts."""

from __future__ import annotations

import re

from turing_research_plus.case_study.models import (
    CaseStudyRedaction,
    CaseStudyRedactionReport,
)

PRIVATE_PATH_PATTERN = re.compile(
    r"([A-Za-z]:[\\/][^\s)`]+|/home/[^\s)`]+|/Users/[^\s)`]+)"
)
RAW_DATA_PATTERN = re.compile(r"\b(raw data|raw dataset|predictions\.npz)\b", re.IGNORECASE)
MODEL_FILE_PATTERN = re.compile(r"\b(SMPL[-_]?X[^\\/\s]*\.(?:pkl|npz)|SMPLX_model\.pkl)\b")
PRIVATE_FEEDBACK_PATTERN = re.compile(r"\bprivate advisor feedback\b", re.IGNORECASE)


def redact_public_case_study_text(text: str) -> tuple[str, CaseStudyRedactionReport]:
    """Redact private paths, raw data markers, model files, and private feedback."""

    redactions: list[CaseStudyRedaction] = []
    sanitized = text
    sanitized = _replace_pattern(
        sanitized,
        PRIVATE_PATH_PATTERN,
        "[redacted-local-path]",
        "private-local-path",
        redactions,
    )
    sanitized = _replace_pattern(
        sanitized,
        RAW_DATA_PATTERN,
        "restricted data reference",
        "raw-data",
        redactions,
    )
    sanitized = _replace_pattern(
        sanitized,
        MODEL_FILE_PATTERN,
        "restricted model file reference",
        "model-file",
        redactions,
    )
    sanitized = _replace_pattern(
        sanitized,
        PRIVATE_FEEDBACK_PATTERN,
        "advisor review note",
        "private-advisor-feedback",
        redactions,
    )
    return sanitized, CaseStudyRedactionReport(redactions=redactions, sanitized=True)


def _replace_pattern(
    text: str,
    pattern: re.Pattern[str],
    replacement: str,
    finding_type: str,
    redactions: list[CaseStudyRedaction],
) -> str:
    def replace(match: re.Match[str]) -> str:
        redactions.append(
            CaseStudyRedaction(
                finding_type=finding_type,
                original_hint=_safe_hint(match.group(0)),
                replacement=replacement,
                applied=True,
            )
        )
        return replacement

    return pattern.sub(replace, text)


def _safe_hint(value: str) -> str:
    if len(value) <= 12:
        return value
    return value[:6] + "..." + value[-3:]
