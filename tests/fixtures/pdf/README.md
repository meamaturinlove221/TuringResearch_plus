# TuringResearch Plus PDF Fixtures

This directory is reserved for tiny local PDF fixtures used by PDF Markdown tests.

## Fixture Rules

- Use only generated, public-domain, or clearly authorized PDFs.
- Do not store private papers.
- Do not store restricted datasets.
- Do not store large publisher PDFs.
- Keep fixtures small enough for fast local tests.
- Do not require network access.
- Do not require OCR services.

## Planned Phase B Fixture Types

- Text-only PDF for Phase A regression.
- Simple figure PDF for `pdf.extract_figures`.
- Simple table PDF for `pdf.extract_tables`.
- Heading hierarchy PDF for `pdf.sectionize`.
- Empty or low-text PDF for quality warning tests.

## Expected Metadata

Each fixture should document:

- fixture purpose
- creation method
- license or ownership status
- expected pages
- expected figures
- expected tables
- expected section headings

## Current Status

Round 33 creates the fixture policy only. It does not add new PDF binaries.
