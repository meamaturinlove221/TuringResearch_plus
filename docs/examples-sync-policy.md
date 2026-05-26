# Examples Sync Policy

Status: design policy.

Round: 160.

This policy defines how a future `turingresearch-examples` repository would stay
aligned with the flagship repo.

## Source Of Truth

The flagship TuringResearch Plus repo remains the source of truth for:

- package install instructions;
- public demo policy;
- release gates;
- privacy and compliance gates;
- current examples until split approval.

The examples repo may mirror approved public-safe examples only.

## Allowed Sync Content

- public demo files;
- generated project template examples;
- demo workspace;
- static dashboard demo;
- paper scaffold demo;
- advisor pack demo;
- example manifests and READMEs.

## Blocked Sync Content

- private VGGT files;
- raw data;
- model files;
- API keys or tokens;
- huge artifacts;
- private logs;
- private advisor feedback;
- live adapter credentials;
- unsupported experiment claims.

## Sync Gate

Before any sync:

1. run public demo tests;
2. run privacy gate;
3. scan for secrets and private paths;
4. scan for raw data and model payloads;
5. verify all examples are marked fake/demo;
6. verify README links back to flagship;
7. get human maintainer approval.

## Versioning

The examples repo should not claim independent product versions until it has a
dedicated release process. It should reference the compatible flagship version
instead.

## Drift Policy

If examples drift from the flagship API, update the flagship first or mark the
example as archived. Do not silently patch examples in the split repo in a way
that hides main-repo incompatibility.
