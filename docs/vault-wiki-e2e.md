# Vault Wiki E2E

Status: v1.4 fake/default production parity demo.

Round: 316.

This E2E demo shows the vault/wiki flow as a runnable review surface:

```text
markdown notes -> wikilinks -> backlink index -> edge audit -> wiki export
```

It uses the existing `vault_graph` helpers and does not introduce a graph
database or a new runtime.

## Inputs

The demo workspace is:

- `examples/vault_wiki_demo/e2e/notes/Research Catalog.md`
- `examples/vault_wiki_demo/e2e/notes/Stress Test.md`
- `examples/vault_wiki_demo/e2e/notes/Experiment Runbook.md`
- `examples/vault_wiki_demo/e2e/notes/Claim Review.md`
- `examples/vault_wiki_demo/e2e/notes/Artifact Audit.md`

The notes contain wikilinks such as [[Stress Test]], [[Experiment Runbook]],
[[Claim Review]], [[Artifact Audit]], and [[Missing Evidence]].

## Runtime Surfaces

The workflow test parses the note wikilinks into a lightweight `VaultGraph`,
then runs:

- `build_backlink_index`
- `build_dangling_link_report`
- `evaluate_edge_quality`
- `build_wiki_vault_export`

The generated demo reports are under:

- `examples/vault_wiki_demo/e2e/generated/backlink_index.md`
- `examples/vault_wiki_demo/e2e/generated/dangling_link_report.md`
- `examples/vault_wiki_demo/e2e/generated/edge_audit_report.md`
- `examples/vault_wiki_demo/e2e/generated/wiki_export_index.md`
- `examples/vault_wiki_demo/e2e/generated/wiki/`

## Expected Review Findings

- `artifact-audit -> missing-evidence` is a dangling link.
- `claim-review->artifact-audit:supports` is missing evidence refs.
- `artifact-audit->missing-evidence:supports` is missing evidence refs.
- `artifact-audit->missing-evidence:supports` is a weak edge.
- All nodes require human review.

## Safety Boundary

- fake/demo only;
- review-only graph output;
- no graph database;
- no private data;
- no raw data;
- no default network;
- no Evidence Ledger mutation;
- no automatic truth inference;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_vault_wiki_e2e.py -q
```
