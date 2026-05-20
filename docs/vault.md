# TulingResearch Plus Vault

TulingResearch Plus Vault is a local markdown knowledge graph memory. It stores typed pages, evidence-preserving frontmatter, typed graph edges, and a simple replaceable BM25-like index.

## Tools

- `vault.search`
- `vault.ingest_source`
- `vault.compile_page`
- `vault.add_edge`
- `vault.query_graph`
- `vault.graph_stats`
- `vault.lint`
- `vault.edge_audit`

## Entity Types

- `source`
- `concept`
- `entity`
- `claim`
- `relation`
- `question`
- `evidence`
- `failure`
- `topic`

## Edge Types

- `component_of`
- `instance_of`
- `supported_by`
- `contradicts`
- `supersedes`
- `derived_from`
- `addresses`
- `raises`
- `failed_for`
- `related_to`

## Rules

- `ResearchArtifact` ingestion creates a claim page and evidence pages.
- Claim pages connect to evidence pages with `supported_by` edges.
- Duplicate edges are rejected.
- Orphan pages and missing frontmatter are lint issues.
- Search is local only and uses a small BM25-like index.
- The Vault performs no network calls.

## Release Scope

The `v0.1.0` Vault is a local memory foundation. It is intended for deterministic ingestion, graph edge validation, lint, and fake-mode workflow persistence. Remote sync, multi-user auth, and hosted search are outside the release candidate.
