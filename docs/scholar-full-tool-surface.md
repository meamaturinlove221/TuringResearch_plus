# Scholar Full Tool Surface

Status: implemented.

Round: 271.

This round adds an operator-facing Scholar tool surface for v1.3
Neocortica-Scholar parity. It wraps the existing fake/default Scholar pipeline
into stable tool entries that are easy to show, test, and document.

## Tool Surface

| Tool | Module | Purpose | Default |
| --- | --- | --- | --- |
| `scholar.paper_searching` | `turing_research_plus.scholar_tools.paper_searching` | Cache-first paper lookup | fake/default |
| `scholar.paper_content` | `turing_research_plus.scholar_tools.paper_content` | Read existing cached Markdown | local cached file |
| `scholar.paper_reference` | `turing_research_plus.scholar_tools.paper_reference` | Resolve references through fake/default, cached, or manual fallback | fake/default |
| `scholar.paper_reading` | `turing_research_plus.scholar_tools.paper_reading` | Build a three-pass reading plan | local scaffold |

## What It Adds

- A public `turing_research_plus.scholar_tools` package.
- Stable request/result models for the four Scholar tool entries.
- A `ScholarFullToolSurface` catalog for docs and tests.
- Fake/default workflow tests across search, content, references, and reading.

## Safety Boundary

- No MinerU.
- No heavy OCR.
- No automatic full paper download.
- No paywall bypass.
- No final paper conclusion.
- No camera-ready paper text.
- No real API key required.
- Live tests remain skipped by default.
- Cached Markdown and fake adapter outputs are review context, not final
  verified paper evidence.

## Relationship To Existing Scholar Pipeline

The new package is a thin tool surface over the existing Scholar pipeline:

- `paper_searching` reuses cache-first Scholar search.
- `paper_content` reuses cached Markdown reading.
- `paper_reference` reuses reference fallback resolution.
- `paper_reading` reuses the three-pass reading plan.

The goal is parity of usable tool entry points, not a new paper ingestion stack.

## Validation

Run:

```powershell
python -m pytest tests/unit/test_scholar_tool_surface.py tests/unit/test_paper_searching_tool.py tests/unit/test_paper_content_tool.py tests/unit/test_paper_reference_tool.py tests/unit/test_paper_reading_tool.py tests/workflow/test_scholar_full_tool_surface_fake.py -q
```
