# Split Sync Policy

Status: manual policy for local split-ready bundles.

The flagship TuringResearch repository is the source of truth. The directories
under `split_ready/` are public-safe export bundles and are not published
repositories.

## Current Bundles

- `turingresearch-vggt-case`: case-study mirror candidate.
- `turingresearch-examples`: public demo/examples mirror candidate.
- `turingresearch-plugins`: plugin policy/registry draft candidate, deferred
  until real ecosystem demand.

## Sync Rules

- Copy from the flagship into split bundles, not the reverse.
- Keep install, docs, release, quickstart, public API, and issue triage anchored
  in the flagship.
- Keep spoke README files pointing readers back to the flagship.
- Do not add core framework source to split bundles.
- Do not add raw data, private paths, secrets, restricted model files, huge
  artifacts, real private logs, or unsupported claims.
- Do not write nonexistent GitHub URLs.
- Do not push external repositories without explicit human approval.

## Manual Sync Checklist

1. Choose reviewed source files from the flagship.
2. Update the relevant split bundle.
3. Update the bundle manifest and safety report.
4. Run split safety tests and privacy gate.
5. Record the change in the master ledger.
6. Ask for human approval before external repository creation or push.
