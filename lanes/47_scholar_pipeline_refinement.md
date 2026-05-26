# Lane 47 - Scholar Pipeline Refinement

Status: completed minimal implementation.

## Scope

Round 66 refines the Scholar / Paper pipeline with source priority, references
fallback, cached Markdown policy, and a three-pass reading template.

## Implemented Surface

- `src/turing_research_plus/scholar_pipeline/`
- `contracts/scholar_pipeline.yaml`
- `docs/scholar-pipeline-refinement.md`
- `docs/paper-reading-three-pass.md`
- `docs/cached-paper-content-policy.md`
- `tests/unit/test_scholar_pipeline_models.py`
- `tests/unit/test_scholar_search_priority.py`
- `tests/unit/test_reference_pipeline_fallback.py`
- `tests/unit/test_cached_paper_content.py`
- `tests/unit/test_three_pass_reading_plan.py`
- `tests/workflow/test_vggt_scholar_pipeline_fake.py`

## Source Priority

1. Existing cached Markdown
2. arXiv metadata / known arXiv URL
3. Semantic Scholar lookup
4. Unpaywall optional placeholder
5. Manual fallback

## Reference Priority

1. Semantic Scholar references when a paper id exists
2. Cached Markdown references section
3. Manual reference list
4. Unknown / requires human review

## Boundaries

- No default network access.
- No API key required for tests.
- No copyrighted full text download.
- No MinerU implementation.
- No OCR-heavy pipeline.
- No upstream code copying.
- No fake reading marked as human verified.
- No old project naming.

## Validation

- Scholar pipeline unit tests.
- VGGT fake scholar workflow test.
- Semantic Scholar fake adapter tests.
- Citation graph tests.
- Contract/name/package checks.
