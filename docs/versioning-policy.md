# Versioning Policy

Status: planning policy.

Round: 150.

TuringResearch Plus uses explicit version updates during release-prep rounds.
Version changes must be paired with release notes, feature lists, known
limitations, test summaries, and changelog updates.

## Version Cadence

| Version kind | Example | Use |
| --- | --- | --- |
| Alpha | `0.x.0a0` | Early feature aggregation or public-facing alpha planning. |
| Beta | `0.x.0b0` | Stabilization after alpha integration gates. |
| Release candidate | `0.x.0rc0` | Candidate release after full replay, security/privacy audit, docs review, and maintainer approval. |
| Final | `0.x.0` | Public release only after clean branch review and explicit release approval. |
| Patch | `0.x.y` | Bug fixes, docs fixes, safety fixes, compatibility patches, and test repairs. |

## Files That Must Stay Synchronized

- `VERSION`
- `pyproject.toml`
- `src/turing_research/__init__.py`
- `src/turing_research_plus/__init__.py`
- package import tests
- public import surface tests
- `CHANGELOG.md`
- release notes and test summary docs

## Branch Policy

- Version bumps belong in release-prep or release-candidate branches.
- Feature branches should not bump package versions unless the round explicitly
  asks for release prep.
- Dirty worktrees require selective staging before version commits.
- Do not tag or publish during planning-only rounds.

## Compatibility Policy

- Patch releases should not break public imports, CLI entrypoints, MCP
  entrypoints, or existing fake/default examples.
- Minor releases may add contracts, modules, and docs, but must document any
  behavior changes.
- Contract-breaking changes require migration notes and tests.
- Optional dependencies must remain optional unless a future release explicitly
  changes that policy.

## Deprecation Policy

1. Mark feature, command, contract, or doc surface as deprecated.
2. Add migration notes.
3. Keep tests for the replacement.
4. Keep compatibility shims for at least one minor release when practical.
5. Remove only after a release gate confirms the migration path.

## Release Labels

Every release document should state whether the release is:

- planning;
- alpha;
- beta;
- release candidate;
- final;
- fake/default only;
- optional-live;
- review-first.

## What Versioning Must Not Imply

- A release candidate is not a public release.
- A roadmap is not an implementation commitment.
- A version bump does not imply experiment success.
- Optional live or export adapters do not become default behavior.
- Paper-writing support does not become final paper authorship.
