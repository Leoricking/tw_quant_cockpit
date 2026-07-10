"""
paper_trading/small_capital_strategy/mistake_taxonomy_classifier_v176.py
Mistake classification logic for v1.7.6.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import List, Optional

from paper_trading.small_capital_strategy.mistake_taxonomy_enums_v176 import (
    MistakeCategory, MistakeSeverity, BehaviorRiskLevel,
    CATEGORY_SEVERITY, get_category_severity, get_severity_weight,
)
from paper_trading.small_capital_strategy.mistake_taxonomy_models_v176 import (
    MistakeEvent, MistakeTaxonomyRule, ImprovementAction,
)

_SCHEMA  = "176"
_POLICY  = "1.7.6-mistake-taxonomy-weekly-review"

# Corrective actions per category
_CORRECTIVE_ACTIONS: dict = {
    MistakeCategory.FOMO_CHASE:                  "Wait for confirmed entry signal; do not chase price.",
    MistakeCategory.EARLY_ENTRY:                 "Wait for pattern completion before entering.",
    MistakeCategory.LATE_ENTRY:                  "Skip extended entries; wait for next pullback.",
    MistakeCategory.NO_STOP_LOSS:                "Always set a stop loss before entering a trade.",
    MistakeCategory.MOVED_STOP_LOSS:             "Never widen a stop loss after entry.",
    MistakeCategory.OVERSIZED_POSITION:          "Reduce position size to max 30% of capital.",
    MistakeCategory.OVERTRADING:                 "Limit to 1-2 trades per week; quality over quantity.",
    MistakeCategory.IGNORE_MARKET_REGIME:        "Only trade in BULL or RANGE regimes; sit out BEAR/RISK_OFF.",
    MistakeCategory.IGNORE_WATCHLIST_RANK:       "Only trade watchlist Tier-1 or Tier-2 candidates.",
    MistakeCategory.IGNORE_ABC_PLAN:             "Follow ABC buy point plan; no off-plan entries.",
    MistakeCategory.TAKE_PROFIT_TOO_EARLY:       "Hold to target pivot; review exit plan before trading.",
    MistakeCategory.HOLD_LOSER_TOO_LONG:         "Honor stop loss; cut loss at predefined level.",
    MistakeCategory.REVENGE_TRADE:               "Wait 24h after a loss before next trade.",
    MistakeCategory.NEWS_CHASE:                  "Ignore news catalysts; trade only technical setups.",
    MistakeCategory.EARNINGS_RISK_IGNORED:       "Avoid holding through earnings; close before report.",
    MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT:  "[BLOCKED] No margin or leverage. Paper only.",
    MistakeCategory.BROKER_OR_REAL_ORDER_ATTEMPT: "[BLOCKED] No real broker orders. Paper only.",
    MistakeCategory.UNKNOWN:                     "Classify mistake category and document corrective action.",
}

_RULES: List[MistakeTaxonomyRule] = [
    MistakeTaxonomyRule(
        rule_id="R176-001", category=MistakeCategory.NO_STOP_LOSS,
        severity=MistakeSeverity.HIGH,
        description="Trade entered without a stop loss.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.NO_STOP_LOSS],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-002", category=MistakeCategory.OVERSIZED_POSITION,
        severity=MistakeSeverity.HIGH,
        description="Position size exceeds 30% of capital.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.OVERSIZED_POSITION],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-003", category=MistakeCategory.IGNORE_MARKET_REGIME,
        severity=MistakeSeverity.CRITICAL,
        description="Trade entered in BEAR or RISK_OFF market regime.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.IGNORE_MARKET_REGIME],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-004", category=MistakeCategory.REVENGE_TRADE,
        severity=MistakeSeverity.CRITICAL,
        description="Trade entered immediately after a loss to recover.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.REVENGE_TRADE],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-005", category=MistakeCategory.FOMO_CHASE,
        severity=MistakeSeverity.MEDIUM,
        description="Trade entered on price momentum without a confirmed setup.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.FOMO_CHASE],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-006", category=MistakeCategory.MOVED_STOP_LOSS,
        severity=MistakeSeverity.HIGH,
        description="Stop loss was widened after entry.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.MOVED_STOP_LOSS],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-007", category=MistakeCategory.HOLD_LOSER_TOO_LONG,
        severity=MistakeSeverity.HIGH,
        description="Loss exceeded stop loss level without closing.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.HOLD_LOSER_TOO_LONG],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-008", category=MistakeCategory.IGNORE_ABC_PLAN,
        severity=MistakeSeverity.HIGH,
        description="Entry did not follow the A/B/C buy point plan.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.IGNORE_ABC_PLAN],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-009", category=MistakeCategory.IGNORE_WATCHLIST_RANK,
        severity=MistakeSeverity.MEDIUM,
        description="Trade on a symbol not in Tier-1 or Tier-2 watchlist.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.IGNORE_WATCHLIST_RANK],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-010", category=MistakeCategory.OVERTRADING,
        severity=MistakeSeverity.MEDIUM,
        description="More than 2 trades in the same week.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.OVERTRADING],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-011", category=MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT,
        severity=MistakeSeverity.BLOCKING,
        description="Attempt to use margin or leverage.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.MARGIN_OR_LEVERAGE_ATTEMPT],
    ),
    MistakeTaxonomyRule(
        rule_id="R176-012", category=MistakeCategory.BROKER_OR_REAL_ORDER_ATTEMPT,
        severity=MistakeSeverity.BLOCKING,
        description="Attempt to place a real broker order.",
        corrective_action=_CORRECTIVE_ACTIONS[MistakeCategory.BROKER_OR_REAL_ORDER_ATTEMPT],
    ),
]


def get_all_rules() -> List[MistakeTaxonomyRule]:
    """Return all taxonomy rules."""
    return list(_RULES)


def get_rule_by_category(category: MistakeCategory) -> Optional[MistakeTaxonomyRule]:
    """Return the rule for a given category, or None."""
    for r in _RULES:
        if r.category == category:
            return r
    return None


def classify_event(
    symbol: str,
    trade_date: str,
    category: MistakeCategory,
    cost_twd: float = 0.0,
    week_label: str = "",
    month_label: str = "",
    event_id: str = "",
) -> MistakeEvent:
    """Create a MistakeEvent from classification inputs."""
    severity = get_category_severity(category)
    rule = get_rule_by_category(category)
    description = rule.description if rule else ""
    return MistakeEvent(
        event_id=event_id or f"EVT-{trade_date}-{category.value}",
        symbol=symbol,
        trade_date=trade_date,
        category=category,
        severity=severity,
        cost_twd=cost_twd,
        description=description,
        week_label=week_label,
        month_label=month_label,
    )


def get_corrective_action(category: MistakeCategory) -> str:
    """Return corrective action string for a category."""
    return _CORRECTIVE_ACTIONS.get(category, "")


def build_improvement_action(
    category: MistakeCategory,
    priority: int = 3,
    deadline: str = "",
    action_id: str = "",
) -> ImprovementAction:
    """Build an ImprovementAction for a given category."""
    rule = get_rule_by_category(category)
    return ImprovementAction(
        action_id=action_id or f"ACT-{category.value}",
        category=category,
        priority=priority,
        description=_CORRECTIVE_ACTIONS.get(category, ""),
        rationale=rule.description if rule else "",
        deadline=deadline,
    )
