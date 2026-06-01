"""
knowledge/rule_candidate_mapper.py — RuleCandidateMapper: maps knowledge items to governance rules (v0.4.1.1).
[!] Knowledge Only. Research Only. No Real Orders. Production Trading: BLOCKED.
[!] auto_activated is ALWAYS False. All candidates require review.
"""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

from knowledge.knowledge_schema import (
    StrategyKnowledgeItem,
    CATEGORY_ENTRY_CONDITION,
    CATEGORY_AVOID_CONDITION,
    CATEGORY_RISK_CONDITION,
    CATEGORY_RULE_CANDIDATE,
    CATEGORY_LONG_CYCLE_RISK,
    CATEGORY_POSITION_SIZING,
)

# ---------------------------------------------------------------------------
# Governance status constants
# ---------------------------------------------------------------------------

GOVERNANCE_MAPPED = "MAPPED_TO_EXISTING"
GOVERNANCE_CANDIDATE = "CANDIDATE"

# ---------------------------------------------------------------------------
# Categories eligible for rule candidate mapping
# ---------------------------------------------------------------------------

_MAPPABLE_CATEGORIES = {
    CATEGORY_ENTRY_CONDITION,
    CATEGORY_AVOID_CONDITION,
    CATEGORY_RISK_CONDITION,
    CATEGORY_RULE_CANDIDATE,
    CATEGORY_LONG_CYCLE_RISK,
    CATEGORY_POSITION_SIZING,
}

# ---------------------------------------------------------------------------
# Rule mapping table
# ---------------------------------------------------------------------------

RULE_MAPPING: dict[str, dict] = {
    "財報底部翻多": {
        "suggested_rule_id": "BUY.SHORT.SECOND_WAVE.V1",
        "existing_rule_match": "BUY.SHORT.SECOND_WAVE.V1",
    },
    "EPS優於去年": {
        "suggested_rule_id": "LONG.FUNDAMENTAL.EPS_POSITIVE.V1",
        "existing_rule_match": "SCREEN.UNIVERSAL.REVENUE_GROWTH.V1",
    },
    "底部翻多": {
        "suggested_rule_id": "BUY.SHORT.SECOND_WAVE.V1",
        "existing_rule_match": "BUY.SHORT.SECOND_WAVE.V1",
    },
    "M頭": {
        "suggested_rule_id": "RISK.TECHNICAL.TOP_PATTERN.V1",
        "existing_rule_match": "",
    },
    "頭肩頂": {
        "suggested_rule_id": "RISK.TECHNICAL.TOP_PATTERN.V1",
        "existing_rule_match": "",
    },
    "多重頂": {
        "suggested_rule_id": "RISK.TECHNICAL.TOP_PATTERN.V1",
        "existing_rule_match": "",
    },
    "大盤創高但個股不創高": {
        "suggested_rule_id": "RISK.RELATIVE_WEAKNESS.MARKET_NEW_HIGH_STOCK_LAG.V1",
        "existing_rule_match": "",
    },
    "假突破": {
        "suggested_rule_id": "INTRADAY.BREAKOUT.FAKE_BREAKOUT_RISK.V1",
        "existing_rule_match": "",
    },
    "股災": {
        "suggested_rule_id": "RISK.CYCLE.CRASH_WATCH.V1",
        "existing_rule_match": "",
    },
    "2028": {
        "suggested_rule_id": "RISK.CYCLE.CRASH_WATCH.V1",
        "existing_rule_match": "",
    },
    "長週期": {
        "suggested_rule_id": "RISK.CYCLE.CRASH_WATCH.V1",
        "existing_rule_match": "",
    },
    "題材無業績": {
        "suggested_rule_id": "RISK.FUNDAMENTAL.REVENUE_NOT_SUPPORTING_THEME.V1",
        "existing_rule_match": "",
    },
    "不融資": {
        "suggested_rule_id": "RISK.PORTFOLIO.MARGIN_USAGE.V1",
        "existing_rule_match": "",
    },
    "不單押": {
        "suggested_rule_id": "RISK.PORTFOLIO.OVER_CONCENTRATION.V1",
        "existing_rule_match": "",
    },
}


class RuleCandidateMapper:
    """
    Maps StrategyKnowledgeItems to governance rule candidates.

    Safety invariants:
      auto_activated = False  (ALWAYS — never auto-activates any rule)
      needs_review = True     (all candidates require human review)
    """

    read_only: bool = True
    no_real_orders: bool = True
    auto_activated: bool = False

    def __init__(self, registry=None):
        self._registry = registry  # optional RuleRegistry reference (not required)

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def map_item(self, item: StrategyKnowledgeItem) -> dict:
        """
        Map a single StrategyKnowledgeItem to a rule candidate dict.

        Returns dict with keys:
          knowledge_id, source_id, category, statement, confidence,
          suggested_rule_id, existing_rule_match, governance_status,
          auto_activated, needs_review
        """
        # Try to find a matching entry in RULE_MAPPING via normalized_statement
        # or by checking if any rule_mapping key appears in the statement/title
        suggested_rule_id = item.suggested_rule_id or ""
        existing_rule_match = ""

        # Search rule mapping table for keyword matches
        stmt_check = (item.normalized_statement + " " + item.statement + " " + item.title).lower()
        for kw, mapping in RULE_MAPPING.items():
            if kw.lower() in stmt_check:
                suggested_rule_id = mapping["suggested_rule_id"]
                existing_rule_match = mapping["existing_rule_match"]
                break

        # If item already has a suggested_rule_id set and no mapping found, keep it
        if not suggested_rule_id and item.suggested_rule_id:
            suggested_rule_id = item.suggested_rule_id

        governance_status = GOVERNANCE_MAPPED if existing_rule_match else GOVERNANCE_CANDIDATE

        return {
            "knowledge_id": item.knowledge_id,
            "source_id": item.source_id,
            "category": item.category,
            "statement": item.statement,
            "confidence": item.confidence,
            "polarity": item.polarity,
            "suggested_rule_id": suggested_rule_id,
            "existing_rule_match": existing_rule_match,
            "governance_status": governance_status,
            "auto_activated": False,   # ALWAYS False
            "needs_review": True,      # all candidates need review
            "caveats": item.caveats,
            "research_only": True,
            "no_real_orders": True,
        }

    def map_items(self, items: list) -> list:
        """
        Map a list of StrategyKnowledgeItems to rule candidate dicts.

        Only maps items in eligible categories:
          entry_condition, avoid_condition, risk_condition, rule_candidate,
          long_cycle_risk, position_sizing

        Returns list of rule candidate dicts.
        """
        candidates: list[dict] = []
        for item in items:
            if item.category in _MAPPABLE_CATEGORIES:
                candidate = self.map_item(item)
                candidates.append(candidate)
        return candidates
