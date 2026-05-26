# VGGT Case Split Dry-run Report

Status: dry-run complete.

Round: 169.

This report records a dry-run export for the future
`turingresearch-vggt-case` split candidate. It does not create a GitHub
repository, does not push to any remote, and does not approve publication.

## Source And Output

- Source: `examples/split_repos/turingresearch-vggt-case/`
- Output: `examples/split_exports/turingresearch-vggt-case/`
- Manifest: `examples/split_exports/turingresearch-vggt-case/split_manifest.yaml`
- Safety report: `examples/split_exports/turingresearch-vggt-case/safety_report.md`

## Exported Files

- `README.md`
- `CASE_STUDY.md`
- `PRIVACY.md`
- `manifest.yaml`
- `split_manifest.yaml`
- `safety_report.md`

## Dry-run Result

- status: `pass-with-warnings`
- release_blocker: `false`
- omitted_files: none
- requires_human_review: `true`

The warning is a policy mention: `PRIVACY.md` says private advisor feedback is
excluded. That is kept as a non-blocking reminder, not as leaked private
feedback.

## Required Checks

| Check | Result |
| --- | --- |
| no private local paths | pass |
| no raw data | pass |
| no SMPL-X payload | pass |
| no unsupported claims | pass |
| no fake observed | pass |
| no secrets | pass |
| README clear | pass |
| main repo referenced as flagship | pass |

## Boundaries

- No real repository was created.
- No external repository was pushed.
- No branch was created.
- No raw data or model payload was exported.
- No private VGGT path was read.
- No VGGT or SparseConv3D success claim was added.
- Human review is still required before any physical split.
