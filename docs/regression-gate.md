# Regression Gate

Status: implemented minimal.

The regression gate catches safety and release blockers before a branch is
considered ready for review.

## Fail Conditions

- Prior project naming appears outside allowlisted historical docs.
- Secret-like values or forbidden local config files are detected.
- Public demo files are missing.
- Required contracts are missing.
- Fake/demo result is marked observed.
- Live tests are required by default.

## Output

`RegressionGateReport` records:

- gate id
- checks
- status
- blockers
- warnings
- human review requirement

## Boundary

- The gate does not delete files.
- The gate does not publish or tag a release.
- The gate does not replace human review.
