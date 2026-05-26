# Vault Graph Enhancement

Status: implemented minimal.

Round 74 adds a lightweight vault graph layer for typed nodes, typed edges,
source refs, confidence labels, status labels, edge audit, and optional
wikilink export. It does not introduce a graph database or UI.

## Node Types

- paper
- method
- dataset
- experiment
- artifact
- claim
- failure
- route
- skill
- concept
- architecture_component

## Edge Types

- supports
- contradicts
- derived_from
- cites
- related_to
- maps_to
- uses
- blocks
- requires
- improves
- risks
- belongs_to

## Audit

`VaultGraphAuditReport` records:

- dangling edges
- missing evidence refs on evidence-bearing edges
- low-confidence nodes
- requires-human-review nodes

## Safety Boundary

- Graph output is not final truth.
- Evidence-bearing edges require source refs.
- Low-confidence and requires-human-review nodes must remain visible.
- No live service or external graph database is required.
