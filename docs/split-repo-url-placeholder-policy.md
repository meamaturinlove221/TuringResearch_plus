# Split Repo URL Placeholder Policy

Round: 370
Status: policy locked

## Purpose

Split repositories such as `turingresearch-vggt-case` and
`turingresearch-examples` are manual-ready packs, not current external
repositories. Before a split repository is manually created, project docs must
not contain fake GitHub URLs or URLs that imply the child repository already
exists.

## Required Placeholder

Before repository creation, use one of these placeholders only:

```text
<approved-real-repository-url>
```

```text
TuringResearch main repository URL goes here after human publication approval
```

The first placeholder is for a future child repository remote. The second
placeholder is for the flagship repository backlink until the canonical public
URL is approved.

## Rules

1. Before creation, split repo docs may only write `PLACEHOLDER`, the approved
   remote placeholder, or the approved flagship placeholder.
2. Fake GitHub URLs are not allowed.
3. A URL that looks like a real child repository link is not allowed until the
   repository exists and a maintainer approves it.
4. Creating a child repository is a manual action, never a workflow side effect.
5. After creation, docs must be updated manually in a follow-up commit.
6. The main README must not imply that split repositories already exist.
7. Child README files must point back to the flagship TuringResearch repository
   above the fold, using the approved placeholder before the real URL exists.
8. The flagship repository remains the install, docs, release, API, roadmap,
   and star entry.

## Forbidden Before Creation

- fake GitHub URLs;
- guessed organization or owner URLs;
- links to child repositories that do not exist;
- placeholder URLs treated as real remotes;
- automatic URL insertion during split-pack generation;
- auto-created repository URLs from CI;
- external push instructions that are not commented reference notes.

## Allowed Before Creation

- local paths such as `split_ready/turingresearch-examples/`;
- local docs links;
- `PLACEHOLDER` markers;
- `<approved-real-repository-url>`;
- `TuringResearch main repository URL goes here after human publication approval`;
- commented manual command examples that keep the remote as a placeholder.

## Child Repository Requirement

Every child README must include a clear flagship backlink placeholder before any
external creation:

```text
Flagship placeholder: TuringResearch main repository URL goes here after human publication approval
```

After creation, the backlink must be manually replaced only after the
maintainer verifies the real flagship URL.

## Decision

The current split packs are URL-placeholder only. They are ready for human
review and are not evidence that external repositories exist.
