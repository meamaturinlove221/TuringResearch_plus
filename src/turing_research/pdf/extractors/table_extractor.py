"""Lightweight table extraction for local PDFs."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from turing_research.pdf.asset_report import PDFExtractedTable, PDFExtractionStatus


def extract_tables(
    pdf_path: Path,
    output_dir: Path | None = None,
) -> tuple[list[PDFExtractedTable], list[str]]:
    """Extract simple text tables from local PDFs.

    This Phase B path intentionally avoids OCR and layout-heavy table models. It
    recognizes pipe-delimited text tables first, then simple tab-delimited rows.
    """

    try:
        import fitz  # type: ignore[import-untyped]
    except ModuleNotFoundError:
        return [], ["PyMuPDF is not installed; table extraction skipped."]

    tables: list[PDFExtractedTable] = []
    warnings: list[str] = []
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)

    try:
        document = fitz.open(str(pdf_path))
    except Exception as exc:
        return [], [f"Could not open PDF for table extraction: {exc}"]

    source_hash = _source_hash(pdf_path)
    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text") or ""
            page_tables = _tables_from_text(text)
            for table_index, markdown_table in enumerate(page_tables, start=1):
                table_id = f"table-{source_hash}-p{page_number}-{table_index}"
                output_path = None
                if output_dir is not None:
                    output_path = output_dir / f"{table_id}.md"
                    output_path.write_text(markdown_table + "\n", encoding="utf-8")
                tables.append(
                    PDFExtractedTable(
                        table_id=table_id,
                        source_pdf=pdf_path,
                        page_number=page_number,
                        extraction_format="markdown_table",
                        output_path=output_path,
                        markdown_table=markdown_table,
                        extraction_status=PDFExtractionStatus.EXTRACTED,
                        warnings=[],
                    )
                )
    finally:
        document.close()

    if not tables:
        warnings.append("No lightweight text tables were found.")
    return tables, warnings


def _tables_from_text(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    tables: list[str] = []
    current: list[str] = []
    for line in lines:
        if "|" in line and line.count("|") >= 2:
            current.append(_normalize_pipe_row(line))
            continue
        if "\t" in line:
            current.append("| " + " | ".join(part.strip() for part in line.split("\t")) + " |")
            continue
        if len(current) >= 2:
            tables.append(_with_separator(current))
        current = []
    if len(current) >= 2:
        tables.append(_with_separator(current))
    return tables


def _normalize_pipe_row(line: str) -> str:
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    return "| " + " | ".join(cells) + " |"


def _with_separator(rows: list[str]) -> str:
    if len(rows) >= 2 and set(rows[1].replace("|", "").strip()) <= {"-", ":", " "}:
        return "\n".join(rows)
    cell_count = max(rows[0].count("|") - 1, 1)
    separator = "| " + " | ".join(["---"] * cell_count) + " |"
    return "\n".join([rows[0], separator, *rows[1:]])


def _source_hash(pdf_path: Path) -> str:
    return sha256(str(pdf_path.resolve()).encode("utf-8")).hexdigest()[:10]
