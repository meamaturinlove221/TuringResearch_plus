# Original Author Showcase Migration Plan

This plan describes how to move authorized upstream academic showcase materials into TuringResearch as attributed project-product demonstrations.

## Goal

Create a public-safe showcase section that demonstrates how TuringResearch can organize, audit, and present research-operating-system workflows inspired by the original reference projects.

The showcase should strengthen the public README and interview story while preserving attribution and safety boundaries.

## Target Directory

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

## Migration Types

Use one of the following labels for every migrated item:

- `copied_with_authorization`: copied content with explicit authorization and attribution;
- `adapted_with_authorization`: modified or reformatted content with authorization;
- `summarized_with_attribution`: summary or taxonomy derived from upstream docs;
- `reimplemented_clean_room`: independently implemented equivalent based on public behavior;
- `reference_only`: not copied into the repo, only linked or cited.

## Initial Content Candidates

### Neocortica-Session

Recommended showcase material:

- architecture summary;
- session lifecycle diagram;
- Git-context / pod-deployment workflow;
- safety notes around dotfile handling, shell injection, cross-platform archive unpacking;
- TuringResearch comparison: local-first session runtime, context pack, fake transfer, return verifier, human confirmation.

### Neocortica-Scholar

Recommended showcase material:

- paper tool surface table;
- `paper_searching`, `paper_fetching`, `paper_content`, `paper_reference`, `paper_reading` workflow;
- three-pass reading demo;
- MCP env-block pattern;
- TuringResearch comparison: scholar pipeline, fake/live boundary, optional heavy backend slot.

### Neocortica-Web

Recommended showcase material:

- `web_fetching` / `web_content` workflow;
- Apify optional-live pattern;
- cache-first web content model;
- no-dotenv public config policy;
- TuringResearch comparison: web tool surface, URL normalization, cache manifest, live redaction gate.

### yogsoth-ai Research Engine

Recommended showcase material:

- campaign / strategy / tactic / SOP layered architecture;
- executable research spec idea;
- context checkpointing;
- TuringResearch comparison: campaign catalog, vault graph, ontology SOP, stress/convergence, experiment runbook.

## Required Safety Filter

Do not migrate:

- `.env`, private configuration, tokens, or secrets;
- raw logs or private session context;
- local cache contents;
- personal data;
- copyrighted third-party PDFs unless separately allowed;
- raw generated academic claims without attribution;
- anything that says TuringResearch created the upstream idea from scratch.

## README Integration

After migration, update the public README with a small section:

```md
## Authorized Academic Showcase

This repository includes an attributed showcase of selected academic workflow ideas authorized by the original developer of the reference projects. The showcase is used to demonstrate how TuringResearch organizes research workflows, evidence ledgers, artifact audits, and public-safe reporting.
```

Do not make the showcase the main product. TuringResearch remains the flagship project.

## Migration Gate

Before merge:

1. all items have source repository and path;
2. all items have migration type;
3. all items have authorization note;
4. all items pass secret scan;
5. all items pass public naming check;
6. all upstream license notes are retained;
7. README mentions attribution;
8. no fake GitHub URL is introduced.
