# Multi-project Workspace



Status: feature capsule draft.



Release target: v0.6 Sprint 1.



## 1. Problem



TuringResearch Plus can organize a single research line well, but v0.6 needs a safe way to track multiple research projects without mixing evidence.



## 2. VGGT / Research Motivating Example



A VGGT human-prior project and a separate scene-reconstruction project should share workflow patterns while keeping evidence and artifacts separate.



## 3. Upstream / Internal Inspiration



Round 102 Research OS positioning and the VGGT-to-general-template planning documents.



## 4. User Story



As a researcher, I want a workspace overview that shows each project's status, blockers, evidence state, and next action.



## 5. Inputs



- project metadata

- project root paths

- evidence summaries

- artifact summaries

- dashboard summaries



## 6. Outputs



- WorkspaceRegistry

- WorkspaceOverview

- Markdown workspace summary



## 7. Data Model



WorkspaceProject, WorkspaceRegistry, WorkspaceOverview



## 8. Proposed Commands / Tools



- command: `turing workspace list`; tool: `workspace.list`; output: `WorkspaceOverview`

- command: `turing workspace summarize`; tool: `workspace.summarize`; output: `WorkspaceSummary`



## 9. Related Contracts



- multi_project_workspace.yaml

- project_template.yaml

- privacy_data_policy.yaml



## 10. Related Skills



- turingresearch-master-orchestrator

- turingresearch-cache-and-ledger



## 11. Required Tests



- workspace model tests

- registry loader tests

- demo workspace workflow test



## 12. Risks



- cross-project evidence leakage

- private path exposure

- dashboard overclaiming



## 13. Done Criteria



- workspace registry can load fake/demo projects

- overview marks all project summaries review-required

- no evidence crosses projects automatically



## 14. Release Target



v0.6 Sprint 1



## 15. Non-goals



- no SaaS workspace

- no cloud account system

- no automatic project discovery outside explicit roots
