"""
data/providers/tpex/endpoints_v141.py — TPEx endpoint registry v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from data.providers.tpex.models_v141 import TPExCapability

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


@dataclass
class TPExEndpoint:
    """Definition of a single TPEx API endpoint."""
    endpoint_id: str
    official_name: str
    capability: TPExCapability
    transport: str
    path: str
    method: str
    response_format: str
    board: str
    security_scope: str
    query_params: Dict[str, Any] = field(default_factory=dict)
    expected_fields: List[str] = field(default_factory=list)
    source_timestamp_rule: str = "response_date"
    cache_ttl_seconds: int = 3600
    update_cadence: str = "daily"
    supports_history: bool = False
    date_range_limit_days: int = 0
    enabled: bool = True
    official: bool = True
    fallback_endpoint_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TPExEndpointRegistry:
    """Registry of all TPEx API endpoints."""

    def __init__(self) -> None:
        self._endpoints: Dict[str, TPExEndpoint] = {}
        self._register_all()

    def _register_all(self) -> None:
        endpoints = [
            TPExEndpoint(
                endpoint_id="security_master_otc",
                official_name="TPEx OTC Listed Company Information",
                capability=TPExCapability.SECURITY_MASTER,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="ALL",
                query_params={},
                expected_fields=["SecuritiesCompanyCode", "CompanyName", "Industry"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=86400 * 7,
                update_cadence="weekly",
                supports_history=False,
                date_range_limit_days=0,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "OTC listed company info. Verify path against official TPEx OpenAPI docs."},
            ),
            TPExEndpoint(
                endpoint_id="daily_quotes_otc",
                official_name="TPEx Daily OTC Stock Quotes",
                capability=TPExCapability.DAILY_OHLCV,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_st_daily_trade",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="COMMON_STOCK",
                query_params={},
                expected_fields=["SecuritiesCompanyCode", "Open", "High", "Low", "Close", "Volume"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=3600,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "Returns latest trading day. Verify path against official docs."},
            ),
            TPExEndpoint(
                endpoint_id="historical_quotes_otc",
                official_name="TPEx Historical OTC Stock Quotes",
                capability=TPExCapability.DAILY_OHLCV,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_st_daily_trade_hist",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="COMMON_STOCK",
                query_params={"date": ""},
                expected_fields=["SecuritiesCompanyCode", "Open", "High", "Low", "Close"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=86400 * 7,
                update_cadence="daily",
                supports_history=True,
                date_range_limit_days=365,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "Historical daily quotes. Date param required. Verify path."},
            ),
            TPExEndpoint(
                endpoint_id="institutional_otc",
                official_name="TPEx Institutional Investors (Three Major)",
                capability=TPExCapability.INSTITUTIONAL,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_mainboard_institution_trading",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="COMMON_STOCK",
                query_params={},
                expected_fields=["SecuritiesCompanyCode", "ForeignInvestorBuy", "InvestmentTrustBuy"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=14400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "Three major institutional investors for OTC market. Verify path."},
            ),
            TPExEndpoint(
                endpoint_id="institutional_dealer_split_otc",
                official_name="TPEx Dealer Proprietary vs Hedge Split",
                capability=TPExCapability.INSTITUTIONAL,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_mainboard_dealer_trading",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="COMMON_STOCK",
                query_params={},
                expected_fields=["SecuritiesCompanyCode", "DealerProprietaryBuy", "DealerHedgeBuy"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=14400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=False,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "Dealer proprietary vs hedge split detail. Path needs verification."},
            ),
            TPExEndpoint(
                endpoint_id="margin_otc",
                official_name="TPEx Margin & Short Sales (OTC)",
                capability=TPExCapability.MARGIN,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_mainboard_margin_trading",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="COMMON_STOCK",
                query_params={},
                expected_fields=["SecuritiesCompanyCode", "MarginBuy", "MarginSell", "ShortSell"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=14400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "Margin and short sales for OTC mainboard. Verify path."},
            ),
            TPExEndpoint(
                endpoint_id="market_summary_otc",
                official_name="TPEx Market Summary (OTC Daily)",
                capability=TPExCapability.DAILY_TRADING_SUMMARY,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="ALL",
                query_params={},
                expected_fields=["Date", "TradingValue", "TradingVolume", "Index"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=3600,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "OTC daily market summary. Verify path against official docs."},
            ),
            TPExEndpoint(
                endpoint_id="tpex_index_daily",
                official_name="TPEx Composite Index Daily",
                capability=TPExCapability.MARKET_INDEX,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_mainboard_index_daily",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="INDEX",
                query_params={},
                expected_fields=["Date", "Open", "High", "Low", "Close", "Change"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=3600,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "TPEx composite index daily data. Verify path against official docs."},
            ),
            TPExEndpoint(
                endpoint_id="trading_calendar_otc",
                official_name="TPEx Trading Calendar (Heuristic)",
                capability=TPExCapability.TRADING_CALENDAR,
                transport="HEURISTIC",
                path="",
                method="LOCAL",
                response_format="INTERNAL",
                board="MAINBOARD",
                security_scope="ALL",
                query_params={},
                expected_fields=["date", "is_trading_day", "holiday_name"],
                source_timestamp_rule="fixed",
                cache_ttl_seconds=86400 * 30,
                update_cadence="annual",
                supports_history=True,
                date_range_limit_days=0,
                enabled=False,
                official=False,
                fallback_endpoint_id=None,
                metadata={
                    "note": "No official OpenAPI for TPEx calendar. Shares same holiday schedule as TWSE. Always approximate=True.",
                    "approximate": True,
                },
            ),
            TPExEndpoint(
                endpoint_id="suspension_otc",
                official_name="TPEx Suspension & Resumption Announcements",
                capability=TPExCapability.SUSPENSION_RESUMPTION,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_mainboard_suspension",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="ALL",
                query_params={},
                expected_fields=["SecuritiesCompanyCode", "EffectiveDate", "ResumeDate", "Reason"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=86400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "Suspension/resumption announcements. Verify path against official docs."},
            ),
            TPExEndpoint(
                endpoint_id="corporate_actions_otc",
                official_name="TPEx Corporate Actions (Ex-Rights/Dividend)",
                capability=TPExCapability.CORPORATE_ACTIONS,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_mainboard_exrights",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="ALL",
                query_params={},
                expected_fields=["SecuritiesCompanyCode", "ExRightsDate", "ExDividendDate"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=86400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=False,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "Ex-rights/dividend announcements. Path needs verification."},
            ),
            TPExEndpoint(
                endpoint_id="valuation_otc",
                official_name="TPEx Valuation Metrics (P/E, P/B, Yield)",
                capability=TPExCapability.VALUATION,
                transport="HTTP/JSON",
                path="https://www.tpex.org.tw/openapi/v1/tpex_mainboard_peratio",
                method="GET",
                response_format="JSON",
                board="MAINBOARD",
                security_scope="COMMON_STOCK",
                query_params={},
                expected_fields=["SecuritiesCompanyCode", "PEratio", "DividendYield", "PBratio"],
                source_timestamp_rule="response_date",
                cache_ttl_seconds=86400,
                update_cadence="daily",
                supports_history=False,
                date_range_limit_days=1,
                enabled=True,
                official=True,
                fallback_endpoint_id=None,
                metadata={"note": "P/E, P/B, dividend yield for OTC stocks. Verify path."},
            ),
        ]
        for ep in endpoints:
            self._endpoints[ep.endpoint_id] = ep

    def get(self, endpoint_id: str) -> Optional[TPExEndpoint]:
        return self._endpoints.get(endpoint_id)

    def list_all(self) -> List[TPExEndpoint]:
        return list(self._endpoints.values())

    def list_enabled(self) -> List[TPExEndpoint]:
        return [ep for ep in self._endpoints.values() if ep.enabled]

    def list_by_capability(self, capability: TPExCapability) -> List[TPExEndpoint]:
        return [ep for ep in self._endpoints.values() if ep.capability == capability]

    def is_endpoint_available(self, endpoint_id: str) -> bool:
        ep = self._endpoints.get(endpoint_id)
        return ep is not None and ep.enabled
