# TuringResearch Plus

Local-first Research OS for evidence-led research work.

TuringResearch Plus helps researchers manage complex research state without
pretending to automate research judgment. It keeps evidence, artifacts, route
plans, paper notes, dashboards, advisor packs, plugin manifests, privacy checks,
and replay gates in one local workflow.

It is a flagship monorepo, fake/demo-first by default, and built for human
review. Live adapters are optional and disabled by default. It is not a hosted
SaaS product, not an autonomous scientist, not a final-paper generator, and not
proof that any VGGT experiment succeeded.

It is not proof that any VGGT experiment succeeded and does not claim VGGT or
SparseConv3D experiment success.

Start here:

- [v1.0 Public Quickstart](docs/v1.0.0-quickstart.md)
- [Public Demo Walkthrough](docs/v1.0.0-public-demo-walkthrough.md)
- [Docs Home](docs/README.md)
- [v1.1 Scope](docs/v1.1.0-final-scope.md)
- [v1.4 Original Repo Production Parity Summary](docs/original-repo-production-parity-summary.md)
- [Original Repo Parity Dashboard v2](docs/original-repo-parity-dashboard-v2.md)
- [v1.3 Original Reference Parity Summary](docs/original-reference-parity-summary.md)
- [Reference Parity Dashboard](docs/reference-parity-dashboard.md)
- [Future Split Repositories](docs/future-split-repos.md)
- [Split Manual Packs](docs/split-manual-packs.md)

## Architecture

The system is organized around a review-first loop:

```text
Research intent
  -> Workspace
  -> Evidence Ledger
  -> Artifact Audit
  -> Route DSL / Hard Gates
  -> Paper Intelligence
  -> Advisor Pack
  -> Static Dashboard
  -> Privacy / Quality / Replay Gates
```

Full Mermaid planning diagrams live in:

- `docs/architecture-diagram-final.mmd`
- `docs/research-os-flow.mmd`
- `docs/vggt-case-flow.mmd`
- `docs/plugin-system-flow.mmd`

These are architecture and launch-planning assets, not generated research
results.

## Visual Tour

Use the architecture diagrams and dashboard demo as a lightweight visual tour of
the Research OS flow. Screenshots and demo GIFs are planned assets; they should
not be treated as experiment evidence.

## Problem

Research projects often scatter across notebooks, papers, run logs, cloud
folders, dashboards, messages, and half-remembered claims. The hard part is not
just generating more text. The hard part is keeping the project honest:

- what was planned;
- what was actually observed;
- what evidence exists;
- which artifacts are missing;
- which routes are blocked;
- which claims are unsafe;
- what still requires human review.

TuringResearch Plus makes those boundaries explicit.

## Core Capabilities

| Area | What it provides |
| --- | --- |
| Workspace | Multi-project registries, project templates, local overview state, and modular namespace facades. |
| Evidence | Evidence ledgers, planned/observed boundaries, claim status, and fake/live checks. |
| Artifact | Artifact audit, handoff metadata, remote artifact metadata, and export quality checks. |
| Route | Experiment Route DSL, hard gates, failure taxonomy, run/replay status, and next actions. |
| Paper | Paper digest, method cards, related-work positioning, deep review, and writing scaffolds. |
| Advisor | Markdown advisor packs plus optional PDF/PPTX export plans with quality gates. |
| Dashboard | Static local HTML/Markdown dashboards, public demo views, and search indexes. |
| Plugin | Manifest-first plugin registry, compatibility harness, MCP mapping, and sandbox policy. |
| Privacy | Privacy scans, redaction reports, compliance checklists, and public-demo safety gates. |
| Replay | Fake/default benchmark replay, quality regression gates, and release-candidate checks. |

## Quickstart

For the 5-10 minute public-safe path, start here:

- [`docs/v1.0.0-quickstart.md`](docs/v1.0.0-quickstart.md)
- [`examples/public_demo/QUICKSTART.md`](examples/public_demo/QUICKSTART.md)

Minimal local setup:

```powershell
python -m pip install -e .[dev]
python -m pytest tests/workflow/test_public_demo_suite.py tests/workflow/test_public_demo_expansion.py -q
python -m pytest tests/workflow/test_v1_public_quickstart_fake.py -q
```

Optional local MCP smoke check:

```powershell
python -m pip install -e .[dev,mcp]
python -m turing_research.mcp_server --manifest
turingresearch-plus-mcp --health-check
```

MCP server name: `turingresearch-plus`.

Console entry points:

- `turingresearch-plus`
- `turingresearch-plus-mcp`

Both call `turing_research.mcp_server:main`.

## Public Demo

The public demo suite is demo-only and does not require private data, API keys,
network access, VGGT data, or restricted model files:

