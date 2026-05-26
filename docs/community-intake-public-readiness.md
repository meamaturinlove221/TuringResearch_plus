# Community Intake Public Readiness

Status: ready for docs-only intake review.

Round: 393.

## Decision

`GO FOR DOCS-ONLY COMMUNITY INTAKE / NO-GO FOR CODE CONTRIBUTIONS`

PR #2 is public-ready as a documentation intake surface for trusted friends or
collaborators, subject to maintainer review.

## Why It Is Ready

- README explains the collaboration workflow.
- Contributor guide limits PRs to Markdown documents.
- Review policy blocks implementation paths and release-sensitive files.
- Idea template can map into feature capsules, SOP graphs, campaign items, or
  docs examples.
- Skill template can map into `.agents/skills/` after maintainer review.
- Intake log has contributor, file, type, status, and notes fields.
- Safety language blocks secrets, private data, raw datasets, model files, and
  unlicensed third-party media.

## Public Safety Boundary

Community intake is not an implementation channel. It should not accept:

- code;
- tests;
- CI changes;
- release file changes;
- package metadata changes;
- private logs;
- raw data;
- restricted model payloads;
- copied third-party PDFs/images;
- secrets or API keys;
- unsupported research claims.

## Integration Status

Git refs show PR #2 is already an ancestor of `origin/main`. The current
`release/v1.6.0-rc` branch does not contain `community/`; this gate does not
merge the intake surface into release.

## Public Readiness Result

Ready for review / no automatic merge needed from this round.

Recommended next step: if a friend wants to contribute, ask them to submit one
Markdown-only idea or skill proposal on a branch from `main`, using the
templates under `community/ideas/` or `community/skills/`.
