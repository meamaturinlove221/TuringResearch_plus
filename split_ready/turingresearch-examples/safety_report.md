# Split Safety Report: turingresearch-examples

- safe_to_export: `true`
- release_blocker: `false`
- requires_human_review: `true`
- export_stage: `v1.0-final-public-safe-bundle`
- round_210_stage: `physical-split-prep`
- main_repo_remains_flagship: `true`

## Checked Files

- `README.md`
- `QUICKSTART.md`
- `examples_manifest.yaml`
- `PRIVACY.md`
- `safety_report.md`
- `.gitignore`

## Omitted Files

- none

## Findings

- `medium` `policy-mention:private_advisor_feedback` `README.md`: Safety policy text mentions an excluded private item.

## Final Safety Checks

- Demo only: pass.
- No private data: pass.
- No secrets: pass.
- No raw data: pass.
- No huge artifacts: pass.
- No unsupported claims: pass.
- Main repo referenced as flagship: pass.
- Ready for manual copy after approval: pass.

## Limitations

- Final export bundle does not create repositories.
- Final export bundle does not push git remotes.
- Safety checks are pattern based and require human review.
- Public split candidates must still pass maintainer review before publication.
