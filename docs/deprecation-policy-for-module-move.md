# Deprecation Policy For Module Move

Status: planning policy.

Round: 153.

This policy defines how to deprecate old module paths during a future namespace
move. It does not deprecate anything in Round 153.

## Deprecation Timeline

| Stage | Timing | Behavior |
| --- | --- | --- |
| Planning | current | Document target namespaces; no code change. |
| Preview | future minor | Add new namespace wrappers; old imports remain primary-compatible. |
| Dual support | future minor | New docs recommend target namespace; old imports still supported. |
| Soft deprecation | after at least one minor release of dual support | Old imports may warn in developer-facing contexts. |
| Compatibility freeze | pre-v1 | Decide which old imports remain permanent shims. |
| Removal consideration | v1.0 or later | Remove only with migration guide, tests, changelog, and maintainer approval. |

## Deprecation Requirements

Before marking an old module path deprecated:

- new namespace exists;
- new namespace has tests;
- old import still works;
- migration guide exists;
- docs recommend the new path;
- package import tests cover old and new paths;
- no public demo or release gate depends only on the old path;
- rollback plan is documented.

## Warning Policy

- Do not warn during preview.
- Avoid warnings in normal user quickstart until migration is stable.
- If warnings are added, use clear action text.
- Warnings must not break tests unless tests explicitly opt in.
- Warnings must not appear during import smoke checks unless expected.

## Test Impact

Every module move requires:

- old import test;
- new import test;
- representative symbol equivalence test;
- contract path update if needed;
- docs example update;
- mypy package list update after target namespace becomes real;
- `pyproject.toml` package discovery update after target namespace becomes
  real.

## Risk

| Risk | Mitigation |
| --- | --- |
| Users depend on old imports | Keep wrappers until v1.0 or later. |
| Docs drift | Update docs and migration guide in the same round as implementation. |
| Import cycles | Move one group at a time and run package import tests. |
| Type-check drift | Update mypy package list only after packages exist. |
| Package discovery misses new namespace | Add package discovery tests before release. |
| Rollback becomes difficult | Keep wrappers thin and move implementation in small groups. |

## Rollback Plan

1. Stop recommending the new namespace in docs.
2. Keep or restore old implementation path.
3. Remove or disable new wrappers for the affected group only.
4. Restore package discovery and mypy package list if changed.
5. Run package import, public import, name integrity, and group-specific tests.
6. Record rollback in the lane and changelog if release-facing.

## Non-removal Commitment

`turing_research_plus` remains the compatibility namespace through the v0.x
line. A future v1.0 plan may revisit removal, but removal is not automatic.
