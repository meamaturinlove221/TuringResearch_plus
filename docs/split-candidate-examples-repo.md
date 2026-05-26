# Split Candidate: `turingresearch-examples`

Status: design draft.

Round: 160.

This document designs the future `turingresearch-examples` repository. No
repository is created in this round and no files are moved out of the flagship
monorepo.

## Purpose

`turingresearch-examples` would be a public-safe examples repository that helps
new users explore TuringResearch Plus without private data, live services, or
research-result overclaims.

The repo should show:

- public demo suite;
- project template examples;
- demo workspace;
- dashboard demo;
- paper demo;
- advisor pack demo;
- fake/live boundary;
- privacy-first policy.

## Flagship Relationship

The flagship TuringResearch Plus repository remains the main star, install,
docs, release, and contribution entry point.

Every examples repo README should link to the flagship in the first section and
say that examples are optional public walkthrough material.

## Proposed Contents

- `public_demo/`
- `project_templates/`
- `demo_workspace/`
- `dashboard_demo/`
- `paper_demo/`
- `advisor_pack_demo/`
- `examples_manifest.yaml`

## Excluded Content

- private VGGT files;
- raw data;
- model files;
- API keys;
- huge artifacts;
- real private logs;
- private advisor feedback;
- unsupported experiment success claims.

## Why This Is A Good Split Candidate

Examples can stand alone without moving core runtime behavior. They are easier
to make public-safe than core modules and can help users understand the flagship
project quickly.

They should not split until:

- public demo tests pass;
- privacy gate passes;
- no raw data or private paths are present;
- README points back to flagship;
- sync policy is clear;
- examples do not imply research success.

## Current Round 160 Decision

Design-only. Keep examples in the monorepo for now. Use
`examples/split_repos/turingresearch-examples/` as a skeleton for future
extraction review.
