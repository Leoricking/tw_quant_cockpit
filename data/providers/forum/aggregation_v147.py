"""
data/providers/forum/aggregation_v147.py — MarketSentimentAggregator v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] formal_standalone=False ALWAYS. SUPPLEMENTARY authority only.
[!] Insufficient timestamp precision blocks fine-grained (intraday) windows.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED = False

# Supported aggregation windows
SUPPORTED_WINDOWS = ("15min", "1h", "4h", "1d", "3d", "5d", "20d")

# Dimensions for aggregation
SUPPORTED_DIMENSIONS = ("market", "stock", "etf", "industry", "topic")

# Minimum precision needed for sub-day windows
_INTRADAY_WINDOWS = {"15min", "1h", "4h"}
_REQUIRED_PRECISION_FOR_INTRADAY = ("MINUTE", "SECOND")


class MarketSentimentAggregator:
    """
    Aggregates forum sentiment signals into time-windowed market sentiment snapshots.
    [!] formal_standalone=False ALWAYS.
    [!] Insufficient timestamp precision blocks intraday windows.
    """

    def __init__(self, store=None) -> None:
        if store is None:
            from data.providers.forum.store_v147 import ForumStore
            store = ForumStore()
        self._store = store

    # ------------------------------------------------------------------
    # aggregate
    # ------------------------------------------------------------------
    def aggregate(
        self,
        window: str,
        dimension: str = "market",
        dimension_value: Optional[str] = None,
        as_of: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Aggregate forum sentiment for given window and dimension.
        [!] Returns formal_standalone=False always.
        [!] Intraday windows blocked if timestamp precision insufficient.
        """
        if window not in SUPPORTED_WINDOWS:
            return self._blocked_result(
                window, dimension, dimension_value,
                reason=f"Unsupported window: {window}. Supported: {SUPPORTED_WINDOWS}"
            )
        if dimension not in SUPPORTED_DIMENSIONS:
            return self._blocked_result(
                window, dimension, dimension_value,
                reason=f"Unsupported dimension: {dimension}"
            )

        # Compute time range
        now_str = as_of or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        cutoff = self._compute_cutoff(window, now_str)

        # Fetch sentiment signals in window
        signals = self._fetch_signals_in_window(
            cutoff=cutoff, as_of=now_str,
            dimension=dimension, dimension_value=dimension_value
        )

        # Precision check for intraday windows
        if window in _INTRADAY_WINDOWS:
            precision_ok = self._check_timestamp_precision(signals)
            if not precision_ok:
                return self._blocked_result(
                    window, dimension, dimension_value,
                    reason=(
                        f"Intraday window '{window}' requires MINUTE or SECOND precision, "
                        "but insufficient precision found in signals. "
                        "Blocked to prevent misleading fine-grained aggregation."
                    )
                )

        # Aggregate
        bullish = sum(1 for s in signals if s.get("polarity") in ("BULLISH", "VERY_BULLISH"))
        bearish = sum(1 for s in signals if s.get("polarity") in ("BEARISH", "VERY_BEARISH"))
        neutral = sum(1 for s in signals if s.get("polarity") == "NEUTRAL")
        total = len(signals)
        disagreement = self._compute_disagreement(bullish, bearish, total)
        confidence = self._compute_confidence(signals, total)

        result = {
            "window": window,
            "dimension": dimension,
            "dimension_value": dimension_value,
            "article_count": total,
            "bullish_count": bullish,
            "bearish_count": bearish,
            "neutral_count": neutral,
            "disagreement": round(disagreement, 4),
            "confidence": round(confidence, 4),
            "formal_standalone": False,  # ALWAYS FALSE
            "can_generate_buy_sell": False,
            "can_override_official": False,
            "authority": "SUPPLEMENTARY",
            "computed_at": now_str,
            "blocked": False,
        }

        # Persist snapshot
        self._store.insert_market_sentiment_snapshot(result)
        return result

    # ------------------------------------------------------------------
    # aggregate_all_windows
    # ------------------------------------------------------------------
    def aggregate_all_windows(
        self,
        dimension: str = "market",
        dimension_value: Optional[str] = None,
        as_of: Optional[str] = None,
    ) -> List[Dict]:
        """Aggregate across all supported windows."""
        results = []
        for w in SUPPORTED_WINDOWS:
            r = self.aggregate(w, dimension=dimension, dimension_value=dimension_value, as_of=as_of)
            results.append(r)
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _compute_cutoff(self, window: str, now_str: str) -> str:
        """Compute ISO cutoff string for window."""
        now = datetime.fromisoformat(now_str.replace("Z", "+00:00"))
        if window == "15min":
            delta = timedelta(minutes=15)
        elif window == "1h":
            delta = timedelta(hours=1)
        elif window == "4h":
            delta = timedelta(hours=4)
        elif window == "1d":
            delta = timedelta(days=1)
        elif window == "3d":
            delta = timedelta(days=3)
        elif window == "5d":
            delta = timedelta(days=5)
        elif window == "20d":
            delta = timedelta(days=20)
        else:
            delta = timedelta(days=1)
        return (now - delta).isoformat()

    def _fetch_signals_in_window(
        self,
        cutoff: str,
        as_of: str,
        dimension: str,
        dimension_value: Optional[str],
    ) -> List[Dict]:
        """Fetch sentiment signals within the time window."""
        with self._store._conn() as conn:
            if dimension == "market":
                rows = conn.execute(
                    "SELECT * FROM forum_sentiment_signals WHERE scored_at >= ? AND scored_at <= ?",
                    (cutoff, as_of)
                ).fetchall()
            elif dimension in ("stock", "etf") and dimension_value:
                rows = conn.execute(
                    "SELECT * FROM forum_sentiment_signals "
                    "WHERE target_symbol = ? AND scored_at >= ? AND scored_at <= ?",
                    (dimension_value, cutoff, as_of)
                ).fetchall()
            elif dimension == "industry" and dimension_value:
                # Join via symbol_mentions to get industry
                rows = conn.execute(
                    "SELECT s.* FROM forum_sentiment_signals s "
                    "WHERE s.scored_at >= ? AND s.scored_at <= ?",
                    (cutoff, as_of)
                ).fetchall()
            elif dimension == "topic" and dimension_value:
                rows = conn.execute(
                    "SELECT s.* FROM forum_sentiment_signals s "
                    "JOIN forum_topic_signals t ON s.article_id = t.article_id "
                    "WHERE t.topic_label = ? AND s.scored_at >= ? AND s.scored_at <= ?",
                    (dimension_value, cutoff, as_of)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM forum_sentiment_signals WHERE scored_at >= ? AND scored_at <= ?",
                    (cutoff, as_of)
                ).fetchall()
        return [dict(r) for r in rows]

    def _check_timestamp_precision(self, signals: List[Dict]) -> bool:
        """
        Check if sufficient signals have MINUTE or SECOND precision.
        Returns False if any signal lacks time precision (only DAY or UNKNOWN).
        """
        if not signals:
            return False
        # For this check, we look at article precision via article IDs
        article_ids = list({s.get("article_id") for s in signals if s.get("article_id")})
        if not article_ids:
            return False
        with self._store._conn() as conn:
            placeholders = ",".join("?" * len(article_ids))
            rows = conn.execute(
                f"SELECT published_at_precision FROM forum_articles WHERE article_id IN ({placeholders})",
                article_ids
            ).fetchall()
        if not rows:
            return False
        for row in rows:
            prec = row[0] if row[0] else "DAY"
            if prec in _REQUIRED_PRECISION_FOR_INTRADAY:
                return True
        return False

    def _compute_disagreement(self, bullish: int, bearish: int, total: int) -> float:
        """Compute disagreement ratio (0=consensus, 1=max disagreement)."""
        if total == 0:
            return 0.0
        minority = min(bullish, bearish)
        return 2.0 * minority / total if total > 0 else 0.0

    def _compute_confidence(self, signals: List[Dict], total: int) -> float:
        """Compute aggregate confidence from individual signal confidences."""
        if total == 0:
            return 0.0
        total_conf = sum(float(s.get("confidence", 0.5)) for s in signals)
        return total_conf / total

    def _blocked_result(
        self,
        window: str,
        dimension: str,
        dimension_value: Optional[str],
        reason: str,
    ) -> Dict:
        return {
            "window": window,
            "dimension": dimension,
            "dimension_value": dimension_value,
            "article_count": 0,
            "bullish_count": 0,
            "bearish_count": 0,
            "neutral_count": 0,
            "disagreement": 0.0,
            "confidence": 0.0,
            "formal_standalone": False,
            "can_generate_buy_sell": False,
            "can_override_official": False,
            "authority": "SUPPLEMENTARY",
            "blocked": True,
            "blocked_reason": reason,
            "computed_at": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
        }
