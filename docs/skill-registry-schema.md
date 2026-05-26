# Skill Registry Schema

Status: implemented minimal.

`SkillRegistryEntry` records:

- `skill_name`
- `path`
- `role`
- `when_to_use`
- `inputs`
- `outputs`
- `related_contracts`
- `related_lanes`
- `related_modules`
- `status`
- `release_target`

`SkillRoute` records:

- `category`
- `recommended_skill`
- `ranked_skills`
- `related_lane`
- `related_contracts`
- `keywords`

`SkillRoutingDecision` records:

- `query`
- `category`
- `recommended_skill`
- `ranked_skills`
- `confidence`
- `rationale`
- `related_lane`
- `does_not_execute`

All skill names must use the `turingresearch-*` prefix.
