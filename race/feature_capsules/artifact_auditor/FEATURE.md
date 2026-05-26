# TuringResearch Plus Feature Capsule: artifact_auditor

## Problem

Round 36 confirmed that the VGGT local artifact index currently contains no
scanned artifacts. Sprint 1 needs a deterministic local auditor for bundles,
sidecars, checksums, boards, and missing files before evidence can be trusted.

## VGGT motivating example

The dry-run artifact index says no artifacts were scanned because private local
config is missing. A future user-provided scan may include zip/json/csv/png/npz
files, full archives, thin bundles, visual boards, and Modal-like sidecars.

## User story

As a TuringResearch Plus maintainer, I need an artifact auditor that can inspect
local evidence bundles and report completeness without running VGGT or writing
into VGGT directories.

## Inputs

- Local artifact bundle path when explicitly supplied by the user.
- Committed fake fixture bundles.
- Optional manifest and sidecar files.
- `VGGTEvidenceLedger` status boundaries.

## Outputs

- `ArtifactAuditReport`
- Bundle manifest
- Missing artifact list
- Checksum list
- Board inventory summary

## Data model

- `ArtifactAuditReport`
- `ArtifactRecord`
- `ArtifactBundleManifest`
- `ArtifactSidecar`
- `BundleDiff`

## Proposed commands / tools

- command: `tuling audit artifact`
- tool: `artifact.audit`
- output: `ArtifactAuditReport`

This is a capsule-local proposal. It is not a frozen public MCP API until the
root contracts and `docs/mcp-tools.md` are updated in a later contracts-first
round.

## Related contracts

- `contracts/artifact_schema.yaml`
- `contracts/vault_schema.yaml`
- `contracts/race_features.yaml`

## Related skills

- `turingresearch-race-feature-capsule-factory`
- `turingresearch-fusion-wiki-vault`
- `turingresearch-cache-and-ledger`

## Required tests

- Valid zip fixture.
- Broken zip fixture.
- sha256 checksum fixture.
- Manifest completeness.
- Missing `.npz`.
- Candidate predictions discovery.
- Sidecar consistency.
- Local scan versus uploaded bundle diff.
- No-write-into-linked-project regression.

## Risks

- Treating incomplete bundles as valid.
- Accidentally scanning or writing private VGGT paths.
- Inferring experiment success from filenames.
- Leaking private artifacts into committed docs.

## Done criteria

- Auditor is local-only and read-only by default.
- Reports contain provenance and warnings.
- Missing files stay missing, not successful.
- Evidence Ledger can consume audit results.

## Release target

v0.2.0 Sprint 1, second implementation slice.

Future Sync Adapters remain out of scope for this sprint. Handoff, NAS/SMB,
SSH/SFTP, GitHub sync, and cloud object storage must wait for later adapter
planning.
