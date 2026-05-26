# Post-split Docs Linking

Status: planning policy.

Round: 171.

This document defines how docs should link between the flagship repository and
future case/example spoke repositories.

## Link Direction

Primary direction:

1. spoke repo points to flagship;
2. flagship links to spoke only as optional deeper material.

The flagship must not require users to visit a spoke repo to understand install,
quickstart, architecture, safety policy, or core workflows.

## Main Docs Must Retain

- `docs/README.md`
- `docs/docs-index.md`
- `docs/quickstart.md`
- `docs/install.md`
- `docs/examples.md`
- `docs/public-demo-guide.md`
- `docs/plugin-guide.md`
- `docs/dashboard-guide.md`
- `docs/advisor-export-guide.md`
- `docs/limitations.md`
- release and safety docs

## Spoke Link Placement

Recommended placement in main docs:

- README: optional examples/case-study links after quickstart and capability map;
- docs index: `Optional spoke repositories` section;
- examples guide: links to `turingresearch-examples` only after local examples;
- case study guide: links to `turingresearch-vggt-case` as an optional public
  case-study package.

## Broken-link Policy

Until a spoke repo is real, links should point to local design/dry-run docs:

- `docs/split-candidate-vggt-case-repo.md`
- `docs/vggt-case-split-dry-run-report.md`
- `docs/split-candidate-examples-repo.md`
- `docs/examples-repo-split-dry-run-report.md`

Real external links should be added only after the repositories exist and pass
privacy/safety review.
