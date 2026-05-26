# GitHub Artifact Sync

Status: v0.4 minimal implementation.

GitHub Artifact Sync imports selected GitHub artifact metadata and safe small
review files from release assets, workflow artifacts, or a private repository
artifact index. It is fake/default by design and does not use network access
unless live mode is explicitly enabled.

## Scope

The minimal implementation supports:

- fake client;
- local JSON fixture index;
- optional live GitHub client;
- private repository token optional;
- no-token graceful skip;
- release asset listing;
- workflow artifact metadata listing;
- selected metadata/small-file import;
- large file omission by default.

## Output

`GitHubArtifactSyncReport` contains:

- `source_repo`
- `source_ref`
- `artifact_list`
- `selected_files`
- `omitted_files`
- `sha256`
- `size`
- `safety_warnings`
- `proposed_imports`
- `requires_human_review`

## Safety Rules

- Default tests and examples do not access the network.
- Do not commit tokens.
- Do not download oversized files by default.
- Do not download raw data.
- Do not download SMPL-X model files.
- Do not overwrite Evidence Ledger automatically.
- Generate proposed imports only.
- Live results are retrieved, not verified.

## VGGT Use

For VGGT / Modal review, GitHub Artifact Sync should bring back only small
review outputs such as `final_status.json`, `failure_report.md`,
`board_inventory.md`, sha256 manifests, and thin summaries. Large arrays,
private configs, raw datasets, and body model files remain omitted or
summary-only.

## Live Mode

Live mode requires:

- `TURINGRESEARCH_ENABLE_LIVE_TESTS=1`
- `GITHUB_TOKEN`

Without explicit opt-in and token, live tests skip or return a typed missing-key
state. Default workflows use fake or fixture input.
