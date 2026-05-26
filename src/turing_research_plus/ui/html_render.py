"""HTML and Markdown rendering for static dashboards."""

from __future__ import annotations

import html

from turing_research_plus.ui.assets import DEFAULT_CSS
from turing_research_plus.ui.models import StaticDashboardSpec


def render_dashboard_html(spec: StaticDashboardSpec) -> str:
    """Render a standalone HTML dashboard."""

    sections = "\n".join(
        _render_section(section.title, section.markdown) for section in spec.sections
    )
    limitations = "\n".join(f"<li>{html.escape(item)}</li>" for item in spec.limitations)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(spec.title)}</title>
  <style>{DEFAULT_CSS}</style>
</head>
<body>
  <header>
    <h1>{html.escape(spec.title)}</h1>
    <p class="meta">
      {html.escape(spec.project_name)} · static review dashboard · requires human review
    </p>
    <span class="badge warning">No Modal execution</span>
    <span class="badge warning">No VGGT execution</span>
    <span class="badge warning">Not an experiment result</span>
  </header>
  <main>
    {sections}
    <section>
      <h2>Limitations</h2>
      <ul>{limitations}</ul>
    </section>
  </main>
  <footer>
    This static dashboard displays existing review artifacts only. It does not run
    experiments, require login, or use a server.
  </footer>
</body>
</html>
"""


def render_dashboard_markdown(spec: StaticDashboardSpec) -> str:
    """Render a Markdown companion dashboard."""

    lines = [
        f"# {spec.title}",
        "",
        f"- Project: {spec.project_name}",
        "- Status: static review dashboard",
        "- Requires human review: true",
        "- No Modal execution",
        "- No VGGT execution",
        "- Not an experiment result",
        "",
    ]
    for section in spec.sections:
        lines.extend(
            [
                f"## {section.title}",
                "",
                section.markdown.strip(),
                "",
            ]
        )
    lines.extend(["## Limitations", "", *[f"- {item}" for item in spec.limitations], ""])
    return "\n".join(lines)


def _render_section(title: str, markdown: str) -> str:
    escaped = html.escape(markdown.strip())
    return f"<section><h2>{html.escape(title)}</h2><pre>{escaped}</pre></section>"
