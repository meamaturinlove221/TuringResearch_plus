# Contributor Guide for Idea and Skill Documents

This guide is for trusted collaborators who want to submit idea documents or skill proposals to TuringResearch.

## What to Submit

Submit Markdown files only.

Recommended types:

1. Idea document
2. Skill proposal
3. SOP proposal
4. Campaign proposal
5. Feature capsule draft
6. Public-safe reference summary

## Where to Put Files

For ideas:

```text
community/ideas/<your-github-username>/<short-title>.md
```

For skill proposals:

```text
community/skills/<your-github-username>/<short-title>.md
```

Use lowercase filenames with hyphens.

## Branch Naming

Use one of:

```text
community/<username>/idea-<short-title>
community/<username>/skill-<short-title>
```

## Pull Request Rules

Your PR should:

- only modify files under `community/`;
- not include code;
- not include secrets or private data;
- explain whether the idea is original, adapted, or based on public references;
- include links to public references when relevant;
- state what TuringResearch module it may affect.

## Review Criteria

Maintainers will check:

- originality or attribution;
- usefulness to TuringResearch;
- whether it can become a skill, feature capsule, SOP, or campaign;
- safety and privacy;
- whether it conflicts with current roadmap priorities;
- whether it should be accepted, deferred, split, or rejected.

## Contributor Credit

Accepted idea or skill proposals can be credited in:

- `community/intake-log.md`;
- README acknowledgements;
- release notes;
- feature capsule notes;
- skill metadata, if a proposal later becomes an implemented skill.

The exact credit format is decided by the maintainer before public release.
