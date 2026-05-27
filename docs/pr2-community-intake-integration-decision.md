# PR #2 Community Intake Integration Decision

Round: 394R
Status: integration decision only

## Decision

PR #2 can be integrated if, and only if, the integration remains limited to
community documentation intake files.

PR #1 is excluded.

Do not merge PR #1.

Do not make the repository public as part of this round.

## Source State

Local git refs show:

- PR #2 branch `origin/feature/community-idea-docs-intake` is an ancestor of
  `origin/main`.
- `origin/main` contains the `community/` intake tree.
- `release/v1.6.0-rc` does not currently contain the `community/` intake tree.

This round records the release-line integration decision. It does not merge the
community tree into `release/v1.6.0-rc`.

## Integration Boundary

Allowed PR #2 integration scope:

- `community/README.md`
- `community/CONTRIBUTOR_GUIDE.md`
- `community/REVIEW_POLICY.md`
- `community/ideas/README.md`
- `community/ideas/_template.md`
- `community/ideas/example-friend/example-idea.md`
- `community/skills/README.md`
- `community/skills/_template.md`
- `community/skills/example-friend/example-skill-proposal.md`
- `community/intake-log.md`

Forbidden PR #2 integration scope:

- `src/`
- `tests/`
- `.github/`
- release workflow files
- package metadata
- `README.md`
- `CHANGELOG.md`
- `VERSION`
- v1.6 release notes
- implementation modules

## Required Conditions

PR #2 can be merged or cherry-picked into a release line only if:

1. the diff is community-docs only;
2. it does not modify code, tests, CI, or release files;
3. it does not include secrets, raw data, private logs, private paths, copied
   PDFs/images, or unsupported claims;
4. it preserves TuringResearch public naming;
5. it keeps community intake as proposal intake, not implementation.

## Friend Contribution Path

After PR #2 is integrated, a friend can submit one Markdown-only idea or skill
proposal:

1. branch from `main`;
2. copy `community/ideas/_template.md` or `community/skills/_template.md`;
3. create a file under `community/ideas/<github-username>/` or
   `community/skills/<github-username>/`;
4. avoid code, secrets, private data, raw data, PDFs/images, and release files;
5. open a PR for maintainer review.

Any implementation must happen later in a separate maintainer/Codex-owned
branch. Community intake documents do not directly change runtime behavior.

## Go / No-Go

`GO FOR PR #2 COMMUNITY-DOCS INTEGRATION REVIEW`

`NO-GO FOR CODE, TEST, CI, RELEASE, OR PR #1 INTEGRATION`
