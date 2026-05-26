"""Static parity showcase view for original repo replication progress."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ParityShowcaseRow:
    """One upstream-to-TuringResearch parity row."""

    upstream: str
    capability: str
    our_equivalent: str
    status: str
    tests: tuple[str, ...]
    docs: tuple[str, ...]
    safety_enhancement: str
    deferred_items: tuple[str, ...]


@dataclass(frozen=True)
class ParityShowcasePage:
    """Data needed to render the parity showcase page."""

    title: str
    subtitle: str
    status: str
    rows: tuple[ParityShowcaseRow, ...]
    safety_summary: tuple[str, ...]


def build_parity_showcase_page() -> ParityShowcasePage:
    """Build the default v1.5 parity showcase page model."""

    return ParityShowcasePage(
        title="Original Repo Parity Showcase",
        subtitle=(
            "A static comparison of upstream capabilities, TuringResearch "
            "equivalents, tests, docs, safety enhancements, and deferred items."
        ),
        status="static-local-first-demo",
        rows=(
            ParityShowcaseRow(
                upstream="Neocortica-Session",
                capability="Git context, context packs, safe transfer planning, return review",
                our_equivalent=(
                    "Session CLI, context pack runtime, script export, archive "
                    "hardening, remote dry-run plan, return confirmation, E2E gate"
                ),
                status="production parity with live defaults disabled",
                tests=(
                    "tests/workflow/test_session_production_parity_gate.py",
                    "tests/workflow/test_session_production_parity_e2e.py",
                ),
                docs=(
                    "docs/session-production-parity-gate-report.md",
                    "docs/v1.4.0-session-parity-summary.md",
                ),
                safety_enhancement=(
                    "No remote command, no automatic Evidence Ledger write, "
                    "manual confirmation before import."
                ),
                deferred_items=(
                    "default live SSH/SFTP",
                    "remote command execution",
                    "automatic remote cleanup",
                ),
            ),
            ParityShowcaseRow(
                upstream="Neocortica-Scholar",
                capability="Paper search, content, reference, reading, README tool list",
                our_equivalent=(
                    "Scholar tool surface, paper content/reference E2E, "
                    "three-pass reading, optional heavy backend slot"
                ),
                status="production parity in fake/default mode",
                tests=(
                    "tests/workflow/test_scholar_production_parity_gate.py",
                    "tests/workflow/test_three_pass_reading_e2e_fake.py",
                ),
                docs=(
                    "docs/scholar-production-parity-gate-report.md",
                    "docs/v1.4.0-scholar-production-summary.md",
                ),
                safety_enhancement=(
                    "No paper download by default, no paywall bypass, no fake "
                    "citation marked verified."
                ),
                deferred_items=(
                    "MinerU implementation",
                    "OCR default",
                    "live provider proof",
                ),
            ),
            ParityShowcaseRow(
                upstream="Neocortica-Web",
                capability="Web fetching, content extraction, cache metadata, Apify optional",
                our_equivalent=(
                    "URL normalization, cache manifest, content fixtures, "
                    "Apify fake/live report, Web production gate"
                ),
                status="production parity in fake/default mode",
                tests=(
                    "tests/workflow/test_web_production_parity_gate.py",
                    "tests/workflow/test_web_content_extraction_fixtures.py",
                ),
                docs=(
                    "docs/web-production-parity-gate-report.md",
                    "docs/v1.4.0-scholar-web-production-summary.md",
                ),
                safety_enhancement=(
                    "No default network, no private scraping, no login bypass, "
                    "no cookie storage."
                ),
                deferred_items=(
                    "default live network",
                    "private scraping",
                    "live Apify proof",
                ),
            ),
            ParityShowcaseRow(
                upstream="yogsoth-ai",
                capability="Campaigns, catalog, vault, ontology, stress, convergence, runbooks",
                our_equivalent=(
                    "Campaign trace E2E, Research Catalog E2E, Vault Wiki E2E, "
                    "Ontology E2E, Stress/Convergence E2E, Experiment Runbook E2E"
                ),
                status="production parity with review boundary",
                tests=(
                    "tests/workflow/test_yogsoth_production_parity_gate.py",
                    "tests/workflow/test_stress_convergence_e2e.py",
                ),
                docs=(
                    "docs/yogsoth-production-parity-gate-report.md",
                    "docs/v1.4.0-yogsoth-production-summary.md",
                ),
                safety_enhancement=(
                    "No autonomous agent runtime, no automatic experiment execution, "
                    "no fake result observed."
                ),
                deferred_items=(
                    "autonomous agent runtime",
                    "automatic experiment execution",
                    "final paper automation",
                ),
            ),
            ParityShowcaseRow(
                upstream="ARIS",
                capability="Cross-model review, proof checking, meta optimization, claim audit",
                our_equivalent=(
                    "Deferred future-study references and explicit non-goal docs"
                ),
                status="deferred",
                tests=(
                    "tests/contract/test_v1_4_release_contracts.py",
                    "tests/workflow/test_v1_4_full_production_replay.py",
                ),
                docs=(
                    "docs/aris-still-deferred-v1.4.md",
                    "docs/v1.5.0-aris-still-deferred.md",
                ),
                safety_enhancement=(
                    "Kept out of default implementation because it would create "
                    "research-automation and claim-authority risk."
                ),
                deferred_items=(
                    "cross-model review",
                    "proof-checker",
                    "meta-optimize",
                    "paper-claim-audit",
                    "ARIS runtime",
                ),
            ),
        ),
        safety_summary=(
            "No default network access.",
            "No live provider call.",
            "No remote command execution.",
            "No automatic experiment execution.",
            "No automatic Evidence Ledger write.",
            "No fake/demo result promotion.",
            "ARIS remains deferred.",
        ),
    )


def render_parity_showcase_html(page: ParityShowcasePage | None = None) -> str:
    """Render a standalone static parity showcase page."""

    page = page or build_parity_showcase_page()
    rows = "\n".join(_render_row(row) for row in page.rows)
    safety = "\n".join(
        f"          <li>{html.escape(item)}</li>" for item in page.safety_summary
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page.title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #17202a;
      --muted: #5f6b7a;
      --line: #d7dde5;
      --accent: #006b5f;
      --warn: #8a5a00;
      --soft: #edf4f3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    header {{
      background: var(--panel);
      border-bottom: 1px solid var(--line);
      padding: 32px 28px 24px;
    }}
    .hero, main {{
      max-width: 1180px;
      margin: 0 auto;
    }}
    main {{ padding: 24px; }}
    .eyebrow {{
      color: var(--accent);
      font-weight: 700;
      margin: 0 0 8px;
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 2.2rem;
      line-height: 1.15;
    }}
    h2, h3 {{ margin: 0 0 10px; }}
    p, li {{ line-height: 1.55; }}
    .subtitle {{ color: var(--muted); max-width: 820px; }}
    .badge {{
      display: inline-block;
      border: 1px solid var(--line);
      border-left: 4px solid var(--accent);
      background: #fbfcfd;
      padding: 6px 10px;
      margin: 0 8px 8px 0;
      font-size: 0.92rem;
    }}
    .badge.warning {{ border-left-color: var(--warn); }}
    .matrix {{
      display: grid;
      gap: 14px;
    }}
    .row {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }}
    .row-grid {{
      display: grid;
      grid-template-columns: minmax(180px, 0.8fr) minmax(240px, 1.2fr) minmax(220px, 1fr);
      gap: 14px;
    }}
    .label {{
      color: var(--muted);
      font-size: 0.84rem;
      font-weight: 700;
      margin: 0 0 4px;
    }}
    .value {{ margin: 0 0 10px; }}
    .list {{ margin: 0 0 10px; padding-left: 18px; color: var(--muted); }}
    .safety {{
      margin-top: 18px;
      border: 1px solid var(--line);
      background: var(--soft);
      border-radius: 8px;
      padding: 16px;
    }}
    footer {{
      border-top: 1px solid var(--line);
      color: var(--muted);
      padding: 18px 28px;
    }}
    @media (max-width: 860px) {{
      .row-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <p class="eyebrow">Parity showcase</p>
      <h1>{html.escape(page.title)}</h1>
      <p class="subtitle">{html.escape(page.subtitle)}</p>
      <span class="badge">{html.escape(page.status)}</span>
      <span class="badge">upstream capability</span>
      <span class="badge">our equivalent</span>
      <span class="badge warning">ARIS deferred</span>
    </div>
  </header>
  <main>
    <section aria-labelledby="parity-matrix">
      <h2 id="parity-matrix">Replication Matrix</h2>
      <div class="matrix">
{rows}
      </div>
    </section>
    <section class="safety" aria-labelledby="safety-enhancements">
      <h2 id="safety-enhancements">Safety Enhancements</h2>
      <ul>
{safety}
      </ul>
    </section>
  </main>
  <footer>
    Static/local-first parity showcase. It does not run providers, remote
    commands, experiments, or claim verification.
  </footer>
</body>
</html>
"""


