# Lane 93 - Skill Marketplace Layout

Status: implemented minimal.

## Scope

Round 112 organizes `.agents/skills` into a local marketplace-style catalog for
browsing, filtering, and referencing skills.

## Added

- `src/turing_research_plus/skill_market/`
- `contracts/skill_marketplace.yaml`
- `docs/skill-marketplace-layout.md`
- `docs/skill-catalog.md`
- `docs/skill-categories.md`
- `.agents/MARKETPLACE.md`
- skill marketplace unit and contract tests

## Categories

- orchestration
- evidence
- artifact
- visual
- advisor
- pdf
- paper
- web
- remote
- route
- failure
- dashboard
- workspace
- plugin
- release

## Boundaries

- Local documentation only.
- No online marketplace.
- No skill upload.
- No remote install.
- No automatic agent runtime.
- Feature Capsule `SKILL.md` files remain planning material unless promoted to
  `.agents/skills`.
