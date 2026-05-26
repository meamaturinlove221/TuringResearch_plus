# Vault Wiki Export Demo

Status: v1.3 public-safe demo.

Round: 279.

This demo packages the vault/wiki/edge audit parity surface into a browsable
example. It shows wikilinks, backlinks, dangling links, missing edges, weak
edges, requires-review nodes, and a graph summary.

Demo files:

- `examples/vault_wiki_demo/README.md`
- `examples/vault_wiki_demo/wiki/`
- `examples/vault_wiki_demo/edge_audit_report.md`

## Demo Graph

The demo graph has three fake nodes:

- `north-star`
- `hypothesis`
- `artifact`

It intentionally includes:

- a backlink from `Hypothesis` to `North Star`;
- a wikilink from `Artifact Audit` to `Missing Result`;
- a dangling link to `missing-result`;
- a missing evidence-bearing edge for `hypothesis->artifact:supports`;
- a weak edge for `artifact->missing-result:related_to`.

## Safety Boundary

- fake/demo only;
- no graph database;
- no private data;
- no raw data;
- no Evidence Ledger mutation;
- no automatic truth inference;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_vault_wiki_export_demo.py -q
```
