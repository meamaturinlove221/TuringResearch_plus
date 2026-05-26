"""Build a local static docs site from docs-site navigation."""

from __future__ import annotations

import html
from pathlib import Path

from turing_research_plus.docs_site.assets import copy_docs_site_assets
from turing_research_plus.docs_site.markdown_render import render_markdown_to_html
from turing_research_plus.docs_site.models import (
    DocsSiteBuildRequest,
    DocsSiteBuildResult,
    DocsSiteNav,
)
from turing_research_plus.docs_site.nav import (
    load_docs_site_manifest,
    load_docs_site_nav,
    validate_nav_against_manifest,
)

DOCS_SITE_CSS = """
:root {
  color-scheme: light;
  --bg: #f8fafc;
  --panel: #ffffff;
  --text: #1f2937;
  --muted: #5f6b7a;
  --line: #d7dde7;
  --accent: #215f9a;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.55;
}
header, main, footer { max-width: 1120px; margin: 0 auto; padding: 24px; }
header { padding-top: 34px; }
.layout { display: grid; grid-template-columns: 240px 1fr; gap: 24px; }
nav {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 14px;
  align-self: start;
  position: sticky;
  top: 12px;
}
nav a { display: block; color: var(--accent); text-decoration: none; padding: 5px 0; }
article {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 22px;
}
pre { overflow: auto; background: #f1f4f8; padding: 12px; border-radius: 4px; }
code { background: #edf1f7; padding: 1px 4px; border-radius: 3px; }
.meta { color: var(--muted); }
@media (max-width: 800px) {
  .layout { grid-template-columns: 1fr; }
  nav { position: static; }
}
"""

LEGACY_SUPPORT_PAGES = {
    "showcase": "pages/showcase.md",
    "case-study-gallery": "pages/case-study-gallery.md",
}


def build_docs_site(request: DocsSiteBuildRequest) -> DocsSiteBuildResult:
    """Build static HTML pages from docs-site nav and Markdown pages."""

    manifest = load_docs_site_manifest(request.manifest_path)
    nav = load_docs_site_nav(request.nav_path)
    warnings = validate_nav_against_manifest(nav, manifest)

    request.output_root.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    nav_html = _render_nav(nav)
    for item in nav.items:
        source_page = request.docs_site_root / item.page
        if not source_page.exists():
            warnings.append(f"missing page: {item.page}")
            continue
        markdown = source_page.read_text(encoding="utf-8")
        body = render_markdown_to_html(markdown)
        target = request.output_root / Path(item.page).with_suffix(".html").name
        target.write_text(
            _render_page(
                site_title=nav.site_title,
                page_title=item.title,
                nav_html=nav_html,
                body_html=body,
                source_docs=item.source_docs,
            ),
            encoding="utf-8",
        )
        generated.append(target)

    index_target = request.output_root / "index.html"
    if not any(path.name == "index.html" for path in generated):
        index_target.write_text(
            _render_index(nav.site_title, nav_html),
            encoding="utf-8",
        )
        generated.insert(0, index_target)

    generated_names = {path.name for path in generated}
    for title, page in LEGACY_SUPPORT_PAGES.items():
        target_name = Path(page).with_suffix(".html").name
        if target_name in generated_names:
            continue
        source_page = request.docs_site_root / page
        if not source_page.exists():
            warnings.append(f"missing legacy support page: {page}")
            continue
        body = render_markdown_to_html(source_page.read_text(encoding="utf-8"))
        target = request.output_root / target_name
        target.write_text(
            _render_page(
                site_title=nav.site_title,
                page_title=title.replace("-", " ").title(),
                nav_html=nav_html,
                body_html=body,
                source_docs=[],
            ),
            encoding="utf-8",
        )
        generated.append(target)
        generated_names.add(target_name)

    css_target = request.output_root / "site.css"
    css_target.write_text(DOCS_SITE_CSS.strip() + "\n", encoding="utf-8")
    generated.append(css_target)

    copied_assets = copy_docs_site_assets(request.docs_site_root, request.output_root)
    return DocsSiteBuildResult(
        site_id=manifest.site_id,
        output_root=request.output_root,
        generated_files=generated,
        copied_assets=copied_assets if request.copy_assets else [],
        warnings=warnings,
    )


def build_docs_site_from_repo(
    repo_root: Path,
    *,
    output_root: Path | None = None,
) -> DocsSiteBuildResult:
    """Build the docs-site skeleton from the repository root."""

    docs_site_root = repo_root / "docs-site"
    return build_docs_site(
        DocsSiteBuildRequest(
            repo_root=repo_root,
            docs_site_root=docs_site_root,
            output_root=output_root or docs_site_root / "output",
            nav_path=docs_site_root / "nav.yaml",
            manifest_path=docs_site_root / "site_manifest.yaml",
        )
    )


def _render_nav(nav: DocsSiteNav) -> str:
    links = [
        f'<a href="{html.escape(Path(item.page).with_suffix(".html").name)}">'
        f"{html.escape(item.title)}</a>"
        for item in nav.items
    ]
    return "\n".join(links)


def _render_page(
    *,
    site_title: str,
    page_title: str,
    nav_html: str,
    body_html: str,
    source_docs: list[str],
) -> str:
    sources = "\n".join(f"<li><code>{html.escape(source)}</code></li>" for source in source_docs)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page_title)} - {html.escape(site_title)}</title>
  <link rel="stylesheet" href="site.css">
</head>
<body>
  <header>
    <h1>{html.escape(site_title)}</h1>
    <p class="meta">Local-first static docs. No deployment or cloud service required.</p>
  </header>
  <main class="layout">
    <nav aria-label="Docs navigation">{nav_html}</nav>
    <article>
      {body_html}
      <h2>Source Docs</h2>
      <ul>{sources}</ul>
    </article>
  </main>
  <footer class="meta">Generated locally from repository Markdown. Requires human review.</footer>
</body>
</html>
"""


def _render_index(site_title: str, nav_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(site_title)}</title>
  <link rel="stylesheet" href="site.css">
</head>
<body>
  <header>
    <h1>{html.escape(site_title)}</h1>
    <p class="meta">Local-first static documentation index.</p>
  </header>
  <main class="layout">
    <nav aria-label="Docs navigation">{nav_html}</nav>
    <article>
      <h2>Start Here</h2>
      <p>This static site is generated from repository Markdown.</p>
      <p>No server, Node, deployment, cloud account, or private data is required.</p>
    </article>
  </main>
</body>
</html>
"""
