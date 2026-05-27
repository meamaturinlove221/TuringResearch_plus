<p align="center">
  <img src="./assets/turingresearch_mascot.svg" width="260" alt="TuringResearch mascot" />
</p>

<h1 align="center">TuringResearch</h1>

<p align="center">
  <b>A local-first research operating system for AI-assisted scientific iteration.</b>
</p>

<p align="center">
  Turn messy research goals into evidence ledgers, method cards, experiment routes, artifact audits, and advisor-ready reports.
</p>

<p align="center">
  <a href="#why-turingresearch">Why</a> ·
  <a href="#what-it-does">Features</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#safety-boundaries">Safety</a> ·
  <a href="./README_CN.md">中文</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue" />
  <img alt="MCP first" src="https://img.shields.io/badge/MCP-first-7C3AED" />
  <img alt="Local first" src="https://img.shields.io/badge/local--first-by%20default-16A34A" />
  <img alt="Dry run" src="https://img.shields.io/badge/dry--run-safe%20by%20default-F59E0B" />
  <img alt="Status" src="https://img.shields.io/badge/status-public%20RC-0EA5E9" />
</p>

---

## Why TuringResearch

Most AI tools can summarize a paper or draft a plan.

Real research is harder:

- advisor goals change;
- experiments produce incomplete evidence;
- artifact bundles get huge and messy;
- “planned”, “observed”, and “fake demo” results get mixed together;
- long-running Codex sessions drift away from the original objective;
- reports need to be honest enough for a mentor, not just polished enough for a README.

**TuringResearch is built for that gap.**

It helps organize the research loop:

```text
intent → literature → gap → hypothesis → route → experiment → artifact → report → next sprint
```

---

## What it does

TuringResearch focuses on research workflow infrastructure:

| Capability | What it helps with |
|---|---|
| Research intake | Convert fuzzy goals into constraints, non-goals, blockers, and next actions. |
| Evidence ledger | Separate observed facts, planned work, fake fixtures, missing papers, and missing experiments. |
| Literature workflow | Prepare survey plans, method cards, reference maps, and related-work positioning. |
| Hypothesis planning | Turn gaps into testable hypotheses and route trees. |
| Experiment runbooks | Compile Codex-ready long-horizon plans with hard gates and fallback branches. |
| Artifact audit | Track bundles, logs, boards, reports, hashes, missing files, and unsupported claims. |
| Advisor pack | Produce mentor-facing summaries, architecture diagrams, boundaries, and next-step plans. |
| Community intake | Accept idea documents and skill proposals without letting unreviewed code into the project. |

---

## Architecture

