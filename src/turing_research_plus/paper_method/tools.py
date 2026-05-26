"""Capsule-local tool wrapper for Paper-to-Method Card."""

from __future__ import annotations

from typing import Any

from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import PaperMethodCardInput


def paper_method_card_extract(request: PaperMethodCardInput) -> dict[str, Any]:
    """Extract a method card and return JSON-safe data."""

    return extract_paper_method_card(request).model_dump(mode="json")
