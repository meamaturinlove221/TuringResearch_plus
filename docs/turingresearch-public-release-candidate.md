# TuringResearch Public Release Candidate

Round: 400R
Status: release candidate draft, not published
Version marker: `1.7.0rc0`

## Highlights

- Public project name is TuringResearch.
- PR #1 is excluded after NO-GO review.
- Upstream materials are framed as reference docs / workflow inspiration only.
- PR #2 community idea / skill intake is acceptable if kept docs-only.
- Open-source safety gate result is `PUBLIC_GO_AFTER_MANUAL_FIX`.
- GitHub repository rename manual pack is ready for human review.
- Fake/demo-first workflows remain the default.

## What Is TuringResearch?

TuringResearch is a local-first Research OS for keeping research evidence,
artifacts, routes, paper notes, dashboards, plugins, and release gates
reviewable.

It helps humans manage complex research state without pretending to automate
scientific judgment.

## Install / Quickstart

Recommended local editable install:

```powershell
python -m pip install -e .[dev]
python -m pytest tests/contract/test_v1_6_release_contracts.py tests/workflow/test_v1_6_full_replay.py -q
```

The package distribution and import compatibility names remain unchanged for
now. TuringResearch is the public project name.

## Community Idea / Skill Intake

Community intake is docs-only. Friends or collaborators may submit Markdown
idea or skill proposal documents after maintainers decide whether to include
PR #2 community docs in the final public branch.

Community intake must not modify:

- `src/`
- `tests/`
- CI
- release files
- package metadata
- README
- CHANGELOG
- VERSION

Implementation work must happen later in a separate maintainer/Codex branch.

## Upstream Reference / Inspiration

Upstream repositories may be referenced as:

- reference documentation;
- workflow inspiration;
- related projects;
- docs/tool-surface parity targets.

No upstream academic publication package has been found or migrated.

Do not describe README, SKILL.md, workflow docs, MCP tool docs, source code,
examples, or showcase material as academic publications.

## Safety Boundary

Default mode:

- fake/local;
- no automatic remote execution;
- no default live network;
- no default SSH/SFTP;
- no automatic evidence promotion;
- no raw data packaging;
- no secrets;
- no unsupported VGGT or SparseConv3D success claim.

## Known Limitations

- No GitHub Release is created automatically.
- No tag is created automatically.
- No PyPI publication is performed.
- No GitHub Pages deployment is performed.
- No split repository is created automatically.
- No migrated academic publication is claimed.
- No fake benchmark is claimed.
- ARIS is not implemented.

## Roadmap

Near-term public launch work:

1. decide whether to include PR #2 community intake docs;
2. complete manual GitHub repository rename review;
3. complete final public visibility review;
4. rerun safety/name/privacy gates after final branch selection;
5. decide separately on GitHub Release, tag, PyPI, Pages, and split repos.

## Release Boundary

This is a release candidate document only. It does not publish a release.
