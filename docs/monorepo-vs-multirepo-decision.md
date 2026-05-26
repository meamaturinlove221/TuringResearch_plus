# Monorepo vs Multirepo Decision

Status: decision record.

Round: 151.

## Decision Summary

TuringResearch should stay in a monorepo for now.

Long term, it may become a hub-and-spoke ecosystem, but only after modules have
stable APIs, complete docs, passing independent tests, demo value, and clean
privacy/license posture.

## Required Conclusions

1. Short term: do not split the repository immediately.
2. The main `turingresearch` repository is the flagship project.
3. Improve internal modularity before moving code.
4. Split only modules that are stable, independently installable,
   independently demoable, and independently testable.
5. Repository splits must not dilute the flagship repository's star growth.
6. Case studies can be early independent showcase candidates.
7. Plugins and examples can split later.
8. Core should not be moved out too early; otherwise the flagship repository
   becomes empty and confusing.

## Monorepo Advantages

- Stronger first impression for public users.
- One README, one quickstart, one docs index, one public demo path.
- Easier release gates for privacy, compliance, plugins, and fake/demo
  boundaries.
- Easier internal refactoring while APIs are still settling.
- Better chance of concentrating stars and issues in one visible project.

## Monorepo Risks

- The repository may feel large.
- Users may have trouble finding the right module.
- Optional features can look like default behavior.
- Public demos, case studies, plugins, and core code can blur together.

Mitigations:

- improve docs index;
- add clear module boundaries;
- keep optional/live features labeled;
- keep examples demo-safe;
- introduce future repository map before splitting.

## Multirepo Advantages

- Clear ownership for mature modules.
- Smaller install and contribution surfaces.
- Easier dedicated demos for case studies and plugin examples.
- Better long-term ecosystem shape.

## Multirepo Risks

- Split attention and stars.
- More release coordination.
- More duplicated docs and CI.
- More confusing install paths.
- More places to accidentally drift on safety policy.

Mitigations:

- split only after stable APIs;
- keep the flagship repo as the hub;
- require shared release gates;
- require every satellite to link back to the flagship;
- maintain compatibility and migration docs.

## Decision Gate For Splitting

A proposed split should answer:

- What independent user value does the repository provide?
- Can it be installed and tested alone?
- Does it have a public-safe demo?
- Are docs complete?
- Are privacy and license risks cleared?
- Does the main repo still run and explain itself clearly?
- Does this split help, rather than dilute, public discovery?

## Current Recommendation

Keep all code in the current repository. Start by improving internal module
boundaries and docs. Revisit repository splitting after v0.8 dashboard, paper
beta, public plugin registry draft, and additional case studies create clearer
independent surfaces.
