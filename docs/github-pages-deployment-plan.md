# GitHub Pages Deployment Plan

Status: plan only.

Round: 332.

This plan describes how TuringResearch could become GitHub Pages-ready during
v1.5. It does not deploy a site, create a GitHub Pages setting, push a branch,
write a live URL, or enable GitHub Actions.

## Intended Use

GitHub Pages is the recommended first public hosting route because it is close
to the repository, easy for reviewers to reason about, and does not require a
separate provider account for the basic path.

## Prepared Inputs

- `docs-site/site_manifest.yaml`
- `docs-site/nav.yaml`
- `docs-site/pages/*.md`
- source docs referenced by nav entries
- fake/demo public examples
- local static build output after human review

## Manual Deployment Shape

A future human deployment would likely follow this shape:

1. Run the local docs-site build.
2. Review generated HTML and CSS.
3. Run public-safety scans.
4. Choose a GitHub Pages source mode.
5. Commit only reviewed static output or a reviewed build workflow.
6. Enable Pages manually in repository settings.
7. Record the generated URL only after GitHub provides it.

No step in v1.5 performs those actions automatically.

## Required Checks Before Manual Enablement

- docs-site build passes locally;
- nav entries resolve;
- no private files are referenced;
- no generated page includes secrets, raw data, private paths, or restricted
  model payloads;
- no fake/demo result is described as observed evidence;
- no unsupported experiment success claim appears;
- ARIS is still described as deferred;
- analytics and tracking are absent;
- generated output is reviewed by a human.

## GitHub Pages Options

| Option | Notes | v1.5 stance |
| --- | --- | --- |
| Commit generated output | simple and reviewable, but adds generated files | allowed as future manual option |
| Build from source with Actions | cleaner source tree, more CI surface | future option, not automatic |
| Separate docs branch | isolates static output | future option, not automatic |

## Non-goals

- No automatic Pages enablement.
- No workflow secrets.
- No real URL written in docs.
- No analytics.
- No custom domain.
- No private file upload.
- No automatic release publication.

## Recommendation

Prepare for GitHub Pages, but keep the actual enablement as a human action
after v1.5 safety and release review.
