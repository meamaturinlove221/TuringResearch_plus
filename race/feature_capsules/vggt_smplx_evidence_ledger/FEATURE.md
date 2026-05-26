# TuringResearch Plus Feature Capsule: vggt_smplx_evidence_ledger

## Problem

VGGT / SMPL-X dogfooding has several milestone labels, but Round 36 confirmed
that user-provided engineering context, local-observed evidence, missing local
scan files, and human-review requirements must not be mixed.

## VGGT motivating example

V770, V129, V260, V900, V930, and V999 are currently engineering context.
V120 and V121 remain `requires-human-review` because
`local_scan_evidence_ledger.json` and `local_scan_visual_inventory.md` are
missing.

## User story

As a TuringResearch Plus maintainer, I need a structured evidence ledger so
Sprint 1 tools can record VGGT/SMPL-X evidence without overstating experiment
success, promotion readiness, or advisor approval.

## Inputs

- `docs/dogfooding-vggt-smplx.md`
- `docs/vggt-smplx-evidence-ledger.md`
- `examples/vggt-human-prior-survey/local_scan_summary.md`
- `examples/vggt-human-prior-survey/local_scan_artifact_index.md`
- Optional local `local_scan_evidence_ledger.json` when provided by the user

## Outputs

- `VGGTEvidenceLedger`
- Markdown summary
- JSON summary
- Missing evidence report

## Data model

- `VGGTEvidenceLedger`
- `VGGTEvidenceRow`
- `VGGTEvidenceStatus`
- `VGGTMilestone`
- `EvidenceRef`

## Proposed commands / tools

- command: `tuling vggt ledger build`
- tool: `vggt.evidence_ledger_build`
- output: `VGGTEvidenceLedger`

This is a capsule-local proposal. It is not a frozen public MCP API until the
root contracts and `docs/mcp-tools.md` are updated in a later contracts-first
round.

## Related contracts

- `contracts/artifact_schema.yaml`
- `contracts/vault_schema.yaml`
- `contracts/race_features.yaml`

## Related skills

- `turingresearch-cache-and-ledger`
- `turingresearch-fusion-wiki-vault`
- `turingresearch-race-feature-capsule-factory`

## Required tests

- Status enum validation.
- Milestone rows for V770, V129, V260, V900, V930, V999, V120, and V121.
- `observed` versus `local-observed` separation.
- `review-ready-proxy` is not promotion.
- Missing evidence marks V120/V121 as `requires-human-review`.
- Markdown and JSON serialization.

## Risks

- Overclaiming V120/V121 without local evidence.
- Treating advisor review readiness as promotion.
- Letting missing local files look like successful scans.
- Future sync adapters importing private paths or private artifacts.

## Done criteria

- Contract draft accepted.
- Ledger model and tests exist.
- Missing local evidence cannot become local-observed.
- Outputs preserve EvidenceRef.
- No VGGT experiment result is fabricated.

## Release target

v0.2.0 Sprint 1, first implementation slice.

Future Sync Adapters remain out of scope for this sprint. Handoff, NAS/SMB,
SSH/SFTP, GitHub sync, and cloud object storage must wait for later adapter
planning.
