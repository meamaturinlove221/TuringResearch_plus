# Lane 111 - Plugin Compatibility Test Harness

Status: implemented minimal.

Round 130 implements the v0.7 plugin compatibility harness. It validates local
plugin metadata across manifest schema, capability ids, declared permissions,
MCP mapping, docs/tests, naming, and sandbox policy. It does not execute plugin
code, start MCP, enable plugins, or promote registry entries.

## Outputs

- `src/turing_research_plus/plugins/compatibility.py`
- `src/turing_research_plus/plugins/compat_test_runner.py`
- `src/turing_research_plus/plugins/compat_report.py`
- `contracts/plugin_compatibility.yaml`
- `docs/plugin-compatibility-harness.md`
- `examples/plugins/compatibility_reports/demo_exporter_plugin_compatibility.md`

## Checks

- manifest schema valid
- capability ids valid
- required permissions declared
- safety policy satisfied
- MCP mapping valid
- docs present
- tests declared
- no core tool override
- no old project naming
- no forbidden permission

## Boundaries

- No plugin execution.
- No dynamic entrypoint loading.
- No MCP server startup.
- No default networking.
- No plugin enablement.
- Compatibility remains a review artifact.
