# TulingResearch Plus Codex Multi-Agent Workflow

TulingResearch Plus uses one Codex window and one repository. Parallel work is represented by lane files, contracts, and skills inside the same project context.

## Lane Rules

- Every lane has a file under `lanes/`.
- Every lane writes a summary entry to `lanes/00_master_ledger.md`.
- Contract changes are recorded before model or implementation changes.
- Race Mode cannot produce implementation work until Source Hygiene Gate passes.
- Paper Draft work is blocked when `ExperimentReport` is absent.

## Skill Rules

- Local skill names must start with `tulingresearch-`.
- Skills support coordination only; they do not create a second repository or second Codex window.

## Subtask Runtime

TulingResearch Plus uses `TaskProfile` and `SubtaskRunner` to simulate multi-agent roles inside the single Codex window.

Execution modes:

- `manual_codex_role`: render a role prompt for the current Codex context to follow manually.
- `llm_client`: reserved for a future adapter; Round 5B raises a typed unsupported-path error instead of calling an LLM.
- `dry_run`: deterministic test mode that returns fake artifacts.

`TaskProfile` records:

- `name`
- `role`
- `goal`
- `input_schema`
- `output_schema`
- `allowed_tools`
- `reasoning_style`
- `quality_gate`

The runtime must not invoke external LLMs, Claude-specific agent tools, or network services.

## Review Rules

- Network behavior is mocked in tests.
- STDIO MCP logging goes to stderr or structured sinks, never stdout.
- Dry-run and fake-service paths are treated as first-class workflow modes.
