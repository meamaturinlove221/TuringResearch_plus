# Vault Wiki Edge Audit Demo

Status: public-safe fake demo.

Graph id: `vault-wiki-demo`.

## Graph Summary

- Nodes: `3`
- Edges: `3`
- Node types: `1`
- Edge types: `3`
- Requires human review: `true`

## Wikilinks

- [[North Star]]
- [[Hypothesis]]
- [[Artifact Audit]]
- [[Missing Result]]

## Backlinks

| Node | Backlinks | Outgoing |
| --- | --- | --- |
| `north-star` | none | `hypothesis` |
| `hypothesis` | `north-star` | `artifact` |
| `artifact` | `hypothesis` | `missing-result` |

## Dangling Links

- `artifact` -> `missing-result` (`related_to`)

## Missing Edges

- `hypothesis->artifact:supports`

## Weak Edges

- `artifact->missing-result:related_to`

## Requires Review Nodes

- `north-star`
- `hypothesis`
- `artifact`

## Safety Boundary

- fake/demo only;
- review-only graph output;
- no graph database;
- no private data;
- no Evidence Ledger mutation;
- no automatic truth inference.
