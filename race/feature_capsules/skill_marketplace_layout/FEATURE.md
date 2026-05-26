# Skill Marketplace Layout



Status: feature capsule draft.



Release target: v0.6 Sprint 2.



## 1. Problem



Repo skills are useful, but future public skill distribution needs directory and metadata conventions before install flows expand.



## 2. VGGT / Research Motivating Example



A TuringResearch skill should declare when to use it, contracts, tests, safety boundaries, and release target before being listed publicly.



## 3. Upstream / Internal Inspiration



Skill ENTRY / Routing Table and MCP marketplace readiness planning.



## 4. User Story



As a maintainer, I want a skill marketplace layout that can be reviewed before any install automation exists.



## 5. Inputs



- skill metadata

- SKILL.md files

- routing table

- capability manifest



## 6. Outputs



- SkillMarketplaceIndex

- SkillReviewReport



## 7. Data Model



SkillMarketplaceIndex, SkillMarketplaceEntry, SkillReviewReport



## 8. Proposed Commands / Tools



- command: `turing skills marketplace-check`; tool: `skills.marketplace_check`; output: `SkillReviewReport`



## 9. Related Contracts



- skill_marketplace_layout.yaml

- skill_routing.yaml



## 10. Related Skills



- turingresearch-master-orchestrator

- turingresearch-qa-release



## 11. Required Tests



- skill marketplace layout tests

- routing consistency tests

- skills integrity tests



## 12. Risks



- skill name drift

- unsafe skill instructions

- install expectation without installer



## 13. Done Criteria



- layout is documented

- entries align with turingresearch-* names

- no automatic install



## 14. Release Target



v0.6 Sprint 2



## 15. Non-goals



- no marketplace publishing

- no remote skill install

- no automatic agent runtime
