# Round 396R - Reference Docs Only Decision

Status: completed

## Goal

Decide whether upstream materials should be positioned as reference project
documentation / workflow inspiration instead of academic-output migration.

## Inputs Reviewed

- `docs/upstream-academic-publication-audit.md`
- `docs/upstream-publication-no-go-report.md`
- `docs/pr1-authorized-showcase-no-go.md`
- `docs/community-idea-skill-intake-gate-report.md`

## Decision

Use **Upstream Reference Docs / Workflow Inspiration**.

Do not use **Academic Showcase Migration**.

Do not migrate papers because no upstream publication package was found.

PR #1 does not enter the mainline.

## README Guidance

README may say upstream repositories are reference docs / workflow inspiration
for TuringResearch parity and independent implementation.

README must not claim upstream academic outputs, publication migration, migrated
papers, or accepted academic artifacts.

## Next

Open a new issue if durable tracking is needed:

- track reference-docs-only usage;
- track that publication migration is blocked;
- reopen publication migration only if the upstream author provides a concrete
  publication package.

## Outputs

- `docs/upstream-reference-docs-policy.md`
- `docs/no-upstream-publication-found-decision.md`
- `docs/reference-only-upstream-usage-plan.md`
- `docs/readme-upstream-reference-wording.md`
- `lanes/396R_reference_docs_only_decision.md`
