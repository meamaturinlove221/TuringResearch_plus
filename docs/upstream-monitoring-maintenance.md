# Upstream Monitoring Maintenance

Status: planning policy.

Round: 150.

Upstream monitoring is allowed only in explicit upstream-scan rounds. Default
maintenance rounds must not use network access.

## Upstream Scan Cadence

| Trigger | Expected action |
| --- | --- |
| Planned upstream-scan round | Run approved public-source scans, record snapshots, and update watch reports. |
| Dependency or provider change suspected | Plan an upstream-scan round before modifying implementation. |
| Release candidate preparation | Review existing upstream reports; run new scans only if the round explicitly permits it. |
| Security concern | Follow security policy; do not paste sensitive findings into public issues. |

## Source Hygiene

Every upstream scan must record:

- source URL or repository;
- access date;
- source license or terms status when visible;
- what was read;
- what was not copied;
- whether the source is public, authorized, or blocked;
- whether implementation is allowed, documentation-only, or disallowed.

## What Upstream Monitoring Must Not Do

- No private repository access without explicit authorization.
- No copying upstream code into the repo without license review.
- No scraping paywalled or restricted content.
- No storing credentials, cookies, tokens, or private headers.
- No turning public demos into claims about upstream performance.

## Watch Areas

- MCP and local install tooling changes.
- Optional PDF/PPTX backend compatibility.
- Plugin sandboxing approaches and platform constraints.
- Public plugin registry and marketplace practices.
- Scholarly API terms and rate-limit changes.
- Dataset/model license changes relevant to public case studies.
- Browser/local server security guidance for local dashboard work.

## Snapshot Policy

- Keep upstream snapshots as summaries, not copied bodies of source material.
- Record uncertainty and blocked items.
- Do not treat upstream mentions as evidence for project experiment results.
- Do not promote upstream ideas to feature work until source hygiene passes.

## Release Interaction

Release candidates should cite the latest relevant upstream monitoring status
only as planning context. If a release depends on current external behavior, an
explicit upstream-scan round is required before release approval.
