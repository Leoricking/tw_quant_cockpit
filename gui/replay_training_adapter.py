"""gui/replay_training_adapter.py — ReplayTrainingAdapter for TW Replay Training Cockpit v0.5.6.

GUI adapter bridge — wraps all replay training modules. Returns dicts for GUI consumption.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No BUY/SELL/ORDER outputs. No broker connection.
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ReplayTrainingAdapter:
    """Bridges GUI panel to all replay training modules.

    All methods are wrapped in try/except — never crash. Lazy imports.
    Returns dicts (not objects) for GUI consumption.
    No real orders. No broker connection.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        output_dir: str = "data/backtest_results/replay_training",
        report_dir: str = "reports",
    ) -> None:
        self._output_dir = output_dir
        self._report_dir = report_dir
        self._engine        = None
        self._marker_store  = None
        self._ai_reviewer   = None
        self._score_engine  = None
        self._drill_builder = None
        self._store         = None
        self._current_session_id: Optional[str] = None
        self._current_session    = None
        self._current_bars       = []
        self._current_markers    = []
        self._current_mistakes   = []
        self._current_ai_review  = None
        self._current_score      = {}
        self._current_drills     = []

    # ------------------------------------------------------------------
    # Lazy init helpers
    # ------------------------------------------------------------------

    def _get_engine(self):
        if self._engine is None:
            try:
                from replay_training.replay_bar_engine import ReplayBarEngine
                self._engine = ReplayBarEngine(output_dir=self._output_dir)
            except Exception as exc:
                logger.error("[ReplayTrainingAdapter] engine init error: %s", exc)
        return self._engine

    def _get_marker_store(self):
        if self._marker_store is None:
            try:
                from replay_training.replay_marker_store import ReplayMarkerStore
                self._marker_store = ReplayMarkerStore(output_dir=self._output_dir)
            except Exception as exc:
                logger.error("[ReplayTrainingAdapter] marker_store init error: %s", exc)
        return self._marker_store

    def _get_ai_reviewer(self):
        if self._ai_reviewer is None:
            try:
                from replay_training.ai_replay_reviewer import AIReplayReviewer
                self._ai_reviewer = AIReplayReviewer(marker_store=self._get_marker_store())
            except Exception as exc:
                logger.error("[ReplayTrainingAdapter] ai_reviewer init error: %s", exc)
        return self._ai_reviewer

    def _get_score_engine(self):
        if self._score_engine is None:
            try:
                from replay_training.replay_score_engine import ReplayScoreEngine
                self._score_engine = ReplayScoreEngine()
            except Exception as exc:
                logger.error("[ReplayTrainingAdapter] score_engine init error: %s", exc)
        return self._score_engine

    def _get_drill_builder(self):
        if self._drill_builder is None:
            try:
                from replay_training.replay_drill_builder import ReplayDrillBuilder
                self._drill_builder = ReplayDrillBuilder()
            except Exception as exc:
                logger.error("[ReplayTrainingAdapter] drill_builder init error: %s", exc)
        return self._drill_builder

    def _get_store(self):
        if self._store is None:
            try:
                from replay_training.replay_training_store import ReplayTrainingStore
                self._store = ReplayTrainingStore(output_dir=self._output_dir)
            except Exception as exc:
                logger.error("[ReplayTrainingAdapter] store init error: %s", exc)
        return self._store

    # ------------------------------------------------------------------
    # Session control
    # ------------------------------------------------------------------

    def create_session(
        self,
        symbol: str,
        trade_date: str,
        timeframe: str = "1min",
        mode: str = "real",
    ) -> dict:
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}
            session = engine.create_session(symbol, trade_date, timeframe, mode)
            self._current_session_id = session.session_id
            self._current_session    = session
            self._current_bars       = engine.load_session_data(symbol, trade_date, timeframe)
            self._current_markers    = []
            self._current_mistakes   = []
            self._current_ai_review  = None
            self._current_score      = {}
            self._current_drills     = []
            return {
                "ok":               True,
                "session":          session.to_dict(),
                "no_real_orders":   True,
                "replay_training_only": True,
            }
        except Exception as exc:
            logger.error("[ReplayTrainingAdapter] create_session error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def next_bar(self, session_id: str) -> dict:
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}
            result = engine.next_bar(session_id)
            result["no_real_orders"]     = True
            result["replay_training_only"] = True
            return result
        except Exception as exc:
            logger.error("[ReplayTrainingAdapter] next_bar error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def prev_bar(self, session_id: str) -> dict:
        try:
            engine = self._get_engine()
            if engine is None:
                return {"ok": False, "error": "engine_unavailable"}
            result = engine.prev_bar(session_id)
            result["no_real_orders"]     = True
            result["replay_training_only"] = True
            return result
        except Exception as exc:
            logger.error("[ReplayTrainingAdapter] prev_bar error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Markers
    # ------------------------------------------------------------------

    def add_marker(
        self,
        session_id: str,
        marker_type: str,
        price: Optional[float] = None,
        note: str = "",
    ) -> dict:
        try:
            from replay_training.replay_training_schema import ReplayMarker
            engine = self._get_engine()
            session = self._current_session
            if session is None:
                return {"ok": False, "error": "no_active_session"}

            bars = engine.get_visible_bars(session_id) if engine else []
            bar_index = session.current_bar_index
            bar_time  = ""
            if bars and bar_index < len(bars):
                b = bars[bar_index]
                bar_time = str(b.get("datetime", b.get("time", b.get("date", bar_index))))

            marker = ReplayMarker(
                marker_id=f"MK-{uuid.uuid4().hex[:8].upper()}",
                session_id=session_id,
                symbol=session.symbol,
                trade_date=session.trade_date,
                bar_time=bar_time,
                bar_index=bar_index,
                marker_type=marker_type,
                price=price or 0.0,
                note=note,
                created_at=datetime.now().isoformat(),
                no_real_orders=True,
            )
            ms = self._get_marker_store()
            if ms:
                ms.add_marker(marker)
            self._current_markers.append(marker)
            session.markers_count = len(self._current_markers)
            return {
                "ok":      True,
                "marker":  marker.to_dict(),
                "no_real_orders": True,
            }
        except Exception as exc:
            logger.error("[ReplayTrainingAdapter] add_marker error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # AI Review
    # ------------------------------------------------------------------

    def run_ai_review(self, session_id: str) -> dict:
        try:
            reviewer = self._get_ai_reviewer()
            engine   = self._get_engine()
            if reviewer is None:
                return {"ok": False, "error": "reviewer_unavailable"}

            bars    = self._current_bars
            markers = self._current_markers

            review   = reviewer.review_session(session_id, bars, markers)
            mistakes = reviewer.detect_mistakes(bars, markers)

            self._current_ai_review = review
            self._current_mistakes  = mistakes

            # Score
            se = self._get_score_engine()
            if se and self._current_session:
                score = se.score_session(self._current_session, bars, markers, mistakes)
                self._current_score = score
                self._current_session.score = score.get("total_score", 0.0)
                self._current_session.mistakes_count = len(mistakes)
            else:
                score = {}

            # Drills
            db = self._get_drill_builder()
            if db:
                drills = db.build_drills(mistakes, review)
                self._current_drills = drills
            else:
                drills = []

            return {
                "ok":          True,
                "review":      review.to_dict() if review else {},
                "mistakes":    [m.to_dict() for m in mistakes],
                "score":       score,
                "drills":      drills,
                "no_real_orders": True,
                "replay_training_only": True,
            }
        except Exception as exc:
            logger.error("[ReplayTrainingAdapter] run_ai_review error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def generate_report(self, mode: str = "real") -> dict:
        try:
            from reports.replay_training_report import ReplayTrainingReport
            rpt = ReplayTrainingReport()
            content = rpt.generate(
                session=self._current_session,
                markers=self._current_markers,
                mistakes=self._current_mistakes,
                ai_review=self._current_ai_review,
                score=self._current_score,
                drills=self._current_drills,
                mode=mode,
            )
            path = rpt.save(content, report_dir=self._report_dir)

            # Persist to store
            store = self._get_store()
            if store and self._current_session:
                store.save_session(self._current_session)
                store.save_markers(self._current_markers)
                store.save_mistakes(self._current_mistakes)
                if self._current_ai_review:
                    store.save_ai_review(self._current_ai_review)
                if self._current_score:
                    store.save_score(self._current_score)
                if self._current_drills:
                    store.save_drills(self._current_drills)
                store.save_summary({
                    "latest_session_id":        self._current_session.session_id,
                    "latest_symbol":            self._current_session.symbol,
                    "latest_score":             self._current_session.score,
                    "mistakes_count":           len(self._current_mistakes),
                    "drills_count":             len(self._current_drills),
                    "hidden_future_data":       True,
                    "latest_replay_training_at": datetime.now().isoformat(),
                    "no_real_orders":           True,
                })

            return {
                "ok":          True,
                "report_path": path,
                "no_real_orders": True,
                "replay_training_only": True,
            }
        except Exception as exc:
            logger.error("[ReplayTrainingAdapter] generate_report error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Journal export
    # ------------------------------------------------------------------

    def export_to_journal(self, session_id: str) -> dict:
        try:
            from replay_training.replay_journal_bridge import ReplayJournalBridge
            bridge = ReplayJournalBridge()
            result = bridge.export_to_journal(
                self._current_session,
                self._current_ai_review,
                self._current_mistakes,
            )
            return result
        except Exception as exc:
            logger.error("[ReplayTrainingAdapter] export_to_journal error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Summary / report path
    # ------------------------------------------------------------------

    def load_latest_summary(self) -> dict:
        try:
            store = self._get_store()
            if store is None:
                return {"ok": False, "error": "store_unavailable"}
            return store.load_latest_summary()
        except Exception as exc:
            logger.error("[ReplayTrainingAdapter] load_latest_summary error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def load_latest_report_path(self) -> Optional[str]:
        try:
            import glob
            abs_dir = os.path.join(BASE_DIR, self._report_dir)
            pattern = os.path.join(abs_dir, "replay_training_report_*.md")
            matches = sorted(glob.glob(pattern), reverse=True)
            return matches[0] if matches else None
        except Exception as exc:
            logger.warning("[ReplayTrainingAdapter] load_latest_report_path error: %s", exc)
            return None
