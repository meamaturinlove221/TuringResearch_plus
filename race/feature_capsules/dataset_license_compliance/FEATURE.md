# Dataset / License Compliance Assistant

Status: feature capsule draft.

Release target: v0.7.

## 1. Problem

Public research workflows need a way to flag dataset and license risks before
examples, artifacts, or case studies are shared.

## 2. Research Motivating Example

A public case study should not accidentally include raw data, licensed model
files, or third-party material with unclear redistribution terms.

## 3. Inputs

- artifact manifest
- project privacy policy
- license notes
- public release strategy
- privacy scan report

## 4. Outputs

- DatasetLicenseReviewReport
- LicenseRiskFinding
- ReleaseUseRecommendation

## 5. Proposed Commands / Tools

- command: `turing release license-check`
- tool: `release.dataset_license_check`
- output: `DatasetLicenseReviewReport`

## 6. Related Contracts

- dataset_license_compliance.yaml
- privacy_data_policy.yaml

## 7. Related Skills

- turingresearch-qa-release
- turingresearch-race-source-hygiene

## 8. Required Tests

- license risk model tests
- raw data blocking tests
- human-review disclaimer tests

## 9. Risks

- user treats report as legal advice
- false sense of compliance
- missed third-party restriction

## 10. Done Criteria

- report labels risks and recommended actions
- no legal guarantee is claimed
- human review remains required

## 11. Non-goals

- no legal advice
- no license bypass
- no automatic redistribution approval
