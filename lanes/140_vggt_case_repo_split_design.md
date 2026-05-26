# Lane 140 - VGGT Case Repo Split Design

Status: design complete.

Round: 159.

## Goal

Design the first future split candidate repository,
`turingresearch-vggt-case`, without creating a real repository or moving code.

## Outputs

- `docs/split-candidate-vggt-case-repo.md`
- `docs/vggt-case-repo-skeleton.md`
- `docs/vggt-case-public-safety-checklist.md`
- `examples/split_repos/turingresearch-vggt-case/README.md`
- `examples/split_repos/turingresearch-vggt-case/CASE_STUDY.md`
- `examples/split_repos/turingresearch-vggt-case/PRIVACY.md`
- `examples/split_repos/turingresearch-vggt-case/manifest.yaml`
- `lanes/00_master_ledger.md`

## Decision

`turingresearch-vggt-case` is a promising first future split candidate, but the
current result is design-only. A real repository should not be created until a
dedicated extraction gate passes.

## Boundaries

- Not a VGGT experiment source repo.
- No private data.
- No raw data.
- No SMPL-X files.
- No unsupported experiment claims.
- No SparseConv3D success claim.
- Main TuringResearch repo remains the star and install entry point.
- No network access.
- No repository creation.
- No code movement.
