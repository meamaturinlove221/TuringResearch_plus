# Lane 21: Upstream Watch Baseline

## Scope

Round 38.7 creates the first public upstream watch baseline for selected
Pthahnix Neocortica-related repositories and Yogsoth AI repositories.

## Done

- Added upstream watch target registry.
- Added baseline schema documentation.
- Added learning policy documentation.
- Added scan report template.
- Added baseline, diff, and report models under `turing_research_plus.upstream`.
- Added unit tests for upstream models, baseline classification, and diffing.

## Non-Goals

- No upstream modification.
- No incompatible code copying.
- No live auto-sync.
- No Handoff, NAS, SSH, GitHub Artifact Sync, or cloud sync implementation.
- No VGGT local path reads.

## Baseline Meaning

This is the first baseline. It cannot prove that a feature was newly added. It
only records public upstream metadata and unresolved repositories for future
comparison.
