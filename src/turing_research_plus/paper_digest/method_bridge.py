"""Bridge PaperDigest objects into PaperMethodCard extraction."""

from __future__ import annotations

from turing_research_plus.paper_digest.markdown_export import export_paper_digest_markdown
from turing_research_plus.paper_digest.models import PaperDigest
from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import (
    PaperMethodCard,
    PaperMethodCardInput,
    PaperSourceType,
)


def digest_to_method_card(digest: PaperDigest) -> PaperMethodCard:
    """Convert a PaperDigest into a conservative PaperMethodCard."""

    return extract_paper_method_card(
        PaperMethodCardInput(
            paper_id=digest.paper_id,
            title=digest.title,
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_text=export_paper_digest_markdown(digest),
            requires_real_paper_review=True,
        )
    )
