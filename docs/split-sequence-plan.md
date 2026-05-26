# Split Sequence Plan

Status: design sequence.

Round: 162.

This sequence keeps the flagship repository central while preparing future
spoke repositories.

## Phase 0: Current State

Keep all split candidates as skeletons under `examples/split_repos/`.

## Phase 1: Case Study Rehearsal

Candidate: `turingresearch-vggt-case`.

Actions:

1. freeze exact export set;
2. run privacy scan;
3. run claim safety scan;
4. run compliance checklist;
5. verify flagship link;
6. verify no unsupported claims;
7. get maintainer approval.

## Phase 2: Examples Rehearsal

Candidate: `turingresearch-examples`.

Actions:

1. freeze exact public demo and template export set;
2. run public demo tests;
3. run privacy gate;
4. run no-secrets/no-raw-data scan;
5. verify fake/demo markings;
6. define sync policy.

## Phase 3: Plugin Catalog Rehearsal

Candidate: `turingresearch-plugins`.

Actions:

1. freeze manifest-only plugin catalog;
2. run plugin compatibility harness;
3. run sandbox policy review;
4. run extension safety gate;
5. verify third-party plugins disabled by default;
6. verify no executable unknown plugin code.

## Phase 4: Real Split Decision

Only after Phases 1-3 are reviewed should maintainers decide whether to create
actual repositories.

The main repo remains the hub throughout.
