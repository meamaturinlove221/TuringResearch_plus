# Lane 132 - Repository Strategy

Status: complete.

Round: 151.

## Goal

Decide the repository strategy for TuringResearch: short-term monorepo,
long-term hub-and-spoke ecosystem. This lane does not move code, split
repositories, publish packages, create repositories, or change install behavior.

## Inputs

- `docs/long-term-maintenance-plan.md`
- `docs/public-release-strategy.md`
- `docs/research-os-positioning-v2.md`
- `docs/community-plugin-strategy.md`
- `docs/v0.8.0-roadmap.md`
- `README.md`
- `pyproject.toml`
- `lanes/131_long_term_maintenance.md`
- `lanes/00_master_ledger.md`

## Outputs

- `docs/repository-strategy.md`
- `docs/monorepo-vs-multirepo-decision.md`
- `docs/module-split-policy.md`
- `docs/future-repository-map.md`
- `docs/star-growth-repository-strategy.md`
- `docs/internship-portfolio-positioning.md`
- `README.md`
- `lanes/00_master_ledger.md`

## Decision

1. Do not split repositories immediately.
2. Keep the main `turingresearch` repository as the flagship project.
3. Improve internal modularity first.
4. Split only modules with stable API, complete docs, passing tests, no private
   data, no license risk, available demo, independent value, and clear install
   path.
5. Splits must not dilute flagship star growth.
6. Case studies are preferred early split candidates.
7. Plugins and examples can split later.
8. Core should not move out too early because the flagship repo must remain
   useful and coherent.

## Future Repository Map

- `turingresearch`
- `turingresearch-core`
- `turingresearch-paper`
- `turingresearch-artifacts`
- `turingresearch-dashboard`
- `turingresearch-plugins`
- `turingresearch-vggt-case`
- `turingresearch-examples`

## Boundaries

- No code movement.
- No repository creation.
- No package split.
- No publishing.
- No network access.
- No private path read.
- No plugin execution.
- No release action.
- No old project naming.

## Result

Round 151 establishes the repository strategy: keep TuringResearch as a
flagship monorepo now, modularize internally, and consider future satellite
repositories only after modules are stable, demoable, testable, public-safe,
and independently valuable.