<svg width="1600" height="980" viewBox="0 0 1600 980" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1600" y2="980" gradientUnits="userSpaceOnUse">
      <stop stop-color="#FFF8FC"/>
      <stop offset="0.45" stop-color="#F7F8FF"/>
      <stop offset="1" stop-color="#F2FBFF"/>
    </linearGradient>

    <linearGradient id="pink" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#FFB7D5"/>
      <stop offset="1" stop-color="#FFCFE6"/>
    </linearGradient>

    <linearGradient id="blue" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#B8D9FF"/>
      <stop offset="1" stop-color="#D8E9FF"/>
    </linearGradient>

    <linearGradient id="mint" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#BDF4E4"/>
      <stop offset="1" stop-color="#D8FFF4"/>
    </linearGradient>

    <linearGradient id="violet" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#D7C8FF"/>
      <stop offset="1" stop-color="#EFE7FF"/>
    </linearGradient>

    <linearGradient id="yellow" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#FFE8A8"/>
      <stop offset="1" stop-color="#FFF4CD"/>
    </linearGradient>

    <filter id="shadow" x="-30%" y="-30%" width="160%" height="180%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#C9D4EA" flood-opacity="0.35"/>
    </filter>

    <style>
      .title { font: 700 42px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #2F3654; }
      .subtitle { font: 500 18px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #66708F; }
      .section { font: 700 20px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #33405F; }
      .label { font: 600 17px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #36435F; }
      .small { font: 500 14px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #5F6B88; }
      .tiny { font: 500 12px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #72809E; }
      .pill { font: 700 13px "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; fill: #4B5575; }
      .white { fill: white; }
      .stroke { stroke: #DCE4F4; stroke-width: 2; }
      .arrow { stroke: #9FB2D9; stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
      .dash { stroke: #B9C8E8; stroke-width: 2.2; stroke-linecap: round; stroke-dasharray: 9 8; fill: none; }
    </style>

    <marker id="arrowHead" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M1 1L10 6L1 11" fill="none" stroke="#9FB2D9" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>

  <rect width="1600" height="980" rx="30" fill="url(#bg)"/>

  <!-- Header -->
  <rect x="56" y="40" width="1488" height="120" rx="28" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="86" y="92" class="title">TuringResearch</text>
  <text x="86" y="126" class="subtitle">AI-assisted research operating system · literature → evidence → experiment → advisor pack</text>

  <rect x="1198" y="63" width="124" height="34" rx="17" fill="#FDE3EF"/>
  <text x="1224" y="85" class="pill">MCP-first</text>

  <rect x="1336" y="63" width="90" height="34" rx="17" fill="#E6F1FF"/>
  <text x="1358" y="85" class="pill">Fake-safe</text>

  <rect x="1435" y="63" width="81" height="34" rx="17" fill="#E6FBF4"/>
  <text x="1455" y="85" class="pill">Docs</text>

  <text x="86" y="150" class="tiny">For real research projects: papers, experiment bundles, advisor feedback, path-linked local repos, and reproducible planning.</text>

  <!-- Left inputs -->
  <text x="86" y="214" class="section">Inputs</text>

  <rect x="70" y="236" width="250" height="84" rx="22" fill="url(#pink)" class="stroke" filter="url(#shadow)"/>
  <text x="96" y="272" class="label">Research Intent</text>
  <text x="96" y="298" class="small">topic · north star · constraints</text>

  <rect x="70" y="338" width="250" height="84" rx="22" fill="url(#blue)" class="stroke" filter="url(#shadow)"/>
  <text x="96" y="374" class="label">Advisor Feedback</text>
  <text x="96" y="400" class="small">goals · blockers · non-goals</text>

  <rect x="70" y="440" width="250" height="84" rx="22" fill="url(#mint)" class="stroke" filter="url(#shadow)"/>
  <text x="96" y="476" class="label">Papers / PDFs / Notes</text>
  <text x="96" y="502" class="small">PDF → Markdown · figures · tables</text>

  <rect x="70" y="542" width="250" height="84" rx="22" fill="url(#violet)" class="stroke" filter="url(#shadow)"/>
  <text x="96" y="578" class="label">Artifact Bundles</text>
  <text x="96" y="604" class="small">zip · npz · json · boards · logs</text>

  <rect x="70" y="644" width="250" height="84" rx="22" fill="url(#yellow)" class="stroke" filter="url(#shadow)"/>
  <text x="96" y="680" class="label">Local Project Paths</text>
  <text x="96" y="706" class="small">co-location mode · dry-run scan</text>

  <!-- Core -->
  <text x="388" y="214" class="section">Core pipeline</text>

  <rect x="360" y="236" width="332" height="118" rx="26" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="388" y="274" class="label">1. Intake &amp; Source Hygiene</text>
  <text x="388" y="300" class="small">normalize inputs · preserve manifests · verify provenance</text>
  <text x="388" y="324" class="tiny">planned / observed / fake-data / requires-real-source / requires-real-experiment</text>

  <rect x="360" y="382" width="332" height="118" rx="26" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="388" y="420" class="label">2. Paper / PDF Understanding</text>
  <text x="388" y="446" class="small">method cards · figure/table extraction · architecture mapping</text>
  <text x="388" y="470" class="tiny">README-safe outputs and Codex-friendly markdown</text>

  <rect x="360" y="528" width="332" height="118" rx="26" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="388" y="566" class="label">3. Evidence Ledger</text>
  <text x="388" y="592" class="small">claims · risks · blockers · experiment status</text>
  <text x="388" y="616" class="tiny">honest classification, no fake promotion</text>

  <rect x="360" y="674" width="332" height="118" rx="26" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="388" y="712" class="label">4. Experiment Route Compiler</text>
  <text x="388" y="738" class="small">hypothesis tree · route DSL · Codex prompt compile</text>
  <text x="388" y="762" class="tiny">hard gates · fallback · release-safe planning</text>

  <!-- Right side -->
  <text x="760" y="214" class="section">Evaluation &amp; delivery</text>

  <rect x="732" y="266" width="346" height="122" rx="26" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="760" y="304" class="label">5. Artifact Auditor</text>
  <text x="760" y="330" class="small">bundle audit · manifest check · path scan · thin bundle</text>
  <text x="760" y="354" class="tiny">zip / npz / board / json / runtime / cleanup</text>

  <rect x="732" y="430" width="346" height="122" rx="26" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="760" y="468" class="label">6. Visual Evidence Auditor</text>
  <text x="760" y="494" class="small">figure inventory · board typing · advisor-readiness hints</text>
  <text x="760" y="518" class="tiny">point cloud / depth proxy / mask / close-up / chart</text>

  <rect x="732" y="594" width="346" height="122" rx="26" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="760" y="632" class="label">7. Advisor Pack Builder</text>
  <text x="760" y="658" class="small">summary · roadmap · failure analysis · next action</text>
  <text x="760" y="682" class="tiny">for mentor review, not for inflated success claims</text>

  <!-- Outputs -->
  <text x="1146" y="214" class="section">Outputs</text>

  <rect x="1118" y="236" width="398" height="106" rx="24" fill="#FFFFFF" class="stroke" filter="url(#shadow)"/>
  <text x="1146" y="272" class="label">Structured Docs</text>
  <text x="1146" y="298" class="small">research brief · method plan · sprint plan · release docs</text>

  <rect x="1118" y="360" width="398" height="106" rx="24" fill="#FFFFFF" class="stroke" filter="url(#shadow)"/>
  <text x="1146" y="396" class="label">Skills / MCP / Contracts</text>
  <text x="1146" y="422" class="small">reusable skills · schemas · tests · fake-mode workflows</text>

  <rect x="1118" y="484" width="398" height="106" rx="24" fill="#FFFFFF" class="stroke" filter="url(#shadow)"/>
  <text x="1146" y="520" class="label">Architecture &amp; Figures</text>
  <text x="1146" y="546" class="small">mermaid · svg · diagram assets · README visuals</text>

  <rect x="1118" y="608" width="398" height="106" rx="24" fill="#FFFFFF" class="stroke" filter="url(#shadow)"/>
  <text x="1146" y="644" class="label">Research Operations</text>
  <text x="1146" y="670" class="small">evidence-led planning for VGGT / SMPL-X and future projects</text>

  <!-- Footer panel -->
  <rect x="70" y="826" width="1446" height="106" rx="24" fill="white" class="stroke" filter="url(#shadow)"/>
  <text x="100" y="865" class="label">Current emphasis</text>
  <text x="100" y="892" class="small">Stabilize core reproduction first, then extend with research-facing features. Keep cross-machine sync, NAS/SMB, SSH/SFTP, and cloud artifact adapters as future work.</text>

  <!-- Arrows from inputs to core -->
  <path d="M320 278H346" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M320 380H346" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M320 482H346" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M320 584H346" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M320 686H346" class="arrow" marker-end="url(#arrowHead)"/>

  <!-- Vertical core arrows -->
  <path d="M526 354V370" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M526 500V516" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M526 646V662" class="arrow" marker-end="url(#arrowHead)"/>

  <!-- Core to right -->
  <path d="M692 733C725 733 707 327 732 327" class="dash"/>
  <path d="M692 587H718C724 587 728 577 732 552" class="dash"/>
  <path d="M692 441H718C724 441 728 452 732 470" class="dash"/>
  <path d="M692 295H718C724 295 728 306 732 327" class="dash"/>

  <!-- Right vertical -->
  <path d="M905 388V414" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M905 552V578" class="arrow" marker-end="url(#arrowHead)"/>

  <!-- To outputs -->
  <path d="M1078 327H1104" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M1078 491H1104" class="arrow" marker-end="url(#arrowHead)"/>
  <path d="M1078 655H1104" class="arrow" marker-end="url(#arrowHead)"/>

  <!-- Decorative cute stars -->
  <g opacity="0.65">
    <circle cx="1468" cy="130" r="4" fill="#FFC6DE"/>
    <circle cx="1488" cy="144" r="3" fill="#BFD8FF"/>
    <circle cx="1510" cy="126" r="4" fill="#C8F2E4"/>
    <circle cx="121" cy="79" r="4" fill="#FFDCA8"/>
    <circle cx="144" cy="94" r="3" fill="#CDBEFF"/>
  </g>
</svg>

The repository is intentionally **docs-first, evidence-first, and contract-first**.

---

## What is implemented vs planned

TuringResearch is a public release candidate. The README is conservative by design.

| Status | Meaning |
|---|---|
| Implemented | Code/docs/tests exist in this repo. |
| Partial | Working skeleton or workflow exists, but not full production scope. |
| Planned | Described as a roadmap item only. |
| Reference | Inspired by external/public projects; not claimed as TuringResearch output. |

No section in this README should imply that a planned module has already produced verified scientific results.

---

## Repository layout

```text
TuringResearch/
├─ assets/                     # mascot and visual assets
├─ community/                  # idea and skill proposal intake
├─ docs/                       # manuals, policies, release docs, route reports
├─ examples/                   # public-safe examples and fake-mode demos
├─ lanes/                      # round-by-round ledgers and decision records
├─ src/                        # Python packages
│  ├─ turing_research/
│  └─ turing_research_plus/
├─ tests/                      # contract and workflow tests
├─ README.md
└─ README_CN.md
```

Historical package names may still exist for compatibility during the rename period.

---

## Quickstart

```bash
git clone https://github.com/meamaturinlove221/TuringResearch_plus.git
cd TuringResearch_plus
python -m pip install -e .[dev]
python -m pytest
```

Optional local MCP smoke check:

```bash
python -m tuling_research.mcp_server --manifest
```

Default workflows should be safe to run without live API keys.

---

## Example workflows

Typical workflows this project is designed to support:

1. **Paper route planning** — turn a paper set into method cards, gap analysis, and experiment ideas.
2. **Long-horizon Codex planning** — compile route trees and hard gates into prompts that do not return too early.
3. **Artifact review** — inspect output bundles and decide whether claims are supported.
4. **Advisor report generation** — prepare clear reports with scope, evidence, failure modes, and next steps.
5. **Community idea intake** — let trusted collaborators submit idea/skill documents without changing code.

---

## Safety boundaries

TuringResearch should not:

- fake benchmark results;
- claim paper conclusions without sources;
- call live APIs by default;
- publish private paths, tokens, `.env`, cookies, or logs;
- redistribute restricted data or model assets;
- present reference-project ideas as untracked original output;
- mark planning-only workflows as production-ready.

The project prefers a boring but honest `planned` label over an impressive but false `done` label.

---

## Reference projects

Some public projects inspired parts of this repository’s workflow design and documentation style. They should be treated as **reference / inspiration**, not as silently migrated academic publications or hidden implementation sources.

When a reference project influences a module, the documentation should say so plainly and avoid overclaiming.

---

## Roadmap

Near-term directions:

- stronger artifact audit reports;
- better evidence ledger workflows;
- figure/table extraction planning;
- richer advisor-pack generation;
- cleaner modular repo presentation;
- friend/community skill proposal intake;
- optional live adapters behind explicit gates.

Deferred:

- ARIS-like homepage generation;
- automatic public release automation;
- automatic remote execution by default;
- unverified upstream “academic output” migration.

---

## Contributing

For implementation work, use maintainer-reviewed branches.

For idea and skill proposals, use the community intake flow:

```text
community/ideas/<github-username>/<idea-title>.md
community/skills/<github-username>/<skill-name>.md
```

Accepted proposals can later become feature capsules, skills, SOPs, campaign entries, or roadmap tasks.

---

## License

Check `LICENSE` before reuse. If the license file is not present in your local checkout, treat the project as not yet formally licensed for redistribution.

---

<p align="center">
  <b>TuringResearch makes research iteration clearer, more auditable, and less likely to drift.</b>
</p>
