# Real-world Dogfooding Plan

Status: planning draft.

v0.7 should move from fake/default replay toward carefully scoped real-world
dogfooding. The goal is to test the research workflow on real projects without
uploading private data, fabricating outcomes, or weakening evidence gates.

## Candidate Dogfooding Tracks

1. VGGT human-prior case study.
2. Public demo project expansion.
3. Paper-survey-only project.
4. Software tooling research project.
5. Dataset/license compliance dry-run.

## Dogfooding Rules

- Real artifacts must be reviewed before they become evidence.
- Planned experiments must remain planned until executed.
- Missing results must remain missing.
- Private data stays local.
- Raw data and licensed model files are not packaged.
- Public outputs must pass privacy and release hygiene gates.
- Advisor-facing outputs must distinguish observed, retrieved, planned,
  missing, and requires-human-review.

## VGGT Dogfooding Path

Near-term:

- refresh research knowledge pack from existing committed review artifacts;
- re-run benchmark replay and quality gate;
- check paper assembly blockers;
- update advisor brief with missing evidence items.

Requires real VGGT machine / explicit dry-run:

- inspect real artifact manifests;
- verify sparse backend logs;
- collect result-table-ready outputs if experiments ran;
- update evidence ledger only after review.

## Public Demo Expansion

Add fake/demo projects that show:

- paper survey workflow;
- experiment-heavy workflow;
- software tooling workflow;
- privacy gate failure and remediation report;
- plugin manifest review workflow.

## What TuringResearch Should Measure

- Can a new project be generated from templates?
- Can evidence and artifact status be inspected quickly?
- Can unsafe public-release material be detected?
- Can paper assembly correctly block unsupported sections?
- Can replay checks catch missing outputs?
- Can dashboards and advisor bundles explain what is not done?

## What Still Requires Human Research

- Experiment design decisions.
- Real run interpretation.
- Citation verification.
- Related work positioning.
- Dataset/license judgement.
- Advisor communication and final claim approval.

## Non-goals

- No automatic experiment execution.
- No private data upload.
- No final paper generation.
- No VGGT success claims without evidence ledger support.
