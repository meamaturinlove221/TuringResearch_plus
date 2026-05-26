# Final Push Commands: turingresearch-examples

Status: commented reference only / not executable.

These commands are deliberately commented. They document the final shape a
human may adapt only after repository creation, privacy review, and maintainer
approval. Do not run them from the flagship repository root.

## Preconditions

- External repository was created manually by a human.
- Real remote URL is approved.
- Copied files exactly match the reviewed demo-only source bundle.
- `FINAL_PRIVACY_CHECK.md` has no blockers.
- `FINAL_RELEASE_CHECKLIST.md` is complete.
- No private data, raw data, API key, huge artifact, or unsupported claim is
  present.

## Reference Commands

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

- Do not run these commands automatically.
- Do not use a placeholder URL as a remote.
- Do not push from the flagship repository root.
- Do not add unreviewed local files.
- Do not add raw data, private logs, cache directories, or generated huge
  artifacts.
- Do not claim demo output is observed research evidence.
- Keep the main TuringResearch repository as the flagship entry.
