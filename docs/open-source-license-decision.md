# Open Source License Decision

Round: 360.4
Status: decision draft; human approval required

## Current State

TuringResearch is preparing public-facing repository files, but the current
repository license remains proprietary:

```toml
license = { text = "Proprietary" }
```

The root `LICENSE` file and `pyproject.toml` intentionally remain consistent.
This round does not choose an open source license, publish a release, publish to
PyPI, create a tag, or grant redistribution rights.

## Recommendation

Before any public open source release, maintainers should make an explicit
license decision and review it with appropriate human/legal guidance.

Possible future choices include:

- keep proprietary for private review only;
- choose a permissive open source license;
- choose a copyleft open source license;
- use a dual-license model;
- split public demo material and core package under different license terms.

This document does not recommend a legal outcome. It records the decision that
no open source license is approved yet.

## Required If License Changes

- Update `LICENSE`.
- Update `pyproject.toml`.
- Update `README.md`.
- Update `docs/license-review.md`.
- Update `docs/open-source-license-decision.md`.
- Update release notes and public release checklists.
- Re-run public name integrity, privacy/security gates, source hygiene, and
  dependency/license review.
- Confirm examples, split packs, generated assets, and citation metadata are
  distributable under the selected terms.

## Non-actions

- No legal advice.
- No upstream license text copied.
- No open source license selected.
- No license approval claimed.
- No PyPI publication.
- No GitHub release publication.
- No tag creation.
