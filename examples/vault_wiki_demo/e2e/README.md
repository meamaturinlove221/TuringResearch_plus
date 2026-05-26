# Vault Wiki E2E Demo

Status: public-safe fake/demo only.

Round: 316.

This demo turns a small set of Markdown notes into a review-only vault/wiki
flow:

1. Markdown notes contain wikilinks.
2. Wikilinks are represented as graph edges.
3. The backlink index shows incoming and outgoing links.
4. The edge audit flags dangling links, missing evidence-bearing edges, and
   weak edges.
5. The wiki export renders review pages and an export index.

## Contents

- `notes/`: fake Markdown notes with wikilinks.
- `generated/backlink_index.md`: backlink index output.
- `generated/dangling_link_report.md`: dangling link report.
- `generated/edge_audit_report.md`: edge quality report.
- `generated/wiki_export_index.md`: wiki export index.
- `generated/wiki/`: sample generated wiki pages.

## Demo Flow

`Research Catalog` links to [[Stress Test]] and [[Experiment Runbook]].
`Stress Test` links to [[Claim Review]].
`Claim Review` links to [[Artifact Audit]] with a deliberately missing
evidence-bearing edge.
`Artifact Audit` links to [[Missing Evidence]], which is intentionally absent
from the note set to demonstrate a dangling link.

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
