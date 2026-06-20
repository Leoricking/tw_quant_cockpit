"""
data/providers/twse/endpoints_v140.py — TWSE endpoint registry v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from data.providers.twse.models_v140 import TWSECapability

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


@dataclass
class TWSEEndpoint:
    """Definition of a single TWSE API endpoint."""
    endpoint_id: str
    official_name: str
    capability: TWSECapability
    transport: str           # e.g. "HTTP/JSON", "HTTP/CSV", "HTTP/HTML"
    path: str
    method: str              # "GET"
    response_format: str     # "JSON", "CSV", "HTML"
    market: str
    query_params: Dict[str, Any] = field(default_factory=dict)
    expected_fields: List[str] = field(default_factory=list)
    source_timestamp_rule: str = "response_date"
    cache_ttl_seconds: int = 3600
    update_cadence: str = "daily"
    supports_history: bool = False
    date_range_limit_days: int = 0
    enabled: bool = True
    fallback_endpoint_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TWSEEndpointRegistry:
    """Registry of all TWSE API endpoints."""

    def __init__(self) -> None:
        self._endpoints: Dict[str, TWSEEndpoint] = {}
        self._register_all()

    def _register_all(self) -> None:
        endpoints = [
            TWSEEndpoint(
                endpoint_id="security_master_listed",
                official_name="TWSE Listed Company Information",
                capability=TWSECapability.SECURITY_MASTER,
                transport="HTTP/JSON",
                path="https://openapi.twse.com.tw/v1/opendata/t187ap03_L",
                method="GET",
                response_format="JSON",
                market="TWSE",
                query_params={},
                expected_fields=["公司代號", "公司簡稱", "產業別", "上市日期", "ISIN碼"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=86400 * 7,
                update_cadence="weekly",
                supports_history=False,
                date_range_limit_days=0,
                enabled=True,
                fallback_endpoint_id=None,
                metadata={"note": "Listed company info. Verify path against official docs."},
            ),
            TWSEEndpoint(
                endpoint_id="daily_ohlcv_all",
                official_name="TWSE Daily Stock OHLCV (All Stocks)",
                capability=TWSECapability.DAILY_OHLCV,
                transport="HTTP/JSON",
                path="https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",
                method="GET",
                response_format="JSON",
                market="TWSE",
                query_params={},
                expected_fields=["證券代號", "證券名稱", "開盤價", "最高價", "最低價", "收盤價", "成交股數"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=3600,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                fallback_endpoint_id=None,
                metadata={"note": "Returns latest trading day data. No date parameter."},
            ),
            TWSEEndpoint(
                endpoint_id="institutional_all",
                official_name="TWSE Institutional Investors (Three Major)",
                capability=TWSECapability.INSTITUTIONAL,
                transport="HTTP/JSON",
                path="https://openapi.twse.com.tw/v1/fund/T86",
                method="GET",
                response_format="JSON",
                market="TWSE",
                query_params={},
                expected_fields=["證券代號", "證券名稱", "外陸資買進股數(不含外資自營商)", "投信買進股數"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=14400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                fallback_endpoint_id=None,
                metadata={"note": "Three major institutional investors."},
            ),
            TWSEEndpoint(
                endpoint_id="margin_all",
                official_name="TWSE Margin & Short Sales (All Stocks)",
                capability=TWSECapability.MARGIN,
                transport="HTTP/JSON",
                path="https://openapi.twse.com.tw/v1/marginShortSales/MS_margin_short_sales",
                method="GET",
                response_format="JSON",
                market="TWSE",
                query_params={},
                expected_fields=["股票代號", "名稱", "融資買進", "融資賣出", "融券賣出"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=14400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                fallback_endpoint_id=None,
                metadata={"note": "Margin and short sales. Verify path against official docs."},
            ),
            TWSEEndpoint(
                endpoint_id="market_summary",
                official_name="TWSE Market Summary (FMTQIK)",
                capability=TWSECapability.DAILY_TRADING_SUMMARY,
                transport="HTTP/JSON",
                path="https://openapi.twse.com.tw/v1/exchangeReport/FMTQIK",
                method="GET",
                response_format="JSON",
                market="TWSE",
                query_params={},
                expected_fields=["Date", "TradeVolume", "TradeValue", "Transaction", "TAIEX"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=3600,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                fallback_endpoint_id=None,
                metadata={},
            ),
            TWSEEndpoint(
                endpoint_id="taiex_daily",
                official_name="TWSE TAIEX Daily Index (MI_INDEX)",
                capability=TWSECapability.MARKET_INDEX,
                transport="HTTP/JSON",
                path="https://openapi.twse.com.tw/v1/exchangeReport/MI_INDEX",
                method="GET",
                response_format="JSON",
                market="TWSE",
                query_params={},
                expected_fields=["Date", "Open", "High", "Low", "Close", "Change"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=3600,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                fallback_endpoint_id=None,
                metadata={"note": "TAIEX and sub-index data. Verify path against official docs."},
            ),
            TWSEEndpoint(
                endpoint_id="trading_calendar",
                official_name="TWSE Trading Calendar (Heuristic)",
                capability=TWSECapability.TRADING_CALENDAR,
                transport="HEURISTIC",
                path="",
                method="LOCAL",
                response_format="INTERNAL",
                market="TWSE",
                query_params={},
                expected_fields=["date", "is_trading_day", "holiday_name"],
                source_timestamp_rule="fixed",
                cache_ttl_seconds=86400 * 30,
                update_cadence="annual",
                supports_history=True,
                date_range_limit_days=0,
                enabled=True,
                fallback_endpoint_id=None,
                metadata={
                    "note": "No official OpenAPI for calendar. Uses heuristic (weekend + known holidays). Always approximate=True.",
                    "approximate": True,
                },
            ),
            TWSEEndpoint(
                endpoint_id="corporate_actions_ex",
                official_name="TWSE Ex-Rights/Dividend Announcements",
                capability=TWSECapability.CORPORATE_ACTIONS,
                transport="HTTP/JSON",
                path="https://openapi.twse.com.tw/v1/exchangeReport/TWT49U",
                method="GET",
                response_format="JSON",
                market="TWSE",
                query_params={},
                expected_fields=["Code", "Name", "ExRightsDate", "ExDividendDate"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=86400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=False,  # path needs verification
                fallback_endpoint_id=None,
                metadata={"note": "Path needs verification against official TWSE OpenAPI docs."},
            ),
            TWSEEndpoint(
                endpoint_id="valuation",
                official_name="TWSE Valuation Metrics (BWIBBU_ALL)",
                capability=TWSECapability.VALUATION,
                transport="HTTP/JSON",
                path="https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_ALL",
                method="GET",
                response_format="JSON",
                market="TWSE",
                query_params={},
                expected_fields=["Code", "Name", "PEratio", "DividendYield", "PBratio"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=86400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                fallback_endpoint_id=None,
                metadata={"note": "P/E, P/B, dividend yield for all listed stocks."},
            ),
        ]
        for ep in endpoints:
            self._endpoints[ep.endpoint_id] = ep

    def get(self, endpoint_id: str) -> Optional[TWSEEndpoint]:
        return self._endpoints.get(endpoint_id)

    def list_all(self) -> List[TWSEEndpoint]:
        return list(self._endpoints.values())

    def list_enabled(self) -> List[TWSEEndpoint]:
        return [ep for ep in self._endpoints.values() if ep.enabled]

    def list_by_capability(self, capability: TWSECapability) -> List[TWSEEndpoint]:
        return [ep for ep in self._endpoints.values() if ep.capability == capability]

    def is_endpoint_available(self, endpoint_id: str) -> bool:
        ep = self._endpoints.get(endpoint_id)
        return ep is not None and ep.enabled
