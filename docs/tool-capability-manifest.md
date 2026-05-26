# Tool Capability Manifest

Status: implemented minimal.

Round 111 adds a static, review-only capability manifest for TuringResearch Plus
tools, adapters, exporters, and workflows. The manifest is meant for docs,
skill routing, MCP plugin registry review, and public release summaries.

## What It Contains

Each capability entry records:

- `capability_id`
- `name`
- `category`
- optional `tool_name`
- optional `command`
- `module`
- `input_model`
- `output_model`
- `live_mode`
- `fake_mode`
- `required_env`
- `safety_level`
- `status`
- `docs`
- `tests`
- `related_skills`

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

## Safety Boundary

- The collector uses a static catalog.
- It does not execute tools.
- It does not start an MCP server.
- It does not perform live discovery.
- Live capabilities remain opt-in and list their required environment gates.
- Capability entries are release documentation aids, not proof that a research
  claim is verified.

## Local Helpers

- `capabilities_collect()`
- `capabilities_markdown()`
- `capabilities_export_json(path)`

These helpers are local Python surfaces, not public MCP tools.