- `examples/public_demo/`
- [`docs/v1.0.0-public-demo-walkthrough.md`](docs/v1.0.0-public-demo-walkthrough.md)
- `examples/public_demo/WALKTHROUGH.md`
- `examples/public_demo/EXPECTED_OUTPUTS.md`
- `examples/public_demo/demo_manifest.yaml`
- `examples/public_demo/dashboard/index.html`
- `examples/public_demo/projects/vggt_like_demo/`
- `examples/public_demo/projects/paper_survey_demo/`
- `examples/public_demo/projects/software_tooling_demo/`
- `examples/benchmarks/v1_public_demo_replay.yaml`

The demo shows:

- evidence ledger inspection;
- static dashboard viewing;
- advisor Markdown bundle review;
- related-work fake demo review;
- benchmark replay that checks expected files exist.

It does not run a real experiment, does not generate real research results, and
does not turn fake/demo material into observed evidence.

## v1.4 Original Repo Production Parity

v1.4 upgrades the original reference parity work from structural and
fake-runtime alignment into production parity for the stable reference surfaces.
Production parity means the fake/default path is runnable, documented,
dashboarded, and covered by gate tests. It does not mean live providers,
remote machines, autonomous agents, or experiments run by default.

| Area | v1.4 production status | Boundary |
| --- | --- | --- |
| Neocortica Session | production parity complete for fake/default local workflow | no default SSH/SFTP, no remote command execution, no automatic Evidence Ledger write |
| Neocortica Scholar | production parity complete for fake/default paper tooling | no MinerU, no OCR default, no paper download, no fake citation verified |
| Neocortica Web | production parity complete for fake/default Web tooling | no default network, no private scraping, no cookies, live Apify skipped by default |
| yogsoth-ai | production parity complete with review for deterministic research workflows | no autonomous agent runtime, no automatic experiment execution, no fake result observed |
| ARIS | still future reference only | no cross-model review, proof-checker, meta-optimize, or paper-claim-audit |

Start here:

- [`docs/original-repo-production-parity-summary.md`](docs/original-repo-production-parity-summary.md)
- [`docs/original-repo-parity-dashboard-v2.md`](docs/original-repo-parity-dashboard-v2.md)
- [`docs/v1.4.0-full-production-replay-report.md`](docs/v1.4.0-full-production-replay-report.md)
- [`docs/aris-still-deferred-v1.4.md`](docs/aris-still-deferred-v1.4.md)

The v1.4 replay remains fake/default and review-first. It is not a live
provider proof, remote execution proof, autonomous research runtime, or
experiment success claim.

## v1.3 Original Reference Parity

v1.3 focuses on original reference parity: making selected stable ideas from
Neocortica and yogsoth visible, testable, and locally replayable without
turning TuringResearch into an autonomous runtime.

| Area | v1.3 status | Boundary |
| --- | --- | --- |
| Neocortica Session parity | fake/default runtime replay works | no automatic remote execution |
| Neocortica Scholar parity | full fake/default tool surface works | no MinerU, no paper download, no paywall bypass |
| Neocortica Web parity | full fake/default tool surface works | no default network, no private scraping, no cookies |
| MCP / Skill parity | config and SOP surfaces are documented | no live MCP server is started by default |
| yogsoth parity | campaign trace, catalog dashboard, vault, ontology, stress, and convergence surfaces work | no agent runtime or automatic tool execution |
| ARIS | deferred and reference-only | no cross-model review, proof-checker, meta-optimize, or paper-claim audit |

Start here:

- [`docs/original-reference-parity-summary.md`](docs/original-reference-parity-summary.md)
- [`docs/reference-parity-dashboard.md`](docs/reference-parity-dashboard.md)
- [`docs/aris-still-deferred-v1.3.md`](docs/aris-still-deferred-v1.3.md)
- [`examples/public_demo/v1_3_original_parity_demo/README.md`](examples/public_demo/v1_3_original_parity_demo/README.md)

The v1.3 replay is fake/default. It does not prove live provider behavior,
remote execution behavior, or experiment success.

## VGGT Case Study

The VGGT material is a public-safe dogfooding case, not a claim of final
scientific success.

Start here:

- [`docs/vggt-case-study-public.md`](docs/vggt-case-study-public.md)
- `examples/vggt-human-prior-survey/public_case_study/case_study_draft.md`
- `examples/vggt-human-prior-survey/public_case_study/redaction_report.md`
- `examples/vggt-human-prior-survey/public_case_study/claim_safety_report.md`

The case study shows how TuringResearch Plus helped organize:

- north star and problem background;
- route changes;
- evidence management;
- failures and blockers;
- advisor pack material;
- public redaction and claim safety.

It does not claim VGGT experiment success or SparseConv3D success.

## Fake / Live Boundary

Default tests use fake services, local fixtures, and dry-run workflows. They do
not require real API keys, provider credentials, live network access, Modal,
remote machines, or private project folders.

They do not require real API keys or live network access.

Live adapters are optional and disabled by default:

```text
TURINGRESEARCH_MODE=fake
TURINGRESEARCH_ENABLE_LIVE_TESTS=0
TURINGRESEARCH_ENABLE_PLUGINS=0
TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE=0
```

Live mode requires explicit opt-in in private local configuration. Do not commit
real credentials.

