# Privacy / Data Policy Skill



Status: planning skill draft.



Use this skill when a task is about `privacy_data_policy` planning, contract alignment, test

planning, or review. This skill does not execute live services, upload private

research data, or promote proposed evidence to observed evidence.



## When to Use



- The user asks for `Privacy / Data Policy` scope, docs, contracts, tests, or review.

- The task needs v0.6 planning consistency.

- The output should remain local-first and review-required.



## Inputs



- workspace files

- project manifests

- examples

- dashboard outputs

- export bundles



## Outputs



- PrivacyScanReport

- DataClassificationReport

- ReleaseGateDecision



## Safety Rules



- Do not use network access by default.

- Do not read private VGGT paths.

- Do not package secrets, raw data, or private model files.

- Do not mark fake/demo/planned results as observed.

- Do not claim experiment success without evidence.



## Related Contracts



- privacy_data_policy.yaml

- public_release_hygiene.yaml
