# Push Commands

Status: reference-only command notes.

This file is intentionally not executable. It records the shape of commands a
human may adapt after repository creation has been approved. Do not run these
commands without maintainer approval.

## Preconditions

- The external repository has been manually created by a human.
- `SAFETY_CHECKLIST.md` is complete.
- The exact copied files match `manifest.yaml`.
- The approved public demo file set has been reviewed.
- The repository remote URL is real and approved.
- No private data, raw data, API keys, huge artifacts, or unsupported claims are
  present.

## Reference Command Shape

Replace placeholders manually after approval:

```sh
# cd <manual-local-copy-of-turingresearch-examples>
# git init
# git add README.md QUICKSTART.md examples_manifest.yaml PRIVACY.md safety_report.md .gitignore
# git commit -m "Initial public-safe examples bundle"
# git branch -M main
# git remote add origin <approved-real-repository-url>
# git push -u origin main
```

## Safety Notes

- Commands are commented so this document cannot be pasted as an execution
  script.
- Do not use placeholder URLs as remotes.
- Do not push from the flagship repository root.
- Do not push unreviewed local files.
- Do not add raw data, caches, or generated heavy artifacts.
- Do not claim demo output is observed evidence.

## After Manual Push

After a human completes a real push, update the flagship repository manually:

- replace placeholders with the approved real URL;
- record the action in `lanes/00_master_ledger.md`;
- rerun privacy and public-release checks;
- keep the flagship repository as the canonical install and docs entry.
