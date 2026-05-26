# Quickstart

Status: v1 public entry guide.

For the maintained v1 public-safe path, use
[`v1.0.0-quickstart.md`](v1.0.0-quickstart.md). This page remains the short
front-door version.

## Install

```powershell
python -m pip install -e .[dev]
```

## Run Local Checks

```powershell
python -m pytest -q
python -m mypy src
```

Default tests are fake/demo and local-first. They do not require real API keys,
live network access, Modal, remote machines, private project folders, or live
research data.

## Try The Public Demo

Open these files locally:

- `examples/public_demo/README.md`
- `examples/public_demo/QUICKSTART.md`
- `examples/public_demo/WALKTHROUGH.md`
- `examples/public_demo/dashboard/index.html`
- `examples/public_demo/projects/vggt_like_demo/dashboard.html`
- `examples/public_demo/projects/paper_survey_demo/dashboard.html`
- `examples/public_demo/projects/software_tooling_demo/dashboard.html`

No server is required.

The demo is explicitly demo-only. It does not run real experiments or turn fake
material into observed evidence.

## Optional MCP Smoke Check

```powershell
python -m pip install -e .[dev,mcp]
python -m turing_research.mcp_server --manifest
turingresearch-plus-mcp --health-check
```

MCP live features and plugin tools remain opt-in. Default config keeps fake mode
enabled and live/plugin tools disabled.

## What Not To Expect

- No automatic experiment execution.
- No automatic final paper generation.
- No default live networking.
- No unknown plugin execution.
- No publication approval.

Human review is required before making claims or releases.
