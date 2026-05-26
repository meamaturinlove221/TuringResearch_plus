# VGGT Case Repo Skeleton

Status: design draft.

Round: 159.

This document describes the proposed skeleton for the future
`turingresearch-vggt-case` repository. The current skeleton lives under
`examples/split_repos/turingresearch-vggt-case/` for review only.

## Proposed Files

```text
turingresearch-vggt-case/
  README.md
  CASE_STUDY.md
  PRIVACY.md
  manifest.yaml
```

## File Roles

- `README.md`: first-screen positioning, safety boundaries, and flagship link.
- `CASE_STUDY.md`: public-safe dogfooding case-study draft.
- `PRIVACY.md`: privacy, redaction, compliance, and claim-safety boundaries.
- `manifest.yaml`: file inventory and safety metadata.

## Required README Statements

- This repo demonstrates TuringResearch dogfooding.
- This repo is not the VGGT experiment source repo.
- It does not contain private data.
- It does not contain raw data.
- It does not contain SMPL-X model files.
- It does not claim final research success.
- The main TuringResearch repo remains the install and star entry point.

## Required Manifest Fields

- `repo_id`
- `status`
- `purpose`
- `flagship_repo`
- `included_files`
- `safety`
- `claim_boundaries`
- `requires_human_review`

## Extraction Rule

Do not create a real repository until this skeleton passes a dedicated public
extraction gate and maintainer review.
