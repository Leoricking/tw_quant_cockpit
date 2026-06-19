"""
data/providers/real_data_provider_retry.py — Provider retry policy v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No infinite retry. No high-frequency bombardment. Respect retry-after.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List

from data.providers.real_data_provider_models import (
    ProviderError,
    ProviderErrorCategory,
)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False

# Shorthand references
NETWORK = ProviderErrorCategory.NETWORK
TIMEOUT = ProviderErrorCategory.TIMEOUT
DNS = ProviderErrorCategory.DNS
RATE_LIMIT = ProviderErrorCategory.RATE_LIMIT

_NON_RETRYABLE = {
    ProviderErrorCategory.AUTHENTICATION,
    ProviderErrorCategory.AUTHORIZATION,
    ProviderErrorCategory.INVALID_REQUEST,
    ProviderErrorCategory.INVALID_SYMBOL,
    ProviderErrorCategory.UNSUPPORTED_CAPABILITY,
    ProviderErrorCategory.UNSUPPORTED_MARKET,
    ProviderErrorCategory.SCHEMA_MISMATCH,
    ProviderErrorCategory.BLOCKED,
}


@dataclass
class ProviderRetryPolicy:
    """
    Retry policy for provider fetch operations.

    [!] No infinite retry. max_attempts enforced.
    [!] Respects retry_after from provider error.
    [!] Non-retryable categories never retried.
    """
    max_attempts: int = 3
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0
    backoff_multiplier: float = 2.0
    retryable_categories: List[str] = field(
        default_factory=lambda: [
            ProviderErrorCategory.NETWORK,
            ProviderErrorCategory.TIMEOUT,
            ProviderErrorCategory.DNS,
            ProviderErrorCategory.RATE_LIMIT,
        ]
    )
    respect_retry_after: bool = True
    jitter_enabled: bool = True

    def is_retryable(self, error: ProviderError) -> bool:
        """Return True if this error should trigger a retry."""
        if error.category in _NON_RETRYABLE:
            return False
        return error.category in self.retryable_categories

    def get_delay(self, attempt: int, retry_after: int = 0) -> float:
        """
        Compute wait time for given attempt number (1-based).
        Uses exponential backoff + optional jitter.
        Respects retry_after if set and respect_retry_after=True.
        """
        if self.respect_retry_after and retry_after > 0:
            return min(float(retry_after), self.max_delay_seconds)

        delay = self.initial_delay_seconds * (self.backoff_multiplier ** (attempt - 1))
        delay = min(delay, self.max_delay_seconds)
        if self.jitter_enabled and delay > 0:
            delay = delay * (0.5 + random.random() * 0.5)
        return max(0.0, delay)

    def to_dict(self) -> dict:
        return {
            "max_attempts": self.max_attempts,
            "initial_delay_seconds": self.initial_delay_seconds,
            "max_delay_seconds": self.max_delay_seconds,
            "backoff_multiplier": self.backoff_multiplier,
            "retryable_categories": list(self.retryable_categories),
            "respect_retry_after": self.respect_retry_after,
            "jitter_enabled": self.jitter_enabled,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ProviderRetryPolicy":
        return cls(
            max_attempts=d.get("max_attempts", 3),
            initial_delay_seconds=d.get("initial_delay_seconds", 1.0),
            max_delay_seconds=d.get("max_delay_seconds", 30.0),
            backoff_multiplier=d.get("backoff_multiplier", 2.0),
            retryable_categories=list(d.get("retryable_categories", [NETWORK, TIMEOUT, DNS, RATE_LIMIT])),
            respect_retry_after=d.get("respect_retry_after", True),
            jitter_enabled=d.get("jitter_enabled", True),
        )


# ---------------------------------------------------------------------------
# Preset policies (defined after class so they can reference it)
# ---------------------------------------------------------------------------

CONSERVATIVE_POLICY = ProviderRetryPolicy(
    max_attempts=3,
    initial_delay_seconds=2.0,
    max_delay_seconds=60.0,
    backoff_multiplier=2.0,
)

TEST_POLICY = ProviderRetryPolicy(
    max_attempts=2,
    initial_delay_seconds=0.0,
    max_delay_seconds=0.0,
    backoff_multiplier=1.0,
    jitter_enabled=False,
)
