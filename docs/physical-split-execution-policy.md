# Physical Split Execution Policy

Status: policy locked.

Round: 337.

v1.5 enters physical split execution preparation, but it still does not create
GitHub repositories, push external remotes, publish releases, or write real
URLs for repositories that do not exist.

The flagship TuringResearch repository remains the source of truth. Split
bundles under `split_ready/` are manual execution packs for future human
review.

## Current Candidate Bundles

| Bundle | Role | Execution status |
| --- | --- | --- |
| `split_ready/turingresearch-vggt-case` | public-safe dogfooding case mirror | ready after human approval |
| `split_ready/turingresearch-examples` | public demo and template mirror | ready after human approval |
| `split_ready/turingresearch-plugins` | plugin policy/registry draft mirror | deferred until ecosystem demand |

## Execution Policy

1. The main repository remains the flagship.
2. Split bundles are optional spokes, not replacements for the flagship.
3. Every child README must link or point back to the flagship above the fold.
4. A placeholder may say the flagship URL will be inserted after human approval.
5. No nonexistent real URL may be written.
6. No GitHub repository may be created automatically.
7. No external child repository may be pushed automatically.
8. No private data, secrets, raw data, restricted model payloads, or unsupported
   claims may enter a child bundle.
9. Child bundles must pass safety review before any human creates a repository.
10. Any future external push requires explicit human confirmation.

## Manual Execution Shape

A future human split should follow this shape:

1. Choose one bundle.
2. Review the exact file tree.
3. Run split safety and privacy checks.
4. Confirm README flagship backlink wording.
5. Confirm no real URL is written before the repo exists.
6. Create the external repository manually if approved.
7. Push only the reviewed public-safe bundle.
8. Insert the real URL only after the repository exists.
9. Record the action in the flagship ledger.

## Flagship Protection

The main repository keeps:

- install and quickstart;
- package metadata and public API;
- docs, dashboards, release notes, and security gates;
- original repo production parity narrative;
- issue triage and roadmap;
- release tags and package publication.

Spokes may host public-safe case or example material, but they must not become
the canonical install path.
