"""Simple section heading detection for PDF text."""

from __future__ import annotations


def _looks_like_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) > 120:
        return False
    if stripped.startswith(("#", "-", "*")):
        return False
    words = stripped.split()
    if len(words) > 12:
        return False
    known = {
        "abstract",
        "introduction",
        "background",
        "methods",
        "method",
        "results",
        "discussion",
        "conclusion",
        "references",
    }
    normalized = stripped.rstrip(":").lower()
    if normalized in known:
        return True
    return stripped.isupper() and any(char.isalpha() for char in stripped)


def sectionize_text(text: str) -> str:
    """Apply simple Markdown headings to likely section headings."""

    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if _looks_like_heading(stripped):
            lines.append(f"## {stripped.rstrip(':')}")
        else:
            lines.append(line.rstrip())
    return "\n".join(lines).strip()
