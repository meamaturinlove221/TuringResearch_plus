# Final Push Commands: turingresearch-vggt-case

Status: commented reference only / not executable.

These commands are deliberately commented. They document the final shape a
human may adapt only after repository creation, privacy review, and maintainer
approval. Do not run them from the flagship repository root.

## Preconditions

- External repository was created manually by a human.
- Real remote URL is approved.
- Copied files exactly match the reviewed source bundle.
- `FINAL_PRIVACY_CHECK.md` has no blockers.
- `FINAL_RELEASE_CHECKLIST.md` is complete.
- No private data, raw data, restricted model payload, or secret is present.

## Reference Commands

```sh
# cd <manual-local-copy-of-turingresearch-vggt-case>
# git init
# git add README.md QUICKSTART.md CASE_STUDY.md PRIVACY.md CLAIM_SAFETY.md LICENSE_NOTE.md manifest.yaml safety_report.md .gitignore
# git commit -m "Initial public-safe VGGT case study"
# git branch -M main
# git remote add origin <approved-real-repository-url>
# git push -u origin main
```

## Safety Notes

- Do not run these commands automatically.
- Do not use a placeholder URL as a remote.
- Do not push from the flagship repository root.
- Do not add unreviewed local files.
- Do not add raw data, model payloads, cache directories, or generated heavy
  artifacts.
- Do not claim VGGT or SparseConv3D success in the commit message.
