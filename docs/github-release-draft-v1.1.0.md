# GitHub Release Draft - v1.1.0

Status: draft only.

Round: 229.

Do not publish this draft automatically. Do not create a tag, GitHub release,
PyPI package, or child repository from this file without maintainer approval.

## Title

TuringResearch Plus v1.1.0rc0 - Post-v1 stabilization, docs/dashboard, and demo
expansion

## Summary

v1.1.0rc0 strengthens the v1.0 local-first Research OS baseline with
split-ready bundles, a local docs site builder, a read-only local dashboard,
Dashboard Data API, paper writing beta, more public demo cases, a case study
gallery, and GitHub Actions hardening.

## Highlights

- Post-v1.0 stabilization and public entry cleanup.
- Split-ready case/examples bundles for human repository creation review.
- Local-first docs site skeleton and builder.
- Read-only localhost dashboard and Dashboard Data API.
- Review-only paper writing beta.
- More public demo cases and Case Study Gallery.
- CI/CD plan and GitHub Actions hardening.
- Full v1.1 regression gate passed.

## Quickstart

Use the main repository:

```bash
python -m pip install -e .[dev]
python -m pytest tests/workflow/test_v1_1_full_fake_replay.py -q
```

For the public demo path, start with:

- `docs/v1.0.0-quickstart.md`
- `examples/public_demo/WALKTHROUGH.md`
- `docs/public-showcase.md`

## Limitations

- No SaaS.
- Split repos still require manual creation.
- Local server is localhost-only and read-only.
- Paper writing beta requires human review.
- No automatic experiment execution.
- Live tests are skipped by default.
- CI does not publish releases automatically.
- No automatic GitHub release or PyPI publish.

## Safety Note

All public demo and paper beta outputs are fake/demo or review-only. They must
not be treated as observed experiment evidence. Do not claim VGGT or SparseConv3D
success without evidence.

## Next Roadmap

- Human review of v1.1 release notes and README.
- Optional manual creation of split repositories after approval.
- Further docs/dashboard polish.
- Paper writing beta hardening.
- More public-safe demo cases.
