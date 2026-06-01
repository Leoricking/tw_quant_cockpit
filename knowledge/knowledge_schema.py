"""
knowledge/knowledge_schema.py — StrategyKnowledgeItem schema (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] auto_activated is ALWAYS False. Confidence capped at PARTIAL for transcript-only sources.
"""
from __future__ import annotations

import random
import string
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar

# ---------------------------------------------------------------------------
# Confidence levels
# ---------------------------------------------------------------------------

CONFIDENCE_LEVELS = ["LOW", "WEAK", "PARTIAL", "GOOD", "HIGH"]
MAX_TRANSCRIPT_CONFIDENCE = "PARTIAL"

# ---------------------------------------------------------------------------
# Category and polarity constants
# ---------------------------------------------------------------------------

CATEGORY_ENTRY_CONDITION = "entry_condition"
CATEGORY_EXIT_CONDITION = "exit_condition"
CATEGORY_AVOID_CONDITION = "avoid_condition"
CATEGORY_RISK_CONDITION = "risk_condition"
CATEGORY_FACTOR_CANDIDATE = "factor_candidate"
CATEGORY_RULE_CANDIDATE = "rule_candidate"
CATEGORY_MARKET_REGIME_NOTE = "market_regime_note"
CATEGORY_LONG_CYCLE_RISK = "long_cycle_risk"
CATEGORY_POSITION_SIZING = "position_sizing"
CATEGORY_PORTFOLIO_DISCIPLINE = "portfolio_discipline"
CATEGORY_TRANSCRIPT_SUMMARY = "transcript_summary"

VALID_CATEGORIES = [
    CATEGORY_ENTRY_CONDITION,
    CATEGORY_EXIT_CONDITION,
    CATEGORY_AVOID_CONDITION,
    CATEGORY_RISK_CONDITION,
    CATEGORY_FACTOR_CANDIDATE,
    CATEGORY_RULE_CANDIDATE,
    CATEGORY_MARKET_REGIME_NOTE,
    CATEGORY_LONG_CYCLE_RISK,
    CATEGORY_POSITION_SIZING,
    CATEGORY_PORTFOLIO_DISCIPLINE,
    CATEGORY_TRANSCRIPT_SUMMARY,
]

POLARITY_BULLISH = "bullish"
POLARITY_BEARISH = "bearish"
POLARITY_NEUTRAL = "neutral"
POLARITY_RISK = "risk"
POLARITY_AVOID = "avoid"

VALID_POLARITIES = [POLARITY_BULLISH, POLARITY_BEARISH, POLARITY_NEUTRAL, POLARITY_RISK, POLARITY_AVOID]

TIMEFRAME_INTRADAY = "intraday"
TIMEFRAME_SHORT = "short"
TIMEFRAME_MEDIUM = "medium"
TIMEFRAME_LONG = "long"
TIMEFRAME_CYCLE = "cycle"
TIMEFRAME_UNIVERSAL = "universal"

VALID_TIMEFRAMES = [
    TIMEFRAME_INTRADAY,
    TIMEFRAME_SHORT,
    TIMEFRAME_MEDIUM,
    TIMEFRAME_LONG,
    TIMEFRAME_CYCLE,
    TIMEFRAME_UNIVERSAL,
]


# ---------------------------------------------------------------------------
# Helper function
# ---------------------------------------------------------------------------

def confidence_cap_for_transcript_source(confidence: str) -> str:
    """
    Return the capped confidence for a transcript-only knowledge item.
    Transcript sources must never exceed PARTIAL confidence.
    HIGH and GOOD are reduced to PARTIAL.
    """
    try:
        idx = CONFIDENCE_LEVELS.index(confidence)
        cap_idx = CONFIDENCE_LEVELS.index(MAX_TRANSCRIPT_CONFIDENCE)
        return CONFIDENCE_LEVELS[min(idx, cap_idx)]
    except ValueError:
        return MAX_TRANSCRIPT_CONFIDENCE


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class StrategyKnowledgeItem:
    """
    A single extracted strategy knowledge item from a transcript or document.

    Safety invariants:
      research_only = True
      no_real_orders = True
      auto_activated = False  (ALWAYS)
    """

    # Class-level safety flags
    _cls_research_only: ClassVar[bool] = True
    _cls_no_real_orders: ClassVar[bool] = True
    _cls_auto_activated: ClassVar[bool] = False

    knowledge_id: str = field(default_factory=lambda: StrategyKnowledgeItem._generate_knowledge_id())
    source_id: str = ""
    category: str = CATEGORY_TRANSCRIPT_SUMMARY
    title: str = ""
    statement: str = ""
    normalized_statement: str = ""
    evidence: str = ""
    confidence: str = "LOW"
    polarity: str = "neutral"
    timeframe: str = "universal"
    applies_to: str = ""
    required_data: str = ""
    suggested_rule_id: str = ""
    suggested_feature_name: str = ""
    tags: str = ""           # comma-separated
    caveats: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    research_only: bool = True
    no_real_orders: bool = True
    auto_activated: bool = False

    def __post_init__(self):
        # Enforce safety invariants — these must never be overridden
        self.research_only = True
        self.no_real_orders = True
        self.auto_activated = False  # ALWAYS False

        # Cap confidence at PARTIAL for all knowledge items
        self.confidence = confidence_cap_for_transcript_source(self.confidence)

        # Validate category
        if self.category not in VALID_CATEGORIES:
            self.category = CATEGORY_TRANSCRIPT_SUMMARY

        # Validate polarity
        if self.polarity not in VALID_POLARITIES:
            self.polarity = POLARITY_NEUTRAL

        # Validate timeframe
        if self.timeframe not in VALID_TIMEFRAMES:
            self.timeframe = TIMEFRAME_UNIVERSAL

    def to_dict(self) -> dict:
        """Return all fields as a plain dictionary."""
        return {
            "knowledge_id": self.knowledge_id,
            "source_id": self.source_id,
            "category": self.category,
            "title": self.title,
            "statement": self.statement,
            "normalized_statement": self.normalized_statement,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "polarity": self.polarity,
            "timeframe": self.timeframe,
            "applies_to": self.applies_to,
            "required_data": self.required_data,
            "suggested_rule_id": self.suggested_rule_id,
            "suggested_feature_name": self.suggested_feature_name,
            "tags": self.tags,
            "caveats": self.caveats,
            "created_at": self.created_at,
            "research_only": self.research_only,
            "no_real_orders": self.no_real_orders,
            "auto_activated": self.auto_activated,
        }

    @staticmethod
    def _generate_knowledge_id() -> str:
        """Return KNW-YYYYMMDD-HHMMSS-XXXXXX format unique ID."""
        now = datetime.now()
        date_part = now.strftime("%Y%m%d")
        time_part = now.strftime("%H%M%S")
        rand_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"KNW-{date_part}-{time_part}-{rand_part}"

    def __repr__(self) -> str:
        return (
            f"StrategyKnowledgeItem(knowledge_id={self.knowledge_id!r}, "
            f"category={self.category!r}, confidence={self.confidence!r}, "
            f"auto_activated={self.auto_activated})"
        )