def write_parity_showcase(path: Path, page: ParityShowcasePage | None = None) -> Path:
    """Write the parity showcase HTML to a local path."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_parity_showcase_html(page), encoding="utf-8")
    return path


def _render_row(row: ParityShowcaseRow) -> str:
    tests = _render_list(row.tests)
    docs = _render_list(row.docs)
    deferred = _render_list(row.deferred_items)
    return f"""        <article class="row">
          <div class="row-grid">
            <div>
              <p class="label">upstream capability</p>
              <h3>{html.escape(row.upstream)}</h3>
              <p class="value">{html.escape(row.capability)}</p>
              <p class="label">status</p>
              <p class="value">{html.escape(row.status)}</p>
            </div>
            <div>
              <p class="label">our equivalent</p>
              <p class="value">{html.escape(row.our_equivalent)}</p>
              <p class="label">safety enhancement</p>
              <p class="value">{html.escape(row.safety_enhancement)}</p>
            </div>
            <div>
              <p class="label">tests</p>
              <ul class="list">
{tests}
              </ul>
              <p class="label">docs</p>
              <ul class="list">
{docs}
              </ul>
              <p class="label">deferred items</p>
              <ul class="list">
{deferred}
              </ul>
            </div>
          </div>
        </article>"""


def _render_list(items: tuple[str, ...]) -> str:
    return "\n".join(f"                <li>{html.escape(item)}</li>" for item in items)
