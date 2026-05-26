# Review Policy for Community Ideas and Skill Proposals

This policy keeps community contributions useful while protecting TuringResearch's codebase, authorship story, and public safety boundary.

## Scope

Community intake PRs are documentation-only by default.

Allowed paths:

```text
community/ideas/**
community/skills/**
community/intake-log.md
```

Maintainer-created policy/template files under `community/` are also allowed.

Disallowed paths for community idea PRs:

```text
src/**
tests/**
contracts/**
.github/**
pyproject.toml
README.md
CHANGELOG.md
VERSION
```

## Decision Labels

Suggested review decisions:

- `accept-as-idea`
- `accept-as-skill-candidate`
- `convert-to-feature-capsule`
- `convert-to-sop`
- `convert-to-campaign`
- `needs-attribution`
- `needs-scope-trim`
- `defer`
- `reject`

## Safety Checks

A reviewer should confirm:

- no implementation code was added;
- no secrets or private paths are present;
- no raw datasets or model files are included;
- public references are attributed;
- copied text is either original, licensed, or explicitly authorized;
- the proposal does not claim unsupported project results;
- the proposal does not alter current release gates.

## Conversion Path

A submitted idea may later become:

1. roadmap item;
2. feature capsule;
3. `.agents/skills/` skill;
4. SOP graph;
5. docs example;
6. campaign catalog item.

Implementation should happen in a separate maintainer-owned branch after review.
