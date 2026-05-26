# Vault Edge Quality: vault-wiki-e2e

- Release blocker: `true`
- Requires human review: `true`

## Summary

- nodes: `5`
- edges: `6`
- node_types: `1`
- edge_types: `4`

## Missing Edges

- `claim-review->artifact-audit:supports`
- `artifact-audit->missing-evidence:supports`

## Weak Edges

- `artifact-audit->missing-evidence:supports`

## Requires Review Nodes

- `artifact-audit`
- `claim-review`
- `experiment-runbook`
- `research-catalog`
- `stress-test`

## Safety Boundary

- fake/demo only;
- review-only graph output;
- no graph database;
- no private data;
- no default network;
- no Evidence Ledger mutation;
- no automatic truth inference;
- human review required.
