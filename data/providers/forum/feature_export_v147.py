"""
data/providers/forum/feature_export_v147.py — ForumFeatureExporter v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] PIT-valid features only. Auxiliary/supplementary features only.
[!] formal_standalone=False ALWAYS. Cannot override official data features.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_FORMAL_CONCLUSION_STANDALONE_ALLOWED = False
FORUM_FEATURE_FORMAL_STANDALONE = False  # ALWAYS FALSE


class ForumFeatureExporter:
    """
    Exports PIT-valid forum features as auxiliary/supplementary inputs.
    [!] formal_standalone=False ALWAYS.
    [!] Features cannot override or replace official market data features.
    [!] All features are PIT-validated before export.
    """

    FEATURE_NAMESPACE = "forum_v147"
    FORMAL_STANDALONE = False  # ALWAYS FALSE
    AUTHORITY = "SUPPLEMENTARY"

    def __init__(self, store=None) -> None:
        if store is None:
            from data.providers.forum.store_v147 import ForumStore
            store = ForumStore()
        self._store = store

    # ------------------------------------------------------------------
    # export_features_for_symbol
    # ------------------------------------------------------------------
    def export_features_for_symbol(
        self,
        symbol: str,
        as_of: str,
        windows: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Export PIT-valid forum features for a symbol as of a timestamp.
        [!] All features are auxiliary/supplementary only.
        [!] formal_standalone is always False.
        """
        if windows is None:
            windows = ["1d", "5d", "20d"]

        features: Dict[str, Any] = {
            "_namespace": self.FEATURE_NAMESPACE,
            "_symbol": symbol,
            "_as_of": as_of,
            "_formal_standalone": False,
            "_authority": self.AUTHORITY,
            "_can_generate_buy_sell": False,
            "_can_override_official": False,
            "_auxiliary_only": True,
        }

        for window in windows:
            prefix = f"forum_{window}_"
            window_features = self._compute_window_features(symbol, as_of, window)
            for k, v in window_features.items():
                features[prefix + k] = v

        return features

    # ------------------------------------------------------------------
    # export_features_for_article
    # ------------------------------------------------------------------
    def export_features_for_article(self, article_id: str, as_of: str) -> Dict[str, Any]:
        """
        Export PIT-valid features for a single article.
        [!] Auxiliary only. formal_standalone=False.
        """
        from data.providers.forum.point_in_time_v147 import ForumPointInTimeService
        pit = ForumPointInTimeService(store=self._store)
        article = pit.get_article_as_of(article_id, as_of)
        if article is None:
            return {
                "_namespace": self.FEATURE_NAMESPACE,
                "_article_id": article_id,
                "_as_of": as_of,
                "_visible": False,
                "_formal_standalone": False,
                "_authority": self.AUTHORITY,
            }

        engagement = self._store.get_article(article_id)
        features = {
            "_namespace": self.FEATURE_NAMESPACE,
            "_article_id": article_id,
            "_as_of": as_of,
            "_visible": True,
            "_formal_standalone": False,
            "_authority": self.AUTHORITY,
            "category": article.get("category"),
            "is_deleted": bool(article.get("is_deleted")),
            "body_length": article.get("body_length", 0),
            "duplicate_status": article.get("duplicate_status", "UNIQUE"),
        }

        # Sentiment
        with self._store._conn() as conn:
            sent = conn.execute(
                "SELECT polarity, confidence, sarcasm_risk FROM forum_sentiment_signals "
                "WHERE article_id = ? AND scored_at <= ? ORDER BY scored_at DESC LIMIT 1",
                (article_id, as_of)
            ).fetchone()
        if sent:
            features["sentiment_polarity"] = sent["polarity"]
            features["sentiment_confidence"] = sent["confidence"]
            features["sarcasm_risk"] = sent["sarcasm_risk"]

        return features

    # ------------------------------------------------------------------
    # batch_export_features
    # ------------------------------------------------------------------
    def batch_export_features(
        self,
        symbols: List[str],
        as_of: str,
        windows: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Batch export features for multiple symbols."""
        return [self.export_features_for_symbol(s, as_of, windows) for s in symbols]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _compute_window_features(
        self, symbol: str, as_of: str, window: str
    ) -> Dict[str, Any]:
        """Compute aggregated features for symbol/window."""
        from data.providers.forum.aggregation_v147 import MarketSentimentAggregator
        aggregator = MarketSentimentAggregator(store=self._store)
        snap = aggregator.aggregate(
            window=window,
            dimension="stock",
            dimension_value=symbol,
            as_of=as_of,
        )
        if snap.get("blocked"):
            return {
                "blocked": True,
                "blocked_reason": snap.get("blocked_reason", ""),
            }
        total = snap.get("article_count", 0)
        return {
            "article_count": total,
            "bullish_count": snap.get("bullish_count", 0),
            "bearish_count": snap.get("bearish_count", 0),
            "neutral_count": snap.get("neutral_count", 0),
            "disagreement": snap.get("disagreement", 0.0),
            "confidence": snap.get("confidence", 0.0),
            "bullish_ratio": (
                snap.get("bullish_count", 0) / total if total > 0 else 0.0
            ),
            "bearish_ratio": (
                snap.get("bearish_count", 0) / total if total > 0 else 0.0
            ),
        }

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------
    def get_feature_metadata(self) -> Dict[str, Any]:
        return {
            "namespace": self.FEATURE_NAMESPACE,
            "formal_standalone": self.FORMAL_STANDALONE,
            "authority": self.AUTHORITY,
            "feature_type": "auxiliary_supplementary",
            "can_generate_buy_sell": False,
            "can_override_official": False,
            "pit_valid": True,
            "windows": ["1d", "5d", "20d"],
            "note": (
                "Forum features are PIT-valid auxiliary inputs. "
                "Cannot be used as standalone formal research conclusions. "
                "Cannot override official market data features."
            ),
        }
