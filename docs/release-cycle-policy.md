# Release Cycle Policy

Status: planning policy.

Round: 150.

This policy defines the maintenance cycle for planning, implementation,
integration, release candidates, and post-release upkeep.

## Cycle Overview

1. Roadmap planning.
2. Scope lock and feature capsules.
3. Contracts and test plan.
4. Focused implementation rounds.
5. Integration gate.
6. Full fake/default replay.
7. Security, privacy, compliance, and release hygiene audit.
8. Release prep.
9. Release candidate gate.
10. Maintainer review.
11. Optional publication in a separate explicit release round.

## Release Gate Checklist

Before a release candidate can be considered ready:

- full default tests pass;
- `python -m mypy src` passes or exceptions are documented;
- name integrity passes;
- public release hygiene passes;
- privacy gate passes;
- compliance gate passes when relevant;
- public demo tests pass;
- plugin safety checks pass when plugins are in scope;
- optional backends skip gracefully when unavailable;
- docs index, README, release notes, known limitations, and changelog are
  current;
- no secrets, private paths, raw payloads, or private model files are included;
- fake/demo/planned material is not marked observed;
- maintainer approves license and public posture.

## Version Cadence

- Roadmap and planning can happen after every major release prep.
- Minor releases should follow clear scope locks and integration gates.
- Patch releases may happen whenever a user-facing bug, safety issue, docs
  defect, or compatibility issue needs correction.
- Release candidates should be cut only from clean, selectively staged
  branches.

## Branch Policy

- Use feature branches for scoped work.
- Use integration branches for reviewed accumulation.
- Use release candidate branches for frozen release prep.
- Do not push directly from a dirty worktree with unrelated historical changes.
- Do not publish from a planning or integration gate round.

## Documentation Maintenance

Every release prep should update:

- README status and positioning;
- docs index;
- quickstart/install/examples when commands change;
- feature list;
- known limitations;
- test summary;
- upgrade guide;
- public README update notes;
- changelog.

## Security and Privacy Cadence

- Run secret/privacy scan every release candidate.
- Run public demo privacy gate after any public demo change.
- Run compliance review after any case-study or license-relevant change.
- Review plugin permissions after any plugin, registry, or MCP tool-surface
  change.

## What Requires a Separate Explicit Round

- Network upstream scans.
- Publishing to a package index.
- Creating tags.
- Creating GitHub releases.
- Enabling live adapters by default.
- Executing unknown plugins.
- Running remote experiments.
- Reading private project paths.

## Post-release Maintenance

After release, maintainers should:

- record issues and blockers;
- patch docs quickly when public users hit setup confusion;
- triage security reports privately;
- refresh public demos when output formats change;
- archive stale case studies;
- update roadmap and priority board based on real usage.
