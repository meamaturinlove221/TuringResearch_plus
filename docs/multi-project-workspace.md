# Multi-project Workspace

Status: v0.6 minimal implementation.

Round 104 adds a local multi-project workspace registry. It lets
TuringResearch Plus list, summarize, and export overview Markdown for multiple
research projects without ingesting data automatically.

## Purpose

The workspace layer makes VGGT one project case among many. It keeps project
state visible while preserving evidence boundaries:

- workspace index is not an evidence source;
- projects remain isolated by `project_id`;
- missing paths are reported instead of silently ignored;
- demo projects stay explicitly fake/demo;
- every overview requires human review.

## Models

- `Workspace`
- `WorkspaceProject`
- `WorkspaceProjectSummary`
- `WorkspaceOverview`
- `WorkspaceContext`

## Local Helpers

- command: `turing workspace load`
- tool: `workspace.load`
- output: `ProjectIndex`

- command: `turing workspace overview`
- tool: `workspace.overview`
- output: `WorkspaceOverview`

- command: `turing workspace overview-md`
- tool: `workspace.overview_markdown`
- output: Markdown

These helpers are local Python helpers and are not frozen public MCP APIs.

## Registry Format

The registry is a local JSON or simple YAML file. The demo fixture lives at:

`examples/workspaces/demo_workspace/workspace.yaml`

Required project fields:

- `project_id`
- `project_type`
- `project_root`
- `docs_path`
- `evidence_path`
- `artifacts_path`
- `advisor_pack_path`
- `routes_path`
- `status`
- `privacy_level`
- `requires_human_review`

## Demo Workspace

The demo workspace includes:

- `vggt_human_prior`: a public-demo mirror of the VGGT review case.
- `demo_medical_imaging`: a fake/demo non-VGGT project with no real patient
  data.

Both are review-only. Neither is a real experiment result.

## Safety Policy

- No network access.
- No upload.
- No automatic data ingestion.
- No private VGGT path reads.
- No evidence promotion.
- No demo result marked observed.
- No workspace summary treated as a source of truth.

## Limitations

- No graph database.
- No SaaS workspace.
- No cloud account system.
- No automatic project discovery outside explicit registry roots.
- No real privacy scanner yet.
- No cross-project evidence graph yet.
