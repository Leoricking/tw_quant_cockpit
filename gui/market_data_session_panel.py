"""
gui/market_data_session_panel.py — Market Data Session GUI Panel v1.6.1
[!] Research Only. No Real Orders. No Broker. Simulation Only.
Display-only panel for market data session status and event monitoring.
Real order methods raise NotImplementedError.
"""
from __future__ import annotations
from typing import Optional, Dict, Any, List

NO_REAL_ORDERS: bool = True
BROKER_EXECUTION_ENABLED: bool = False
PRODUCTION_TRADING_BLOCKED: bool = True
MARKET_DATA_ONLY: bool = True
PANEL_VERSION: str = "1.6.1"
PANEL_NAME: str = "Market Data Session"

_DISCLAIMER = (
    "[!] MARKET DATA ONLY. NO REAL ORDERS. NO BROKER. "
    "RESEARCH ONLY. NOT INVESTMENT ADVICE."
)


class MarketDataSessionPanel:
    """
    GUI panel for market data session monitoring.
    Display-only. No real order submission. No broker connection.
    """

    def __init__(self) -> None:
        self._current_session_id: Optional[str] = None
        self._session_status: Optional[str] = None
        self._event_log: List[Dict[str, Any]] = []
        self._feed_health: Dict[str, Any] = {}

    def render_header(self) -> str:
        return (
            f"=== {PANEL_NAME} Panel v{PANEL_VERSION} ===\n"
            f"{_DISCLAIMER}"
        )

    def render_session_status(self, session_info: Optional[Dict[str, Any]] = None) -> str:
        if not session_info:
            return "No active market data session."
        lines = [
            f"Session ID:   {session_info.get('session_id', 'N/A')}",
            f"Status:       {session_info.get('status', 'N/A')}",
            f"Adapter:      {session_info.get('adapter_id', 'N/A')}",
            f"Source Class: {session_info.get('source_class', 'N/A')}",
            f"Events:       {session_info.get('event_count', 0)}",
            f"Started:      {session_info.get('started_at', 'N/A')}",
            f"[Research Only] [No Real Orders] [Market Data Only]",
        ]
        return "\n".join(lines)

    def render_feed_health(self, health_report: Optional[Dict[str, Any]] = None) -> str:
        if not health_report:
            return "No feed health data."
        lines = [
            f"Feed:    {health_report.get('adapter_id', 'N/A')}",
            f"Alive:   {health_report.get('is_alive', False)}",
            f"Gaps:    {health_report.get('gap_count', 0)}",
            f"Message: {health_report.get('message', 'N/A')}",
        ]
        return "\n".join(lines)

    def render_event_table(self, events: Optional[List[Dict[str, Any]]] = None, limit: int = 20) -> str:
        if not events:
            return "No events to display."
        rows = events[-limit:]
        lines = ["Symbol  | Type  | Timestamp           | Freshness | Quality"]
        lines.append("-" * 62)
        for ev in rows:
            sym = ev.get("symbol", "?")[:7].ljust(7)
            etype = ev.get("event_type", "?")[:5].ljust(5)
            ts = str(ev.get("timestamp_utc", "?"))[:19]
            fresh = str(ev.get("freshness_status", "?"))[:9].ljust(9)
            qual = str(ev.get("quality_status", "?"))[:7]
            lines.append(f"{sym} | {etype} | {ts} | {fresh} | {qual}")
        return "\n".join(lines)

    def render_disclaimer(self) -> str:
        return _DISCLAIMER

    # Forbidden real-order methods
    def submit_real_order(self, *args, **kwargs):
        raise NotImplementedError(
            "submit_real_order FORBIDDEN — PRODUCTION_TRADING_BLOCKED=True. "
            "This panel is MARKET_DATA_ONLY."
        )

    def connect_to_broker(self, *args, **kwargs):
        raise NotImplementedError(
            "connect_to_broker FORBIDDEN — NO_BROKER_API=True."
        )

    def execute_live_trade(self, *args, **kwargs):
        raise NotImplementedError(
            "execute_live_trade FORBIDDEN — PRODUCTION_TRADING_BLOCKED=True."
        )
