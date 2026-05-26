# Split Repo Git Init Dry-run

Status: dry-run report generated.

Round: 340.

This report records git initialization dry-run plans for the current
`split_manual/` packs. It does not run `git init`, create repositories, add
remotes, or push external repositories.

## Covered Manual Packs

| Pack | Source bundle | Dry-run file |
| --- | --- | --- |
| `turingresearch-vggt-case` | `split_ready/turingresearch-vggt-case/` | `split_manual/turingresearch-vggt-case/GIT_INIT_DRY_RUN.md` |
| `turingresearch-examples` | `split_ready/turingresearch-examples/` | `split_manual/turingresearch-examples/GIT_INIT_DRY_RUN.md` |

## Shared Dry-run Rules

- Files to include must match the reviewed source bundle manifest.
- Files to exclude include raw data, secrets, private paths, caches, generated
  heavy artifacts, restricted model payloads, and unreviewed local files.
- Initial branch suggestion is `main`.
- Remote URL remains `<approved-real-repository-url>` until a human approves a
  real repository.
- Manual commands are commented reference notes only.
- The flagship TuringResearch repository remains the canonical install, docs,
  release, public API, and star entry point.

## Non-actions

- No `git init` was executed.
- No `.git/` directory was created in split manual packs.
- No GitHub repository was created.
- No external remote was configured.
- No external push was performed.
- No real public URL was written.

## Safety Result

| Check | Result |
| --- | --- |
| dry-run only | pass |
| remote URL placeholder only | pass |
| no auto repo creation | pass |
| no external push | pass |
| no raw data | pass |
| no private path | pass |
| no secrets | pass |
| no unsupported claim | pass |
