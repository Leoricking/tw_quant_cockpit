"""
data/providers/mops/endpoints_v142.py — MOPS endpoint registry v1.4.2.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] MOPS_REALTIME_AVAILABLE = False. MOPS_BROKER_EXECUTION_AVAILABLE = False.
[!] MOPS_AUTO_DOWNLOAD_ENABLED = False. MOPS_MOCK_FALLBACK_ENABLED = False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from data.providers.mops.models_v142 import MOPSCapability

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_MOPS_BASE = "https://mops.twse.com.tw"


@dataclass
class MOPSEndpoint:
    """Definition of a single MOPS endpoint."""
    endpoint_id: str
    official_name: str
    capability: MOPSCapability
    transport: str
    path: str
    method: str  # GET or POST
    response_format: str  # JSON, HTML, XML
    requires_form_params: bool
    form_params: Dict[str, Any] = field(default_factory=dict)
    expected_fields: List[str] = field(default_factory=list)
    charset: str = "utf-8"
    cache_ttl_seconds: int = 3600
    update_cadence: str = "quarterly"
    supports_history: bool = True
    enabled: bool = True
    official: bool = True
    requires_session_cookie: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class MOPSEndpointRegistry:
    """Registry of all MOPS API endpoints."""

    def __init__(self) -> None:
        self._endpoints: Dict[str, MOPSEndpoint] = {}
        self._register_all()

    def _register_all(self) -> None:
        endpoints = [
            MOPSEndpoint(
                endpoint_id="company_profile",
                official_name="MOPS Company Basic Profile",
                capability=MOPSCapability.COMPANY_PROFILE,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t01sb01",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["公司名稱", "統一編號", "產業類別"],
                charset="utf-8",
                cache_ttl_seconds=86400 * 7,
                update_cadence="annual",
                supports_history=False,
                enabled=True,
                official=True,
                metadata={"note": "Company basic information. POST form required."},
            ),
            MOPSEndpoint(
                endpoint_id="monthly_revenue",
                official_name="MOPS Monthly Revenue",
                capability=MOPSCapability.MONTHLY_REVENUE,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t05st10_ifrs",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["公司代號", "當月營收", "上月比較增減(%)"],
                charset="utf-8",
                cache_ttl_seconds=86400 * 30,
                update_cadence="monthly",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "Monthly revenue disclosure. Revision detection required."},
            ),
            MOPSEndpoint(
                endpoint_id="financial_report_announcement",
                official_name="MOPS Financial Report Filing Announcement",
                capability=MOPSCapability.FINANCIAL_REPORT_ANNOUNCEMENT,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t21sc03",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["公司代號", "申報日期", "報告期間"],
                charset="utf-8",
                cache_ttl_seconds=86400,
                update_cadence="quarterly",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "Financial report filing announcements."},
            ),
            MOPSEndpoint(
                endpoint_id="balance_sheet",
                official_name="MOPS Consolidated Balance Sheet (IFRS)",
                capability=MOPSCapability.BALANCE_SHEET,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t26sb01_ifrs",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["資產總計", "負債總計", "權益總計"],
                charset="utf-8",
                cache_ttl_seconds=86400 * 90,
                update_cadence="quarterly",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "IFRS consolidated balance sheet. Balance check required."},
            ),
            MOPSEndpoint(
                endpoint_id="income_statement",
                official_name="MOPS Consolidated Income Statement (IFRS)",
                capability=MOPSCapability.INCOME_STATEMENT,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t26sb04_ifrs",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["營業收入", "稅後淨利", "每股盈餘"],
                charset="utf-8",
                cache_ttl_seconds=86400 * 90,
                update_cadence="quarterly",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "IFRS consolidated income statement."},
            ),
            MOPSEndpoint(
                endpoint_id="cash_flow",
                official_name="MOPS Cash Flow Statement (IFRS)",
                capability=MOPSCapability.CASH_FLOW,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t26sb07_ifrs",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["營業活動", "投資活動", "籌資活動"],
                charset="utf-8",
                cache_ttl_seconds=86400 * 90,
                update_cadence="quarterly",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "IFRS cash flow statement. Mismatch detection required."},
            ),
            MOPSEndpoint(
                endpoint_id="equity_statement_index",
                official_name="MOPS Equity Statement Index",
                capability=MOPSCapability.EQUITY_STATEMENT_INDEX,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t26sb10_ifrs",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["公司代號", "期間"],
                charset="utf-8",
                cache_ttl_seconds=86400 * 90,
                update_cadence="quarterly",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "Equity statement index (disclosure list only, no inline data)."},
            ),
            MOPSEndpoint(
                endpoint_id="material_information",
                official_name="MOPS Material Information Disclosure",
                capability=MOPSCapability.MATERIAL_INFORMATION,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t36sb01",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["公司代號", "公告日期", "主旨"],
                charset="utf-8",
                cache_ttl_seconds=3600,
                update_cadence="continuous",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "Material information disclosures. Corrections explicitly tracked."},
            ),
            MOPSEndpoint(
                endpoint_id="investor_conference",
                official_name="MOPS Investor Conference Announcements",
                capability=MOPSCapability.INVESTOR_CONFERENCE,
                transport="HTTP/HTML",
                path=f"{_MOPS_BASE}/mops/web/t100sb01",
                method="POST",
                response_format="HTML",
                requires_form_params=True,
                form_params={"encodeURIComponent": "1", "step": "1"},
                expected_fields=["公司代號", "法說會日期", "地點"],
                charset="utf-8",
                cache_ttl_seconds=86400,
                update_cadence="quarterly",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "Investor conference (法說會) announcements."},
            ),
            MOPSEndpoint(
                endpoint_id="xbrl_index",
                official_name="MOPS XBRL Document Index",
                capability=MOPSCapability.XBRL_DOCUMENT_INDEX,
                transport="HTTP/JSON",
                path=f"{_MOPS_BASE}/mops/web/ajax_t164sb03",
                method="GET",
                response_format="JSON",
                requires_form_params=False,
                form_params={},
                expected_fields=["co_id", "year", "season"],
                charset="utf-8",
                cache_ttl_seconds=86400 * 90,
                update_cadence="quarterly",
                supports_history=True,
                enabled=True,
                official=True,
                metadata={"note": "XBRL document index. Taxonomy detection required."},
            ),
        ]
        for ep in endpoints:
            self._endpoints[ep.endpoint_id] = ep

    def get(self, endpoint_id: str) -> Optional[MOPSEndpoint]:
        return self._endpoints.get(endpoint_id)

    def list_all(self) -> List[MOPSEndpoint]:
        return list(self._endpoints.values())

    def list_enabled(self) -> List[MOPSEndpoint]:
        return [ep for ep in self._endpoints.values() if ep.enabled]

    def list_by_capability(self, capability: MOPSCapability) -> List[MOPSEndpoint]:
        return [ep for ep in self._endpoints.values() if ep.capability == capability]

    def is_endpoint_available(self, endpoint_id: str) -> bool:
        ep = self._endpoints.get(endpoint_id)
        return ep is not None and ep.enabled
