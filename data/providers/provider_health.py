"""
data/providers/provider_health.py - Provider health checker (v0.3.18).

Checks availability, token configuration, and read-only status for all
TW Quant Cockpit data providers. Never places orders. Never logs full tokens.

[!] Read Only. No Real Orders.
[!] Tokens masked in all output.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from data.providers.token_safe_config import TokenSafeConfig

logger = logging.getLogger(__name__)

# Status constants
OK              = "OK"
NOT_CONFIGURED  = "NOT_CONFIGURED"
PARTIAL         = "PARTIAL"
FAILED          = "FAILED"
PLANNED         = "PLANNED"
DISABLED        = "DISABLED"


class ProviderHealthStatus:
    """Structured result for a single provider health check."""

    __slots__ = (
        "provider_name", "status", "read_only", "no_real_orders",
        "token_required", "token_configured", "token_masked",
        "base_url", "last_checked_at", "message", "error",
        "recommended_action", "capabilities",
    )

    def __init__(
        self,
        provider_name:    str,
        status:           str = NOT_CONFIGURED,
        read_only:        bool = True,
        no_real_orders:   bool = True,
        token_required:   bool = False,
        token_configured: bool = False,
        token_masked:     str = "(not configured)",
        base_url:         str = "",
        last_checked_at:  str = "",
        message:          str = "",
        error:            str = "",
        recommended_action: str = "",
        capabilities:     Optional[dict] = None,
    ):
        self.provider_name      = provider_name
        self.status             = status
        self.read_only          = read_only
        self.no_real_orders     = no_real_orders
        self.token_required     = token_required
        self.token_configured   = token_configured
        self.token_masked       = token_masked
        self.base_url           = base_url
        self.last_checked_at    = last_checked_at or datetime.now().isoformat()
        self.message            = message
        self.error              = error
        self.recommended_action = recommended_action
        self.capabilities       = capabilities or {}

    def to_dict(self) -> dict:
        return {
            "provider_name":      self.provider_name,
            "status":             self.status,
            "read_only":          self.read_only,
            "no_real_orders":     self.no_real_orders,
            "token_required":     self.token_required,
            "token_configured":   self.token_configured,
            "token_masked":       self.token_masked,
            "base_url":           self.base_url,
            "last_checked_at":    self.last_checked_at,
            "message":            self.message,
            "error":              self.error,
            "recommended_action": self.recommended_action,
            "capabilities":       self.capabilities,
        }


class ProviderHealthChecker:
    """
    Checks health status of all registered data providers.

    Parameters
    ----------
    env_path     : Path to .env file (default: ".env")
    providers    : List of provider names to check (None = all)
    mask_tokens  : Always mask tokens in output (default: True)
    """

    def __init__(
        self,
        env_path:    str = ".env",
        providers:   Optional[List[str]] = None,
        mask_tokens: bool = True,
    ):
        self._token_cfg  = TokenSafeConfig(env_path=env_path)
        self._providers  = providers  # None = check all
        self._mask_tokens = mask_tokens

    def mask_token(self, token: str) -> str:
        return self._token_cfg.mask_token(token)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run_all(self) -> dict:
        """
        Run all provider health checks.

        Returns dict with keys:
            checked_at, providers (list of ProviderHealthStatus.to_dict()),
            summary (counts by status), token_status (masked),
            read_only_guarantee, no_real_orders
        """
        self._token_cfg.load_env()
        checked_at = datetime.now().isoformat()

        checks = [
            ("csv",                  self.check_csv_provider),
            ("xq_export",            self.check_xq_provider),
            ("finmind",              self.check_finmind),
            ("twse",                 self.check_twse),
            ("tpex",                 self.check_tpex),
            ("mops",                 self.check_mops),
            ("mega_readonly_planned",self.check_mega_readonly),
        ]

        results = []
        for name, fn in checks:
            if self._providers and name not in self._providers:
                continue
            try:
                result = fn()
            except Exception as exc:
                logger.error("ProviderHealthChecker: %s check raised: %s", name, exc)
                result = ProviderHealthStatus(
                    provider_name=name,
                    status=FAILED,
                    message=f"Check raised exception: {exc}",
                    error=str(exc),
                )
            results.append(result.to_dict())

        # Summary counts
        summary = {s: 0 for s in [OK, NOT_CONFIGURED, PARTIAL, FAILED, PLANNED, DISABLED]}
        for r in results:
            s = r.get("status", FAILED)
            if s in summary:
                summary[s] += 1

        token_status = self._token_cfg.get_all_token_status()

        return {
            "checked_at":         checked_at,
            "providers":          results,
            "summary":            summary,
            "token_status":       token_status,
            "read_only_guarantee": True,
            "no_real_orders":     True,
        }

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def check_csv_provider(self) -> ProviderHealthStatus:
        """CSV provider — always available if data files exist."""
        try:
            from data.providers.csv_provider import CSVProvider
            p = CSVProvider()
            hc = p.health_check() if hasattr(p, "health_check") else {}
            ok = hc.get("ok", hc.get("available", True))
            return ProviderHealthStatus(
                provider_name   = "csv",
                status          = OK if ok else PARTIAL,
                read_only       = True,
                no_real_orders  = True,
                token_required  = False,
                token_configured= True,
                token_masked    = "(no token needed)",
                base_url        = "local",
                message         = hc.get("note", "Local CSV data provider. No token required."),
                recommended_action = (
                    "Import CSV data files if not yet imported."
                    if not ok else ""
                ),
                capabilities    = {"daily_price": True, "monthly_revenue": True,
                                   "institutional": True, "margin": True,
                                   "real_order_execution": False},
            )
        except Exception as exc:
            return ProviderHealthStatus(
                provider_name="csv",
                status=FAILED,
                message=f"CSVProvider unavailable: {exc}",
                error=str(exc),
                recommended_action="Check data/providers/csv_provider.py is present.",
            )

    def check_xq_provider(self) -> ProviderHealthStatus:
        """XQ Export provider — available if XQ export files exist."""
        try:
            from data.providers.xq_export_provider import XQExportProvider
            p = XQExportProvider()
            hc = p.health_check() if hasattr(p, "health_check") else {}
            ok = hc.get("ok", hc.get("available", True))
            return ProviderHealthStatus(
                provider_name   = "xq_export",
                status          = OK if ok else PARTIAL,
                read_only       = True,
                no_real_orders  = True,
                token_required  = False,
                token_configured= True,
                token_masked    = "(no token needed)",
                base_url        = "local",
                message         = hc.get("note", "XQ export file provider. No token required."),
                recommended_action = (
                    "Import XQ export files if not yet imported."
                    if not ok else ""
                ),
                capabilities    = {"daily_price": True, "intraday": True,
                                   "real_order_execution": False},
            )
        except Exception as exc:
            return ProviderHealthStatus(
                provider_name="xq_export",
                status=FAILED,
                message=f"XQExportProvider unavailable: {exc}",
                error=str(exc),
                recommended_action="Check data/providers/xq_export_provider.py is present.",
            )

    def check_finmind(self) -> ProviderHealthStatus:
        """FinMind API provider — checks token config and network reachability."""
        token_configured = self._token_cfg.has_token("FINMIND_TOKEN")
        token_masked     = self._token_cfg.get_masked_token("FINMIND_TOKEN")

        # Try a lightweight network check via the provider
        try:
            from data.providers.finmind_provider import FinMindProvider
            p = FinMindProvider()
            hc = p.health_check()
            network_ok = hc.get("ok", hc.get("available", False))
        except Exception as exc:
            network_ok = False
            logger.debug("FinMind health check error: %s", exc)

        if not token_configured and not network_ok:
            status = NOT_CONFIGURED
            message = "FINMIND_TOKEN not set. Network unreachable. Limited or no data available."
            action  = "Set FINMIND_TOKEN in your .env file. See docs/api_provider_hardening.md."
        elif not token_configured:
            status  = PARTIAL
            message = "FINMIND_TOKEN not set. Public data may be accessible but rate-limited."
            action  = "Set FINMIND_TOKEN in .env for full access."
        elif not network_ok:
            status  = FAILED
            message = "FINMIND_TOKEN configured but FinMind API not reachable."
            action  = "Check network connection or FinMind service status."
        else:
            status  = OK
            message = "FinMind API reachable. Token configured."
            action  = ""

        return ProviderHealthStatus(
            provider_name   = "finmind",
            status          = status,
            read_only       = True,
            no_real_orders  = True,
            token_required  = False,
            token_configured= token_configured,
            token_masked    = token_masked if token_configured else "(not configured)",
            base_url        = "https://api.finmindtrade.com/api/v4/data",
            message         = message,
            recommended_action = action,
            capabilities    = {
                "daily_price": True, "monthly_revenue": True,
                "institutional": True, "margin": True, "fundamental": True,
                "real_order_execution": False,
            },
        )

    def check_twse(self) -> ProviderHealthStatus:
        """TWSE Open API provider — planned, no auth required."""
        try:
            from data.providers.twse_openapi_provider import TWSEOpenAPIProvider
            p = TWSEOpenAPIProvider()
            hc = p.health_check()
            planned = hc.get("planned", True)
            available = hc.get("available", False)
        except Exception as exc:
            planned   = True
            available = False
            logger.debug("TWSE health check error: %s", exc)

        status = PLANNED if planned and not available else (OK if available else PARTIAL)

        return ProviderHealthStatus(
            provider_name   = "twse",
            status          = status,
            read_only       = True,
            no_real_orders  = True,
            token_required  = False,
            token_configured= True,
            token_masked    = "(no token needed)",
            base_url        = "https://openapi.twse.com.tw/",
            message         = (
                "PLANNED for v0.4. TWSE Open API requires no authentication."
                if planned else "TWSE provider available."
            ),
            recommended_action = "No action needed. Will be enabled in v0.4.",
            capabilities    = {
                "daily_price": False, "monthly_revenue": False,
                "institutional": False, "real_order_execution": False,
            },
        )

    def check_tpex(self) -> ProviderHealthStatus:
        """TPEx provider — planned, no auth required."""
        return ProviderHealthStatus(
            provider_name   = "tpex",
            status          = PLANNED,
            read_only       = True,
            no_real_orders  = True,
            token_required  = False,
            token_configured= True,
            token_masked    = "(no token needed)",
            base_url        = "https://www.tpex.org.tw/openapi/",
            message         = "PLANNED for v0.4. TPEx Open API requires no authentication.",
            recommended_action = "No action needed. Will be enabled in v0.4.",
            capabilities    = {
                "daily_price": False, "monthly_revenue": False,
                "real_order_execution": False,
            },
        )

    def check_mops(self) -> ProviderHealthStatus:
        """MOPS provider — planned, no auth required."""
        mops_key = self._token_cfg.has_token("MOPS_API_KEY")
        return ProviderHealthStatus(
            provider_name   = "mops",
            status          = PLANNED,
            read_only       = True,
            no_real_orders  = True,
            token_required  = False,
            token_configured= mops_key,
            token_masked    = self._token_cfg.get_masked_token("MOPS_API_KEY") if mops_key else "(optional)",
            base_url        = "https://mops.twse.com.tw/",
            message         = "PLANNED for v0.4. MOPS public disclosure API. No token required.",
            recommended_action = "No action needed. Will be enabled in v0.4.",
            capabilities    = {
                "monthly_revenue": False, "fundamental": False,
                "real_order_execution": False,
            },
        )

    def check_mega_readonly(self) -> ProviderHealthStatus:
        """Mega provider — PLANNED / READ-ONLY ONLY. No order execution."""
        try:
            from data.providers.mega_provider import MegaProvider
            p = MegaProvider()
            hc = p.health_check()
            order_enabled = hc.get("order_enabled", False)
        except Exception as exc:
            order_enabled = False
            logger.debug("Mega health check error: %s", exc)

        # Safety check: if somehow order_enabled is True, flag it
        if order_enabled:
            return ProviderHealthStatus(
                provider_name    = "mega_readonly_planned",
                status           = FAILED,
                read_only        = False,
                no_real_orders   = False,
                token_required   = False,
                token_configured = False,
                token_masked     = "(unsafe)",
                base_url         = "",
                message          = "[FAIL] Mega provider has order_enabled=True. This is UNSAFE.",
                error            = "order_enabled=True detected — real order execution should be disabled",
                recommended_action = "Immediately set _MEGA_ORDER_ENABLED=False in mega_provider.py",
            )

        mega_key = self._token_cfg.has_token("MEGA_API_KEY")
        return ProviderHealthStatus(
            provider_name   = "mega_readonly_planned",
            status          = PLANNED,
            read_only       = True,
            no_real_orders  = True,
            token_required  = False,
            token_configured= mega_key,
            token_masked    = self._token_cfg.get_masked_token("MEGA_API_KEY") if mega_key else "(planned)",
            base_url        = "",
            message         = (
                "PLANNED for v0.4+. Chiao-Tung Securities (兆豐證券) read-only API. "
                "Real order execution permanently disabled."
            ),
            recommended_action = "No action needed. Read-only API integration planned for v0.4+.",
            capabilities    = {
                "daily_price": False, "intraday": False,
                "tick": False, "bidask": False,
                "real_order_execution": False,
            },
        )
