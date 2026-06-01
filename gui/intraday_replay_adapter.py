"""gui/intraday_replay_adapter.py — Intraday Replay GUI Adapter (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class IntradayReplayAdapter:
    """Bridges the GUI panel to the replay engine and analysis modules.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    All methods are wrapped in try/except — never crash. Lazy imports.
    """

    read_only = True
    no_real_orders = True

    def __init__(self, replay_root: str = "replay_sessions", report_dir: str = "reports"):
        self._replay_root = replay_root
        self._report_dir = report_dir
        self._engine = None  # IntradayReplayEngine — lazy init
        self._session_manager = None
        self._current_session = None

    # ------------------------------------------------------------------
    # Internal lazy init
    # ------------------------------------------------------------------
    def _get_engine(self):
        if self._engine is None:
            try:
                from replay.replay_engine import IntradayReplayEngine
                self._engine = IntradayReplayEngine()
            except Exception as exc:
                logger.error("[IntradayReplayAdapter] engine init error: %s", exc)
        return self._engine

    def _get_session_manager(self):
        if self._session_manager is None:
            try:
                from replay.replay_session import ReplaySessionManager
                self._session_manager = ReplaySessionManager(replay_root=self._replay_root)
            except Exception as exc:
                logger.error("[IntradayReplayAdapter] session manager init error: %s", exc)
        return self._session_manager

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------
    def create_session(
        self, symbol: str, date: Optional[str] = None, freq: str = "1min"
    ) -> dict:
        try:
            mgr = self._get_session_manager()
            if mgr is None:
                return {"ok": False, "error": "session_manager_unavailable"}
            session = mgr.create_session(symbol=symbol, date=date, freq=freq)
            self._current_session = session
            return {"ok": True, "session": session.to_dict()}
        except Exception as exc:
            logger.error("[IntradayReplayAdapter] create_session error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def load_session(self, session_id: str) -> dict:
        try:
            mgr = self._get_session_manager()
            if mgr is None:
                return {"ok": False, "error": "session_manager_unavailable"}
            session = mgr.load_session(session_id)
            if session is None:
                return {"ok": False, "error": "session_not_found"}
            self._current_session = session
            return {"ok": True, "session": session.to_dict()}
        except Exception as exc:
            logger.error("[IntradayReplayAdapter] load_session error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Replay control
    # ------------------------------------------------------------------
    def prepare_replay(
        self, symbol: str, date: Optional[str] = None, freq: str = "1min"
    ) -> dict:
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}

            # Create session
            self.create_session(symbol=symbol, date=date, freq=freq)

            summary = engine.prepare_replay(symbol=symbol, date=date, freq=freq)
            status = summary.get("status", "")
            if status in ("INSUFFICIENT_INTRADAY_DATA", "NOT_LOADED"):
                return {"ok": False, "error": status, "summary": summary}

            return {
                "ok": True,
                "summary": summary,
                "current_bar": summary.get("current_bar", {}),
                "research_only": True,
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.error("[IntradayReplayAdapter] prepare_replay error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def step_forward(self) -> dict:
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}
            bar = engine.step_forward()
            return {
                "ok": True,
                "bar": bar,
                "index": engine.current_index,
                "total": engine.total_bars,
                "research_only": True,
            }
        except Exception as exc:
            logger.error("[IntradayReplayAdapter] step_forward error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def step_backward(self) -> dict:
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}
            bar = engine.step_backward()
            return {
                "ok": True,
                "bar": bar,
                "index": engine.current_index,
                "total": engine.total_bars,
                "research_only": True,
            }
        except Exception as exc:
            logger.error("[IntradayReplayAdapter] step_backward error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def jump_to_time(self, time_str: str) -> dict:
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}
            bar = engine.jump_to_time(time_str)
            return {
                "ok": True,
                "bar": bar,
                "index": engine.current_index,
                "total": engine.total_bars,
                "research_only": True,
            }
        except Exception as exc:
            logger.error("[IntradayReplayAdapter] jump_to_time error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # State building
    # ------------------------------------------------------------------
    def build_current_state(self) -> dict:
        """Build full overlay state from visible bars. Never crash."""
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}

            if engine.status not in ("READY",):
                return {"ok": False, "error": f"engine_status={engine.status}"}

            visible = engine.get_visible_bars()
            current_bar = engine.get_current_bar()

            # Convert visible bars list to a dataframe-like structure
            # Use dict-list approach; overlays will try to use pandas if available
            visible_df = _to_df(visible)

            # Opening range overlay
            or_overlay = {}
            try:
                from replay.opening_range_replay import OpeningRangeReplay
                or_overlay = OpeningRangeReplay().build_overlay(visible_df)
            except Exception as exc:
                logger.warning("[Adapter] opening range overlay error: %s", exc)

            # VWAP overlay
            vwap_overlay = {}
            try:
                from replay.vwap_replay import VWAPReplay
                vwap_overlay = VWAPReplay().build_overlay(visible_df)
            except Exception as exc:
                logger.warning("[Adapter] vwap overlay error: %s", exc)

            # Fake breakout overlay
            fb_overlay = {}
            try:
                from replay.fake_breakout_replay import FakeBreakoutReplay
                fb_overlay = FakeBreakoutReplay().build_warning(visible_df)
            except Exception as exc:
                logger.warning("[Adapter] fake breakout overlay error: %s", exc)

            # Volume profile overlay
            vp_overlay = {}
            try:
                from replay.volume_profile_replay import VolumeProfileReplay
                vp_overlay = VolumeProfileReplay().build_profile_so_far(visible_df)
            except Exception as exc:
                logger.warning("[Adapter] volume profile overlay error: %s", exc)

            # Events
            events = []
            try:
                from replay.replay_events import ReplayEventBuilder
                events = ReplayEventBuilder().build_events(visible_df)
                events = [e.to_dict() if hasattr(e, "to_dict") else e for e in events]
            except Exception as exc:
                logger.warning("[Adapter] event build error: %s", exc)

            # Strategy signals
            active_signals = []
            try:
                from replay.strategy_replay import StrategyReplayOverlay
                overlay_obj = StrategyReplayOverlay()
                current_time = str(current_bar.get("datetime", ""))
                overlay_obj.build_overlay(visible_df)
                active_signals = overlay_obj.get_active_signals(current_time)
            except Exception as exc:
                logger.warning("[Adapter] strategy overlay error: %s", exc)

            state = {
                "current_bar": current_bar,
                "bar_index": engine.current_index,
                "total_bars": engine.total_bars,
                "opening_range": or_overlay,
                "vwap": vwap_overlay,
                "fake_breakout": fb_overlay,
                "volume_profile": vp_overlay,
                "events": events,
                "active_signals": active_signals,
                "research_only": True,
                "no_real_orders": True,
                "label": "Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED",
            }
            return {"ok": True, "state": state}

        except Exception as exc:
            logger.error("[IntradayReplayAdapter] build_current_state error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def get_visible_bars(self) -> dict:
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}
            bars = engine.get_visible_bars()
            return {"ok": True, "bars": bars, "research_only": True}
        except Exception as exc:
            logger.error("[IntradayReplayAdapter] get_visible_bars error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    def generate_report(self, mode: str = "real") -> dict:
        try:
            engine = self._get_engine()
            visible = engine.get_visible_bars() if engine else []
            visible_df = _to_df(visible)

            session_summary = {}
            if self._current_session:
                session_summary = self._current_session.to_dict()
            if engine:
                session_summary.update({
                    "total_bars": engine.total_bars,
                    "bars_replayed": engine.current_index,
                })

            # Gather all overlays
            or_overlay, vwap_overlay, fb_overlay, vp_overlay = {}, {}, {}, {}
            events = []
            try:
                from replay.opening_range_replay import OpeningRangeReplay
                or_overlay = OpeningRangeReplay().build_overlay(visible_df)
            except Exception:
                pass
            try:
                from replay.vwap_replay import VWAPReplay
                vwap_overlay = VWAPReplay().build_overlay(visible_df)
            except Exception:
                pass
            try:
                from replay.fake_breakout_replay import FakeBreakoutReplay
                fb_overlay = FakeBreakoutReplay().build_warning(visible_df)
            except Exception:
                pass
            try:
                from replay.volume_profile_replay import VolumeProfileReplay
                vp_overlay = VolumeProfileReplay().build_profile_so_far(visible_df)
            except Exception:
                pass
            try:
                from replay.replay_events import ReplayEventBuilder
                raw_events = ReplayEventBuilder().build_events(visible_df)
                events = [e.to_dict() if hasattr(e, "to_dict") else e for e in raw_events]
            except Exception:
                pass

            # Events summary
            events_summary = {
                "total": len(events),
                "opening_range_count": sum(1 for e in events if e.get("event_type", "").startswith("OPENING")),
                "vwap_count": sum(1 for e in events if "VWAP" in e.get("event_type", "")),
                "fake_breakout_count": sum(1 for e in events if "FAKE" in e.get("event_type", "")),
                "volume_spike_count": sum(1 for e in events if "VOLUME_SPIKE" in e.get("event_type", "")),
                "poc_touch_count": sum(1 for e in events if "POC" in e.get("event_type", "")),
                "signal_trigger_count": sum(1 for e in events if "SIGNAL" in e.get("event_type", "")),
                "events": events,
            }

            from reports.intraday_replay_report import IntradayReplayReportBuilder
            builder = IntradayReplayReportBuilder(report_dir=self._report_dir, mode=mode)
            path = builder.build(
                session_summary=session_summary,
                events_summary=events_summary,
                opening_range_summary=or_overlay,
                vwap_summary=vwap_overlay,
                fake_breakout_summary=fb_overlay,
                volume_profile_summary=vp_overlay,
            )
            return {"ok": True, "report_path": path, "research_only": True}
        except Exception as exc:
            logger.error("[IntradayReplayAdapter] generate_report error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def load_latest_report_path(self) -> Optional[str]:
        try:
            report_dir = os.path.join(BASE_DIR, self._report_dir)
            if not os.path.isdir(report_dir):
                return None
            import glob
            pattern = os.path.join(report_dir, "intraday_replay_report_*.md")
            matches = sorted(glob.glob(pattern), reverse=True)
            return matches[0] if matches else None
        except Exception as exc:
            logger.warning("[IntradayReplayAdapter] load_latest_report_path error: %s", exc)
            return None


# ---------------------------------------------------------------------------
# Helper: convert list of bar dicts to a minimal DataFrame-like object
# ---------------------------------------------------------------------------
def _to_df(bars: list):
    """Convert list of bar dicts to pandas DataFrame, or to a dict-list wrapper."""
    if not bars:
        return _DictListDF([])
    try:
        import pandas as pd
        return pd.DataFrame(bars)
    except ImportError:
        return _DictListDF(bars)
    except Exception:
        return _DictListDF(bars)


class _DictListDF:
    """Minimal pandas-compatible wrapper for list of dicts when pandas is not available."""

    def __init__(self, records: list):
        self._records = records
        if records:
            self.columns = list(records[0].keys())
        else:
            self.columns = []

    def __len__(self):
        return len(self._records)

    def __iter__(self):
        return iter(self._records)

    @property
    def iloc(self):
        return _IlocAccessor(self._records)

    def iterrows(self):
        for i, row in enumerate(self._records):
            yield i, _RowAccessor(row)

    def __getitem__(self, key):
        return _ColumnAccessor([r.get(key) for r in self._records])


class _IlocAccessor:
    def __init__(self, records):
        self._records = records

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return _DictListDF(self._records[idx])
        if isinstance(idx, int):
            return _RowAccessor(self._records[idx])
        return _DictListDF(self._records[idx])


class _RowAccessor:
    def __init__(self, row: dict):
        self._row = row

    def __getitem__(self, key):
        return self._row.get(key)

    def get(self, key, default=None):
        return self._row.get(key, default)


class _ColumnAccessor:
    def __init__(self, values: list):
        self._values = values

    def astype(self, dtype):
        try:
            return _ColumnAccessor([dtype(v) for v in self._values])
        except Exception:
            return self

    def tolist(self):
        return self._values

    def max(self):
        vals = [v for v in self._values if v is not None]
        return max(vals) if vals else None

    def min(self):
        vals = [v for v in self._values if v is not None]
        return min(vals) if vals else None
