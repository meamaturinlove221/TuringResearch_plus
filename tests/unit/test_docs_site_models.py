from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.docs_site.models import (
    DocsSiteBuildRequest,
    DocsSiteManifest,
    DocsSiteNav,
    DocsSiteNavItem,
)


def test_docs_site_nav_model_requires_unique_ids() -> None:
    with pytest.raises(ValueError, match="unique"):
        DocsSiteNav(
            site_title="Docs",
            status="test",
            items=[
                DocsSiteNavItem(item_id="intro", title="Intro", page="pages/a.md"),
                DocsSiteNavItem(item_id="intro", title="Intro Again", page="pages/b.md"),
            ],
        )


def test_docs_site_manifest_rejects_cloud_dependency() -> None:
    with pytest.raises(ValueError, match="cloud"):
        DocsSiteManifest(
            site_id="docs",
            status="bad",
            source_of_truth="repo",
            cloud_dependency=True,
            required_sections=["introduction"],
        )


def test_docs_site_build_request_is_local_paths() -> None:
    request = DocsSiteBuildRequest(
        repo_root=Path("."),
        docs_site_root=Path("docs-site"),
        output_root=Path("docs-site/output"),
        nav_path=Path("docs-site/nav.yaml"),
        manifest_path=Path("docs-site/site_manifest.yaml"),
    )

    assert request.copy_assets is True
