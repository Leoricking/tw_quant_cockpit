"""replay/replay_events.py — Replay Event detection (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ReplayEvent dataclass
# ---------------------------------------------------------------------------

@dataclass
class ReplayEvent:
    """A single detected event during intraday replay.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    """

    event_id: str
    event_type: str
    symbol: str = ""
    date: str = ""
    time: str = ""
    bar_index: int = 0
    title: str = ""
    description: str = ""
    severity: str = "INFO"  # INFO / WARNING / CRITICAL
    feature_values: dict = field(default_factory=dict)
    rule_id: str = ""
    source: str = ""
    visible_at_index: int = 0

    # Event type constants
    OPENING_RANGE_HIGH = "OPENING_RANGE_HIGH"
    OPENING_RANGE_LOW = "OPENING_RANGE_LOW"
    OPENING_RANGE_BREAK = "OPENING_RANGE_BREAK"
    VWAP_RECLAIM = "VWAP_RECLAIM"
    VWAP_LOST = "VWAP_LOST"
    FAKE_BREAKOUT_WARNING = "FAKE_BREAKOUT_WARNING"
    VOLUME_SPIKE = "VOLUME_SPIKE"
    POC_TOUCH = "POC_TOUCH"
    SUPPORT_PRESSURE = "SUPPORT_PRESSURE"
    SIGNAL_TRIGGER = "SIGNAL_TRIGGER"
    TRAINING_QUESTION = "TRAINING_QUESTION"
    USER_ANNOTATION = "USER_ANNOTATION"

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "symbol": self.symbol,
            "date": self.date,
            "time": self.time,
            "bar_index": self.bar_index,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "feature_values": self.feature_values,
            "rule_id": self.rule_id,
            "source": self.source,
            "visible_at_index": self.visible_at_index,
        }


def _make_id() -> str:
    return str(uuid.uuid4())[:12]


# ---------------------------------------------------------------------------
# ReplayEventBuilder
# ---------------------------------------------------------------------------

class ReplayEventBuilder:
    """Builds events from intraday data for replay training.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    """

    read_only = True
    no_real_orders = True

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Master builder
    # ------------------------------------------------------------------
    def build_events(self, df, features=None) -> list:
        """Build all event types from visible_df. No crash if df empty/None."""
        if df is None:
            return []
        try:
            if len(df) == 0:
                return []
        except Exception:
            return []

        events: list = []
        try:
            events.extend(self.build_opening_range_events(df))
        except Exception as exc:
            logger.warning("[ReplayEventBuilder] opening range error: %s", exc)
        try:
            events.extend(self.build_vwap_events(df))
        except Exception as exc:
            logger.warning("[ReplayEventBuilder] vwap error: %s", exc)
        try:
            events.extend(self.build_fake_breakout_events(df))
        except Exception as exc:
            logger.warning("[ReplayEventBuilder] fake breakout error: %s", exc)
        try:
            events.extend(self.build_volume_profile_events(df))
        except Exception as exc:
            logger.warning("[ReplayEventBuilder] volume profile error: %s", exc)
        return events

    # ------------------------------------------------------------------
    # Opening range events
    # ------------------------------------------------------------------
    def build_opening_range_events(self, df) -> list:
        """Detect opening range high/low from first N=15 bars; detect breaks."""
        events: list = []
        if df is None or len(df) == 0:
            return events

        n = min(15, len(df))
        opening_df = df.iloc[:n]

        high_col = self._find_col(df, ("high", "h"))
        low_col = self._find_col(df, ("low", "l"))
        close_col = self._find_col(df, ("close", "c", "price"))
        time_col = self._find_col(df, ("datetime", "time", "timestamp"))

        if high_col is None or low_col is None:
            return events

        try:
            or_high = float(opening_df[high_col].max())
            or_low = float(opening_df[low_col].min())
        except Exception:
            return events

        def _time(idx):
            if time_col and time_col in df.columns:
                try:
                    return str(df.iloc[idx][time_col])
                except Exception:
                    pass
            return str(idx)

        # OR high event at bar n-1
        events.append(
            ReplayEvent(
                event_id=_make_id(),
                event_type=ReplayEvent.OPENING_RANGE_HIGH,
                bar_index=n - 1,
                title=f"Opening Range High: {or_high:.2f}",
                description=f"Opening range high established at {or_high:.2f} after {n} bars.",
                severity="INFO",
                feature_values={"opening_high": or_high, "n_bars": n},
                source="opening_range",
                visible_at_index=n - 1,
                time=_time(n - 1),
            )
        )

        # OR low event at bar n-1
        events.append(
            ReplayEvent(
                event_id=_make_id(),
                event_type=ReplayEvent.OPENING_RANGE_LOW,
                bar_index=n - 1,
                title=f"Opening Range Low: {or_low:.2f}",
                description=f"Opening range low established at {or_low:.2f} after {n} bars.",
                severity="INFO",
                feature_values={"opening_low": or_low, "n_bars": n},
                source="opening_range",
                visible_at_index=n - 1,
                time=_time(n - 1),
            )
        )

        # Detect breaks after opening range
        if close_col is not None and len(df) > n:
            for i in range(n, len(df)):
                try:
                    close = float(df.iloc[i][close_col])
                except Exception:
                    continue

                if close > or_high:
                    events.append(
                        ReplayEvent(
                            event_id=_make_id(),
                            event_type=ReplayEvent.OPENING_RANGE_BREAK,
                            bar_index=i,
                            title=f"OR Break High at bar {i}",
                            description=f"Close {close:.2f} broke above OR high {or_high:.2f}.",
                            severity="WARNING",
                            feature_values={"close": close, "or_high": or_high},
                            source="opening_range",
                            visible_at_index=i,
                            time=_time(i),
                        )
                    )
                    break  # report first break only
                elif close < or_low:
                    events.append(
                        ReplayEvent(
                            event_id=_make_id(),
                            event_type=ReplayEvent.OPENING_RANGE_BREAK,
                            bar_index=i,
                            title=f"OR Break Low at bar {i}",
                            description=f"Close {close:.2f} broke below OR low {or_low:.2f}.",
                            severity="WARNING",
                            feature_values={"close": close, "or_low": or_low},
                            source="opening_range",
                            visible_at_index=i,
                            time=_time(i),
                        )
                    )
                    break

        return events

    # ------------------------------------------------------------------
    # VWAP events
    # ------------------------------------------------------------------
    def build_vwap_events(self, df) -> list:
        """Detect VWAP reclaim/lost events."""
        events: list = []
        if df is None or len(df) < 4:
            return events

        close_col = self._find_col(df, ("close", "c", "price"))
        volume_col = self._find_col(df, ("volume", "vol", "v"))
        time_col = self._find_col(df, ("datetime", "time", "timestamp"))

        if close_col is None:
            return events

        def _time(idx):
            if time_col and time_col in df.columns:
                try:
                    return str(df.iloc[idx][time_col])
                except Exception:
                    pass
            return str(idx)

        try:
            closes = df[close_col].astype(float).tolist()
            if volume_col:
                volumes = df[volume_col].astype(float).tolist()
            else:
                volumes = [1.0] * len(closes)

            # compute cumulative VWAP
            cumvol = 0.0
            cumtpvol = 0.0
            vwaps = []
            for c, v in zip(closes, volumes):
                v = max(v, 1e-9)
                cumvol += v
                cumtpvol += c * v
                vwaps.append(cumtpvol / cumvol)

            # detect crossings
            for i in range(3, len(df)):
                above_now = closes[i] >= vwaps[i]
                above_prev = closes[i - 1] >= vwaps[i - 1]
                above_2 = closes[i - 2] >= vwaps[i - 2]

                if above_now and not above_prev and not above_2:
                    events.append(
                        ReplayEvent(
                            event_id=_make_id(),
                            event_type=ReplayEvent.VWAP_RECLAIM,
                            bar_index=i,
                            title=f"VWAP Reclaim at bar {i}",
                            description=f"Price {closes[i]:.2f} reclaimed VWAP {vwaps[i]:.2f}.",
                            severity="INFO",
                            feature_values={"close": closes[i], "vwap": vwaps[i]},
                            source="vwap",
                            visible_at_index=i,
                            time=_time(i),
                        )
                    )
                elif not above_now and above_prev and above_2:
                    events.append(
                        ReplayEvent(
                            event_id=_make_id(),
                            event_type=ReplayEvent.VWAP_LOST,
                            bar_index=i,
                            title=f"VWAP Lost at bar {i}",
                            description=f"Price {closes[i]:.2f} fell below VWAP {vwaps[i]:.2f}.",
                            severity="WARNING",
                            feature_values={"close": closes[i], "vwap": vwaps[i]},
                            source="vwap",
                            visible_at_index=i,
                            time=_time(i),
                        )
                    )
        except Exception as exc:
            logger.warning("[ReplayEventBuilder] vwap event error: %s", exc)

        return events

    # ------------------------------------------------------------------
    # Fake breakout events
    # ------------------------------------------------------------------
    def build_fake_breakout_events(self, df) -> list:
        """Detect when price breaks then reverses back."""
        events: list = []
        if df is None or len(df) < 12:
            return events

        close_col = self._find_col(df, ("close", "c", "price"))
        high_col = self._find_col(df, ("high", "h"))
        time_col = self._find_col(df, ("datetime", "time", "timestamp"))

        if close_col is None or high_col is None:
            return events

        def _time(idx):
            if time_col and time_col in df.columns:
                try:
                    return str(df.iloc[idx][time_col])
                except Exception:
                    pass
            return str(idx)

        try:
            closes = df[close_col].astype(float).tolist()
            highs = df[high_col].astype(float).tolist()

            lookback = 10
            for i in range(lookback + 2, len(df)):
                recent_high = max(highs[i - lookback : i])
                broke = closes[i - 1] > recent_high
                reversed_back = closes[i] < recent_high
                if broke and reversed_back:
                    events.append(
                        ReplayEvent(
                            event_id=_make_id(),
                            event_type=ReplayEvent.FAKE_BREAKOUT_WARNING,
                            bar_index=i,
                            title=f"Fake Breakout Warning at bar {i}",
                            description=(
                                f"Price broke above {recent_high:.2f} at bar {i-1} "
                                f"but reversed to {closes[i]:.2f}. Possible fake breakout."
                            ),
                            severity="WARNING",
                            feature_values={
                                "close": closes[i],
                                "breakout_level": recent_high,
                                "prev_close": closes[i - 1],
                            },
                            source="fake_breakout",
                            visible_at_index=i,
                            time=_time(i),
                        )
                    )
        except Exception as exc:
            logger.warning("[ReplayEventBuilder] fake breakout event error: %s", exc)

        return events

    # ------------------------------------------------------------------
    # Volume profile events
    # ------------------------------------------------------------------
    def build_volume_profile_events(self, df) -> list:
        """Detect volume spikes (> 2x rolling mean) and POC touches."""
        events: list = []
        if df is None or len(df) < 5:
            return events

        volume_col = self._find_col(df, ("volume", "vol", "v"))
        close_col = self._find_col(df, ("close", "c", "price"))
        time_col = self._find_col(df, ("datetime", "time", "timestamp"))

        if volume_col is None:
            return events

        def _time(idx):
            if time_col and time_col in df.columns:
                try:
                    return str(df.iloc[idx][time_col])
                except Exception:
                    pass
            return str(idx)

        try:
            volumes = df[volume_col].astype(float).tolist()
            closes = df[close_col].astype(float).tolist() if close_col else [0.0] * len(volumes)

            window = 10
            for i in range(window, len(df)):
                rolling_mean = sum(volumes[i - window : i]) / window
                if rolling_mean <= 0:
                    continue
                ratio = volumes[i] / rolling_mean
                if ratio >= 2.0:
                    events.append(
                        ReplayEvent(
                            event_id=_make_id(),
                            event_type=ReplayEvent.VOLUME_SPIKE,
                            bar_index=i,
                            title=f"Volume Spike x{ratio:.1f} at bar {i}",
                            description=(
                                f"Volume {volumes[i]:.0f} is {ratio:.1f}x the rolling mean "
                                f"{rolling_mean:.0f}. Watch for directional move."
                            ),
                            severity="WARNING" if ratio >= 3.0 else "INFO",
                            feature_values={
                                "volume": volumes[i],
                                "rolling_mean": rolling_mean,
                                "ratio": ratio,
                                "close": closes[i],
                            },
                            source="volume_profile",
                            visible_at_index=i,
                            time=_time(i),
                        )
                    )

            # Simple POC touch: find price level with highest cumulative volume
            if close_col and len(volumes) >= 5:
                from collections import defaultdict
                price_vol: dict = defaultdict(float)
                for c, v in zip(closes, volumes):
                    price_bin = round(c, 1)
                    price_vol[price_bin] += v
                if price_vol:
                    poc_price = max(price_vol, key=lambda p: price_vol[p])
                    # detect when current close is within 0.5% of POC
                    last_idx = len(df) - 1
                    last_close = closes[last_idx]
                    if poc_price and abs(last_close - poc_price) / max(poc_price, 1e-9) < 0.005:
                        events.append(
                            ReplayEvent(
                                event_id=_make_id(),
                                event_type=ReplayEvent.POC_TOUCH,
                                bar_index=last_idx,
                                title=f"POC Touch at {poc_price:.2f}",
                                description=f"Price {last_close:.2f} is near POC {poc_price:.2f}.",
                                severity="INFO",
                                feature_values={"close": last_close, "poc": poc_price},
                                source="volume_profile",
                                visible_at_index=last_idx,
                                time=_time(last_idx),
                            )
                        )
        except Exception as exc:
            logger.warning("[ReplayEventBuilder] volume profile event error: %s", exc)

        return events

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    @staticmethod
    def _find_col(df, candidates: tuple) -> Optional[str]:
        cols = [c.lower() for c in df.columns]
        for cand in candidates:
            if cand in cols:
                # return original column name
                for orig in df.columns:
                    if orig.lower() == cand:
                        return orig
        return None
