# Post-launch Hotfix Policy

Status: hotfix policy.

Round: 198.

Use hotfixes for urgent release issues after a future public launch.

## Hotfix Candidates

- Install failure.
- Quickstart failure.
- Public demo breakage.
- Broken CLI/MCP entry point.
- Privacy/security issue.
- Unsafe plugin policy gap.
- Incorrect docs that could cause overclaiming.
- Version or packaging metadata mismatch.

## Hotfix Non-candidates

- New feature requests.
- Broad UI redesign.
- Physical split repository creation.
- Live adapter expansion.
- Research paper writing automation.
- Remote execution orchestration.

## Hotfix Process

1. Reproduce locally.
2. Scope the smallest safe fix.
3. Add or update a regression test when practical.
4. Run focused tests plus name/privacy gates.
5. Update changelog or patch notes.
6. Request maintainer review.
7. Publish only in an explicit release round.

## Safety Rules

- Do not include secrets in reproduction.
- Do not ask for private data in public issues.
- Do not relax plugin safety defaults.
- Do not convert fake/demo outputs into observed evidence.
- Do not patch around privacy gates without documenting the reason.
