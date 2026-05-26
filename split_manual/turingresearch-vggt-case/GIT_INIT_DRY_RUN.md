# Git Init Dry-run: turingresearch-vggt-case

Status: dry-run only.

This file describes how a human may initialize a future
`turingresearch-vggt-case` repository after approval. It does not run `git
init`, create a repository, add a remote, or push.

## Files To Include

- `README.md`
- `QUICKSTART.md`
- `CASE_STUDY.md`
- `CLAIM_SAFETY.md`
- `PRIVACY.md`
- `LICENSE_NOTE.md`
- `manifest.yaml`
- `safety_report.md`
- `.gitignore`

## Files To Exclude

- raw data;
- private local paths;
- secrets, tokens, credentials, or `.env` values;
- SMPL-X files or restricted model payloads;
- model checkpoints;
- generated heavy artifacts;
- cache directories;
- unreviewed local files.

## Initial Commit Message Suggestion

```text
Initial public-safe VGGT case study
```

## Branch Suggestion

```text
main
```

## Remote URL Placeholder

```text
<approved-real-repository-url>
```

Do not replace this placeholder until a human confirms that the external
repository exists and the URL is real.

## Manual Commands

These commands are commented reference notes only:

```sh
# cd <manual-local-copy-of-turingresearch-vggt-case>
# git init
# git add README.md QUICKSTART.md CASE_STUDY.md PRIVACY.md CLAIM_SAFETY.md LICENSE_NOTE.md manifest.yaml safety_report.md .gitignore
# git commit -m "Initial public-safe VGGT case study"
# git branch -M main
# git remote add origin <approved-real-repository-url>
# git push -u origin main
```

## Safety Warnings

- Do not run this from the flagship repository root.
- Do not use a placeholder URL as a remote.
- Do not create a repository automatically.
- Do not push before human approval.
- Do not claim VGGT or SparseConv3D success.
- Do not present fake/demo material as observed evidence.
