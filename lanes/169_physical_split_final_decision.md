# Round 188 - Physical Split Final Decision

Status: complete.

## Decision

v1.0 should launch the main repository first. Physical split is not a v1.0
launch prerequisite.

## Ready-to-create After Human Approval

1. `turingresearch-vggt-case`
2. `turingresearch-examples`

## Not Split In v1.0

- core
- paper
- artifact
- dashboard
- plugins

## Rationale

- Protect flagship star concentration.
- Avoid release-before-launch complexity.
- Keep install, quickstart, docs, release gates, and product narrative in the
  main repository.
- Treat child repos as later growth points, not as v1.0 blockers.
- Split after public launch feedback or explicit maintainer approval.

## Verification

- Decision docs updated.
- Pre-push check pending final scan.

## Boundaries

- No GitHub repository creation.
- No code movement.
- No external child repository push.
- No install-path change.
- No release action.
