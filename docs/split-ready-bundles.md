# Split-ready Bundles

Status: local export bundles only.

The `split_ready/` directory contains public-safe export bundles that could be
used to create future spoke repositories after human approval. These bundles
are not published repositories and are not required for installation.

For v1.5, matching human execution packs live under `split_manual/`. The
`split_ready/` tree remains the reviewed source bundle; `split_manual/` records
manual creation instructions, git-init dry-run notes, and release checklists.
Neither tree is a published repository.

## Bundle Inventory

| Bundle | Status | Public-safe purpose | Main repo relationship |
| --- | --- | --- | --- |
| `split_ready/turingresearch-vggt-case/` | `ready_to_create_after_human_approval` | Sanitized VGGT dogfooding case study | Points back to the flagship |
| `split_ready/turingresearch-examples/` | `ready_to_create_after_human_approval` | Demo-only examples inventory | Points back to the flagship |
| `split_ready/turingresearch-plugins/` | `deferred_until_ecosystem_demand` | Plugin contribution and review policy | Main repo keeps core framework |

Root-level sync files:

- `split_ready/SPLIT_SYNC_POLICY.md`
- `split_ready/split_manifest.yaml`

## Bundle Files

### `turingresearch-vggt-case`

- `README.md`
- `QUICKSTART.md`
- `CASE_STUDY.md`
- `PRIVACY.md`
- `CLAIM_SAFETY.md`
- `LICENSE_NOTE.md`
- `manifest.yaml`
- `safety_report.md`
- `.gitignore`

### `turingresearch-examples`

- `README.md`
- `QUICKSTART.md`
- `examples_manifest.yaml`
- `PRIVACY.md`
- `safety_report.md`
- `.gitignore`

### `turingresearch-plugins`

- `README.md`
- `PLUGIN_POLICY.md`
- `plugins_manifest.yaml`
- `safety_report.md`

## What These Bundles Are Not

- They are not GitHub repositories.
- They are not pushed to external remotes.
- They are not package install paths.
- They do not replace the flagship README, quickstart, or docs.
- They do not contain core framework source.
- They do not contain private data, raw data, restricted model payloads, or
  real credentials.
- They do not contain real private logs or unsupported observed-result claims.

## Cross-link Rule

Split-ready README files may include a flagship URL placeholder, but they must
not include nonexistent GitHub URLs. After a real repository is created by a
human maintainer, replace the placeholder with the approved flagship URL.

## Main Repo Protection

- The main repository remains the install entry.
- The main repository remains the quickstart entry.
- The main repository remains the public API and release entry.
- The main repository remains the star target.
- Child repositories are case/demo spokes only.
- Child repositories must not become package install paths.
- Child repositories must not pull attention away from the flagship.

## Review Checklist

Before any bundle becomes a real repository, confirm:

- privacy gate passes;
- compliance gate passes;
- claim-safety gate passes;
- README links back to the flagship;
- no unsupported observed-result claim exists;
- install and quickstart remain in the main repository;
- maintainer approval is recorded.
