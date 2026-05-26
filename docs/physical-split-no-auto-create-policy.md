# Physical Split No Auto-create Policy

Status: enforced policy.

Round: 337.

TuringResearch must not automatically create GitHub repositories or push
external child repositories during v1.5 split preparation.

## Forbidden Automation

- No `gh repo create`.
- No automatic remote creation.
- No automatic `git push` to child repos.
- No automatic GitHub release in child repos.
- No automatic PyPI publishing from child repos.
- No automatic URL insertion for repos that do not exist.
- No automatic private data upload.

## Allowed Automation

- Generate manual execution packs.
- Generate safety reports.
- Generate README/backlink checklists.
- Generate manifest files.
- Run privacy and public-safety scans.
- Prepare commands as comments for human review.

## URL Policy

Before a child repository exists, docs may use a placeholder such as:

```text
TuringResearch main repository URL goes here after human approval.
```

Docs must not invent a real GitHub URL. A real URL may only be written after a
human creates the repository and confirms the destination.

## Flagship Rule

The main TuringResearch repository remains the flagship for install, docs,
release notes, API, roadmap, and public attention.
