# Round 397R - TuringResearch Public Naming Final Sweep

Status: completed

## Goal

Unify public-facing naming around TuringResearch and remove PR #1 showcase
semantics from the public launch prep line.

## Inputs Checked

- `README.md`
- `docs/`
- `docs-site/`
- `examples/`
- `community/` if present
- `split_ready/`
- `split_manual/`
- `pyproject.toml`
- `.mcp.example.json`
- `CHANGELOG.md`
- `VERSION`

## Findings

- Public project name remains TuringResearch.
- `examples/original-author-showcase/` is absent on this branch.
- `community/` is absent on this release-derived branch.
- PR #1 is excluded.
- Upstream materials must be framed as Reference / Inspiration / Related
  Projects only.
- Compatibility names remain allowed for package/import/entry-point surfaces.
- Forbidden academic showcase wording appears only in no-go/policy contexts.

## Outputs

- `docs/public-naming-final-sweep-v1.7.md`
- `docs/legacy-name-compatibility-final.md`
- `docs/github-rename-readiness.md`
- `docs/upstream-reference-wording-check.md`
- `lanes/397R_public_naming_final_sweep.md`

## Decision

`GO FOR PUBLIC NAMING FINAL SWEEP`

`NO-GO FOR PR #1 SHOWCASE SEMANTICS`

`NO-GO FOR ACADEMIC PUBLICATION MIGRATION CLAIMS`
