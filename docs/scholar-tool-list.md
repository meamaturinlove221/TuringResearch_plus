# Scholar Tool List

Status: v1.2 public tool list.

Round: 237.

The Scholar pipeline exposes review-oriented tools. They are fake/default and
do not require real API keys.

| Tool | Purpose | Default mode | Human review |
| --- | --- | --- | --- |
| `paper.search_pipeline` | Cache-first paper lookup using cached Markdown, arXiv metadata, fake adapters, or manual fallback. | fake/default | required |
| `paper.reference_pipeline` | Resolve references from fake Semantic Scholar, cached Markdown, or manual lists. | fake/default | required |
| `paper.three_pass_reading_plan` | Build a Keshav-style reading checklist. | local scaffold | required |
| `paper.digest` | Turn fixture or cached notes into a review-only paper digest. | local scaffold | required |

## Safety

- No automatic full paper download.
- No paywall bypass.
- No heavy OCR.
- No final paper conclusion.
- Live tests are skipped by default.
