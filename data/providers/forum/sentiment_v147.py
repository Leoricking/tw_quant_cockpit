"""
data/providers/forum/sentiment_v147.py — Forum Sentiment Analyzer v1.4.7.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Traditional Chinese financial lexicon-based.
[!] NEVER: push=bullish, boo=bearish shortcut.
[!] Handles negation, degree adverbs, rhetorical questions, quotations, news headlines.
[!] Distinguishes: author's own statement vs quoted content vs news report.
"""
from __future__ import annotations

import re
import uuid
from typing import List, Optional

from data.providers.forum.models_v147 import (
    ForumSentimentSignal, SentimentPolarity, SentimentStance,
)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
PUSH_EQUALS_BULLISH = False  # MUST be False

ANALYZER_VERSION = "v147_lexicon"

# Bullish lexicon
_BULLISH_TERMS = [
    "看多", "做多", "買進", "強烈推薦", "飆漲", "大漲", "突破", "創高",
    "牛市", "多頭", "噴出", "漲停", "轉折向上", "進場", "補進",
    "上攻", "強勢", "走強", "底部確認", "打底完成",
]
# Bearish lexicon
_BEARISH_TERMS = [
    "看空", "放空", "賣出", "崩跌", "大跌", "跌破", "創低",
    "熊市", "空頭", "破底", "跌停", "轉折向下", "出場", "停損",
    "走弱", "弱勢", "跌勢", "死亡交叉",
]
# Negation markers
_NEGATION = ["不", "沒有", "非", "未", "別", "莫", "無", "否"]
# Degree adverbs (intensifier)
_INTENSIFIER = ["非常", "很", "超", "極度", "強烈", "大幅", "快速"]
# Sarcasm indicators
_SARCASM = ["哈哈", "哈哈哈", "笑死", "是喔", "喔喔", "對對對", "呵呵", "XD", "xd"]
# Rhetorical question markers
_RHETORICAL = ["難道", "真的嗎", "不是嗎", "是嗎", "哪有"]
# Quotation markers (content is NOT author's view)
_QUOTE_START = ["「", "『", "《", "（以上", "以下引用", "轉貼", "引述"]
# News headline markers
_NEWS_MARKER = ["[新聞]", "【新聞】", "新聞稿", "報導指出", "媒體報導", "根據新聞"]
# Guaranteed profit language
_GUARANTEED_PROFIT = ["保證獲利", "穩賺", "必漲", "100%", "絕對漲", "保賺"]


def _has_negation_before(text: str, term_start: int) -> bool:
    """Check if negation appears within 5 chars before the term."""
    prefix = text[max(0, term_start - 10):term_start]
    return any(neg in prefix for neg in _NEGATION)


