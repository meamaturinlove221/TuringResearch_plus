# General Research Project Template Skill



Status: planning skill draft.



Use this skill when a task is about `general_research_project_template` planning, contract alignment, test

planning, or review. This skill does not execute live services, upload private

research data, or promote proposed evidence to observed evidence.



## When to Use



- The user asks for `General Research Project Template` scope, docs, contracts, tests, or review.

- The task needs v0.6 planning consistency.

- The output should remain local-first and review-required.



## Inputs



- project name

- research topic

- owner label

- safety profile

- template options



## Outputs



- ResearchProjectTemplate

- GeneratedProjectSkeleton

- TemplateManifest



## Safety Rules



- Do not use network access by default.

- Do not read private VGGT paths.

- Do not package secrets, raw data, or private model files.

- Do not mark fake/demo/planned results as observed.

- Do not claim experiment success without evidence.



## Related Contracts



- project_template.yaml

- privacy_data_policy.yaml
