"""
reports/finmind_adapter_report.py — FinMind Adapter Report v1.4.4.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SECONDARY_AGGREGATOR. Cannot override TWSE/TPEx/MOPS.
[!] No token in report. formal_use_allowed=False by default.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FINMIND_MOCK_FALLBACK_ENABLED = False
FINMIND_AUTO_DOWNLOAD_ENABLED = False
FINMIND_AUTO_DISCOVERY_ENABLED = False
FINMIND_DATASET_ALLOWLIST_REQUIRED = True
FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER = False


class FinMindAdapterReport:
    """
    Builds FinMind Adapter Report v1.4.4 in Markdown.

    Sections:
    1. Overview
    2. Authentication
    3. Quota
    4. Dataset Registry
    5. Requests
    6. Schema Drift
    7. Primary Comparison
    8. Point-in-Time
    9. Data Quality
    10. Freshness
    11. Safety
    12. Known Limitations
    """

    REPORT_TITLE = "FinMind Adapter Report"
    REPORT_VERSION = "v1.4.4"

    def __init__(
        self,
        report_date: Optional[str] = None,
        mode: str = "real",
        health_data: Optional[dict] = None,
        allowlist_data: Optional[dict] = None,
    ) -> None:
        self._report_date = report_date or datetime.now().strftime("%Y-%m-%d")
        self._mode = mode
        self._health_data = health_data
        self._allowlist_data = allowlist_data

    def _get_health(self) -> Dict[str, Any]:
        if self._health_data is not None:
            return self._health_data
        try:
            from data.providers.finmind.health_v144 import FinMindAdapterHealthCheck
            return FinMindAdapterHealthCheck().get_health_summary()
        except Exception as exc:
            return {"error": str(exc)}

    def _get_allowlist(self) -> Dict[str, Any]:
        if self._allowlist_data is not None:
            return self._allowlist_data
        try:
            from data.providers.finmind.datasets_v144 import FinMindDatasetAllowlist
            return FinMindDatasetAllowlist().summary()
        except Exception as exc:
            return {"error": str(exc)}

    def _get_auth(self) -> Dict[str, Any]:
        try:
            from data.providers.finmind.auth_v144 import FinMindAuthManager
            return FinMindAuthManager().get_auth_summary()
        except Exception as exc:
            return {"error": str(exc)}

    def _get_quota(self) -> Dict[str, Any]:
        try:
            from data.providers.finmind.quota_v144 import FinMindQuotaManager
            state = FinMindQuotaManager().get_status()
            return {"status": state.status.value, "plan_unknown": state.plan_unknown}
        except Exception as exc:
            return {"error": str(exc)}

    def render(self) -> str:
        lines: List[str] = []
        health = self._get_health()
        allowlist = self._get_allowlist()
        auth = self._get_auth()
        quota = self._get_quota()

        lines += self._section_overview(health)
        lines += self._section_authentication(auth)
        lines += self._section_quota(quota)
        lines += self._section_dataset_registry(allowlist)
        lines += self._section_requests()
        lines += self._section_schema_drift()
        lines += self._section_primary_comparison()
        lines += self._section_point_in_time()
        lines += self._section_data_quality()
        lines += self._section_freshness()
        lines += self._section_safety()
        lines += self._section_known_limitations()

        return "\n".join(lines)

    def _section_overview(self, health: dict) -> List[str]:
        status = health.get("provider_status", "UNKNOWN")
        passed = health.get("passed", "?")
        failed = health.get("failed", "?")
        total = health.get("total", "?")
        return [
            f"# {self.REPORT_TITLE} {self.REPORT_VERSION}",
            "",
            f"> **Report Date:** {self._report_date}  ",
            f"> **Mode:** {self._mode}  ",
            f"> **Version:** {self.REPORT_VERSION}",
            "",
            "## 1. Overview",
            "",
            f"- Provider: `finmind`",
            f"- Authoritative Level: `SECONDARY_AGGREGATOR`",
            f"- Official: `False`",
            f"- Health Status: `{status}`",
            f"- Health Checks: {passed}/{total} passed, {failed} failed",
            f"- Can Override Primary: `False`",
            f"- No Real Orders: `True`",
            "",
            "> **[!] Research Only. No Real Orders. Not Investment Advice.**",
            "> **[!] SECONDARY_AGGREGATOR — cannot override TWSE/TPEx/MOPS primary sources.**",
            "",
        ]

    def _section_authentication(self, auth: dict) -> List[str]:
        return [
            "## 2. Authentication",
            "",
            f"- Token Present: `{auth.get('token_present', False)}`",
            f"- Token Source: `{auth.get('token_source', 'N/A')}`",
            f"- Token Fingerprint: `{auth.get('token_fingerprint', 'N/A')}` (first 8 chars of SHA256 only)",
            f"- Anonymous Mode: `{auth.get('anonymous_mode', True)}`",
            f"- Token Optional: `{auth.get('token_optional', True)}`",
            f"- Token Storage Secure: `{auth.get('token_storage_secure', True)}`",
            "",
            "> **[!] Token value never stored in report. Set FINMIND_API_TOKEN env var.**",
            "",
        ]

    def _section_quota(self, quota: dict) -> List[str]:
        return [
            "## 3. Quota",
            "",
            f"- Quota Status: `{quota.get('status', 'UNKNOWN')}`",
            f"- Plan Unknown: `{quota.get('plan_unknown', True)}`",
            "",
            "> **[!] EXHAUSTED → stop non-essential prefetch, no retry, no token rotation, no mock fallback.**",
            "",
        ]

    def _section_dataset_registry(self, allowlist: dict) -> List[str]:
        return [
            "## 4. Dataset Registry",
            "",
            f"- Total Datasets: `{allowlist.get('total', '?')}`",
            f"- Supported: `{allowlist.get('supported', '?')}`",
            f"- Wildcard Allowed: `{allowlist.get('wildcard_allowlist_enabled', False)}`",
            f"- Auto-Approve: `{allowlist.get('auto_approve_enabled', False)}`",
            f"- Auto-Discovery: `{allowlist.get('auto_discovery_enabled', False)}`",
            f"- Formal Use Policy: `{allowlist.get('formal_use_policy', 'BLOCKED_BY_DEFAULT')}`",
            "",
        ]

    def _section_requests(self) -> List[str]:
        return [
            "## 5. Requests",
            "",
            "- API Version: `v4`",
            "- Base URL: `https://api.finmindtrade.com/api/v4/data`",
            "- Injectable transport: available for offline tests",
            "- Dry-run default: `True`",
            "",
            "> **[!] FINMIND_AUTO_DOWNLOAD_ENABLED=False. Manual execute required.**",
            "",
        ]

    def _section_schema_drift(self) -> List[str]:
        return [
            "## 6. Schema Drift",
            "",
            "- Schema drift detection: available",
            "- Additive drift: WARN (not blocking)",
            "- Missing required field: BLOCKING",
            "- Type change: BLOCKING",
            "- Key change: BLOCKING",
            "",
        ]

    def _section_primary_comparison(self) -> List[str]:
        return [
            "## 7. Primary Comparison",
            "",
            "- Primary source always wins conflict",
            "- FinMind data preserved as secondary evidence",
            "- No auto-repair",
            "- Conflicts logged for review",
            "",
            "> **[!] can_override_primary_provider = False**",
            "",
        ]

    def _section_point_in_time(self) -> List[str]:
        return [
            "## 8. Point-in-Time",
            "",
            "- All FinMind daily datasets: `DATE_ONLY`",
            "- UNKNOWN PIT class: formal historical conclusion blocked",
            "- Never infer minute-level PIT from daily data",
            "",
        ]

    def _section_data_quality(self) -> List[str]:
        return [
            "## 9. Data Quality",
            "",
            "- Authority: `SECONDARY_AGGREGATOR`",
            "- Source: `finmind`",
            "- Formal conclusion requires primary source validation",
            "- mock_formal_conclusion_allowed: `False`",
            "",
        ]

    def _section_freshness(self) -> List[str]:
        return [
            "## 10. Freshness",
            "",
            "- Daily OHLCV TTL: 24 hours",
            "- Monthly Revenue TTL: 7 days",
            "- Financial Statements TTL: 30 days",
            "- Stale cache: flagged as stale, not returned as fresh",
            "",
        ]

    def _section_safety(self) -> List[str]:
        return [
            "## 11. Safety Invariants",
            "",
            "| Invariant | Value |",
            "| --- | --- |",
            "| NO_REAL_ORDERS | True |",
            "| BROKER_EXECUTION_ENABLED | False |",
            "| PRODUCTION_TRADING_BLOCKED | True |",
            "| can_override_primary_provider | False |",
            "| silent_fallback_enabled | False |",
            "| mock_fallback_enabled | False |",
            "| auto_download_enabled | False |",
            "| auto_discovery_enabled | False |",
            "| realtime_formal_use_allowed | False |",
            "| broker_execution_available | False |",
            "| token_in_report | NEVER |",
            "",
        ]

    def _section_known_limitations(self) -> List[str]:
        return [
            "## 12. Known Limitations",
            "",
            "- FinMind plan limits are unknown until API response — plan_unknown=True by default",
            "- DATE_ONLY PIT class: no intraday precision",
            "- SECONDARY_AGGREGATOR: formal conclusions require primary source cross-check",
            "- Token is optional but recommended for higher quota limits",
            "- Wide institutional format is EXPERIMENTAL status",
            "- Not all FinMind datasets are in the allowlist — only explicitly approved ones",
            "",
            "---",
            "",
            f"*Generated by {self.REPORT_TITLE} {self.REPORT_VERSION} on {self._report_date}.*  ",
            "*[!] Research Only. No Real Orders. Not Investment Advice.*",
            "",
        ]
