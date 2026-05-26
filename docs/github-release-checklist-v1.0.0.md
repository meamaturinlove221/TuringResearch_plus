# GitHub Release Checklist: v1.0.0

Status: checklist only.

Round: 196.

This checklist must be completed manually before any GitHub release is created.

## Before Tagging

- [ ] Confirm full pytest passed.
- [ ] Confirm `python -m mypy src` passed.
- [ ] Confirm name integrity passed.
- [ ] Confirm privacy/security gates passed.
- [ ] Confirm public demo and quickstart pass.
- [ ] Confirm version is correct in `VERSION`, `pyproject.toml`, and package
      `__version__` values.
- [ ] Confirm release notes and changelog are reviewed.
- [ ] Confirm README does not claim automatic research, automatic final paper
      writing, or VGGT experiment success.
- [ ] Confirm no private data, raw data, restricted model payloads, or real
      credentials are included.
- [ ] Confirm split repositories are not described as published unless they
      actually exist.

## Release Draft Review

- [ ] Title is accurate.
- [ ] Summary is honest.
- [ ] Highlights match implemented/reviewed surfaces.
- [ ] Quickstart points to local fake/demo workflow.
- [ ] Demo link points to local public demo material.
- [ ] Safety note is visible.
- [ ] Known issues are not hidden.
- [ ] Next roadmap does not promise unapproved work.

## Do Not Do Automatically

- [ ] Do not create a tag automatically.
- [ ] Do not create a GitHub release automatically.
- [ ] Do not publish to PyPI automatically.
- [ ] Do not push external child repositories automatically.
