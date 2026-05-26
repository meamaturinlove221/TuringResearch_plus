"""Static landing page renderer for the public dashboard showcase."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ShowcaseLandingSection:
    """A compact landing page section."""

    section_id: str
    title: str
    summary: str
    links: tuple[str, ...]


@dataclass(frozen=True)
class ShowcaseLandingPage:
    """Data needed to render the static showcase landing page."""

    title: str
    subtitle: str
    status: str
    sections: tuple[ShowcaseLandingSection, ...]
    safety_boundaries: tuple[str, ...]


def build_showcase_landing_page() -> ShowcaseLandingPage:
    """Build the default v1.5 dashboard showcase landing page model."""

    return ShowcaseLandingPage(
        title="TuringResearch Dashboard Showcase",
        subtitle=(
            "A static, local-first product view for original repo parity, "
            "public demos, split readiness, and review-safe research workflows."
        ),
        status="static-local-first-demo",
        sections=(
            ShowcaseLandingSection(
                section_id="project-pitch",
                title="Project Pitch",
                summary=(
                    "TuringResearch is a local-first Research OS for evidence-led "
                    "research workflows, public-safe demos, and human-reviewed "
                    "claim boundaries."
                ),
                links=("docs/public-showcase.md", "README.md"),
            ),
            ShowcaseLandingSection(
                section_id="quickstart",
                title="Quickstart",
                summary=(
                    "Start with fake/default workflows, inspect demo fixtures, "
                    "and run local tests without credentials or network access."
                ),
                links=("docs-site/pages/quickstart.md", "examples/public_demo/QUICKSTART.md"),
            ),
            ShowcaseLandingSection(
                section_id="original-parity-status",
                title="Original Parity Status",
                summary=(
                    "v1.4 reached production parity for stable original repo "
                    "surfaces while keeping unsafe live and ARIS features deferred."
                ),
                links=(
                    "docs/original-repo-parity-dashboard-v2.md",
                    "docs/v1.4.0-full-production-replay-report.md",
                ),
            ),
            ShowcaseLandingSection(
                section_id="public-demo",
                title="Public Demo",
                summary=(
                    "Demo-only fixtures show dashboard data, parity summaries, "
                    "paper/web examples, and review reports without private data."
                ),
                links=("examples/public_demo/", "docs/original-repo-replication-public-version.md"),
            ),
            ShowcaseLandingSection(
                section_id="docs-site",
                title="Docs Site",
                summary=(
                    "The docs site is build-hardened and deployment-ready as a "
                    "dry-run package, but no public deployment is performed here."
                ),
                links=("docs-site/", "docs/v1.5.0-docs-sprint-gate-report.md"),
            ),
            ShowcaseLandingSection(
                section_id="split-repo-readiness",
                title="Split Repo Readiness",
                summary=(
                    "Manual packs are prepared for case/demo child repos while "
                    "the main repository remains the flagship install and docs entry."
                ),
                links=("split_manual/", "docs/v1.5.0-split-sprint-gate-report.md"),
            ),
            ShowcaseLandingSection(
                section_id="safety-boundary",
                title="Safety Boundary",
                summary=(
                    "The showcase is read-only, fake/default, privacy-first, and "
                    "does not turn planned or demo outputs into observed evidence."
                ),
                links=("docs/v1.4.0-security-audit.md", "docs/optional-live-safety-gate.md"),
            ),
        ),
        safety_boundaries=(
            "No default network access.",
            "No live provider call.",
            "No SSH or SFTP connection.",
            "No remote command execution.",
            "No credentials or private paths.",
            "No raw data or restricted model payloads.",
            "No automatic Evidence Ledger write.",
            "No planned or demo output promoted to observed evidence.",
        ),
    )


def render_showcase_landing_html(page: ShowcaseLandingPage | None = None) -> str:
    """Render a standalone static HTML landing page."""

    page = page or build_showcase_landing_page()
    sections = "\n".join(_render_section(section) for section in page.sections)
    boundaries = "\n".join(
        f"          <li>{html.escape(item)}</li>" for item in page.safety_boundaries
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
      --accent-soft: #e8f3f1;
      --warn: #8a5a00;
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
    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 24px;
    }}
    .hero {{
      max-width: 1120px;
      margin: 0 auto;
    }}
    .eyebrow {{
      color: var(--accent);
      font-weight: 700;
      letter-spacing: 0;
      margin: 0 0 8px;
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 2.25rem;
      line-height: 1.12;
    }}
    h2, h3 {{ margin: 0 0 10px; }}
    p, li {{ line-height: 1.55; }}
    .subtitle {{
      max-width: 760px;
      color: var(--muted);
      font-size: 1.05rem;
    }}
    .badges {{ margin-top: 18px; }}
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
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }}
    .card p {{ color: var(--muted); }}
    .links {{
      margin: 12px 0 0;
      padding-left: 18px;
      color: var(--muted);
    }}
    .safety {{
      margin-top: 18px;
      border: 1px solid var(--line);
      background: var(--accent-soft);
      border-radius: 8px;
      padding: 16px;
    }}
    footer {{
      border-top: 1px solid var(--line);
      color: var(--muted);
      padding: 18px 28px;
    }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <p class="eyebrow">Static dashboard showcase</p>
      <h1>{html.escape(page.title)}</h1>
      <p class="subtitle">{html.escape(page.subtitle)}</p>
      <div class="badges" aria-label="showcase status">
        <span class="badge">{html.escape(page.status)}</span>
        <span class="badge">fake/default workflows</span>
        <span class="badge warning">human review required</span>
      </div>
    </div>
  </header>
  <main>
    <section aria-labelledby="showcase-sections">
      <h2 id="showcase-sections">Showcase Map</h2>
      <div class="grid">
{sections}
      </div>
    </section>
    <section class="safety" aria-labelledby="safety-boundary">
      <h2 id="safety-boundary">Safety Boundary</h2>
      <ul>
{boundaries}
      </ul>
    </section>
  </main>
  <footer>
    Static/local-first landing page. No analytics, no external assets, no live
    provider calls, and no public deployment is performed by this file.
  </footer>
</body>
</html>
"""


def write_showcase_landing(path: Path, page: ShowcaseLandingPage | None = None) -> Path:
    """Write the landing page HTML to a local path."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_showcase_landing_html(page), encoding="utf-8")
    return path


def _render_section(section: ShowcaseLandingSection) -> str:
    links = "\n".join(f"          <li>{html.escape(link)}</li>" for link in section.links)
    return f"""        <article class="card" id="{html.escape(section.section_id)}">
          <h3>{html.escape(section.title)}</h3>
          <p>{html.escape(section.summary)}</p>
          <ul class="links">
{links}
          </ul>
        </article>"""
