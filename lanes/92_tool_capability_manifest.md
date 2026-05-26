# Lane 92 - Tool Capability Manifest

Status: implemented minimal.

## Scope

Round 111 adds a static, review-only capability manifest for TuringResearch Plus
tools, adapters, exporters, and workflows.

## Added

- `src/turing_research_plus/capabilities/`
- `contracts/tool_capability_manifest.yaml`
- `docs/tool-capability-manifest.md`
- `docs/capability-index.md`
- `examples/capabilities/turingresearch_capabilities.json`
- capability unit and workflow tests

## Covered Categories

- evidence
- artifact
- visual
- advisor
- pdf
- paper
- citation
- collision
- related work
- route
- failure
- dashboard
- remote artifact
- handoff
- plugin
- workspace

## Boundaries

- Static catalog only.
- No live discovery.
- No tool execution.
- No MCP server start.
- No marketplace publish.
- Capability entries are documentation and routing aids, not verified research
  claims.
