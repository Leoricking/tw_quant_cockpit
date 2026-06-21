"""
data/governance/request_fingerprint_v145.py — Request Fingerprint Service v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Secrets removed (token, key, cookie, auth). Param order independent (sorted keys).
[!] Deterministic — no random hash(). Real/mock modes produce different fingerprints.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_SECRET_PARAM_NAMES = {
    "token", "key", "api_key", "apikey", "auth", "authorization",
    "cookie", "password", "secret", "access_token", "private_key",
    "refresh_token",
}


class RequestFingerprintService:
    """
    Computes deterministic request fingerprints.
    [!] Secrets removed. Parameter order independent (sorted keys).
    [!] Real/mock modes → different fingerprint.
    [!] Provider different → different fingerprint.
    [!] No random hash(). SHA-256 only.
    """

    def compute(
        self,
        provider_id: str,
        host: str,
        endpoint: str,
        method: str,
        dataset: str,
        data_id: str,
        start_date: str,
        end_date: str,
        schema_version: str,
        mode: str,
        api_version: str,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Compute SHA-256 fingerprint. Deterministic, secrets-free, order-independent."""
        params: Dict[str, Any] = {
            "provider_id": provider_id,
            "host": host,
            "endpoint": endpoint,
            "method": method.upper(),
            "dataset": dataset,
            "data_id": data_id,
            "start_date": start_date,
            "end_date": end_date,
            "schema_version": schema_version,
            "mode": mode,
            "api_version": api_version,
        }
        if extra_params:
            cleaned = self._remove_secrets(extra_params)
            params.update(cleaned)

        # Sort keys for order independence
        canonical = json.dumps(params, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _remove_secrets(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Remove secret keys from params dict."""
        return {
            k: v
            for k, v in params.items()
            if k.lower() not in _SECRET_PARAM_NAMES
        }
