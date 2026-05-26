"""Default failure taxonomy."""

from __future__ import annotations

from turing_research_plus.failure.models import (
    FailureCategory,
    FailureSeverity,
    FailureTaxonomyEntry,
    RetryPolicy,
)


def default_failure_taxonomy() -> dict[FailureCategory, FailureTaxonomyEntry]:
    """Return deterministic failure taxonomy entries."""

    return {
        FailureCategory.FAST_RETURN: _entry(
            FailureCategory.FAST_RETURN,
            FailureSeverity.HIGH,
            "Route returned too quickly to support real experiment evidence.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Disable fast-return path and collect artifact-backed evidence."],
        ),
        FailureCategory.REPORT_ONLY: _entry(
            FailureCategory.REPORT_ONLY,
            FailureSeverity.HIGH,
            "Output contains a report but no supporting artifacts.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Require candidate predictions, boards, and artifact checks."],
        ),
        FailureCategory.IDENTITY_COPY: _entry(
            FailureCategory.IDENTITY_COPY,
            FailureSeverity.HIGH,
            "Route may have copied identity behavior without real transformation.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Add diff evidence and identity-copy checks."],
        ),
        FailureCategory.FALLBACK_ONLY: _entry(
            FailureCategory.FALLBACK_ONLY,
            FailureSeverity.HIGH,
            "Only fallback output is available.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Separate fallback output from promotable experiment output."],
        ),
        FailureCategory.REAL_BACKEND_UNAVAILABLE: _entry(
            FailureCategory.REAL_BACKEND_UNAVAILABLE,
            FailureSeverity.CRITICAL,
            "Required real backend is unavailable.",
            RetryPolicy.REQUIRES_REAL_EXPERIMENT,
            ["Provision or verify the real backend before retry."],
        ),
        FailureCategory.MISSING_ASSETS: _entry(
            FailureCategory.MISSING_ASSETS,
            FailureSeverity.HIGH,
            "Required assets are missing.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Collect adjacent predictions, semantic assets, and manifest entries."],
        ),
        FailureCategory.VISUAL_PROOF_INSUFFICIENT: _entry(
            FailureCategory.VISUAL_PROOF_INSUFFICIENT,
            FailureSeverity.HIGH,
            "Visual proof is insufficient for advisor-ready claims.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Collect full body, hairline, and hand close-up boards."],
        ),
        FailureCategory.FULL_BODY_REGRESSION: _entry(
            FailureCategory.FULL_BODY_REGRESSION,
            FailureSeverity.HIGH,
            "Full-body visual regression is unresolved.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Collect comparable full-body before/after evidence."],
        ),
        FailureCategory.HAIRLINE_REGRESSION: _entry(
            FailureCategory.HAIRLINE_REGRESSION,
            FailureSeverity.MEDIUM,
            "Hairline degradation is unresolved.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Add hairline close-up evidence and compare against baseline."],
        ),
        FailureCategory.HAND_OBJECT_CONFUSION: _entry(
            FailureCategory.HAND_OBJECT_CONFUSION,
            FailureSeverity.MEDIUM,
            "Hand/object confusion is unresolved.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Add hand-object close-up checks."],
        ),
        FailureCategory.DEPTH_POINT_SCHEMA_MISMATCH: _entry(
            FailureCategory.DEPTH_POINT_SCHEMA_MISMATCH,
            FailureSeverity.HIGH,
            "Depth or point schema does not match route expectations.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Align schema and rerun validation before experiment."],
        ),
        FailureCategory.PACKAGE_INCOMPLETE: _entry(
            FailureCategory.PACKAGE_INCOMPLETE,
            FailureSeverity.HIGH,
            "Artifact package is incomplete.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Rebuild package and rerun zip test."],
        ),
        FailureCategory.SPARSE_BACKEND_UNAVAILABLE: _entry(
            FailureCategory.SPARSE_BACKEND_UNAVAILABLE,
            FailureSeverity.CRITICAL,
            "Sparse backend is unavailable.",
            RetryPolicy.REQUIRES_REAL_EXPERIMENT,
            ["Run sparse backend probe on a real backend."],
        ),
        FailureCategory.SMPLX_ALIGNMENT_WEAK: _entry(
            FailureCategory.SMPLX_ALIGNMENT_WEAK,
            FailureSeverity.MEDIUM,
            "SMPL-X alignment evidence is weak.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Add alignment diagnostics and visual evidence."],
        ),
        FailureCategory.NOT_ENOUGH_EVIDENCE: _entry(
            FailureCategory.NOT_ENOUGH_EVIDENCE,
            FailureSeverity.HIGH,
            "Evidence is insufficient for a stronger claim.",
            RetryPolicy.REQUIRES_HUMAN_REVIEW,
            ["Keep claim unpromoted and collect evidence."],
        ),
        FailureCategory.PROMOTION_FORBIDDEN: _entry(
            FailureCategory.PROMOTION_FORBIDDEN,
            FailureSeverity.CRITICAL,
            "Promotion is forbidden by evidence state.",
            RetryPolicy.DO_NOT_RETRY,
            ["Do not promote until status changes with evidence."],
        ),
        FailureCategory.STRICT_REGISTRY_FORBIDDEN: _entry(
            FailureCategory.STRICT_REGISTRY_FORBIDDEN,
            FailureSeverity.HIGH,
            "Strict registry path is forbidden or invalid.",
            RetryPolicy.RETRY_AFTER_FIX,
            ["Remove strict registry dependency or document approval."],
        ),
        FailureCategory.HUMAN_REVIEW_REQUIRED: _entry(
            FailureCategory.HUMAN_REVIEW_REQUIRED,
            FailureSeverity.MEDIUM,
            "Human review is required.",
            RetryPolicy.REQUIRES_HUMAN_REVIEW,
            ["Request human review with evidence and limitations."],
        ),
    }


def _entry(
    category: FailureCategory,
    severity: FailureSeverity,
    description: str,
    retry_policy: RetryPolicy,
    next_actions: list[str],
) -> FailureTaxonomyEntry:
    return FailureTaxonomyEntry(
        category=category,
        severity=severity,
        description=description,
        default_retry_policy=retry_policy,
        default_next_actions=next_actions,
    )
