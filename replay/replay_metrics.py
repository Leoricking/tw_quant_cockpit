"""replay/replay_metrics.py — Replay Session Metrics calculator (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def _safe_float(val, default: float = 0.0) -> float:
    try:
        return float(val)
    except Exception:
        return default


def _parse_dt(s: str) -> Optional[datetime]:
    if not s:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    return None


def _grade_from_score(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


class ReplayMetrics:
    """Computes aggregate metrics for a completed replay session.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    """

    read_only = True
    no_real_orders = True

    def __init__(self):
        pass

    def calculate_session_metrics(
        self,
        session,
        events: Optional[list] = None,
        answers: Optional[list] = None,
    ) -> dict:
        """Calculate metrics from session, events, and answers.

        No crash if session is None or events is None.
        """
        empty = {
            "bars_replayed": 0,
            "session_duration_seconds": 0.0,
            "events_detected": 0,
            "questions_answered": 0,
            "quiz_accuracy": 0.0,
            "fake_breakout_warnings": 0,
            "vwap_reclaims": 0,
            "chase_risk_events": 0,
            "user_annotations": 0,
            "training_score": 0.0,
            "grade": "F",
            "research_only": True,
            "no_real_orders": True,
        }

        if session is None:
            return empty

        # Bars replayed
        try:
            bars_replayed = int(session.current_index if hasattr(session, "current_index")
                                else session.get("current_index", 0))
        except Exception:
            bars_replayed = 0

        # Session duration
        try:
            started_str = session.started_at if hasattr(session, "started_at") else session.get("started_at", "")
            finished_str = session.finished_at if hasattr(session, "finished_at") else session.get("finished_at", "")
            start_dt = _parse_dt(started_str)
            end_dt = _parse_dt(finished_str)
            if start_dt and end_dt:
                duration_secs = (end_dt - start_dt).total_seconds()
            else:
                duration_secs = 0.0
        except Exception:
            duration_secs = 0.0

        # Events
        events_list = events or []
        events_detected = len(events_list)

        fake_breakout_warnings = 0
        vwap_reclaims = 0
        chase_risk_events = 0
        user_annotations = 0

        for evt in events_list:
            try:
                etype = evt.event_type if hasattr(evt, "event_type") else evt.get("event_type", "")
                if etype == "FAKE_BREAKOUT_WARNING":
                    fake_breakout_warnings += 1
                elif etype == "VWAP_RECLAIM":
                    vwap_reclaims += 1
                elif etype in ("VOLUME_SPIKE", "FAKE_BREAKOUT_WARNING"):
                    chase_risk_events += 1
                elif etype == "USER_ANNOTATION":
                    user_annotations += 1
            except Exception:
                pass

        # Answers / quiz
        answers_list = answers or []
        questions_answered = len(answers_list)
        correct_count = 0
        for ans in answers_list:
            try:
                if isinstance(ans, dict) and ans.get("correct", False):
                    correct_count += 1
                elif hasattr(ans, "correct") and ans.correct:
                    correct_count += 1
            except Exception:
                pass

        quiz_accuracy = correct_count / max(questions_answered, 1) if questions_answered > 0 else 0.0

        # Training score (0-100)
        if questions_answered > 0:
            training_score = quiz_accuracy * 100.0
        else:
            # base score from session completeness
            try:
                total_bars = int(session.total_bars if hasattr(session, "total_bars")
                                 else session.get("total_bars", 0))
                if total_bars > 0:
                    training_score = min(50.0, bars_replayed / total_bars * 50.0)
                else:
                    training_score = 0.0
            except Exception:
                training_score = 0.0

        grade = _grade_from_score(training_score)

        return {
            "bars_replayed": bars_replayed,
            "session_duration_seconds": round(duration_secs, 2),
            "events_detected": events_detected,
            "questions_answered": questions_answered,
            "quiz_accuracy": round(quiz_accuracy, 4),
            "fake_breakout_warnings": fake_breakout_warnings,
            "vwap_reclaims": vwap_reclaims,
            "chase_risk_events": chase_risk_events,
            "user_annotations": user_annotations,
            "training_score": round(training_score, 2),
            "grade": grade,
            "research_only": True,
            "no_real_orders": True,
        }
