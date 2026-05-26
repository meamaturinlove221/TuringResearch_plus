# Structured Output Return Policy

Status: v0.3 Sprint 1 design draft.

Remote or pod-side work must return structured artifacts, not vague prose-only
claims.

## Required Output Files

- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

## Review Rules

- `PROPOSED_EVIDENCE_UPDATES.json` is never applied automatically.
- Missing outputs are blockers or human-review items.
- `FINAL_STATUS.json` cannot claim success without artifacts and hard-gate
  evidence.
- `SHA256SUMS.txt` must cover every included artifact.
- Large files must be omitted with reason and sha256 metadata.

## Failure Handling

Failed pod work still returns:

- run status;
- failure report;
- missing artifacts;
- proposed next action;
- cleanup status.

Report-only returns are not promotion-ready.
