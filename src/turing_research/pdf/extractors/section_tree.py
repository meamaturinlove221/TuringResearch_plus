"""Lightweight section tree extraction for local PDFs."""

from __future__ import annotations

from pathlib import Path

from turing_research.pdf.asset_report import PDFSectionNode

KNOWN_HEADINGS = {
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


def extract_section_tree(pdf_path: Path) -> tuple[list[PDFSectionNode], list[str]]:
    """Extract a simple heading-based section tree."""

    try:
        import fitz  # type: ignore[import-untyped]
    except ModuleNotFoundError:
        return [], ["PyMuPDF is not installed; section tree extraction skipped."]

    nodes: list[PDFSectionNode] = []
    warnings: list[str] = []
    try:
        document = fitz.open(str(pdf_path))
    except Exception as exc:
        return [], [f"Could not open PDF for section tree extraction: {exc}"]

    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text") or ""
            for line in text.splitlines():
                stripped = line.strip()
                if not _looks_like_heading(stripped):
                    continue
                section_id = f"sec-{len(nodes) + 1}"
                nodes.append(
                    PDFSectionNode(
                        section_id=section_id,
                        title=stripped.rstrip(":"),
                        level=1,
                        page_start=page_number,
                        page_end=page_number,
                        parent_section_id=None,
                        child_section_ids=[],
                        evidence_locator=f"page:{page_number}",
                        confidence=0.75 if stripped.lower().rstrip(":") in KNOWN_HEADINGS else 0.55,
                    )
                )
    finally:
        document.close()

    if not nodes:
        warnings.append("No confident section headings detected.")
    return nodes, warnings


def _looks_like_heading(line: str) -> bool:
    if not line or len(line) > 120:
        return False
    normalized = line.rstrip(":").lower()
    if normalized in KNOWN_HEADINGS:
        return True
    words = line.split()
    return len(words) <= 8 and line.isupper() and any(char.isalpha() for char in line)
