# Reference-Only Upstream Usage Plan

Round: 396R
Status: active plan

## Positioning

Use upstream repositories as:

- reference documentation;
- workflow inspiration;
- parity comparison targets;
- architecture and tool-surface references;
- public examples of research workflow design.

Do not use upstream repositories as academic publication sources unless a
future concrete publication package is provided.

## Practical Use

TuringResearch may continue to reference upstream materials for:

- Neocortica-Session style session/pod/runtime workflows;
- Neocortica-Scholar style paper-tool surfaces and three-pass reading workflow;
- Neocortica-Web style web/cache/fetching/MCP boundaries;
- yogsoth-ai style research engine, campaign, SOP, convergence, stress-test,
  vault, ontology, and experiment runbook concepts.

Each reference should stay clearly framed as inspiration or docs parity.

## Required Language

Preferred phrases:

- Upstream Reference Docs
- Workflow Inspiration
- reference parity
- docs/tool-surface comparison
- independently implemented TuringResearch equivalent

Avoid phrases:

- Academic Showcase Migration
- academic-output migration
- publication migration
- migrated papers
- upstream academic outputs
- accepted publication artifacts

## Issue Tracking

Create a new tracking issue if the project needs a durable public record:

```text
Title: Track upstream reference-docs-only usage and blocked publication migration

Scope:
- Keep upstream materials framed as reference docs / workflow inspiration.
- Do not claim academic publication migration.
- Track whether the upstream author later provides a publication package.
- Reopen publication migration only after concrete source artifacts exist.
```

## Future Gate

A future migration branch must pass:

1. publication package presence check;
2. provenance check;
3. authorization check;
4. privacy check;
5. public naming check;
6. README wording check.
