# Project Template Generator

Status: scope_locked.

## Problem

New research projects need a repeatable evidence/artifact/advisor/run structure without copying VGGT-specific assumptions.

## VGGT motivating example

A new HART or NeuralBody follow-up should start with a clean project template, not a fork of VGGT files.

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

- contracts/handoff_bundle.yaml, contracts/vggt_evidence.yaml

## Related skills

- $(System.Collections.Hashtable.Skill)

## Required tests

- Fake/default workflow test.
- JSON serialization test.
- Markdown export test.
- Evidence-boundary regression test.
- No secret/raw-data/SMPL-X model packaging test.

## Risks

Templates may accidentally encode VGGT-only claims as generic project truth.

## Done criteria

Generic project skeleton, manifest, evidence placeholders, privacy defaults, fake workspace test.

## Release target

v0.5

## Non-goals

- No complex SaaS.
- No user system.
- No cloud deployment.
- No automatic paper writing.
- No unauthorized data upload.
- No legacy project naming.
