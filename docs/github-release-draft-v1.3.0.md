# GitHub Release Draft - v1.3.0

Status: draft only.

Round: 289.

Do not publish this draft automatically. Do not create a tag, GitHub release,
PyPI package, or child repository from this file without maintainer approval.

## Title

TuringResearch Plus v1.3.0rc0 - Full original reference parity

## Summary

v1.3.0rc0 focuses on full original-reference parity. It turns the v1.2
structural parity work into fake/default replayable surfaces for Session
runtime, Scholar/Web tools, MCP/Skill mapping, yogsoth-inspired catalog demos,
stress/convergence review, and public demo presentation.

ARIS remains intentionally deferred and reference-only.

## Highlights

- Full original reference parity scope.
- Session runtime parity with fake pod workflow replay.
- Context pack runtime.
- Optional SFTP transfer fake-first.
- Remote return verifier.
- Scholar full tool surface.
- Web full tool surface.
- MCP tool parity.
- Campaign execution trace.
- Research Catalog dashboard.
- Vault wiki demo.
- Ontology runbook demo.
- Stress scenario library.
- Convergence decision report.
- Original parity public demo.
- ARIS still deferred.

## Quickstart

Use the main repository:

```bash
python -m pip install -e .[dev]
python -m pytest tests/workflow/test_v1_3_full_original_parity_replay.py -q
```

For the v1.3 public demo path, start with:

- `examples/public_demo/v1_3_original_parity_demo/README.md`
- `docs/original-reference-parity-summary.md`
- `docs/reference-parity-dashboard.md`

## Limitations

- ARIS features are deferred.
- No automatic remote execution.
- No live SSH/SFTP by default.
- No automatic experiment execution.
- No default live network.
- No final paper automation.
- No automatic GitHub release or PyPI publish.

## Safety Note

All v1.3 public demo surfaces are fake/demo or review-only. They must not be
treated as observed evidence. Human review remains required before release-facing
claims, live provider use, live SSH/SFTP use, or publication.

## Next Roadmap

- Human review of v1.3 release notes and README.
- Optional live provider review in a dedicated live-test round.
- Separately scoped ARIS study after safety review.
- Continued public docs and demo polish.
