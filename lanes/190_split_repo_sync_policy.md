# Round 212 - Split Repo Sync Policy

Status: completed.

## Goal

Define how the flagship repository and future split repositories should stay in
sync without implementing automatic synchronization.

## Outputs

- Added `docs/v1.1.0-split-repo-sync-policy.md`.
- Added `docs/v1.1.0-split-repo-manual-sync-sop.md`.
- Added `docs/v1.1.0-split-repo-versioning-policy.md`.
- Added `split_ready/SPLIT_SYNC_POLICY.md`.
- Added `split_ready/split_manifest.yaml`.

## Policy

- The flagship TuringResearch repository is the source of truth.
- Spokes are public demo or case mirrors.
- Spokes do not introduce core framework functionality.
- Spoke README files must route readers back to the flagship.
- Spoke issues should flow back to flagship policy and issue triage.
- Safety gates are required before every manual sync.

## Non-actions

- No automatic sync implementation.
- No GitHub repository creation.
- No external remote push.
- No install path change.
