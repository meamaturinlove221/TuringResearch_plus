# GitHub Release Draft - v1.5.0

Status: draft only.

Round: 358.

Do not publish this draft automatically. Do not create a tag, GitHub release,
PyPI package, public docs deployment, or child repository from this file without
maintainer approval.

## Title

TuringResearch Plus v1.5.0rc0 - Public externalization release candidate

## Summary

v1.5.0rc0 prepares TuringResearch Plus for public externalization. It adds docs
deployment dry-run artifacts, split repo manual packs, optional live polish, a
unified live safety gate, and static dashboard showcase pages.

ARIS remains intentionally deferred and reference-only.

## Highlights

- Docs deployment dry-run.
- Docs navigation polish.
- Split repo manual packs.
- Optional live Scholar/Web/SFTP polish.
- Live safety gate.
- Dashboard landing page.
- Parity showcase view.
- Interview demo view.

## Quickstart

Use the main repository:

```bash
python -m pip install -e .[dev]
python -m pytest tests/workflow/test_v1_5_full_replay.py -q
```

For the v1.5 public externalization overview, start with:

- `docs/v1.5.0-full-replay-report.md`
- `docs/v1.5.0-feature-list.md`
- `examples/public_demo/dashboard_showcase/landing.html`

## Docs Site Dry-run

v1.5 includes a local docs-site deployment dry-run, not a public deployment.

- Dry-run output: `docs-site/dist/`
- Manifest: `docs-site/dist_manifest.yaml`
- Report: `docs-site/deployment_dry_run_report.md`
- Gate: `docs/v1.5.0-docs-sprint-gate-report.md`

The manifest records `deployment_performed: false` and `public_url: none`.

## Original Repo Parity

v1.5 keeps the v1.4 original repo production parity baseline intact:

- Session production parity.
- Scholar production parity.
- Web production parity.
- yogsoth production parity.
- Full v1.4 production replay.

Entry points:

- `docs/v1.4.0-full-production-replay-report.md`
- `docs/original-repo-production-parity-summary.md`
- `docs/original-repo-parity-dashboard-v2.md`

## Dashboard Showcase

Static/local-first dashboard showcase pages:

- `examples/public_demo/dashboard_showcase/landing.html`
- `examples/public_demo/dashboard_showcase/parity.html`
- `examples/public_demo/dashboard_showcase/interview.html`

These pages use no JavaScript, no external assets, no analytics, and no live
provider calls.

## Split Manual Packs

Manual child-repo packs are prepared for human review:

- `split_manual/turingresearch-vggt-case/`
- `split_manual/turingresearch-examples/`

No repository is created automatically. No external push is performed. No real
child-repo URL is written.

## Optional Live Policy

Scholar, Web/Apify, and SFTP live polish remains optional and disabled by
default:

- live tests are skipped by default;
- env opt-in is explicit;
- no API key or token is committed;
- no SSH/SFTP connection is opened by default;
- no remote command is executed;
- live output is review context, not observed evidence.

Entry point:

- `docs/v1.5.0-optional-live-sprint-gate-report.md`

## Limitations

- No automatic public deployment.
- No real public URL.
- No automatic child repository creation.
- No automatic external push.
- No default live network.
- No live SSH/SFTP by default.
- No remote command execution.
- No automatic experiment execution.
- No ARIS implementation.
- No automatic GitHub release or PyPI publish.

## ARIS Still Deferred

ARIS remains future-study only. v1.5 does not implement:

- ARIS runtime;
- cross-model review;
- proof-checker;
- meta-optimize;
- paper-claim-audit;
- automated research loop.

See `docs/v1.5.0-aris-still-deferred.md`.

## Safety Note

All v1.5 public demo surfaces are fake/demo, dry-run, manual-pack, or
review-only. They must not be treated as observed evidence. Human review remains
required before release-facing claims, live provider use, live SSH/SFTP use,
child repository creation, public deployment, or publication.

## Next Roadmap

- Human review of v1.5 release notes and docs-site dry-run package.
- Manual decision on public docs deployment.
- Manual decision on split repository creation.
- Continued live opt-in review in private environments.
- Future ARIS study only after a separate scope lock.
