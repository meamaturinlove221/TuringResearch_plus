"""Static interview demo view for short project walkthroughs."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InterviewDemoSection:
    """One section in the interview demo view."""

    section_id: str
    title: str
    talking_point: str
    proof_points: tuple[str, ...]


@dataclass(frozen=True)
class InterviewDemoView:
    """Data for a 3-10 minute interview dashboard view."""

    title: str
    subtitle: str
    status: str
    sections: tuple[InterviewDemoSection, ...]
    closing_points: tuple[str, ...]


def build_interview_demo_view() -> InterviewDemoView:
    """Build the default v1.5 interview demo view."""

    return InterviewDemoView(
        title="TuringResearch Interview Demo",
        subtitle=(
            "A 3-10 minute static walkthrough of architecture, module breadth, "
            "original repo parity, gates, demos, split strategy, and ARIS deferral."
        ),
        status="static-local-first-demo",
        sections=(
            InterviewDemoSection(
                section_id="architecture",
                title="Architecture",
                talking_point=(
                    "TuringResearch is organized as a local-first Research OS: "
                    "docs, examples, contracts, tests, dashboards, and review-only "
                    "runtime surfaces all reinforce the same safety model."
                ),
                proof_points=(
                    "src/turing_research_plus/",
                    "docs/original-repo-production-parity-summary.md",
                    "docs/v1.4.0-full-production-replay-report.md",
                ),
            ),
            InterviewDemoSection(
                section_id="modules",
                title="Modules",
                talking_point=(
                    "The project spans Session runtime, Scholar/Web tooling, "
                    "campaigns, vault/ontology, stress testing, convergence, "
                    "experiment runbooks, docs-site, and static dashboard UI."
                ),
                proof_points=(
                    "docs/v1.4.0-feature-list.md",
                    "docs/v1.4.0-session-parity-summary.md",
                    "docs/v1.4.0-scholar-web-production-summary.md",
                    "docs/v1.4.0-yogsoth-production-summary.md",
                ),
            ),
            InterviewDemoSection(
                section_id="original-repo-parity",
                title="Original Repo Parity",
                talking_point=(
                    "Stable Neocortica Session, Scholar, Web, and yogsoth-ai "
                    "ideas were replicated through structural, runtime, and "
                    "production parity gates."
                ),
                proof_points=(
                    "docs/original-repo-parity-dashboard-v2.md",
                    "examples/public_demo/dashboard_showcase/parity.html",
                    "docs/original-repo-replication-scorecard.md",
                ),
            ),
            InterviewDemoSection(
                section_id="safety-gates",
                title="Safety Gates",
                talking_point=(
                    "The repo treats safety as product infrastructure: no default "
                    "network, no unsafe remote execution, no private data, and no "
                    "planned result promoted to observed evidence."
                ),
                proof_points=(
                    "docs/v1.4.0-security-audit.md",
                    "docs/v1.4.0-privacy-audit.md",
                    "docs/optional-live-safety-gate.md",
                ),
            ),
            InterviewDemoSection(
                section_id="tests-contracts",
                title="Tests / Contracts",
                talking_point=(
                    "Behavior is captured in workflow tests and contract tests, "
                    "so docs, examples, configs, and safety boundaries stay aligned."
                ),
                proof_points=(
                    "tests/workflow/",
                    "tests/contract/",
                    "contracts/",
                    "docs/v1.4.0-test-summary.md",
                ),
            ),
            InterviewDemoSection(
                section_id="public-demo",
                title="Public Demo",
                talking_point=(
                    "The showcase uses fake/demo data to explain workflows without "
                    "requiring credentials, private files, live providers, or raw "
                    "research payloads."
                ),
                proof_points=(
                    "examples/public_demo/",
                    "examples/public_demo/dashboard_showcase/landing.html",
                    "docs/public-showcase.md",
                ),
            ),
            InterviewDemoSection(
                section_id="split-strategy",
                title="Split Strategy",
                talking_point=(
                    "The main repo remains the flagship, while case/demo child repos "
                    "are prepared as manual packs instead of being auto-created."
                ),
                proof_points=(
                    "docs/v1.5.0-split-sprint-gate-report.md",
                    "split_manual/turingresearch-vggt-case/",
                    "split_manual/turingresearch-examples/",
                ),
            ),
            InterviewDemoSection(
                section_id="aris-deferred",
                title="Why ARIS Deferred",
                talking_point=(
                    "ARIS stays out of the default implementation because cross-model "
                    "review, proof checking, meta optimization, and paper claim audit "
                    "would add research-automation and claim-authority risk."
                ),
                proof_points=(
                    "docs/aris-still-deferred-v1.4.md",
                    "docs/v1.5.0-aris-still-deferred.md",
                    "docs/v1.5.0-non-goals-final.md",
                ),
            ),
        ),
        closing_points=(
            "Show the landing page first.",
            "Open the parity showcase for replication progress.",
            "Point to gates and tests as evidence of engineering discipline.",
            "Close with ARIS deferred as a deliberate scope decision.",
        ),
    )


def render_interview_demo_html(view: InterviewDemoView | None = None) -> str:
    """Render a standalone static interview demo page."""

    view = view or build_interview_demo_view()
    sections = "\n".join(_render_section(section) for section in view.sections)
    closing = "\n".join(
        f"          <li>{html.escape(item)}</li>" for item in view.closing_points
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(view.title)}</title>
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
      max-width: 1160px;
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
    .timeline {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }}
    .card p {{ color: var(--muted); }}
    .proof {{
      margin: 12px 0 0;
      padding-left: 18px;
      color: var(--muted);
    }}
    .closing {{
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
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <p class="eyebrow">3-10 minute interview demo</p>
      <h1>{html.escape(view.title)}</h1>
      <p class="subtitle">{html.escape(view.subtitle)}</p>
      <span class="badge">{html.escape(view.status)}</span>
      <span class="badge">tests and contracts</span>
      <span class="badge">public demo</span>
      <span class="badge warning">ARIS deferred</span>
    </div>
  </header>
  <main>
    <section aria-labelledby="demo-flow">
      <h2 id="demo-flow">Demo Flow</h2>
      <div class="timeline">
{sections}
      </div>
    </section>
    <section class="closing" aria-labelledby="closing-script">
      <h2 id="closing-script">Suggested Closing</h2>
      <ul>
{closing}
      </ul>
    </section>
  </main>
  <footer>
    Static/local-first interview view. It does not run providers, commands,
    experiments, analytics, or deployment.
  </footer>
</body>
</html>
"""


def write_interview_demo_view(
    path: Path, view: InterviewDemoView | None = None
) -> Path:
    """Write the interview demo HTML to a local path."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_interview_demo_html(view), encoding="utf-8")
    return path


def _render_section(section: InterviewDemoSection) -> str:
    proof_points = "\n".join(
        f"          <li>{html.escape(item)}</li>" for item in section.proof_points
    )
    return f"""        <article class="card" id="{html.escape(section.section_id)}">
          <h3>{html.escape(section.title)}</h3>
          <p>{html.escape(section.talking_point)}</p>
          <ul class="proof">
{proof_points}
          </ul>
        </article>"""
