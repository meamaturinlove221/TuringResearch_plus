# GitHub Release Final Checklist v1.6.0

Status: maintainer checklist.

Round: 388.

This checklist is for final human review before any GitHub release action. It
does not create a tag, publish a release, upload artifacts, deploy docs, publish
to PyPI, or create split repositories.

## Required Review

| Item | Status | Evidence |
| --- | --- | --- |
| release draft reviewed | pending maintainer review | `docs/github-release-draft-v1.6.0.md` |
| release notes reviewed | pending maintainer review | `docs/v1.6.0-release-notes.md` |
| feature list reviewed | pending maintainer review | `docs/v1.6.0-feature-list.md` |
| known limitations reviewed | pending maintainer review | `docs/v1.6.0-known-limitations.md` |
| test summary reviewed | pending maintainer review | `docs/v1.6.0-test-summary.md` |
| README reviewed | pending maintainer review | `README.md` |
| docs bundle reviewed | pending maintainer review | `docs-site/release_bundle/` |
| split packs reviewed | pending maintainer review | `split_manual/` |
| security/privacy reviewed | pending maintainer review | `docs/open-source-hygiene-gate-report.md` |
| tag decision made | pending maintainer decision | no tag created by this checklist |
| GitHub release decision made | pending maintainer decision | no release published by this checklist |
| PyPI decision made | pending maintainer decision | no package upload by this checklist |
| split repo decision made | pending maintainer decision | no child repository created by this checklist |

## Must Remain True

- Public project name is TuringResearch.
- No fake GitHub, Pages, or split-repo URL is written.
- No secrets, API keys, cookies, or private credentials are present.
- No `.env` file is committed as release payload.
- No raw data or restricted model payload is included.
- No private local path appears in public release materials.
- Live providers remain disabled by default.
- Live output is not treated as observed evidence.
- ARIS remains deferred.

## Stop Conditions

Stop before release if:

- any secret or private path is found;
- a public URL is claimed before deployment exists;
- split repositories are described as already created before a human creates
  them;
- package publication is implied before PyPI approval;
- live smoke output is unredacted;
- fake/demo output is promoted to observed evidence;
- VGGT or SparseConv3D success is claimed without evidence-ledger proof.

## Final Human Decisions

The maintainer must explicitly decide:

- tag name and source commit;
- whether to publish GitHub release;
- whether to attach any artifacts;
- whether to deploy docs;
- whether to publish to PyPI;
- whether to create split repositories;
- whether any optional live smoke should run privately.
