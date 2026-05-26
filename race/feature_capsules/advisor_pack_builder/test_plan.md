# Test Plan: advisor_pack_builder

## Unit tests

- `test_required_pack_sections_present`
- `test_no_promotion_wording_allowed`
- `test_missing_visual_inventory_blocks_readiness`
- `test_failures_and_next_steps_included`
- `test_pack_references_evidence_and_artifact_rows`

## Contract tests

- `test_advisor_pack_contract_fields`
- `test_advisor_pack_requires_evidence_refs`

## Workflow tests

- Dry run from fake Evidence Ledger, Artifact Audit, and Visual Audit reports.
- Dry run with missing visual inventory.

## Fixtures

- Fake ledger report.
- Fake artifact audit report.
- Fake visual evidence report.

## Non-goals

- No final advisor approval.
- No paper draft generation.
- No cross-machine sync.
