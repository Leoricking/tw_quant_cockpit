"""
paper_trading/performance_attribution/scenario_registry_v167.py
Scenario Registry for Paper Performance Attribution v1.6.7.
[!] Research Only. Paper Only. No Real Orders. No Broker. Not Investment Advice.
[!] 80+ scenarios with unique IDs, categories, expected statuses. No stubs.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

RESEARCH_ONLY  = True
PAPER_ONLY     = True
NO_REAL_ORDERS = True

# ── Scenario category constants ───────────────────────────────────────────────
CAT_RETURN       = "return_decomposition"
CAT_PNL          = "pnl_attribution"
CAT_SELECTION    = "selection_attribution"
CAT_ALLOCATION   = "allocation_attribution"
CAT_TIMING       = "timing_attribution"
CAT_EXECUTION    = "execution_attribution"
CAT_COST         = "cost_attribution"
CAT_SLIPPAGE     = "slippage_attribution"
CAT_TURNOVER     = "turnover_attribution"
CAT_EXPOSURE     = "exposure_attribution"
CAT_RISK         = "risk_attribution"
CAT_DRAWDOWN     = "drawdown_attribution"
CAT_REGIME       = "regime_attribution"
CAT_BENCHMARK    = "benchmark_attribution"
CAT_FACTOR       = "factor_attribution"
CAT_STRATEGY     = "strategy_attribution"
CAT_SESSION      = "session_attribution"
CAT_SYMBOL       = "symbol_attribution"
CAT_SECTOR       = "sector_attribution"
CAT_POSITION     = "position_attribution"
CAT_TRADE        = "trade_attribution"
CAT_PORTFOLIO    = "portfolio_attribution"
CAT_RECON        = "reconciliation"
CAT_SCORE        = "scorecard"
CAT_SAFETY       = "safety"
CAT_REGRESSION   = "regression"
CAT_INTEGRATION  = "integration"

STATUS_PASS         = "PASS"
STATUS_FAIL         = "FAIL"
STATUS_DEGRADED     = "DEGRADED"
STATUS_BLOCKED      = "BLOCKED"
STATUS_EMPTY        = "EMPTY"
STATUS_INSUFFICIENT = "INSUFFICIENT_DATA"


_SCENARIOS: List[Dict[str, Any]] = [
    # ── Return decomposition ──────────────────────────────────────────────────
    {"id": "RD-001", "category": CAT_RETURN, "name": "simple_return_positive",
     "description": "Positive simple return from price appreciation",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RD-002", "category": CAT_RETURN, "name": "simple_return_negative",
     "description": "Negative simple return from price decline",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RD-003", "category": CAT_RETURN, "name": "gross_to_net_with_known_costs",
     "description": "Gross-to-net decomposition with all costs known",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RD-004", "category": CAT_RETURN, "name": "gross_to_net_unknown_costs",
     "description": "Gross-to-net decomposition with unknown costs → warning",
     "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "RD-005", "category": CAT_RETURN, "name": "active_return_sum_check",
     "description": "Active return equals sum of all attribution components",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RD-006", "category": CAT_RETURN, "name": "twr_single_period",
     "description": "Time-weighted return for a single sub-period",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RD-007", "category": CAT_RETURN, "name": "twr_multi_period",
     "description": "Time-weighted return chained across multiple sub-periods",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RD-008", "category": CAT_RETURN, "name": "mwr_irr_single_cashflow",
     "description": "Money-weighted return via IRR with one external cashflow",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RD-009", "category": CAT_RETURN, "name": "mwr_insufficient_data",
     "description": "MWR returns None when equity curve is empty",
     "expected_status": STATUS_INSUFFICIENT, "paper_only": True},
    {"id": "RD-010", "category": CAT_RETURN, "name": "residual_visible_threshold",
     "description": "Residual above threshold is flagged, never zeroed",
     "expected_status": STATUS_DEGRADED, "paper_only": True},

    # ── PnL attribution ───────────────────────────────────────────────────────
    {"id": "PN-001", "category": CAT_PNL, "name": "trade_pnl_long_profit",
     "description": "Long trade with positive PnL",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "PN-002", "category": CAT_PNL, "name": "trade_pnl_short_profit",
     "description": "Short trade with positive PnL (price falls)",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "PN-003", "category": CAT_PNL, "name": "trade_pnl_long_loss",
     "description": "Long trade with negative PnL",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "PN-004", "category": CAT_PNL, "name": "aggregate_symbol_pnl",
     "description": "Multiple trades aggregated to symbol level",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "PN-005", "category": CAT_PNL, "name": "hierarchy_sum_check",
     "description": "Symbol PnL sums to portfolio total within tolerance",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "PN-006", "category": CAT_PNL, "name": "realized_unrealized_split",
     "description": "Realized + unrealized = total PnL",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Selection attribution ─────────────────────────────────────────────────
    {"id": "SE-001", "category": CAT_SELECTION, "name": "positive_selection_effect",
     "description": "Portfolio overweights high-return stock → positive selection",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SE-002", "category": CAT_SELECTION, "name": "negative_selection_effect",
     "description": "Portfolio overweights low-return stock → negative selection",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SE-003", "category": CAT_SELECTION, "name": "selection_no_benchmark",
     "description": "Missing benchmark → INSUFFICIENT_DATA, not silent zero",
     "expected_status": STATUS_INSUFFICIENT, "paper_only": True},
    {"id": "SE-004", "category": CAT_SELECTION, "name": "brinson_fachler_formula",
     "description": "bw*(pr-br) decomposition verified numerically",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Allocation attribution ────────────────────────────────────────────────
    {"id": "AL-001", "category": CAT_ALLOCATION, "name": "positive_allocation_overweight",
     "description": "Overweight outperforming sector → positive allocation",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "AL-002", "category": CAT_ALLOCATION, "name": "negative_allocation_underweight",
     "description": "Underweight outperforming sector → negative allocation",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "AL-003", "category": CAT_ALLOCATION, "name": "cash_drag_allocation",
     "description": "Undeployed cash in rising market → negative allocation",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "AL-004", "category": CAT_ALLOCATION, "name": "allocation_no_benchmark",
     "description": "Missing benchmark → INSUFFICIENT_DATA",
     "expected_status": STATUS_INSUFFICIENT, "paper_only": True},

    # ── Timing attribution ────────────────────────────────────────────────────
    {"id": "TM-001", "category": CAT_TIMING, "name": "positive_entry_timing",
     "description": "Early entry before trend → positive timing",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "TM-002", "category": CAT_TIMING, "name": "negative_delayed_entry",
     "description": "Late entry after move → negative timing (stale signal drag)",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "TM-003", "category": CAT_TIMING, "name": "timing_no_reference",
     "description": "No reference price → INSUFFICIENT_DATA, not zero",
     "expected_status": STATUS_INSUFFICIENT, "paper_only": True},

    # ── Execution attribution ─────────────────────────────────────────────────
    {"id": "EX-001", "category": CAT_EXECUTION, "name": "implementation_shortfall_buy",
     "description": "Buy at price above decision price → negative IS",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "EX-002", "category": CAT_EXECUTION, "name": "implementation_shortfall_sell",
     "description": "Sell at price below decision price → negative IS",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "EX-003", "category": CAT_EXECUTION, "name": "execution_not_simulated_blocked",
     "description": "Execution without simulated=True → BLOCKED",
     "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "EX-004", "category": CAT_EXECUTION, "name": "partial_fill",
     "description": "Partial fill scenario → fill_ratio < 1.0",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "EX-005", "category": CAT_EXECUTION, "name": "spread_cost_decomposition",
     "description": "Bid-ask spread explicitly separated from market impact",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Cost attribution ──────────────────────────────────────────────────────
    {"id": "CO-001", "category": CAT_COST, "name": "known_commission_only",
     "description": "Trade with known commission → KNOWN quality",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "CO-002", "category": CAT_COST, "name": "estimated_tax_cost",
     "description": "Estimated tax → ESTIMATED quality, score penalized",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "CO-003", "category": CAT_COST, "name": "unknown_cost_flag",
     "description": "Unknown cost → warning, not blocked",
     "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "CO-004", "category": CAT_COST, "name": "cost_bps_derived",
     "description": "cost_bps derived from commission / notional",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Slippage attribution ──────────────────────────────────────────────────
    {"id": "SL-001", "category": CAT_SLIPPAGE, "name": "positive_slippage_buy",
     "description": "Fill below ask → positive slippage on buy",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SL-002", "category": CAT_SLIPPAGE, "name": "negative_slippage_buy",
     "description": "Fill above ask → negative slippage on buy",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SL-003", "category": CAT_SLIPPAGE, "name": "slippage_vs_vwap",
     "description": "Slippage computed relative to VWAP reference",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Turnover attribution ──────────────────────────────────────────────────
    {"id": "TV-001", "category": CAT_TURNOVER, "name": "high_turnover_drag",
     "description": "High turnover → significant drag_bps",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "TV-002", "category": CAT_TURNOVER, "name": "zero_trades_zero_turnover",
     "description": "No trades → turnover_rate = 0.0",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Exposure attribution ──────────────────────────────────────────────────
    {"id": "EXP-001", "category": CAT_EXPOSURE, "name": "net_long_exposure",
     "description": "Net long portfolio → positive market exposure",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "EXP-002", "category": CAT_EXPOSURE, "name": "concentrated_position",
     "description": "Single position >20% AUM → high concentration warning",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "EXP-003", "category": CAT_EXPOSURE, "name": "leverage_above_one",
     "description": "Gross exposure > equity → leverage > 1.0",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Risk attribution ──────────────────────────────────────────────────────
    {"id": "RK-001", "category": CAT_RISK, "name": "volatility_high",
     "description": "High-vol portfolio → vol_annualized > benchmark",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RK-002", "category": CAT_RISK, "name": "sharpe_positive",
     "description": "Positive Sharpe ratio computed from equity curve",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RK-003", "category": CAT_RISK, "name": "risk_data_insufficient",
     "description": "Fewer than 2 equity curve points → DEGRADED fallback",
     "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "RK-004", "category": CAT_RISK, "name": "downside_vol_computed",
     "description": "Downside vol uses only negative returns",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Drawdown attribution ──────────────────────────────────────────────────
    {"id": "DD-001", "category": CAT_DRAWDOWN, "name": "max_drawdown_single_peak",
     "description": "Single peak-to-trough drawdown detected",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "DD-002", "category": CAT_DRAWDOWN, "name": "drawdown_source_decomposition",
     "description": "Drawdown decomposed into strategy/regime/execution sources",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "DD-003", "category": CAT_DRAWDOWN, "name": "no_drawdown_flat_curve",
     "description": "Flat equity curve → max_drawdown = 0.0",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "DD-004", "category": CAT_DRAWDOWN, "name": "drawdown_residual_visible",
     "description": "Unattributed drawdown appears as residual, not zeroed",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Regime attribution ────────────────────────────────────────────────────
    {"id": "RG-001", "category": CAT_REGIME, "name": "bull_regime_contribution",
     "description": "Bull market period contributes positive return",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RG-002", "category": CAT_REGIME, "name": "bear_regime_contribution",
     "description": "Bear market period contributes negative return",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RG-003", "category": CAT_REGIME, "name": "unknown_regime_not_forced",
     "description": "UNKNOWN regime stays UNKNOWN, not converted to SIDEWAYS",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RG-004", "category": CAT_REGIME, "name": "multi_regime_period",
     "description": "Period spanning bull+sideways → two RegimeContribution items",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Benchmark attribution ─────────────────────────────────────────────────
    {"id": "BM-001", "category": CAT_BENCHMARK, "name": "market_benchmark_positive",
     "description": "Benchmark outperforms → negative relative return",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "BM-002", "category": CAT_BENCHMARK, "name": "missing_benchmark_flagged",
     "description": "No benchmark → status EMPTY, score penalized",
     "expected_status": STATUS_EMPTY, "paper_only": True},
    {"id": "BM-003", "category": CAT_BENCHMARK, "name": "stale_benchmark_warning",
     "description": "Stale benchmark → warning, not silent acceptance",
     "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "BM-004", "category": CAT_BENCHMARK, "name": "no_equal_weight_fallback",
     "description": "equal_weight_fallback=False enforced; no silent proxy",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Factor attribution ────────────────────────────────────────────────────
    {"id": "FA-001", "category": CAT_FACTOR, "name": "momentum_factor_positive",
     "description": "Portfolio with momentum tilt → positive factor contribution",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "FA-002", "category": CAT_FACTOR, "name": "value_factor_negative",
     "description": "Anti-value tilt → negative value factor contribution",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "FA-003", "category": CAT_FACTOR, "name": "factor_data_unavailable",
     "description": "Missing factor data → UNAVAILABLE status, not zero",
     "expected_status": STATUS_INSUFFICIENT, "paper_only": True},
    {"id": "FA-004", "category": CAT_FACTOR, "name": "proxy_confidence_not_high",
     "description": "Proxy factor data → confidence = MEDIUM or LOW, not HIGH",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Strategy attribution ──────────────────────────────────────────────────
    {"id": "ST-001", "category": CAT_STRATEGY, "name": "two_strategy_comparison",
     "description": "Two strategies compared by return contribution",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "ST-002", "category": CAT_STRATEGY, "name": "strategy_top_contributor",
     "description": "Top contributor identified by return descending",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "ST-003", "category": CAT_STRATEGY, "name": "strategy_bottom_contributor",
     "description": "Bottom contributor identified correctly",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Session attribution ───────────────────────────────────────────────────
    {"id": "SS-001", "category": CAT_SESSION, "name": "session_read_only_check",
     "description": "Session attribution must NOT modify session state",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SS-002", "category": CAT_SESSION, "name": "session_compare_two",
     "description": "Two sessions compared by return",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SS-003", "category": CAT_SESSION, "name": "session_not_found",
     "description": "Non-existent session_id returns error, not empty PASS",
     "expected_status": STATUS_FAIL, "paper_only": True},

    # ── Symbol attribution ────────────────────────────────────────────────────
    {"id": "SY-001", "category": CAT_SYMBOL, "name": "symbol_weight_computed",
     "description": "Symbol weight = position_value / portfolio_value",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SY-002", "category": CAT_SYMBOL, "name": "symbol_return_contribution",
     "description": "Symbol return contribution = weight * return",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SY-003", "category": CAT_SYMBOL, "name": "symbol_top5_bottom5",
     "description": "Top-5 and bottom-5 symbols by return",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Sector attribution ────────────────────────────────────────────────────
    {"id": "SC-001", "category": CAT_SECTOR, "name": "sector_aggregate",
     "description": "Technology sector aggregated from symbol weights/returns",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "SC-002", "category": CAT_SECTOR, "name": "missing_sector_data",
     "description": "No sector mapping → empty result, not error",
     "expected_status": STATUS_EMPTY, "paper_only": True},

    # ── Position attribution ──────────────────────────────────────────────────
    {"id": "PO-001", "category": CAT_POSITION, "name": "position_open_close_dates",
     "description": "Entry/exit dates correctly extracted from trades",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "PO-002", "category": CAT_POSITION, "name": "add_on_trim_effect",
     "description": "Position add-on increases cost basis correctly",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Trade attribution ─────────────────────────────────────────────────────
    {"id": "TR-001", "category": CAT_TRADE, "name": "trade_gross_net_pnl",
     "description": "Gross PnL minus costs equals net PnL",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "TR-002", "category": CAT_TRADE, "name": "trade_execution_quality",
     "description": "Execution quality: fill_price vs decision_price",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Portfolio attribution ─────────────────────────────────────────────────
    {"id": "PF-001", "category": CAT_PORTFOLIO, "name": "full_portfolio_compute",
     "description": "Complete portfolio attribution round-trip",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "PF-002", "category": CAT_PORTFOLIO, "name": "multi_period_aggregate",
     "description": "Multi-period arithmetic chain returns",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "PF-003", "category": CAT_PORTFOLIO, "name": "portfolio_reconciliation_check",
     "description": "Portfolio attribution includes reconciliation result",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Reconciliation ────────────────────────────────────────────────────────
    {"id": "RC-001", "category": CAT_RECON, "name": "reconciled_within_tolerance",
     "description": "Component sum within tolerance → RECONCILED",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RC-002", "category": CAT_RECON, "name": "reconciled_rounding_only",
     "description": "Very small residual → RECONCILED_WITH_ROUNDING",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "RC-003", "category": CAT_RECON, "name": "reconciliation_degraded",
     "description": "Residual 5x tolerance → DEGRADED",
     "expected_status": STATUS_DEGRADED, "paper_only": True},
    {"id": "RC-004", "category": CAT_RECON, "name": "reconciliation_failed",
     "description": "Large residual → FAILED, never auto-fixed",
     "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "RC-005", "category": CAT_RECON, "name": "residual_never_zeroed",
     "description": "Residual field always present and non-zero when applicable",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Scorecard ─────────────────────────────────────────────────────────────
    {"id": "QS-001", "category": CAT_SCORE, "name": "score_high_all_complete",
     "description": "All data complete + reconciled → score near max",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "QS-002", "category": CAT_SCORE, "name": "score_zero_real_markers",
     "description": "Real markers present → score = 0, grade F, BLOCKED",
     "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "QS-003", "category": CAT_SCORE, "name": "fixture_cap_80pct",
     "description": "Fixture-only run → scores capped at 80%",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "QS-004", "category": CAT_SCORE, "name": "missing_benchmark_penalty",
     "description": "Missing benchmark subtracts 10 from max score",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Safety ────────────────────────────────────────────────────────────────
    {"id": "SF-001", "category": CAT_SAFETY, "name": "forbidden_field_blocked",
     "description": "broker_session in input → BLOCKED immediately",
     "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "SF-002", "category": CAT_SAFETY, "name": "missing_safety_marker_invalid",
     "description": "paper_only=False → validation fails explicitly",
     "expected_status": STATUS_FAIL, "paper_only": True},
    {"id": "SF-003", "category": CAT_SAFETY, "name": "real_account_token_blocked",
     "description": "real_account_token in run data → save_run rejected",
     "expected_status": STATUS_BLOCKED, "paper_only": True},
    {"id": "SF-004", "category": CAT_SAFETY, "name": "all_safety_flags_present",
     "description": "All safety flags verified on every module",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Regression ───────────────────────────────────────────────────────────
    {"id": "REG-001", "category": CAT_REGRESSION, "name": "v166_compatibility",
     "description": "v1.6.6 fixture can be loaded without error",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "REG-002", "category": CAT_REGRESSION, "name": "deterministic_same_input",
     "description": "Same input produces identical output across two runs",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "REG-003", "category": CAT_REGRESSION, "name": "empty_store_summary",
     "description": "Empty AttributionStore returns zero totals, not error",
     "expected_status": STATUS_PASS, "paper_only": True},

    # ── Integration ───────────────────────────────────────────────────────────
    {"id": "INT-001", "category": CAT_INTEGRATION, "name": "full_pipeline_single_symbol",
     "description": "End-to-end: input → all engines → store → query → report",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "INT-002", "category": CAT_INTEGRATION, "name": "full_pipeline_multi_symbol",
     "description": "Multi-symbol portfolio through full attribution pipeline",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "INT-003", "category": CAT_INTEGRATION, "name": "report_all_31_sections",
     "description": "Report engine produces all 31 sections without error",
     "expected_status": STATUS_PASS, "paper_only": True},
    {"id": "INT-004", "category": CAT_INTEGRATION, "name": "cli_query_all_levels",
     "description": "CLI query returns all attribution levels for a run",
     "expected_status": STATUS_PASS, "paper_only": True},
]

assert len(_SCENARIOS) >= 80, f"Expected >=80 scenarios, got {len(_SCENARIOS)}"

# Build lookup indices
_BY_ID: Dict[str, Dict[str, Any]] = {s["id"]: s for s in _SCENARIOS}
_BY_CATEGORY: Dict[str, List[Dict[str, Any]]] = {}
for _s in _SCENARIOS:
    _BY_CATEGORY.setdefault(_s["category"], []).append(_s)


class ScenarioRegistry:
    """
    Registry for all paper attribution scenarios.
    Read-only after construction. Never modifies scenarios.
    """

    def get(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        """Get scenario by unique ID. Returns None if not found."""
        return _BY_ID.get(scenario_id)

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all scenarios in a category."""
        return list(_BY_CATEGORY.get(category, []))

    def list_ids(self) -> List[str]:
        """Sorted list of all scenario IDs."""
        return sorted(_BY_ID.keys())

    def list_categories(self) -> List[str]:
        """Sorted list of all category names."""
        return sorted(_BY_CATEGORY.keys())

    def count(self) -> int:
        """Total number of scenarios."""
        return len(_SCENARIOS)

    def count_by_status(self, expected_status: str) -> int:
        """Count scenarios with given expected_status."""
        return sum(1 for s in _SCENARIOS if s["expected_status"] == expected_status)

    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find scenario by name (first match)."""
        for s in _SCENARIOS:
            if s["name"] == name:
                return s
        return None

    def all_scenarios(self) -> List[Dict[str, Any]]:
        """Return all scenarios (copies)."""
        return list(_SCENARIOS)

    def summarize(self) -> Dict[str, Any]:
        """Return registry statistics."""
        statuses = [s["expected_status"] for s in _SCENARIOS]
        return {
            "total": len(_SCENARIOS),
            "categories": len(_BY_CATEGORY),
            "pass_scenarios": statuses.count(STATUS_PASS),
            "fail_scenarios": statuses.count(STATUS_FAIL),
            "blocked_scenarios": statuses.count(STATUS_BLOCKED),
            "degraded_scenarios": statuses.count(STATUS_DEGRADED),
            "insufficient_scenarios": statuses.count(STATUS_INSUFFICIENT),
            "empty_scenarios": statuses.count(STATUS_EMPTY),
            "paper_only": True,
            "research_only": True,
        }
