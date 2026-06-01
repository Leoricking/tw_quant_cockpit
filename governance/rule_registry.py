"""
governance/rule_registry.py — Central rule registry (v0.3.28).
[!] Research Only. No Real Orders. No Auto Weight Apply. Production Trading: BLOCKED.

Safety invariants:
  read_only = True
  no_real_orders = True
  production_blocked = True
  Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
"""

import os
from typing import Optional

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from governance.rule_metadata import (
    RuleMetadata,
    RULE_STATUS_ACTIVE,
    RULE_STATUS_EXPERIMENTAL,
    RULE_STATUS_NEEDS_REVIEW,
    RULE_STATUS_INSUFFICIENT_SAMPLE,
    CONFIDENCE_UNKNOWN,
    CONFIDENCE_PLANNED,
)

# Candidate status: ingested from transcript, NOT yet validated or auto-activated.
RULE_STATUS_CANDIDATE = "CANDIDATE"


class RuleRegistry:
    """
    Central registry for all strategy rules.

    Safety invariants:
      read_only = True
      no_real_orders = True
      production_blocked = True
      Research Only, No Real Orders, No Auto Weight Apply, Production Trading BLOCKED
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self):
        self._rules: dict = {}  # rule_id -> RuleMetadata

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_rule(self, metadata: RuleMetadata) -> None:
        """Register a single rule (overwrites if rule_id already exists)."""
        if not metadata.rule_id:
            raise ValueError("RuleMetadata must have a non-empty rule_id")
        self._rules[metadata.rule_id] = metadata

    # ------------------------------------------------------------------
    # Built-in rule definitions
    # ------------------------------------------------------------------

    def load_builtin_rules(self) -> int:
        """Register all built-in rules and return the count loaded."""

        _defs = [
            # ----------------------------------------------------------------
            # A. Buy Point Rules
            # ----------------------------------------------------------------
            dict(
                rule_id="BUY.SHORT.PULLBACK_10MA.V1",
                rule_name="Pullback to 10-day MA",
                category="buy_point",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Price pulls back to 10-day MA in uptrend",
                signal_type="buy",
            ),
            dict(
                rule_id="BUY.SHORT.PULLBACK_5MA.V1",
                rule_name="Pullback to 5-day MA",
                category="buy_point",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Price pulls back to 5-day MA in strong uptrend",
                signal_type="buy",
            ),
            dict(
                rule_id="BUY.SHORT.RECLAIM_20MA.V1",
                rule_name="Reclaim 20-day MA",
                category="buy_point",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Price reclaims 20-day MA after dip",
                signal_type="buy",
            ),
            dict(
                rule_id="BUY.SHORT.BREAKOUT_VOLUME.V1",
                rule_name="Breakout with Volume",
                category="buy_point",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Breakout above resistance with >1.5x avg volume",
                signal_type="buy",
                dependencies=["SCREEN.UNIVERSAL.VOLUME_BREAKOUT.V1"],
            ),
            dict(
                rule_id="BUY.SHORT.SECOND_WAVE.V1",
                rule_name="Second Wave Entry",
                category="buy_point",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Second wave entry after confirmed uptrend",
                signal_type="buy",
                dependencies=[
                    "SCREEN.UNIVERSAL.MAIN_THEME_STRENGTH.V1",
                    "SCREEN.UNIVERSAL.INSTITUTIONAL_BUYING.V1",
                ],
            ),
            # ----------------------------------------------------------------
            # B. Screener Rules
            # ----------------------------------------------------------------
            dict(
                rule_id="SCREEN.UNIVERSAL.MAIN_THEME_STRENGTH.V1",
                rule_name="Main Theme Strength",
                category="screener",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Strong sector theme momentum",
                signal_type="screen",
            ),
            dict(
                rule_id="SCREEN.UNIVERSAL.REVENUE_GROWTH.V1",
                rule_name="Revenue Growth",
                category="screener",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Monthly revenue YoY > threshold",
                signal_type="screen",
            ),
            dict(
                rule_id="SCREEN.UNIVERSAL.MA_ALIGNMENT.V1",
                rule_name="MA Alignment",
                category="screener",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="5MA > 20MA > 60MA alignment",
                signal_type="screen",
            ),
            dict(
                rule_id="SCREEN.UNIVERSAL.VOLUME_BREAKOUT.V1",
                rule_name="Volume Breakout",
                category="screener",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Volume > 1.5x 20-day average",
                signal_type="screen",
            ),
            dict(
                rule_id="SCREEN.UNIVERSAL.INSTITUTIONAL_BUYING.V1",
                rule_name="Institutional Buying",
                category="screener",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="3-day net institutional buying positive",
                signal_type="screen",
            ),
            dict(
                rule_id="SCREEN.UNIVERSAL.MARGIN_CONTROL.V1",
                rule_name="Margin Control",
                category="screener",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Margin ratio within safe bounds",
                signal_type="filter",
            ),
            dict(
                rule_id="SCREEN.UNIVERSAL.MAJOR_HOLDER_UP.V1",
                rule_name="Major Holder Increasing",
                category="screener",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Major holder count increasing",
                signal_type="screen",
            ),
            dict(
                rule_id="SCREEN.UNIVERSAL.RETAIL_HOLDER_DOWN.V1",
                rule_name="Retail Holder Decreasing",
                category="screener",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Retail holder count decreasing (institutional accumulation)",
                signal_type="screen",
            ),
            # ----------------------------------------------------------------
            # C. Strategy Knowledge Rules
            # ----------------------------------------------------------------
            dict(
                rule_id="STRATEGY.SHORT.VOLUME_BREAKOUT_CONFIRMED.V1",
                rule_name="Volume Breakout Confirmed",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Volume breakout confirmed by price action",
                signal_type="buy",
            ),
            dict(
                rule_id="STRATEGY.SHORT.VOLUME_ROLLING.V1",
                rule_name="Volume Rolling Pattern",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Rolling volume pattern suggests accumulation",
                signal_type="buy",
            ),
            dict(
                rule_id="STRATEGY.SHORT.FAILED_BREAKOUT_EXIT.V1",
                rule_name="Failed Breakout Exit",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Exit on failed breakout detection",
                signal_type="sell",
            ),
            dict(
                rule_id="STRATEGY.SHORT.MACD_PULLBACK.V1",
                rule_name="MACD Pullback",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="MACD histogram pullback buy signal",
                signal_type="buy",
            ),
            dict(
                rule_id="STRATEGY.SHORT.MACD_BEAR_REBOUND.V1",
                rule_name="MACD Bear Rebound",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="MACD bear-phase rebound end detection",
                signal_type="buy",
            ),
            dict(
                rule_id="STRATEGY.SHORT.KD_GOLDEN_CROSS.V1",
                rule_name="KD Golden Cross",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="KD low-zone golden cross buy signal",
                signal_type="buy",
            ),
            dict(
                rule_id="STRATEGY.SHORT.SHORT_INTEREST_RISK.V1",
                rule_name="Short Interest Risk",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_NEEDS_REVIEW,
                description="High short interest risk flag",
                signal_type="filter",
            ),
            dict(
                rule_id="STRATEGY.SHORT.BOTTOM_REVERSAL.V1",
                rule_name="Bottom Reversal",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Bottom reversal pattern detection",
                signal_type="buy",
            ),
            dict(
                rule_id="STRATEGY.SHORT.SECTOR_ROTATION.V1",
                rule_name="Sector Rotation",
                category="strategy_knowledge",
                timeframe="short",
                status=RULE_STATUS_ACTIVE,
                description="Sector rotation entry signal",
                signal_type="buy",
            ),
            dict(
                rule_id="STRATEGY.UNIVERSAL.FUNDAMENTAL_QUALITY.V1",
                rule_name="Fundamental Quality Gate",
                category="strategy_knowledge",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Fundamental quality gate",
                signal_type="filter",
            ),
            # ----------------------------------------------------------------
            # D. Long-Term Rules
            # ----------------------------------------------------------------
            dict(
                rule_id="LONG.FUNDAMENTAL.EPS_POSITIVE.V1",
                rule_name="EPS Positive and Growing",
                category="long_term",
                timeframe="long",
                status=RULE_STATUS_ACTIVE,
                description="EPS positive and growing",
                signal_type="filter",
            ),
            dict(
                rule_id="LONG.FUNDAMENTAL.GROSS_MARGIN_TREND.V1",
                rule_name="Gross Margin Trend",
                category="long_term",
                timeframe="long",
                status=RULE_STATUS_ACTIVE,
                description="Gross margin improving over 4 quarters",
                signal_type="filter",
            ),
            dict(
                rule_id="LONG.FUNDAMENTAL.OPERATING_MARGIN_TREND.V1",
                rule_name="Operating Margin Trend",
                category="long_term",
                timeframe="long",
                status=RULE_STATUS_ACTIVE,
                description="Operating margin stable or improving",
                signal_type="filter",
            ),
            dict(
                rule_id="LONG.FUNDAMENTAL.PE_BUCKET.V1",
                rule_name="P/E Bucket",
                category="long_term",
                timeframe="long",
                status=RULE_STATUS_ACTIVE,
                description="P/E in reasonable range for sector",
                signal_type="filter",
            ),
            dict(
                rule_id="LONG.FUNDAMENTAL.TIMING_QUALITY.V1",
                rule_name="Timing Quality",
                category="long_term",
                timeframe="long",
                status=RULE_STATUS_ACTIVE,
                description="Entry timing quality relative to MA60",
                signal_type="filter",
            ),
            dict(
                rule_id="LONG.FUNDAMENTAL.LONG_TERM_SCORE.V1",
                rule_name="Long-Term Score",
                category="long_term",
                timeframe="long",
                status=RULE_STATUS_ACTIVE,
                description="Composite long-term fundamental score",
                signal_type="filter",
            ),
            # ----------------------------------------------------------------
            # E. Portfolio Rules
            # ----------------------------------------------------------------
            dict(
                rule_id="PORTFOLIO.RISK.MAX_POSITION_SIZE.V1",
                rule_name="Max Position Size",
                category="portfolio",
                timeframe="portfolio",
                status=RULE_STATUS_ACTIVE,
                description="Max single position <= 20% of portfolio",
                signal_type="filter",
            ),
            dict(
                rule_id="PORTFOLIO.RISK.MAX_SECTOR_EXPOSURE.V1",
                rule_name="Max Sector Exposure",
                category="portfolio",
                timeframe="portfolio",
                status=RULE_STATUS_ACTIVE,
                description="Max sector exposure <= 40%",
                signal_type="filter",
            ),
            dict(
                rule_id="PORTFOLIO.RISK.DRAWDOWN_GUARD.V1",
                rule_name="Drawdown Guard",
                category="portfolio",
                timeframe="portfolio",
                status=RULE_STATUS_ACTIVE,
                description="Portfolio drawdown guard -15%",
                signal_type="filter",
            ),
            dict(
                rule_id="PORTFOLIO.RISK.CASH_BUFFER.V1",
                rule_name="Cash Buffer",
                category="portfolio",
                timeframe="portfolio",
                status=RULE_STATUS_ACTIVE,
                description="Maintain min 10% cash buffer",
                signal_type="filter",
            ),
            dict(
                rule_id="PORTFOLIO.RISK.RISK_BUDGET.V1",
                rule_name="Risk Budget",
                category="portfolio",
                timeframe="portfolio",
                status=RULE_STATUS_ACTIVE,
                description="Total risk budget within limits",
                signal_type="filter",
            ),
            dict(
                rule_id="PORTFOLIO.RISK.LIQUIDITY_FILTER.V1",
                rule_name="Liquidity Filter",
                category="portfolio",
                timeframe="portfolio",
                status=RULE_STATUS_ACTIVE,
                description="Min daily liquidity for position sizing",
                signal_type="filter",
            ),
            # ----------------------------------------------------------------
            # F. Signal Quality Rules
            # ----------------------------------------------------------------
            dict(
                rule_id="SIGNAL.QUALITY.BOOST.V1",
                rule_name="Signal Boost",
                category="signal_quality",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Signal boost: strong confirmation across timeframes",
                signal_type="quality",
            ),
            dict(
                rule_id="SIGNAL.QUALITY.KEEP.V1",
                rule_name="Signal Keep",
                category="signal_quality",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Signal keep: moderate but consistent",
                signal_type="quality",
            ),
            dict(
                rule_id="SIGNAL.QUALITY.REDUCE.V1",
                rule_name="Signal Reduce",
                category="signal_quality",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Signal reduce: weak or conflicting signals",
                signal_type="quality",
            ),
            dict(
                rule_id="SIGNAL.QUALITY.DISABLE.V1",
                rule_name="Signal Disable",
                category="signal_quality",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Signal disable: contradictory evidence",
                signal_type="quality",
            ),
            dict(
                rule_id="SIGNAL.QUALITY.INSUFFICIENT_SAMPLE.V1",
                rule_name="Insufficient Sample",
                category="signal_quality",
                timeframe="universal",
                status=RULE_STATUS_INSUFFICIENT_SAMPLE,
                description="Signal insufficient sample for reliable scoring",
                signal_type="quality",
            ),
            # ----------------------------------------------------------------
            # G. Intraday Rules
            # ----------------------------------------------------------------
            dict(
                rule_id="INTRADAY.OPENING.RANGE_STRENGTH.V1",
                rule_name="Opening Range Strength",
                category="intraday",
                timeframe="intraday",
                status=RULE_STATUS_ACTIVE,
                description="Opening range breakout strength score",
                signal_type="buy",
            ),
            dict(
                rule_id="INTRADAY.VWAP.RECLAIM.V1",
                rule_name="VWAP Reclaim",
                category="intraday",
                timeframe="intraday",
                status=RULE_STATUS_ACTIVE,
                description="Price reclaims VWAP after dip",
                signal_type="buy",
            ),
            dict(
                rule_id="INTRADAY.VWAP.LOST.V1",
                rule_name="VWAP Lost",
                category="intraday",
                timeframe="intraday",
                status=RULE_STATUS_ACTIVE,
                description="Price loses VWAP support — caution signal",
                signal_type="sell",
            ),
            dict(
                rule_id="INTRADAY.BREAKOUT.FAKE_BREAKOUT_RISK.V1",
                rule_name="Fake Breakout Risk",
                category="intraday",
                timeframe="intraday",
                status=RULE_STATUS_EXPERIMENTAL,
                experimental=True,
                description="Fake breakout risk from opening range",
                signal_type="filter",
            ),
            dict(
                rule_id="INTRADAY.VOLUME.POC_SUPPORT.V1",
                rule_name="POC Support Level",
                category="intraday",
                timeframe="intraday",
                status=RULE_STATUS_EXPERIMENTAL,
                experimental=True,
                description="Point of control support level",
                signal_type="filter",
            ),
            dict(
                rule_id="INTRADAY.MICROSTRUCTURE.BAR_ONLY.V1",
                rule_name="Bar-Only Microstructure",
                category="intraday",
                timeframe="intraday",
                status=RULE_STATUS_EXPERIMENTAL,
                experimental=True,
                description="Microstructure using bar data only (tick unavailable)",
                signal_type="filter",
            ),
            dict(
                rule_id="INTRADAY.MICROSTRUCTURE.TICK_PLANNED.V1",
                rule_name="Tick Microstructure (Planned)",
                category="intraday",
                timeframe="intraday",
                status=RULE_STATUS_EXPERIMENTAL,
                experimental=True,
                confidence_level=CONFIDENCE_PLANNED,
                description="Tick/bidask microstructure — planned for v0.4+",
                signal_type="filter",
            ),
            # ----------------------------------------------------------------
            # H. Backtest / Governance Rules
            # ----------------------------------------------------------------
            dict(
                rule_id="BACKTEST.EXECUTION.NEXT_OPEN.V1",
                rule_name="Entry at Next-Day Open",
                category="governance",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Entry at next-day open (realistic)",
                signal_type="governance",
                source_module="backtest.execution_model",
            ),
            dict(
                rule_id="BACKTEST.EXECUTION.SIGNAL_CLOSE.V1",
                rule_name="Entry at Signal-Day Close",
                category="governance",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Entry at signal-day close (optimistic)",
                signal_type="governance",
                source_module="backtest.execution_model",
            ),
            dict(
                rule_id="BACKTEST.COST.TAIWAN_REALISTIC.V1",
                rule_name="Taiwan Realistic Cost Model",
                category="governance",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description=(
                    "Taiwan stock cost: 0.1425% comm x 0.6, "
                    "0.3% sell tax, 5bps slippage"
                ),
                signal_type="governance",
                source_module="backtest.cost_model",
            ),
            dict(
                rule_id="BACKTEST.LIQUIDITY.REQUIRED.V1",
                rule_name="Liquidity Filter Required",
                category="governance",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Liquidity filter required for valid backtest",
                signal_type="governance",
                source_module="backtest.liquidity_filter",
            ),
            dict(
                rule_id="BACKTEST.RISK.GAP_BLOCK.V1",
                rule_name="Gap Risk Block",
                category="governance",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Gap risk block: no entry on large gap days",
                signal_type="governance",
                source_module="backtest.gap_risk_model",
            ),
            dict(
                rule_id="BACKTEST.VALIDATION.WALK_FORWARD.V1",
                rule_name="Walk-Forward Validation",
                category="governance",
                timeframe="universal",
                status=RULE_STATUS_ACTIVE,
                description="Walk-forward validation required for grade A/B",
                signal_type="governance",
                source_module="backtest.validation_split",
            ),
            # ----------------------------------------------------------------
            # H. Transcript Candidate Rules (v0.4.1.1)
            #    Status: CANDIDATE — ingested from transcripts only.
            #    NOT auto-activated. NOT validated by backtest.
            #    Confidence capped at PARTIAL per transcript source policy.
            # ----------------------------------------------------------------
            dict(
                rule_id="RISK.TECHNICAL.TOP_PATTERN.V1",
                rule_name="Top Pattern Risk",
                category="risk",
                timeframe="short",
                status=RULE_STATUS_NEEDS_REVIEW,
                description=(
                    "Avoid stocks showing M-top, triple-top, head-and-shoulders, "
                    "arc-top, or single-day reversal patterns. "
                    "Candidate from transcript ingestion — not backtest validated."
                ),
                signal_type="risk",
                confidence=CONFIDENCE_PLANNED,
            ),
            dict(
                rule_id="RISK.RELATIVE_WEAKNESS.MARKET_NEW_HIGH_STOCK_LAG.V1",
                rule_name="Market New High But Stock Lags",
                category="risk",
                timeframe="short",
                status=RULE_STATUS_NEEDS_REVIEW,
                description=(
                    "Index makes new high but individual stock fails to make new high. "
                    "Relative weakness signal — avoid or reduce. "
                    "Candidate from transcript ingestion — not backtest validated."
                ),
                signal_type="risk",
                confidence=CONFIDENCE_PLANNED,
            ),
            dict(
                rule_id="RISK.CYCLE.CRASH_WATCH.V1",
                rule_name="Long-Cycle Crash Watch",
                category="risk",
                timeframe="cycle",
                status=RULE_STATUS_NEEDS_REVIEW,
                description=(
                    "Long-cycle crash watch: potential 50% drawdown risk in 2028-2031 window. "
                    "Qualitative / cycle risk only. "
                    "NOT a short-term sell signal. NOT investment advice. "
                    "Candidate from transcript ingestion — not backtest validated."
                ),
                signal_type="risk",
                confidence=CONFIDENCE_PLANNED,
            ),
            dict(
                rule_id="RISK.FUNDAMENTAL.REVENUE_NOT_SUPPORTING_THEME.V1",
                rule_name="Revenue Not Supporting Theme",
                category="risk",
                timeframe="medium",
                status=RULE_STATUS_NEEDS_REVIEW,
                description=(
                    "Pure theme play without revenue/EPS backing. "
                    "Revenue stagnant or declining while narrative continues. "
                    "Candidate from transcript ingestion — not backtest validated."
                ),
                signal_type="risk",
                confidence=CONFIDENCE_PLANNED,
            ),
            dict(
                rule_id="RISK.PORTFOLIO.OVER_CONCENTRATION.V1",
                rule_name="Portfolio Over-Concentration",
                category="risk",
                timeframe="universal",
                status=RULE_STATUS_NEEDS_REVIEW,
                description=(
                    "Portfolio discipline: max 4 positions for small capital, "
                    "6-8 for larger capital. No single-stock concentration. "
                    "Candidate from transcript ingestion — not backtest validated."
                ),
                signal_type="risk",
                confidence=CONFIDENCE_PLANNED,
            ),
            dict(
                rule_id="RISK.PORTFOLIO.MARGIN_USAGE.V1",
                rule_name="Margin Usage Risk",
                category="risk",
                timeframe="universal",
                status=RULE_STATUS_NEEDS_REVIEW,
                description=(
                    "No margin (融資) usage. Risk discipline from knowledge source. "
                    "Candidate from transcript ingestion — not backtest validated."
                ),
                signal_type="risk",
                confidence=CONFIDENCE_PLANNED,
            ),
        ]

        count = 0
        for d in _defs:
            self.register_rule(RuleMetadata(**d))
            count += 1
        return count

    # ------------------------------------------------------------------
    # Query / access
    # ------------------------------------------------------------------

    def list_rules(self, category=None, status=None) -> list:
        """Return list of RuleMetadata objects, optionally filtered."""
        result = list(self._rules.values())
        if category is not None:
            result = [r for r in result if r.category == category]
        if status is not None:
            result = [r for r in result if r.status == status]
        return result

    def get_rule(self, rule_id: str) -> Optional[RuleMetadata]:
        """Return RuleMetadata for the given rule_id, or None."""
        return self._rules.get(rule_id)

    def update_rule_status(
        self, rule_id: str, status: str, reason: str = None
    ) -> bool:
        """Update status for a rule. Returns True on success."""
        rule = self._rules.get(rule_id)
        if rule is None:
            return False
        rule.status = status
        if reason:
            rule.notes = (rule.notes + f" | Status updated: {reason}").strip(" |")
        return True

    def export_rules(self) -> list:
        """Return list of all rules as dicts."""
        return [r.to_dict() for r in self._rules.values()]

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_rule_summary(self) -> dict:
        """Build a summary dict of registry statistics."""
        rules = list(self._rules.values())

        by_status: dict = {}
        by_category: dict = {}
        by_confidence: dict = {}

        for r in rules:
            by_status[r.status] = by_status.get(r.status, 0) + 1
            by_category[r.category] = by_category.get(r.category, 0) + 1
            by_confidence[r.confidence_level] = (
                by_confidence.get(r.confidence_level, 0) + 1
            )

        return {
            "total_rules": len(rules),
            "by_status": by_status,
            "by_category": by_category,
            "by_confidence": by_confidence,
            "experimental_count": sum(1 for r in rules if r.experimental),
            "needs_review_count": sum(
                1 for r in rules if r.status == RULE_STATUS_NEEDS_REVIEW
            ),
            "active_count": sum(
                1 for r in rules if r.status == RULE_STATUS_ACTIVE
            ),
            "read_only": True,
            "no_real_orders": True,
            "production_blocked": True,
        }
