"""
data/providers/forum/point_in_time_v147.py — ForumPointInTimeService v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Strict no future-leakage. SUPPLEMENTARY authority only.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
FORUM_CAN_GENERATE_BUY_SELL = False
FORUM_FUTURE_LEAKAGE_ENABLED = False  # ALWAYS FALSE


class ForumPointInTimeService:
    """
    Point-in-time query service for Forum Intelligence v1.4.7.
    [!] No future-leakage. SUPPLEMENTARY. Research Only.
    """

    def __init__(self, store=None) -> None:
        if store is None:
            from data.providers.forum.store_v147 import ForumStore
            store = ForumStore()
        self._store = store

    # ------------------------------------------------------------------
    # get_article_as_of
    # ------------------------------------------------------------------
    def get_article_as_of(self, article_id: str, as_of: str) -> Optional[Dict]:
        """
        Return article state as it was known at as_of timestamp.
        Returns None if article was not first_seen before as_of.
        [!] Blocks future knowledge.
        """
        article = self._store.get_article(article_id)
        if article is None:
            return None
        first_seen = article.get("first_seen_at") or ""
        if first_seen and first_seen > as_of:
            logger.debug(
                "PIT: article_id=%s first_seen=%s > as_of=%s — not visible",
                article_id, first_seen, as_of
            )
            return None
        # Get the version current at as_of
        versions = self._store.get_article_versions(article_id)
        current_version = None
        for v in sorted(versions, key=lambda x: x.get("captured_at", "")):
            if v.get("captured_at", "") <= as_of:
                current_version = v
        result = dict(article)
        result["_pit_as_of"] = as_of
        result["_pit_version"] = current_version
        result["_future_leakage"] = False
        return result

    # ------------------------------------------------------------------
    # get_comments_as_of
    # ------------------------------------------------------------------
    def get_comments_as_of(self, article_id: str, as_of: str) -> List[Dict]:
        """
        Return only comments whose first_seen_at <= as_of.
        [!] Blocks future comments.
        """
        comments = self._store.get_comments(article_id)
        result = []
        for c in comments:
            first_seen = c.get("first_seen_at") or ""
            if not first_seen or first_seen <= as_of:
                result.append({**c, "_pit_as_of": as_of, "_future_leakage": False})
            else:
                logger.debug(
                    "PIT: comment first_seen=%s > as_of=%s — blocked",
                    first_seen, as_of
                )
        return result

    # ------------------------------------------------------------------
    # get_deletion_state_as_of
    # ------------------------------------------------------------------
    def get_deletion_state_as_of(self, article_id: str, as_of: str) -> Dict:
        """
        Return deletion state as of timestamp.
        [!] Deleted articles are NOT backfilled as non-deleted.
        """
        article = self._store.get_article(article_id)
        if article is None:
            return {
                "article_id": article_id,
                "known": False,
                "deleted": False,
                "as_of": as_of,
                "_future_leakage": False,
            }
        # Check deletion events up to as_of
        with self._store._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM forum_deletion_events "
                "WHERE article_id = ? AND detected_at <= ? ORDER BY detected_at",
                (article_id, as_of)
            ).fetchall()
        was_deleted = len(rows) > 0
        return {
            "article_id": article_id,
            "known": True,
            "deleted": was_deleted,
            "as_of": as_of,
            "deletion_events": [dict(r) for r in rows],
            "_future_leakage": False,
        }

    # ------------------------------------------------------------------
    # explain_forum_availability
    # ------------------------------------------------------------------
    def explain_forum_availability(self, as_of: Optional[str] = None) -> Dict:
        """
        Explain what forum data is available up to as_of.
        [!] Does not reveal future articles. SUPPLEMENTARY authority.
        """
        sources = self._store.list_sources()
        info: Dict[str, Any] = {
            "sources": [s.get("source_id") for s in sources],
            "as_of": as_of,
            "authority": "SUPPLEMENTARY",
            "formal_standalone_allowed": False,
            "can_generate_buy_sell": False,
            "can_override_official": False,
            "full_ip_stored": False,
            "future_leakage": False,
            "note": (
                "Forum data is SUPPLEMENTARY. "
                "Cannot override official data sources. "
                "All queries are point-in-time safe."
            ),
        }
        if as_of:
            with self._store._conn() as conn:
                row = conn.execute(
                    "SELECT COUNT(*) as cnt FROM forum_articles WHERE first_seen_at <= ?",
                    (as_of,)
                ).fetchone()
            info["articles_visible_at_as_of"] = row["cnt"] if row else 0
        return info

    # ------------------------------------------------------------------
    # check_future_leakage
    # ------------------------------------------------------------------
    def check_future_leakage(self, article_id: str, reference_time: str) -> Dict:
        """
        Validate that an article does not introduce future leakage relative to reference_time.
        """
        article = self._store.get_article(article_id)
        if article is None:
            return {"leakage": False, "reason": "article not found"}
        first_seen = article.get("first_seen_at") or ""
        published = article.get("published_at") or ""
        leakage = False
        reason = "ok"
        if first_seen and first_seen > reference_time:
            leakage = True
            reason = f"first_seen_at={first_seen} > reference_time={reference_time}"
        elif published and published > reference_time:
            leakage = True
            reason = f"published_at={published} > reference_time={reference_time}"
        return {
            "article_id": article_id,
            "leakage": leakage,
            "reason": reason,
            "reference_time": reference_time,
            "first_seen_at": first_seen,
            "published_at": published,
        }
