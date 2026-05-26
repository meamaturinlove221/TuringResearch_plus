"""Build refined local-first project dashboards."""

from __future__ import annotations

import html
import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.ui.assets import DEFAULT_CSS
from turing_research_plus.ui.cards import DashboardCard, build_dashboard_cards
from turing_research_plus.ui.filters import DashboardFilterOption, build_status_filters
from turing_research_plus.ui.models import StaticDashboardRequest, StaticDashboardSpec
from turing_research_plus.ui.navigation import (
    DashboardNavItem,
    build_dashboard_navigation,
    section_slug,
)
from turing_research_plus.ui.search_index import DashboardSearchEntry, build_search_index
from turing_research_plus.ui.static_dashboard import build_static_dashboard

REFINED_EXTRA_CSS = """
.safe-banner { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.layout { display: grid; grid-template-columns: 220px 1fr; gap: 24px; }
nav { position: sticky; top: 12px; align-self: start; display: grid; gap: 8px; }
nav a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid var(--line);
  padding-bottom: 6px;
}
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}
.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 14px;
}
.card h3 { font-size: 1rem; margin-bottom: 8px; }
.filter {
  display: inline-block;
  margin: 0 8px 8px 0;
  padding: 4px 8px;
  border: 1px solid var(--line);
  border-radius: 4px;
}
.search-index { font-size: 0.85rem; color: var(--muted); }
@media (max-width: 760px) {
  .layout { grid-template-columns: 1fr; }
  nav { position: static; }
}
"""


class RefinedDashboardBundle(BaseModel):
    """A static refined dashboard bundle."""

    model_config = ConfigDict(extra="forbid")

    dashboard_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    spec: StaticDashboardSpec
    navigation: list[DashboardNavItem]
    cards: list[DashboardCard]
    filters: list[DashboardFilterOption]
    search_index: list[DashboardSearchEntry]
    generated_files: list[str] = Field(default_factory=list)
    safe_demo_mode: bool = True
    requires_human_review: bool = True
    server_required: bool = False
    login_required: bool = False
    cloud_deployed: bool = False
    network_required: bool = False
    ui_executed_experiment: bool = False

    @model_validator(mode="after")
    def bundle_is_static_and_review_only(self) -> RefinedDashboardBundle:
        if not self.safe_demo_mode:
            raise ValueError("refined dashboard requires safe demo mode")
        if not self.requires_human_review:
            raise ValueError("refined dashboard requires human review")
        if self.server_required or self.login_required or self.cloud_deployed:
            raise ValueError("refined dashboard must stay local-first/static-first")
        if self.network_required:
            raise ValueError("refined dashboard must not require network")
        if self.ui_executed_experiment:
            raise ValueError("dashboard UI must not execute experiments")
        return self


def build_refined_project_dashboard(
    request: StaticDashboardRequest,
    *,
    write_files: bool = True,
    output_filename: str = "refined_dashboard.html",
) -> RefinedDashboardBundle:
    """Build a refined static dashboard bundle."""

    spec = build_static_dashboard(request, write_files=False)
    navigation = build_dashboard_navigation(spec.sections)
    cards = build_dashboard_cards(spec.sections)
    filters = build_status_filters(cards)
    search_index = build_search_index(spec.sections, cards)
    output_path = request.output_dir / output_filename
    generated_files = [str(output_path)]

    bundle = RefinedDashboardBundle(
        dashboard_id=f"{spec.dashboard_id}_refined",
        title=f"{spec.title} - Refined",
        project_name=spec.project_name,
        spec=spec,
        navigation=navigation,
        cards=cards,
        filters=filters,
        search_index=search_index,
        generated_files=generated_files,
    )
    if write_files:
        request.output_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_refined_dashboard_html(bundle), encoding="utf-8")
    return bundle


