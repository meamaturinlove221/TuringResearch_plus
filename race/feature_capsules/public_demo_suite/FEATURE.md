# Public Demo Suite

Status: scope_locked.

## Problem

The repo has many fake workflows, but public users need a small curated demo path that shows value without live services.

## VGGT motivating example

VGGT demo should run from fixtures through remote artifact report, dashboard, comparison, paper digest, and advisor Markdown bundle.

## User story

As a TuringResearch operator, I want this capability to turn existing review artifacts into safer, clearer project workflows without weakening evidence boundaries.

## Inputs

- Existing Markdown and JSON review artifacts.
- v0.4 remote artifact, dashboard, paper digest, or advisor export outputs.
- Project manifests and source refs.
- Manual review notes when needed.

## Outputs

- $(System.Collections.Hashtable.Output).
- JSON-serializable report.
- Markdown review summary.
- Required human-review flags.

## Data model

- status: planned / generated / blocked / requires-human-review.
- source refs and sha256 metadata where applicable.
- limitations, omitted items, and safety warnings.
- no verified result unless evidence explicitly supports it.

## Proposed commands / tools

- command: $(System.Collections.Hashtable.Command)
- tool: $(System.Collections.Hashtable.Tool)
- output: $(System.Collections.Hashtable.Output)

## Related contracts

- contracts/remote_artifacts.yaml, contracts/advisor_export.yaml

## Related skills

- $(System.Collections.Hashtable.Skill)

## Required tests

- Fake/default workflow test.
- JSON serialization test.
- Markdown export test.
- Evidence-boundary regression test.
- No secret/raw-data/SMPL-X model packaging test.

## Risks

Demos can be mistaken for real experimental validation.

## Done criteria

Curated fake demo suite, README, expected outputs, CI-safe tests, no live credentials.

## Release target

v0.5

## Non-goals

- No complex SaaS.
- No user system.
- No cloud deployment.
- No automatic paper writing.
- No unauthorized data upload.
- No legacy project naming.
