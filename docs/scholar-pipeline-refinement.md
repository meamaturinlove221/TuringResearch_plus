# Scholar Pipeline Refinement

Status: v0.3 Sprint 2 minimal implementation.

This refinement gives TuringResearch Plus a clearer cache-first paper pipeline
without changing the default no-network behavior.

## Source Priority

1. Existing cached Markdown
2. arXiv metadata or known arXiv URL
3. Semantic Scholar lookup
4. Unpaywall optional placeholder
5. Manual fallback

The current implementation uses local cached Markdown, known arXiv URLs, and
fake adapters by default. Live adapters remain optional and disabled unless a
future live round explicitly enables them.

## Reference Priority

1. Semantic Scholar references when a paper id exists
2. Cached Markdown references section
3. Manual reference list
4. Unknown / requires human review

The Semantic Scholar path uses the existing fake/live adapter surface. Pagination
is recorded when the requested reference limit is filled, but default tests use
fake adapters only.

## Cached Paper Content

`paper.search_pipeline` can read existing local Markdown and return a
`CachedPaperContent` object. Cached Markdown is treated as useful context, not
as human-verified paper review.

## Three-Pass Reading

The pipeline includes a Keshav-style reading plan:

- Pass 1: bird's-eye scan
- Pass 2: content grasp
- Pass 3: deep understanding

Expected outputs are a method card, collision notes, borrow/not-copy list, and
VGGT mapping. These outputs still require real paper review.

## VGGT Use

For VGGT / SMPL-X work, the refined pipeline connects:

`cached paper note -> three-pass plan -> PaperMethodCard -> CollisionRiskReport`

This is a review scaffold. It is not complete related work, not a definitive
collision finding, and not a claim that the paper has been fully read.

## Non-Goals

- No default network access.
- No copyrighted full-text download.
- No MinerU implementation.
- No OCR-heavy pipeline.
- No copied upstream code.
- No fake reading marked as human verified.
