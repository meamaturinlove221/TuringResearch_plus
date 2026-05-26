"""Unsupported claim guard for public case study drafts."""

from __future__ import annotations

import re

from turing_research_plus.case_study.models import (
    CaseStudyClaimFinding,
    CaseStudyClaimSafetyReport,
)

BLOCKED_PATTERNS = [
    (
        re.compile(r"\bSparseConv3D\b.{0,80}\b(success|succeeded|successful)\b", re.IGNORECASE),
        "SparseConv3D success is not established by committed evidence.",
        "SparseConv3D remains planned / not-enough-evidence.",
    ),
    (
        re.compile(r"\bexperiment(?:s)?\b.{0,60}\b(success|succeeded|successful)\b", re.IGNORECASE),
        "Experiment success cannot be claimed without evidence ledger support.",
        "The case study describes workflow organization, not experiment success.",
    ),
    (
        re.compile(r"\b(planned route|route plan)\b.{0,80}\b(observed|executed)\b", re.IGNORECASE),
        "Planned routes must not be written as observed or executed.",
        "Planned routes remain planned until real run evidence exists.",
    ),
]


def guard_case_study_claims(text: str) -> CaseStudyClaimSafetyReport:
    """Find unsupported claims that must be blocked in public case studies."""

    findings: list[CaseStudyClaimFinding] = []
    for pattern, reason, replacement in BLOCKED_PATTERNS:
        for match in pattern.finditer(text):
            if _is_negated_boundary(text, match.start()):
                continue
            findings.append(
                CaseStudyClaimFinding(
                    claim=match.group(0),
                    reason=reason,
                    replacement=replacement,
                    severity="blocker",
                )
            )
    unsupported = [finding.claim for finding in findings]
    return CaseStudyClaimSafetyReport(
        findings=findings,
        unsupported_experiment_claims=unsupported,
        safe_to_publish=not findings,
    )


def _is_negated_boundary(text: str, start: int) -> bool:
    window = text[max(0, start - 40) : start].lower()
    return any(
        marker in window
        for marker in {
            "do not claim",
            "does not claim",
            "not claim",
            "no ",
            "without claiming",
        }
    )
