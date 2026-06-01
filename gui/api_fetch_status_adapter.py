"""
gui/api_fetch_status_adapter.py - GUI bridge for API Fetch Status panel (v0.4.1).

[!] Read Only. No Real Orders.
[!] Never modifies real .env.
[!] Never displays full token.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class APIFetchStatusAdapter:
    """
    GUI bridge for the API Fetch Status panel.

    Parameters
    ----------
    report_dir : Directory where reports are written (default: reports/)

    All methods return safe dicts (no full tokens in output).
    """

    read_only      = True
    no_real_orders = True

    def __init__(self, report_dir: str = "reports"):
        self._report_dir = os.path.join(_BASE_DIR, report_dir) if not os.path.isabs(report_dir) else report_dir

    # ------------------------------------------------------------------
    # Token check
    # ------------------------------------------------------------------

    def check_token_setup(self) -> dict:
        """
        Run TokenSetupAssistant.inspect(). Returns safe dict with masked tokens.
        Never modifies .env.
        """
        try:
            from data.providers.token_setup_assistant import TokenSetupAssistant
            assistant = TokenSetupAssistant()
            result = assistant.inspect()
            return {"ok": True, "data": result}
        except Exception as exc:
            logger.warning("APIFetchStatusAdapter.check_token_setup: %s", exc)
            return {
                "ok": False,
                "error": str(exc),
                "data": {
                    "all_required_configured": False,
                    "required_tokens": {},
                    "env_safety": {},
                    "setup_instructions": {},
                },
            }

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def run_diagnostics(self, mode: str = "real") -> dict:
        """
        Run lightweight API fetch diagnostics.
        Returns provider health and cache status summary.
        Does NOT fetch real market data.
        """
        result: dict = {
            "mode":                mode,
            "read_only":           True,
            "no_real_orders":      True,
            "generated_at":        datetime.now().isoformat(),
            "provider_health":     {},
            "cache_stats":         {},
            "token_status":        {},
            "diagnostics_records": [],
            "warnings":            [],
        }

        # Provider health
        try:
            from data.providers.provider_health import ProviderHealthChecker
            checker = ProviderHealthChecker()
            health  = checker.run_all()
            result["provider_health"] = health
        except Exception as exc:
            result["warnings"].append(f"provider_health: {exc}")

        # Cache stats
        try:
            from data.providers.api_cache import APICache
            cache = APICache()
            result["cache_stats"] = cache.stats()
        except Exception as exc:
            result["warnings"].append(f"api_cache: {exc}")

        # Token status
        try:
            from data.providers.token_setup_assistant import TokenSetupAssistant
            assistant = TokenSetupAssistant()
            result["token_status"] = assistant.check_required_tokens()
        except Exception as exc:
            result["warnings"].append(f"token_setup: {exc}")

        return result

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> dict:
        """
        Generate API fetch production report.
        Returns {"ok": bool, "report_path": str, "error": str}.
        """
        try:
            # Gather inputs
            token_status    = None
            cache_stats     = None
            lineage_summary = None
            diag_summary    = None
            parser_health   = {}

            try:
                from data.providers.token_setup_assistant import TokenSetupAssistant
                token_status = TokenSetupAssistant().inspect()
            except Exception as exc:
                logger.debug("generate_report: token_setup: %s", exc)

            try:
                from data.providers.api_cache import APICache
                cache_stats = APICache().stats()
            except Exception as exc:
                logger.debug("generate_report: api_cache: %s", exc)

            try:
                from data.providers.api_diagnostics import APIFetchDiagnostics
                diag = APIFetchDiagnostics()
                diag_summary = diag.summarize()
            except Exception as exc:
                logger.debug("generate_report: api_diagnostics: %s", exc)

            try:
                from data.providers.twse_tpex_parser import TWSETPEXParser
                parser_health["twse_tpex"] = {"schema_status": "OK", "timing_quality": "—"}
            except Exception as exc:
                parser_health["twse_tpex"] = {"schema_status": f"IMPORT_ERROR: {exc}"}

            try:
                from data.providers.mops_financial_parser import MOPSFinancialParser
                parser_health["mops"] = {"schema_status": "OK", "timing_quality": "—"}
            except Exception as exc:
                parser_health["mops"] = {"schema_status": f"IMPORT_ERROR: {exc}"}

            from reports.api_fetch_production_report import APIFetchProductionReportBuilder
            builder = APIFetchProductionReportBuilder(report_dir=self._report_dir, mode=mode)
            path = builder.build(
                token_status=token_status,
                diagnostics=diag_summary,
                cache_stats=cache_stats,
                lineage_summary=lineage_summary,
                parser_health=parser_health,
            )
            return {"ok": True, "report_path": path, "error": None}

        except Exception as exc:
            logger.warning("APIFetchStatusAdapter.generate_report: %s", exc)
            return {"ok": False, "report_path": None, "error": str(exc)}

    # ------------------------------------------------------------------
    # Cache
    # ------------------------------------------------------------------

    def cache_stats(self) -> dict:
        """Return current cache statistics."""
        try:
            from data.providers.api_cache import APICache
            return APICache().stats()
        except Exception as exc:
            return {"enabled": False, "error": str(exc)}

    def cleanup_expired_cache(self) -> dict:
        """Remove expired cache entries. Returns count."""
        try:
            from data.providers.api_cache import APICache
            cache   = APICache()
            removed = cache.cleanup_expired()
            return {"ok": True, "removed": removed}
        except Exception as exc:
            return {"ok": False, "removed": 0, "error": str(exc)}

    # ------------------------------------------------------------------
    # Latest report
    # ------------------------------------------------------------------

    def load_latest_report_path(self) -> Optional[str]:
        """Find the most recent api_fetch_production_report_*.md in report_dir."""
        if not os.path.isdir(self._report_dir):
            return None
        try:
            files = [
                f for f in os.listdir(self._report_dir)
                if f.startswith("api_fetch_production_report_") and f.endswith(".md")
            ]
            if not files:
                return None
            files.sort(reverse=True)
            return os.path.join(self._report_dir, files[0])
        except Exception as exc:
            logger.debug("load_latest_report_path: %s", exc)
            return None
