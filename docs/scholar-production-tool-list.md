# Scholar Production Tool List

Status: v1.4 README parity draft.

Round: 301.

This document gives the public README-style Scholar tool list for production
parity. It mirrors the reference repo habit of showing the tool surface,
pipeline role, MCP status, and safety boundary in one place.

## Tool List

| Tool | Module | Pipeline role | Default mode | Live requirement |
| --- | --- | --- | --- | --- |
| `scholar.paper_searching` | `turing_research_plus.scholar_tools.paper_searching` | cache-first paper discovery | fake/default | none |
| `scholar.paper_content` | `turing_research_plus.scholar_tools.paper_content` | cached Markdown content review | local cached file | none |
| `scholar.paper_reference` | `turing_research_plus.scholar_tools.paper_reference` | reference fallback and review | fake/default | none |
| `scholar.paper_reading` | `turing_research_plus.scholar_tools.paper_reading` | three-pass reading plan | local scaffold | none |

## Pipeline

1. Prefer existing cached Markdown when available.
2. Use known arXiv metadata or URL when present.
3. Use fake/default Semantic Scholar adapter output for public tests.
4. Keep manual fallback available for unresolved references.
5. Produce review-only reading plans and reports.

## MCP Display

The committed `.mcp.example.json` keeps Scholar tools documentation-only:

- fake mode default;
- live tests disabled by default;
- Semantic Scholar live disabled by default;
- credential fields blank;
- MCP tool surface documented but not enabled by default.

## Safety Boundaries

- no MinerU;
- no heavy OCR;
- no automatic full paper download;
- no paywall bypass;
- no final paper conclusion;
- no camera-ready paper text;
- no fake citation is marked as verified;
- human review required.
