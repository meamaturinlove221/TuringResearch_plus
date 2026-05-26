# Extension Safety Gate

Status: implemented minimal.

Round 113 adds a unified safety gate for plugins, MCP plugins, skills, and
adapters. It validates manifest declarations and requested permissions before
an extension can be considered for enablement, registry exposure, export, or
release packaging.

## Covered Extension Kinds

- plugin
- mcp_plugin
- skill
- adapter

## Permission Types

- `read_local_files`
- `write_local_files`
- `network_access`
- `live_api`
- `remote_read`
- `remote_write`
- `execute_code`
- `export_artifacts`
- `package_release`

## Default Rules

- Third-party extensions are disabled by default.
- `execute_code` is forbidden by default.
- `network_access` must be explicit and remains restricted.
- `remote_write` is forbidden by default.
- Secrets access is forbidden.
- Raw data access is restricted.
- Every extension requires a manifest and safety report.

## Output

`ExtensionSafetyReport` records:

- extension id and kind
- validation status
- permission decisions
- findings
- release blocker flag
- human review requirement
- proof that no extension code was executed or loaded

## Boundary

- No third-party code execution.
- No unknown Python entrypoint loading.
- No runtime permission grants.
- No network access.
- No automatic enabling of extensions.
- Reports are review aids, not trust guarantees.