## Privacy-first

Public material is designed to exclude:

- private local paths;
- raw data;
- private model payloads;
- API keys or tokens;
- confidential review notes;
- unsupported experiment claims.

Source Hygiene blocks unsafe or unauthorized source material.

Compliance and privacy reports are review aids. They are not legal approval.

## Plugin Safety

Plugin support is manifest-first and disabled-by-default:

- plugin manifest required;
- compatibility report required;
- sandbox policy required;
- extension safety report required;
- unknown third-party plugins disabled by default;
- no `execute_code` by default;
- no secrets access;
- live/network permission requires explicit opt-in;
- plugin tools remain disabled by default in the MCP example config.

The plugin system describes and reviews plugin metadata. It does not execute
unknown third-party code by default.

## Public API And Packages

v1.0 keeps `turing_research_plus` as the compatibility namespace and recommends
domain facade namespaces for new imports:

- `turing_research_core`
- `turing_research_paper`
- `turing_research_artifact`
- `turing_research_experiment`
- `turing_research_dashboard`
- `turing_research_plugins`
- `turing_research_cases`

See:

- [`docs/v1.0.0-public-api.md`](docs/v1.0.0-public-api.md)
- [`docs/v1.0.0-import-guide.md`](docs/v1.0.0-import-guide.md)
- [`docs/v1.0.0-api-stability-matrix.md`](docs/v1.0.0-api-stability-matrix.md)

## Documentation

- [Docs Home](docs/README.md)
- [v1.0 Public Quickstart](docs/v1.0.0-quickstart.md)
- [Install Guide](docs/install.md)
- [Examples](docs/examples.md)
- [Public Demo Guide](docs/public-demo-guide.md)
- [Public Positioning](docs/public-positioning.md)
- [Plugin Guide](docs/plugin-guide.md)
- [Advisor Export Guide](docs/advisor-export-guide.md)
- [Dashboard Guide](docs/dashboard-guide.md)
- [Limitations](docs/limitations.md)

## Roadmap

Near-term v1.1 stabilization focuses on:

- v1.0 baseline stabilization;
- split-ready finalization for public-safe case/examples bundles;
- public docs site planning;
- local server dashboard scope;
- paper writing beta scope;
- more public demo cases;
- CI/CD release hardening;
- maintaining the main repository as the flagship entry point.

Longer term, optional satellite repositories may be created for public-safe case
studies and examples. For v1.5 these remain planned / manual-ready spokes with
local export bundles under `split_ready/` and human execution packs under
`split_manual/`; they are not published GitHub repositories and they are not
install targets. Core runtime, install path, public API, release gates, and star
focus remain centered in the flagship repository. See
[Future Split Repositories](docs/future-split-repos.md),
[Split-ready Bundles](docs/split-ready-bundles.md), and
[Split Manual Packs](docs/split-manual-packs.md).

## Planned / Manual-ready Split Repositories

Planned Split Repositories remain manual-ready only.

The following split repositories are planned or manual-ready, but not
published:

- `turingresearch-vggt-case`: public-safe VGGT dogfooding case bundle.
- `turingresearch-examples`: public demo and project-template bundle.
- `turingresearch-plugins`: deferred plugin policy/registry draft bundle.

No real GitHub URLs are listed until a maintainer manually creates and approves
the repositories. The local `split_ready/` directory contains export-ready
bundles, and `split_manual/` contains human-only creation packs, git-init
dry-run notes, and release checklists. Neither directory is a published
repository. The main TuringResearch repository remains the only install,
quickstart, public API, release, and star entry.

See:

- [`docs/future-split-repos.md`](docs/future-split-repos.md)
- [`docs/split-ready-bundles.md`](docs/split-ready-bundles.md)
- [`docs/split-manual-packs.md`](docs/split-manual-packs.md)
- [`docs/main-repo-post-split-patch-v2.md`](docs/main-repo-post-split-patch-v2.md)
- [`docs/v1.1.0-split-repo-sync-policy.md`](docs/v1.1.0-split-repo-sync-policy.md)
- [`split_ready/split_manifest.yaml`](split_ready/split_manifest.yaml)

## Limitations

TuringResearch Plus does not:

- automatically complete research;
- automatically run real experiments;
- automatically write final paper conclusions;
- replace human review;
- provide legal advice;
- default to live networking;
- upload private data by default;
- execute unknown third-party plugins by default;
- guarantee star growth;
- claim VGGT or SparseConv3D experiment success without evidence.

## Development Checks

```powershell
python -m pytest -q
python -m mypy src
python -m pytest tests/contract/test_name_integrity.py -q
python -m pytest tests/workflow/test_v1_public_quickstart_fake.py -q
python -m pytest tests/workflow/test_v1_demo_refresh.py tests/workflow/test_v1_benchmark_replay.py -q
```

## Status

Current prepared package metadata is `1.3.0rc0`. The v1.4 production parity
docs and replay reports are release-candidate preparation material, not a
published release, live provider proof, remote execution proof, or experiment
success claim.
