"""replay_training/ai_replay_reviewer.py — AIReplayReviewer for TW Replay Training Cockpit v0.5.6.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Rule-based only. NO external LLM API. No network calls. No broker connection.
[!] No BUY/SELL/ORDER outputs. Allowed actions are training suggestions only.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Allowed suggested actions — training-only (no trade execution)
# ---------------------------------------------------------------------------
SUGGESTED_ACTIONS = [
    "PRACTICE_MORE",
    "REVIEW_MISTAKE",
    "WAIT_CONFIRMATION",
    "IMPROVE_STOP_DISCIPLINE",
    "AVOID_CHASING",
    "TRAIN_VWAP",
    "TRAIN_FAKE_BREAKOUT",
    "TRAIN_OPENING_RANGE",
]


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


class AIReplayReviewer:
    """Rule-based AI reviewer for replay training sessions.

    Implements 7 detection rules. No external API calls. No broker connection.
    No BUY/SELL/ORDER outputs.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, marker_store=None) -> None:
        self._marker_store = marker_store

    # ------------------------------------------------------------------
    # Public: review session
    # ------------------------------------------------------------------

    def review_session(
        self,
        session_id: str,
        bars: List[dict],
        markers: list,
        strategy_context: Optional[dict] = None,
    ):
        """Run full rule-based AI review of a replay session.

        Returns ReplayAIReview (no BUY/SELL/ORDER outputs).
        """
        from replay_training.replay_training_schema import ReplayAIReview

        try:
            mistakes   = self.detect_mistakes(bars, markers)
            entry_qual = self.evaluate_entry_quality(bars, markers)
            exit_qual  = self.evaluate_exit_quality(bars, markers)
            strat_viol = self.evaluate_strategy_violations(bars, markers, strategy_context or {})
            score      = self._compute_score(markers, mistakes)
            feedback   = self.build_feedback(mistakes, score)

            # Build entry/exit summaries (no ORDER output)
            best_entry  = entry_qual.get("best_entry_desc", "N/A")
            worst_entry = entry_qual.get("worst_entry_desc", "N/A")
            best_exit   = exit_qual.get("best_exit_desc", "N/A")
            worst_exit  = exit_qual.get("worst_exit_desc", "N/A")

            mistakes_summary    = "; ".join(m.mistake_type for m in mistakes) if mistakes else "None detected"
            violations_summary  = "; ".join(v.get("violation", "") for v in strat_viol) if strat_viol else "None"
            tape_feedback       = feedback.get("tape_reading_feedback", "")
            next_focus          = feedback.get("next_training_focus", "")
            drills_summary      = "; ".join(feedback.get("suggested_drills", []))

            symbol     = markers[0].symbol     if markers else ""
            trade_date = markers[0].trade_date if markers else ""

            review = ReplayAIReview(
                review_id=f"REV-{uuid.uuid4().hex[:8].upper()}",
                session_id=session_id,
                symbol=symbol,
                trade_date=trade_date,
                summary=self._build_summary(mistakes, score),
                best_entry=best_entry,
                worst_entry=worst_entry,
                best_exit=best_exit,
                worst_exit=worst_exit,
                detected_mistakes=mistakes_summary,
                strategy_violations=violations_summary,
                tape_reading_feedback=tape_feedback,
                next_training_focus=next_focus,
                suggested_drills=drills_summary,
                score=score,
                created_at=datetime.now().isoformat(),
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
            )
            return review

        except Exception as exc:
            logger.error("[AIReplayReviewer] review_session error: %s", exc)
            from replay_training.replay_training_schema import ReplayAIReview
            return ReplayAIReview(
                review_id=f"REV-{uuid.uuid4().hex[:8].upper()}",
                session_id=session_id,
                symbol="",
                trade_date="",
                summary=f"Review failed: {exc}",
                score=0.0,
                created_at=datetime.now().isoformat(),
                read_only=True,
                no_real_orders=True,
                production_blocked=True,
            )

    # ------------------------------------------------------------------
    # Rule 1: chase_high
    # ------------------------------------------------------------------

    def detect_mistakes(self, bars: List[dict], markers: list) -> list:
        """Detect all mistakes using rule-based checks."""
        from replay_training.replay_training_schema import (
            ReplayMistake,
            MARKER_ENTRY, MARKER_EXIT, MARKER_STOP_LOSS,
            MISTAKE_CHASE_HIGH, MISTAKE_IGNORED_VWAP_LOSS,
            MISTAKE_IGNORED_FAKE_BREAKOUT, MISTAKE_IGNORED_OPENING_RANGE_FAIL,
            MISTAKE_EARLY_TAKE_PROFIT, MISTAKE_LATE_STOP_LOSS,
            MISTAKE_VIOLATED_STRATEGY,
        )

        mistakes = []
        entry_markers = [m for m in markers if m.marker_type == MARKER_ENTRY]
        exit_markers  = [m for m in markers if m.marker_type == MARKER_EXIT]
        stop_markers  = [m for m in markers if m.marker_type == MARKER_STOP_LOSS]

        # Rule 1: chase_high — entry after 3+ consecutive up bars AND price > VWAP * 1.01
        for em in entry_markers:
            idx = em.bar_index
            if idx >= 3 and idx < len(bars):
                lookback = bars[max(0, idx - 3): idx]
                up_bars  = sum(
                    1 for b in lookback
                    if _safe_float(b, "close") > _safe_float(b, "open")
                )
                entry_price = em.price or _safe_float(bars[idx], "close")
                vwap        = _get_vwap(bars[idx])
                if up_bars >= 3 and vwap > 0 and entry_price > vwap * 1.01:
                    mistakes.append(ReplayMistake(
                        mistake_id=f"M-{uuid.uuid4().hex[:6].upper()}",
                        session_id=em.session_id,
                        mistake_type=MISTAKE_CHASE_HIGH,
                        bar_time=em.bar_time,
                        price=entry_price,
                        severity="high",
                        description=(
                            f"Entry at {entry_price:.2f} chased high: "
                            f"{up_bars} consecutive up bars before entry, "
                            f"price was {(entry_price/vwap - 1)*100:.1f}% above VWAP ({vwap:.2f})."
                        ),
                        suggested_fix="AVOID_CHASING — wait for pullback to VWAP or support before entry.",
                        related_marker_id=em.marker_id,
                    ))

        # Rule 2: ignored_vwap_loss — entry followed by close below VWAP, no stop added within 3 bars
        for em in entry_markers:
            idx = em.bar_index
            found_stop_near = any(
                sm.bar_index <= idx + 3 for sm in stop_markers
            )
            if not found_stop_near and idx + 1 < len(bars):
                for j in range(idx + 1, min(idx + 4, len(bars))):
                    b    = bars[j]
                    c    = _safe_float(b, "close")
                    vwap = _get_vwap(b)
                    if vwap > 0 and c < vwap:
                        mistakes.append(ReplayMistake(
                            mistake_id=f"M-{uuid.uuid4().hex[:6].upper()}",
                            session_id=em.session_id,
                            mistake_type=MISTAKE_IGNORED_VWAP_LOSS,
                            bar_time=str(b.get("datetime", b.get("time", j))),
                            price=c,
                            severity="high",
                            description=(
                                f"VWAP loss at bar {j}: price closed below VWAP ({vwap:.2f}) "
                                f"with no stop marker added within 3 bars of entry."
                            ),
                            suggested_fix="IMPROVE_STOP_DISCIPLINE — add stop marker when price loses VWAP.",
                            related_marker_id=em.marker_id,
                        ))
                        break

        # Rule 3: ignored_fake_breakout — breakout bar retraced within 3 bars, user had ENTRY on breakout
        try:
            from replay_training.tape_reading_detector import TapeReadingDetector
            detector = TapeReadingDetector()
            fb_events = detector.detect_fake_breakout(bars)
            for ev in fb_events:
                ev_idx = ev.get("bar_index", 0)
                for em in entry_markers:
                    if abs(em.bar_index - ev_idx) <= 1:
                        mistakes.append(ReplayMistake(
                            mistake_id=f"M-{uuid.uuid4().hex[:6].upper()}",
                            session_id=em.session_id,
                            mistake_type=MISTAKE_IGNORED_FAKE_BREAKOUT,
                            bar_time=ev.get("bar_time", ""),
                            price=em.price,
                            severity="high",
                            description=(
                                f"Entry on a fake breakout at bar {ev_idx}. "
                                f"Breakout bar reversed within 3 bars."
                            ),
                            suggested_fix="TRAIN_FAKE_BREAKOUT — look for volume confirmation before entry.",
                            related_marker_id=em.marker_id,
                        ))
        except Exception as exc:
            logger.warning("[AIReplayReviewer] fake_breakout rule error: %s", exc)

        # Rule 4: ignored_opening_range_fail
        try:
            from replay_training.tape_reading_detector import TapeReadingDetector
            orf_events = TapeReadingDetector().detect_opening_range_fail(bars)
            for ev in orf_events:
                ev_idx = ev.get("bar_index", 0)
                for em in entry_markers:
                    if em.bar_index >= ev_idx - 2 and em.bar_index <= ev_idx:
                        mistakes.append(ReplayMistake(
                            mistake_id=f"M-{uuid.uuid4().hex[:6].upper()}",
                            session_id=em.session_id,
                            mistake_type=MISTAKE_IGNORED_OPENING_RANGE_FAIL,
                            bar_time=ev.get("bar_time", ""),
                            price=em.price,
                            severity="medium",
                            description=(
                                f"Entry near opening range fail event at bar {ev_idx}. "
                                f"Opening range break failed — price fell back."
                            ),
                            suggested_fix="TRAIN_OPENING_RANGE — wait for OR hold before adding.",
                            related_marker_id=em.marker_id,
                        ))
        except Exception as exc:
            logger.warning("[AIReplayReviewer] opening_range_fail rule error: %s", exc)

        # Rule 5: early_take_profit — EXIT followed by price continuing up 2%+
        from replay_training.replay_training_schema import MARKER_EXIT as ME
        for xm in exit_markers:
            idx        = xm.bar_index
            exit_price = xm.price or (_safe_float(bars[idx], "close") if idx < len(bars) else 0)
            if exit_price > 0:
                for j in range(idx + 1, min(idx + 10, len(bars))):
                    future_close = _safe_float(bars[j], "close")
                    if future_close > exit_price * 1.02:
                        # Check no weakness signal (long upper shadow or VWAP loss)
                        weakness = False
                        for k in range(idx, j):
                            b    = bars[k]
                            high = _safe_float(b, "high")
                            cls  = _safe_float(b, "close")
                            opn  = _safe_float(b, "open")
                            body = abs(cls - opn)
                            shadow = high - max(cls, opn)
                            if shadow > body * 1.5:
                                weakness = True
                                break
                        if not weakness:
                            mistakes.append(ReplayMistake(
                                mistake_id=f"M-{uuid.uuid4().hex[:6].upper()}",
                                session_id=xm.session_id,
                                mistake_type=MISTAKE_EARLY_TAKE_PROFIT,
                                bar_time=xm.bar_time,
                                price=exit_price,
                                severity="medium",
                                description=(
                                    f"Early exit at {exit_price:.2f}: price continued to "
                                    f"{future_close:.2f} (+{(future_close/exit_price-1)*100:.1f}%) "
                                    f"with no weakness signal."
                                ),
                                suggested_fix="WAIT_CONFIRMATION — hold through minor retracements.",
                                related_marker_id=xm.marker_id,
                            ))
                        break

        # Rule 6: late_stop_loss — price dropped 3%+ below entry before stop/exit
        for em in entry_markers:
            idx        = em.bar_index
            entry_price = em.price or (_safe_float(bars[idx], "close") if idx < len(bars) else 0)
            if entry_price <= 0:
                continue
            stop_exit_after = [
                m for m in (stop_markers + exit_markers)
                if m.bar_index > idx
            ]
            first_stop = min((m.bar_index for m in stop_exit_after), default=len(bars))
            for j in range(idx + 1, min(first_stop, len(bars))):
                low = _safe_float(bars[j], "low")
                if low > 0 and low < entry_price * 0.97:
                    mistakes.append(ReplayMistake(
                        mistake_id=f"M-{uuid.uuid4().hex[:6].upper()}",
                        session_id=em.session_id,
                        mistake_type=MISTAKE_LATE_STOP_LOSS,
                        bar_time=str(bars[j].get("datetime", bars[j].get("time", j))),
                        price=low,
                        severity="high",
                        description=(
                            f"Late stop: price dropped to {low:.2f} "
                            f"({(1 - low/entry_price)*100:.1f}% below entry {entry_price:.2f}) "
                            f"before any stop/exit marker."
                        ),
                        suggested_fix="IMPROVE_STOP_DISCIPLINE — pre-plan stop loss before entry.",
                        related_marker_id=em.marker_id,
                    ))
                    break

        # Rule 7: violated_strategy — strategy_context says WAIT_PULLBACK but user had ENTRY on up-bar
        # (handled in evaluate_strategy_violations)

        return mistakes

    # ------------------------------------------------------------------
    # Entry/exit quality
    # ------------------------------------------------------------------

    def evaluate_entry_quality(self, bars: List[dict], markers: list) -> dict:
        from replay_training.replay_training_schema import MARKER_ENTRY
        entry_markers = [m for m in markers if m.marker_type == MARKER_ENTRY]
        if not entry_markers:
            return {
                "best_entry_desc":  "No entry markers placed",
                "worst_entry_desc": "No entry markers placed",
                "entry_count":      0,
            }

        # Score each entry by distance from VWAP
        scored = []
        for em in entry_markers:
            idx = em.bar_index
            if idx < len(bars):
                b    = bars[idx]
                c    = _safe_float(b, "close")
                vwap = _get_vwap(b)
                dist = abs(c - vwap) / vwap if vwap > 0 else 1.0
                scored.append((dist, em))

        scored.sort(key=lambda x: x[0])
        best  = scored[0][1]  if scored else None
        worst = scored[-1][1] if scored else None

        return {
            "best_entry_desc":  f"Bar {best.bar_index} @ {best.price:.2f} (near VWAP)" if best  else "N/A",
            "worst_entry_desc": f"Bar {worst.bar_index} @ {worst.price:.2f} (far from VWAP)" if worst else "N/A",
            "entry_count":      len(entry_markers),
        }

    def evaluate_exit_quality(self, bars: List[dict], markers: list) -> dict:
        from replay_training.replay_training_schema import MARKER_EXIT
        exit_markers = [m for m in markers if m.marker_type == MARKER_EXIT]
        if not exit_markers:
            return {
                "best_exit_desc":  "No exit markers placed",
                "worst_exit_desc": "No exit markers placed",
                "exit_count":      0,
            }

        # Score exits by price (higher is better for long)
        scored = [(em.price or 0.0, em) for em in exit_markers]
        scored.sort(key=lambda x: x[0], reverse=True)
        best  = scored[0][1]  if scored else None
        worst = scored[-1][1] if scored else None

        return {
            "best_exit_desc":  f"Bar {best.bar_index} @ {best.price:.2f}" if best  else "N/A",
            "worst_exit_desc": f"Bar {worst.bar_index} @ {worst.price:.2f}" if worst else "N/A",
            "exit_count":      len(exit_markers),
        }

    def evaluate_strategy_violations(
        self, bars: List[dict], markers: list, strategy_context: dict
    ) -> List[dict]:
        """Check for strategy violations based on strategy_context rules."""
        from replay_training.replay_training_schema import MARKER_ENTRY, ReplayMistake, MISTAKE_VIOLATED_STRATEGY
        violations = []
        if not strategy_context:
            return violations

        entry_markers = [m for m in markers if m.marker_type == MARKER_ENTRY]
        # Rule: WAIT_PULLBACK in strategy but user entered on up-bar
        if strategy_context.get("WAIT_PULLBACK"):
            for em in entry_markers:
                idx = em.bar_index
                if idx < len(bars):
                    b = bars[idx]
                    if _safe_float(b, "close") > _safe_float(b, "open"):
                        violations.append({
                            "violation":    "WAIT_PULLBACK violated",
                            "bar_index":    idx,
                            "description":  (
                                f"Entry on up-bar (bar {idx}) violates WAIT_PULLBACK strategy rule. "
                                f"Strategy requires pullback confirmation before entry."
                            ),
                            "suggested_fix": "WAIT_CONFIRMATION",
                        })

        return violations

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def _compute_score(self, markers: list, mistakes: list) -> float:
        """Simple score: 100 - (10 * high mistakes) - (5 * medium mistakes)."""
        high_count   = sum(1 for m in mistakes if m.severity == "high")
        medium_count = sum(1 for m in mistakes if m.severity == "medium")
        score = 100.0 - (high_count * 10.0) - (medium_count * 5.0)
        return max(0.0, min(100.0, score))

    # ------------------------------------------------------------------
    # Feedback builder
    # ------------------------------------------------------------------

    def build_feedback(self, mistakes: list, score: float) -> dict:
        """Build training feedback from mistakes and score."""
        tape_parts = []
        drills     = []
        focus      = []

        type_set = {m.mistake_type for m in mistakes}

        if "chase_high" in type_set:
            tape_parts.append("Avoid chasing breakouts without VWAP/support confirmation.")
            drills.append("TRAIN_VWAP")
            focus.append("VWAP pullback entries")
        if "ignored_vwap_loss" in type_set:
            tape_parts.append("Add stop markers immediately when price loses VWAP.")
            drills.append("TRAIN_VWAP")
            focus.append("VWAP stop discipline")
        if "ignored_fake_breakout" in type_set:
            tape_parts.append("Identify fake breakouts using volume + wick analysis.")
            drills.append("TRAIN_FAKE_BREAKOUT")
            focus.append("Fake breakout recognition")
        if "ignored_opening_range_fail" in type_set:
            tape_parts.append("Wait for OR hold before adding near opening range break.")
            drills.append("TRAIN_OPENING_RANGE")
            focus.append("Opening range discipline")
        if "early_take_profit" in type_set:
            tape_parts.append("Avoid exiting prematurely — wait for weakness signal.")
            drills.append("PRACTICE_MORE")
            focus.append("Exit timing")
        if "late_stop_loss" in type_set:
            tape_parts.append("Pre-plan stop loss level before every entry.")
            drills.append("IMPROVE_STOP_DISCIPLINE")
            focus.append("Stop placement discipline")
        if "violated_strategy" in type_set:
            tape_parts.append("Follow strategy rules — do not override with impulse entries.")
            drills.append("REVIEW_MISTAKE")
            focus.append("Strategy adherence")

        if score >= 80:
            tape_parts.append("Overall solid session — keep practicing to maintain consistency.")
        elif score >= 60:
            tape_parts.append("Room for improvement — focus on the areas flagged above.")
        else:
            tape_parts.append("Several key mistakes detected — prioritize drill training.")

        tape_feedback = " ".join(tape_parts) if tape_parts else "No specific feedback."
        next_focus    = ", ".join(dict.fromkeys(focus)) if focus else "General tape reading practice"
        unique_drills = list(dict.fromkeys(drills))

        return {
            "tape_reading_feedback": tape_feedback,
            "next_training_focus":   next_focus,
            "suggested_drills":      unique_drills,
        }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def _build_summary(self, mistakes: list, score: float) -> str:
        n = len(mistakes)
        if n == 0:
            return f"Clean session — no mistakes detected. Score: {score:.0f}/100."
        high = sum(1 for m in mistakes if m.severity == "high")
        med  = sum(1 for m in mistakes if m.severity == "medium")
        return (
            f"Detected {n} mistake(s): {high} high severity, {med} medium severity. "
            f"Score: {score:.0f}/100. "
            f"[Replay Training Only / No Real Orders]"
        )
