# Public Launch Human Actions v1.6

Status: pending maintainer action.

Round: 385.

These actions must be performed manually if the maintainer decides to launch
TuringResearch publicly.

## Review Actions

1. Review `README.md` as the public project entry point.
2. Review `docs-site/release_bundle/` locally.
3. Review `assets/screenshots/SCREENSHOT_MANIFEST.yaml` and capture only real
   screenshots if needed.
4. Review split manual packs under `split_manual/`.
5. Review optional live docs and confirm live remains disabled by default.
6. Review license, citation, contributing, conduct, and security files.
7. Rerun final privacy/security/name checks on the exact launch commit.

## Release Decisions

| Decision | Current state | Human action |
| --- | --- | --- |
| tag | undecided | choose whether to create a v1.6 tag |
| GitHub release | undecided | approve or defer a release draft |
| PyPI | undecided | approve package publication or defer |
| GitHub Pages | undecided | manually enable only after docs bundle review |
| split repositories | undecided | create only after manual safety review |
| live smoke | deferred/private | run only with explicit private env and redaction |

## Manual Safety Confirmation

Before any public action, confirm:

- no secrets;
- no API keys;
- no `.env`;
- no raw data;
- no private paths;
- no restricted model payloads;
- no fake GitHub, Pages, or split-repo URL;
- no fake benchmark, fake users, or fake stars;
- no automatic research-completion claim;
- no automatic final-paper claim;
- ARIS remains deferred;
- live networking remains opt-in and disabled by default.

## Commands Are Intentionally Omitted

This document does not provide one-shot release commands. The maintainer should
make tag, GitHub release, PyPI, Pages, and split-repo decisions deliberately
from the reviewed launch commit.
