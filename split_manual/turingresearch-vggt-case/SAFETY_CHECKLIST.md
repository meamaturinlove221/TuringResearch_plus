# Safety Checklist

Status: required before manual repository creation.

Every item below must be reviewed by a human before any external repository is
created or pushed.

## Content Safety

- [ ] Source tree is exactly `split_ready/turingresearch-vggt-case/`.
- [ ] No raw data is included.
- [ ] No SMPL-X files or restricted model payloads are included.
- [ ] No private local path is included.
- [ ] No secret, token, API key, credential, or `.env` value is included.
- [ ] No huge binary artifact is included.
- [ ] No private advisor feedback is included.

## Claim Safety

- [ ] README says this is not a VGGT experiment source repository.
- [ ] README says this is not proof of final research success.
- [ ] Claim safety file does not claim VGGT experiment success.
- [ ] Claim safety file does not claim SparseConv3D success.
- [ ] Planned work is not written as observed evidence.
- [ ] Fake/demo material is not written as observed research evidence.

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
