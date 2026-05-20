# TulingResearch Plus PDF Markdown

Phase A implements the minimal local PDF to Markdown route for TulingResearch Plus. It supports local PDF paths, a replaceable PyMuPDF converter adapter, Markdown file output, simple section heading detection, local page maps, and CacheManager entries under the `pdf/markdown` namespace.

It does not include heavy OCR, complex layout understanding, paper fetching, paper search, fusion workflows, or external APIs in `v0.1.0`.

## Contract

The stable interface is described in `contracts/pdf_markdown.yaml`.

## Tools

- `pdf.inspect`: inspect a local PDF path and return page count, title, warnings, or a typed error.
- `pdf.to_markdown`: convert a local PDF path to Markdown and cache the `PDFMarkdownOutput`.
- `pdf.cache_lookup`: return cached `PDFMarkdownOutput` for a local PDF path.
- `pdf.markdown_content`: read cached Markdown text for a local PDF path.

## PDFMarkdownOutput

The conversion output includes:

- `title`
- `markdown_path`
- `markdown_chars`
- `converter_used`
- `assets`
- `page_map_path`
- `quality_score`
- `warnings`
- `cache_hit`

## Model Boundary

The Core model package is `tuling_research.pdf`. It describes:

- PDF source location or bytes reference.
- Conversion options.
- Per-page Markdown output.
- Conversion warnings and metadata.
- Phase A tool input and output models.

## Plus Integration

The Plus workflow layer wraps PDF Markdown outputs as `ResearchArtifact` records and attaches `EvidenceRef` entries where a conclusion is made from extracted content.

## Local Demo

The release example `examples/pdf-to-markdown-demo/` generates a tiny local fixture PDF, converts it to Markdown, reads the cached Markdown, and verifies cache-hit behavior. It does not require a large PDF, OCR service, or network access.
