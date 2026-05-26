# Module Public API Surface

Status: audit artifact.

Round: 152.

This document records the current public-facing and semi-public module surfaces
that matter for future split readiness. It is not a promise that every helper is
stable public API.

## Stable Public Surface Today

| Surface | Current role | Split implication |
| --- | --- | --- |
| package name `turingresearch-plus` | install/package identity | Must remain in flagship until release strategy changes. |
| import packages `turing_research`, `turing_research_plus` | package import surface | Must remain stable across patch releases. |
| CLI entrypoints `turingresearch-plus`, `turingresearch-plus-mcp` | local smoke and MCP entry path | Keep in flagship; satellites should not replace this path. |
| contracts under `contracts/` | schema and release boundary docs | Can be copied or versioned later, but source of truth is main repo for now. |
| docs index and README | public onboarding | Must stay in flagship. |
| public demo examples | fake/default onboarding | Can later become `turingresearch-examples` after demo safety review. |

## Semi-public Module Surfaces

| Group | Semi-public surfaces | Stability |
| --- | --- | --- |
| core | workspace registry, project templates, privacy scan, quality gate | medium; should stay in main repo. |
| paper | paper scaffold, method section, related work draft, experiment section, deep review | medium-low; needs paper beta API stabilization. |
| artifact | artifact audit, handoff bundles, remote artifact metadata, run ingest | medium-low; live boundaries and safety docs need hardening. |
| experiment | routes, hard gates, failure taxonomy, run comparison | medium; keep near core until route semantics settle. |
| dashboard_export | dashboard renderer, advisor export, optional PDF/PPTX, export quality, case study | medium; candidate for later split after DTOs stabilize. |
| plugins | plugin manifest, trust policy, sandbox policy, compatibility harness, MCP registry | medium; split only after circular dependency cleanup. |
| examples_cases | demo projects, VGGT dogfooding case, benchmark replay | medium; best early standalone showcase candidate. |

## API Stabilization Needs

- Define stable DTOs for dashboard cards and local dashboard server inputs.
- Define stable export plan/result models for Markdown/PDF/PPTX outputs.
- Define stable paper section status and claim-safety models.
- Define stable plugin manifest to MCP mapping boundaries.
- Define stable case-study redaction and claim-safety reports.
- Define adapter safety interfaces for remote artifact modules.

## What Is Not Stable Public API

- Internal helper functions.
- Test fixture builders.
- Case-specific VGGT helper logic.
- Live adapter internals.
- Optional backend internals.
- Historical lane text.
- Planning-only feature capsule contracts.

## Split-readiness API Rule

A module cannot split until its public API can be described in one page, tested
independently, and used by the main repository without importing private
implementation details.
