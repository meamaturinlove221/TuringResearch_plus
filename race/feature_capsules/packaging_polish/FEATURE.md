# MCP / CLI Packaging Polish

Status: scope_locked.

## Problem

Public release needs sharper CLI/MCP registry consistency, package metadata, and install smoke documentation.

## VGGT motivating example

A maintainer should install TuringResearch Plus, list tools, run fake workflows, and understand live-disabled defaults.

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

- contracts/live_adapters.yaml, contracts/skill_routing.yaml

## Related skills

- $(System.Collections.Hashtable.Skill)

## Required tests

- Fake/default workflow test.
- JSON serialization test.
- Markdown export test.
- Evidence-boundary regression test.
- No secret/raw-data/SMPL-X model packaging test.

## Risks

Packaging polish can accidentally expose unfinished local helper tools as public API.

## Done criteria

CLI entry check, MCP registry check, docs sync, install smoke, no secret defaults.

## Release target

v0.5

## Non-goals

- No complex SaaS.
- No user system.
- No cloud deployment.
- No automatic paper writing.
- No unauthorized data upload.
- No legacy project naming.
