"""replay_training/replay_score_engine.py — ReplayScoreEngine for TW Replay Training Cockpit v0.5.6.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Score breakdown weights (total: 100)
# ---------------------------------------------------------------------------
_WEIGHTS = {
    "entry_quality":           25,
    "exit_stop_discipline":    20,
    "fake_breakout_avoidance": 15,
    "vwap_opening_range":      15,
    "strategy_adherence":      15,
    "notes_completeness":      10,
}


def _safe_float(bar: dict, key: str, default: float = 0.0) -> float:
    try:
        return float(bar.get(key, default) or default)
    except (ValueError, TypeError):
        return default


def _get_vwap(bar: dict) -> float:
    for k in ["vwap", "VWAP"]:
        v = bar.get(k)
        if v is not None:
            try:
                return float(v)
            except (ValueError, TypeError):
                pass
    return 0.0


class ReplayScoreEngine:
    """Computes a 0-100 training score for a replay session.

    Score breakdown:
      - Entry quality:           25pts (near VWAP/support = high, chase/fake = low)
      - Exit/stop discipline:    20pts (has stop marker = high, late_stop = low)
      - Fake breakout avoidance: 15pts
      - VWAP/opening range:      15pts
      - Strategy adherence:      15pts
      - Notes completeness:      10pts

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        pass

    def score_session(
        self,
        session,
        bars: List[dict],
        markers: list,
        mistakes: list,
    ) -> dict:
        """Compute full score breakdown for a session."""
        try:
            breakdown = {}

            # --- Entry quality (25pts) ---
            breakdown["entry_quality"] = self._score_entry_quality(bars, markers, mistakes)

            # --- Exit/stop discipline (20pts) ---
            breakdown["exit_stop_discipline"] = self._score_exit_stop(bars, markers, mistakes)

            # --- Fake breakout avoidance (15pts) ---
            breakdown["fake_breakout_avoidance"] = self._score_fake_breakout(mistakes)

            # --- VWAP/opening range compliance (15pts) ---
            breakdown["vwap_opening_range"] = self._score_vwap_or(bars, markers, mistakes)

            # --- Strategy adherence (15pts) ---
            breakdown["strategy_adherence"] = self._score_strategy(mistakes)

            # --- Notes completeness (10pts) ---
            breakdown["notes_completeness"] = self._score_notes(session, markers)

            total = sum(breakdown.values())
            total = max(0.0, min(100.0, total))

            grade = self._grade(total)
            interpretation = self._interpretation(total, mistakes)

            return {
                "total_score":     round(total, 1),
                "breakdown":       {k: round(v, 1) for k, v in breakdown.items()},
                "interpretation":  interpretation,
                "grade":           grade,
                "max_score":       100,
                "weights":         _WEIGHTS,
                "no_real_orders":  True,
                "replay_training_only": True,
            }

        except Exception as exc:
            logger.error("[ReplayScoreEngine] score_session error: %s", exc)
            return {
                "total_score":    0.0,
                "breakdown":      {},
                "interpretation": f"Scoring failed: {exc}",
                "grade":          "F",
                "no_real_orders": True,
            }

    # ------------------------------------------------------------------
    # Sub-scorers
    # ------------------------------------------------------------------

    def _score_entry_quality(self, bars: List[dict], markers: list, mistakes: list) -> float:
        from replay_training.replay_training_schema import MARKER_ENTRY
        entry_markers = [m for m in markers if m.marker_type == MARKER_ENTRY]
        if not entry_markers:
            return _WEIGHTS["entry_quality"] * 0.5  # neutral if no markers

        chase_count = sum(1 for m in mistakes if m.mistake_type == "chase_high")
        fb_count    = sum(1 for m in mistakes if m.mistake_type == "ignored_fake_breakout")

        penalty = (chase_count + fb_count) * 8.0
        return max(0.0, _WEIGHTS["entry_quality"] - penalty)

    def _score_exit_stop(self, bars: List[dict], markers: list, mistakes: list) -> float:
        from replay_training.replay_training_schema import MARKER_STOP_LOSS, MARKER_EXIT
        has_stop = any(m.marker_type == MARKER_STOP_LOSS for m in markers)
        has_exit = any(m.marker_type == MARKER_EXIT        for m in markers)

        late_stops     = sum(1 for m in mistakes if m.mistake_type == "late_stop_loss")
        early_exits    = sum(1 for m in mistakes if m.mistake_type == "early_take_profit")
        ignored_stops  = sum(1 for m in mistakes if m.mistake_type == "ignored_stop")

        score = _WEIGHTS["exit_stop_discipline"]
        if not has_stop:
            score -= 10.0
        if not has_exit:
            score -= 5.0
        score -= late_stops     * 7.0
        score -= early_exits    * 4.0
        score -= ignored_stops  * 5.0
        return max(0.0, score)

    def _score_fake_breakout(self, mistakes: list) -> float:
        fb_mistakes = sum(1 for m in mistakes if m.mistake_type == "ignored_fake_breakout")
        penalty = fb_mistakes * 7.0
        return max(0.0, _WEIGHTS["fake_breakout_avoidance"] - penalty)

    def _score_vwap_or(self, bars: List[dict], markers: list, mistakes: list) -> float:
        vwap_mistakes = sum(1 for m in mistakes if m.mistake_type in (
            "ignored_vwap_loss", "ignored_opening_range_fail"
        ))
        penalty = vwap_mistakes * 7.0
        return max(0.0, _WEIGHTS["vwap_opening_range"] - penalty)

    def _score_strategy(self, mistakes: list) -> float:
        strat_mistakes = sum(1 for m in mistakes if m.mistake_type == "violated_strategy")
        penalty = strat_mistakes * 7.0
        return max(0.0, _WEIGHTS["strategy_adherence"] - penalty)

    def _score_notes(self, session, markers: list) -> float:
        """Notes completeness: 10pts for having notes and markers."""
        note_count   = getattr(session, "notes_count",   0)
        marker_count = getattr(session, "markers_count", len(markers))
        # 5pts for notes, 5pts for markers
        notes_pts   = 5.0 if note_count   >= 1 else 2.0 * note_count
        markers_pts = 5.0 if marker_count >= 2 else 2.5 * marker_count
        return min(_WEIGHTS["notes_completeness"], notes_pts + markers_pts)

    # ------------------------------------------------------------------
    # Grade / interpretation
    # ------------------------------------------------------------------

    def _grade(self, score: float) -> str:
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B+"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 40:
            return "D"
        else:
            return "F"

    def _interpretation(self, score: float, mistakes: list) -> str:
        n = len(mistakes)
        if score >= 80:
            return f"Excellent session ({score:.0f}/100). {n} mistake(s). Keep training!"
        elif score >= 60:
            return f"Good session ({score:.0f}/100). {n} mistake(s). Focus on flagged areas."
        elif score >= 40:
            return f"Developing ({score:.0f}/100). {n} mistake(s). Review drill suggestions."
        else:
            return f"Needs work ({score:.0f}/100). {n} mistake(s). Prioritize drill training."
