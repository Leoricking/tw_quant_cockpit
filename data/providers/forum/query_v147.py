"""
data/providers/forum/query_v147.py — ForumQueryService v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] SUPPLEMENTARY authority only. No BUY/SELL. No formal standalone conclusions.
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


class ForumQueryService:
    """
    Query layer for Forum Intelligence v1.4.7. 21 query methods.
    [!] Research Only. SUPPLEMENTARY authority. No formal conclusions.
    """

    def __init__(self, store=None) -> None:
        if store is None:
            from data.providers.forum.store_v147 import ForumStore
            store = ForumStore()
        self._store = store

    # ------------------------------------------------------------------
    # 1. list_sources
    # ------------------------------------------------------------------
    def list_sources(self) -> List[Dict]:
        """List all registered forum sources."""
        return self._store.list_sources()

    # ------------------------------------------------------------------
    # 2. get_source
    # ------------------------------------------------------------------
    def get_source(self, source_id: str) -> Optional[Dict]:
        """Get a forum source by ID."""
        return self._store.get_source(source_id)

    # ------------------------------------------------------------------
    # 3. get_article
    # ------------------------------------------------------------------
    def get_article(self, article_id: str) -> Optional[Dict]:
        """Get an article by ID."""
        return self._store.get_article(article_id)

    # ------------------------------------------------------------------
    # 4. get_article_as_of (PIT)
    # ------------------------------------------------------------------
    def get_article_as_of(self, article_id: str, as_of: str) -> Optional[Dict]:
        """
        Get article state as of a point-in-time timestamp.
        Returns None if article was not yet first_seen before as_of.
        [!] No future-leakage.
        """
        article = self._store.get_article(article_id)
        if article is None:
            return None
        first_seen = article.get("first_seen_at") or ""
        if first_seen and first_seen > as_of:
            return None  # not visible yet at as_of
        # Return version that was current at as_of
        versions = self._store.get_article_versions(article_id)
        current_version = None
        for v in sorted(versions, key=lambda x: x.get("captured_at", "")):
            if v.get("captured_at", "") <= as_of:
                current_version = v
        if current_version:
            result = dict(article)
            result["_as_of_version"] = current_version
            result["_as_of"] = as_of
            return result
        return article

    # ------------------------------------------------------------------
    # 5. get_comments (current)
    # ------------------------------------------------------------------
    def get_comments(self, article_id: str) -> List[Dict]:
        """Get all comments for an article."""
        return self._store.get_comments(article_id)

    # ------------------------------------------------------------------
    # 6. get_comments_as_of (PIT)
    # ------------------------------------------------------------------
    def get_comments_as_of(self, article_id: str, as_of: str) -> List[Dict]:
        """
        Get comments visible as of timestamp. Blocks future comments.
        [!] No future-leakage.
        """
        comments = self._store.get_comments(article_id)
        result = []
        for c in comments:
            first_seen = c.get("first_seen_at") or ""
            if not first_seen or first_seen <= as_of:
                result.append(c)
        return result

    # ------------------------------------------------------------------
    # 7. get_deletion_state_as_of (PIT)
    # ------------------------------------------------------------------
    def get_deletion_state_as_of(self, article_id: str, as_of: str) -> Dict:
        """
        Return deletion state as of timestamp.
        [!] Deleted articles are not backfilled as non-deleted.
        """
        from data.providers.forum.store_v147 import ForumStore
        store = self._store
        article = store.get_article(article_id)
        if article is None:
            return {"article_id": article_id, "known": False, "deleted": False, "as_of": as_of}
        # Check deletion events up to as_of
        with store._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_deletion_events WHERE article_id = ? AND detected_at <= ? ORDER BY detected_at",
                (article_id, as_of)
            ).fetchall()
        was_deleted = len(rows) > 0
        return {
            "article_id": article_id,
            "known": True,
            "deleted": was_deleted,
            "as_of": as_of,
            "deletion_events": [dict(r) for r in rows],
        }

    # ------------------------------------------------------------------
    # 8. search_articles
    # ------------------------------------------------------------------
    def search_articles(self, keyword: str, limit: int = 20) -> List[Dict]:
        """Full-text search on article titles."""
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_articles WHERE title LIKE ? LIMIT ?",
                (f"%{keyword}%", limit)
            ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 9. list_articles_by_source
    # ------------------------------------------------------------------
    def list_articles_by_source(self, source_id: str, limit: int = 50) -> List[Dict]:
        """List articles for a given source."""
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_articles WHERE source_id = ? ORDER BY published_at DESC LIMIT ?",
                (source_id, limit)
            ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 10. get_symbol_mentions
    # ------------------------------------------------------------------
    def get_symbol_mentions(self, symbol: str, limit: int = 50) -> List[Dict]:
        """Get all mentions of a symbol."""
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_symbol_mentions WHERE symbol = ? ORDER BY mentioned_at DESC LIMIT ?",
                (symbol, limit)
            ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 11. get_sentiment_for_symbol
    # ------------------------------------------------------------------
    def get_sentiment_for_symbol(self, symbol: str, limit: int = 50) -> List[Dict]:
        """Get sentiment signals for a symbol."""
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_sentiment_signals WHERE target_symbol = ? ORDER BY scored_at DESC LIMIT ?",
                (symbol, limit)
            ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 12. get_topics_for_article
    # ------------------------------------------------------------------
    def get_topics_for_article(self, article_id: str) -> List[Dict]:
        """Get topic signals for an article."""
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_topic_signals WHERE article_id = ?",
                (article_id,)
            ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 13. get_engagement_for_article
    # ------------------------------------------------------------------
    def get_engagement_for_article(self, article_id: str) -> Optional[Dict]:
        """Get engagement signal for an article."""
        with self._store._conn() as conn:
            row = conn.execute(
                "SELECT * FROM forum_engagement_signals WHERE article_id = ? ORDER BY engagement_id DESC LIMIT 1",
                (article_id,)
            ).fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # 14. get_credibility_for_article
    # ------------------------------------------------------------------
    def get_credibility_for_article(self, article_id: str) -> Optional[Dict]:
        """Get credibility signal for an article."""
        with self._store._conn() as conn:
            row = conn.execute(
                "SELECT * FROM forum_credibility_signals WHERE article_id = ? ORDER BY credibility_id DESC LIMIT 1",
                (article_id,)
            ).fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # 15. get_coordination_risk
    # ------------------------------------------------------------------
    def get_coordination_risk(self, article_id: str) -> Optional[Dict]:
        """Get coordination risk for an article."""
        with self._store._conn() as conn:
            row = conn.execute(
                "SELECT * FROM forum_coordination_risks WHERE article_id = ? ORDER BY coord_id DESC LIMIT 1",
                (article_id,)
            ).fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # 16. get_manipulation_risk
    # ------------------------------------------------------------------
    def get_manipulation_risk(self, article_id: str) -> Optional[Dict]:
        """Get manipulation risk for an article."""
        with self._store._conn() as conn:
            row = conn.execute(
                "SELECT * FROM forum_manipulation_risks WHERE article_id = ? ORDER BY manip_id DESC LIMIT 1",
                (article_id,)
            ).fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # 17. get_deleted_articles
    # ------------------------------------------------------------------
    def get_deleted_articles(self, source_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get articles marked as deleted."""
        with self._store._conn() as conn:
            if source_id:
                rows = conn.execute(
                    "SELECT * FROM forum_articles WHERE is_deleted = 1 AND source_id = ? LIMIT ?",
                    (source_id, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM forum_articles WHERE is_deleted = 1 LIMIT ?",
                    (limit,)
                ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 18. get_edited_articles
    # ------------------------------------------------------------------
    def get_edited_articles(self, source_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get articles that have edit events."""
        with self._store._conn() as conn:
            if source_id:
                rows = conn.execute(
                    """SELECT DISTINCT a.* FROM forum_articles a
                    JOIN forum_edit_events e ON a.article_id = e.article_id
                    WHERE a.source_id = ? LIMIT ?""",
                    (source_id, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT DISTINCT a.* FROM forum_articles a
                    JOIN forum_edit_events e ON a.article_id = e.article_id
                    LIMIT ?""",
                    (limit,)
                ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 19. get_duplicate_cluster
    # ------------------------------------------------------------------
    def get_duplicate_cluster(self, body_hash: str) -> List[Dict]:
        """Get articles sharing a body hash (duplicate cluster)."""
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_articles WHERE body_hash = ?",
                (body_hash,)
            ).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 20. get_market_sentiment_snapshot
    # ------------------------------------------------------------------
    def get_market_sentiment_snapshot(self, window: str, dimension: str = "market",
                                       dimension_value: Optional[str] = None) -> Optional[Dict]:
        """
        Get most recent market sentiment snapshot.
        [!] formal_standalone is always False.
        """
        with self._store._conn() as conn:
            if dimension_value:
                row = conn.execute(
                    """SELECT * FROM market_sentiment_snapshots
                    WHERE window = ? AND dimension = ? AND dimension_value = ?
                    ORDER BY snapshot_id DESC LIMIT 1""",
                    (window, dimension, dimension_value)
                ).fetchone()
            else:
                row = conn.execute(
                    """SELECT * FROM market_sentiment_snapshots
                    WHERE window = ? AND dimension = ?
                    ORDER BY snapshot_id DESC LIMIT 1""",
                    (window, dimension)
                ).fetchone()
        if row:
            result = dict(row)
            result["formal_standalone"] = False  # always
            return result
        return None

    # ------------------------------------------------------------------
    # 21. get_lineage_for_article
    # ------------------------------------------------------------------
    def get_lineage_for_article(self, article_id: str) -> Dict:
        """Get full lineage: versions, edits, deletions for an article."""
        article = self._store.get_article(article_id)
        versions = self._store.get_article_versions(article_id)
        with self._store._conn() as conn:
            edits = conn.execute(
                "SELECT * FROM forum_edit_events WHERE article_id = ? ORDER BY edit_id",
                (article_id,)
            ).fetchall()
            deletions = conn.execute(
                "SELECT * FROM forum_deletion_events WHERE article_id = ? ORDER BY deletion_id",
                (article_id,)
            ).fetchall()
        return {
            "article_id": article_id,
            "article": article,
            "versions": versions,
            "edit_events": [dict(e) for e in edits],
            "deletion_events": [dict(d) for d in deletions],
            "formal_standalone_allowed": False,
            "authority": "SUPPLEMENTARY",
        }

    # ------------------------------------------------------------------
    # Explain forum availability
    # ------------------------------------------------------------------
    def explain_forum_availability(self) -> Dict:
        """Explain what forum data is available and its limitations."""
        sources = self.list_sources()
        return {
            "sources_available": len(sources),
            "authority": "SUPPLEMENTARY",
            "can_generate_buy_sell": False,
            "can_override_official_source": False,
            "formal_standalone_allowed": False,
            "private_board_access": False,
            "login_bypass": False,
            "full_ip_stored": False,
            "identity_inference": False,
            "note": (
                "Forum data is SUPPLEMENTARY and UNVERIFIED. "
                "Cannot replace or override official market data. "
                "Research use only."
            ),
        }
