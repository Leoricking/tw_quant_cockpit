"""
knowledge/knowledge_extractor.py — StrategyKnowledgeExtractor: rule-based keyword extraction (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No external API calls. No LLM. No requests. Rule-based keyword matching only.
[!] auto_activated is ALWAYS False. Confidence capped at PARTIAL.
"""
from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

from knowledge.knowledge_schema import (
    StrategyKnowledgeItem,
    MAX_TRANSCRIPT_CONFIDENCE,
    CATEGORY_ENTRY_CONDITION,
    CATEGORY_EXIT_CONDITION,
    CATEGORY_AVOID_CONDITION,
    CATEGORY_RISK_CONDITION,
    CATEGORY_FACTOR_CANDIDATE,
    CATEGORY_RULE_CANDIDATE,
    CATEGORY_MARKET_REGIME_NOTE,
    CATEGORY_LONG_CYCLE_RISK,
    CATEGORY_POSITION_SIZING,
    POLARITY_BULLISH,
    POLARITY_BEARISH,
    POLARITY_NEUTRAL,
    POLARITY_RISK,
    POLARITY_AVOID,
    TIMEFRAME_UNIVERSAL,
    TIMEFRAME_CYCLE,
    TIMEFRAME_SHORT,
)

# ---------------------------------------------------------------------------
# Keyword pattern definitions
# ---------------------------------------------------------------------------

_ENTRY_KEYWORDS = [
    "財報", "EPS", "第一季", "去年同期", "全年", "乘以4",
    "底部翻多", "提前佈局", "提前卡位", "業績翻多", "績優翻多",
    "低位階", "基本面翻多",
]

_AVOID_TOP_PATTERN_KEYWORDS = [
    "M頭", "多重頂", "三重頂", "頭肩頂", "弧形頂",
    "單日反轉", "兩個高點沒過", "大盤創高但個股", "做頭", "頭部型態",
]

_AVOID_FUNDAMENTAL_KEYWORDS = [
    "題材", "營收跟不上", "財報衰退", "EPS不支撐",
    "炒題材", "純題材", "概念股沒業績",
]

_MARKET_REGIME_KEYWORDS = [
    "末升段", "多頭第三階段", "指數創高", "個股分化",
    "換股操作", "財報基優", "主流股", "權值股",
]

_LONG_CYCLE_RISK_KEYWORDS = [
    "股災", "50%", "2028", "2029", "2030", "2031",
    "長週期", "世代", "崩盤", "大跌",
]

_RISK_CONDITION_KEYWORDS = [
    "外資期貨空單", "權值股壓回", "指數修正", "主力出貨", "止損", "停損",
]

_POSITION_SIZING_KEYWORDS = [
    "不融資", "不單押", "4檔", "六到八檔", "6到8檔", "分散", "淨資產", "持股上限",
]

_FACTOR_CANDIDATE_KEYWORDS = [
    "EPS成長", "毛利率", "營收成長", "本益比", "殖利率",
    "股東權益報酬率", "ROE", "三率三升",
]

_LONG_CYCLE_CAVEAT = (
    "NOT a short-term sell signal. Long-cycle risk observation only. Not investment advice."
)

_EVIDENCE_CONTEXT = 50  # characters of context on each side of keyword match


def _extract_evidence(text: str, keyword: str) -> str:
    """Return the sentence / surrounding context where keyword appears."""
    idx = text.find(keyword)
    if idx == -1:
        return ""
    start = max(0, idx - _EVIDENCE_CONTEXT)
    end = min(len(text), idx + len(keyword) + _EVIDENCE_CONTEXT)
    return text[start:end].strip()


def _make_item(
    source,
    category: str,
    keyword: str,
    text: str,
    polarity: str = POLARITY_NEUTRAL,
    timeframe: str = TIMEFRAME_UNIVERSAL,
    caveats: str = "",
    suggested_rule_id: str = "",
    suggested_feature_name: str = "",
) -> StrategyKnowledgeItem:
    """Build a StrategyKnowledgeItem for a matched keyword."""
    source_id = getattr(source, "source_id", "UNKNOWN")
    evidence = _extract_evidence(text, keyword)
    return StrategyKnowledgeItem(
        source_id=source_id,
        category=category,
        title=f"Keyword match: {keyword}",
        statement=f"Keyword pattern matched: {keyword} in source {source_id}",
        normalized_statement=keyword.lower().strip(),
        evidence=evidence,
        confidence=MAX_TRANSCRIPT_CONFIDENCE,  # capped at PARTIAL
        polarity=polarity,
        timeframe=timeframe,
        caveats=caveats,
        suggested_rule_id=suggested_rule_id,
        suggested_feature_name=suggested_feature_name,
        auto_activated=False,  # ALWAYS False
        research_only=True,
        no_real_orders=True,
    )


def _deduplicate(items: list) -> list:
    """Remove items where (category, normalized_statement) is already seen."""
    seen: set = set()
    result: list = []
    for item in items:
        key = (item.category, item.normalized_statement)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


