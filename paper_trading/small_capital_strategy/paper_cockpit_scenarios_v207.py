"""
paper_trading/small_capital_strategy/paper_cockpit_scenarios_v207.py
v2.0.7 Paper Theme Rotation & Market Regime Control — Scenarios
[!] Paper Only. Research Only. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "207"

SCENARIOS: List[Dict[str, Any]] = [
    # --- 1-10: theme state classification ---
    {"scenario_id": "SC207-001", "schema_version": "207", "paper_only": True, "description": "Leading theme: high score + high momentum + low overheat", "theme_score": 85.0, "momentum_score": 80.0, "overheating_score": 25.0, "weakening_score": 10.0, "breadth_score": 75.0, "expected_state": "leading"},
    {"scenario_id": "SC207-002", "schema_version": "207", "paper_only": True, "description": "Strengthening theme: solid score + momentum", "theme_score": 72.0, "momentum_score": 65.0, "overheating_score": 20.0, "weakening_score": 15.0, "breadth_score": 60.0, "expected_state": "strengthening"},
    {"scenario_id": "SC207-003", "schema_version": "207", "paper_only": True, "description": "Emerging theme: moderate score + moderate momentum", "theme_score": 48.0, "momentum_score": 42.0, "overheating_score": 10.0, "weakening_score": 20.0, "breadth_score": 40.0, "expected_state": "emerging"},
    {"scenario_id": "SC207-004", "schema_version": "207", "paper_only": True, "description": "Overheating theme: very high overheating score", "theme_score": 88.0, "momentum_score": 75.0, "overheating_score": 80.0, "weakening_score": 5.0, "breadth_score": 70.0, "expected_state": "overheating"},
    {"scenario_id": "SC207-005", "schema_version": "207", "paper_only": True, "description": "Weakening theme: high weakening score", "theme_score": 50.0, "momentum_score": 40.0, "overheating_score": 20.0, "weakening_score": 75.0, "breadth_score": 50.0, "expected_state": "weakening"},
    {"scenario_id": "SC207-006", "schema_version": "207", "paper_only": True, "description": "Crowded theme: high score + very high breadth + moderate overheat", "theme_score": 75.0, "momentum_score": 65.0, "overheating_score": 55.0, "weakening_score": 10.0, "breadth_score": 85.0, "expected_state": "crowded"},
    {"scenario_id": "SC207-007", "schema_version": "207", "paper_only": True, "description": "Cooling theme: moderate weakening + low score", "theme_score": 35.0, "momentum_score": 30.0, "overheating_score": 15.0, "weakening_score": 55.0, "breadth_score": 30.0, "expected_state": "cooling"},
    {"scenario_id": "SC207-008", "schema_version": "207", "paper_only": True, "description": "Stale theme: very low score + low momentum", "theme_score": 15.0, "momentum_score": 18.0, "overheating_score": 5.0, "weakening_score": 55.0, "breadth_score": 15.0, "expected_state": "stale"},
    {"scenario_id": "SC207-009", "schema_version": "207", "paper_only": True, "description": "Risk-off theme: very low momentum + very low score", "theme_score": 20.0, "momentum_score": 15.0, "overheating_score": 0.0, "weakening_score": 30.0, "breadth_score": 20.0, "expected_state": "risk_off"},
    {"scenario_id": "SC207-010", "schema_version": "207", "paper_only": True, "description": "Neutral theme: mid range all scores", "theme_score": 52.0, "momentum_score": 48.0, "overheating_score": 30.0, "weakening_score": 25.0, "breadth_score": 50.0, "expected_state": "neutral"},
    # --- 11-20: market state classification ---
    {"scenario_id": "SC207-011", "schema_version": "207", "paper_only": True, "description": "Strong uptrend: high index + high breadth + strong volume", "index_trend_score": 80.0, "breadth_score": 75.0, "volatility_score": 35.0, "volume_score": 70.0, "risk_appetite_score": 75.0, "expected_state": "strong_uptrend"},
    {"scenario_id": "SC207-012", "schema_version": "207", "paper_only": True, "description": "Healthy pullback: moderate index + moderate breadth", "index_trend_score": 60.0, "breadth_score": 58.0, "volatility_score": 40.0, "volume_score": 52.0, "risk_appetite_score": 60.0, "expected_state": "healthy_pullback"},
    {"scenario_id": "SC207-013", "schema_version": "207", "paper_only": True, "description": "Range bound: mid range all scores", "index_trend_score": 50.0, "breadth_score": 50.0, "volatility_score": 40.0, "volume_score": 45.0, "risk_appetite_score": 50.0, "expected_state": "range_bound"},
    {"scenario_id": "SC207-014", "schema_version": "207", "paper_only": True, "description": "Weak rebound: moderate index + low volume", "index_trend_score": 45.0, "breadth_score": 42.0, "volatility_score": 45.0, "volume_score": 38.0, "risk_appetite_score": 45.0, "expected_state": "weak_rebound"},
    {"scenario_id": "SC207-015", "schema_version": "207", "paper_only": True, "description": "Downtrend: low index + low breadth", "index_trend_score": 25.0, "breadth_score": 28.0, "volatility_score": 55.0, "volume_score": 40.0, "risk_appetite_score": 35.0, "expected_state": "downtrend"},
    {"scenario_id": "SC207-016", "schema_version": "207", "paper_only": True, "description": "High volatility: very high volatility score", "index_trend_score": 50.0, "breadth_score": 45.0, "volatility_score": 85.0, "volume_score": 60.0, "risk_appetite_score": 40.0, "expected_state": "high_volatility"},
    {"scenario_id": "SC207-017", "schema_version": "207", "paper_only": True, "description": "Risk-off: very low risk appetite + low trend", "index_trend_score": 20.0, "breadth_score": 22.0, "volatility_score": 70.0, "volume_score": 30.0, "risk_appetite_score": 15.0, "expected_state": "risk_off"},
    {"scenario_id": "SC207-018", "schema_version": "207", "paper_only": True, "description": "Volatility overrides uptrend classification", "index_trend_score": 75.0, "breadth_score": 70.0, "volatility_score": 82.0, "volume_score": 65.0, "risk_appetite_score": 55.0, "expected_state": "high_volatility"},
    {"scenario_id": "SC207-019", "schema_version": "207", "paper_only": True, "description": "Risk-off overrides downtrend label", "index_trend_score": 28.0, "breadth_score": 25.0, "volatility_score": 65.0, "volume_score": 30.0, "risk_appetite_score": 18.0, "expected_state": "risk_off"},
    {"scenario_id": "SC207-020", "schema_version": "207", "paper_only": True, "description": "Boundary strong uptrend minimum", "index_trend_score": 70.0, "breadth_score": 65.0, "volatility_score": 30.0, "volume_score": 60.0, "risk_appetite_score": 65.0, "expected_state": "strong_uptrend"},
    # --- 21-30: allowed_risk_mode classification ---
    {"scenario_id": "SC207-021", "schema_version": "207", "paper_only": True, "description": "aggressive_paper in strong_uptrend", "market_state": "strong_uptrend", "expected_risk_mode": "aggressive_paper"},
    {"scenario_id": "SC207-022", "schema_version": "207", "paper_only": True, "description": "normal_paper in healthy_pullback", "market_state": "healthy_pullback", "expected_risk_mode": "normal_paper"},
    {"scenario_id": "SC207-023", "schema_version": "207", "paper_only": True, "description": "normal_paper in range_bound", "market_state": "range_bound", "expected_risk_mode": "normal_paper"},
    {"scenario_id": "SC207-024", "schema_version": "207", "paper_only": True, "description": "defensive_paper in weak_rebound", "market_state": "weak_rebound", "expected_risk_mode": "defensive_paper"},
    {"scenario_id": "SC207-025", "schema_version": "207", "paper_only": True, "description": "observation_only in downtrend", "market_state": "downtrend", "expected_risk_mode": "observation_only"},
    {"scenario_id": "SC207-026", "schema_version": "207", "paper_only": True, "description": "defensive_paper in high_volatility", "market_state": "high_volatility", "expected_risk_mode": "defensive_paper"},
    {"scenario_id": "SC207-027", "schema_version": "207", "paper_only": True, "description": "freeze_promotion in risk_off", "market_state": "risk_off", "expected_risk_mode": "freeze_promotion"},
    {"scenario_id": "SC207-028", "schema_version": "207", "paper_only": True, "description": "candidate_promotion_allowed in strong_uptrend", "market_state": "strong_uptrend", "expected_promotion_allowed": True},
    {"scenario_id": "SC207-029", "schema_version": "207", "paper_only": True, "description": "candidate_promotion_blocked in downtrend", "market_state": "downtrend", "expected_promotion_allowed": False},
    {"scenario_id": "SC207-030", "schema_version": "207", "paper_only": True, "description": "aggressive_entry only in strong_uptrend", "market_state": "strong_uptrend", "expected_aggressive": True},
    # --- 31-40: theme action classification ---
    {"scenario_id": "SC207-031", "schema_version": "207", "paper_only": True, "description": "increase_attention for emerging theme", "theme_state": "emerging", "expected_action": "increase_attention"},
    {"scenario_id": "SC207-032", "schema_version": "207", "paper_only": True, "description": "increase_attention for strengthening theme", "theme_state": "strengthening", "expected_action": "increase_attention"},
    {"scenario_id": "SC207-033", "schema_version": "207", "paper_only": True, "description": "keep_priority for leading theme", "theme_state": "leading", "expected_action": "keep_priority"},
    {"scenario_id": "SC207-034", "schema_version": "207", "paper_only": True, "description": "require_rescore for crowded theme", "theme_state": "crowded", "expected_action": "require_rescore"},
    {"scenario_id": "SC207-035", "schema_version": "207", "paper_only": True, "description": "freeze_new_candidates for overheating theme", "theme_state": "overheating", "expected_action": "freeze_new_candidates"},
    {"scenario_id": "SC207-036", "schema_version": "207", "paper_only": True, "description": "reduce_priority for weakening theme", "theme_state": "weakening", "expected_action": "reduce_priority"},
    {"scenario_id": "SC207-037", "schema_version": "207", "paper_only": True, "description": "downgrade_theme for cooling theme", "theme_state": "cooling", "expected_action": "downgrade_theme"},
    {"scenario_id": "SC207-038", "schema_version": "207", "paper_only": True, "description": "downgrade_theme for stale theme", "theme_state": "stale", "expected_action": "downgrade_theme"},
    {"scenario_id": "SC207-039", "schema_version": "207", "paper_only": True, "description": "human_review_required for risk_off theme", "theme_state": "risk_off", "expected_action": "human_review_required"},
    {"scenario_id": "SC207-040", "schema_version": "207", "paper_only": True, "description": "keep_priority for neutral theme", "theme_state": "neutral", "expected_action": "keep_priority"},
    # --- 41-50: candidate priority adjustment ---
    {"scenario_id": "SC207-041", "schema_version": "207", "paper_only": True, "description": "Promote priority: leading theme + uptrend market", "theme_state": "leading", "market_state": "strong_uptrend", "original_score": 70.0, "expected_priority_change": "promote_priority"},
    {"scenario_id": "SC207-042", "schema_version": "207", "paper_only": True, "description": "Keep priority: neutral theme + range_bound market", "theme_state": "neutral", "market_state": "range_bound", "original_score": 60.0, "expected_priority_change": "keep_priority"},
    {"scenario_id": "SC207-043", "schema_version": "207", "paper_only": True, "description": "Reduce priority: weakening theme + healthy_pullback", "theme_state": "weakening", "market_state": "healthy_pullback", "original_score": 60.0, "expected_priority_change": "reduce_priority"},
    {"scenario_id": "SC207-044", "schema_version": "207", "paper_only": True, "description": "Freeze candidate: downtrend market blocks promotion", "theme_state": "neutral", "market_state": "downtrend", "original_score": 65.0, "expected_priority_change": "freeze_candidate"},
    {"scenario_id": "SC207-045", "schema_version": "207", "paper_only": True, "description": "Freeze candidate: overheating theme blocks promotion", "theme_state": "overheating", "market_state": "range_bound", "original_score": 65.0, "expected_priority_change": "freeze_candidate"},
    {"scenario_id": "SC207-046", "schema_version": "207", "paper_only": True, "description": "Human review: risk_off theme triggers review", "theme_state": "risk_off", "market_state": "range_bound", "original_score": 60.0, "expected_priority_change": "human_review_required"},
    {"scenario_id": "SC207-047", "schema_version": "207", "paper_only": True, "description": "should_auto_apply always False on adjustment", "theme_state": "leading", "market_state": "strong_uptrend", "should_auto_apply": False},
    {"scenario_id": "SC207-048", "schema_version": "207", "paper_only": True, "description": "blocked_by_market_regime True when downtrend", "market_state": "downtrend", "expected_blocked_by_market": True},
    {"scenario_id": "SC207-049", "schema_version": "207", "paper_only": True, "description": "blocked_by_theme_state True when overheating", "theme_state": "overheating", "expected_blocked_by_theme": True},
    {"scenario_id": "SC207-050", "schema_version": "207", "paper_only": True, "description": "blocked_by_theme_state True when stale", "theme_state": "stale", "expected_blocked_by_theme": True},
    # --- 51-60: theme rotation review result ---
    {"scenario_id": "SC207-051", "schema_version": "207", "paper_only": True, "description": "Review result has theme_rotation_review_id"},
    {"scenario_id": "SC207-052", "schema_version": "207", "paper_only": True, "description": "Review result theme_rotation_version is 2.0.7"},
    {"scenario_id": "SC207-053", "schema_version": "207", "paper_only": True, "description": "Review result paper_only is True"},
    {"scenario_id": "SC207-054", "schema_version": "207", "paper_only": True, "description": "Review result should_auto_apply is False"},
    {"scenario_id": "SC207-055", "schema_version": "207", "paper_only": True, "description": "Review result all_passed is True"},
    {"scenario_id": "SC207-056", "schema_version": "207", "paper_only": True, "description": "Review result has non-empty theme_strength_snapshot"},
    {"scenario_id": "SC207-057", "schema_version": "207", "paper_only": True, "description": "Review result has market_regime_snapshot"},
    {"scenario_id": "SC207-058", "schema_version": "207", "paper_only": True, "description": "Review result has theme_rotation_summary"},
    {"scenario_id": "SC207-059", "schema_version": "207", "paper_only": True, "description": "Overheat snapshot lists overheating theme IDs only"},
    {"scenario_id": "SC207-060", "schema_version": "207", "paper_only": True, "description": "Weakening snapshot lists weakening/cooling theme IDs only"},
    # --- 61-70: export integration ---
    {"scenario_id": "SC207-061", "schema_version": "207", "paper_only": True, "description": "JSON export contains theme_rotation_review_id", "export_format": "json"},
    {"scenario_id": "SC207-062", "schema_version": "207", "paper_only": True, "description": "JSON export has paper_only=true", "export_format": "json"},
    {"scenario_id": "SC207-063", "schema_version": "207", "paper_only": True, "description": "JSON export has should_auto_apply=false", "export_format": "json"},
    {"scenario_id": "SC207-064", "schema_version": "207", "paper_only": True, "description": "Markdown report header present", "export_format": "markdown"},
    {"scenario_id": "SC207-065", "schema_version": "207", "paper_only": True, "description": "Markdown includes Paper Only disclaimer", "export_format": "markdown"},
    {"scenario_id": "SC207-066", "schema_version": "207", "paper_only": True, "description": "Theme strength CSV header correct", "export_format": "csv"},
    {"scenario_id": "SC207-067", "schema_version": "207", "paper_only": True, "description": "Market regime CSV has should_auto_apply=False", "export_format": "csv"},
    {"scenario_id": "SC207-068", "schema_version": "207", "paper_only": True, "description": "Priority adjustment CSV has rows", "export_format": "csv"},
    {"scenario_id": "SC207-069", "schema_version": "207", "paper_only": True, "description": "Audit snapshot reproducibility_hash set", "export_format": "audit_snapshot"},
    {"scenario_id": "SC207-070", "schema_version": "207", "paper_only": True, "description": "Audit snapshot safety_snapshot contains paper_only", "export_format": "audit_snapshot"},
    # --- 71-80: safety flags & backward compat ---
    {"scenario_id": "SC207-071", "schema_version": "207", "paper_only": True, "description": "SAFETY_FLAGS_V207 has 20 flags"},
    {"scenario_id": "SC207-072", "schema_version": "207", "paper_only": True, "description": "should_auto_apply_always_false flag is True"},
    {"scenario_id": "SC207-073", "schema_version": "207", "paper_only": True, "description": "MarketRegime.should_auto_apply is always False even if set True"},
    {"scenario_id": "SC207-074", "schema_version": "207", "paper_only": True, "description": "CandidatePriorityAdjustment.should_auto_apply always False"},
    {"scenario_id": "SC207-075", "schema_version": "207", "paper_only": True, "description": "ThemeRotationReviewResult.should_auto_apply always False"},
    {"scenario_id": "SC207-076", "schema_version": "207", "paper_only": True, "description": "NO_REAL_ORDERS is True"},
    {"scenario_id": "SC207-077", "schema_version": "207", "paper_only": True, "description": "BROKER_EXECUTION_ENABLED is False"},
    {"scenario_id": "SC207-078", "schema_version": "207", "paper_only": True, "description": "PRODUCTION_TRADING_BLOCKED is True"},
    {"scenario_id": "SC207-079", "schema_version": "207", "paper_only": True, "description": "v2.0.6 run_lifecycle_review still callable"},
    {"scenario_id": "SC207-080", "schema_version": "207", "paper_only": True, "description": "v2.0.5 run_watchlist_rotation still callable"},
]

assert len(SCENARIOS) == 80, f"Expected 80 scenarios, got {len(SCENARIOS)}"
assert all(s["schema_version"] == "207" for s in SCENARIOS)
assert all(s["paper_only"] is True for s in SCENARIOS)
