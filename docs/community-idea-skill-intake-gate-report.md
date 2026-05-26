# Community Idea / Skill Intake Gate Report

Status: GO for docs-only community intake.

Round: 393.

This gate reviews PR #2, `Add community idea and skill proposal intake`, using
locally fetched git refs and the community files present on `origin/main`. It
does not merge PRs, change repository visibility, add implementation code, or
move community files into `release/v1.6.0-rc`.

## Source Reviewed

PR #2 merge commit observed on `origin/main`:

```text
976a742 Merge pull request #2 from meamaturinlove221/feature/community-idea-docs-intake
```

PR #2 branch status from git refs:

```text
origin/feature/community-idea-docs-intake is an ancestor of origin/main: yes
```

Files reviewed from `origin/main`:

- `community/README.md`
- `community/CONTRIBUTOR_GUIDE.md`
- `community/REVIEW_POLICY.md`
- `community/ideas/_template.md`
- `community/skills/_template.md`
- `community/intake-log.md`

## Gate Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| only allows documentation contributions | pass | README and contributor guide say Markdown / docs-only |
| explicitly forbids submitting code | pass | README, contributor guide, and review policy forbid implementation code |
| forbids modifying `src`, `tests`, CI, release files | pass | review policy disallows `src/**`, `tests/**`, `.github/**`, `pyproject.toml`, `README.md`, `CHANGELOG.md`, `VERSION` |
| forbids secrets, raw data, private logs, third-party PDFs/images | pass | README and review policy ban secrets, raw datasets/model files, private data, and unlicensed third-party PDFs/images |
| idea template can convert to feature capsule / SOP / campaign | pass | idea template has expected artifacts and suggested conversion path |
| skill template can convert to `.agents/skills/` | pass | skill template asks maintainers how to convert to `.agents/skills/<skill-name>/SKILL.md` |
| intake log records contributor attribution | pass | log includes date, contributor, file, type, status, and notes |
| README explains collaboration flow | pass | README lists branch, file location, template, PR label, maintainer review, and conversion path |

## Go / No-Go

Decision: `GO FOR DOCS-ONLY COMMUNITY INTAKE / NO-GO FOR CODE OR RELEASE-SURFACE CONTRIBUTIONS`.

PR #2 is suitable as a community documentation intake surface for trusted
friends or collaborators who should not touch implementation code.

## Merge Recommendation

Recommendation: PR #2 is acceptable to merge from a gate perspective if it is
still open in the GitHub UI.

Git-ref note: locally fetched refs show PR #2 is already integrated into
`origin/main`. Do not merge it again from this round. Do not merge it into
`release/v1.6.0-rc` without a separate release-line integration decision.

## Remaining Review Notes

- The current `release/v1.6.0-rc` branch does not contain `community/`; this
  gate reviews PR #2 as it exists on `origin/main`.
- If the intake area is later brought into a release branch, rerun name,
  privacy, no-secret, and no-fake-URL gates on that branch.
- Maintainers should decide whether community intake belongs in main only or
  also in a future release branch.

## Friend Submission Summary

A friend should submit the first document by:

1. creating a branch from `main`;
2. copying `community/ideas/_template.md` or `community/skills/_template.md`;
3. placing one Markdown file under
   `community/ideas/<github-username>/<short-title>.md` or
   `community/skills/<github-username>/<short-title>.md`;
4. avoiding code, private data, raw data, copied PDFs/images, API keys, and
   release/CI files;
5. opening a PR with label `community-idea` or `skill-proposal`;
6. waiting for maintainer review before any conversion into feature capsules,
   SOPs, campaigns, or `.agents/skills/`.
