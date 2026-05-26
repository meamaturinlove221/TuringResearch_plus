# Compliance Report: vggt_fake_compliance

- Redistribution risk: `blocker`
- Publication risk: `blocker`
- Requires human review: `true`
- Disclaimer: This compliance report is a research checklist and is not legal advice.

## Datasets

- `vggt_raw_dataset` VGGT private/raw experiment data (license: `restricted-data`, status: `restricted`, bundled: `false`, public release allowed: `false`, requires human review: `true`) restrictions: raw dataset is not public-demo safe; do not bundle in public release; requires project owner review

## Models

- `smplx_body_model_files` SMPL-X body model files (license: `SMPL-X restricted model license`, status: `restricted`, bundled: `false`, public release allowed: `false`, requires human review: `true`) restrictions: license restricted; not bundled; requires user-provided licensed copy

## Papers

- `third_party_paper_figures` Third-party paper figures used as related-work references (license: `review-required`, status: `review-required`, bundled: `false`, public release allowed: `none`, requires human review: `true`) restrictions: third-party paper figures require reuse rights review; do not copy figures into public case study without permission

## Code Repositories

- `github_code_dependency` GitHub code dependency with missing license metadata (license: `unknown`, status: `unknown`, bundled: `false`, public release allowed: `none`, requires human review: `true`) restrictions: GitHub code license missing; record license before redistribution

## Licenses

- `SMPL-X restricted model license`
- `restricted-data`
- `review-required`
- `unknown`

## Usage Restrictions

- GitHub code license missing
- do not bundle in public release
- do not copy figures into public case study without permission
- license restricted
- not bundled
- raw dataset is not public-demo safe
- record license before redistribution
- requires project owner review
- requires user-provided licensed copy
- third-party paper figures require reuse rights review

## Missing License Info

- `github_code_dependency`

## Findings

- `blocker` `dataset` `vggt_raw_dataset`: Asset has restricted or proprietary license status. Action: Do not bundle; require human license review. Release blocker: `true`
- `blocker` `dataset` `vggt_raw_dataset`: Raw dataset material is not public-release safe by default. Action: Keep raw data out of public examples and release packages. Release blocker: `true`
- `blocker` `model` `smplx_body_model_files`: Asset has restricted or proprietary license status. Action: Do not bundle; require human license review. Release blocker: `true`
- `medium` `paper` `third_party_paper_figures`: License status requires human review. Action: Confirm license terms before public reuse. Release blocker: `false`
- `medium` `paper` `third_party_paper_figures`: Third-party paper figures require reuse permission review. Action: Use citations or redraw only after confirming reuse rights. Release blocker: `false`
- `high` `code_repo` `github_code_dependency`: License information is unknown. Action: Record license source before publication or redistribution. Release blocker: `true`

## Boundary

- This report is a compliance checklist, not legal advice.
- It does not download licenses or package restricted assets.
- Human review is required before publication or redistribution.
