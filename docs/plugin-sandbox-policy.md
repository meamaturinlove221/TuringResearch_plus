# Plugin Sandbox Policy

Status: implemented minimal.

Round 129 adds a plugin sandbox policy layer for v0.7. It does not implement a
real OS-level sandbox. It defines permission categories, default decisions,
risk reporting, release blockers, and future sandbox requirements.

## Permission Categories

- `read_project_files`
- `write_project_files`
- `network_access`
- `live_api_access`
- `remote_read`
- `remote_write`
- `execute_code`
- `shell_access`
- `secrets_access`
- `artifact_export`

## Default Rules

| Permission | Default | Notes |
| --- | --- | --- |
| `read_project_files` | scoped only | Allowed only with scoped project paths. |
| `write_project_files` | explicit only | Requires explicit enable and future sandbox work. |
| `network_access` | explicit only | Never default; requires explicit enable and future network policy. |
| `live_api_access` | explicit only | Requires explicit live-mode review. |
| `remote_read` | explicit only | May expose private remote metadata. |
| `remote_write` | denied | Remote mutation is blocked. |
| `execute_code` | denied | Runtime code execution is blocked. |
| `shell_access` | denied | Shell access is blocked. |
| `secrets_access` | denied | Secrets access is forbidden. |
| `artifact_export` | explicit only | Export can leak data and needs review. |

## Outputs

`PluginSandboxRiskReport` includes:

- requested permissions;
- per-permission decisions;
- allowed and denied permissions;
- permissions requiring explicit enable;
- severity;
- release blocker flag;
- future sandbox requirements;
- human review flag.

## Safety Boundary

- No OS-level sandbox is implemented.
- No plugin code is executed.
- No unknown code is loaded.
- No network access is used.
- No runtime permissions are granted.
- Reports are policy review artifacts.

## Relationship To Trusted Local Loading

Trusted local plugin loading can load reviewed manifests as metadata. Sandbox
policy describes what would be required before any future runtime behavior.
The two layers together still keep capabilities disabled by default.
