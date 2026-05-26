"""Paper workflow public namespace facade."""

from turing_research_paper.public_api import (
    COMPATIBILITY_NAMESPACE,
    NAMESPACE,
    PUBLIC_MODULE_ALIASES,
    STABILITY,
    DeepReviewReport,
    PaperDigest,
    PaperMethodCard,
    PaperScaffold,
    RelatedWorkDraftSkeleton,
    build_paper_digest,
    build_vggt_paper_scaffold,
)

__all__ = [
    "COMPATIBILITY_NAMESPACE",
    "NAMESPACE",
    "PUBLIC_MODULE_ALIASES",
    "STABILITY",
    "DeepReviewReport",
    "PaperDigest",
    "PaperMethodCard",
    "PaperScaffold",
    "RelatedWorkDraftSkeleton",
    "build_paper_digest",
    "build_vggt_paper_scaffold",
]
