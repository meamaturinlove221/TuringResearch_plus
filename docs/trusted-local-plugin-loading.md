# Trusted Local Plugin Loading

Status: implemented minimal.

Round 128 adds a trusted local plugin loading layer on top of the v0.6
manifest-only plugin architecture. It still does not execute plugin code. It
loads local plugin manifests as metadata, validates them, applies trust policy,
runs the extension safety gate, and exposes plugin capabilities as
disabled-by-default declarations.

## What It Does

- Loads `plugin.yaml` from a local path.
- Validates the manifest with the existing plugin validator.
- Applies trust policy.
- Converts plugin permissions into an extension safety reference.
- Runs the extension safety gate.
- Produces `PluginLoadingReport`.
- Exposes capabilities only as disabled-by-default metadata.

## Trust Policy

| Source | Decision |
| --- | --- |
| built-in demo plugin | allowed as manifest metadata |
| workspace-local plugin | requires explicit trusted flag |
| third-party plugin | disabled by default |
| plugin with `execute_code` | blocked |
| plugin with `network_access` or `live_api` | requires explicit live flag |
| plugin with secrets access | forbidden |
| plugin with dynamic Python entrypoint | blocked |

## Safety Boundary

- No arbitrary third-party Python code execution.
- No dynamic entrypoint loading.
- No default networking.
- No system directory writes.
- No core tool override.
- No secret storage.
- No capability is enabled by default.
- Human review is required.

## Example

```python
from pathlib import Path

from turing_research_plus.plugins import PluginTrustSource, load_trusted_local_plugin

report = load_trusted_local_plugin(
    Path("examples/plugins/trusted_local_demo_plugin/plugin.yaml"),
    source=PluginTrustSource.BUILT_IN_DEMO,
)
```

The returned report is review material. It is not a runtime plugin execution
handle.

## Non-goals

- No online marketplace install.
- No unknown third-party plugin execution.
- No automatic permission grant.
- No live service call.
- No public MCP tool registration.
