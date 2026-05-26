"""Optional GitHub live client.

This module performs no network access unless callers explicitly request live
mode through the importer and provide credentials.
"""

from __future__ import annotations

import os
from importlib.util import find_spec
from typing import Any

from turing_research_plus.adapters.errors import AdapterError, AdapterErrorCode
from turing_research_plus.github_sync.models import (
    GitHubArtifactRecord,
    GitHubArtifactSourceType,
)


class GitHubLiveClient:
    """Small guarded GitHub REST client for artifact metadata."""

    def __init__(
        self,
        *,
        token_env: str = "GITHUB_TOKEN",
        base_url: str = "https://api.github.com",
        client_factory: Any | None = None,
    ) -> None:
        self.token_env = token_env
        self.base_url = base_url.rstrip("/")
        self.client_factory = client_factory

    def has_token(self) -> bool:
        """Return whether a token is present."""

        return bool(os.getenv(self.token_env))

    def missing_token_error(self) -> AdapterError:
        """Return typed missing-token error."""

        return AdapterError(
            code=AdapterErrorCode.MISSING_API_KEY,
            message=f"{self.token_env} is required for GitHub live artifact sync",
            provider="github",
        )

    def list_release_assets(self, source_repo: str, source_ref: str) -> list[GitHubArtifactRecord]:
        """List GitHub release assets for a release tag or release id."""

        payload = self._get_json(f"/repos/{source_repo}/releases/tags/{source_ref}")
        assets = payload.get("assets", []) if isinstance(payload, dict) else []
        return [
            GitHubArtifactRecord(
                name=str(asset.get("name") or "asset"),
                path=str(asset.get("name") or "asset"),
                source_type=GitHubArtifactSourceType.RELEASE_ASSET,
                size=int(asset.get("size") or 0),
                sha256=None,
                download_url=asset.get("browser_download_url"),
                content_type=asset.get("content_type"),
                metadata={"retrieved": "true"},
            )
            for asset in assets
            if isinstance(asset, dict)
        ]

    def list_workflow_artifacts(
        self,
        source_repo: str,
        source_ref: str,
    ) -> list[GitHubArtifactRecord]:
        """List GitHub workflow artifact metadata.

        `source_ref` is recorded as metadata; GitHub's artifact listing endpoint
        is repository-wide, so filtering remains a future refinement.
        """

        payload = self._get_json(f"/repos/{source_repo}/actions/artifacts")
        artifacts = payload.get("artifacts", []) if isinstance(payload, dict) else []
        return [
            GitHubArtifactRecord(
                name=str(item.get("name") or "artifact"),
                path=str(item.get("name") or "artifact"),
                source_type=GitHubArtifactSourceType.WORKFLOW_ARTIFACT,
                size=int(item.get("size_in_bytes") or 0),
                sha256=None,
                download_url=item.get("archive_download_url"),
                content_type="application/zip",
                metadata={"source_ref": source_ref, "retrieved": "true"},
            )
            for item in artifacts
            if isinstance(item, dict)
        ]

    def _get_json(self, path: str) -> Any:
        httpx_module = self._httpx_module()
        if httpx_module is None:
            raise RuntimeError("httpx is required for GitHub live artifact sync")
        token = os.getenv(self.token_env)
        if not token:
            raise RuntimeError(self.missing_token_error().message)
        client_factory = self.client_factory or httpx_module.Client
        with client_factory(timeout=20.0, follow_redirects=True) as client:
            response = client.get(
                f"{self.base_url}{path}",
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {token}",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            )
            response.raise_for_status()
            return response.json()

    def _httpx_module(self) -> Any | None:
        if find_spec("httpx") is None:
            return None
        import httpx  # type: ignore[import-not-found]

        return httpx
