"""
data/providers/forum/credibility_v147.py — Forum Credibility Analyzer v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Evaluates CONTENT EVIDENCE QUALITY ONLY — NOT author character.
[!] NEVER outputs person credit score or real identity judgment.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List

from data.providers.forum.models_v147 import ForumCredibilitySignal

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
PERSON_CREDIT_SCORE_ENABLED = False  # MUST be False

_OFFICIAL_SOURCE_INDICATORS = [
    "twse", "mops", "tpex", "data.gov.tw", "金管會", "證交所",
    "公開資訊觀測站", "財報", "法說會", "官方公告",
]
_CONCRETE_NUMBER_PATTERN = [
    "eps", "pe", "pb", "毛利率", "營收", "億元", "萬元",
    "成長率", "%", "倍",
]
_RUMOR_TERMS = ["聽說", "傳說", "據說", "消息稱", "耳聞", "小道消息", "未經證實"]
_GUARANTEED_PROFIT = ["保證賺", "穩賺", "必漲", "百分百", "100%獲利", "保證獲利"]
_CERTAINTY_RISK_TERMS = ["一定會", "絕對", "必然", "不可能輸", "100%"]


class ForumCredibilityAnalyzer:
    """
    Content credibility analyzer.
    [!] No person credit score. Content evidence quality only.
    """

    def analyze(self, article_id: str, text: str,
                has_edit: bool = False, has_deletion_risk: bool = False) -> ForumCredibilitySignal:
        """Evaluate content credibility. Returns ForumCredibilitySignal."""
        if not text:
            return ForumCredibilitySignal(
                signal_id=str(uuid.uuid4())[:8],
                article_id=article_id,
                person_credit_score_generated=False,
            )

        text_lower = text.lower()

        official_links = sum(1 for t in _OFFICIAL_SOURCE_INDICATORS if t.lower() in text_lower)
        concrete_nums = sum(1 for t in _CONCRETE_NUMBER_PATTERN if t.lower() in text_lower)
        rumor = sum(1 for t in _RUMOR_TERMS if t in text)
        guaranteed = sum(1 for t in _GUARANTEED_PROFIT if t in text)
        certainty = sum(1 for t in _CERTAINTY_RISK_TERMS if t in text)
        unsupported = max(0, rumor)

        # Compute content quality score (0-1)
        positive = min(1.0, (official_links * 0.3 + concrete_nums * 0.1))
        negative = min(1.0, (rumor * 0.15 + guaranteed * 0.3 + certainty * 0.1))
        quality = max(0.0, min(1.0, 0.5 + positive - negative))

        # Certainty risk (0-1)
        certainty_risk = min(1.0, (guaranteed + certainty) * 0.25)

        return ForumCredibilitySignal(
            signal_id=str(uuid.uuid4())[:8],
            article_id=article_id,
            official_source_links=official_links,
            concrete_numbers=concrete_nums,
            unsupported_claims=unsupported,
            rumor_terms=rumor,
            guaranteed_profit_language=(guaranteed > 0),
            certainty_risk=round(certainty_risk, 3),
            edit_after_publish=has_edit,
            deletion_risk=0.3 if has_deletion_risk else 0.0,
            content_quality_score=round(quality, 3),
            person_credit_score_generated=False,  # MUST be False
        )


class ForumCredibilityAssessor:
    """
    Simplified credibility assessor interface.
    Wraps ForumCredibilityAnalyzer.analyze() accepting article dicts.
    [!] Content evidence quality only. NEVER person credit score.
    """

    def __init__(self) -> None:
        self._analyzer = ForumCredibilityAnalyzer()

    def assess(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess credibility of an article dict.
        article: dict with 'title', 'body', optional 'edit_count', 'is_deleted'
        Returns dict with credibility metrics.
        [!] NEVER scores a person. Content quality only.
        """
        if not isinstance(article, dict):
            article = {}
        text = (article.get("title") or "") + " " + (article.get("body") or "")
        article_id = article.get("article_id") or ""
        edit_count = article.get("edit_count", 0) or 0
        is_deleted = article.get("is_deleted", False)

        signal = self._analyzer.analyze(
            article_id=article_id,
            text=text.strip(),
            has_edit=(edit_count > 0),
            has_deletion_risk=bool(is_deleted),
        )

        return {
            "has_official_link": (signal.official_source_links or 0) > 0,
            "has_concrete_numbers": (signal.concrete_numbers or 0) > 0,
            "has_unsupported_claim": (signal.unsupported_claims or 0) > 0,
            "has_rumor_terms": (signal.rumor_terms or 0) > 0,
            "has_guaranteed_profit": signal.guaranteed_profit_language or False,
            "edit_risk": "HIGH" if edit_count > 2 else "LOW",
            "deletion_risk": signal.deletion_risk or 0.0,
            "content_credibility": signal.content_quality_score or 0.5,
            "certainty_risk": signal.certainty_risk or 0.0,
            "formal_standalone": False,
        }
