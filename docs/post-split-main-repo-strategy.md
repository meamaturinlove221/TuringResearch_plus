# Post-split Main Repo Strategy

Status: planning policy.

Round: 171.

This document defines how the main TuringResearch repository should remain the
flagship if future spoke repositories such as `turingresearch-vggt-case` or
`turingresearch-examples` are physically created.

No repository split happens in this round.

## Decision

The main repository remains the only flagship.

Future split repositories are optional spokes. They may host demo/case material,
but they must not replace the main repository, duplicate the install story, or
scatter the product narrative.

## Main Repo Responsibilities

The main repo must keep:

- first-screen README positioning;
- install and quickstart;
- package metadata and CLI/MCP entry points;
- full feature map;
- docs index;
- public demo overview;
- split candidate links;
- release gates;
- privacy, compliance, quality, and plugin safety policies;
- roadmap and version history.

## Spoke Repo Responsibilities

Future split repos should be narrow:

- `turingresearch-vggt-case`: public-safe dogfooding case study only;
- `turingresearch-examples`: fake/demo examples and templates only.

They should link back to the flagship in the first README section and say that
the main repo remains the install, docs, release, and star entry point.

## What Must Not Change

- The install path must remain centered on the main repo.
- The main repo must keep a complete quickstart.
- The main repo must keep enough examples to be understandable without visiting
  a spoke.
- The main repo must not become a landing-page shell.
- Spoke repos must not claim to be the canonical package.

## Flagship Protection Rules

1. Every spoke README links to the flagship above the fold.
2. Every spoke states it is optional demo/case material.
3. Every spoke says it does not replace the main repo.
4. The flagship README links out only after showing the core product story.
5. Main repo docs preserve quickstart, architecture, examples, plugin safety,
   dashboard/export, paper workflow, and privacy/compliance gates.
6. Main repo release notes mention spokes as optional public artifacts, not as
   required dependencies.

## Split Validation Gate

Before any actual split, confirm:

- main repo README still explains the product in one screen;
- quickstart still works without any spoke repo;
- examples remain discoverable from the main docs;
- spoke README points back to flagship;
- no private data or unsupported claims in spoke;
- no split changes package import paths.

## Non-goals

- No split in this round.
- No code movement.
- No package rename.
- No install-path change.
- No release action.
