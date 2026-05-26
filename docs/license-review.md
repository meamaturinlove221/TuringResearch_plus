# License Review

Status: current license is proprietary.

## Current Status

`LICENSE` and `pyproject.toml` currently state a proprietary license. Public
release preparation must not imply open-source rights unless the license is
changed deliberately after human approval.

## Required If License Changes

- Update `LICENSE`.
- Update `pyproject.toml`.
- Update this document.
- Update `NOTICE.md`.
- Re-run source hygiene review for third-party references.
- Review public examples for redistributable content.

## Source Reuse Boundary

TuringResearch can reference public ideas and workflow patterns, but must not
copy incompatible-license implementation code, private source material, leaked
roadmaps, NDA content, private papers, or restricted datasets.

## Open Source Decision Boundary

The public project name is TuringResearch, but the license has not been changed
to an open source license. See `docs/open-source-license-decision.md` for the
human-review decision record and `docs/open-source-compliance-checklist.md` for
the release checklist.
