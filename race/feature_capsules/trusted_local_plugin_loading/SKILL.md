# Trusted Local Plugin Loading Skill

Status: planning skill draft.

Use this skill for v0.7 trusted local plugin loading planning, contract review,
and test planning. It does not execute plugin code.

## Inputs

- plugin manifest
- trusted allowlist
- extension safety report
- compatibility harness result

## Outputs

- TrustedPluginLoadPlan
- PluginLoadDecision
- PluginLoadSafetyReport

## Safety Rules

- Do not execute unknown plugin code.
- Do not use network access by default.
- Do not read private VGGT paths.
- Do not package secrets, raw data, or private model files.
- Do not mark fake/demo/planned results as observed.

## Related Contracts

- trusted_local_plugin_loading.yaml
- plugin_architecture.yaml
- extension_safety.yaml
