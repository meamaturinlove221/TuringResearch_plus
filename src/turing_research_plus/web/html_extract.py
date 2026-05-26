"""Small HTML extraction helpers.

This is intentionally lightweight and does not try to be a full readability
engine.
"""

from __future__ import annotations

import re
from html import unescape

TITLE_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
SCRIPT_STYLE_PATTERN = re.compile(
    r"<(script|style)[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL
)
TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")


def extract_title(html: str) -> str | None:
    """Extract a simple title from HTML."""

    match = TITLE_PATTERN.search(html)
    if match is None:
        return None
    title = normalize_text(match.group(1))
    return title or None


def html_to_text(html: str) -> str:
    """Convert HTML to compact plain text for review fixtures."""

    no_scripts = SCRIPT_STYLE_PATTERN.sub(" ", html)
    with_breaks = re.sub(r"</(p|div|section|article|h[1-6]|li)>", "\n", no_scripts, flags=re.I)
    text = TAG_PATTERN.sub(" ", with_breaks)
    return normalize_text(unescape(text))


def normalize_text(text: str) -> str:
    """Normalize whitespace."""

    return SPACE_PATTERN.sub(" ", text).strip()
