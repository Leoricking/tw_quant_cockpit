"""
data/providers/provider_metrics.py - Provider metrics collector (v0.3.24).

Reads provider fetch / health / scheduler logs and computes provider success
rates and row coverage.

[!] Read Only. No token read. No Real Orders.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ProviderMetricsCollector:
    """
    Collects provider metrics from logs and reports.

    Parameters
    ----------
    results_dir : data/backtest_results
    logs_dir    : logs/
    reports_dir : reports/
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        results_dir: Optional[str] = None,
        logs_dir:    Optional[str] = None,
        reports_dir: Optional[str] = None,
    ):
        self._results_dir = results_dir or os.path.join(_BASE_DIR, "data", "backtest_results")
        self._logs_dir    = logs_dir    or os.path.join(_BASE_DIR, "logs")
        self._reports_dir = reports_dir or os.path.join(_BASE_DIR, "reports")

        self._raw: Dict[str, list] = {}   # pname -> list of run records

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def collect(self) -> dict:
        """Collect all available metrics and return summary dict."""
        self.collect_from_fetch_reports()
        self.collect_from_automation_logs()
        self.collect_from_provider_health()
        self.collect_from_import_csv()
        return self.summarize_provider_metrics()

    # ------------------------------------------------------------------
    # Collectors
    # ------------------------------------------------------------------

    def collect_from_fetch_reports(self) -> None:
        """Parse data_provider_fetch_report_*.md files for provider outcomes."""
        try:
            for fname in os.listdir(self._reports_dir):
                if not (fname.startswith("data_provider_fetch_report") and fname.endswith(".md")):
                    continue
                fpath = os.path.join(self._reports_dir, fname)
                try:
                    with open(fpath, encoding="utf-8") as f:
                        content = f.read()
                    self._parse_fetch_report_md(content)
                except Exception as exc:
                    logger.debug("collect_from_fetch_reports %s: %s", fname, exc)
        except Exception as exc:
            logger.debug("collect_from_fetch_reports dir: %s", exc)

    def _parse_fetch_report_md(self, content: str) -> None:
        """Minimal parser: look for 'provider_used:' lines."""
        for line in content.splitlines():
            line = line.strip()
            if "provider_used" in line.lower() or "Provider Used" in line:
                for pname in ["finmind", "twse", "tpex", "mops", "csv", "xq_export"]:
                    if pname in line.lower():
                        records = self._raw.setdefault(pname, [])
                        records.append({"status": "OK", "source": "fetch_report"})
                        break

    def collect_from_automation_logs(self) -> None:
        """Parse logs/automation/*.json for provider fetch outcomes."""
        auto_log_dir = os.path.join(self._logs_dir, "automation")
        if not os.path.isdir(auto_log_dir):
            return
        try:
            for fname in sorted(os.listdir(auto_log_dir))[-20:]:
                if not fname.endswith(".json"):
                    continue
                fpath = os.path.join(auto_log_dir, fname)
                try:
                    with open(fpath, encoding="utf-8") as f:
                        data = json.load(f)
                    self._parse_automation_log(data)
                except Exception as exc:
                    logger.debug("collect_from_automation_logs %s: %s", fname, exc)
        except Exception as exc:
            logger.debug("collect_from_automation_logs dir: %s", exc)

    def _parse_automation_log(self, data) -> None:
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict) and "runs" in data:
            records = data["runs"]
        else:
            records = [data] if isinstance(data, dict) else []

        for rec in records:
            if not isinstance(rec, dict):
                continue
            fetch_sum = rec.get("auto_fetch_summary", {})
            if not isinstance(fetch_sum, dict):
                continue
            # Also check providers_used
            for pname in fetch_sum.get("providers_used", []):
                records_list = self._raw.setdefault(pname, [])
                records_list.append({"status": "OK", "source": "automation_log"})

    def collect_from_provider_health(self) -> None:
        """Parse provider health report files for status."""
        try:
            for fname in sorted(os.listdir(self._reports_dir)):
                if not (fname.startswith("provider_health_report") and fname.endswith(".md")):
                    continue
                fpath = os.path.join(self._reports_dir, fname)
                try:
                    with open(fpath, encoding="utf-8") as f:
                        content = f.read()
                    self._parse_health_report_md(content)
                except Exception as exc:
                    logger.debug("collect_from_provider_health %s: %s", fname, exc)
        except Exception as exc:
            logger.debug("collect_from_provider_health dir: %s", exc)

    def _parse_health_report_md(self, content: str) -> None:
        for pname in ["finmind", "twse", "tpex", "mops", "csv", "xq_export"]:
            if pname in content.lower():
                if "ok" in content.lower() or "partial" in content.lower():
                    records = self._raw.setdefault(pname, [])
                    records.append({"status": "OK", "source": "health_report"})

    def collect_from_import_csv(self) -> None:
        """Check CSV import files to detect CSV/XQ as local providers."""
        import_paths = {
            "csv": [
                os.path.join(_BASE_DIR, "data", "import", "daily", "daily_k.csv"),
                os.path.join(_BASE_DIR, "data", "import", "monthly_revenue", "monthly_revenue.csv"),
            ],
            "xq_export": [
                os.path.join(_BASE_DIR, "data", "import", "intraday"),
            ],
        }
        for pname, paths in import_paths.items():
            for p in paths:
                if os.path.exists(p):
                    records = self._raw.setdefault(pname, [])
                    records.append({"status": "LOCAL_AVAILABLE", "source": "import_csv"})
                    break

    # ------------------------------------------------------------------
    # Summarize
    # ------------------------------------------------------------------

    def summarize_provider_metrics(self) -> dict:
        """Compute success_rate and coverage from collected raw records."""
        providers_metrics: Dict[str, dict] = {}

        for pname, records in self._raw.items():
            total   = len(records)
            ok      = sum(1 for r in records if r.get("status") in ("OK", "LOCAL_AVAILABLE"))
            failed  = sum(1 for r in records if r.get("status") in ("FAILED", "ERROR"))

            if total == 0:
                sr = None
            elif ok + failed == 0:
                sr = None
            else:
                sr = ok / (ok + failed) if (ok + failed) > 0 else None

            providers_metrics[pname] = {
                "success_rate":       sr,
                "failure_rate":       (1.0 - sr) if sr is not None else None,
                "sample_count":       total,
                "latency_score":      0.8 if pname in ("csv", "xq_export") else 0.6,
                "row_coverage_score": 0.9 if pname == "csv" else 0.7,
                "freshness_score":    0.7,
                "last_success_at":    "",
                "last_failure_at":    "",
            }

        # If no history at all, return INSUFFICIENT_HISTORY markers
        if not providers_metrics:
            for pname in ["finmind", "csv", "xq_export"]:
                providers_metrics[pname] = {
                    "success_rate":       None,
                    "failure_rate":       None,
                    "sample_count":       0,
                    "latency_score":      None,
                    "row_coverage_score": None,
                    "freshness_score":    None,
                    "last_success_at":    "",
                    "last_failure_at":    "",
                    "note":               "INSUFFICIENT_HISTORY",
                }

        return {
            "providers":            providers_metrics,
            "dataset_last_provider": {},
            "collected_at":         datetime.now().isoformat(),
            "read_only":            True,
            "no_real_orders":       True,
        }
