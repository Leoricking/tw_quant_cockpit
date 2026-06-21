"""
data/providers/forum/engagement_v147.py — Forum Engagement Analyzer v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No real person identification. repeat_commenter_ratio based on hash only.
"""
from __future__ import annotations

import uuid
from typing import List, Optional

from data.providers.forum.models_v147 import ForumComment, ForumEngagementSignal

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
IDENTITY_INFERENCE_ENABLED = False


class ForumEngagementAnalyzer:
    """
    Engagement analytics for forum articles.
    [!] All commenter tracking is via hash — never real identity.
    """

    def analyze(self, article_id_or_comments, comments: Optional[List] = None) -> dict:
        """
        Compute engagement metrics from comment list.
        Accepts:
          analyze(article_id, comments)  — original signature
          analyze(comments)              — simplified, article_id defaults to ""
        Comments may be ForumComment objects or dicts with 'tag'/'author_display_id' keys.
        Always returns dict for easy consumption.
        """
        if comments is None:
            # Called as analyze(comments_list)
            article_id = ""
            comments = article_id_or_comments if isinstance(article_id_or_comments, list) else []
        else:
            article_id = article_id_or_comments if isinstance(article_id_or_comments, str) else ""

        def _get(c, key, default=None):
            if isinstance(c, dict):
                return c.get(key, default)
            return getattr(c, key, default)

        if not comments:
            return {
                "total_comments": 0, "push_count": 0, "boo_count": 0,
                "neutral_count": 0, "unique_commenters": 0,
                "push_ratio": 0.0, "boo_ratio": 0.0, "neutral_ratio": 0.0,
                "velocity": 0.0, "velocity_1h": 0.0, "burst_score": 0.0,
                "concentration": 0.0, "repeat_commenter_ratio": 0.0,
                "duplicate_adjusted_volume": 0,
            }

        push = sum(1 for c in comments if _get(c, "tag") == "PUSH")
        boo = sum(1 for c in comments if _get(c, "tag") == "BOO")
        neutral = sum(1 for c in comments if _get(c, "tag") == "NEUTRAL")
        total = len(comments)

        push_ratio = push / total if total > 0 else 0.0
        boo_ratio = boo / total if total > 0 else 0.0
        neutral_ratio = neutral / total if total > 0 else 0.0

        # Unique commenter count by display_id or hash
        ids = [
            _get(c, "author_display_id") or _get(c, "author_id_hash")
            for c in comments
        ]
        ids = [i for i in ids if i]
        unique_count = len(set(ids))

        # Repeat commenter ratio
        if total > 0 and ids:
            from collections import Counter
            id_counts = Counter(ids)
            repeat = sum(1 for cnt in id_counts.values() if cnt > 1)
            repeat_ratio = repeat / len(id_counts) if id_counts else 0.0
        else:
            repeat_ratio = 0.0

        # Concentration: max single commenter contribution
        if ids:
            from collections import Counter
            max_count = Counter(ids).most_common(1)[0][1]
            concentration = max_count / total if total > 0 else 0.0
        else:
            concentration = 0.0

        # Duplicate-adjusted volume
        from collections import Counter
        texts = [_get(c, "text") or "" for c in comments]
        text_counts = Counter(t.strip().lower() for t in texts if t)
        spam_count = sum(cnt - 1 for cnt in text_counts.values() if cnt > 2)
        dup_adj = max(0, total - spam_count)

        # Burst score
        burst_score = 0.0
        if total >= 5:
            seq = [_get(c, "sequence", 0) or 0 for c in comments]
            first_half = len([s for s in seq if s < total // 2])
            burst_score = round(first_half / total, 3)

        return {
            "total_comments": total,
            "push_count": push,
            "boo_count": boo,
            "neutral_count": neutral,
            "unique_commenters": unique_count,
            "push_ratio": round(push_ratio, 3),
            "boo_ratio": round(boo_ratio, 3),
            "neutral_ratio": round(neutral_ratio, 3),
            "velocity": 0.0,
            "velocity_1h": 0.0,
            "burst_score": burst_score,
            "concentration": round(concentration, 3),
            "repeat_commenter_ratio": round(repeat_ratio, 3),
            "duplicate_adjusted_volume": dup_adj,
        }
