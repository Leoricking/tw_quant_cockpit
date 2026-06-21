"""
data/providers/forum/manipulation_risk_v147.py — ForumManipulationRiskDetector v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Risk classification only. No criminal labels. No legal accusations.
[!] SUPPLEMENTARY authority. Cannot override official sources.
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
FORUM_CAN_MAKE_CRIMINAL_ACCUSATIONS = False  # ALWAYS FALSE
FORUM_CAN_MAKE_LEGAL_ACCUSATIONS = False      # ALWAYS FALSE

_URGENCY_TERMS = frozenset([
    "今天最後機會", "明天就來不及", "限時", "搶先", "千萬別錯過",
    "last chance", "urgent", "must buy now", "don't miss",
])
_PROFIT_GUARANTEE_TERMS = frozenset([
    "保證獲利", "穩賺", "不虧", "100%賺", "保證漲",
    "guaranteed profit", "100% gain", "no loss", "sure win",
])
_EXTREME_TARGET_PATTERNS = (
    "漲停", "漲停板", "飆漲", "翻倍", "十倍",
    "to the moon", "10x", "100%",
)


class ForumManipulationRiskDetector:
    """
    Detects manipulation risk signals in forum articles.
    [!] Risk classification only — no criminal or legal labels.
    [!] No identity inference. No criminal accusations.
    """

    def assess(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess manipulation risk for an article.
        Returns risk_level (LOW/MEDIUM/HIGH/CRITICAL) and risk signals.
        [!] No criminal label. No legal accusation.
        """
        title = str(article.get("title") or "").lower()
        body = str(article.get("body") or "").lower()
        content = title + " " + body

        signals: List[str] = []

        # Urgency language
        for term in _URGENCY_TERMS:
            if term.lower() in content:
                signals.append(f"urgency_language:{term}")

        # Profit guarantees
        for term in _PROFIT_GUARANTEE_TERMS:
            if term.lower() in content:
                signals.append(f"profit_guarantee:{term}")

        # Extreme price targets
        for pat in _EXTREME_TARGET_PATTERNS:
            if pat.lower() in content:
                signals.append(f"extreme_target:{pat}")

        # Coordination signals from article metadata
        coord_risk = article.get("coordination_risk_level", "LOW")
        if coord_risk in ("HIGH", "CRITICAL"):
            signals.append(f"coordination_input:{coord_risk}")

        # Conflict with official sources
        official_conflict = article.get("conflicts_with_official", False)
        if official_conflict:
            signals.append("official_source_conflict")

        # Low liquidity targeting (if symbol info provided)
        if article.get("low_liquidity_symbol"):
            signals.append("low_liquidity_targeting")

        # Determine risk level
        risk_level = self._classify_risk(signals)

        result = {
            "article_id": article.get("article_id"),
            "risk_level": risk_level,
            "risk_signals": signals,
            "assessed_at": datetime.utcnow().isoformat() + "Z",
            "criminal_label": None,   # ALWAYS None
            "legal_accusation": None, # ALWAYS None
            "formal_standalone": False,
            "authority": "SUPPLEMENTARY",
            "note": (
                "Manipulation risk is a content signal only. "
                "No criminal or legal labels assigned. "
                "Not Investment Advice."
            ),
        }
        return result

    def _classify_risk(self, signals: List[str]) -> str:
        """Classify risk level based on signal count and severity."""
        if not signals:
            return "LOW"
        profit_guarantee = sum(1 for s in signals if s.startswith("profit_guarantee"))
        official_conflict = sum(1 for s in signals if s == "official_source_conflict")
        if profit_guarantee >= 1 and official_conflict >= 1:
            return "CRITICAL"
        if profit_guarantee >= 1:
            return "HIGH"
        if len(signals) >= 3:
            return "MEDIUM"
        if len(signals) >= 1:
            return "LOW"
        return "LOW"

    def assess_batch(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assess multiple articles."""
        return [self.assess(a) for a in articles]
