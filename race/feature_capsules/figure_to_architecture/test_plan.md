# Test Plan: figure_to_architecture

## Unit tests

- `test_architecture_spec_requires_nodes`
- `test_edge_requires_supporting_method_card_or_warning`
- `test_figure_component_mapping_preserves_source`
- `test_mermaid_export_contains_nodes_and_edges`
- `test_output_labeled_draft_when_evidence_incomplete`

## Contract tests

- `test_figure_architecture_contract_fields`
- `test_architecture_spec_serializes_to_json_and_markdown`

## Workflow tests

- Generate draft from minimal Method Card fixture.
- Generate warning from unsupported edge fixture.
- Generate diagram from PDF Phase B figure registry fixture.

## Non-goals

- No final paper figure claim.
- No live paper lookup.
- No unsupported architecture inference.
