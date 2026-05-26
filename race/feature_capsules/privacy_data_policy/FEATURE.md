# Privacy / Data Policy



Status: feature capsule draft.



Release target: v0.6 Sprint 1.



## 1. Problem



Multi-project workflows increase the risk of leaking private paths, raw data, credentials, model files, and unreleased results.



## 2. VGGT / Research Motivating Example



A workspace dashboard must not expose private VGGT paths, raw captures, API keys, or private model files.



## 3. Upstream / Internal Inspiration



Public Release Hardening, Secret Scan Policy, and Future UI Dashboard planning.



## 4. User Story



As a maintainer, I want privacy gates that classify unsafe files and block public/demo exports before review.



## 5. Inputs



- workspace files

- project manifests

- examples

- dashboard outputs

- export bundles



## 6. Outputs



- PrivacyScanReport

- DataClassificationReport

- ReleaseGateDecision



## 7. Data Model



PrivacyScanReport, DataPolicyRule, ReleaseGateDecision



## 8. Proposed Commands / Tools



- command: `turing privacy scan`; tool: `privacy.scan`; output: `PrivacyScanReport`



## 9. Related Contracts



- privacy_data_policy.yaml

- public_release_hygiene.yaml



## 10. Related Skills



- turingresearch-race-source-hygiene

- turingresearch-qa-release



## 11. Required Tests



- privacy model tests

- scanner tests

- release gate contract tests



## 12. Risks



- false negatives

- allowlist drift

- unsafe public examples



## 13. Done Criteria



- policy flags secrets/raw data/private model files

- public examples remain demo-safe

- release decision is explicit



## 14. Release Target



v0.6 Sprint 1



## 15. Non-goals



- no destructive cleanup

- no automatic deletion

- no upload of scan results
