"""Rate limit placeholders for optional live adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from turing_research_plus.adapters.errors import AdapterError, AdapterErrorCode
from turing_research_plus.adapters.models import RateLimitPolicy


@dataclass
class RateLimitState:
    """In-memory rate window used by tests; it never sleeps."""

    timestamps: list[datetime] = field(default_factory=list)


class RateLimitChecker:
    """Return typed errors when a simple per-minute quota is exceeded."""

    def __init__(self, policy: RateLimitPolicy, state: RateLimitState | None = None) -> None:
        self.policy = policy
        self.state = state or RateLimitState()

    def check(self, *, provider: str) -> AdapterError | None:
        if self.policy.requests_per_minute is None:
            return None

        now = datetime.now(UTC)
        cutoff = now - timedelta(minutes=1)
        self.state.timestamps = [stamp for stamp in self.state.timestamps if stamp >= cutoff]
        if len(self.state.timestamps) >= self.policy.requests_per_minute:
            return AdapterError(
                code=AdapterErrorCode.RATE_LIMITED,
                message="adapter rate limit placeholder exceeded",
                retryable=True,
                provider=provider,
                details={"policy": self.policy.provider_quota_label or "requests_per_minute"},
            )
        self.state.timestamps.append(now)
        return None
