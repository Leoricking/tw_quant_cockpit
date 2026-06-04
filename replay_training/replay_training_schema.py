"""replay_training/replay_training_schema.py — Data schemas for TW Replay Training Cockpit v0.5.6.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No broker connection. No live trading. Not investment advice.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Marker type constants
# ---------------------------------------------------------------------------
MARKER_ENTRY               = "ENTRY"
MARKER_EXIT                = "EXIT"
MARKER_STOP_LOSS           = "STOP_LOSS"
MARKER_TAKE_PROFIT         = "TAKE_PROFIT"
MARKER_ADD_POSITION        = "ADD_POSITION"
MARKER_AVOID_ENTRY         = "AVOID_ENTRY"
MARKER_FAKE_BREAKOUT       = "FAKE_BREAKOUT"
MARKER_VWAP_LOSS           = "VWAP_LOSS"
MARKER_VWAP_RECLAIM        = "VWAP_RECLAIM"
MARKER_OPENING_RANGE_BREAK = "OPENING_RANGE_BREAK"
MARKER_OPENING_RANGE_FAIL  = "OPENING_RANGE_FAIL"
MARKER_SUPPORT             = "SUPPORT"
MARKER_RESISTANCE          = "RESISTANCE"
MARKER_NOTE                = "NOTE"

ALL_MARKER_TYPES = [
    MARKER_ENTRY, MARKER_EXIT, MARKER_STOP_LOSS, MARKER_TAKE_PROFIT,
    MARKER_ADD_POSITION, MARKER_AVOID_ENTRY, MARKER_FAKE_BREAKOUT,
    MARKER_VWAP_LOSS, MARKER_VWAP_RECLAIM, MARKER_OPENING_RANGE_BREAK,
    MARKER_OPENING_RANGE_FAIL, MARKER_SUPPORT, MARKER_RESISTANCE, MARKER_NOTE,
]

# ---------------------------------------------------------------------------
# Mistake type constants
# ---------------------------------------------------------------------------
MISTAKE_CHASE_HIGH                = "chase_high"
MISTAKE_IGNORED_STOP              = "ignored_stop"
MISTAKE_OVERSIZED_POSITION        = "oversized_position"
MISTAKE_BOUGHT_WEAK_STOCK         = "bought_weak_stock"
MISTAKE_IGNORED_FAKE_BREAKOUT     = "ignored_fake_breakout"
MISTAKE_IGNORED_VWAP_LOSS         = "ignored_vwap_loss"
MISTAKE_IGNORED_TOP_PATTERN       = "ignored_top_pattern"
MISTAKE_IGNORED_OPENING_RANGE_FAIL = "ignored_opening_range_fail"
MISTAKE_NO_PLAN                   = "no_plan"
MISTAKE_EMOTIONAL_TRADE           = "emotional_trade"
MISTAKE_OVERTRADING               = "overtrading"
MISTAKE_EARLY_TAKE_PROFIT         = "early_take_profit"
MISTAKE_LATE_STOP_LOSS            = "late_stop_loss"
MISTAKE_MISSED_SECOND_WAVE        = "missed_second_wave"
MISTAKE_LOW_QUALITY_ENTRY         = "low_quality_entry"
MISTAKE_VIOLATED_STRATEGY         = "violated_strategy"

ALL_MISTAKE_TYPES = [
    MISTAKE_CHASE_HIGH, MISTAKE_IGNORED_STOP, MISTAKE_OVERSIZED_POSITION,
    MISTAKE_BOUGHT_WEAK_STOCK, MISTAKE_IGNORED_FAKE_BREAKOUT, MISTAKE_IGNORED_VWAP_LOSS,
    MISTAKE_IGNORED_TOP_PATTERN, MISTAKE_IGNORED_OPENING_RANGE_FAIL, MISTAKE_NO_PLAN,
    MISTAKE_EMOTIONAL_TRADE, MISTAKE_OVERTRADING, MISTAKE_EARLY_TAKE_PROFIT,
    MISTAKE_LATE_STOP_LOSS, MISTAKE_MISSED_SECOND_WAVE, MISTAKE_LOW_QUALITY_ENTRY,
    MISTAKE_VIOLATED_STRATEGY,
]


@dataclass
class ReplayTrainingSession:
    """A single replay training session.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    session_id:          str
    symbol:              str
    trade_date:          str
    timeframe:           str = "1min"
    mode:                str = "real"
    started_at:          str = ""
    ended_at:            str = ""
    current_bar_index:   int = 0
    total_bars:          int = 0
    status:              str = "CREATED"
    hidden_future_data:  bool = True
    replay_speed:        int = 1
    notes_count:         int = 0
    markers_count:       int = 0
    mistakes_count:      int = 0
    score:               float = 0.0
    # Safety flags — always True
    read_only:           bool = True
    no_real_orders:      bool = True
    production_blocked:  bool = True

    def to_dict(self) -> dict:
        return {
            "session_id":         self.session_id,
            "symbol":             self.symbol,
            "trade_date":         self.trade_date,
            "timeframe":          self.timeframe,
            "mode":               self.mode,
            "started_at":         self.started_at,
            "ended_at":           self.ended_at,
            "current_bar_index":  self.current_bar_index,
            "total_bars":         self.total_bars,
            "status":             self.status,
            "hidden_future_data": self.hidden_future_data,
            "replay_speed":       self.replay_speed,
            "notes_count":        self.notes_count,
            "markers_count":      self.markers_count,
            "mistakes_count":     self.mistakes_count,
            "score":              self.score,
            "read_only":          self.read_only,
            "no_real_orders":     self.no_real_orders,
            "production_blocked": self.production_blocked,
        }


