"""replay_training/tape_reading_detector.py — TapeReadingDetector for TW Replay Training Cockpit v0.5.6.

[!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Only uses visible_bars (no future data). Graceful warning on missing columns.
"""
from __future__ import annotations

import logging
from typing import List

logger = logging.getLogger(__name__)


def _safe_float(bar: dict, key: str, default: float = 0.0) -> float:
    try:
        return float(bar.get(key, default) or default)
    except (ValueError, TypeError):
        return default


def _has_columns(bars: List[dict], *cols: str) -> bool:
    if not bars:
        return False
    for col in cols:
        if col not in bars[0]:
            logger.warning("[TapeReadingDetector] missing column: %s — detection skipped", col)
            return False
    return True


class TapeReadingDetector:
    """Rule-based tape reading pattern detector.

    Only uses visible_bars (bars up to current_bar_index). Never reads future data.

    [!] Replay Training Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Top-level aggregator
    # ------------------------------------------------------------------

    def detect_events(self, visible_bars: List[dict]) -> List[dict]:
        """Run all detectors and return combined event list."""
        events: List[dict] = []
        if not visible_bars:
            return events
        try:
            events += self.detect_fake_breakout(visible_bars)
        except Exception as exc:
            logger.warning("[TapeReadingDetector] fake_breakout error: %s", exc)
        try:
            events += self.detect_vwap_loss(visible_bars)
        except Exception as exc:
            logger.warning("[TapeReadingDetector] vwap_loss error: %s", exc)
        try:
            events += self.detect_vwap_reclaim(visible_bars)
        except Exception as exc:
            logger.warning("[TapeReadingDetector] vwap_reclaim error: %s", exc)
        try:
            events += self.detect_opening_range_break(visible_bars)
        except Exception as exc:
            logger.warning("[TapeReadingDetector] opening_range_break error: %s", exc)
        try:
            events += self.detect_opening_range_fail(visible_bars)
        except Exception as exc:
            logger.warning("[TapeReadingDetector] opening_range_fail error: %s", exc)
        try:
            events += self.detect_long_upper_shadow(visible_bars)
        except Exception as exc:
            logger.warning("[TapeReadingDetector] long_upper_shadow error: %s", exc)
        try:
            events += self.detect_volume_no_follow_through(visible_bars)
        except Exception as exc:
            logger.warning("[TapeReadingDetector] volume_no_follow_through error: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Individual detectors
    # ------------------------------------------------------------------

    def detect_fake_breakout(self, visible_bars: List[dict]) -> List[dict]:
        """Detect fake breakout: price breaks above recent high then falls back within 3 bars."""
        events = []
        if len(visible_bars) < 4:
            return events
        if not _has_columns(visible_bars, "high", "close", "open"):
            return events

        for i in range(3, len(visible_bars)):
            lookback = visible_bars[max(0, i - 5):i]
            prev_high = max((_safe_float(b, "high") for b in lookback), default=0.0)
            bar       = visible_bars[i]
            b_high    = _safe_float(bar, "high")
            b_close   = _safe_float(bar, "close")
            b_open    = _safe_float(bar, "open")

            if prev_high > 0 and b_high > prev_high and b_close < b_open:
                bar_time = str(bar.get("datetime", bar.get("time", bar.get("date", i))))
                events.append({
                    "event_type":  "FAKE_BREAKOUT",
                    "bar_time":    bar_time,
                    "bar_index":   i,
                    "description": (
                        f"Fake breakout detected: bar broke above {prev_high:.2f} "
                        f"but closed lower ({b_close:.2f}). Watch for bearish reversal."
                    ),
                    "no_real_orders": True,
                })
        return events

    def detect_vwap_loss(self, visible_bars: List[dict]) -> List[dict]:
        """Detect price closing below VWAP after being above it."""
        events = []
        if len(visible_bars) < 2:
            return events
        vwap_key = None
        for k in ["vwap", "VWAP"]:
            if k in visible_bars[0]:
                vwap_key = k
                break
        if vwap_key is None:
            logger.warning("[TapeReadingDetector] missing column: vwap — vwap_loss detection skipped")
            return events
        if not _has_columns(visible_bars, "close"):
            return events

        for i in range(1, len(visible_bars)):
            prev = visible_bars[i - 1]
            curr = visible_bars[i]
            prev_vwap  = _safe_float(prev, vwap_key)
            curr_vwap  = _safe_float(curr, vwap_key)
            prev_close = _safe_float(prev, "close")
            curr_close = _safe_float(curr, "close")

            if prev_vwap > 0 and curr_vwap > 0:
                if prev_close >= prev_vwap and curr_close < curr_vwap:
                    bar_time = str(curr.get("datetime", curr.get("time", i)))
                    events.append({
                        "event_type":  "VWAP_LOSS",
                        "bar_time":    bar_time,
                        "bar_index":   i,
                        "description": (
                            f"VWAP loss: price closed below VWAP ({curr_vwap:.2f}). "
                            f"Consider stop or avoid adding."
                        ),
                        "no_real_orders": True,
                    })
        return events

    def detect_vwap_reclaim(self, visible_bars: List[dict]) -> List[dict]:
        """Detect price reclaiming VWAP after being below it."""
        events = []
        if len(visible_bars) < 2:
            return events
        vwap_key = None
        for k in ["vwap", "VWAP"]:
            if k in visible_bars[0]:
                vwap_key = k
                break
        if vwap_key is None:
            return events
        if not _has_columns(visible_bars, "close"):
            return events

        for i in range(1, len(visible_bars)):
            prev = visible_bars[i - 1]
            curr = visible_bars[i]
            prev_vwap  = _safe_float(prev, vwap_key)
            curr_vwap  = _safe_float(curr, vwap_key)
            prev_close = _safe_float(prev, "close")
            curr_close = _safe_float(curr, "close")

            if prev_vwap > 0 and curr_vwap > 0:
                if prev_close < prev_vwap and curr_close >= curr_vwap:
                    bar_time = str(curr.get("datetime", curr.get("time", i)))
                    events.append({
                        "event_type":  "VWAP_RECLAIM",
                        "bar_time":    bar_time,
                        "bar_index":   i,
                        "description": (
                            f"VWAP reclaim: price closed above VWAP ({curr_vwap:.2f}). "
                            f"Potential strength signal."
                        ),
                        "no_real_orders": True,
                    })
        return events

    def detect_opening_range_break(self, visible_bars: List[dict]) -> List[dict]:
        """Detect break above opening range (first 30 bars / 30 minutes)."""
        events = []
        if len(visible_bars) < 5:
            return events
        if not _has_columns(visible_bars, "high", "close"):
            return events

        # Opening range = first 30 bars
        or_bars = visible_bars[:min(30, len(visible_bars))]
        or_high = max((_safe_float(b, "high") for b in or_bars), default=0.0)
        if or_high <= 0:
            return events

        for i in range(30, len(visible_bars)):
            bar   = visible_bars[i]
            close = _safe_float(bar, "close")
            if close > or_high:
                bar_time = str(bar.get("datetime", bar.get("time", i)))
                events.append({
                    "event_type":  "OPENING_RANGE_BREAK",
                    "bar_time":    bar_time,
                    "bar_index":   i,
                    "description": (
                        f"Opening range break: price ({close:.2f}) closed above OR high ({or_high:.2f}). "
                        f"Watch for continuation or fake breakout."
                    ),
                    "no_real_orders": True,
                })
                break  # Only first break
        return events

    def detect_opening_range_fail(self, visible_bars: List[dict]) -> List[dict]:
        """Detect opening range break followed by price falling back inside range."""
        events = []
        if len(visible_bars) < 35:
            return events
        if not _has_columns(visible_bars, "high", "low", "close"):
            return events

        or_bars = visible_bars[:30]
        or_high = max((_safe_float(b, "high") for b in or_bars), default=0.0)
        or_low  = min((_safe_float(b, "low")  for b in or_bars), default=0.0)
        if or_high <= 0:
            return events

        broke_above = False
        for i in range(30, len(visible_bars)):
            bar   = visible_bars[i]
            close = _safe_float(bar, "close")
            if not broke_above and close > or_high:
                broke_above = True
            elif broke_above and close < or_high:
                bar_time = str(bar.get("datetime", bar.get("time", i)))
                events.append({
                    "event_type":  "OPENING_RANGE_FAIL",
                    "bar_time":    bar_time,
                    "bar_index":   i,
                    "description": (
                        f"Opening range fail: price fell back below OR high ({or_high:.2f}) "
                        f"after breakout. Bearish signal."
                    ),
                    "no_real_orders": True,
                })
                broke_above = False
        return events

    def detect_long_upper_shadow(self, visible_bars: List[dict]) -> List[dict]:
        """Detect bars with long upper shadow (doji/shooting star pattern)."""
        events = []
        if not visible_bars:
            return events
        if not _has_columns(visible_bars, "open", "high", "low", "close"):
            return events

        for i, bar in enumerate(visible_bars):
            o = _safe_float(bar, "open")
            h = _safe_float(bar, "high")
            l = _safe_float(bar, "low")
            c = _safe_float(bar, "close")
            body   = abs(c - o)
            shadow = h - max(c, o)
            rng    = h - l
            if rng > 0 and shadow > 0 and shadow > body * 1.5 and shadow > rng * 0.4:
                bar_time = str(bar.get("datetime", bar.get("time", i)))
                events.append({
                    "event_type":  "LONG_UPPER_SHADOW",
                    "bar_time":    bar_time,
                    "bar_index":   i,
                    "description": (
                        f"Long upper shadow at {h:.2f}. "
                        f"Sellers rejected higher prices — possible top/resistance."
                    ),
                    "no_real_orders": True,
                })
        return events

    def detect_volume_no_follow_through(self, visible_bars: List[dict]) -> List[dict]:
        """Detect high-volume bar with no price follow-through (volume divergence)."""
        events = []
        if len(visible_bars) < 3:
            return events
        if not _has_columns(visible_bars, "volume", "close", "open"):
            return events

        volumes = [_safe_float(b, "volume") for b in visible_bars]
        avg_vol = sum(volumes) / len(volumes) if volumes else 0.0

        for i in range(1, len(visible_bars)):
            bar  = visible_bars[i]
            vol  = _safe_float(bar, "volume")
            o    = _safe_float(bar, "open")
            c    = _safe_float(bar, "close")
            if avg_vol > 0 and vol > avg_vol * 1.5 and abs(c - o) < avg_vol * 0.001:
                bar_time = str(bar.get("datetime", bar.get("time", i)))
                events.append({
                    "event_type":  "VOLUME_NO_FOLLOW_THROUGH",
                    "bar_time":    bar_time,
                    "bar_index":   i,
                    "description": (
                        f"High volume ({vol:.0f} vs avg {avg_vol:.0f}) with minimal price movement. "
                        f"Possible distribution or exhaustion."
                    ),
                    "no_real_orders": True,
                })
        return events