class StrategyKnowledgeExtractor:
    """
    Rule-based keyword extractor for strategy knowledge from transcript text.

    Safety invariants:
      read_only = True
      no_real_orders = True
      auto_activated = False  (ALWAYS)

    No external API calls. No LLM. No network requests. Pure keyword matching.
    """

    read_only: bool = True
    no_real_orders: bool = True
    auto_activated: bool = False

    def __init__(self, mode: str = "rule_based"):
        self.mode = mode

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def extract(self, source, text: str) -> list:
        """
        Extract all knowledge items from text using all sub-extractors.

        Parameters
        ----------
        source : TranscriptSource
        text   : raw transcript text

        Returns
        -------
        list of StrategyKnowledgeItem
        """
        if not text:
            return []

        all_items: list[StrategyKnowledgeItem] = []
        all_items.extend(self.extract_entry_conditions(text, source))
        all_items.extend(self.extract_exit_conditions(text, source))
        all_items.extend(self.extract_avoid_conditions(text, source))
        all_items.extend(self.extract_risk_conditions(text, source))
        all_items.extend(self.extract_market_regime_notes(text, source))
        all_items.extend(self.extract_long_cycle_risk(text, source))
        all_items.extend(self.extract_position_sizing_notes(text, source))
        all_items.extend(self.extract_factor_candidates(text, source))
        all_items.extend(self.extract_rule_candidates(text, source))

        return _deduplicate(all_items)

    # ------------------------------------------------------------------
    # Sub-extractors
    # ------------------------------------------------------------------

    def extract_entry_conditions(self, text: str, source) -> list:
        """Extract entry condition signals (bullish triggers)."""
        items: list[StrategyKnowledgeItem] = []
        for kw in _ENTRY_KEYWORDS:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_ENTRY_CONDITION,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_BULLISH,
                    timeframe=TIMEFRAME_SHORT,
                ))
        return items

    def extract_exit_conditions(self, text: str, source) -> list:
        """Extract exit / sell condition patterns."""
        exit_keywords = ["出場", "賣出", "出清", "減碼", "獲利了結", "停利"]
        items: list[StrategyKnowledgeItem] = []
        for kw in exit_keywords:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_EXIT_CONDITION,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_BEARISH,
                    timeframe=TIMEFRAME_SHORT,
                ))
        return items

    def extract_avoid_conditions(self, text: str, source) -> list:
        """Extract technical top patterns and fundamental avoid conditions."""
        items: list[StrategyKnowledgeItem] = []

        for kw in _AVOID_TOP_PATTERN_KEYWORDS:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_AVOID_CONDITION,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_AVOID,
                    timeframe=TIMEFRAME_SHORT,
                ))

        for kw in _AVOID_FUNDAMENTAL_KEYWORDS:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_AVOID_CONDITION,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_AVOID,
                    timeframe=TIMEFRAME_UNIVERSAL,
                ))

        return items

    def extract_risk_conditions(self, text: str, source) -> list:
        """Extract risk management and institutional signal patterns."""
        items: list[StrategyKnowledgeItem] = []
        for kw in _RISK_CONDITION_KEYWORDS:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_RISK_CONDITION,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_RISK,
                    timeframe=TIMEFRAME_SHORT,
                ))
        return items

    def extract_market_regime_notes(self, text: str, source) -> list:
        """Extract market regime / phase observation notes."""
        items: list[StrategyKnowledgeItem] = []
        for kw in _MARKET_REGIME_KEYWORDS:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_MARKET_REGIME_NOTE,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_NEUTRAL,
                    timeframe=TIMEFRAME_UNIVERSAL,
                ))
        return items

    def extract_long_cycle_risk(self, text: str, source) -> list:
        """
        Extract long-cycle crash / systemic risk observations.

        These are NOT short-term sell signals. Confidence capped at PARTIAL.
        auto_activated is ALWAYS False.
        """
        items: list[StrategyKnowledgeItem] = []
        for kw in _LONG_CYCLE_RISK_KEYWORDS:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_LONG_CYCLE_RISK,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_RISK,
                    timeframe=TIMEFRAME_CYCLE,
                    caveats=_LONG_CYCLE_CAVEAT,
                    suggested_rule_id="RISK.CYCLE.CRASH_WATCH.V1",
                ))
        return items

    def extract_position_sizing_notes(self, text: str, source) -> list:
        """Extract position sizing and portfolio discipline observations."""
        items: list[StrategyKnowledgeItem] = []
        for kw in _POSITION_SIZING_KEYWORDS:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_POSITION_SIZING,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_NEUTRAL,
                    timeframe=TIMEFRAME_UNIVERSAL,
                ))
        return items

    def extract_factor_candidates(self, text: str, source) -> list:
        """Extract quantitative factor / feature candidates."""
        items: list[StrategyKnowledgeItem] = []
        for kw in _FACTOR_CANDIDATE_KEYWORDS:
            if kw in text:
                # Suggest a feature name: lowercase, replace spaces with underscores
                feat_name = kw.lower().replace(" ", "_").replace("/", "_")
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_FACTOR_CANDIDATE,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_NEUTRAL,
                    timeframe=TIMEFRAME_UNIVERSAL,
                    suggested_feature_name=f"feat_{feat_name}",
                ))
        return items

    def extract_rule_candidates(self, text: str, source) -> list:
        """
        Extract general rule candidate patterns not covered by more specific
        sub-extractors.
        """
        rule_keywords = [
            "阪田戰法", "卡位", "轉折", "突破", "換手", "量縮", "量增", "波段",
            "強勢股", "弱勢股", "支撐", "壓力", "缺口", "跳空",
        ]
        items: list[StrategyKnowledgeItem] = []
        for kw in rule_keywords:
            if kw in text:
                items.append(_make_item(
                    source=source,
                    category=CATEGORY_RULE_CANDIDATE,
                    keyword=kw,
                    text=text,
                    polarity=POLARITY_NEUTRAL,
                    timeframe=TIMEFRAME_UNIVERSAL,
                ))
        return items
