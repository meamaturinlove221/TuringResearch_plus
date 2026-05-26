# Lane 109 - Trusted Local Plugin Loading

Status: implemented minimal.

Round 128 implements trusted local plugin loading on top of v0.6 manifest-only
plugin architecture. The implementation loads local manifests as metadata only.
It does not execute plugin code, load dynamic entrypoints, or enable
capabilities by default.

## Outputs

- `src/turing_research_plus/plugins/loader.py`
- `src/turing_research_plus/plugins/trust_policy.py`
- `src/turing_research_plus/plugins/local_plugin.py`
- `src/turing_research_plus/plugins/demo_plugins.py`
- `src/turing_research_plus/plugins/loading_report.py`
- `contracts/trusted_local_plugin_loading.yaml`
- `docs/trusted-local-plugin-loading.md`
- `examples/plugins/trusted_local_demo_plugin/`

## Trust Policy

- Built-in demo plugin: allowed as manifest metadata.
- Workspace-local plugin: requires explicit trusted flag.
- Third-party plugin: disabled by default.
- `execute_code`: blocked.
- `network_access` / `live_api`: requires explicit live flag.
- Secrets access: forbidden.

## Boundaries

- No arbitrary third-party Python execution.
- No dynamic entrypoint loading.
- No default network access.
- No system directory writes.
- No core tool override.
- No secret storage.
- No prior project naming.
