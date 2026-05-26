# GitHub Release Draft - v1.2.0

Status: draft only.

Round: 256.

Do not publish this draft automatically. Do not create a tag, GitHub release,
PyPI package, or child repository from this file without maintainer approval.

## Title

TuringResearch Plus v1.2.0rc0 - Original reference parity and Research Catalog

## Summary

v1.2.0rc0 focuses on original-reference parity. It aligns stable Session,
Scholar, Web, MCP, Skill SOP, campaign, vault, ontology, stress-test, and
experiment-runbook ideas with TuringResearch's local-first Research OS model.
ARIS remains intentionally deferred to v1.3+ study.

## Highlights

- Original reference parity strategy.
- Neocortica Session / Scholar / Web parity.
- MCP config and Skill SOP parity.
- yogsoth campaign, vault/wiki/edge audit, ontology, stress-test, and
  experiment execution parity.
- TuringResearch Research Catalog.
- Reference Parity Dashboard.
- v1.2 public demo refresh.
- v1.2 security/privacy gate and full regression.
- ARIS deferral roadmap.

## Quickstart

Use the main repository:

```bash
python -m pip install -e .[dev]
python -m pytest tests/workflow/test_v1_2_full_fake_replay.py -q
```

For the v1.2 public demo path, start with:

- `examples/public_demo/v1_2_demo/README.md`
- `docs/reference-parity-dashboard.md`
- `docs/turingresearch-research-catalog.md`

## Limitations

- ARIS features are deferred.
- No MinerU heavy fallback.
- No remote execution orchestration.
- No automatic experiment execution.
- No default live network.
- No final paper automation.
- No automatic GitHub release or PyPI publish.

## Safety Note

All v1.2 public demo surfaces are fake/demo or review-only. They must not be
treated as verified live research work. Human review remains required before
release-facing claims, live provider use, or publication.

## Next Roadmap

- Human review of v1.2 release notes and README.
- v1.3 ARIS study roadmap.
- Optional live provider review in a dedicated live-test round.
- Continued public docs and demo polish.
