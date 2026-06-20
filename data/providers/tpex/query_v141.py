"""
data/providers/tpex/query_v141.py — TPEx query service v1.4.1.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TPEx Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
[!] Mainboard Common Stocks Only By Default.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from data.providers.tpex.corporate_actions_v141 import TPExCorporateActionsService
from data.providers.tpex.daily_ohlcv_v141 import TPExDailyOHLCVService
from data.providers.tpex.indices_v141 import TPExIndicesService
from data.providers.tpex.institutional_v141 import TPExInstitutionalService
from data.providers.tpex.margin_v141 import TPExMarginService
from data.providers.tpex.market_summary_v141 import TPExMarketSummaryService
from data.providers.tpex.models_v141 import (
    TPExCorporateActionPreview,
    TPExDailyBar,
    TPExIndexRecord,
    TPExInstitutionalFlow,
    TPExMarginRecord,
    TPExMarketSummary,
    TPExSecurity,
    TPExSuspensionRecord,
    TPExTradingDay,
    TPExValuationRecord,
)
from data.providers.tpex.security_master_v141 import TPExSecurityMasterService
from data.providers.tpex.suspension_v141 import TPExSuspensionService
from data.providers.tpex.trading_calendar_v141 import TPExTradingCalendar
from data.providers.tpex.valuation_v141 import TPExValuationService

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TPExQueryService:
    """Unified query interface wrapping all TPEx services. All missing data -> None or [] (never crash)."""

    def __init__(self) -> None:
        self._security_master = TPExSecurityMasterService()
        self._daily_ohlcv = TPExDailyOHLCVService()
        self._institutional = TPExInstitutionalService()
        self._margin = TPExMarginService()
        self._market_summary = TPExMarketSummaryService()
        self._indices = TPExIndicesService()
        self._calendar = TPExTradingCalendar()
        self._suspension = TPExSuspensionService()
        self._corporate_actions = TPExCorporateActionsService()
        self._valuation = TPExValuationService()

    def get_security(self, symbol: str) -> Optional[TPExSecurity]:
        try:
            return self._security_master.get_security(symbol)
        except Exception:
            return None

    def list_securities(
        self,
        board: Optional[str] = None,
        security_type: Optional[str] = None,
    ) -> List[TPExSecurity]:
        try:
            return self._security_master.list_securities(board=board, security_type=security_type)
        except Exception:
            return []

    def get_daily_bar(self, symbol: str, trade_date: str) -> Optional[TPExDailyBar]:
        try:
            return self._daily_ohlcv.get_bar(symbol, trade_date)
        except Exception:
            return None

    def get_daily_bars(self, symbol: str, start_date: str, end_date: str) -> List[TPExDailyBar]:
        try:
            return self._daily_ohlcv.get_bars(symbol, start_date, end_date)
        except Exception:
            return []

    def get_latest_bar(self, symbol: str) -> Optional[TPExDailyBar]:
        try:
            return self._daily_ohlcv.get_latest_bar(symbol)
        except Exception:
            return None

    def get_institutional_flow(self, symbol: str, trade_date: str) -> Optional[TPExInstitutionalFlow]:
        try:
            return self._institutional.get_flow(symbol, trade_date)
        except Exception:
            return None

    def get_margin(self, symbol: str, trade_date: str) -> Optional[TPExMarginRecord]:
        try:
            return self._margin.get_margin(symbol, trade_date)
        except Exception:
            return None

    def get_market_summary(self, trade_date: str) -> Optional[TPExMarketSummary]:
        try:
            return self._market_summary.get_summary(trade_date)
        except Exception:
            return None

    def get_index_history(
        self, index_code: str, start_date: str, end_date: str
    ) -> List[TPExIndexRecord]:
        try:
            return self._indices.get_index_history(index_code, start_date, end_date)
        except Exception:
            return []

    def get_trading_calendar(self, start_date: str, end_date: str) -> List[TPExTradingDay]:
        try:
            import datetime
            result: List[TPExTradingDay] = []
            d = datetime.date.fromisoformat(start_date)
            end_d = datetime.date.fromisoformat(end_date)
            now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            while d <= end_d:
                ds = d.isoformat()
                info = self._calendar.is_trading_day(ds)
                result.append(
                    TPExTradingDay(
                        date=ds,
                        is_trading_day=info["is_trading_day"],
                        holiday_name=info.get("holiday_name"),
                        market="TPEx",
                        source=info.get("source", "heuristic"),
                        approximate=info.get("approximate", True),
                        fetched_at=now_iso,
                        metadata={},
                    )
                )
                d += datetime.timedelta(days=1)
            return result
        except Exception:
            return []

    def get_suspensions(self, symbol: Optional[str] = None) -> List[TPExSuspensionRecord]:
        try:
            return self._suspension.get_suspensions(symbol=symbol)
        except Exception:
            return []

    def get_corporate_actions(self, symbol: str) -> List[TPExCorporateActionPreview]:
        try:
            return self._corporate_actions.get_actions(symbol)
        except Exception:
            return []

    def get_valuation(
        self, symbol: str, trade_date: Optional[str] = None
    ) -> Optional[TPExValuationRecord]:
        try:
            return self._valuation.get_valuation(symbol, trade_date)
        except Exception:
            return None

    def summarize_coverage(self) -> Dict[str, Any]:
        try:
            return {
                "securities": self._security_master.count(),
                "common_stocks": len(self._security_master.list_common_stocks()),
                "daily_bars": "offline_mode",
                "source": "tpex_official",
                "official": True,
                "no_real_orders": True,
                "realtime_available": False,
                "board_scope": "MAINBOARD",
                "market": "TPEx",
            }
        except Exception:
            return {"error": "Could not summarize coverage"}
