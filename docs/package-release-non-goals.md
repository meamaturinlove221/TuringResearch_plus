# Package Release Non-goals

Round: 378
Status: active for v1.6 packaging readiness

Round 378 is a packaging readiness review. It is not a release action.

## Non-goals

- No PyPI publish.
- No TestPyPI publish.
- No package upload.
- No GitHub release publish.
- No tag creation.
- No automatic release artifact upload.
- No package distribution rename.
- No import namespace removal.
- No CLI rename.
- No MCP server rename.
- No default live network access.
- No API key requirement.
- No remote command execution.
- No automatic experiment execution.
- No fake result promotion to observed evidence.

## Deferred Decisions

- Whether to rename the distribution from `turingresearch-plus` to
  `turingresearch`.
- Whether to add new unsuffixed console scripts.
- Whether to change MCP server naming.
- Whether to publish to PyPI.
- Whether to change license metadata after human legal/project review.
- The final license decision before public package publication.

## Compatibility Policy

TuringResearch is the public project name. Existing package and import
compatibility surfaces remain available until a dedicated migration plan is
approved and tested.
