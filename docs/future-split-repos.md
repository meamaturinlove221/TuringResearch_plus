# Future Split Repositories

Status: planned / manual-ready documentation.

TuringResearch remains the flagship repository. Future split repositories
are planned or manual-ready spokes, not current GitHub repositories and not
installation targets.

## Current Decision

The main repository remains the install, quickstart, public API, release, docs,
and star entry. v1.5 may prepare human execution packs, but it still does not
auto-create repositories, auto-push remotes, or write real URLs for repositories
that do not exist.

Future spokes may be created only after human approval, final safety review,
and explicit repository creation approval.

## Planned Spokes

| Planned repo | Current status | Purpose | v1.5 action |
| --- | --- | --- | --- |
| `turingresearch-vggt-case` | split-ready and manual-ready | Public-safe dogfooding case study | Human may review manual pack; do not publish automatically |
| `turingresearch-examples` | split-ready and manual-ready | Demo-only examples and templates | Human may review manual pack; do not publish automatically |
| `turingresearch-plugins` | local draft bundle, deferred | Plugin policy and contribution surface | Do not publish automatically |

## Link Placeholders

Do not write real GitHub URLs until the repositories exist and the maintainer
approves the links. Until then, use placeholders such as:

```text
TuringResearch main repository URL goes here after human publication approval.
```

The current local bundles are under `split_ready/`; manual creation packets are
under `split_manual/`. Both are local review materials, not published
repositories.

See also:

- [`split-repo-url-placeholder-policy.md`](split-repo-url-placeholder-policy.md)
- [`split-repo-url-update-after-creation.md`](split-repo-url-update-after-creation.md)

## Sync Policy

The flagship repository remains the source of truth. Future spoke repositories
are mirrors for public demo or case material only.

See:

- [`split-ready-bundles.md`](split-ready-bundles.md)
- [`split-manual-packs.md`](split-manual-packs.md)
- [`main-repo-post-split-patch-v2.md`](main-repo-post-split-patch-v2.md)
- [`v1.1.0-split-repo-sync-policy.md`](v1.1.0-split-repo-sync-policy.md)
- `../split_ready/split_manifest.yaml`

## Not Split In v1.0

These remain in the flagship repository:

- core runtime;
- paper workflow;
- artifact workflow;
- dashboard/export workflow;
- plugin framework implementation;
- package install path;
- CLI/MCP entry points;
- release, privacy, compliance, and regression gates.

## Linking Policy

- Do not add external GitHub URLs until those repositories exist.
- Link only to local docs and `split_ready/` bundles before publication.
- Use `split_manual/` packs only as human review packets.
- Spoke README files must point back to the flagship above the fold.
- The flagship remains the only install, quickstart, release, and star entry.
- Split spokes should not disperse star attention away from the flagship.
- Main README language must stay planned / manual-ready until a child repository
  actually exists.

## Safety Boundaries

Future split repositories must not include:

- private data;
- raw data;
- restricted model payloads;
- private local paths;
- real credentials;
- unsupported research-success claims;
- fake/demo output presented as observed evidence.

## Human Approval Required

Before creating any real split repository, the maintainer must approve:

- repository name and ownership;
- final export tree;
- README wording;
- license posture;
- privacy/compliance/claim-safety reports;
- whether the flagship README should link to the new repository.
