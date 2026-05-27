# GitHub Repo Rename Manual Pack

Round: 399R
Status: manual pack, not executed

## Goal

Prepare the human steps for renaming the GitHub repository to:

```text
TuringResearch
```

This document does not rename the repository, change repository visibility,
publish a release, create tags, deploy Pages, publish to PyPI, or merge PRs.

## Preconditions

Required before manual rename:

- PR #1 is closed or explicitly not merged.
- PR #2 is merged or explicitly approved as docs-only community intake.
- Open-source safety gate has passed with no content blocker.
- No misleading Academic Showcase wording is used as a launch claim.
- Upstream materials are framed only as Reference / Inspiration / Related
  Projects.

Current branch status:

- `integration/public-launch-prep` is the prepared integration branch.
- PR #1 showcase files are absent from this branch.
- Open-source safety gate result is `PUBLIC_GO_AFTER_MANUAL_FIX`.

## Manual Rename Steps

1. Open GitHub repository settings.
2. Confirm the current repository is the intended TuringResearch repository.
3. Confirm no release/tag/Pages/PyPI action is being performed in the same step.
4. Rename the repository to:

```text
TuringResearch
```

5. Save the GitHub rename.
6. Confirm GitHub redirects from the old URL if needed.
7. Update local remotes manually:

```powershell
git remote set-url origin https://github.com/<owner>/TuringResearch.git
```

8. Run the post-rename link check plan.
9. Re-run name integrity and open-source safety gates.

## Do Not Do During Rename

- Do not merge PR #1.
- Do not revive `examples/original-author-showcase/`.
- Do not make academic publication migration claims.
- Do not create fake GitHub Pages URLs.
- Do not create fake split repo URLs.
- Do not publish a GitHub Release.
- Do not publish to PyPI.
- Do not create split repositories automatically.

## Rollback / Recovery Notes

If the rename creates broken links or unexpected CI failures:

1. Do not rush release publication.
2. Keep repository visibility unchanged until links are reviewed.
3. Update local remotes.
4. Fix docs references in a normal PR.
5. Rerun safety/name/docs gates before launch.
