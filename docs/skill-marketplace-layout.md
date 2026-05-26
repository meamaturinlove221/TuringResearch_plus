# Skill Marketplace Layout

Status: implemented minimal.

Round 112 organizes repo skills into a local marketplace-style catalog. The
layout is designed for browsing, filtering, and referencing skills in docs,
routing, capability manifests, and future release planning.

## Inputs

- `.agents/skills/*/SKILL.md`
- `docs/skills-index.md`
- `docs/skill-entry-routing.md`
- `docs/capability-index.md`

Feature Capsule `SKILL.md` files remain related planning material. They are not
automatically published as marketplace entries.

## Outputs

- `.agents/MARKETPLACE.md`
- `docs/skill-catalog.md`
- `docs/skill-categories.md`
- `contracts/skill_marketplace.yaml`

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

Not every category has a repo skill yet. Empty categories are allowed in the
layout so later skills can be added without changing the contract.

## Safety Boundary

- Local documentation only.
- No online marketplace.
- No upload.
- No remote install.
- No automatic agent runtime.
- Skill names must keep the `turingresearch-*` prefix.
- The catalog does not override round instructions or execute skills.
