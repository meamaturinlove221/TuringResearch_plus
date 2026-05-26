# Post-split Star Protection

Status: planning policy.

Round: 171.

The goal of future split repositories is to make the TuringResearch ecosystem
easier to understand, not to drain attention from the main repo.

## Principle

The flagship repo should collect the primary star and first impression.

Spoke repositories should deepen the story and send users back to the flagship.

## Star Protection Rules

- Main repo README remains the polished landing page.
- Main repo keeps quickstart, install, docs index, and core demo.
- Spoke README files link back to the flagship near the top.
- Spoke repos describe themselves as optional demo/case material.
- Spoke repos do not claim to be the main package.
- Spoke repos do not duplicate the full roadmap.
- Spoke repos do not split issues or support in a confusing way before there is
  maintainer capacity.

## Recommended Star Flow

1. User discovers main repo.
2. User sees local-first Research OS positioning.
3. User runs quickstart or browses public demo.
4. User optionally clicks case/examples spoke repo.
5. Spoke README points back to the main repo for install, docs, and star.

## Risk Controls

| Risk | Control |
| --- | --- |
| Spoke gets mistaken for main project | First README section links to flagship and says optional demo/case only. |
| Main repo looks empty after split | Keep local examples, docs, screenshots, and quickstart in main repo. |
| Stars fragment across repos | Make spoke repos explicitly route stars to main repo. |
| Users install from wrong repo | Keep package install instructions only in flagship. |
| Case repo overclaims research result | Keep claim-safety and human-review labels visible. |

## Interview And Portfolio Use

Spoke repos can be useful in interviews as focused artifacts, but the main repo
should remain the proof of system design, testing discipline, and product
thinking.
