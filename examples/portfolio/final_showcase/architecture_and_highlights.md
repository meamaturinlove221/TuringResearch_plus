# Architecture And Technical Highlights

## Architecture

Use these visual references:

- `examples/portfolio/turingresearch_architecture.mmd`
- `docs/architecture-diagram-final.mmd`
- `docs/research-os-flow.mmd`

The architecture story:

1. Workspace and project templates keep research state organized.
2. Evidence ledger, artifact audit, route DSL, and failure taxonomy keep claims
   reviewable.
3. Paper scaffold, deep review, dashboard, and advisor pack turn state into
   human-review material.
4. Plugin manifests, sandbox policy, privacy, compliance, quality, and replay
   gates keep public release and extension surfaces bounded.

## Technical Highlights

- Contract-first module surfaces.
- Modular monorepo facade namespaces.
- Fake/demo-first workflows with optional live adapters.
- Planned vs observed evidence discipline.
- Plugin safety without default unknown code execution.
- Static dashboard and advisor export paths.
- Privacy, compliance, quality, replay, and split dry-run gates.
