"""Minimal PDF Markdown quality scoring."""

from __future__ import annotations


def score_markdown(markdown: str, warnings: list[str]) -> float:
    """Return a small deterministic quality score for extracted Markdown."""

    if not markdown.strip():
        return 0.0
    score = 1.0
    score -= min(len(warnings) * 0.1, 0.7)
    if len(markdown.strip()) < 50:
        score -= 0.2
    return max(0.0, round(score, 3))
