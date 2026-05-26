# Examples Repo Skeleton

Status: design draft.

Round: 160.

This document describes the proposed skeleton for a future
`turingresearch-examples` repository.

## Proposed Tree

```text
turingresearch-examples/
  README.md
  examples_manifest.yaml
  public_demo/
  project_templates/
  demo_workspace/
  dashboard_demo/
  paper_demo/
  advisor_pack_demo/
```

Round 160 only creates the skeleton README and manifest under
`examples/split_repos/turingresearch-examples/`. It does not copy all demo
directories.

## Required README Claims

- This repo is public-demo material for TuringResearch Plus.
- The flagship repo remains the install, star, and release entry point.
- All examples are fake/demo unless clearly marked otherwise.
- No raw data, model files, API keys, private logs, or private VGGT files are
  included.
- Demo output is not research success evidence.

## Manifest Requirements

The manifest must list:

- repo id;
- status;
- flagship repo;
- intended example groups;
- excluded content;
- safety gates;
- sync policy summary;
- human review requirement.

## Split Rule

Do not extract examples into a real repository until public demo tests and
privacy gates pass on the exact extraction set.
