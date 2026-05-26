# Dataset / License Compliance Assistant Skill

Status: planning skill draft.

Use this skill for dataset/license risk planning. It produces review aids, not
legal advice or redistribution approval.

## Inputs

- artifact manifest
- project privacy policy
- license notes
- public release strategy
- privacy scan report

## Outputs

- DatasetLicenseReviewReport
- LicenseRiskFinding
- ReleaseUseRecommendation

## Safety Rules

- Do not provide legal conclusions.
- Do not bypass licenses.
- Do not package raw data or private model files.
- Require human review.

## Related Contracts

- dataset_license_compliance.yaml
- privacy_data_policy.yaml
