# GitHub Release Draft - TuringResearch Public v1.7 RC

Status: draft only, not published

## Highlights

- First public release-candidate package after PR #1 NO-GO.
- TuringResearch public naming finalized.
- Open-source safety gate completed with `PUBLIC_GO_AFTER_MANUAL_FIX`.
- GitHub repo rename manual pack prepared.
- Upstream materials reframed as Reference / Inspiration / Related Projects.
- Community idea / skill intake can be used if kept docs-only.

## Install

```powershell
python -m pip install -e .[dev]
```

## Quickstart

```powershell
python -m pytest tests/contract/test_v1_6_release_contracts.py tests/workflow/test_v1_6_full_replay.py -q
```

## What Is TuringResearch?

TuringResearch is a local-first Research OS for reviewable research evidence,
artifacts, workflows, dashboards, plugins, and release gates.

It is built for human review and does not claim to automate scientific judgment.

## Community Intake

Community idea / skill proposal intake is documentation-only. It is intended
for Markdown proposals that maintainers may later convert into feature capsules,
SOPs, campaigns, docs examples, or `.agents/skills/` proposals.

## Upstream Reference / Inspiration

Upstream repositories are used as reference docs and workflow inspiration only.

No upstream academic publication package has been found or migrated.

## Safety Notes

- No automatic remote execution.
- No default live network.
- No default SSH/SFTP.
- No fake benchmark.
- No migrated academic publication.
- No VGGT or SparseConv3D success claim.
- No ARIS implementation.

## Known Limitations

- GitHub Release is not published automatically.
- Git tag is not created automatically.
- PyPI is not published automatically.
- GitHub Pages is not deployed automatically.
- Split repositories are not created automatically.
- Optional live integrations remain disabled by default.

## Roadmap

Next human decisions:

1. final branch selection;
2. repository rename;
3. visibility change;
4. PR #2 community-doc inclusion;
5. GitHub Release / tag / PyPI / Pages decisions;
6. post-release monitoring.
