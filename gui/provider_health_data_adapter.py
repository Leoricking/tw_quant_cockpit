"""
gui/provider_health_data_adapter.py - Data adapter for Provider Health GUI (v0.3.18).

Bridges ProviderHealthChecker / ProviderHealthReportBuilder to the GUI panel.
No subprocess usage. No real token display. No order placement.

[!] Read Only. No Real Orders.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProviderHealthDataAdapter:
    """
    Adapter that the GUI uses to get provider health data and run reports.

    Parameters
    ----------
    env_path   : Path to .env file (default: project root .env)
    report_dir : Directory for report output (default: reports/)
    """

    def __init__(
        self,
        env_path:   Optional[str] = None,
        report_dir: Optional[str] = None,
    ):
        self._env_path  = env_path  or os.path.join(_BASE_DIR, ".env")
        self._report_dir = report_dir or os.path.join(_BASE_DIR, "reports")

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    def run_health_check(self) -> dict:
        """
        Run provider health check and return results dict.
        Never raises — returns error info on failure.
        """
        try:
            from data.providers.provider_health import ProviderHealthChecker
            checker = ProviderHealthChecker(env_path=self._env_path)
            result = checker.run_all()
            result["error"] = None
            return result
        except Exception as exc:
            logger.error("ProviderHealthDataAdapter.run_health_check failed: %s", exc)
            return {
                "checked_at":          datetime.now().isoformat(),
                "providers":           [],
                "summary":             {},
                "token_status":        {},
                "read_only_guarantee": True,
                "no_real_orders":      True,
                "error":               str(exc),
            }

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> dict:
        """
        Run health check and generate a Markdown report.
        Returns {"path": str, "error": str or None}.
        """
        try:
            health_data = self.run_health_check()
            if health_data.get("error"):
                return {"path": None, "error": health_data["error"]}

            from reports.provider_health_report import ProviderHealthReportBuilder
            builder = ProviderHealthReportBuilder(
                report_date=datetime.now().strftime("%Y-%m-%d"),
                mode=mode,
                health_data=health_data,
            )
            path = builder.build(output_dir=self._report_dir)
            return {"path": path, "error": None}
        except Exception as exc:
            logger.error("ProviderHealthDataAdapter.generate_report failed: %s", exc)
            return {"path": None, "error": str(exc)}

    # ------------------------------------------------------------------
    # .env.example creation
    # ------------------------------------------------------------------

    def create_env_example(self, path: Optional[str] = None) -> dict:
        """
        Create a safe .env.example file.
        Returns {"path": str, "error": str or None}.
        Never writes to real .env.
        """
        target = path or os.path.join(_BASE_DIR, ".env.example")
        try:
            from data.providers.token_safe_config import TokenSafeConfig
            cfg = TokenSafeConfig(env_path=self._env_path)
            written = cfg.create_env_example(path=target)
            return {"path": written, "error": None}
        except Exception as exc:
            logger.error("ProviderHealthDataAdapter.create_env_example failed: %s", exc)
            return {"path": None, "error": str(exc)}

    # ------------------------------------------------------------------
    # Latest report path
    # ------------------------------------------------------------------

    def load_latest_report_path(self) -> Optional[str]:
        """Return path of the most recent provider health report, or None."""
        try:
            import glob
            pattern = os.path.join(self._report_dir, "provider_health_report_*.md")
            files = sorted(glob.glob(pattern))
            return files[-1] if files else None
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Registry info
    # ------------------------------------------------------------------

    def get_capability_matrix(self) -> dict:
        """Return capability matrix from ProviderRegistry."""
        try:
            from data.providers.provider_registry import ProviderRegistry
            reg = ProviderRegistry()
            return reg.get_readonly_capabilities()
        except Exception as exc:
            logger.debug("get_capability_matrix failed: %s", exc)
            return {}

    def get_provider_list(self) -> list:
        """Return list of all registered providers."""
        try:
            from data.providers.provider_registry import ProviderRegistry
            reg = ProviderRegistry()
            return reg.list_providers()
        except Exception as exc:
            logger.debug("get_provider_list failed: %s", exc)
            return []
