# Lane 141 - Examples Repo Split Design

Status: design complete.

Round: 160.

## Goal

Design the future `turingresearch-examples` repository without actually
splitting the repository or moving example trees.

## Outputs

- `docs/split-candidate-examples-repo.md`
- `docs/examples-repo-skeleton.md`
- `docs/examples-sync-policy.md`
- `examples/split_repos/turingresearch-examples/README.md`
- `examples/split_repos/turingresearch-examples/examples_manifest.yaml`
- `lanes/00_master_ledger.md`

## Intended Future Repo Contents

- `public_demo`
- `project_templates`
- `demo_workspace`
- dashboard demo
- paper demo
- advisor pack demo

## Excluded Content

- private VGGT files
- raw data
- model files
- API keys
- huge artifacts
- real private logs

## Boundaries

- No repository split.
- No code movement.
- No example tree extraction.
- No network access.
- No private path read.
- No raw data packaging.
- No model payload packaging.
- No demo result promoted to observed evidence.
