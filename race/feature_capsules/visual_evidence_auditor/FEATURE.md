# TulingResearch Plus Feature Capsule: visual_evidence_auditor

## Problem

Visual artifacts for VGGT / SMPL-X can be proxy debugging images or genuine
review evidence. Sprint 1 needs a gate that prevents proxy heatmaps and boards
from being mistaken for true pointcloud closeups or advisor-ready evidence.

## VGGT motivating example

Round 36 confirmed that `local_scan_visual_inventory.md` is missing. Therefore
V121 true region pointcloud visual readiness remains `requires-human-review`.

## User story

As a TulingResearch Plus maintainer, I need visual evidence classification so
advisor packs can explain what each image proves and what it does not prove.

## Inputs

- `ArtifactAuditReport` board inventory.
- Visual sidecars.
- Optional user-supplied local visual inventory.
- Evidence Ledger status rows.

## Outputs

- `VisualEvidenceAuditReport`
- Visual evidence classification table
- Advisor readiness summary
- Missing visual evidence report

## Data model

- `VisualEvidenceAuditReport`
- `VisualEvidenceItem`
- `VisualEvidenceLevel`
- `VisualRegionLabel`
- `VisualReadinessGate`

## Proposed commands / tools

- command: `tuling audit visual`
- tool: `visual.audit_evidence`
- output: `VisualEvidenceAuditReport`

This is a capsule-local proposal. It is not a frozen public MCP API until the
root contracts and `docs/mcp-tools.md` are updated in a later contracts-first
round.

## Related contracts

- `contracts/artifact_schema.yaml`
- `contracts/paper_pipeline.yaml`
- `contracts/race_features.yaml`

## Related skills

- `tulingresearch-paper-figure-asset-pipeline`
- `tulingresearch-race-feature-capsule-factory`
- `tulingresearch-cache-and-ledger`

## Required tests

- Proxy heatmap classification.
- Mask/delta board classification.
- Full pointcloud proxy classification.
- True region pointcloud closeup classification.
- Unknown visual artifact requires-human-review.
- Advisor readiness summary gate.

## Risks

- Confusing proxy visual evidence with true visual evidence.
- Overclaiming V121 readiness.
- Letting missing visual inventory pass silently.
- Packaging private images into committed docs.

## Done criteria

- Every visual item has source artifact provenance.
- Unknown visual items require human review.
- Advisor readiness cannot pass without required visual evidence.
- No image content is fabricated.

## Release target

v0.2.0 Sprint 1, third implementation slice.

Future Sync Adapters remain out of scope for this sprint. Handoff, NAS/SMB,
SSH/SFTP, GitHub sync, and cloud object storage must wait for later adapter
planning.

