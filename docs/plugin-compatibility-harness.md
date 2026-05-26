# Plugin Compatibility Harness

Status: implemented minimal.

Round 130 adds a static compatibility harness for local plugin manifests. It
checks whether plugin metadata, capability ids, MCP mapping, permissions,
sandbox policy, docs, and tests line up before a plugin is considered for
review.

## What It Checks

- manifest schema validity;
- capability id syntax and uniqueness;
- required permissions declaration;
- plugin sandbox policy compatibility;
- MCP plugin mapping validity;
- docs presence;
- tests declaration;
- no `core.*` tool override;
- old project naming absence;
- forbidden permission absence.

## Safety Boundary

- Plugin code is not executed.
- Dynamic Python entrypoints are not loaded.
- MCP server is not started.
- Compatibility does not enable plugins.
- Compatibility is not a safety approval.
- Human review remains required.

## Local Helpers

- `check_plugin_compatibility(...)`
- `run_plugin_compatibility_check(...)`
- `run_demo_plugin_compatibility(root)`
- `plugin_compatibility_check(...)`

These are local Python helpers, not public MCP tools.

## Outputs

`PluginCompatibilityReport` includes:

- `plugin_id`
- `status`
- `matrix`
- `findings`
- `capability_ids`
- `mcp_tools`
- `docs`
- `tests`
- `warnings`
- review-only safety flags

Status values:

- `compatible-with-review`
- `needs-review`
- `blocked`

## Demo Fixture

The demo workflow validates:

- `examples/plugins/demo_exporter_plugin/plugin.yaml`
- `examples/plugins/demo_mcp_plugin/registry.yaml`

The generated example report is stored under:

- `examples/plugins/compatibility_reports/demo_exporter_plugin_compatibility.md`

## Limitations

- No plugin runtime is tested.
- No OS sandbox is implemented.
- No marketplace compatibility promise is made.
- Docs and tests checks are path-presence checks, not semantic review.
