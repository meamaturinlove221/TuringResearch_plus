# Split Final Blockers

Round: 367
Status: no machine-detected blocker for final human review

## Current Decision

No release blocker was found for reviewing the current `split_ready/` and
`split_manual/` packages as manual execution packs.

This is not an approval to create public child repositories automatically.

## Blocking Items

| Item | Status | Notes |
| --- | --- | --- |
| secrets in split packs | clear | no token or private-key pattern in scoped split safety test |
| raw data in split packs | clear | no blocked raw-data file or directory names |
| private paths | clear | no machine-local VGGT path or local project-link config |
| restricted model payloads | clear | no SMPL-X payload files or checkpoint-like files |
| fake URLs | clear | only placeholders are allowed |
| unsupported claims | clear | success and release readiness remain review-gated |
| flagship displacement | clear | main repository remains canonical |

## Still Not Ready

The following actions remain blocked until a human explicitly approves them:

- creating a GitHub child repository;
- running `git init` inside a split pack;
- adding a real remote URL;
- pushing an external child repository;
- publishing a child repository release;
- adding real public URLs to flagship or child docs;
- promoting VGGT local metadata into observed public results;
- claiming SparseConv3D success;
- treating fake/demo material as observed research evidence.

## Required Human Review Before Any Split

1. Review every file in the chosen split pack.
2. Confirm the README points back to the flagship repository.
3. Confirm privacy, license, and claim-safety language.
4. Confirm the child repo name and actual destination URL.
5. Create the external repository manually, if approved.
6. Push only the reviewed public-safe files.
7. Record the completed action back in the flagship ledger.

## No-Go Conditions

If any of the following appears, stop and return to the flagship repository for
repair:

- secret, token, password, or private key material;
- raw data, private logs, large arrays, checkpoints, model payloads, or
  restricted SMPL-X assets;
- private machine paths or machine-local config files;
- nonexistent public URLs written as if live;
- unsupported research success claims;
- child repo wording that replaces the flagship install or docs entry.
