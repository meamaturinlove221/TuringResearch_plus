# Skill Marketplace Layout Skill



Status: planning skill draft.



Use this skill when a task is about `skill_marketplace_layout` planning, contract alignment, test

planning, or review. This skill does not execute live services, upload private

research data, or promote proposed evidence to observed evidence.



## When to Use



- The user asks for `Skill Marketplace Layout` scope, docs, contracts, tests, or review.

- The task needs v0.6 planning consistency.

- The output should remain local-first and review-required.



## Inputs



- skill metadata

- SKILL.md files

- routing table

- capability manifest



## Outputs



- SkillMarketplaceIndex

- SkillReviewReport



## Safety Rules



- Do not use network access by default.

- Do not read private VGGT paths.

- Do not package secrets, raw data, or private model files.

- Do not mark fake/demo/planned results as observed.

- Do not claim experiment success without evidence.



## Related Contracts



- skill_marketplace_layout.yaml

- skill_routing.yaml