@dataclass
class ReplayMarker:
    """A user-placed marker on a replay bar.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    marker_id:     str
    session_id:    str
    symbol:        str
    trade_date:    str
    bar_time:      str
    bar_index:     int
    marker_type:   str
    price:         float = 0.0
    reason:        str = ""
    confidence:    int = 0
    note:          str = ""
    tags:          str = ""
    created_at:    str = ""
    # Safety flag
    no_real_orders: bool = True

    def to_dict(self) -> dict:
        return {
            "marker_id":     self.marker_id,
            "session_id":    self.session_id,
            "symbol":        self.symbol,
            "trade_date":    self.trade_date,
            "bar_time":      self.bar_time,
            "bar_index":     self.bar_index,
            "marker_type":   self.marker_type,
            "price":         self.price,
            "reason":        self.reason,
            "confidence":    self.confidence,
            "note":          self.note,
            "tags":          self.tags,
            "created_at":    self.created_at,
            "no_real_orders": self.no_real_orders,
        }


@dataclass
class ReplayMistake:
    """A detected mistake in a replay training session.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    mistake_id:        str
    session_id:        str
    mistake_type:      str
    bar_time:          str = ""
    price:             float = 0.0
    severity:          str = "medium"
    description:       str = ""
    suggested_fix:     str = ""
    related_marker_id: str = ""
    tags:              str = ""

    def to_dict(self) -> dict:
        return {
            "mistake_id":        self.mistake_id,
            "session_id":        self.session_id,
            "mistake_type":      self.mistake_type,
            "bar_time":          self.bar_time,
            "price":             self.price,
            "severity":          self.severity,
            "description":       self.description,
            "suggested_fix":     self.suggested_fix,
            "related_marker_id": self.related_marker_id,
            "tags":              self.tags,
        }


@dataclass
class ReplayAIReview:
    """AI rule-based review of a replay training session.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] Rule-based only. No external LLM API. No broker connection.
    """

    review_id:              str
    session_id:             str
    symbol:                 str
    trade_date:             str
    summary:                str = ""
    best_entry:             str = ""
    worst_entry:            str = ""
    best_exit:              str = ""
    worst_exit:             str = ""
    detected_mistakes:      str = ""
    strategy_violations:    str = ""
    tape_reading_feedback:  str = ""
    next_training_focus:    str = ""
    suggested_drills:       str = ""
    score:                  float = 0.0
    report_path:            str = ""
    created_at:             str = ""
    # Safety flags — always True
    read_only:              bool = True
    no_real_orders:         bool = True
    production_blocked:     bool = True

    def to_dict(self) -> dict:
        return {
            "review_id":             self.review_id,
            "session_id":            self.session_id,
            "symbol":                self.symbol,
            "trade_date":            self.trade_date,
            "summary":               self.summary,
            "best_entry":            self.best_entry,
            "worst_entry":           self.worst_entry,
            "best_exit":             self.best_exit,
            "worst_exit":            self.worst_exit,
            "detected_mistakes":     self.detected_mistakes,
            "strategy_violations":   self.strategy_violations,
            "tape_reading_feedback": self.tape_reading_feedback,
            "next_training_focus":   self.next_training_focus,
            "suggested_drills":      self.suggested_drills,
            "score":                 self.score,
            "report_path":           self.report_path,
            "created_at":            self.created_at,
            "read_only":             self.read_only,
            "no_real_orders":        self.no_real_orders,
            "production_blocked":    self.production_blocked,
        }
