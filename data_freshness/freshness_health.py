"""
data_freshness/freshness_health.py — Health check suite for Data Freshness Monitor v1.1.3.
[!] Research Only. No Real Orders.
[!] Health checks are read-only diagnostics — no repair triggered.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Safety invariants
NO_REAL_ORDERS  = True
RESEARCH_ONLY   = True

_STATUS_PASS = "PASS"
_STATUS_WARN = "WARN"
_STATUS_FAIL = "FAIL"


class DataFreshnessHealthCheck:
    """
    Health check suite for the data_freshness package.

    Checks package imports, safety invariants, SLA configuration,
    detector availability, and git-ignore compliance.

    [!] Read-only — does not modify data or trigger repair.
    """

    def run(self) -> Dict[str, Any]:
        """
        Run all health checks.

        Returns dict:
          checks: list of {check, status, detail}
          total:  total check count
          passed: PASS count
          warned: WARN count
          failed: FAIL count
          overall: "PASS" | "WARN" | "FAIL"
        """
        checks: List[Dict[str, str]] = []

        checks.append(self._check_package_import())
        checks.append(self._check_trading_calendar())
        checks.append(self._check_approximate_calendar_warning())
        checks.append(self._check_policy_available())
        checks.append(self._check_daily_sla())
        checks.append(self._check_monthly_sla())
        checks.append(self._check_quarterly_sla())
        checks.append(self._check_detector_available())
        checks.append(self._check_source_monitor_available())
        checks.append(self._check_prioritizer_available())
        checks.append(self._check_future_date_not_fresh())
        checks.append(self._check_date_regression_detection())
        checks.append(self._check_mock_formal_freshness_disabled())
        checks.append(self._check_auto_external_refresh_disabled())
        checks.append(self._check_stale_auto_repair_disabled())
        checks.append(self._check_coverage_repair_handoff_available())
        checks.append(self._check_store_output_ignored())
        checks.append(self._check_no_broker_execution())
        checks.append(self._check_no_forbidden_actions())

        total  = len(checks)
        passed = sum(1 for c in checks if c["status"] == _STATUS_PASS)
        warned = sum(1 for c in checks if c["status"] == _STATUS_WARN)
        failed = sum(1 for c in checks if c["status"] == _STATUS_FAIL)

        if failed > 0:
            overall = "FAIL"
        elif warned > 0:
            overall = "WARN"
        else:
            overall = "PASS"

        return {
            "checks": checks,
            "total": total,
            "passed": passed,
            "warned": warned,
            "failed": failed,
            "overall": overall,
        }

    def print_health(self) -> None:
        """Print formatted health check output."""
        result = self.run()
        print("")
        print("=" * 60)
        print("  Data Freshness Monitor — Health Check  (v1.1.3)")
        print("  [!] Research Only. No Real Orders.")
        print("=" * 60)
        for c in result["checks"]:
            icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}.get(
                c["status"], "[????]"
            )
            print(f"  {icon}  {c['check']:<42}  {c['detail']}")
        print("-" * 60)
        print(
            f"  Total: {result['total']}  |  "
            f"Passed: {result['passed']}  |  "
            f"Warned: {result['warned']}  |  "
            f"Failed: {result['failed']}"
        )
        print(f"  Overall: {result['overall']}")
        print("=" * 60)
        print("")

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def _check_package_import(self) -> Dict[str, str]:
        check = "package_import"
        try:
            import data_freshness  # type: ignore  # noqa: F401
            return {"check": check, "status": _STATUS_PASS, "detail": "data_freshness imported OK"}
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Import failed: {exc}"}

    def _check_trading_calendar(self) -> Dict[str, str]:
        check = "trading_calendar"
        try:
            from data_freshness.trading_calendar import TradingCalendar
            cal = TradingCalendar()
            _ = cal.expected_latest_trading_day()
            return {"check": check, "status": _STATUS_PASS, "detail": "TradingCalendar instantiated OK"}
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_approximate_calendar_warning(self) -> Dict[str, str]:
        check = "approximate_calendar_warning"
        try:
            from data_freshness.trading_calendar import TradingCalendar
            cal = TradingCalendar()
            if cal.is_approximate():
                return {
                    "check": check,
                    "status": _STATUS_WARN,
                    "detail": (
                        "No holidays loaded — calendar is approximate (weekday heuristic). "
                        "Do NOT claim precise SLA compliance."
                    ),
                }
            return {
                "check": check,
                "status": _STATUS_PASS,
                "detail": "Holiday list loaded; calendar is non-approximate",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_policy_available(self) -> Dict[str, str]:
        check = "policy_available"
        try:
            from data_freshness.freshness_policy import FreshnessPolicy
            policy = FreshnessPolicy()
            _ = policy.get_policy("DAILY_PRICE")
            return {"check": check, "status": _STATUS_PASS, "detail": "FreshnessPolicy instantiated OK"}
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_daily_sla(self) -> Dict[str, str]:
        check = "daily_sla"
        try:
            from data_freshness.freshness_policy import FreshnessPolicy
            from data_freshness.freshness_schema import DATASET_DAILY_PRICE, DATASET_VOLUME
            policy = FreshnessPolicy()
            p1 = policy.get_policy(DATASET_DAILY_PRICE)
            p2 = policy.get_policy(DATASET_VOLUME)
            if p1.get("freq") == "daily" and p2.get("freq") == "daily":
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "DAILY_PRICE and VOLUME have freq=daily",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": f"Unexpected freq: DAILY_PRICE={p1.get('freq')}, VOLUME={p2.get('freq')}",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_monthly_sla(self) -> Dict[str, str]:
        check = "monthly_sla"
        try:
            from data_freshness.freshness_policy import FreshnessPolicy
            from data_freshness.freshness_schema import DATASET_REVENUE
            policy = FreshnessPolicy()
            p = policy.get_policy(DATASET_REVENUE)
            if p.get("freq") == "monthly":
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "REVENUE has freq=monthly",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": f"REVENUE freq={p.get('freq')} (expected monthly)",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_quarterly_sla(self) -> Dict[str, str]:
        check = "quarterly_sla"
        try:
            from data_freshness.freshness_policy import FreshnessPolicy
            from data_freshness.freshness_schema import DATASET_FUNDAMENTALS
            policy = FreshnessPolicy()
            p = policy.get_policy(DATASET_FUNDAMENTALS)
            if p.get("freq") == "quarterly":
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "FUNDAMENTALS has freq=quarterly",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": f"FUNDAMENTALS freq={p.get('freq')} (expected quarterly)",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_detector_available(self) -> Dict[str, str]:
        check = "detector_available"
        try:
            from data_freshness.freshness_detector import DataFreshnessDetector
            det = DataFreshnessDetector()
            return {"check": check, "status": _STATUS_PASS, "detail": "DataFreshnessDetector instantiated OK"}
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_source_monitor_available(self) -> Dict[str, str]:
        check = "source_monitor_available"
        try:
            from data_freshness.source_monitor import DataSourceFreshnessMonitor
            mon = DataSourceFreshnessMonitor()
            return {
                "check": check,
                "status": _STATUS_PASS,
                "detail": "DataSourceFreshnessMonitor instantiated OK",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_prioritizer_available(self) -> Dict[str, str]:
        check = "prioritizer_available"
        try:
            from data_freshness.freshness_prioritizer import FreshnessPrioritizer
            pri = FreshnessPrioritizer()
            return {
                "check": check,
                "status": _STATUS_PASS,
                "detail": "FreshnessPrioritizer instantiated OK",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_future_date_not_fresh(self) -> Dict[str, str]:
        check = "future_date_not_fresh"
        try:
            from data_freshness.freshness_detector import DataFreshnessDetector
            from data_freshness.freshness_schema import STATUS_FUTURE_DATE, STATUS_FRESH

            det = DataFreshnessDetector()
            # Use a date 10 years in the future
            future = datetime.now(timezone.utc).date() + timedelta(days=3650)
            is_future = det.detect_future_date(future)
            if not is_future:
                return {
                    "check": check,
                    "status": _STATUS_FAIL,
                    "detail": f"detect_future_date({future}) returned False — should be True",
                }
            # Build a record and check status
            rec = det.build_record(
                symbol="TEST",
                tier="test",
                dataset="DAILY_PRICE",
                source="test",
                actual_date=future,
            )
            if rec.status == STATUS_FUTURE_DATE and rec.status != STATUS_FRESH:
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": f"Future date {future} correctly classified as FUTURE_DATE (not FRESH)",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": f"Future date classified as {rec.status} — expected FUTURE_DATE",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_date_regression_detection(self) -> Dict[str, str]:
        check = "date_regression_detection"
        try:
            from data_freshness.freshness_detector import DataFreshnessDetector

            det = DataFreshnessDetector()
            today = datetime.now(timezone.utc).date()
            yesterday = today - timedelta(days=1)

            # Manually seed history cache so detect_date_regression can compare
            det._history_cache["REGTEST::DAILY_PRICE"] = today
            result = det.detect_date_regression("REGTEST", "DAILY_PRICE", yesterday)

            if result is True:
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "detect_date_regression correctly returns True when actual < previous",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": (
                    f"detect_date_regression returned {result} for "
                    f"actual={yesterday} < previous={today}"
                ),
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_mock_formal_freshness_disabled(self) -> Dict[str, str]:
        check = "mock_formal_freshness_disabled"
        try:
            import data_freshness
            val = getattr(data_freshness, "MOCK_DATA_FORMAL_FRESHNESS_ALLOWED", None)
            if val is False:
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "MOCK_DATA_FORMAL_FRESHNESS_ALLOWED=False confirmed",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": f"MOCK_DATA_FORMAL_FRESHNESS_ALLOWED={val!r} (expected False)",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_auto_external_refresh_disabled(self) -> Dict[str, str]:
        check = "auto_external_refresh_disabled"
        try:
            import data_freshness
            val = getattr(data_freshness, "AUTO_EXTERNAL_REFRESH_ENABLED", None)
            if val is False:
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "AUTO_EXTERNAL_REFRESH_ENABLED=False confirmed",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": f"AUTO_EXTERNAL_REFRESH_ENABLED={val!r} (expected False)",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_stale_auto_repair_disabled(self) -> Dict[str, str]:
        check = "stale_auto_repair_disabled"
        try:
            import data_freshness
            val = getattr(data_freshness, "STALE_DATA_AUTO_REPAIR_ENABLED", None)
            if val is False:
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "STALE_DATA_AUTO_REPAIR_ENABLED=False confirmed",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": f"STALE_DATA_AUTO_REPAIR_ENABLED={val!r} (expected False)",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_coverage_repair_handoff_available(self) -> Dict[str, str]:
        check = "coverage_repair_handoff_available"
        try:
            import coverage_repair  # type: ignore  # noqa: F401
            return {
                "check": check,
                "status": _STATUS_PASS,
                "detail": "coverage_repair package imported OK",
            }
        except ImportError:
            return {
                "check": check,
                "status": _STATUS_WARN,
                "detail": "coverage_repair package not importable (repair handoff will be dict-only)",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_WARN, "detail": f"Import warning: {exc}"}

    def _check_store_output_ignored(self) -> Dict[str, str]:
        check = "store_output_ignored"
        try:
            import os

            # Attempt to find .gitignore
            here = os.path.abspath(__file__)
            repo_root = os.path.dirname(os.path.dirname(here))
            gitignore_path = os.path.join(repo_root, ".gitignore")

            if not os.path.isfile(gitignore_path):
                return {
                    "check": check,
                    "status": _STATUS_WARN,
                    "detail": ".gitignore not found — verify data/freshness_reports/ is excluded",
                }

            with open(gitignore_path, encoding="utf-8", errors="replace") as f:
                content = f.read()

            if "freshness_reports" in content or "data/freshness_reports" in content:
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "data/freshness_reports/ found in .gitignore",
                }
            return {
                "check": check,
                "status": _STATUS_WARN,
                "detail": (
                    "data/freshness_reports/ NOT found in .gitignore — "
                    "add it to prevent committing runtime outputs"
                ),
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_WARN, "detail": f"Could not verify: {exc}"}

    def _check_no_broker_execution(self) -> Dict[str, str]:
        check = "no_broker_execution"
        try:
            import data_freshness
            val = getattr(data_freshness, "BROKER_DISABLED", None)
            if val is True:
                return {
                    "check": check,
                    "status": _STATUS_PASS,
                    "detail": "BROKER_DISABLED=True confirmed",
                }
            return {
                "check": check,
                "status": _STATUS_FAIL,
                "detail": f"BROKER_DISABLED={val!r} (expected True)",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_FAIL, "detail": f"Failed: {exc}"}

    def _check_no_forbidden_actions(self) -> Dict[str, str]:
        check = "no_forbidden_actions"
        try:
            import os
            import re

            # Trading action patterns that must NOT appear in module code.
            # These are action-verb patterns, not safety disclaimer phrases.
            # Safety disclaimers like "No Real Orders" / "no_real_orders" are acceptable.
            # We look for executable trading calls, not documentation strings.
            forbidden_patterns = [
                r"\bplace_order\s*\(",
                r"\bsubmit_order\s*\(",
                r"\bexecute_trade\s*\(",
                r"\bsend_order\s*\(",
                r"\bbuy_stock\s*\(",
                r"\bsell_stock\s*\(",
                r"\bmarket_order\s*\(",
                r"\blimit_order\s*\(",
            ]
            violations: List[str] = []

            pkg_dir = os.path.dirname(os.path.abspath(__file__))
            for fname in os.listdir(pkg_dir):
                if not fname.endswith(".py"):
                    continue
                fpath = os.path.join(pkg_dir, fname)
                try:
                    with open(fpath, encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    for pattern in forbidden_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            violations.append(f"{fname}: matches pattern '{pattern}'")
                except Exception:
                    pass

            if violations:
                return {
                    "check": check,
                    "status": _STATUS_FAIL,
                    "detail": "; ".join(violations[:3]),
                }
            return {
                "check": check,
                "status": _STATUS_PASS,
                "detail": "No executable trading action calls found in package modules",
            }
        except Exception as exc:
            return {"check": check, "status": _STATUS_WARN, "detail": f"Check incomplete: {exc}"}
