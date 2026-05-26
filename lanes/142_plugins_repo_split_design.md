# Lane 142 - Plugins Repo Split Design

Status: design complete.

Round: 161.

## Goal

Design the future `turingresearch-plugins` repository without splitting the
repository or moving plugin framework code.

## Outputs

- `docs/split-candidate-plugins-repo.md`
- `docs/plugins-repo-skeleton.md`
- `docs/plugin-contribution-guide.md`
- `docs/plugin-review-checklist.md`
- `examples/split_repos/turingresearch-plugins/README.md`
- `examples/split_repos/turingresearch-plugins/PLUGIN_POLICY.md`
- `examples/split_repos/turingresearch-plugins/plugins_manifest.yaml`
- `lanes/00_master_ledger.md`

## Required Safety Position

- Third-party plugins disabled by default.
- Plugin manifest required.
- Sandbox policy required.
- No `execute_code` by default.
- No secrets access.
- Human review required.
- Main repo keeps core plugin framework.

## Boundaries

- No repository split.
- No code movement.
- No plugin execution.
- No dynamic entrypoint loading.
- No network access.
- No secrets.
- No core tool override.
