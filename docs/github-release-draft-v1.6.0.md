# GitHub Release Draft - v1.6.0

Status: draft only.

Round: 387.

Do not publish this draft automatically. Do not create a tag, GitHub release,
PyPI package, public docs deployment, or child repository from this file without
maintainer approval.

## Title

TuringResearch v1.6.0rc0 - Public release execution pack

## Summary

v1.6.0rc0 prepares TuringResearch for human-reviewed public release execution.
It adds docs deployment readiness, a GitHub Pages dry-run workflow draft, split
repository creation packs, optional live smoke policy, live output redaction,
packaging/release artifact readiness, dashboard/demo assets, and a public launch
checklist.

ARIS remains intentionally deferred and reference-only.

## Highlights

- Docs deployment ready.
- GitHub Pages workflow draft.
- Split repo creation packs.
- Optional live smoke.
- Live output redaction gate.
- Packaging readiness.
- Release artifact build.
- Dashboard / demo asset pack.
- Public launch checklist.

## Quickstart

Use the main repository:

```bash
python -m pip install -e .[dev]
python -m pytest tests/contract/test_v1_6_release_contracts.py tests/workflow/test_v1_6_full_replay.py -q
```

For the v1.6 public release execution overview, start with:

- `README.md`
- `docs/v1.6.0-full-regression-report.md`
- `docs/v1.6.0-feature-list.md`
- `docs/public-launch-checklist-v1.6.md`
- `examples/public_demo/dashboard_showcase/landing.html`

## Docs Deployment Ready

v1.6 includes a local docs release bundle and a GitHub Pages-ready dry-run
workflow draft. It is not a public deployment.

- Bundle: `docs-site/release_bundle/`
- Manifest: `docs-site/release_bundle_manifest.yaml`
- Report: `docs-site/release_bundle_report.md`
- Gate: `docs/v1.6.0-docs-deployment-gate-report.md`

The release path must not claim a public URL until a real human deployment
exists.

## Original Repo Parity

v1.6 keeps the v1.4 original repo production parity baseline intact:

- Session production parity.
- Scholar production parity.
- Web production parity.
- yogsoth production parity.
- Full v1.4 production replay.

Entry points:

- `docs/original-repo-replication-progress-report.md`
- `docs/original-repo-production-parity-summary.md`
- `docs/original-repo-parity-dashboard-v2.md`

## Dashboard / Demo Assets

Static/local-first dashboard showcase pages:

- `examples/public_demo/dashboard_showcase/landing.html`
- `examples/public_demo/dashboard_showcase/parity.html`
- `examples/public_demo/dashboard_showcase/interview.html`

Screenshot/demo assets are manifest/checklist driven:

- `assets/screenshots/SCREENSHOT_MANIFEST.yaml`
- `assets/screenshots/SCREENSHOT_TODO.md`
- `assets/demo_gif/DEMO_GIF_SCRIPT.md`

No fake screenshot is included.

## Split Repository Creation Packs

Manual child-repo packs are prepared for human review:

- `split_manual/turingresearch-vggt-case/`
- `split_manual/turingresearch-examples/`

No repository is created automatically. No external push is performed. No real
child-repo URL is written.

## Optional Live Policy

Scholar, Web/Apify, and SFTP live smoke remains optional and disabled by
default:

- live tests are skipped by default;
- env opt-in is explicit;
- no API key or token is committed;
- no SSH/SFTP connection is opened by default;
- no remote command is executed;
- live output is review context, not observed evidence;
- live output must pass redaction before report publication.

Entry points:

- `docs/optional-live-safety-gate.md`
- `docs/live-output-redaction-gate.md`

## Packaging And Release Artifacts

v1.6 is ready for local package/install review and release-artifact review. It
does not publish to PyPI and does not rename the package distribution.

Compatibility surfaces remain:

- package distribution: `turingresearch-plus`;
- Python namespace: `turing_research_plus`;
- MCP compatibility commands.

## Limitations

- No automatic public deployment.
- No real public URL.
- No automatic child repository creation.
- No automatic external push.
- No default live network.
- No live SSH/SFTP by default.
- No remote command execution.
- No automatic experiment execution.
- No GitHub release publication.
- No PyPI publication.
- No ARIS implementation.

## ARIS Still Deferred

ARIS remains future-study only. v1.6 does not implement:

- ARIS runtime;
- cross-model review;
- proof-checker;
- meta-optimize;
- paper-claim-audit;
- automated research loop.

See `docs/v1.6.0-aris-still-deferred.md`.

## Safety Note

All v1.6 public demo surfaces are fake/demo, dry-run, manual-pack,
placeholder-manifest, or review-only. They must not be treated as observed
evidence. Human review remains required before release-facing claims, live
provider use, live SSH/SFTP use, child repository creation, public deployment,
package upload, or publication.
