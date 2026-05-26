# Ontology E2E

Status: v1.4 fake/default production parity demo.

Round: 317.

This E2E demo shows the ontology SOP flow as a runnable review surface:

```text
concept notes -> alias resolution -> gap detection -> edge suggestion -> ontology report
```

It uses the existing `vault_graph` ontology helpers and does not generate a
final knowledge graph.

## Inputs

The demo workspace is:

- `examples/ontology_demo/e2e/concept_notes/Root Ontology.md`
- `examples/ontology_demo/e2e/concept_notes/Research Catalog.md`
- `examples/ontology_demo/e2e/concept_notes/Stress Test.md`
- `examples/ontology_demo/e2e/concept_notes/Claim Review.md`

The notes declare aliases such as `research workflow catalog`, `stress gate`,
and `claim audit note`.

## Runtime Surfaces

The workflow test parses the concept notes into a lightweight `VaultGraph`,
then runs:

- `resolve_aliases`
- `detect_ontology_gaps`
- `run_ontology_sop_plan`
- `render_alias_resolution_report`
- `render_ontology_gap_report`
- `render_ontology_sop_runbook`

The generated demo reports are under:

- `examples/ontology_demo/e2e/generated/alias_resolution.md`
- `examples/ontology_demo/e2e/generated/gap_report.md`
- `examples/ontology_demo/e2e/generated/edge_suggestions.md`
- `examples/ontology_demo/e2e/generated/ontology_report.md`

## Expected Review Findings

- `unknown ontology term` remains unresolved.
- `claim-review` has no source refs.
- `claim-review` is low confidence.
- `stress-test` and `claim-review` need hierarchy edges.
- `claim-review->missing-claim-evidence:supports` is dangling.
- Edge suggestions remain proposed-only.

## Safety Boundary

- fake/demo only;
- review-only ontology output;
- no final knowledge graph;
- no private data;
- no raw data;
- no default network;
- no Evidence Ledger mutation;
- no automatic truth inference;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_ontology_e2e.py -q
```
