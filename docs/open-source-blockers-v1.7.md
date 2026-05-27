# Open Source Blockers v1.7

Round: 398R
Status: blocker review

## Blocking Findings

No content blocker was found from PR #1.

No PR #1 showcase files are present on the public launch prep branch.

No accepted academic-showcase claim is present.

## Non-Blocking Findings

The scan found many safety-policy mentions of:

- secrets;
- API keys;
- tokens;
- cookies;
- raw data;
- private paths;
- SMPL-X;
- VGGT and SparseConv3D boundaries.

These are policy/checklist/example-placeholder mentions, not committed payloads.

Examples:

- `.mcp.example.json` contains blank env placeholders.
- optional live docs name env variables but do not contain values.
- split manual packs contain checklist language.
- README explicitly blocks VGGT/SparseConv3D overclaiming.

## Manual Blockers Before Public Release

These are not code/content blockers, but they must be handled before an actual
public launch:

1. Maintainer decides whether PR #2 community docs belong in the launch branch.
2. Maintainer confirms repository visibility change.
3. Maintainer confirms release/tag/PyPI/Pages decisions.
4. Maintainer reruns safety gates after any final merge or README edit.
5. Maintainer confirms split repo URLs are still placeholders unless actual
   repos have been manually created.

## PR #1 Blocker Status

PR #1 is rejected and excluded.

Do not merge PR #1.

Do not revive `examples/original-author-showcase/` as publication evidence.
