# Module Public API Contracts

Status: contract draft index.

Round: 154.

This document summarizes the public API contract drafts for future module and
repository boundaries. It does not move code, split repositories, add target
namespaces, or change imports.

## Purpose

The contracts define what each future module namespace may expose as public
surface when TuringResearch moves toward clearer namespace and repository
boundaries. They are intentionally conservative:

- internal helpers are not public API;
- experimental modules are not marked stable;
- `turing_research_plus` remains the compatibility namespace;
- default behavior remains local-first and fake/demo-first;
- live, plugin, export, and case-study behavior remains review-gated.

## Contract Files

| Contract | Future namespace | Stability | Current role |
| --- | --- | --- | --- |
| `contracts/core_api.yaml` | `turing_research_core` | beta | Workspace, evidence status, privacy, quality, templates. |
| `contracts/paper_api.yaml` | `turing_research_paper` | experimental | Paper review, scaffold, method, related work, writing, deep review. |
| `contracts/artifact_api.yaml` | `turing_research_artifact` | experimental | Artifact audit, handoff, remote metadata, run ingest. |
| `contracts/experiment_api.yaml` | `turing_research_experiment` | beta | Routes, hard gates, failures, run status, comparison. |
| `contracts/dashboard_api.yaml` | `turing_research_dashboard` | experimental | UI, dashboard, advisor export, case study, vault UI. |
| `contracts/plugin_api.yaml` | `turing_research_plugins` | experimental | Plugin manifests, MCP registry, safety, compatibility, capability and skill catalogs. |
| `contracts/case_api.yaml` | `turing_research_cases` | experimental | Public demos, case studies, benchmark replay, example metadata. |

## Required Contract Fields

Each module API contract must include:

- `module_name`
- `purpose`
- `public_models`
- `public_functions_tools`
- `input_schema`
- `output_schema`
- `stability`
- `internal_only_modules`
- `deprecated_aliases`
- `tests`
- `docs`

Allowed stability values:

- `experimental`
- `beta`
- `stable`
- `internal`

## Compatibility Rule

All contracts name a future namespace, but the current compatibility namespace
remains `turing_research_plus`. The old namespace must not be removed before
v1.0 or later.

## Public Surface Rules

- Public models should be DTOs, reports, manifests, or documented plan objects.
- Public tools should be local helper surfaces, not hidden live execution.
- Internal helper modules, fixture builders, live client internals, optional
  backend internals, and case-specific helper code should stay internal.
- Experimental modules must not be documented as stable.
- Docs must clearly state fake/demo, optional-live, and human-review
  boundaries.

## Split Readiness Use

These contracts are a prerequisite for future repository split evaluation.
A module is not split-ready merely because a contract exists. It still needs:

- stable API;
- complete docs;
- passing independent tests;
- no private data;
- no unresolved license risk;
- demo availability;
- independent user value;
- main repo compatibility.

## Next Steps

1. Keep these contracts in draft status while namespace refactor is planning.
2. Add import compatibility tests when target namespaces are created.
3. Promote individual contracts only after implementation and integration gates.
4. Re-run module boundary audit before any actual repository split.
