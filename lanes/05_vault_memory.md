# Lane 05: Vault Memory

## Scope

Define Vault memory schema boundaries that reference ResearchArtifact and EvidenceRef.

## Outputs

- `contracts/vault_schema.yaml`

## Status

Phase 1 complete. No storage engine is implemented.

## Round 8A Update

2026-05-19: Implemented the local TulingResearch Plus Wiki Vault:

- Markdown vault pages with typed frontmatter.
- Entity types: `source`, `concept`, `entity`, `claim`, `relation`, `question`, `evidence`, `failure`, `topic`.
- Edge types: `component_of`, `instance_of`, `supported_by`, `contradicts`, `supersedes`, `derived_from`, `addresses`, `raises`, `failed_for`, `related_to`.
- Simple replaceable BM25-like local search.
- Typed graph edges with duplicate rejection.
- Graph traversal, stats, and edge audit.
- Lint checks for orphan pages and missing frontmatter.
- `ResearchArtifact` ingestion into claim/evidence pages.

No network behavior was added.

## Round 8B Update

2026-05-19: Implemented TulingResearch Plus Context Management:

- `context.init`
- `context.checkpoint`
- `context.recover`
- `context.index`
- `context.summarize`

Each campaign run creates one local context file. Strategy completion can append checkpoints, and checkpoints must preserve artifact links and evidence refs. The context index can recover the latest summary and artifact list.

Unlike write-only context logs, TulingResearch Plus context files support recovery. No network or LLM behavior was added.