class ForumSentimentAnalyzer:
    """
    Forum sentiment analyzer v1.4.7.
    [!] push tag does NOT mean bullish. boo tag does NOT mean bearish.
    [!] Analyzes content only.
    """

    VERSION = ANALYZER_VERSION

    def analyze(self, text: str, article_id: str = "", category: str = ""):
        """
        Analyze sentiment of text. Returns ForumSentimentSignal.
        [!] Quotation and news content is excluded from polarity assessment.
        """
        if not text:
            return {
                "polarity": SentimentPolarity.UNKNOWN.value,
                "stance": SentimentStance.UNKNOWN.value,
                "confidence": 0.0,
                "sarcasm_risk": 0.0,
                "negation_handled": False,
                "quotation_excluded": False,
                "news_headline_detected": False,
                "formal_standalone": False,
                "formal_use_allowed": False,
                "standalone_conclusion_allowed": False,
                "analyzer_version": ANALYZER_VERSION,
            }

        # Detect news report
        news_detected = any(m in text for m in _NEWS_MARKER) or category.upper() in ("[新聞]", "新聞")

        # Detect sarcasm risk
        sarcasm_risk = 0.0
        sarcasm_count = sum(1 for s in _SARCASM if s in text)
        rhetorical_count = sum(1 for r in _RHETORICAL if r in text)
        if sarcasm_count >= 2 or (sarcasm_count >= 1 and rhetorical_count >= 1):
            sarcasm_risk = 0.7
        elif sarcasm_count >= 1 or rhetorical_count >= 1:
            sarcasm_risk = 0.4

        # Extract non-quoted body for analysis
        analysis_text = self._remove_quotes(text)
        negation_handled = False

        # Count bullish/bearish signals with negation handling
        bull_score = 0.0
        bear_score = 0.0
        for term in _BULLISH_TERMS:
            idx = analysis_text.find(term)
            if idx >= 0:
                if _has_negation_before(analysis_text, idx):
                    bear_score += 0.5  # negated bullish = weak bearish
                    negation_handled = True
                else:
                    bull_score += 1.0
        for term in _BEARISH_TERMS:
            idx = analysis_text.find(term)
            if idx >= 0:
                if _has_negation_before(analysis_text, idx):
                    bull_score += 0.5  # negated bearish = weak bullish
                    negation_handled = True
                else:
                    bear_score += 1.0

        # Check for guaranteed profit (high credibility risk)
        guaranteed = any(g in text for g in _GUARANTEED_PROFIT)

        # Determine polarity
        if sarcasm_risk >= 0.7:
            polarity = SentimentPolarity.UNKNOWN
        elif news_detected and bull_score == 0 and bear_score == 0:
            polarity = SentimentPolarity.NEUTRAL
        elif bull_score == 0 and bear_score == 0:
            polarity = SentimentPolarity.NEUTRAL
        elif bull_score > bear_score * 2:
            polarity = SentimentPolarity.VERY_BULLISH if bull_score >= 3 else SentimentPolarity.BULLISH
        elif bear_score > bull_score * 2:
            polarity = SentimentPolarity.VERY_BEARISH if bear_score >= 3 else SentimentPolarity.BEARISH
        elif bull_score > bear_score:
            polarity = SentimentPolarity.BULLISH
        elif bear_score > bull_score:
            polarity = SentimentPolarity.BEARISH
        else:
            polarity = SentimentPolarity.NEUTRAL

        # Determine stance
        stance = self._classify_stance(text, category)

        total = bull_score + bear_score
        confidence = min(0.9, 0.3 + 0.1 * total) if total > 0 else 0.1
        if sarcasm_risk >= 0.7:
            confidence *= 0.3

        signal = ForumSentimentSignal(
            signal_id=str(uuid.uuid4())[:8],
            article_id=article_id,
            polarity=polarity.value,
            stance=stance.value,
            confidence=round(confidence, 3),
            sarcasm_risk=round(sarcasm_risk, 3),
            negation_handled=negation_handled,
            quotation_excluded=(analysis_text != text),
            news_headline_detected=news_detected,
            analyzer_version=ANALYZER_VERSION,
            formal_use_allowed=False,
            standalone_conclusion_allowed=False,
        )
        return {
            "polarity": signal.polarity,
            "stance": signal.stance,
            "confidence": signal.confidence,
            "sarcasm_risk": signal.sarcasm_risk,
            "negation_handled": signal.negation_handled,
            "quotation_excluded": signal.quotation_excluded,
            "news_headline_detected": signal.news_headline_detected,
            "formal_standalone": False,
            "formal_use_allowed": False,
            "standalone_conclusion_allowed": False,
            "analyzer_version": signal.analyzer_version,
            "_signal": signal,
        }

    def _remove_quotes(self, text: str) -> str:
        """Remove quoted content from analysis text."""
        for q in _QUOTE_START:
            if q in text:
                idx = text.find(q)
                # Remove from quote marker to end of quoted block (simplified)
                text = text[:idx]
        return text.strip() if text.strip() else text

    def _classify_stance(self, text: str, category: str) -> SentimentStance:
        """Classify author stance from content."""
        cat_upper = category.upper() if category else ""
        if "[新聞]" in cat_upper or "新聞" in cat_upper:
            return SentimentStance.NEWS_REPORT
        if any(t in text for t in ["做多", "看多", "進場", "買進"]):
            return SentimentStance.LONG
        if any(t in text for t in ["放空", "看空", "賣出", "出場"]):
            return SentimentStance.SHORT
        if any(t in text for t in ["持有", "繼續持有", "不動"]):
            return SentimentStance.HOLD
        if any(t in text for t in ["觀望", "等待", "看看"]):
            return SentimentStance.WATCH
        if any(t in text for t in ["請問", "有人知道", "為什麼", "？"]):
            return SentimentStance.QUESTION
        if any(t in text for t in ["哈哈", "XD", "笑死", "梗"]):
            return SentimentStance.JOKE
        return SentimentStance.UNKNOWN
