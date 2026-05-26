# Round 193 - Split Execution Go/No-Go

Status: complete.

## Goal

Decide whether to execute physical repository split before the v1.0 public
launch.

## Output

- `docs/v1.0.0-split-execution-go-no-go.md`
- `docs/v1.0.0-split-release-blockers.md`
- `docs/v1.0.0-split-next-actions.md`

## Decision

- No physical split before v1.0 public launch.
- Launch the flagship main repository first.
- After launch, prioritize `turingresearch-vggt-case`.
- Treat `turingresearch-examples` as the second candidate.
- Delay `turingresearch-plugins` until real ecosystem demand exists.
- Keep core, paper, artifact, dashboard, and plugin framework implementation in
  the flagship.

## Verification

- Name integrity: passed.
- Pre-push scan: passed with allowed safety-boundary wording.

## Boundaries

- No GitHub repository creation.
- No external child repository push.
- No nonexistent GitHub repository URL.
- No code movement.
- No install path change.
