"""Local helper wrappers for Paper Digest Engine."""

from __future__ import annotations

from turing_research_plus.paper_digest.digest_builder import build_paper_digest
from turing_research_plus.paper_digest.method_bridge import digest_to_method_card
from turing_research_plus.paper_digest.models import PaperDigest, PaperDigestInput
from turing_research_plus.paper_method.models import PaperMethodCard


def paper_digest_build(request: PaperDigestInput) -> PaperDigest:
    """Build a conservative paper digest."""

    return build_paper_digest(request)


def paper_digest_to_method_card(digest: PaperDigest) -> PaperMethodCard:
    """Convert a digest into a review-required method card."""

    return digest_to_method_card(digest)
