# Long-term Maintenance Plan

Status: planning policy.

Round: 150.

This plan defines how TuringResearch Plus should be maintained after the v0.7
release-candidate work. It is a maintenance policy, not a release action and
not an implementation round.

## Maintenance Principles

- Keep the project local-first, fake/demo-first, optional-live, and
  review-first.
- Preserve evidence boundaries: planned, demo, missing, not-enough-evidence,
  and observed must stay distinct.
- Treat public demos, plugins, case studies, and paper-writing outputs as
  release-sensitive surfaces.
- Prefer small scoped releases over large unreviewed drops.
- Keep safety, privacy, compliance, and documentation gates visible in every
  release cycle.

## Version Cadence

| Release type | Cadence | Purpose |
| --- | --- | --- |
| Patch | as needed | Fix bugs, docs defects, safety wording, contract drift, or broken fake/default workflows. |
| Minor | planned milestone | Add scoped local-first capabilities after scope lock, feature capsules, contracts, tests, and integration gates. |
| Release candidate | before public release | Freeze feature behavior, run full fake/default replay, security/privacy audit, docs review, and maintainer approval. |
| Roadmap update | after each release prep | Reassess priorities, risks, non-goals, and sprint recommendations. |

## Branch Policy

- `dev/mainline`: integration branch for reviewed development.
- `feature/<scope>`: scoped implementation or planning branches.
- `release/<version>-rc`: release candidate branch after selective staging and
  maintainer approval.
- Avoid direct pushes from dirty worktrees.
- Avoid bundling unrelated round outputs into a release branch.
- Use selective staging for release candidates when historical worktree changes
  are mixed.

## Release Gate

Every release candidate should pass:

1. Full default tests.
2. `python -m mypy src`.
3. Name integrity.
4. Public release hygiene.
5. Privacy gate.
6. Compliance gate when public examples or case studies are included.
7. Plugin safety and compatibility gates when plugin surfaces are included.
8. Public demo replay.
9. Quality / regression gate.
10. Docs index and README review.
11. Maintainer review of license posture and release notes.

## Monitoring Cadence

| Area | Cadence | Notes |
| --- | --- | --- |
| Upstream scan | explicit upstream-scan round only | Network access is not default; record snapshots and source hygiene. |
| Security scan | every RC and after dependency/tooling changes | Include secret-like values, private paths, unsafe plugin permissions, and package metadata. |
| Privacy review | every public demo, case study, and release candidate | Confirm no private paths, private artifacts, advisor-private notes, or sensitive payloads. |
| Compliance review | every case study and release candidate | Review dataset/model/code/paper licenses as a human-review aid, not legal advice. |
| Docs review | every release prep and after major feature lanes | Verify README honesty, optional-live labels, fake/demo boundaries, and known limitations. |
| Plugin review | every registry or plugin-surface change | Validate manifest, permissions, sandbox policy, compatibility, docs, tests, and disabled defaults. |

## Public Demo Refresh

- Refresh demos when templates, dashboards, exports, privacy gates, or paper
  assembly behavior changes.
- Keep every public demo clearly marked demo-only.
- Never mark demo evidence as observed.
- Keep demos small, synthetic, and free of private payloads.
- Run public demo workflow tests and privacy checks after refresh.

## Case Study Updates

- VGGT and other case studies must remain dogfooding or evidence-reviewed
  material.
- Update case studies only when new reviewed artifacts, redaction reports,
  compliance reports, and claim safety checks exist.
- Do not claim experiment success without evidence ledger support.
- Keep SparseConv3D success unclaimed unless real evidence supports it.
- Preserve sections for what remains human work and what not to claim.

## Plugin Maintenance

- Unknown third-party plugins stay disabled by default.
- Plugin registry entries require manifest validation, compatibility report,
  sandbox policy review, docs, tests, and human approval.
- Runtime plugin execution requires a later gate with real sandbox enforcement.
- Any plugin requesting code execution, shell access, secrets, remote write, or
  live network access is release-sensitive.

## Deprecated Feature Policy

- Mark deprecated features in docs before removal.
- Keep compatibility shims for at least one minor release when practical.
- Provide migration notes for renamed commands, modules, contracts, or examples.
- Do not remove safety checks without an explicit replacement.
- Do not silently change evidence status semantics.

## Compatibility Policy

- Public import surfaces should remain stable within a minor line.
- Contract schema changes require tests and upgrade notes.
- CLI/MCP changes require docs, examples, and smoke checks.
- Optional backend behavior must keep graceful skip paths.
- Fake/default workflows must remain runnable without live services.

## Maintenance Backlog

- Convert recurring manual scans into documented checklist commands.
- Add docs link checks when the docs set stabilizes.
- Keep feature-capsule and priority-board entries aligned after each roadmap.
- Keep release notes, changelog, and version files synchronized.
- Revisit license posture before any public publication.
