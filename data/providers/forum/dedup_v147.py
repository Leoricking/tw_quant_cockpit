"""
data/providers/forum/dedup_v147.py — Forum Deduplicator v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Duplicate detection: exact, near, cross-post, comment spam.
"""
from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional, Tuple

from data.providers.forum.models_v147 import ForumDuplicateStatus

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _title_similarity(t1: str, t2: str) -> float:
    """Simple character n-gram similarity between two titles."""
    if not t1 or not t2:
        return 0.0
    if t1 == t2:
        return 1.0
    # Jaccard on 3-grams
    def ngrams(s: str, n: int = 3):
        return set(s[i:i+n] for i in range(len(s) - n + 1))
    a = ngrams(t1)
    b = ngrams(t2)
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union > 0 else 0.0


class ForumDeduplicator:
    """
    Deduplication service for forum articles and comments.
    - Exact: canonical URL, article_id, raw_hash, normalized_hash
    - Near: normalized title similarity
    - Cross-post: same external URL across articles
    - Comment spam: repeated text in article/across articles
    """

    def __init__(self) -> None:
        self._url_index: Dict[str, str] = {}        # url -> article_id
        self._id_index: Dict[str, str] = {}         # article_id -> article_id
        self._hash_index: Dict[str, str] = {}       # hash -> article_id
        self._norm_hash_index: Dict[str, str] = {}  # norm_hash -> article_id
        self._ext_link_index: Dict[str, List[str]] = {}  # ext_url -> [article_id]
        self._title_registry: List[Tuple[str, str]] = []  # [(norm_title, article_id)]

    def check_article(
        self,
        article_id: str,
        canonical_url: str,
        raw_hash: str,
        normalized_hash: str,
        title_normalized: str,
        external_links: Optional[List[str]] = None,
    ) -> Tuple[ForumDuplicateStatus, Dict[str, Any]]:
        """Check article for duplicates. Returns (status, evidence)."""
        # Exact: URL
        if canonical_url and canonical_url in self._url_index:
            orig = self._url_index[canonical_url]
            return ForumDuplicateStatus.EXACT_DUPLICATE, {"matched_url": canonical_url, "original_id": orig}
        # Exact: article_id
        if article_id and article_id in self._id_index:
            return ForumDuplicateStatus.EXACT_DUPLICATE, {"matched_id": article_id}
        # Exact: raw hash
        if raw_hash and raw_hash in self._hash_index:
            orig = self._hash_index[raw_hash]
            return ForumDuplicateStatus.EXACT_DUPLICATE, {"matched_hash": raw_hash, "original_id": orig}
        # Exact: normalized hash
        if normalized_hash and normalized_hash in self._norm_hash_index:
            orig = self._norm_hash_index[normalized_hash]
            return ForumDuplicateStatus.NEAR_DUPLICATE, {"matched_norm_hash": normalized_hash, "original_id": orig}
        # Near: title similarity
        if title_normalized:
            for known_title, known_id in self._title_registry:
                sim = _title_similarity(title_normalized, known_title)
                if sim >= 0.85:
                    return ForumDuplicateStatus.NEAR_DUPLICATE, {
                        "title_similarity": sim,
                        "matched_title": known_title,
                        "original_id": known_id,
                    }
        # Cross-post: same external link
        if external_links:
            for link in external_links:
                if link in self._ext_link_index and self._ext_link_index[link]:
                    return ForumDuplicateStatus.CROSS_POST, {
                        "shared_link": link,
                        "existing_articles": self._ext_link_index[link],
                    }
        return ForumDuplicateStatus.UNIQUE, {}

    def register_article(
        self,
        article_id: str,
        canonical_url: str,
        raw_hash: str,
        normalized_hash: str,
        title_normalized: str,
        external_links: Optional[List[str]] = None,
    ) -> None:
        """Register article for future dedup checks."""
        if canonical_url:
            self._url_index[canonical_url] = article_id
        if article_id:
            self._id_index[article_id] = article_id
        if raw_hash:
            self._hash_index[raw_hash] = article_id
        if normalized_hash:
            self._norm_hash_index[normalized_hash] = article_id
        if title_normalized:
            self._title_registry.append((title_normalized, article_id))
        if external_links:
            for link in external_links:
                self._ext_link_index.setdefault(link, []).append(article_id)

    def check_comment_spam(self, text: str, article_id: str, existing_texts: List[str]) -> bool:
        """Returns True if comment text appears to be spam (repeated in same article)."""
        if not text or len(text.strip()) < 3:
            return False
        normalized = " ".join(text.lower().split())
        count = sum(1 for t in existing_texts if " ".join(t.lower().split()) == normalized)
        return count >= 3  # 3+ identical comments = spam

    # ------------------------------------------------------------------
    # Convenience methods for simpler test interfaces
    # ------------------------------------------------------------------

    def check_url_duplicate(self, url1: str, url2: str) -> bool:
        """Return True if two URLs are identical (exact URL duplicate)."""
        return bool(url1 and url2 and url1 == url2)

    def check_id_duplicate(self, id1: str, id2: str) -> bool:
        """Return True if two article IDs are identical."""
        return bool(id1 and id2 and id1 == id2)

    def check_hash_duplicate(self, h1: str, h2: str) -> bool:
        """Return True if two hashes are identical."""
        return bool(h1 and h2 and h1 == h2)

    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute similarity between two texts (0.0 to 1.0).
        Uses length-normalized overlap: shorter text coverage vs longer text.
        """
        if not text1 or not text2:
            return 0.0
        if text1 == text2:
            return 1.0
        # Use prefix/suffix longest common: ratio of shorter contained in longer
        shorter, longer = (text1, text2) if len(text1) <= len(text2) else (text2, text1)
        # Character 3-gram multiset overlap (Dice coefficient)
        def ngrams(s: str, n: int = 3):
            return [s[i:i+n] for i in range(len(s) - n + 1)]
        ng1 = ngrams(shorter)
        ng2 = ngrams(longer)
        if not ng1 or not ng2:
            return len(shorter) / len(longer) if longer else 0.0
        from collections import Counter
        c1 = Counter(ng1)
        c2 = Counter(ng2)
        intersection = sum((c1 & c2).values())
        dice = 2.0 * intersection / (sum(c1.values()) + sum(c2.values()))
        return round(dice, 4)

    def normalize_hash(self, text: str) -> str:
        """Compute a normalized SHA-256 hash for dedup."""
        if not text:
            return ""
        normalized = " ".join(text.lower().split())
        return _sha256(normalized)

    def get_dedup_stats(self, hashes: List[str]) -> Dict[str, Any]:
        """Count duplicates in a list of hashes."""
        from collections import Counter
        counts = Counter(hashes)
        duplicate_count = sum(1 for v in counts.values() if v > 1)
        return {
            "total": len(hashes),
            "unique": len(counts),
            "duplicate_count": duplicate_count,
            "duplicate_adjusted": len(hashes) - duplicate_count,
        }
