"""
paper_trading/small_capital_strategy/portfolio_governance_fixtures_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Fixtures
[!] Paper Only. Research Only. Simulation Only. Validation Only.
[!] No Real Orders. No Broker. No Margin. No Leverage.
[!] Not Investment Advice.
"""

_BASE = {
    "schema_version": "198",
    "paper_only": True,
    "research_only": True,
    "simulate_only": True,
    "validation_only": True,
    "portfolio_governance_only": True,
    "risk_overlay_only": True,
    "dashboard_only": True,
    "report_only": True,
    "audit_only": True,
    "no_real_orders": True,
    "no_broker": True,
    "no_margin": True,
    "no_leverage": True,
    "no_production_strategy_mutation": True,
    "no_automatic_rollback": True,
    "no_live_strategy_activation": True,
    "not_investment_advice": True,
    "demo_only": True,
    "not_for_production": True,
    "production_trading_blocked": True,
}

_FIXTURES = [
    {**_BASE, "id": "PGF198-001", "fixture_id": "PGF198-001", "name": "Valid portfolio governance input — all required fields present and valid", "expected_outcome": "input_accepted"},
    {**_BASE, "id": "PGF198-002", "fixture_id": "PGF198-002", "name": "Minimal governance input — positions empty list, risk_limits empty dict", "expected_outcome": "minimal_input_accepted"},
    {**_BASE, "id": "PGF198-003", "fixture_id": "PGF198-003", "name": "Portfolio snapshot — 5 positions, 10% cash buffer", "expected_outcome": "snapshot_valid"},
    {**_BASE, "id": "PGF198-004", "fixture_id": "PGF198-004", "name": "Portfolio snapshot — 0 positions, 100% cash buffer", "expected_outcome": "empty_snapshot_valid"},
    {**_BASE, "id": "PGF198-005", "fixture_id": "PGF198-005", "name": "Position — TSMC, semiconductor, LONG, weight 0.15", "expected_outcome": "position_valid"},
    {**_BASE, "id": "PGF198-006", "fixture_id": "PGF198-006", "name": "Position — AI chip stock, ai_supply_chain theme, weight 0.10", "expected_outcome": "ai_position_valid"},
    {**_BASE, "id": "PGF198-007", "fixture_id": "PGF198-007", "name": "Position — PCB maker, pcb theme, weight 0.08", "expected_outcome": "pcb_position_valid"},
    {**_BASE, "id": "PGF198-008", "fixture_id": "PGF198-008", "name": "Position — cooling equipment, cooling theme, weight 0.07", "expected_outcome": "cooling_position_valid"},
    {**_BASE, "id": "PGF198-009", "fixture_id": "PGF198-009", "name": "Position — power supply, power theme, weight 0.06", "expected_outcome": "power_position_valid"},
    {**_BASE, "id": "PGF198-010", "fixture_id": "PGF198-010", "name": "Position — ASIC designer, asic theme, weight 0.09", "expected_outcome": "asic_position_valid"},
    {**_BASE, "id": "PGF198-011", "fixture_id": "PGF198-011", "name": "Strategy exposure — abc_breakout, 3 positions, weight 0.25", "expected_outcome": "strategy_exposure_valid"},
    {**_BASE, "id": "PGF198-012", "fixture_id": "PGF198-012", "name": "Theme exposure — semiconductor, 4 positions, weight 0.35", "expected_outcome": "theme_exposure_valid"},
    {**_BASE, "id": "PGF198-013", "fixture_id": "PGF198-013", "name": "Industry exposure — electronic components, 2 positions, weight 0.18", "expected_outcome": "industry_exposure_valid"},
    {**_BASE, "id": "PGF198-014", "fixture_id": "PGF198-014", "name": "Market exposure — beta 0.8, tsmc_sensitivity 0.4, etf_overlap 0.2", "expected_outcome": "market_exposure_valid"},
    {**_BASE, "id": "PGF198-015", "fixture_id": "PGF198-015", "name": "Risk overlay — candidate paper_abc_001, portfolio at low risk 0.15", "expected_outcome": "overlay_passed"},
    {**_BASE, "id": "PGF198-016", "fixture_id": "PGF198-016", "name": "Risk overlay — portfolio at critical risk 0.9, overlay not passed", "expected_outcome": "overlay_not_passed"},
    {**_BASE, "id": "PGF198-017", "fixture_id": "PGF198-017", "name": "Risk limit — max_single_symbol_weight 0.20", "expected_outcome": "limit_valid"},
    {**_BASE, "id": "PGF198-018", "fixture_id": "PGF198-018", "name": "Risk limit — max_single_theme_weight 0.35", "expected_outcome": "limit_valid"},
    {**_BASE, "id": "PGF198-019", "fixture_id": "PGF198-019", "name": "Risk limit — max_ai_supply_chain_weight 0.40", "expected_outcome": "limit_valid"},
    {**_BASE, "id": "PGF198-020", "fixture_id": "PGF198-020", "name": "Risk limit — min_cash_buffer 0.05", "expected_outcome": "limit_valid"},
    {**_BASE, "id": "PGF198-021", "fixture_id": "PGF198-021", "name": "Risk limit result — not breached, current 0.10 vs limit 0.20", "expected_outcome": "limit_not_breached"},
    {**_BASE, "id": "PGF198-022", "fixture_id": "PGF198-022", "name": "Risk limit result — breached, current 0.25 vs limit 0.20", "expected_outcome": "limit_breached"},
    {**_BASE, "id": "PGF198-023", "fixture_id": "PGF198-023", "name": "Concentration risk — symbol weights all below 0.20, no breach", "expected_outcome": "no_breach"},
    {**_BASE, "id": "PGF198-024", "fixture_id": "PGF198-024", "name": "Concentration risk — one symbol at 0.40, breach detected", "expected_outcome": "breach_detected"},
    {**_BASE, "id": "PGF198-025", "fixture_id": "PGF198-025", "name": "Correlation risk — cluster weight 0.30, below threshold 0.50", "expected_outcome": "no_breach"},
    {**_BASE, "id": "PGF198-026", "fixture_id": "PGF198-026", "name": "Correlation risk — cluster weight 0.60, above threshold 0.50, breach", "expected_outcome": "breach_detected"},
    {**_BASE, "id": "PGF198-027", "fixture_id": "PGF198-027", "name": "Theme overlap — semiconductor and pcb overlap score 0.65", "expected_outcome": "overlap_detected"},
    {**_BASE, "id": "PGF198-028", "fixture_id": "PGF198-028", "name": "Theme overlap — cooling and power overlap score 0.20, low", "expected_outcome": "low_overlap"},
    {**_BASE, "id": "PGF198-029", "fixture_id": "PGF198-029", "name": "Decision overlap — two decisions in same semiconductor sub-theme", "expected_outcome": "duplicate_exposure"},
    {**_BASE, "id": "PGF198-030", "fixture_id": "PGF198-030", "name": "Exposure summary — 6 symbols, 3 themes, 2 industries, 2 strategies", "expected_outcome": "exposure_summary_valid"},
    {**_BASE, "id": "PGF198-031", "fixture_id": "PGF198-031", "name": "Risk score 0.0 — raw_score 0.0 returns score 0.0", "expected_outcome": "score_0.0"},
    {**_BASE, "id": "PGF198-032", "fixture_id": "PGF198-032", "name": "Risk score 0.5 — raw_score 0.5 returns score 0.5", "expected_outcome": "score_0.5"},
    {**_BASE, "id": "PGF198-033", "fixture_id": "PGF198-033", "name": "Risk score clamp — raw_score 1.5 clamped to 1.0", "expected_outcome": "score_clamped_1.0"},
    {**_BASE, "id": "PGF198-034", "fixture_id": "PGF198-034", "name": "Risk grade LOW — score 0.05", "expected_outcome": "grade_LOW"},
    {**_BASE, "id": "PGF198-035", "fixture_id": "PGF198-035", "name": "Risk grade MODERATE — score 0.25", "expected_outcome": "grade_MODERATE"},
    {**_BASE, "id": "PGF198-036", "fixture_id": "PGF198-036", "name": "Risk grade ELEVATED — score 0.55", "expected_outcome": "grade_ELEVATED"},
    {**_BASE, "id": "PGF198-037", "fixture_id": "PGF198-037", "name": "Risk grade HIGH — score 0.72", "expected_outcome": "grade_HIGH"},
    {**_BASE, "id": "PGF198-038", "fixture_id": "PGF198-038", "name": "Risk grade CRITICAL — score 0.88", "expected_outcome": "grade_CRITICAL"},
    {**_BASE, "id": "PGF198-039", "fixture_id": "PGF198-039", "name": "Risk recommendation NO_CHANGE for LOW grade", "expected_outcome": "rec_NO_CHANGE"},
    {**_BASE, "id": "PGF198-040", "fixture_id": "PGF198-040", "name": "Risk recommendation RISK_OFF_MODE for CRITICAL grade", "expected_outcome": "rec_RISK_OFF_MODE"},
    {**_BASE, "id": "PGF198-041", "fixture_id": "PGF198-041", "name": "Risk block — candidate blocked due to high portfolio risk", "expected_outcome": "candidate_blocked"},
    {**_BASE, "id": "PGF198-042", "fixture_id": "PGF198-042", "name": "Governance decision — KEEP_SHADOW_ONLY outcome recorded", "expected_outcome": "decision_recorded"},
    {**_BASE, "id": "PGF198-043", "fixture_id": "PGF198-043", "name": "Dashboard — 4 panels rendered, dashboard_mutates_strategy False", "expected_outcome": "dashboard_valid"},
    {**_BASE, "id": "PGF198-044", "fixture_id": "PGF198-044", "name": "Report — 5 sections built, report_triggers_rebalance False", "expected_outcome": "report_valid"},
    {**_BASE, "id": "PGF198-045", "fixture_id": "PGF198-045", "name": "Audit trail entry — event_type GOVERNANCE_RUN, immutable True", "expected_outcome": "audit_immutable"},
    {**_BASE, "id": "PGF198-046", "fixture_id": "PGF198-046", "name": "Health summary — all_passed True, 65 passed, 0 failed", "expected_outcome": "health_all_pass"},
    {**_BASE, "id": "PGF198-047", "fixture_id": "PGF198-047", "name": "Validation result — valid True, no errors, no warnings", "expected_outcome": "validation_clean"},
    {**_BASE, "id": "PGF198-048", "fixture_id": "PGF198-048", "name": "Validation result — valid False, one error present", "expected_outcome": "validation_error"},
    {**_BASE, "id": "PGF198-049", "fixture_id": "PGF198-049", "name": "Full governance pack — all 12 sections present", "expected_outcome": "pack_complete"},
    {**_BASE, "id": "PGF198-050", "fixture_id": "PGF198-050", "name": "Full governance pack — paper_only True in all sections", "expected_outcome": "pack_paper_only"},
    {**_BASE, "id": "PGF198-051", "fixture_id": "PGF198-051", "name": "Malformed input — None type blocked immediately", "expected_outcome": "blocked"},
    {**_BASE, "id": "PGF198-052", "fixture_id": "PGF198-052", "name": "Malformed input — list type blocked immediately", "expected_outcome": "blocked"},
    {**_BASE, "id": "PGF198-053", "fixture_id": "PGF198-053", "name": "Missing paper_only flag — input blocked", "expected_outcome": "blocked_no_paper"},
    {**_BASE, "id": "PGF198-054", "fixture_id": "PGF198-054", "name": "Missing no_broker flag — input blocked", "expected_outcome": "blocked_no_broker"},
    {**_BASE, "id": "PGF198-055", "fixture_id": "PGF198-055", "name": "Missing positions key — input blocked", "expected_outcome": "blocked_no_positions"},
    {**_BASE, "id": "PGF198-056", "fixture_id": "PGF198-056", "name": "Missing snapshot key — input blocked", "expected_outcome": "blocked_no_snapshot"},
    {**_BASE, "id": "PGF198-057", "fixture_id": "PGF198-057", "name": "Missing risk_limits key — input blocked", "expected_outcome": "blocked_no_risk_limits"},
    {**_BASE, "id": "PGF198-058", "fixture_id": "PGF198-058", "name": "Forbidden word BUY in input — blocked", "expected_outcome": "blocked_forbidden_word_BUY"},
    {**_BASE, "id": "PGF198-059", "fixture_id": "PGF198-059", "name": "Forbidden word SELL in input — blocked", "expected_outcome": "blocked_forbidden_word_SELL"},
    {**_BASE, "id": "PGF198-060", "fixture_id": "PGF198-060", "name": "Forbidden word ORDER in candidate — overlay blocked", "expected_outcome": "blocked_forbidden_word_ORDER"},
    {**_BASE, "id": "PGF198-061", "fixture_id": "PGF198-061", "name": "Export with safe path paper_export/test.json — exported True", "expected_outcome": "exported_safe"},
    {**_BASE, "id": "PGF198-062", "fixture_id": "PGF198-062", "name": "Export with path containing .. — blocked unsafe", "expected_outcome": "blocked_dotdot"},
    {**_BASE, "id": "PGF198-063", "fixture_id": "PGF198-063", "name": "Export with path containing live — blocked unsafe", "expected_outcome": "blocked_live_path"},
    {**_BASE, "id": "PGF198-064", "fixture_id": "PGF198-064", "name": "assert_safe with allowed action run_portfolio_governance — returns True", "expected_outcome": "safe_allowed"},
    {**_BASE, "id": "PGF198-065", "fixture_id": "PGF198-065", "name": "assert_safe with forbidden action place_real_order — raises ValueError", "expected_outcome": "raises_ValueError"},
    {**_BASE, "id": "PGF198-066", "fixture_id": "PGF198-066", "name": "assert_safe with forbidden action submit_broker_order — raises ValueError", "expected_outcome": "raises_ValueError"},
    {**_BASE, "id": "PGF198-067", "fixture_id": "PGF198-067", "name": "All SAFETY_FLAGS true flags are True", "expected_outcome": "all_true_flags_correct"},
    {**_BASE, "id": "PGF198-068", "fixture_id": "PGF198-068", "name": "All SAFETY_FLAGS false flags are False", "expected_outcome": "all_false_flags_correct"},
    {**_BASE, "id": "PGF198-069", "fixture_id": "PGF198-069", "name": "FORBIDDEN_ACTIONS has 15 entries", "expected_outcome": "forbidden_actions_count_15"},
    {**_BASE, "id": "PGF198-070", "fixture_id": "PGF198-070", "name": "ALLOWED_ACTIONS has 20 entries", "expected_outcome": "allowed_actions_count_20"},
    {**_BASE, "id": "PGF198-071", "fixture_id": "PGF198-071", "name": "GUI tab count >= 163 in panel info", "expected_outcome": "gui_tab_count_ok"},
    {**_BASE, "id": "PGF198-072", "fixture_id": "PGF198-072", "name": "GUI render_all_tabs returns no error key for governance tabs", "expected_outcome": "gui_all_tabs_no_error"},
    {**_BASE, "id": "PGF198-073", "fixture_id": "PGF198-073", "name": "CLI 19 commands all have group strategy_governance_portfolio or portfolio_governance", "expected_outcome": "cli_group_ok"},
    {**_BASE, "id": "PGF198-074", "fixture_id": "PGF198-074", "name": "CLI all 19 handlers are callable", "expected_outcome": "cli_handlers_callable"},
    {**_BASE, "id": "PGF198-075", "fixture_id": "PGF198-075", "name": "End-to-end: valid input → exposure summary → risk score → grade → recommendations → report", "expected_outcome": "end_to_end_fixture"},
]

assert len(_FIXTURES) == 75


def get_fixtures() -> list:
    return list(_FIXTURES)


def get_fixture_by_id(fid: str) -> dict:
    for f in _FIXTURES:
        if f["fixture_id"] == fid:
            return f
    return {}
