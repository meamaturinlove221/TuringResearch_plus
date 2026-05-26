# Multi-project Workspace Skill



Status: planning skill draft.



Use this skill when a task is about `multi_project_workspace` planning, contract alignment, test

planning, or review. This skill does not execute live services, upload private

research data, or promote proposed evidence to observed evidence.



## When to Use



- The user asks for `Multi-project Workspace` scope, docs, contracts, tests, or review.

- The task needs v0.6 planning consistency.

- The output should remain local-first and review-required.



## Inputs



- project metadata

- project root paths

- evidence summaries

- artifact summaries

- dashboard summaries



## Outputs



- WorkspaceRegistry

- WorkspaceOverview

- Markdown workspace summary



## Safety Rules



- Do not use network access by default.

- Do not read private VGGT paths.

- Do not package secrets, raw data, or private model files.

- Do not mark fake/demo/planned results as observed.

- Do not claim experiment success without evidence.



## Related Contracts



- multi_project_workspace.yaml

- project_template.yaml

- privacy_data_policy.yaml
