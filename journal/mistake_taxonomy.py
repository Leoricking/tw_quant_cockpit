"""
journal/mistake_taxonomy.py — MistakeTaxonomy (v0.4.6).

Mistake tag classification and explanation for research learning.
Does NOT produce trading actions. Research / review only.

[!] Journal Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

from typing import Dict, List

from journal.journal_schema import (
    ALL_MISTAKE_TAGS,
    MISTAKE_CHASE_HIGH, MISTAKE_IGNORED_STOP, MISTAKE_OVERSIZED_POSITION,
    MISTAKE_BOUGHT_WEAK_STOCK, MISTAKE_IGNORED_DATA_QUALITY,
    MISTAKE_IGNORED_PROVIDER_WARNING, MISTAKE_IGNORED_FAKE_BREAKOUT,
    MISTAKE_IGNORED_VWAP_LOSS, MISTAKE_IGNORED_TOP_PATTERN,
    MISTAKE_IGNORED_FUNDAMENTAL_DETERIORATION, MISTAKE_NO_PLAN,
    MISTAKE_EMOTIONAL_TRADE, MISTAKE_OVERTRADING,
)

# ---------------------------------------------------------------------------
# Mistake categories
# ---------------------------------------------------------------------------
CAT_ENTRY_MISTAKE     = "entry_mistake"
CAT_EXIT_MISTAKE      = "exit_mistake"
CAT_SIZING_MISTAKE    = "sizing_mistake"
CAT_RISK_MISTAKE      = "risk_mistake"
CAT_DATA_MISTAKE      = "data_mistake"
CAT_PROCESS_MISTAKE   = "process_mistake"
CAT_EMOTIONAL_MISTAKE = "emotional_mistake"
CAT_SYSTEM_MISTAKE    = "system_mistake"

ALL_CATEGORIES = [
    CAT_ENTRY_MISTAKE, CAT_EXIT_MISTAKE, CAT_SIZING_MISTAKE, CAT_RISK_MISTAKE,
    CAT_DATA_MISTAKE, CAT_PROCESS_MISTAKE, CAT_EMOTIONAL_MISTAKE, CAT_SYSTEM_MISTAKE,
]

# ---------------------------------------------------------------------------
# Taxonomy definitions
# ---------------------------------------------------------------------------
_TAXONOMY: Dict[str, dict] = {
    MISTAKE_CHASE_HIGH: {
        "category": CAT_ENTRY_MISTAKE,
        "severity": "HIGH",
        "explanation": (
            "Bought after a significant move up, chasing price away from the base or "
            "breakout point. Entry had poor risk/reward."
        ),
        "suggested_fix": (
            "Wait for a pullback to key support (VWAP, 20MA, opening range high). "
            "Define max acceptable chase distance before entry."
        ),
    },
    MISTAKE_IGNORED_STOP: {
        "category": CAT_EXIT_MISTAKE,
        "severity": "CRITICAL",
        "explanation": (
            "Did not close the simulated position when the planned stop-loss level was hit. "
            "Let the loss run beyond the original plan."
        ),
        "suggested_fix": (
            "Define stop-loss before entry. Treat stop as a hard rule, not a guideline. "
            "Use invalidation condition: what needs to be true for the thesis to be wrong?"
        ),
    },
    MISTAKE_OVERSIZED_POSITION: {
        "category": CAT_SIZING_MISTAKE,
        "severity": "HIGH",
        "explanation": (
            "Position size was too large relative to the portfolio or risk budget. "
            "Single position risk exceeded plan."
        ),
        "suggested_fix": (
            "Define position_size_pct limit before entry. Max single-name risk = 1-2% of portfolio. "
            "Scale down near key resistance levels."
        ),
    },
    MISTAKE_BOUGHT_WEAK_STOCK: {
        "category": CAT_ENTRY_MISTAKE,
        "severity": "MEDIUM",
        "explanation": (
            "Entered a stock showing relative weakness (underperforming sector, "
            "below VWAP while sector is above, deteriorating fundamentals)."
        ),
        "suggested_fix": (
            "Apply relative strength filter before entry. Prefer stocks outperforming "
            "their sector on up days."
        ),
    },
    MISTAKE_IGNORED_DATA_QUALITY: {
        "category": CAT_DATA_MISTAKE,
        "severity": "HIGH",
        "explanation": (
            "Made a decision while data quality was flagged as WARN or BLOCK. "
            "Ignored data quality gate alerts."
        ),
        "suggested_fix": (
            "Check data_quality_gate before any research decision. "
            "If DQ gate is BLOCKED, postpone signal review until data is clean."
        ),
    },
    MISTAKE_IGNORED_PROVIDER_WARNING: {
        "category": CAT_DATA_MISTAKE,
        "severity": "MEDIUM",
        "explanation": (
            "Proceeded with analysis while provider health was flagged as degraded "
            "or a provider failure notification was active."
        ),
        "suggested_fix": (
            "Check notification center before signal review. "
            "Provider failures may affect data completeness."
        ),
    },
    MISTAKE_IGNORED_FAKE_BREAKOUT: {
        "category": CAT_ENTRY_MISTAKE,
        "severity": "HIGH",
        "explanation": (
            "Entered on a breakout that quickly reversed (fake breakout). "
            "Volume / breadth / pattern confirmation was absent."
        ),
        "suggested_fix": (
            "Require volume expansion on breakout day. "
            "Check if broad market / sector is supportive. "
            "Use opening range high/low as breakout filter."
        ),
    },
    MISTAKE_IGNORED_VWAP_LOSS: {
        "category": CAT_EXIT_MISTAKE,
        "severity": "HIGH",
        "explanation": (
            "Held a long position while price was trading and closing below VWAP. "
            "VWAP loss is a short-term distribution signal."
        ),
        "suggested_fix": (
            "Use intraday VWAP as a trailing exit guide. "
            "Consider reducing or exiting long positions that close below VWAP for N consecutive intervals."
        ),
    },
    MISTAKE_IGNORED_TOP_PATTERN: {
        "category": CAT_ENTRY_MISTAKE,
        "severity": "MEDIUM",
        "explanation": (
            "Entered long while a distribution / topping pattern was forming "
            "(M-top, head-and-shoulders, volume divergence on new highs)."
        ),
        "suggested_fix": (
            "Check volume profile for distribution signs. "
            "Avoid initiating new longs at all-time highs with declining volume."
        ),
    },
    MISTAKE_IGNORED_FUNDAMENTAL_DETERIORATION: {
        "category": CAT_ENTRY_MISTAKE,
        "severity": "MEDIUM",
        "explanation": (
            "Initiated or held a position despite flagged fundamental deterioration "
            "(declining earnings trend, revenue miss, debt increase)."
        ),
        "suggested_fix": (
            "Review fundamental screening flags before entry. "
            "Avoid long entries when strategy knowledge flags fundamental concerns."
        ),
    },
    MISTAKE_NO_PLAN: {
        "category": CAT_PROCESS_MISTAKE,
        "severity": "HIGH",
        "explanation": (
            "Entered without a documented thesis, planned entry price, stop-loss, "
            "or invalidation condition. No plan means no way to evaluate quality."
        ),
        "suggested_fix": (
            "Use journal entry form before every simulated trade. "
            "Required fields: thesis, planned_entry, planned_stop, invalidation_condition."
        ),
    },
    MISTAKE_EMOTIONAL_TRADE: {
        "category": CAT_EMOTIONAL_MISTAKE,
        "severity": "HIGH",
        "explanation": (
            "Trade was driven by FOMO, frustration after a loss, or euphoria after a win — "
            "not by the written system rules."
        ),
        "suggested_fix": (
            "Implement a mandatory cooling-off period after losses. "
            "Require thesis documentation before each entry. "
            "Review emotional state in post-trade review notes."
        ),
    },
    MISTAKE_OVERTRADING: {
        "category": CAT_PROCESS_MISTAKE,
        "severity": "MEDIUM",
        "explanation": (
            "Excessive number of entries in a session. "
            "High turnover reduces average quality per trade."
        ),
        "suggested_fix": (
            "Set daily / weekly maximum entry count. "
            "Focus on highest-conviction setups only."
        ),
    },
}


class MistakeTaxonomy:
    """
    Mistake tag classification and explanation.
    Research / review learning tool only — does NOT produce trading actions.

    [!] Journal Only. Research Only. No Real Orders.
    """

    read_only: bool          = True
    no_real_orders: bool     = True
    production_blocked: bool = True

    def list_tags(self) -> List[str]:
        """Return all known mistake tag strings."""
        return list(ALL_MISTAKE_TAGS)

    def list_categories(self) -> List[str]:
        """Return all mistake categories."""
        return list(ALL_CATEGORIES)

    def tags_by_category(self, category: str) -> List[str]:
        """Return all tags belonging to a given category."""
        return [
            tag for tag, info in _TAXONOMY.items()
            if info.get("category") == category
        ]

    def explain_tag(self, tag: str) -> str:
        """Return explanation text for a tag."""
        info = _TAXONOMY.get(tag)
        if not info:
            return f"Unknown tag: {tag}"
        return info.get("explanation", "")

    def severity(self, tag: str) -> str:
        """Return severity level for a tag: CRITICAL / HIGH / MEDIUM / LOW."""
        info = _TAXONOMY.get(tag)
        if not info:
            return "UNKNOWN"
        return info.get("severity", "MEDIUM")

    def suggested_fix(self, tag: str) -> str:
        """Return suggested fix for a tag."""
        info = _TAXONOMY.get(tag)
        if not info:
            return ""
        return info.get("suggested_fix", "")

    def category(self, tag: str) -> str:
        """Return category for a tag."""
        info = _TAXONOMY.get(tag)
        if not info:
            return ""
        return info.get("category", "")

    def get_full_info(self, tag: str) -> dict:
        """Return full taxonomy info dict for a tag."""
        info = _TAXONOMY.get(tag, {})
        return {
            "tag":           tag,
            "category":      info.get("category", ""),
            "severity":      info.get("severity", ""),
            "explanation":   info.get("explanation", ""),
            "suggested_fix": info.get("suggested_fix", ""),
        }

    def summarize_mistake_list(self, tags: List[str]) -> List[dict]:
        """Return full info for each tag in a list."""
        return [self.get_full_info(t) for t in tags if t in _TAXONOMY]
