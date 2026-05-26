# Cached Paper Content Policy

Status: v0.3 Sprint 2 minimal policy.

Cached paper content means local Markdown that already exists in the workspace.
TuringResearch Plus may read it for dry-run workflows, but it must not download
copyrighted full text by default.

## Rules

- Cached Markdown has the highest source priority.
- Cached Markdown is not automatically human verified.
- A cached references section can be used as fallback when provider references
  are unavailable.
- Missing cached content falls through to arXiv metadata, Semantic Scholar fake
  lookup, Unpaywall placeholder, or manual fallback.
- Live retrieval remains optional and disabled by default.

## Forbidden Defaults

- No copyrighted full-text download.
- No OCR-heavy pipeline.
- No MinerU execution.
- No fake reading marked as human verified.

## Review Boundary

Cached content can seed a `PaperMethodCard`, collision notes, and VGGT mapping,
but those outputs remain `requires_human_review` until a person confirms the
paper evidence.
