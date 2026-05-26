# Original Author Academic Showcase

This directory contains public-safe, attributed showcase materials migrated or adapted from the original reference projects under user-reported authorization from the original developer.

The purpose of this directory is not to erase upstream authorship. The purpose is to demonstrate how **TuringResearch** organizes, audits, summarizes, and presents complex research-operation workflows as project-product demonstrations.

## Current Migration Mode

This initial migration uses mostly:

- `summarized_with_attribution`
- `adapted_with_authorization`
- `reference_only`

Bulk verbatim copying of upstream files, images, diagrams, or generated artifacts should happen only after the maintainer confirms the exact authorization scope and preserves source paths and commit SHAs in `MIGRATION_MANIFEST.yaml`.

## Directory Plan

```text
examples/original-author-showcase/
  README.md
  MIGRATION_MANIFEST.yaml
  MIGRATION_MANIFEST.template.yaml
  SAFETY_REVIEW.md
  neocortica-session/
  neocortica-scholar/
  neocortica-web/
  yogsoth-research-engine/
```

## Required Per-output Summary

Every migrated academic output must have:

1. upstream source repository;
2. upstream file path;
3. upstream commit SHA or retrieval date;
4. migration type;
5. short summary;
6. attribution note;
7. public safety review status.

The user's private Chinese working summary is intentionally kept outside GitHub.

## Safety Boundary

Do not place secrets, raw private data, private session context, unpublished research data, unauthorized third-party PDFs, or private local paths in this directory.
