# Ontology Runbook Demo

Status: v1.3 public-safe demo.

Round: 280.

This demo packages the ontology SOP parity surface into a small, inspectable
example. It shows alias resolution, gap detection, concept pages, and edge
suggestions without generating a final knowledge graph.

Demo files:

- `examples/ontology_demo/README.md`
- `examples/ontology_demo/concepts/`
- `examples/ontology_demo/ontology_runbook.md`
- `examples/ontology_demo/gap_report.md`

## Demonstrated Surface

- alias resolution;
- unresolved aliases;
- missing source references;
- low-confidence concept detection;
- missing hierarchy edge detection;
- dangling edge detection;
- concept page drafting;
- edge suggestions.

## Safety Boundary

- fake/demo only;
- review-only ontology output;
- no network;
- no private data;
- no raw data;
- no Evidence Ledger mutation;
- no automatic alias merge;
- no final knowledge graph;
- human review required.

## Validation

Run:

```powershell
python -m pytest tests/workflow/test_ontology_runbook_demo.py -q
```
