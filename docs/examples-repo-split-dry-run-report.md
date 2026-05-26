# Examples Repo Split Dry-run Report

Status: dry-run complete.

Round: 170.

This report records a dry-run export for the future
`turingresearch-examples` split candidate. It does not create a GitHub
repository, does not push to any remote, and does not approve publication.

## Source And Output

- Source: `examples/split_repos/turingresearch-examples/`
- Output: `examples/split_exports/turingresearch-examples/`
- Manifest: `examples/split_exports/turingresearch-examples/split_manifest.yaml`
- Safety report: `examples/split_exports/turingresearch-examples/safety_report.md`

## Exported Files

- `README.md`
- `examples_manifest.yaml`
- `split_manifest.yaml`
- `safety_report.md`

## Dry-run Result

- status: `pass-with-warnings`
- release_blocker: `false`
- omitted_files: none
- requires_human_review: `true`

The warning is a policy mention: `README.md` lists private advisor feedback as
excluded content. That is a non-blocking safety reminder, not leaked private
feedback.

## Required Checks

| Check | Result |
| --- | --- |
| demo only | pass |
| no private data | pass |
| no secrets | pass |
| no raw data | pass |
| no huge artifacts | pass |
| no unsupported claims | pass |

## Boundaries

- No real repository was created.
- No external repository was pushed.
- No branch was created.
- No raw data, model files, API keys, huge artifacts, or real private logs were exported.
- Demo outputs are not research success evidence.
- Human review is still required before any physical split.
