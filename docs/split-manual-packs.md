# Split Manual Packs

Status: planned / manual-ready, not published.

Round: 342.

The `split_manual/` directory contains human-only execution packs for future
split repositories. These packs support future publication review, but they do
not create repositories, push remotes, publish releases, or write real URLs.

## Current Manual Packs

| Manual pack | Source bundle | Status | Role |
| --- | --- | --- | --- |
| `split_manual/turingresearch-vggt-case/` | `split_ready/turingresearch-vggt-case/` | manual-ready | public-safe case study spoke |
| `split_manual/turingresearch-examples/` | `split_ready/turingresearch-examples/` | manual-ready | public-safe examples spoke |

## Pack Contents

Each manual-ready pack may include:

- `README.md`
- `CREATE_REPO_MANUALLY.md`
- `PUSH_COMMANDS.md`
- `SAFETY_CHECKLIST.md`
- `GIT_INIT_DRY_RUN.md`
- `RELEASE_CHECKLIST.md`
- `manifest.yaml`

## Publication Boundary

Manual-ready means a human can review the pack. It does not mean the child
repository exists or is published.

Required boundaries:

- only planned / manual-ready language;
- no fake URL;
- no automatic GitHub repository creation;
- no automatic external push;
- no automatic release publication;
- no private data, raw data, secrets, private paths, or huge artifacts;
- no unsupported observed-result claims.

## Flagship Boundary

The main TuringResearch repository remains:

- the install entry;
- the quickstart entry;
- the public API entry;
- the release and tag entry;
- the docs and dashboard entry;
- the star target.

Child repositories are only case/demo spokes. They should point readers back to
the flagship rather than replacing it.

## Human Release Flow

1. Review `split_ready/` source bundle.
2. Review matching `split_manual/` pack.
3. Confirm README flagship backlink wording.
4. Confirm no real URL is written before the repository exists.
5. Manually create the child repository, if approved.
6. Push only reviewed public-safe files.
7. Draft first release manually.
8. Update flagship docs only after the child repository exists.
