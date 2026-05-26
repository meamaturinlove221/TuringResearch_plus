# Lane 150 - VGGT Case Split Dry-run

Status: dry-run complete.

Round: 169.

## Goal

Run a dry-run split export for `turingresearch-vggt-case` using the local
split exporter. This lane does not create a GitHub repository and does not push
any external repository.

## Inputs

- `examples/split_repos/turingresearch-vggt-case/`
- `docs/split-candidate-vggt-case-repo.md`
- `docs/vggt-case-public-safety-checklist.md`

## Outputs

- `examples/split_exports/turingresearch-vggt-case/`
- `examples/split_exports/turingresearch-vggt-case/split_manifest.yaml`
- `examples/split_exports/turingresearch-vggt-case/safety_report.md`
- `examples/split_exports/turingresearch-vggt-case/README.md`
- `docs/vggt-case-split-dry-run-report.md`
- `lanes/00_master_ledger.md`

## Dry-run Result

- status: `pass-with-warnings`
- release_blocker: `false`
- omitted_files: none
- human_review_required: `true`

## Checks

- no private local paths;
- no raw data;
- no SMPL-X payload;
- no unsupported claims;
- no fake observed;
- no secrets;
- README clear;
- main repo referenced as flagship.

## Boundaries

- No GitHub repository creation.
- No external push.
- No code movement.
- No raw data or model payload export.
- No private path read.
- No experiment success claim.
