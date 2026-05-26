---
name: Plugin proposal
about: Propose a plugin manifest, plugin metadata, or plugin integration idea
title: "[Plugin]: "
labels: plugin, plugin-safety
assignees: ""
---

## Summary

Describe the proposed plugin.

## Expected Behavior

What should the plugin help users do?

## Actual / Current Gap

What is missing from the current plugin system or manifest registry?

## Reproduction Or Example Workflow

Describe a public-safe fake/default workflow that would demonstrate the plugin.
Do not include secrets, private paths, raw data, or restricted model files.

## Plugin Type

- Metadata-only plugin: yes / no
- MCP tool mapping: yes / no
- Live adapter integration: yes / no
- Third-party dependency: yes / no

## Requested Permissions

Check every permission the plugin would need:

- [ ] Read public demo files
- [ ] Read project files
- [ ] Write project files
- [ ] Network access
- [ ] Live API access
- [ ] Remote read
- [ ] Remote write
- [ ] Execute code
- [ ] Shell access
- [ ] Secrets access
- [ ] Artifact export

## Permission Justification

Explain why each requested permission is necessary.

## Safety Boundary

- Unknown third-party plugins must stay disabled by default.
- `execute_code` is denied by default.
- Shell access is denied by default.
- Secrets access is forbidden.
- Live/network permission requires explicit review and opt-in.

## Environment

- TuringResearch Plus version:
- OS:
- Python version:
- Live mode enabled: yes / no
- Plugins enabled: yes / no

## Data Sensitivity

- Data involved: public demo / public data / private data / unknown
- Does this plugin need raw data? yes / no
- Does this plugin need private local paths? yes / no
- Does this plugin need restricted model files? yes / no

## Tests

What manifest, compatibility, sandbox, MCP, or workflow tests should cover this?

## Safety / Privacy Notes

- Do not upload API keys, tokens, `.env` files, or credentials.
- Do not upload raw data.
- Do not upload SMPL-X model files or other restricted model payloads.
- Do not upload private local paths.

## Checklist

- [ ] I listed requested permissions.
- [ ] I did not request secrets access.
- [ ] I did not require unknown plugin execution by default.
- [ ] I included a fake/default test idea.
- [ ] I did not include private data or credentials.
