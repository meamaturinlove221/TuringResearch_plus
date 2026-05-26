# Plugin Permission Policy

Status: local policy for Extension Safety Gate.

## Permission Decisions

| Permission | Default Decision | Reason |
| --- | --- | --- |
| `read_local_files` | allow with review | Needed by many local review workflows. |
| `write_local_files` | restricted | Can modify workspace outputs; requires explicit review. |
| `network_access` | restricted | Must never happen by default. |
| `live_api` | restricted | Requires explicit live-mode opt-in and environment review. |
| `remote_read` | restricted | May expose private paths or remote artifact metadata. |
| `remote_write` | forbidden | Remote mutation is outside the extension gate. |
| `execute_code` | forbidden | Third-party code execution is not supported. |
| `export_artifacts` | restricted | Export can leak data; requires privacy review. |
| `package_release` | restricted | Release packaging requires public-release hygiene gates. |

## Data Boundaries

- Secrets access is forbidden.
- Raw data access is restricted and release-blocking by default.
- Private model files are restricted or forbidden depending on license and
  payload type.
- Extension safety reports do not redact or delete source files.

## Relationship To Other Gates

- Plugin Architecture provides manifest declarations.
- MCP Plugin Registry controls tool exposure declarations.
- Skill Marketplace is local-only documentation.
- Privacy / Data Policy scans repository and artifact contents.
- Public Release Hardening remains the final release hygiene gate.
