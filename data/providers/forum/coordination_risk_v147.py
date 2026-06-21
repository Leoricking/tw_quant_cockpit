"""
data/providers/forum/coordination_risk_v147.py — Forum Coordination Risk Detector v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] NEVER identify same real person across accounts.
[!] NEVER accuse of crime. NEVER cross-platform de-anonymization.
"""
from __future__ import annotations

import uuid
from collections import Counter
from typing import Any, Dict, List

from data.providers.forum.models_v147 import ForumComment, ForumCoordinationRisk, ManipulationRiskLevel

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
IDENTITY_LINKING_ENABLED = False  # MUST be False
CROSS_PLATFORM_DEANON_ENABLED = False  # MUST be False
CRIME_ACCUSATION_ENABLED = False  # MUST be False


class ForumCoordinationRiskDetector:
    """
    Coordination risk detection based on content patterns.
    [!] No identity linking. No cross-platform de-anonymization. No crime labels.
    """

    def analyze(self, article_id: str, comments: List[ForumComment]) -> ForumCoordinationRisk:
        """Detect coordination risk patterns in comments."""
        if not comments:
            return ForumCoordinationRisk(
                risk_id=str(uuid.uuid4())[:8],
                article_id=article_id,
                risk_level=ManipulationRiskLevel.UNKNOWN.value,
                identity_linking_performed=False,
                cross_platform_deanon_performed=False,
            )

        texts = [c.text.strip().lower() for c in comments if c.text]
        hashes = [c.author_id_hash for c in comments if c.author_id_hash]

        # Repeated text score
        if texts:
            text_counts = Counter(texts)
            max_repeat = max(text_counts.values())
            repeated_text_score = min(1.0, (max_repeat - 1) / max(len(texts), 1))
        else:
            repeated_text_score = 0.0

        # Copy-paste cluster count (texts appearing 3+ times)
        copy_paste = sum(1 for cnt in Counter(texts).values() if cnt >= 3) if texts else 0

        # Commenter overlap (concentration)
        if hashes:
            hash_counts = Counter(hashes)
            top_3 = sum(v for _, v in hash_counts.most_common(3))
            commenter_overlap = top_3 / len(hashes) if hashes else 0.0
        else:
            commenter_overlap = 0.0

        # Synchronized post score (simplified: many comments with no time info)
        # Without timestamps, we use sequence clustering
        synchronized_score = 0.0
        if len(comments) >= 5:
            # Check if many comments came in rapid sequence
            first_10pct = max(1, len(comments) // 10)
            first_batch = comments[:first_10pct]
            if len(first_batch) > 0:
                synchronized_score = min(1.0, len(first_batch) / len(comments))

        # Same symbol burst (simplified: check title mentions of same symbol)
        same_symbol_burst = 0.0

        # Compute overall risk
        risk_score = (
            repeated_text_score * 0.4 +
            commenter_overlap * 0.3 +
            synchronized_score * 0.2 +
            min(1.0, copy_paste * 0.1)
        )
        if risk_score >= 0.7:
            level = ManipulationRiskLevel.CRITICAL
        elif risk_score >= 0.5:
            level = ManipulationRiskLevel.HIGH
        elif risk_score >= 0.3:
            level = ManipulationRiskLevel.MEDIUM
        elif risk_score > 0.0:
            level = ManipulationRiskLevel.LOW
        else:
            level = ManipulationRiskLevel.LOW

        return ForumCoordinationRisk(
            risk_id=str(uuid.uuid4())[:8],
            article_id=article_id,
            repeated_text_score=round(repeated_text_score, 3),
            synchronized_post_score=round(synchronized_score, 3),
            same_link_score=0.0,
            same_symbol_burst_score=same_symbol_burst,
            commenter_overlap_score=round(commenter_overlap, 3),
            copy_paste_cluster_count=copy_paste,
            risk_level=level.value,
            identity_linking_performed=False,  # MUST be False
            cross_platform_deanon_performed=False,  # MUST be False
        )


class ForumCoordinationRiskAssessor:
    """
    Simplified coordination risk interface for assessing article clusters.
    Accepts list of article dicts (no ForumComment objects required).
    [!] No identity linking. No criminal labels. Classification only.
    """

    def __init__(self) -> None:
        self._detector = ForumCoordinationRiskDetector()

    def assess_cluster(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess coordination risk for a cluster of articles.
        articles: list of dicts with 'title', 'body' keys.
        Returns dict with risk_level, risk_signals, criminal_label=None.
        [!] criminal_label=None always. legal_accusation=None always.
        """
        if not isinstance(articles, list) or not articles:
            return {
                "risk_level": ManipulationRiskLevel.LOW.value,
                "risk_signals": [],
                "criminal_label": None,
                "legal_accusation": None,
                "identity_linking_performed": False,
            }

        # Detect risk signals from article content
        risk_signals = []
        all_text = [(a.get("title") or "") + " " + (a.get("body") or "") for a in articles]

        # Repeated title signal
        titles = [(a.get("title") or "").strip() for a in articles]
        if len(set(titles)) < len(titles):
            risk_signals.append("repeated_text")

        # Same URL in bodies
        import re as _re
        url_pattern = _re.compile(r"https?://\S+")
        all_urls = []
        for text in all_text:
            all_urls.extend(url_pattern.findall(text))
        from collections import Counter as _Counter
        url_counts = _Counter(all_urls)
        if any(v > 1 for v in url_counts.values()):
            risk_signals.append("same_url_burst")

        # Symbol burst
        sym_pattern = _re.compile(r"\b\d{4}\b")
        all_syms = []
        for text in all_text:
            all_syms.extend(sym_pattern.findall(text))
        sym_counts = _Counter(all_syms)
        if any(v > 3 for v in sym_counts.values()):
            risk_signals.append("symbol_burst")

        # Determine risk level
        if len(risk_signals) >= 2:
            risk_level = ManipulationRiskLevel.HIGH.value
        elif len(risk_signals) == 1:
            risk_level = ManipulationRiskLevel.MEDIUM.value
        else:
            risk_level = ManipulationRiskLevel.LOW.value

        return {
            "risk_level": risk_level,
            "risk_signals": risk_signals,
            "criminal_label": None,   # MUST be None
            "legal_accusation": None,  # MUST be None
            "identity_linking_performed": False,
        }

    def assess_commenter_overlap(self, cluster_a: List[str], cluster_b: List[str]) -> Dict[str, Any]:
        """
        Assess overlap between two commenter ID sets.
        [!] No identity inference. Classification only.
        Returns dict with overlap_count, overlap_ratio, risk_level.
        """
        if not cluster_a or not cluster_b:
            return {"overlap_count": 0, "overlap_ratio": 0.0, "risk_level": "LOW"}
        set_a = set(cluster_a)
        set_b = set(cluster_b)
        overlap = set_a & set_b
        overlap_ratio = len(overlap) / min(len(set_a), len(set_b))
        risk_level = "HIGH" if overlap_ratio > 0.5 else "MEDIUM" if overlap_ratio > 0.2 else "LOW"
        return {
            "overlap_count": len(overlap),
            "overlap_ratio": round(overlap_ratio, 3),
            "risk_level": risk_level,
            "criminal_label": None,
            "legal_accusation": None,
        }
