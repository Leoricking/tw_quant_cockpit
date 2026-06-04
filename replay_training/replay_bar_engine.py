"""replay_training/replay_bar_engine.py — ReplayBarEngine for TW Replay Training Cockpit v0.5.6.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] hidden_future_data=True by default. get_visible_bars() NEVER returns future bars.
[!] No broker connection. No live trading. Not investment advice.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReplayBarEngine:
    """Bar-by-bar replay engine for Taiwan stock intraday tape reading practice.

    Sessions are stored in memory (_sessions dict).
    Data loading reads CSV from data/intraday/{symbol}/{trade_date}_{timeframe}.csv
    or similar paths; graceful empty state if missing.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        data_root:  str = "data",
        output_dir: str = "data/backtest_results/replay_training",
    ) -> None:
        self._data_root  = os.path.join(BASE_DIR, data_root)
        self._output_dir = os.path.join(BASE_DIR, output_dir)
        os.makedirs(self._output_dir, exist_ok=True)
        # In-memory session store: session_id -> state dict
        self._sessions: Dict[str, dict] = {}

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_session_data(
        self, symbol: str, trade_date: str, timeframe: str = "1min"
    ) -> List[dict]:
        """Load bar data for a symbol/date/timeframe.  Returns list of bar dicts.

        Tries multiple path patterns. Returns [] if data not found (graceful).
        """
        candidates = [
            os.path.join(self._data_root, "intraday", symbol, f"{trade_date}_{timeframe}.csv"),
            os.path.join(self._data_root, "backtest_results", "intraday", f"{symbol}_{trade_date}_{timeframe}.csv"),
            os.path.join(self._data_root, "import", "intraday", symbol, f"{trade_date}_{timeframe}.csv"),
            os.path.join(self._data_root, "import", "intraday", f"{symbol}_{trade_date}_{timeframe}.csv"),
            os.path.join(self._data_root, "intraday", f"{symbol}_{trade_date}_{timeframe}.csv"),
        ]

        for path in candidates:
            if os.path.isfile(path):
                try:
                    bars = self._read_csv(path)
                    logger.info("[ReplayBarEngine] Loaded %d bars from %s", len(bars), path)
                    return bars
                except Exception as exc:
                    logger.warning("[ReplayBarEngine] Failed to load %s: %s", path, exc)

        logger.warning(
            "[ReplayBarEngine] No data found for %s %s %s — empty session", symbol, trade_date, timeframe
        )
        return []

    def _read_csv(self, path: str) -> List[dict]:
        """Read a CSV file and return list of dicts."""
        import csv
        bars = []
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bar = {}
                for k, v in row.items():
                    k = k.strip().lower()
                    try:
                        bar[k] = float(v)
                    except (ValueError, TypeError):
                        bar[k] = v
                bars.append(bar)
        return bars

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def create_session(
        self, symbol: str, trade_date: str, timeframe: str = "1min", mode: str = "real"
    ):
        """Create a new ReplayTrainingSession and load bar data."""
        from replay_training.replay_training_schema import ReplayTrainingSession

        session_id = f"RTRAIN-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
        bars = self.load_session_data(symbol, trade_date, timeframe)

        session = ReplayTrainingSession(
            session_id=session_id,
            symbol=symbol,
            trade_date=trade_date,
            timeframe=timeframe,
            mode=mode,
            started_at=datetime.now().isoformat(),
            current_bar_index=0,
            total_bars=len(bars),
            status="ACTIVE" if bars else "EMPTY",
            hidden_future_data=True,
            replay_speed=1,
            read_only=True,
            no_real_orders=True,
            production_blocked=True,
        )

        self._sessions[session_id] = {
            "session": session,
            "bars": bars,
        }
        return session

    def _get_state(self, session_id: str) -> Optional[dict]:
        state = self._sessions.get(session_id)
        if state is None:
            logger.warning("[ReplayBarEngine] Session not found: %s", session_id)
        return state

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def next_bar(self, session_id: str) -> dict:
        """Advance one bar. Returns current snapshot."""
        state = self._get_state(session_id)
        if state is None:
            return {"ok": False, "error": "session_not_found"}
        session = state["session"]
        bars    = state["bars"]
        if not bars:
            return {"ok": False, "error": "no_data", "snapshot": self._empty_snapshot(session)}
        if session.current_bar_index < len(bars) - 1:
            session.current_bar_index += 1
        return self.get_current_snapshot(session_id)

    def prev_bar(self, session_id: str) -> dict:
        """Go back one bar. Returns current snapshot."""
        state = self._get_state(session_id)
        if state is None:
            return {"ok": False, "error": "session_not_found"}
        session = state["session"]
        bars    = state["bars"]
        if not bars:
            return {"ok": False, "error": "no_data", "snapshot": self._empty_snapshot(session)}
        if session.current_bar_index > 0:
            session.current_bar_index -= 1
        return self.get_current_snapshot(session_id)

    def jump_to_bar(self, session_id: str, bar_index: int) -> dict:
        """Jump to a specific bar index. Returns current snapshot."""
        state = self._get_state(session_id)
        if state is None:
            return {"ok": False, "error": "session_not_found"}
        session = state["session"]
        bars    = state["bars"]
        if not bars:
            return {"ok": False, "error": "no_data", "snapshot": self._empty_snapshot(session)}
        bar_index = max(0, min(bar_index, len(bars) - 1))
        session.current_bar_index = bar_index
        return self.get_current_snapshot(session_id)

    def set_speed(self, session_id: str, speed: int) -> None:
        """Set replay speed (1x/2x/4x/8x)."""
        state = self._get_state(session_id)
        if state is None:
            return
        valid_speeds = [1, 2, 4, 8]
        speed = speed if speed in valid_speeds else 1
        state["session"].replay_speed = speed

    # ------------------------------------------------------------------
    # Visible bars — NEVER returns future bars
    # ------------------------------------------------------------------

    def get_visible_bars(self, session_id: str) -> List[dict]:
        """Return ONLY bars up to current_bar_index (never future bars).

        [!] hidden_future_data is enforced here.
        """
        state = self._get_state(session_id)
        if state is None:
            return []
        session = state["session"]
        bars    = state["bars"]
        if not bars:
            return []
        # CRITICAL: only return bars[0 : current_bar_index+1]
        cutoff = session.current_bar_index + 1
        return list(bars[:cutoff])

    def get_current_snapshot(self, session_id: str) -> dict:
        """Return the current bar snapshot with session metadata."""
        state = self._get_state(session_id)
        if state is None:
            return {"ok": False, "error": "session_not_found"}
        session = state["session"]
        bars    = state["bars"]

        if not bars:
            return {
                "ok": True,
                "snapshot": self._empty_snapshot(session),
                "no_real_orders": True,
                "replay_training_only": True,
            }

        idx         = session.current_bar_index
        current_bar = bars[idx] if idx < len(bars) else {}
        visible     = self.get_visible_bars(session_id)

        return {
            "ok": True,
            "snapshot": {
                "session_id":         session.session_id,
                "symbol":             session.symbol,
                "trade_date":         session.trade_date,
                "timeframe":          session.timeframe,
                "current_bar_index":  idx,
                "total_bars":         len(bars),
                "current_bar":        current_bar,
                "visible_bars_count": len(visible),
                "status":             session.status,
                "hidden_future_data": session.hidden_future_data,
                "replay_speed":       session.replay_speed,
                "no_real_orders":     True,
                "replay_training_only": True,
                "label": "Replay Training Only / Research Only / No Real Orders",
            },
            "no_real_orders":     True,
            "replay_training_only": True,
        }

    def _empty_snapshot(self, session) -> dict:
        return {
            "session_id":         session.session_id,
            "symbol":             session.symbol,
            "trade_date":         session.trade_date,
            "timeframe":          session.timeframe,
            "current_bar_index":  0,
            "total_bars":         0,
            "current_bar":        {},
            "visible_bars_count": 0,
            "status":             "EMPTY",
            "hidden_future_data": True,
            "replay_speed":       1,
            "no_real_orders":     True,
            "replay_training_only": True,
            "label": "Replay Training Only / Research Only / No Real Orders",
        }
