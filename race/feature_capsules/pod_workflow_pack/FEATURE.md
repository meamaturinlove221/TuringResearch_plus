# TuringResearch Plus Feature Capsule: pod_workflow_pack

## Problem

Remote pod work often returns incomplete reports, ambiguous status, or unsafe
artifact bundles. TuringResearch Plus needs a structured pod workflow package
that makes outputs auditable.

## VGGT motivating example

The VGGT Modal SparseConv3D route can be prepared locally, but any pod-side work
must return status, artifacts, failures, proposed evidence updates, and checksums
without claiming success prematurely.

## User story

As a maintainer, I want pod outputs to come back in a fixed structure so
TuringResearch can ingest, audit, classify failures, and prepare advisor inputs.

## Inputs

- `ContextPackage`
- `ROUTE_SPEC.yaml`
- `HARD_GATES.md`
- `ARTIFACT_REQUIREMENTS.md`
- `FAILURE_TAXONOMY.md`

## Outputs

- `PodWorkflowSpec`
- `StructuredOutputReturn`
- `RUN_STATUS.json`
- `FINAL_STATUS.json`
- `ARTIFACT_INDEX.md`
- `FAILURE_REPORT.md`
- `PROPOSED_EVIDENCE_UPDATES.json`
- `ADVISOR_SUMMARY_DRAFT.md`
- `SHA256SUMS.txt`

## Data model

- `PodWorkflowSpec`
- `StructuredOutputReturn`
- `HandoffSafetyPolicy`

## Proposed commands / tools

- command: `turing pod workflow-pack`
- tool: design-only `context.pod_workflow_pack`
- output: `PodWorkflowSpec`

This is not a public MCP API until a later contracts-first implementation
round.

## Related contracts

- `contracts/pod_workflow.yaml`
- `contracts/git_context_handoff.yaml`
- `contracts/run_ingest.yaml`
- `contracts/handoff_bundle.yaml`

## Related skills

- `turingresearch-master-orchestrator`
- `turingresearch-fusion-experiment-execution`
- `turingresearch-cache-and-ledger`

## Required tests

- pod output package contains required files;
- output package is importable by Run Ingestor;
- missing outputs are marked missing;
- report-only output is not promotion-ready;
- proposed evidence updates are not applied automatically.

## Risks

- Treating pod workflow as remote execution control.
- Missing checksums or artifact index.
- Report-only returns hiding real failure.
- Accidental secret or raw-data return.

## Done criteria

- Contract draft and design docs are accepted.
- Output return policy is clear.
- Future implementation can run fake workflow tests without network.

## Release target

v0.3 Sprint 1.

## Upstream learning note

Inspired by structured output return via Git, but TuringResearch Plus keeps pod
execution outside its control surface.

## Relation to v0.2 modules

Builds on Run Ingestor, Artifact Auditor, Failure Taxonomy, Evidence Ledger,
Advisor Pack, and Handoff Bundle.
