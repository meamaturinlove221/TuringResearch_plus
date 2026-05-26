# Final Create Repo: turingresearch-vggt-case

Status: final manual creation instructions / not executed.

This file is a human-only checklist for a possible future public-safe child
repository. It does not create a GitHub repository, does not run commands, does
not write a real URL, and does not push anything outside the flagship
TuringResearch repository.

## Repo Name Suggestion

```text
turingresearch-vggt-case
```

## Initial Branch

```text
main
```

## Initial Commit Message

```text
Initial public-safe VGGT case study
```

## Remote URL Placeholder

```text
<approved-real-repository-url>
```

Do not replace this placeholder until a maintainer confirms that the external
repository exists and the URL is real.

## Manual GitHub Creation Steps

1. Review `split_ready/turingresearch-vggt-case/`.
2. Review `split_manual/turingresearch-vggt-case/FINAL_PRIVACY_CHECK.md`.
3. Confirm every item in `FINAL_RELEASE_CHECKLIST.md`.
4. Manually create a GitHub repository named `turingresearch-vggt-case`, if
   approved.
5. Keep the main TuringResearch repository as the flagship install, docs,
   release, public API, and star entry.
6. Copy only files from the reviewed source bundle.
7. Add a real flagship link only after a maintainer approves the real URL.
8. Record the action back in the flagship ledger after completion.

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
- restricted model payloads;
- model checkpoints;
- generated heavy artifacts;
- cache directories;
- unreviewed local files;
- local scan links or private machine metadata.

## Safety Checklist

- No automatic GitHub repository creation.
- No automatic external push.
- No automatic release creation.
- No fake or placeholder URL used as a real remote.
- No raw VGGT data.
- No restricted model payload.
- No private path.
- No unsupported VGGT success claim.
- No SparseConv3D success claim.
- No fake/demo output written as observed evidence.
