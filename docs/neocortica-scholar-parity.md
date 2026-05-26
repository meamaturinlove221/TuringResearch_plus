# Neocortica Scholar Parity

Status: v1.2 parity implementation.

Round: 237.

This round aligns TuringResearch with stable Scholar reference ideas: safe MCP
configuration, visible tool lists, paper source priority, cached Markdown
policy, reference fallback, usage guidance, and fake/live boundaries.

It does not implement MinerU, heavy OCR, automatic full paper download, paywall
bypass, or final paper conclusions.

## Implemented

- Scholar source priority plan.
- Scholar tool list export.
- Scholar MCP usage guide export.
- Paper source fallback policy.
- Contract and tests for fake/default behavior.

## Source Priority

1. Existing cached Markdown.
2. Known arXiv metadata or URL.
3. Semantic Scholar fake/live adapter surface.
4. Unpaywall placeholder for future review.
5. Manual fallback.

Cached Markdown is useful context, but it is not automatically human-verified
paper review.

## MCP Config Parity

The committed `.mcp.example.json` style remains:

- server name: `turingresearch-plus`;
- command: `turingresearch-plus-mcp`;
- fake/default mode;
- live tests disabled by default;
- Semantic Scholar live disabled by default;
- credential fields blank;
- plugin tools disabled by default.

## Live / Fake Boundary

Default tests use fake adapters and local fixtures. Live Scholar access requires
private local opt-in and human review. Live retrieved material is source
context, not final evidence or paper conclusions.

## Explicit Non-goals

- No MinerU runtime.
- No heavy OCR.
- No automatic full paper download.
- No paywall bypass.
- No final paper conclusion.
- No camera-ready paper text.

## Tests

- `tests/unit/test_scholar_source_priority.py`
- `tests/unit/test_scholar_tool_list_export.py`
- `tests/unit/test_scholar_mcp_usage_export.py`
- `tests/unit/test_scholar_fallback_policy.py`
- `tests/workflow/test_neocortica_scholar_parity_fake.py`
