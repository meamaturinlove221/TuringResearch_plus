# Test Plan: paper_to_method_card

## Unit tests

- `test_method_card_requires_paper_id_title_and_evidence`
- `test_missing_real_paper_returns_requires_real_paper`
- `test_missing_figure_returns_requires_human_review`
- `test_method_component_requires_evidence_ref`
- `test_no_fabricated_method_components`

## Contract tests

- `test_method_card_contract_fields`
- `test_method_card_serializes_to_json_and_markdown`

## Workflow tests

- Dry-run NeuralBody-style method card fixture.
- Dry-run HumanRAM-style missing figure fixture.
- Dry-run HART-style requires-real-paper fixture.

## Non-goals

- No network paper lookup.
- No copyrighted PDF content copied.
- No paper draft generation.
