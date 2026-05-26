# Community Contributor Onboarding

Status: docs-only onboarding guidance.

Round: 393.

This page summarizes how a trusted friend or collaborator should submit a
community idea or skill proposal. It is based on PR #2 community intake docs.

## What A Friend Can Submit

Allowed:

- one Markdown idea document;
- one Markdown skill proposal;
- docs-only workflow notes;
- Mermaid diagrams inside Markdown;
- public-safe references;
- attribution notes.

Not allowed:

- implementation code;
- copied source code;
- changes to `src/`;
- changes to `tests/`;
- changes to CI or `.github/`;
- release files such as `CHANGELOG.md`, `VERSION`, or release notes;
- secrets, tokens, `.env`, cookies, or API keys;
- private logs or private user data;
- raw datasets or model files;
- unlicensed third-party PDFs or images;
- unsupported result claims.

## First Idea Submission

1. Start from `main`.
2. Create a branch like:

```text
community/<github-username>/idea-<short-title>
```

3. Copy:

```text
community/ideas/_template.md
```

4. Save it as:

```text
community/ideas/<github-username>/<short-title>.md
```

5. Fill in:

- contributor name to credit;
- one-line summary;
- problem;
- proposed direction;
- target module;
- expected artifacts;
- references / attribution;
- risks;
- non-goals;
- suggested conversion path.

6. Open a PR with label `community-idea`.

## First Skill Proposal

1. Start from `main`.
2. Create a branch like:

```text
community/<github-username>/skill-<short-title>
```

3. Copy:

```text
community/skills/_template.md
```

4. Save it as:

```text
community/skills/<github-username>/<short-title>.md
```

5. Fill in:

- trigger conditions;
- goal;
- inputs;
- outputs;
- procedure;
- safety boundaries;
- review gates;
- related modules;
- conversion notes for `.agents/skills/<skill-name>/SKILL.md`.

6. Open a PR with label `skill-proposal`.

## Maintainer Review Path

Maintainers review submissions for:

- scope;
- attribution;
- public safety;
- privacy;
- usefulness;
- roadmap fit;
- conversion path.

Accepted documents may later become:

- feature capsule;
- SOP graph;
- campaign catalog item;
- docs-only example;
- `.agents/skills/` skill proposal;
- roadmap item.

Implementation must happen separately in a maintainer-owned branch after
review.
