# Cross-project Evidence Graph

Status: v0.6 minimal implementation.

Round 106 adds a local JSON / Markdown cross-project graph. It compares
projects in a workspace for reusable patterns across claims, artifacts,
methods, failures, and routes.

## Purpose

The graph helps answer:

- which projects share a method pattern;
- which projects share a failure type;
- which artifact patterns can be reused;
- which route / hard gate patterns can be reused;
- which claims are missing evidence.

It does not move proof between projects. Evidence remains scoped to the source
project.

## Models

- `CrossProjectEvidenceGraph`
- `CrossProjectNode`
- `CrossProjectEdge`
- `SharedPattern`
- `ReusableTemplateHint`
- `CrossProjectComparison`

## Local Helpers

- command: `turing workspace graph`
- local helper: `workspace_cross_project_graph`
- output: `CrossProjectEvidenceGraph`

- command: `turing workspace graph-md`
- local helper: `workspace_cross_project_markdown`
- output: Markdown

These helpers are local Python helpers and are not frozen public MCP APIs.

## Safety Policy

- No network access.
- No graph database.
- No private project discovery.
- No automatic data ingestion.
- No automatic evidence promotion.
- No evidence transfer between projects.
- All shared patterns require human review.

## Demo Workspace

The demo graph is generated from:

`examples/workspaces/demo_workspace/workspace.yaml`

Outputs:

- `examples/workspaces/demo_workspace/cross_project_graph.json`
- `examples/workspaces/demo_workspace/cross_project_summary.md`

The demo compares a VGGT review case mirror with a fake medical imaging project.
The shared patterns are reuse hints only. They are not experiment results.

## Limitations

- Pattern extraction is intentionally shallow and text based.
- The graph is not a complete ontology.
- It does not validate claims.
- It does not infer final research conclusions.
- It does not read private projects.
