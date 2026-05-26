# Split Candidate: `turingresearch-vggt-case`

Status: design draft.

Round: 159.

This document designs the first future split candidate repository:
`turingresearch-vggt-case`.

No repository is created in this round. No code or private data is moved.

## Purpose

`turingresearch-vggt-case` would be a public-safe case-study repository showing
how TuringResearch Plus was dogfooded on a VGGT human-prior workflow.

It is meant to show process and tooling:

- evidence management;
- route changes;
- failure and blocker tracking;
- advisor pack structure;
- dashboard/case-study outputs;
- redaction and claim safety;
- what remains human research.

## Non-Purpose

The candidate repo is not:

- a VGGT experiment source repository;
- a model training repository;
- a raw data repository;
- a SMPL-X model mirror;
- proof that VGGT experiments succeeded;
- proof that SparseConv3D succeeded;
- a replacement for the flagship TuringResearch repository.

## Flagship Relationship

The flagship repo remains the star and install entry point. The split candidate
must link back to the main repository in the first viewport of its README.

The candidate repo should say:

> This case study demonstrates TuringResearch dogfooding. Install and develop
> TuringResearch from the flagship repository.

## Allowed Content

- public-safe case-study draft;
- redaction report;
- claim safety report;
- fake/demo artifacts;
- manifest describing included files;
- privacy and compliance disclaimers;
- links back to the flagship repo.

## Forbidden Content

- private local paths;
- raw data;
- SMPL-X files;
- large model or prediction payloads;
- private advisor feedback;
- unsupported experiment claims;
- non-public artifacts;
- credentials or API keys.

## Split Readiness

Current decision: `design-only`.

The candidate is promising because a case-study repo can stand alone without
moving core runtime behavior. It still needs a dedicated extraction gate before
any real repository is created.

## Public Safety Requirements

Before split, the candidate must pass:

- privacy gate;
- compliance checklist;
- claim safety report;
- old-name scan;
- no secrets scan;
- no raw data scan;
- no private path scan;
- no model payload scan;
- human release review.
