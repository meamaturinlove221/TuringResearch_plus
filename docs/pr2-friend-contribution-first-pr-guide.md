# PR #2 Friend Contribution First PR Guide

Round: 394R
Status: user-facing guide

## Who This Is For

This guide is for a friend or collaborator who wants to submit a first idea or
skill proposal after PR #2 community intake is available on the target branch.

## What You May Submit

Allowed:

- one idea document;
- one skill proposal;
- public-safe references;
- attribution notes;
- Markdown diagrams.

Not allowed:

- code;
- copied source files;
- changes under `src/`;
- changes under `tests/`;
- CI or workflow changes;
- release file changes;
- API keys, tokens, `.env`, cookies, or passwords;
- raw data, private logs, private paths, or model payloads;
- third-party PDFs/images unless explicitly licensed and reviewed;
- unsupported claims that an experiment succeeded.

## Submit An Idea

1. Start from `main`.
2. Create a branch:

```text
community/<github-username>/idea-<short-title>
```

3. Copy:

```text
community/ideas/_template.md
```

4. Save as:

```text
community/ideas/<github-username>/<short-title>.md
```

5. Fill in the template.
6. Open a PR with label `community-idea`.

## Submit A Skill Proposal

1. Start from `main`.
2. Create a branch:

```text
community/<github-username>/skill-<short-title>
```

3. Copy:

```text
community/skills/_template.md
```

4. Save as:

```text
community/skills/<github-username>/<short-title>.md
```

5. Fill in the template.
6. Open a PR with label `skill-proposal`.

## What Happens Next

Maintainers review the document for public safety, attribution, usefulness, and
roadmap fit. If accepted, it may later become a feature capsule, SOP, campaign,
docs example, or `.agents/skills/` proposal.

Implementation must be done later by a maintainer or Codex in a separate
branch. The first community PR should stay documentation-only.
