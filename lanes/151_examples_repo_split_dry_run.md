# Lane 151 - Examples Repo Split Dry-run

Status: dry-run complete.

Round: 170.

## Goal

Run a dry-run split export for `turingresearch-examples` using the local repo
split exporter. This lane does not create a GitHub repository and does not push
any external repository.

## Inputs

- `examples/split_repos/turingresearch-examples/`
- `docs/split-candidate-examples-repo.md`
- `docs/examples-repo-skeleton.md`

## Outputs

- `examples/split_exports/turingresearch-examples/`
- `examples/split_exports/turingresearch-examples/split_manifest.yaml`
- `examples/split_exports/turingresearch-examples/safety_report.md`
- `docs/examples-repo-split-dry-run-report.md`
- `lanes/00_master_ledger.md`

## Dry-run Result

- status: `pass-with-warnings`
- release_blocker: `false`
- omitted_files: none
- human_review_required: `true`

## Checks

- demo only;
- no private data;
- no secrets;
- no raw data;
- no huge artifacts;
- no unsupported claims.

## Boundaries

- No GitHub repository creation.
- No external push.
- No code movement.
- No raw data or huge artifact export.
- No private path read.
- No demo result promoted to observed evidence.
