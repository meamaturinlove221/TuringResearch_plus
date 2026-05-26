"""Optional Apify REST adapter.

The adapter is disabled by default. It performs no network access unless the
request explicitly sets `live_enabled=True` and `dry_run=False`.
"""

from __future__ import annotations

import os
from importlib.util import find_spec
from typing import Any

from turing_research_plus.adapters.errors import AdapterErrorCode
from turing_research_plus.web.apify_errors import apify_error
from turing_research_plus.web.apify_fake import FakeApifyAdapter
from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunResult, ApifyRunStatus

DEFAULT_APIFY_BASE_URL = "https://api.apify.com/v2"
APIFY_TOKEN_ENV = "APIFY_TOKEN"


class ApifyAdapter:
    """Guarded optional Apify adapter."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_APIFY_BASE_URL,
        token_env: str = APIFY_TOKEN_ENV,
        client_factory: Any | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token_env = token_env
        self.client_factory = client_factory
        self.fake = FakeApifyAdapter()

    def run(self, request: ApifyRunRequest) -> ApifyRunResult:
        """Run an Apify actor if live mode is explicitly enabled."""

        if request.dry_run:
            return self.fake.run(request)
        if not request.live_enabled:
            return ApifyRunResult(
                actor_id=request.actor_id,
                status=ApifyRunStatus.LIVE_DISABLED,
                input=request.input,
                warnings=["Apify live adapter is disabled by default"],
                errors=[
                    apify_error(
                        AdapterErrorCode.LIVE_DISABLED,
                        "Apify live adapter is disabled by default",
                    )
                ],
            )
        token = os.getenv(self.token_env)
        if not token:
            return ApifyRunResult(
                actor_id=request.actor_id,
                status=ApifyRunStatus.MISSING_TOKEN,
                input=request.input,
                warnings=[f"{self.token_env} is required for Apify live mode"],
                errors=[
                    apify_error(
                        AdapterErrorCode.MISSING_API_KEY,
                        f"{self.token_env} is required for Apify live mode",
                    )
                ],
            )
        httpx_module = self._httpx_module()
        if httpx_module is None:
            return ApifyRunResult(
                actor_id=request.actor_id,
                status=ApifyRunStatus.ERROR,
                input=request.input,
                warnings=["httpx is required for Apify live mode"],
                errors=[
                    apify_error(
                        AdapterErrorCode.UNSUPPORTED,
                        "httpx is required for Apify live mode",
                    )
                ],
            )
        if not request.actor_id:
            return ApifyRunResult(
                status=ApifyRunStatus.ERROR,
                input=request.input,
                warnings=["actor_id is required for Apify live mode"],
                errors=[
                    apify_error(
                        AdapterErrorCode.INVALID_RESPONSE,
                        "actor_id is required for Apify live mode",
                    )
                ],
            )
        return self._run_live(request, httpx_module, token)

    def _run_live(self, request: ApifyRunRequest, httpx_module: Any, token: str) -> ApifyRunResult:
        try:
            client_factory = self.client_factory or httpx_module.Client
            with client_factory(timeout=request.timeout_seconds) as client:
                response = client.post(
                    f"{self.base_url}/acts/{request.actor_id}/run-sync-get-dataset-items",
                    params={"token": token},
                    json=request.input,
                )
                response.raise_for_status()
                payload = response.json()
        except httpx_module.TimeoutException:
            return ApifyRunResult(
                actor_id=request.actor_id,
                status=ApifyRunStatus.ERROR,
                input=request.input,
                warnings=["Apify request timed out"],
                errors=[apify_error(AdapterErrorCode.TIMEOUT, "Apify request timed out")],
            )
        except httpx_module.HTTPStatusError as exc:
            status_code = exc.response.status_code
            code = (
                AdapterErrorCode.RATE_LIMITED
                if status_code == 429
                else AdapterErrorCode.PROVIDER_ERROR
            )
            return ApifyRunResult(
                actor_id=request.actor_id,
                status=ApifyRunStatus.ERROR,
                input=request.input,
                warnings=[f"Apify provider returned HTTP {status_code}"],
                errors=[
                    apify_error(
                        code,
                        "Apify provider returned an error",
                        retryable=status_code == 429 or status_code >= 500,
                        status_code=status_code,
                    )
                ],
            )
        except httpx_module.HTTPError:
            return ApifyRunResult(
                actor_id=request.actor_id,
                status=ApifyRunStatus.ERROR,
                input=request.input,
                warnings=["Apify provider request failed"],
                errors=[
                    apify_error(
                        AdapterErrorCode.PROVIDER_ERROR,
                        "Apify provider request failed",
                        retryable=True,
                    )
                ],
            )
        except ValueError:
            return ApifyRunResult(
                actor_id=request.actor_id,
                status=ApifyRunStatus.ERROR,
                input=request.input,
                warnings=["Apify returned invalid JSON"],
                errors=[
                    apify_error(
                        AdapterErrorCode.INVALID_RESPONSE,
                        "Apify returned invalid JSON",
                    )
                ],
            )
        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            items = [payload]
        else:
            items = []
        output_items = [dict(item) for item in items if isinstance(item, dict)]
        return ApifyRunResult(
            actor_id=request.actor_id,
            run_id=None,
            status=ApifyRunStatus.SUCCEEDED,
            input=request.input,
            output_items=output_items,
            warnings=["live Apify result is retrieved, not human verified"],
            errors=[],
            requires_human_review=True,
        )

    def _httpx_module(self) -> Any | None:
        if find_spec("httpx") is None:
            return None
        import httpx  # type: ignore[import-not-found]

        return httpx
