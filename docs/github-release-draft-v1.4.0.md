# GitHub Release Draft - v1.4.0

Status: draft only.

Round: 327.

Do not publish this draft automatically. Do not create a tag, GitHub release,
PyPI package, or child repository from this file without maintainer approval.

## Title

TuringResearch Plus v1.4.0rc0 - Original repo production parity

## Summary

v1.4.0rc0 focuses on original repo production parity. It turns the v1.3
fake/default original parity work into production-style operator paths for
Session, Scholar, Web, and yogsoth-inspired research workflows.

ARIS remains intentionally deferred and reference-only.

## Highlights

- Session production parity.
- Session CLI surface.
- Shell script equivalent export.
- Cross-platform archive hardening.
- Remote dry-run plan.
- Return import human confirmation.
- Scholar production parity.
- Paper content/reference/reading E2E.
- Web production parity.
- URL normalization/cache/content fixtures.
- Apify fake/live report.
- yogsoth production parity.
- Campaign/catalog/vault/ontology/stress/convergence/experiment E2E.
- Parity dashboard v2.

## Quickstart

Use the main repository:

```bash
python -m pip install -e .[dev]
python -m pytest tests/workflow/test_v1_4_full_production_replay.py -q
```

For the v1.4 production parity overview, start with:

- `docs/original-repo-production-parity-summary.md`
- `docs/original-repo-parity-dashboard-v2.md`
- `docs/v1.4.0-full-production-replay-report.md`

## Limitations

- ARIS features are deferred.
- No automatic remote execution.
- No live SSH/SFTP by default.
- No automatic experiment execution.
- No default live network.
- No final paper automation.
- No automatic GitHub release or PyPI publish.

## Safety Note

All v1.4 public demo surfaces are fake/demo or review-only. They must not be
treated as observed evidence. Human review remains required before release-facing
claims, live provider use, live SSH/SFTP use, or publication.

## Next Roadmap

- Human review of v1.4 release notes and README.
- Optional live provider review in a dedicated live-test round.
- Separately scoped ARIS study after safety review.
- Continued public docs and demo polish.
