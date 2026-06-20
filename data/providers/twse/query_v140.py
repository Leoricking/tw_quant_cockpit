"""
data/providers/twse/query_v140.py — TWSE query service v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official TWSE Public Data Only. No mock fallback in Real mode.
[!] Not Real-Time. Historical data only unless explicitly stated.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from data.providers.twse.corporate_actions_v140 import TWSECorporateActionsService
from data.providers.twse.daily_ohlcv_v140 import TWSEDailyOHLCVService
from data.providers.twse.indices_v140 import TWSEIndicesService
from data.providers.twse.institutional_v140 import TWSEInstitutionalService
from data.providers.twse.margin_v140 import TWSEMarginService
from data.providers.twse.market_summary_v140 import TWSEMarketSummaryService
from data.providers.twse.models_v140 import (
    TWSECorporateActionPreview,
    TWSEDailyBar,
    TWSEIndexRecord,
    TWSEInstitutionalFlow,
    TWSEMarginRecord,
    TWSEMarketSummary,
    TWSESecurity,
    TWSETradingDay,
)
from data.providers.twse.security_master_v140 import TWSESecurityMasterService
from data.providers.twse.trading_calendar_v140 import TWSETradingCalendar

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class TWSEQueryService:
    """Unified query interface wrapping all TWSE services."""

    def __init__(self) -> None:
        self._security_master = TWSESecurityMasterService()
        self._daily_ohlcv = TWSEDailyOHLCVService()
        self._institutional = TWSEInstitutionalService()
        self._margin = TWSEMarginService()
        self._market_summary = TWSEMarketSummaryService()
        self._indices = TWSEIndicesService()
        self._calendar = TWSETradingCalendar()
        self._corporate_actions = TWSECorporateActionsService()

    def get_security(self, symbol: str) -> Optional[TWSESecurity]:
        try:
            return self._security_master.get_security(symbol)
        except Exception:
            return None

    def list_securities(self, market: str = "TWSE") -> List[TWSESecurity]:
        try:
            return self._security_master.list_securities(market)
        except Exception:
            return []

    def get_daily_bar(self, symbol: str, trade_date: str) -> Optional[TWSEDailyBar]:
        try:
            return self._daily_ohlcv.get_bar(symbol, trade_date)
        except Exception:
            return None

    def get_daily_bars(self, symbol: str, start_date: str, end_date: str) -> List[TWSEDailyBar]:
        try:
            return self._daily_ohlcv.get_bars(symbol, start_date, end_date)
        except Exception:
            return []

    def get_latest_bar(self, symbol: str) -> Optional[TWSEDailyBar]:
        try:
            return self._daily_ohlcv.get_latest_bar(symbol)
        except Exception:
            return None

    def get_institutional_flow(self, symbol: str, trade_date: str) -> Optional[TWSEInstitutionalFlow]:
        try:
            return self._institutional.get_flow(symbol, trade_date)
        except Exception:
            return None

    def get_margin(self, symbol: str, trade_date: str) -> Optional[TWSEMarginRecord]:
        try:
            return self._margin.get_margin(symbol, trade_date)
        except Exception:
            return None

    def get_market_summary(self, trade_date: str) -> Optional[TWSEMarketSummary]:
        try:
            return self._market_summary.get_summary(trade_date)
        except Exception:
            return None

    def get_index_history(
        self, index_code: str, start_date: str, end_date: str
    ) -> List[TWSEIndexRecord]:
        try:
            return self._indices.get_index_history(index_code, start_date, end_date)
        except Exception:
            return []

    def get_trading_calendar(self, start_date: str, end_date: str) -> List[TWSETradingDay]:
        try:
            import datetime
            result: List[TWSETradingDay] = []
            d = datetime.date.fromisoformat(start_date)
            end_d = datetime.date.fromisoformat(end_date)
            now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            while d <= end_d:
                ds = d.isoformat()
                info = self._calendar.is_trading_day(ds)
                result.append(
                    TWSETradingDay(
                        date=ds,
                        is_trading_day=info["is_trading_day"],
                        holiday_name=info.get("holiday_name"),
                        market="TWSE",
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

    def get_corporate_actions(self, symbol: str) -> List[TWSECorporateActionPreview]:
        try:
            return self._corporate_actions.get_actions(symbol)
        except Exception:
            return []

    def summarize_coverage(self) -> Dict[str, Any]:
        try:
            return {
                "securities": self._security_master.count(),
                "daily_bars": "offline_mode",
                "source": "twse_official",
                "official": True,
                "no_real_orders": True,
                "realtime_available": False,
            }
        except Exception:
            return {"error": "Could not summarize coverage"}
