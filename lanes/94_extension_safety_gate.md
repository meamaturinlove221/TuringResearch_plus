# Lane 94 - Extension Safety Gate

Status: implemented minimal.

## Scope

Round 113 adds a local extension safety gate for plugin, MCP plugin, skill, and
adapter extension surfaces.

## Added

- `src/turing_research_plus/extension_safety/`
- `contracts/extension_safety.yaml`
- `docs/extension-safety-gate.md`
- `docs/plugin-permission-policy.md`
- extension safety unit and workflow tests

## Permission Rules

- Third-party extensions are disabled by default.
- `execute_code` is forbidden by default.
- `network_access` must be explicit and remains restricted.
- `remote_write` is forbidden by default.
- Secrets access is forbidden.
- Raw data access is restricted and release-blocking.
- Every extension requires manifest and safety report.

## Boundaries

- No third-party code execution.
- No dynamic entrypoint loading.
- No runtime permission grant.
- No network access.
- No automatic extension enabling.
