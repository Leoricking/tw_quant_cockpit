"""
paper_trading/small_capital_strategy/integrated_strategy_engine_v178.py
Core orchestration engine for Small Capital Strategy Integration v1.7.8.
Connects v1.7.0–v1.7.7 subsystems into a single decision pipeline.
[!] Research Only. Paper Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
from typing import Optional

from paper_trading.small_capital_strategy.integrated_strategy_enums_v178 import (
    IntegratedDecisionAction,
    IntegratedRegimeStatus,
    IntegratedWatchlistStatus,
    IntegratedABCStatus,
    IntegratedThemeStatus,
    IntegratedRiskLevel,
    IntegratedBehaviorStatus,
)
from paper_trading.small_capital_strategy.integrated_strategy_models_v178 import (
    IntegratedStrategyInput,
    IntegratedStrategyContext,
    IntegratedStrategyDecision,
    IntegratedWatchlistDecision,
    IntegratedThemeDecision,
    IntegratedABCDecision,
    IntegratedRiskDecision,
    IntegratedBehaviorDecision,
    IntegratedScorecard,
    IntegratedDashboard,
)
from paper_trading.small_capital_strategy.integrated_strategy_scorecard_v178 import (
    compute_scorecard,
)
from paper_trading.small_capital_strategy.integrated_strategy_decisions_v178 import (
    check_hard_blocks,
    collect_no_trade_reasons,
    determine_action,
    build_decision_summary,
)

_SCHEMA  = "178"
_POLICY  = "1.7.8-small-capital-strategy-integration"
_LINEAGE = "paper_trading.small_capital_strategy.integrated_strategy_engine_v178"


class IntegratedStrategyEngine:
    """
    Orchestration engine for v1.7.8 integrated strategy.
    Combines all subsystem signals into a single auditable decision.
    Paper/research only — no real orders, no broker.
    """

    def __init__(self) -> None:
        self._paper_only = True
        self._no_real_orders = True
        self._no_broker = True

    def build_context(self, inp: IntegratedStrategyInput) -> IntegratedStrategyContext:
        """Build context from input, checking subsystem availability."""
        blocks = check_hard_blocks(inp)
        return IntegratedStrategyContext(
            symbol=inp.symbol,
            date=inp.date,
            all_subsystems_present=bool(inp.symbol and inp.date),
            has_hard_blocks=bool(blocks),
            block_reasons=blocks,
            regime_allows_trade=inp.regime_status not in (
                IntegratedRegimeStatus.RISK_OFF, IntegratedRegimeStatus.BEAR
            ),
            watchlist_allows_trade=inp.watchlist_status in (
                IntegratedWatchlistStatus.FOCUS, IntegratedWatchlistStatus.WATCH
            ),
            abc_allows_trade=inp.abc_status in (
                IntegratedABCStatus.A_READY, IntegratedABCStatus.B_READY, IntegratedABCStatus.C_READY
            ),
            risk_allows_trade=inp.risk_level in (
                IntegratedRiskLevel.SAFE, IntegratedRiskLevel.MODERATE
            ),
            behavior_allows_trade=inp.behavior_status in (
                IntegratedBehaviorStatus.CLEAN, IntegratedBehaviorStatus.CAUTION
            ),
            theme_allows_trade=inp.theme_status in (
                IntegratedThemeStatus.LEADER, IntegratedThemeStatus.STRONG, IntegratedThemeStatus.WATCH
            ),
            journal_complete=inp.journal_quality_score >= 50.0,
        )

    def build_sub_decisions(self, inp: IntegratedStrategyInput) -> dict:
        """Build individual sub-decisions for each subsystem."""
        wl = IntegratedWatchlistDecision(
            symbol=inp.symbol,
            status=inp.watchlist_status,
            watchlist_score=inp.watchlist_score,
            allows_trade=inp.watchlist_status in (
                IntegratedWatchlistStatus.FOCUS, IntegratedWatchlistStatus.WATCH
            ),
            reason=inp.watchlist_status.value,
        )
        th = IntegratedThemeDecision(
            top_theme=inp.top_theme,
            theme_status=inp.theme_status,
            theme_score=inp.theme_score,
            allows_trade=inp.theme_status in (
                IntegratedThemeStatus.LEADER, IntegratedThemeStatus.STRONG, IntegratedThemeStatus.WATCH
            ),
            reason=inp.theme_status.value,
        )
        abc = IntegratedABCDecision(
            symbol=inp.symbol,
            abc_status=inp.abc_status,
            abc_score=inp.abc_score,
            buy_point_type=inp.abc_status.value,
            allows_trade=inp.abc_status in (
                IntegratedABCStatus.A_READY, IntegratedABCStatus.B_READY, IntegratedABCStatus.C_READY
            ),
            reason=inp.abc_status.value,
        )
        risk = IntegratedRiskDecision(
            risk_level=inp.risk_level,
            risk_score=inp.risk_score,
            allows_trade=inp.risk_level in (
                IntegratedRiskLevel.SAFE, IntegratedRiskLevel.MODERATE
            ),
            reason=inp.risk_level.value,
        )
        beh = IntegratedBehaviorDecision(
            behavior_status=inp.behavior_status,
            behavior_score=inp.behavior_score,
            mistake_repeat_detected=inp.mistake_repeat_detected,
            allows_trade=inp.behavior_status in (
                IntegratedBehaviorStatus.CLEAN, IntegratedBehaviorStatus.CAUTION
            ),
            reason=inp.behavior_status.value,
        )
        return {
            "watchlist": wl,
            "theme": th,
            "abc": abc,
            "risk": risk,
            "behavior": beh,
        }

    def run(self, inp: IntegratedStrategyInput) -> IntegratedStrategyDecision:
        """
        Run the full integrated strategy pipeline.
        Returns IntegratedStrategyDecision (paper/research only).
        """
        blocks = check_hard_blocks(inp)
        no_trade_reasons = collect_no_trade_reasons(inp)
        scorecard = compute_scorecard(inp)
        action = determine_action(scorecard, blocks, no_trade_reasons, inp)
        summary = build_decision_summary(action, scorecard, blocks, no_trade_reasons)

        return IntegratedStrategyDecision(
            symbol=inp.symbol,
            date=inp.date,
            source_lineage=_LINEAGE,
            action=action,
            final_score=scorecard.final_score,
            grade=scorecard.grade,
            no_trade_reasons=no_trade_reasons,
            block_reasons=blocks,
            summary=summary,
        )

    def build_dashboard(self, inp: IntegratedStrategyInput) -> IntegratedDashboard:
        """Build the full integrated strategy dashboard."""
        from paper_trading.small_capital_strategy.integrated_strategy_paper_plan_v178 import build_paper_plan
        decision = self.run(inp)
        scorecard = compute_scorecard(inp)
        sub = self.build_sub_decisions(inp)

        paper_plan = None
        if decision.action in (
            IntegratedDecisionAction.PAPER_PLAN_READY,
            IntegratedDecisionAction.PAPER_ENTRY_ALLOWED,
            IntegratedDecisionAction.PAPER_ADD_ALLOWED,
        ):
            paper_plan = build_paper_plan(inp, decision)

        sections = [
            {"name": "decision", "action": decision.action.value, "score": scorecard.final_score},
            {"name": "scorecard", "grade": scorecard.grade.value, "scores": {
                "theme": scorecard.theme_score,
                "watchlist": scorecard.watchlist_score,
                "abc": scorecard.abc_score,
                "regime": scorecard.regime_score,
                "risk": scorecard.risk_score,
                "behavior": scorecard.behavior_score,
                "journal": scorecard.journal_quality_score,
            }},
            {"name": "subsystems", "watchlist": sub["watchlist"].status.value,
             "theme": sub["theme"].theme_status.value,
             "abc": sub["abc"].abc_status.value,
             "risk": sub["risk"].risk_level.value,
             "behavior": sub["behavior"].behavior_status.value},
            {"name": "no_trade_reasons", "reasons": [r.value for r in decision.no_trade_reasons]},
            {"name": "block_reasons", "reasons": [b.value for b in decision.block_reasons]},
        ]

        return IntegratedDashboard(
            date=inp.date,
            symbol=inp.symbol,
            decision=decision,
            scorecard=scorecard,
            paper_plan=paper_plan,
            watchlist_decision=sub["watchlist"],
            theme_decision=sub["theme"],
            abc_decision=sub["abc"],
            risk_decision=sub["risk"],
            behavior_decision=sub["behavior"],
            no_trade_reasons=decision.no_trade_reasons,
            block_reasons=decision.block_reasons,
            sections=sections,
        )


def run_integrated_strategy(inp: IntegratedStrategyInput) -> IntegratedStrategyDecision:
    """Convenience function: run engine and return decision."""
    return IntegratedStrategyEngine().run(inp)


def build_integrated_dashboard(inp: IntegratedStrategyInput) -> IntegratedDashboard:
    """Convenience function: run engine and return full dashboard."""
    return IntegratedStrategyEngine().build_dashboard(inp)
