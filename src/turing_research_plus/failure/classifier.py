"""Rule-based failure classification."""

from __future__ import annotations

from turing_research_plus.failure.models import FailureCategory

KEYWORDS: list[tuple[FailureCategory, tuple[str, ...]]] = [
    (FailureCategory.FAST_RETURN, ("fast return", "fast-return")),
    (FailureCategory.REPORT_ONLY, ("report only", "report-only")),
    (FailureCategory.IDENTITY_COPY, ("identity copy", "identity-copy")),
    (FailureCategory.FALLBACK_ONLY, ("fallback only", "fallback-only")),
    (FailureCategory.REAL_BACKEND_UNAVAILABLE, ("real backend unavailable",)),
    (
        FailureCategory.SPARSE_BACKEND_UNAVAILABLE,
        ("sparse backend unavailable", "sparseconv3d backend unavailable"),
    ),
    (
        FailureCategory.MISSING_ASSETS,
        ("missing adjacent predictions", "missing semantic assets", "missing assets"),
    ),
    (FailureCategory.VISUAL_PROOF_INSUFFICIENT, ("missing board", "visual proof", "board proof")),
    (FailureCategory.FULL_BODY_REGRESSION, ("full body regression", "full-body regression")),
    (FailureCategory.HAIRLINE_REGRESSION, ("hairline",)),
    (FailureCategory.HAND_OBJECT_CONFUSION, ("hand object", "hand/object", "hand-object")),
    (FailureCategory.DEPTH_POINT_SCHEMA_MISMATCH, ("depth schema", "point schema")),
    (FailureCategory.PACKAGE_INCOMPLETE, ("package incomplete", "zip incomplete")),
    (FailureCategory.SMPLX_ALIGNMENT_WEAK, ("smplx alignment", "smpl-x alignment")),
    (FailureCategory.PROMOTION_FORBIDDEN, ("promotion forbidden", "no promotion")),
    (FailureCategory.STRICT_REGISTRY_FORBIDDEN, ("strict registry",)),
    (FailureCategory.HUMAN_REVIEW_REQUIRED, ("human review", "requires-human-review")),
    (FailureCategory.NOT_ENOUGH_EVIDENCE, ("not enough evidence", "no real experiment evidence")),
]


def classify_failure_text(text: str, hint: FailureCategory | None = None) -> FailureCategory:
    """Classify failure text conservatively."""

    if hint is not None:
        return hint
    normalized = text.lower()
    for category, patterns in KEYWORDS:
        if any(pattern in normalized for pattern in patterns):
            return category
    return FailureCategory.HUMAN_REVIEW_REQUIRED
