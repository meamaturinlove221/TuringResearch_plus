# TuringResearch Plus Feature Capsule: git_based_context_handoff

## Problem

TuringResearch Plus needs a safe way to move durable context between a main
machine, VGGT machine, and remote pod workflow without copying full sessions or
unsafe data.

## VGGT motivating example

The VGGT / Modal route needs route spec, hard gates, artifact requirements,
failure taxonomy, and advisor intent to travel together. Raw datasets, secrets,
and body model files must not travel.

## User story

As a maintainer, I want to export a Git-friendly context package so another
machine or pod can continue work with enough context and return structured
outputs for review.

## Inputs

- Evidence Ledger summary
- Experiment Route DSL spec
- Hard Gate report
- Failure Taxonomy summary
- Handoff Bundle manifest
- Advisor intent
- Memory summary

## Outputs

- `ContextPackage`
- `MemoryPolicy`
- `GitTransportPolicy`
- `HandoffSafetyPolicy`
- `PROJECT_CONTEXT.md`
- `MEMORY.md`
- `HANDOFF_MANIFEST.yaml`

## Data model

- `ContextPackage`
- `MemoryPolicy`
- `GitTransportPolicy`
- `HandoffSafetyPolicy`

## Proposed commands / tools

- command: `turing context package`
- tool: design-only `context.git_handoff_package`
- output: `ContextPackage`

This is not a public MCP API until a later contracts-first implementation
round.

## Related contracts

- `contracts/git_context_handoff.yaml`
- `contracts/handoff_bundle.yaml`
- `contracts/experiment_route.yaml`

## Related skills

- `turingresearch-master-orchestrator`
- `turingresearch-cache-and-ledger`
- `turingresearch-fusion-context-management`

## Required tests

- context package contains required files;
- `.env`, secrets, raw data, and body model files are omitted;
- memory is marked summary-only;
- Git transport does not imply execution;
- import creates proposed updates only.

## Risks

- Accidentally reintroducing session teleport.
- Treating memory as source of truth.
- Leaking secrets or raw data.
- Confusing transport with remote execution.

## Done criteria

- Design docs and contracts are accepted.
- Safety policy aligns with v0.2 handoff bundle.
- Implementation round can create models without changing public API.

## Release target

v0.3 Sprint 1.

## Upstream learning note

Inspired by the Neocortica-Session Git handoff signal, but TuringResearch Plus
does not copy scripts or depend on Claude-specific paths.

## Relation to v0.2 modules

Builds on Handoff Bundle, Run Ingestor, Evidence Ledger, Artifact Auditor,
Advisor Pack, Experiment Route DSL, Hard Gates, and Failure Taxonomy.
