# TulingResearch Plus Feature Capsule: advisor_pack_builder

## Problem

VGGT / SMPL-X dogfooding needs advisor-readable summaries, but Round 36
confirmed that review-ready proxy evidence is not promotion and final advisor
acceptance must remain human-only.

## VGGT motivating example

The current scan shows root co-location but no scanned artifacts, no evidence
ledger JSON, and no visual inventory. An advisor pack must therefore explain
missing evidence instead of presenting a successful experiment.

## User story

As a TulingResearch Plus maintainer, I need an advisor pack builder that turns
Evidence Ledger, Artifact Auditor, and Visual Evidence Auditor outputs into a
clear review package without fabricating results.

## Inputs

- `VGGTEvidenceLedger`
- `ArtifactAuditReport`
- `VisualEvidenceAuditReport`
- Dogfooding plan
- Missing evidence report

## Outputs

- `AdvisorPack`
- Markdown pack
- Section readiness report
- Missing evidence appendix

## Data model

- `AdvisorPack`
- `AdvisorPackSection`
- `AdvisorReadinessStatus`
- `AdvisorMissingEvidenceItem`
- `EvidenceRef`

## Proposed commands / tools

- command: `tuling advisor pack`
- tool: `advisor.pack_build`
- output: `AdvisorPack`

This is a capsule-local proposal. It is not a frozen public MCP API until the
root contracts and `docs/mcp-tools.md` are updated in a later contracts-first
round.

## Related contracts

- `contracts/paper_pipeline.yaml`
- `contracts/artifact_schema.yaml`
- `contracts/race_features.yaml`

## Related skills

- `tulingresearch-paper-writing-pipeline`
- `tulingresearch-paper-docflow-article-blocks`
- `tulingresearch-race-feature-capsule-factory`

## Required tests

- Required sections present.
- No promotion wording.
- Missing visual inventory blocks readiness.
- Failures and next steps included.
- Pack references artifact and evidence ledger entries.

## Risks

- Implying final advisor acceptance.
- Hiding missing evidence.
- Presenting proxy visuals as conclusive proof.
- Creating paper-like claims without ExperimentReport.

## Done criteria

- Pack contains method status, evidence status, visual status, failures, risks,
  and next steps.
- Pack blocks readiness when evidence is missing.
- Pack preserves EvidenceRef.
- Pack does not fabricate results or approval.

## Release target

v0.2.0 Sprint 1, fourth implementation slice.

Future Sync Adapters remain out of scope for this sprint. Handoff, NAS/SMB,
SSH/SFTP, GitHub sync, and cloud object storage must wait for later adapter
planning.

