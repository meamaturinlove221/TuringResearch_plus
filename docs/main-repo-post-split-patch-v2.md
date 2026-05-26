# Main Repo Post-split Patch v2

Status: documentation patch applied.

Round: 342.

This patch updates the flagship README and split documentation so future split
repo publication can be understood without pretending that the child
repositories already exist.

## What Changed

- README now describes future split repositories as planned / manual-ready.
- README links to `docs/split-manual-packs.md`.
- `docs/future-split-repos.md` now distinguishes `split_ready/` source bundles
  from `split_manual/` human execution packs.
- `docs/split-ready-bundles.md` now records the main repo protection boundary.
- `docs/split-manual-packs.md` documents the manual packs and their safety
  gates.

## Required Boundaries

- Only planned / manual-ready language is used.
- No fake URL is written.
- No nonexistent real URL is written.
- The main repository remains the install entry.
- Child repositories are case/demo spokes only.
- Star attention remains centered on the flagship repository.
- No automatic repository creation, external push, or release publication is
  implied.

## Current Split Status

| Candidate | Status | Main repo relationship |
| --- | --- | --- |
| `turingresearch-vggt-case` | split-ready and manual-ready | case-study spoke, points back to flagship |
| `turingresearch-examples` | split-ready and manual-ready | examples spoke, points back to flagship |
| `turingresearch-plugins` | deferred | plugin policy draft, not a publication target |

## Human Next Step

The next action is human review, not automation. A maintainer may review the
manual packs and decide whether to create child repositories. If a child
repository is created, update the flagship docs only after the repository
exists and the real URL is approved.
