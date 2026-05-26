# Plugins Repo Skeleton

Status: design draft.

Round: 161.

This document describes the proposed skeleton for a future
`turingresearch-plugins` repository.

## Proposed Tree

```text
turingresearch-plugins/
  README.md
  PLUGIN_POLICY.md
  plugins_manifest.yaml
  plugins/
  compatibility_reports/
  review_checklists/
```

Round 161 only creates:

```text
examples/split_repos/turingresearch-plugins/
  README.md
  PLUGIN_POLICY.md
  plugins_manifest.yaml
```

## Required README Claims

- This repo is a future plugin catalog, not the core plugin framework.
- The main repo keeps core plugin loading and safety code.
- Third-party plugins are disabled by default.
- Plugin manifests are required.
- Sandbox policy and extension safety reports are required.
- No unknown plugin code is executed.

## Required Manifest Fields

- `repo_id`
- `status`
- `flagship_repo`
- `core_framework_location`
- `plugin_defaults`
- `required_review_artifacts`
- `forbidden_permissions`
- `release_blockers`
- `requires_human_review`

## Extraction Rule

Do not extract the plugin repo until the plugin review workflow is independent,
repeatable, and still keeps unknown plugins disabled by default.
