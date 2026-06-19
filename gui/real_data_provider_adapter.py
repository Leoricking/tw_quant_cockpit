"""
gui/real_data_provider_adapter.py — Data adapter for Real Data Provider Panel v1.3.2.
[!] Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class RealDataProviderDataAdapter:
    """
    Data adapter that feeds the RealDataProviderPanel with data from the
    provider service and registry.

    Wraps RealDataProviderService and RealDataProviderRegistryV132.
    [!] Read-only. No orders. No credential storage.
    """

    def __init__(self, service=None, registry=None) -> None:
        self._service = service    # Optional[RealDataProviderService]
        self._registry = registry  # Optional[RealDataProviderRegistryV132]

    def get_provider_table_data(self) -> List[dict]:
        """
        Return list of provider info dicts suitable for table display.
        Each dict has keys: provider_id, provider_name, provider_type,
        enabled, status, markets, capabilities, auth_required, batch,
        historical, intraday, warning.
        """
        if self._registry is None:
            return []
        results = []
        try:
            for meta in self._registry.list():
                adapter = self._registry.get(meta.provider_id)
                try:
                    status = adapter.get_status() if adapter else "UNAVAILABLE"
                except Exception as exc:
                    status = f"ERROR: {exc}"

                warning = ""
                if meta.requires_auth:
                    warning = "AUTH_REQUIRED"
                elif not meta.enabled:
                    warning = "DISABLED"

                results.append({
                    "provider_id": meta.provider_id,
                    "provider_name": meta.provider_name,
                    "provider_type": meta.provider_type,
                    "enabled": meta.enabled,
                    "status": status,
                    "markets": ", ".join(meta.markets) if meta.markets else "(all)",
                    "capabilities": meta.capabilities,
                    "auth_required": meta.requires_auth,
                    "batch": meta.supports_batch,
                    "historical": meta.supports_historical,
                    "intraday": meta.supports_intraday,
                    "priority": meta.priority,
                    "warning": warning,
                    "data_mode": meta.data_mode,
                })
        except Exception as exc:
            logger.warning("get_provider_table_data error: %s", exc)
        return results

    def get_capability_matrix_data(self) -> dict:
        """
        Return capability matrix as dict: {provider_id: {capability: support_level}}.
        """
        if self._registry is None:
            return {}
        try:
            return self._registry.get_capability_matrix()
        except Exception as exc:
            logger.warning("get_capability_matrix_data error: %s", exc)
            return {}

    def execute_request(
        self,
        provider_id: str,
        capability: str,
        symbol: str,
        start_date: str,
        end_date: str,
        force_refresh: bool = False,
    ) -> dict:
        """
        Execute a read-only data request and return the response as dict.
        [!] Read-only. No orders.
        """
        if self._service is None:
            return {
                "status": "UNAVAILABLE",
                "errors": ["No provider service configured."],
                "records": [],
                "record_count": 0,
                "provider_id": provider_id,
                "capability": capability,
            }
        try:
            from data.providers.real_data_provider_models import ProviderRequest
            req = ProviderRequest(
                provider_id=provider_id,
                capability=capability,
                symbols=[symbol] if symbol else [],
                start_date=start_date,
                end_date=end_date,
                force_refresh=force_refresh,
            )
            resp = self._service.request(req)
            return resp.to_dict()
        except Exception as exc:
            logger.warning("execute_request error: %s", exc)
            return {
                "status": "UNAVAILABLE",
                "errors": [str(exc)],
                "records": [],
                "record_count": 0,
            }

    def get_health(self) -> dict:
        """Return health summary for all registered providers."""
        if self._registry is None:
            return {"error": "No registry configured."}
        try:
            return self._registry.health_summary()
        except Exception as exc:
            return {"error": str(exc)}
