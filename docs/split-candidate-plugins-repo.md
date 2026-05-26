# Split Candidate: `turingresearch-plugins`

Status: design draft.

Round: 161.

This document designs the future `turingresearch-plugins` repository. No real
repository is created in this round and no plugin framework code is moved out
of the flagship monorepo.

## Purpose

`turingresearch-plugins` would be a public plugin catalog and contribution
workspace for TuringResearch Plus. It would focus on plugin manifests,
compatibility reports, review checklists, and policy documentation.

## Flagship Relationship

The main TuringResearch Plus repository keeps the core plugin framework:

- plugin manifest models;
- plugin registry validation;
- MCP plugin registry;
- capability manifest;
- trusted local plugin loading;
- sandbox policy;
- extension safety gate;
- compatibility harness.

The split plugin repo should link back to the flagship as the install, runtime,
and policy source of truth.

## Allowed Content

- plugin manifests;
- compatibility reports;
- plugin contribution docs;
- plugin review checklists;
- disabled-by-default registry drafts;
- fake/demo plugin examples;
- safety metadata.

## Forbidden Content

- executable third-party plugin code by default;
- unknown Python entrypoints;
- shell scripts that run plugin behavior;
- secrets or credentials;
- raw data;
- private project paths;
- model payloads;
- plugins enabled by default;
- `core.*` tool overrides.

## Safety Rules

- Third-party plugins are disabled by default.
- Plugin manifest is required.
- Sandbox policy review is required.
- `execute_code` is denied by default.
- Secrets access is forbidden.
- Network/live access must be explicit and review-gated.
- Human review is required before any plugin is enabled.

## Current Decision

Design-only. The plugin repo is not ready to split until plugin compatibility,
sandbox policy, MCP mapping, and review workflow can be run independently
without weakening the flagship safety model.
