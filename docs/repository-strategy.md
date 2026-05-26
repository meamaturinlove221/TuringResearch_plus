# Repository Strategy

Status: planning policy.

Round: 151.

This document defines the repository strategy for TuringResearch Plus. It does
not move code, split repositories, publish packages, create GitHub repositories,
or change install behavior.

## Decision

TuringResearch should remain a **short-term monorepo** and evolve toward a
**long-term hub-and-spoke repository ecosystem** only after modules become
stable, independently useful, independently testable, and public-safe.

The flagship repository should stay `turingresearch`. It should continue to
hold the primary story, onboarding path, docs index, public demo, release
notes, and integration gates. Satellite repositories can appear later, but they
must not make the main repository feel empty or confusing.

## Why Not Split Immediately

- The main product story is still best explained as one local-first research OS.
- Many modules share safety concepts: evidence status, privacy gates, fake/demo
  boundaries, plugin policy, and release hygiene.
- Premature repository splits would multiply docs, tests, release gates,
  versioning, and support burden.
- Public star growth is easier when the flagship repo has the full narrative,
  screenshots/demos, and practical examples.
- Core package separation too early would make the flagship repository look
  hollow before the ecosystem has enough gravity.

## Short-term Strategy

1. Keep one flagship repository.
2. Improve internal module boundaries.
3. Keep contracts, docs, examples, tests, and release gates colocated.
4. Keep public demos and case studies visible in the main repo.
5. Treat split candidates as documented modules, not separate repositories.
6. Use package/module APIs and docs to simulate future repository seams.

## Long-term Strategy

Move toward hub-and-spoke only when the ecosystem can support it:

- flagship repository remains the hub;
- satellite repositories provide independently valuable modules;
- each satellite has docs, tests, examples, license review, and release gates;
- main repo still installs and demos coherently without requiring users to
  understand the whole ecosystem.

## Split Eligibility

A module can be considered for a new repository only if it has:

- stable API;
- complete docs;
- passing tests;
- no private data;
- no unresolved license risk;
- available demo;
- independent value;
- clear installation path;
- compatibility policy;
- release ownership;
- no confusion when used from the main repo.

## Preferred First Split Candidates

Case studies can be first because they are presentation-heavy and can stand
alone without draining the core product:

1. `turingresearch-vggt-case`
2. `turingresearch-examples`
3. `turingresearch-plugins`
4. `turingresearch-dashboard`

Core packages should split last, if at all:

- `turingresearch-core`
- `turingresearch-paper`
- `turingresearch-artifacts`

## What Must Stay In The Flagship Repo

- README and product positioning.
- Quickstart and install path.
- Core package metadata.
- Integration tests and release gates.
- Public demo path.
- Docs index.
- Compatibility and migration guides.
- Evidence/privacy/plugin/release safety policies.
- Links to every satellite repository.

## Star Growth Strategy

The flagship repository should collect attention first. Satellite repositories
should amplify the flagship, not compete with it.

Recommended public posture:

- put flagship screenshots, demos, and case-study summaries in the main repo;
- link satellites as optional deeper dives;
- keep install and quickstart in the flagship;
- make every satellite README point back to the flagship;
- avoid splitting a module before it can attract users on its own.

## Non-goals

- No immediate repository split.
- No code movement in Round 151.
- No package renaming.
- No publication.
- No GitHub repository creation.
- No weakening of privacy, license, or release gates.
- No old project naming.
