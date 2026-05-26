# Plugin Contribution Guide

Status: design draft.

Round: 161.

This guide describes how future plugin contributions should be prepared for a
possible `turingresearch-plugins` repository.

## Contribution Requirements

Every plugin contribution must include:

- plugin manifest;
- declared plugin type;
- declared capabilities;
- required permissions;
- safety level;
- config schema;
- input and output schema;
- docs;
- tests or test plan;
- compatibility report;
- sandbox policy review;
- extension safety report.

## Default Posture

- Third-party plugins are disabled by default.
- Unknown plugin code is not executed.
- Dynamic entrypoints are not loaded from untrusted manifests.
- Plugin tools cannot override core tools.
- Live features require explicit review.
- Secrets access is forbidden.

## Permission Guidance

| Permission | Default |
| --- | --- |
| `read_project_files` | scoped only |
| `write_project_files` | explicit enable only |
| `network_access` | explicit live flag and review |
| `live_api_access` | explicit live flag and review |
| `remote_read` | explicit enable only |
| `remote_write` | denied |
| `execute_code` | denied |
| `shell_access` | denied |
| `secrets_access` | forbidden |
| `artifact_export` | explicit enable and review |

## What To Submit

1. Manifest file.
2. README explaining purpose and boundaries.
3. Compatibility report.
4. Safety report.
5. Test plan.
6. Evidence that the plugin is disabled by default.

## What Not To Submit

- secrets;
- private paths;
- raw data;
- model payloads;
- executable code requiring trust by default;
- network-only demos;
- claims that review has been completed when it has not.

## Review Outcome

Possible outcomes:

- `accepted-as-disabled-metadata`;
- `needs-more-review`;
- `blocked-by-permission`;
- `blocked-by-security`;
- `rejected`.

No contribution is enabled merely because it is present in a manifest.
