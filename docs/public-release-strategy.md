# Public Release Strategy

Status: planning draft.

TuringResearch Plus can be prepared for a public release only if the published
surface is honest, demo-safe, and local-first. The public release should show
the workflow engine clearly without exposing private research data, proprietary
model payloads, credentials, or overclaimed research results.

## What To Publish

- Source code for local fake/default workflows.
- Contracts and schemas for implemented local surfaces.
- Public docs, user guide, developer guide, and architecture overview.
- Public demo suite with fake/demo-only data.
- Example workspaces that do not contain private data.
- Static dashboard examples and Markdown advisor/export bundles.
- Plugin and MCP plugin manifests as disabled/review-gated examples.
- Benchmark replay scenarios for public demo outputs.

## What Not To Publish

- Private project links.
- `.env` files or credential-bearing configs.
- API keys, tokens, provider secrets, or personal credentials.
- Raw research data.
- SMPL-X body model payloads or licensed/private model files.
- Private advisor feedback.
- Real VGGT local paths.
- Unreviewed third-party plugin code execution.
- Final paper claims generated from scaffolds.

## Demo-safe Data Policy

- Every public demo file must be marked demo-only or obviously fake.
- Demo evidence may illustrate status transitions but must not be marked as
  real observed experiment evidence.
- Demo artifacts must be small text/metadata examples.
- Demo medical or human-subject examples must be synthetic and non-identifying.
- Public examples must pass privacy and release hygiene checks.

## License Review

- Maintainers must choose the public license posture before release.
- Current proprietary or restricted license language should not be presented as
  open-source licensing.
- Third-party dependency licenses should be reviewed before public
  distribution.
- Model/data licenses are not covered by the code license and need separate
  review.

## README Positioning

The README should say plainly:

- local, MCP-first, review-first research workflow engine;
- default workflows are fake/demo and local;
- live adapters are optional and disabled by default;
- plugins are manifest-only unless explicitly enabled by reviewed policy;
- TuringResearch does not run experiments or write final paper conclusions by
  itself.

## Installation Path

Recommended public path:

```powershell
python -m pip install -e .[dev]
python -m pytest -q
python -m mypy src
```

Optional MCP smoke path:

```powershell
python -m pip install -e .[dev,mcp]
python -m turing_research.mcp_server --manifest
turingresearch-plus-mcp --health-check
```

## Contribution Policy

- Require issue templates for bug reports, feature requests, and research
  workflow requests.
- Require pull requests to state whether they touch live adapters, private data,
  plugin execution, public examples, or release docs.
- Require tests for new public surfaces.
- Require privacy and secret-scan review for examples.

## Issue Templates

Public issue templates should guide users away from posting:

- secrets;
- private dataset paths;
- private advisor comments;
- raw data samples;
- licensed model payloads;
- logs with credentials.

## Security Policy

- Security reports should not be filed as public issues when they contain
  sensitive details.
- The project should document supported versions once public releases exist.
- Reports involving secrets, unsafe plugin behavior, data leaks, or dependency
  supply chain risks should be triaged as security-sensitive.

## Roadmap Honesty

- Label planned, experimental, optional-live, and future work clearly.
- Do not present fake/demo replay as real benchmark success.
- Do not present paper scaffolds as final paper writing.
- Do not present privacy scanning as legal compliance.
- Do not present plugin manifests as safe runtime execution.

## Public Release Gate

Before publishing:

1. Clean branch review.
2. Full tests and mypy pass.
3. Privacy gate and quality regression gate pass.
4. Public demo suite passes.
5. No old project naming appears.
6. No secrets, raw data, private paths, or model payloads are present.
7. License posture is approved.
8. README and release notes are reviewed by a maintainer.
