# Scholar Pipeline Public README Section

Status: v1.4 README parity draft.

Round: 301.

Use this section when describing the Scholar pipeline in public README-style
material.

## Scholar Pipeline

TuringResearch exposes a fake/default Scholar pipeline for paper discovery,
cached paper content review, reference review, and three-pass reading plans.
It is designed for local review and demos, not automatic literature claims.

### Tools

- `scholar.paper_searching`: cache-first paper lookup.
- `scholar.paper_content`: read local cached Markdown paper content.
- `scholar.paper_reference`: resolve references through fake/default, cached,
  or manual fallback.
- `scholar.paper_reading`: build a three-pass reading plan.

### Fake Mode

Fake mode is the default and requires no API key. Public tests and demos use:

- `examples/scholar_demo/fake_paper_search.json`
- `examples/scholar_demo/fake_paper_content.md`
- `examples/scholar_demo/fake_reference_report.md`

### Live Mode

Live mode is private opt-in only. It requires explicit local environment
configuration and human review. It is not required for public demos or tests.

### What It Does Not Do

- It does not download full papers automatically.
- It does not bypass paywalls.
- It does not run MinerU or heavy OCR.
- It does not create final paper conclusions.
- It does not mark fake citations as verified.
