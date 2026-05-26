# Original Author Showcase Authorization

This document records the migration policy for authorized academic showcase materials from the upstream reference projects into TuringResearch.

## Status

- Public project name: **TuringResearch**
- Current repository before final public rename: `meamaturinlove221/TulingResearch_plus`
- Migration branch: `feature/original-author-showcase-migration`
- Authorization status: user-reported authorization from the original project developer via project-resource exchange
- Migration mode: attributed academic showcase, not untracked copying

## Authorization Record

The user reports that the original repository developer has authorized us to move academic成果 / academic project outputs into this repository as project-product demonstrations.

Before making the repository public, the maintainer should preserve an explicit authorization record outside the repo as well, such as:

- screenshot or written message from the original developer;
- date of authorization;
- scope of authorized content;
- whether images, diagrams, README text, markdown skills, academic examples, and generated artifacts are all included;
- whether derivative adaptation is allowed;
- whether attribution text is required.

This repository should not claim exclusive authorship over upstream academic showcase materials. Every migrated item must keep source attribution.

## Source Repositories Covered Initially

- `Pthahnix/Neocortica-Session`
- `Pthahnix/Neocortica-Scholar`
- `Pthahnix/Neocortica-Web`
- selected `yogsoth-ai` research-engine materials, only where compatible with the user's authorization and our public safety policy

## Attribution Requirements

Every migrated showcase item must include:

1. upstream repository name;
2. upstream file path;
3. upstream commit SHA or retrieval date;
4. migration type: copied / adapted / summarized / reimplemented;
5. license / authorization note;
6. local maintainer decision;
7. safety review status.

## Non-goals

- Do not silently copy upstream source code as if it were original TuringResearch code.
- Do not import secrets, `.env`, cache files, private paths, raw data, or generated local context.
- Do not import anything that conflicts with public release safety.
- Do not make legal claims beyond the recorded authorization.
- Do not publish before the authorization scope is manually reviewed.

## Required Local Migration Gate

Before public release, run the migration gate described in:

- `docs/original-author-showcase-migration-plan.md`
- `examples/original-author-showcase/MIGRATION_MANIFEST.template.yaml`
- `examples/original-author-showcase/SAFETY_REVIEW.md`
