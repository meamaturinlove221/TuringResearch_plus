"""Public API facade for paper workflow modules."""

from turing_research_plus.paper_digest import PaperDigest, build_paper_digest
from turing_research_plus.paper_method import PaperMethodCard
from turing_research_plus.paper_review import DeepReviewReport
from turing_research_plus.paper_write import (
    PaperScaffold,
    RelatedWorkDraftSkeleton,
    build_vggt_paper_scaffold,
)

NAMESPACE = "turing_research_paper"
COMPATIBILITY_NAMESPACE = "turing_research_plus"
STABILITY = "experimental"
PUBLIC_MODULE_ALIASES = {
    "paper_digest": "turing_research_plus.paper_digest",
    "paper_method": "turing_research_plus.paper_method",
    "paper_review": "turing_research_plus.paper_review",
    "paper_write": "turing_research_plus.paper_write",
}

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
