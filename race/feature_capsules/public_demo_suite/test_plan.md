# Test Plan: Public Demo Suite

## Unit tests

- Model serialization.
- Required fields.
- Safety boundary validation.
- Markdown export.

## Workflow tests

- Fake/default fixture workflow.
- Missing input handling.
- No live credential requirement.
- No planned-as-observed promotion.

## Contract tests

- Contract file exists.
- Proposed tool remains non-public until explicitly promoted.
- Required safety flags are present.

## Negative tests

- Reject generated claims without evidence.
- Reject raw data / SMPL-X model packaging.
- Reject legacy project naming.
