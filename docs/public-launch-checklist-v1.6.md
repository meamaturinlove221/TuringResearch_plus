# Public Launch Checklist v1.6

Status: ready for maintainer review.

Round: 385.

This checklist prepares TuringResearch for a public launch decision. It does
not publish a release, create a tag, deploy docs, publish to PyPI, create split
repositories, or run live providers.

## Input Notes

- `README.md` reviewed as the public TuringResearch front door.
- `docs/turingresearch-public-naming-policy.md` reviewed for public naming.
- `docs/open-source-preflight-gate-report.md` was requested by the release
  procedure but is not present in this branch. The current checklist therefore
  uses `docs/open-source-hygiene-gate-report.md`, `docs/v1.6.0-final-archive.md`,
  and `docs/v1.6.0-what-is-ready.md` as available evidence.

## Required Checklist

| Item | Status | Evidence / next action |
| --- | --- | --- |
| README reviewed | ready for human review | `README.md`, `docs/readme-launch-checklist-v1.6.md` |
| docs bundle reviewed | ready for human review | `docs/v1.6.0-docs-deployment-gate-report.md`, `docs/docs-release-bundle.md` |
| split manual packs reviewed | ready for final human review | `split_manual/`, `docs/split-final-safety-refresh-v1.6.md` |
| release artifact reviewed | pending maintainer review | docs bundle exists; no PyPI or GitHub release artifact has been published |
| security/privacy pass | pass with review | `docs/open-source-hygiene-gate-report.md`, `docs/v1.6.0-final-archive.md` |
| no secrets | pass with final scan required | hygiene and privacy gates report no committed secrets |
| no fake URL | pass with final scan required | no public docs URL or split-repo URL is claimed |
| no raw data | pass with final scan required | public launch surfaces are docs/demo/checklist only |
| tag decision | pending maintainer decision | no tag created in this round |
| GitHub release decision | pending maintainer decision | no GitHub release created in this round |
| PyPI decision | pending maintainer decision | no PyPI publication in this round |
| split repo creation decision | pending maintainer decision | no child repository created in this round |

## Final Pre-launch Review

Before a human public launch, review:

- README first screen and safety boundary;
- docs release bundle contents;
- screenshot/demo asset placeholders;
- split manual packs and URL placeholder policy;
- package metadata and installation instructions;
- license, citation, contributing, conduct, and security files;
- final secret/private-path/raw-data scan output;
- release notes and GitHub release draft;
- tag naming and branch source;
- PyPI/package-name decision.

## Explicit Non-actions

- No automatic release.
- No tag.
- No GitHub release publication.
- No PyPI publication.
- No GitHub Pages deployment.
- No split repository creation.
- No live provider execution.
- No remote execution.
- No private data upload.

## Decision Shape

This checklist supports a future maintainer go/no-go meeting. It is not itself
launch approval.
