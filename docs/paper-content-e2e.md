# Paper Content E2E

Status: fake/default workflow.

Round: 302.

This document describes the v1.4 paper content E2E path:

```text
paper id / URL / cached Markdown
-> scholar.paper_content
-> cached content extraction
-> PaperMethodCardInput
-> review-only method-card scaffold
```

The purpose is to make `paper_content` feel like a runnable tool surface instead
of a standalone helper. It remains local and conservative.

## Inputs

- `paper_id`: stable local paper identifier.
- `url`: public URL string used as context only.
- `cached_markdown_path`: local Markdown file already present in the repo or a
  private workspace.

## E2E Steps

1. Build a `PaperContentToolRequest`.
2. Run `scholar.paper_content`.
3. Confirm cache hit and references-section detection.
4. Use the cached Markdown path as `PaperMethodCardInput.source_path`.
5. Extract a review-only method-card scaffold.
6. Keep all claims human-reviewed and proposed-only.

## Demo Fixture

The public demo lives under:

```text
examples/scholar_demo/paper_content_e2e/
```

It contains cached Markdown, a method-card input descriptor, and a short E2E
report.

## Safety Boundary

- fake/default workflow only;
- no API key required;
- no automatic full paper download;
- no paywall bypass;
- no heavy OCR;
- no MinerU;
- no fake citation is marked as verified;
- no final paper conclusion;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_paper_content_e2e_fake.py -q
```
