# Lightweight Dashboard UI

Status: scope_locked.

## Problem

Reports are Markdown-first and scattered across remote artifact, dashboard, comparison, paper digest, and advisor export outputs.

## VGGT motivating example

VGGT review needs a local dashboard that lets a maintainer scan run status, artifact gaps, visual readiness, and advisor readiness without treating the UI as an experiment runner.

## User story

As a TuringResearch operator, I want this capability to turn existing review artifacts into safer, clearer project workflows without weakening evidence boundaries.

## Inputs

- Existing Markdown and JSON review artifacts.
- v0.4 remote artifact, dashboard, paper digest, or advisor export outputs.
- Project manifests and source refs.
- Manual review notes when needed.

## Outputs

- `DashboardUIPlan`.
- JSON-serializable report.
- Markdown review summary.
- Required human-review flags.

## Data model

- status: planned / generated / blocked / requires-human-review.
- source refs and sha256 metadata where applicable.
- limitations, omitted items, and safety warnings.
- no verified result unless evidence explicitly supports it.

## Proposed commands / tools

- command: `turing ui dashboard`
- tool: `ui.dashboard_local`
- output: `DashboardUIPlan`

## Related contracts

- contracts/modal_run_dashboard.yaml, contracts/run_comparison.yaml, contracts/remote_artifacts.yaml

## Related skills

- `turingresearch-master-orchestrator`

## Required tests

- Fake/default workflow test.
- JSON serialization test.
- Markdown export test.
- Evidence-boundary regression test.
- No secret/raw-data/SMPL-X model packaging test.

## Risks

A UI can make review artifacts look more final than their evidence supports.

## Done criteria

Local static dashboard scope, data contract map, no-login/no-cloud boundary, fake fixture workflow, accessibility checklist.

## Release target

v0.5

## Non-goals

- No complex SaaS.
- No user system.
- No cloud deployment.
- No automatic paper writing.
- No unauthorized data upload.
- No legacy project naming.
