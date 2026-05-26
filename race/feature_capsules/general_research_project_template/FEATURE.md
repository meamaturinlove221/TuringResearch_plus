# General Research Project Template



Status: feature capsule draft.



Release target: v0.6 Sprint 1.



## 1. Problem



The VGGT template is useful but domain-specific; v0.6 needs a reusable skeleton for new research directions.



## 2. VGGT / Research Motivating Example



A new project should get north star, evidence ledger, artifact plan, routes, related work, advisor pack, dashboard, and lanes without inheriting VGGT claims.



## 3. Upstream / Internal Inspiration



Project Template Generator and VGGT-to-general-template planning.



## 4. User Story



As a researcher, I want to bootstrap a new project with safe planned/empty evidence states and clear review gates.



## 5. Inputs



- project name

- research topic

- owner label

- safety profile

- template options



## 6. Outputs



- ResearchProjectTemplate

- GeneratedProjectSkeleton

- TemplateManifest



## 7. Data Model



ResearchProjectTemplate, TemplateSection, TemplateManifest



## 8. Proposed Commands / Tools



- command: `turing project new`; tool: `project.template_generate`; output: `TemplateManifest`



## 9. Related Contracts



- project_template.yaml

- privacy_data_policy.yaml



## 10. Related Skills



- turingresearch-master-orchestrator

- turingresearch-race-feature-capsule-factory



## 11. Required Tests



- template model tests

- generator tests

- new project workflow fixture



## 12. Risks



- template reads like observed evidence

- domain-specific assumptions leak into generic projects



## 13. Done Criteria



- template emits all required directories

- default evidence is planned/missing

- safety notes are present



## 14. Release Target



v0.6 Sprint 1



## 15. Non-goals



- no automatic literature review

- no observed evidence in template

- no private data copy