def render_refined_dashboard_html(bundle: RefinedDashboardBundle) -> str:
    """Render a refined standalone dashboard HTML file."""

    nav_html = "\n".join(
        f'<a href="{html.escape(item.href)}">{html.escape(item.title)}</a>'
        for item in bundle.navigation
    )
    filter_html = "\n".join(
        f'<span class="filter">{html.escape(item.label)} ({item.count})</span>'
        for item in bundle.filters
    )
    cards_html = "\n".join(_render_card(card) for card in bundle.cards)
    sections_html = "\n".join(
        _render_section(item, section.markdown)
        for item, section in zip(bundle.navigation, bundle.spec.sections, strict=True)
    )
    search_payload = [entry.model_dump(mode="json") for entry in bundle.search_index]
    search_json = html.escape(json.dumps(search_payload, ensure_ascii=False))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(bundle.title)}</title>
  <style>{DEFAULT_CSS}{REFINED_EXTRA_CSS}</style>
</head>
<body>
  <header>
    <h1>{html.escape(bundle.title)}</h1>
    <p class="meta">
      {html.escape(bundle.project_name)} - local static dashboard - requires human review
    </p>
    <div class="safe-banner">
      <span class="badge warning">SAFE DEMO MODE</span>
      <span class="badge warning">No login</span>
      <span class="badge warning">No server</span>
      <span class="badge warning">No network</span>
      <span class="badge warning">Not an experiment result</span>
    </div>
  </header>
  <main class="layout">
    <nav aria-label="Dashboard sections">{nav_html}</nav>
    <div>
      <section>
        <h2>Project Overview Cards</h2>
        <div class="cards">{cards_html}</div>
        <div>{filter_html}</div>
      </section>
      {sections_html}
      <section>
        <h2>Simple Static Search Index</h2>
        <p class="search-index">
          Embedded JSON index for local search tooling. No remote search is used.
        </p>
        <script type="application/json" id="dashboard-search-index">{search_json}</script>
      </section>
    </div>
  </main>
  <footer>
    Refined dashboard displays existing local review artifacts only. It does not run Modal,
    VGGT, remote sync, or paper-writing automation.
  </footer>
</body>
</html>
"""


def _render_card(card: DashboardCard) -> str:
    return f"""<article class="card" id="card-{html.escape(card.card_id)}">
  <h3>{html.escape(card.title)}</h3>
  <p><span class="badge">{html.escape(card.status.value)}</span></p>
  <p>{html.escape(card.summary)}</p>
</article>"""


def _render_section(item: DashboardNavItem, markdown: str) -> str:
    escaped = html.escape(markdown.strip())
    title = html.escape(item.title)
    slug = html.escape(item.item_id or section_slug(item.title))
    return f"""<section id="{slug}">
  <h2>{title}</h2>
  <pre>{escaped}</pre>
</section>"""


def write_public_demo_refined_dashboard(output_path: Path) -> Path:
    """Write a safe standalone refined dashboard for the public demo."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_public_demo_refined_html(), encoding="utf-8")
    return output_path


def _public_demo_refined_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TuringResearch Public Demo Refined Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; color: #1f2937; background: #f7f8fa; }
    header, main, footer { max-width: 1080px; margin: 0 auto; padding: 24px; }
    .badge, .card { border: 1px solid #d7dce3; background: #fff; border-radius: 6px; }
    .badge { display: inline-block; padding: 4px 8px; margin: 0 6px 6px 0; }
    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
    }
    .card { padding: 14px; }
  </style>
</head>
<body>
  <header>
    <h1>TuringResearch Public Demo Refined Dashboard</h1>
    <span class="badge">SAFE DEMO MODE</span>
    <span class="badge">requires human review</span>
    <span class="badge">not an experiment result</span>
  </header>
  <main>
    <section class="cards">
      <article class="card">
        <h2>Evidence Status</h2>
        <p>Demo ledger only; fake entries remain labelled.</p>
      </article>
      <article class="card">
        <h2>Artifact Completeness</h2>
        <p>Raw data is omitted; small summaries only.</p>
      </article>
      <article class="card">
        <h2>Visual Readiness</h2>
        <p>Visual proof remains incomplete in the public demo.</p>
      </article>
      <article class="card">
        <h2>Advisor Next Action</h2>
        <p>Replace demo placeholders with reviewed evidence before claims.</p>
      </article>
    </section>
  </main>
  <footer>No login, no server, no network, no live experiment execution.</footer>
</body>
</html>
"""
