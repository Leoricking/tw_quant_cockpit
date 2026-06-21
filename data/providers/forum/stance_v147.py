"""
data/providers/forum/stance_v147.py — Forum Stance Classifier v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Context-aware stance classification.
"""
from __future__ import annotations

from data.providers.forum.models_v147 import SentimentStance

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ForumStanceClassifier:
    """
    Stance classifier: LONG/SHORT/HOLD/WATCH/QUESTION/NEWS_REPORT/JOKE/SARCASM/UNKNOWN.
    Context-aware. Does not use push/boo tags.
    """

    def classify(self, text: str, category: str = "", title: str = "") -> SentimentStance:
        """Classify author stance from full context."""
        if not text and not title:
            return SentimentStance.UNKNOWN
        combined = (title + " " + text).lower()
        category_upper = category.upper() if category else ""

        # News report
        if "[新聞]" in category or "新聞" in category_upper:
            return SentimentStance.NEWS_REPORT

        # Joke / humor
        if any(t in combined for t in ["哈哈", "xd", "笑死", "梗圖", "幹話"]):
            return SentimentStance.JOKE

        # Sarcasm
        if any(t in combined for t in ["是喔", "對對對", "了不起", "厲害厲害"]):
            return SentimentStance.SARCASM

        # Long
        if any(t in combined for t in ["做多", "看多", "進場", "加碼", "買進", "long"]):
            return SentimentStance.LONG

        # Short
        if any(t in combined for t in ["放空", "看空", "做空", "賣出", "出場", "short"]):
            return SentimentStance.SHORT

        # Hold
        if any(t in combined for t in ["持有", "繼續持", "不動作", "持股", "hold"]):
            return SentimentStance.HOLD

        # Watch
        if any(t in combined for t in ["觀望", "等待", "先看", "再看", "watch"]):
            return SentimentStance.WATCH

        # Question
        if any(t in combined for t in ["請問", "有人嗎", "為什麼", "怎麼了", "?"]):
            return SentimentStance.QUESTION

        return SentimentStance.UNKNOWN
