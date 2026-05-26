# Safety Checklist

Status: required before manual repository creation.

Every item below must be reviewed by a human before any external repository is
created or pushed.

## Content Safety

- [ ] Source tree is exactly `split_ready/turingresearch-examples/`.
- [ ] Content is demo-only.
- [ ] No raw data is included.
- [ ] No private local path is included.
- [ ] No API key, token, credential, or `.env` value is included.
- [ ] No huge artifact is included.
- [ ] No private log is included.
- [ ] No restricted model file is included.

## Claim Safety

- [ ] README says this is not a replacement for the flagship repository.
- [ ] README says this is not a proof of research success.
- [ ] Demo output is not presented as observed research evidence.
- [ ] No benchmark or experiment success claim is included.
- [ ] No automatic final paper or research completion claim is included.

## Repository Safety

- [ ] Main TuringResearch repository remains the flagship.
- [ ] Child README points back to the flagship above the fold.
- [ ] No nonexistent real URL is written.
- [ ] External repository owner/name is approved.
- [ ] Human approval is recorded before manual creation.
- [ ] No automatic GitHub creation or push is used.

## Blocking Conditions

If any item fails, do not create the external repository. Return to the
flagship repository, fix the local bundle, rerun checks, and request review
again.
