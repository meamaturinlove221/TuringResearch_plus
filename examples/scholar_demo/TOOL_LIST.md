# Scholar Demo Tool List

Status: fake/demo only.

This is the public demo tool list for the Scholar production parity surface.
It is safe to show without provider keys.

| Tool | Demo input | Output | Status |
| --- | --- | --- | --- |
| `scholar.paper_searching` | `fake_paper_search.json` | fake search result | runnable fake/default |
| `scholar.paper_content` | `fake_paper_content.md` | cached Markdown review | runnable local |
| `scholar.paper_reference` | `fake_reference_report.md` | reference review report | runnable fake/default |
| `scholar.paper_reading` | cached Markdown | three-pass reading plan | runnable local |

## Pipeline

1. Search in fake/default mode.
2. Review cached Markdown.
3. Review references as fake/cached/manual context.
4. Build a three-pass reading plan.
5. Keep all outputs review-only.

## Safety

- fake mode default;
- no real API key required;
- no paper download;
- no paywall bypass;
- no fake citation is marked as verified;
- no final paper conclusion;
- human review required.
