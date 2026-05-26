# Module Split Readiness Gate

Status: gate complete.

Round: 156.

This gate checks whether the current monorepo modular layout has reached the
minimum bar for a future repository split. It does not split repositories,
move code, rename packages, or remove compatibility imports.

## Gate Decision

Overall decision: `not-ready-for-code-split`.

The repository is ready for continued internal modularization. It is not ready
for an actual repository split because most target namespaces are still
facade/re-export layers and several modules still need API stabilization,
standalone docs, and independent demo gates.

## Evidence Reviewed

- `docs/monorepo-modular-layout.md`
- `docs/module-split-readiness-matrix.md`
- `docs/module-public-api-contracts.md`
- `tests/contract/test_new_namespace_imports.py`
- `tests/contract/test_legacy_namespace_compat.py`

## Candidate Split Order

1. `turingresearch-vggt-case`
2. `turingresearch-examples`
3. `turingresearch-plugins`
4. `turingresearch-paper`
5. `turingresearch-artifact`
6. `turingresearch-dashboard`
7. `turingresearch-core`

## Readiness Table

| Candidate | Gate status | Why |
| --- | --- | --- |
| `turingresearch-vggt-case` | first candidate after public-safe review | A case-study repo can be independently browsed and linked back to the flagship without moving core runtime. |
| `turingresearch-examples` | first candidate after demo-safe review | Examples can stand alone as public demos while keeping the main repo installable and complete. |
| `turingresearch-plugins` | wait for API stabilization | Plugin loading, MCP mapping, compatibility, and sandbox policy exist, but plugin behavior is still policy-level and disabled-by-default. |
| `turingresearch-paper` | wait for API stabilization | Paper APIs are useful but still experimental; citation, claim, and section readiness contracts need more beta hardening. |
| `turingresearch-artifact` | wait for API stabilization | Artifact flows remain coupled to privacy, adapter safety, handoff, and fake/live boundaries. |
| `turingresearch-dashboard` | wait for stable DTOs | Dashboard/export has public value, but UI/export DTOs and optional backend behavior need a clearer standalone package story. |
| `turingresearch-core` | do not split early | Core defines workspace, privacy, quality, template, evidence, and release semantics; removing it too early would hollow out the flagship. |

## Why Case And Examples Fit First

Case-study and example repositories can be read, demoed, tested, and linked as
standalone public material without changing package imports. They are also the
least likely to destabilize the main package because they do not need to own
core execution semantics.

They are still blocked until each candidate has:

- public-safe redaction;
- no raw data or private paths;
- no license overclaim;
- repeatable demo tests;
- clear links back to the flagship repo;
- an explicit statement that demos are not research results.

## Why Core Should Stay In The Flagship

Core should remain in the main repository because it carries the shared mental
model of TuringResearch:

- workspace and project registry;
- privacy and quality gates;
- project templates;
- evidence and status semantics;
- release and regression gate expectations.

If core is split too early, the flagship can become a thin wrapper around
external packages. That would make the main repo less useful, harder to demo,
and less compelling for stars or onboarding.

## Why Paper And Artifact Need Stabilization

Paper and artifact modules have strong future split potential, but their public
surface is still experimental.

Paper still needs:

- stable section and claim DTOs;
- citation-grade review boundaries;
- independent paper beta examples;
- clearer final-paper non-goal docs.

Artifact still needs:

- stable artifact and handoff DTOs;
- clearer remote adapter safety policy;
- independent fake artifact demo;
- privacy/compliance gates for export and redistribution.

## Star And Portfolio Strategy

Splitting too early would scatter attention. The flagship repo should keep a
complete, impressive demo path and remain the canonical place for install,
docs, workflows, and release gates. Future spoke repos should feed interest
back into the flagship rather than compete with it.

## Main Repo Completeness Requirement

Before any split, the flagship must still contain or link clearly to:

- a working install path;
- public demo suite;
- multi-project workspace demo;
- plugin safety story;
- dashboard/export story;
- paper assembly story;
- privacy/compliance gate;
- quality/regression gate;
- README and docs index that make the system understandable without visiting a
  spoke repository.

## Minimum Split Bar

A module can be reconsidered only after it has:

- stable or beta API contract;
- complete docs;
- passing independent tests;
- no private data;
- no unresolved license risk;
- demo availability;
- independent value;
- compatibility story for the main repo.

## Current Result

The current modular layout is a good foundation. It is not a green light to
split repositories yet.
