"""
paper_trading/small_capital_strategy/portfolio_governance_scenarios_v198.py
v1.9.8 Paper Portfolio Governance & Risk Overlay Lab — Scenarios
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

_SCENARIOS = [
    {**_BASE, "id": "PG198-001", "scenario_id": "PG198-001", "name": "Complete portfolio governance snapshot — all positions, exposure, risk limits present", "expected_outcome": "governance_passed"},
    {**_BASE, "id": "PG198-002", "scenario_id": "PG198-002", "name": "Low risk diversified portfolio — all themes balanced, no concentration", "expected_outcome": "risk_grade_LOW"},
    {**_BASE, "id": "PG198-003", "scenario_id": "PG198-003", "name": "Single symbol concentration risk — one symbol exceeds max weight limit", "expected_outcome": "concentration_risk_breach"},
    {**_BASE, "id": "PG198-004", "scenario_id": "PG198-004", "name": "AI supply chain concentration risk — ai_supply_chain_exposure exceeds limit", "expected_outcome": "theme_breach_ai_supply_chain"},
    {**_BASE, "id": "PG198-005", "scenario_id": "PG198-005", "name": "Semiconductor concentration risk — semiconductor_exposure exceeds max limit", "expected_outcome": "theme_breach_semiconductor"},
    {**_BASE, "id": "PG198-006", "scenario_id": "PG198-006", "name": "PCB theme concentration risk — pcb_exposure exceeds allowed threshold", "expected_outcome": "theme_breach_pcb"},
    {**_BASE, "id": "PG198-007", "scenario_id": "PG198-007", "name": "Cooling theme concentration risk — cooling_exposure exceeds allowed threshold", "expected_outcome": "theme_breach_cooling"},
    {**_BASE, "id": "PG198-008", "scenario_id": "PG198-008", "name": "Power theme concentration risk — power_exposure exceeds limit", "expected_outcome": "theme_breach_power"},
    {**_BASE, "id": "PG198-009", "scenario_id": "PG198-009", "name": "ASIC theme concentration risk — asic_exposure exceeds limit", "expected_outcome": "theme_breach_asic"},
    {**_BASE, "id": "PG198-010", "scenario_id": "PG198-010", "name": "High correlation cluster risk — multiple correlated positions exceed cluster weight", "expected_outcome": "correlation_risk_breach"},
    {**_BASE, "id": "PG198-011", "scenario_id": "PG198-011", "name": "High TSMC sensitivity risk — tsmc_sensitivity exceeds max limit", "expected_outcome": "market_risk_tsmc_breach"},
    {**_BASE, "id": "PG198-012", "scenario_id": "PG198-012", "name": "High ETF overlap risk — etf_overlap exceeds threshold", "expected_outcome": "market_risk_etf_breach"},
    {**_BASE, "id": "PG198-013", "scenario_id": "PG198-013", "name": "Market beta too high — taiwan_index_beta exceeds max_market_beta limit", "expected_outcome": "market_beta_breach"},
    {**_BASE, "id": "PG198-014", "scenario_id": "PG198-014", "name": "Cash buffer too low — cash_buffer below min_cash_buffer requirement", "expected_outcome": "cash_buffer_breach"},
    {**_BASE, "id": "PG198-015", "scenario_id": "PG198-015", "name": "Drawdown budget exceeded — total drawdown exceeds max_drawdown_budget", "expected_outcome": "drawdown_breach"},
    {**_BASE, "id": "PG198-016", "scenario_id": "PG198-016", "name": "Foreign futures risk high — foreign_futures_risk exceeds acceptable level", "expected_outcome": "foreign_futures_breach"},
    {**_BASE, "id": "PG198-017", "scenario_id": "PG198-017", "name": "Candidate blocked by portfolio overlay — risk score too high for new candidate", "expected_outcome": "overlay_blocked"},
    {**_BASE, "id": "PG198-018", "scenario_id": "PG198-018", "name": "Candidate keep shadow only — risk elevated, candidate stays in shadow mode", "expected_outcome": "recommendation_KEEP_SHADOW_ONLY"},
    {**_BASE, "id": "PG198-019", "scenario_id": "PG198-019", "name": "Malformed portfolio input blocked — non-dict input triggers hard block", "expected_outcome": "blocked_malformed_input"},
    {**_BASE, "id": "PG198-020", "scenario_id": "PG198-020", "name": "Unsafe export path blocked — path contains production keyword", "expected_outcome": "blocked_unsafe_export"},
    {**_BASE, "id": "PG198-021", "scenario_id": "PG198-021", "name": "Production mutation blocked — overlay_tries_to_mutate_strategy flag triggers block", "expected_outcome": "blocked_production_mutation"},
    {**_BASE, "id": "PG198-022", "scenario_id": "PG198-022", "name": "Live activation blocked — live_strategy_activation flag triggers block", "expected_outcome": "blocked_live_activation"},
    {**_BASE, "id": "PG198-023", "scenario_id": "PG198-023", "name": "Broker request blocked — broker flag triggers hard block", "expected_outcome": "blocked_broker_request"},
    {**_BASE, "id": "PG198-024", "scenario_id": "PG198-024", "name": "Real rebalance blocked — overlay_tries_to_rebalance_real_portfolio triggers block", "expected_outcome": "blocked_real_rebalance"},
    {**_BASE, "id": "PG198-025", "scenario_id": "PG198-025", "name": "Complete portfolio governance report — all 12 sections present and valid", "expected_outcome": "report_complete_12_sections"},
    {**_BASE, "id": "PG198-026", "scenario_id": "PG198-026", "name": "Exposure summary computed from 5 diverse positions — all dimensions counted", "expected_outcome": "exposure_summary_valid"},
    {**_BASE, "id": "PG198-027", "scenario_id": "PG198-027", "name": "Risk limit evaluation — all 14 limit keys evaluated against portfolio", "expected_outcome": "all_limits_evaluated"},
    {**_BASE, "id": "PG198-028", "scenario_id": "PG198-028", "name": "Concentration check — symbol weight dict with no breaches returns any_breach False", "expected_outcome": "no_concentration_breach"},
    {**_BASE, "id": "PG198-029", "scenario_id": "PG198-029", "name": "Concentration check — symbol weight dict with one breach returns any_breach True", "expected_outcome": "concentration_breach_detected"},
    {**_BASE, "id": "PG198-030", "scenario_id": "PG198-030", "name": "Correlation check — cluster with low weight returns any_breach False", "expected_outcome": "no_correlation_breach"},
    {**_BASE, "id": "PG198-031", "scenario_id": "PG198-031", "name": "Correlation check — cluster with high weight returns any_breach True", "expected_outcome": "correlation_breach_detected"},
    {**_BASE, "id": "PG198-032", "scenario_id": "PG198-032", "name": "Theme overlap — two overlapping themes detected with high overlap score", "expected_outcome": "theme_overlap_detected"},
    {**_BASE, "id": "PG198-033", "scenario_id": "PG198-033", "name": "Decision overlap — two decisions with same exposure detected as duplicate", "expected_outcome": "decision_overlap_detected"},
    {**_BASE, "id": "PG198-034", "scenario_id": "PG198-034", "name": "Audit trail entry created — event_type and detail captured immutably", "expected_outcome": "audit_trail_immutable"},
    {**_BASE, "id": "PG198-035", "scenario_id": "PG198-035", "name": "Health check — all checks pass, status is PASS", "expected_outcome": "health_all_passed"},
    {**_BASE, "id": "PG198-036", "scenario_id": "PG198-036", "name": "Release gate — all checks pass, gate_passed True", "expected_outcome": "gate_passed"},
    {**_BASE, "id": "PG198-037", "scenario_id": "PG198-037", "name": "Safety audit — all_safe True, failed 0", "expected_outcome": "safety_audit_clean"},
    {**_BASE, "id": "PG198-038", "scenario_id": "PG198-038", "name": "Version verification — VERSION is 1.9.8, SCHEMA_VERSION is 198", "expected_outcome": "version_verified"},
    {**_BASE, "id": "PG198-039", "scenario_id": "PG198-039", "name": "Model validation — all 26 models have schema_version=198", "expected_outcome": "all_models_valid"},
    {**_BASE, "id": "PG198-040", "scenario_id": "PG198-040", "name": "Model validation — all models with no_real_orders field have it True", "expected_outcome": "no_real_orders_all_models"},
    {**_BASE, "id": "PG198-041", "scenario_id": "PG198-041", "name": "Risk grade LOW — score 0.0 returns grade LOW", "expected_outcome": "grade_LOW"},
    {**_BASE, "id": "PG198-042", "scenario_id": "PG198-042", "name": "Risk grade LOW boundary — score 0.19 returns grade LOW", "expected_outcome": "grade_LOW_boundary"},
    {**_BASE, "id": "PG198-043", "scenario_id": "PG198-043", "name": "Risk grade MODERATE — score 0.3 returns grade MODERATE", "expected_outcome": "grade_MODERATE"},
    {**_BASE, "id": "PG198-044", "scenario_id": "PG198-044", "name": "Risk grade ELEVATED — score 0.5 returns grade ELEVATED", "expected_outcome": "grade_ELEVATED"},
    {**_BASE, "id": "PG198-045", "scenario_id": "PG198-045", "name": "Risk grade HIGH — score 0.7 returns grade HIGH", "expected_outcome": "grade_HIGH"},
    {**_BASE, "id": "PG198-046", "scenario_id": "PG198-046", "name": "Risk grade CRITICAL — score 0.9 returns grade CRITICAL", "expected_outcome": "grade_CRITICAL"},
    {**_BASE, "id": "PG198-047", "scenario_id": "PG198-047", "name": "Risk grade INVALID — negative score returns INVALID", "expected_outcome": "grade_INVALID"},
    {**_BASE, "id": "PG198-048", "scenario_id": "PG198-048", "name": "Recommendations for LOW grade — returns NO_CHANGE", "expected_outcome": "rec_NO_CHANGE"},
    {**_BASE, "id": "PG198-049", "scenario_id": "PG198-049", "name": "Recommendations for MODERATE grade — returns REQUIRE_MORE_EVIDENCE", "expected_outcome": "rec_REQUIRE_MORE_EVIDENCE"},
    {**_BASE, "id": "PG198-050", "scenario_id": "PG198-050", "name": "Recommendations for ELEVATED grade — returns REDUCE_POSITION_SIZE", "expected_outcome": "rec_REDUCE_POSITION_SIZE"},
    {**_BASE, "id": "PG198-051", "scenario_id": "PG198-051", "name": "Recommendations for HIGH grade — returns RISK_OFF_MODE and REQUIRE_HUMAN_REVIEW", "expected_outcome": "rec_RISK_OFF_MODE"},
    {**_BASE, "id": "PG198-052", "scenario_id": "PG198-052", "name": "Recommendations for CRITICAL grade — returns RISK_OFF_MODE and REQUIRE_HUMAN_REVIEW", "expected_outcome": "rec_CRITICAL_RISK_OFF"},
    {**_BASE, "id": "PG198-053", "scenario_id": "PG198-053", "name": "Theme breach adds REDUCE_THEME_EXPOSURE to recommendations", "expected_outcome": "rec_REDUCE_THEME_EXPOSURE"},
    {**_BASE, "id": "PG198-054", "scenario_id": "PG198-054", "name": "Industry breach adds REDUCE_INDUSTRY_EXPOSURE to recommendations", "expected_outcome": "rec_REDUCE_INDUSTRY_EXPOSURE"},
    {**_BASE, "id": "PG198-055", "scenario_id": "PG198-055", "name": "Candidate count breach adds BLOCK_NEW_CANDIDATE to recommendations", "expected_outcome": "rec_BLOCK_NEW_CANDIDATE"},
    {**_BASE, "id": "PG198-056", "scenario_id": "PG198-056", "name": "Dashboard built from valid snapshot — panel_count is 4", "expected_outcome": "dashboard_built"},
    {**_BASE, "id": "PG198-057", "scenario_id": "PG198-057", "name": "Dashboard dashboard_mutates_strategy is False always", "expected_outcome": "dashboard_no_mutation"},
    {**_BASE, "id": "PG198-058", "scenario_id": "PG198-058", "name": "Report built from dashboard — section_count is 5", "expected_outcome": "report_built"},
    {**_BASE, "id": "PG198-059", "scenario_id": "PG198-059", "name": "Report report_triggers_rebalance is False always", "expected_outcome": "report_no_rebalance"},
    {**_BASE, "id": "PG198-060", "scenario_id": "PG198-060", "name": "Export governance pack with safe path — exported True", "expected_outcome": "export_safe_path"},
    {**_BASE, "id": "PG198-061", "scenario_id": "PG198-061", "name": "Export governance pack with unsafe path — blocked unsafe_export_path", "expected_outcome": "export_blocked_unsafe"},
    {**_BASE, "id": "PG198-062", "scenario_id": "PG198-062", "name": "Export governance pack with production path — blocked", "expected_outcome": "export_blocked_production_path"},
    {**_BASE, "id": "PG198-063", "scenario_id": "PG198-063", "name": "Forbidden output word in candidate triggers overlay block", "expected_outcome": "overlay_blocked_forbidden_word"},
    {**_BASE, "id": "PG198-064", "scenario_id": "PG198-064", "name": "Missing paper_only in overlay portfolio triggers block", "expected_outcome": "overlay_blocked_no_paper_flag"},
    {**_BASE, "id": "PG198-065", "scenario_id": "PG198-065", "name": "Risk overlay passes with low risk score (0.1)", "expected_outcome": "overlay_passed_low_risk"},
    {**_BASE, "id": "PG198-066", "scenario_id": "PG198-066", "name": "Risk overlay blocked with high risk score (0.9)", "expected_outcome": "overlay_not_passed_high_risk"},
    {**_BASE, "id": "PG198-067", "scenario_id": "PG198-067", "name": "GUI panel renders portfolio_governance tab with paper_only True", "expected_outcome": "gui_portfolio_governance_tab"},
    {**_BASE, "id": "PG198-068", "scenario_id": "PG198-068", "name": "GUI panel renders risk_overlay tab with risk_overlay_only True", "expected_outcome": "gui_risk_overlay_tab"},
    {**_BASE, "id": "PG198-069", "scenario_id": "PG198-069", "name": "GUI panel renders exposure_dashboard tab with exposure_dashboard_only True", "expected_outcome": "gui_exposure_dashboard_tab"},
    {**_BASE, "id": "PG198-070", "scenario_id": "PG198-070", "name": "CLI command portfolio-governance-version returns version info", "expected_outcome": "cli_version_command"},
    {**_BASE, "id": "PG198-071", "scenario_id": "PG198-071", "name": "CLI command portfolio-governance-health returns health result", "expected_outcome": "cli_health_command"},
    {**_BASE, "id": "PG198-072", "scenario_id": "PG198-072", "name": "CLI command portfolio-governance-gate returns gate result", "expected_outcome": "cli_gate_command"},
    {**_BASE, "id": "PG198-073", "scenario_id": "PG198-073", "name": "CLI command portfolio-governance-safety-audit returns safety result", "expected_outcome": "cli_safety_audit_command"},
    {**_BASE, "id": "PG198-074", "scenario_id": "PG198-074", "name": "All 19 CLI commands have introduced_in 1.9.8 and safety_classification RESEARCH_ONLY", "expected_outcome": "cli_all_19_commands_safe"},
    {**_BASE, "id": "PG198-075", "scenario_id": "PG198-075", "name": "Full end-to-end governance pipeline — input to report with all sections and audit trail", "expected_outcome": "end_to_end_governance_complete"},
]

assert len(_SCENARIOS) == 75


def get_scenarios() -> list:
    return list(_SCENARIOS)


def get_scenario_by_id(sid: str) -> dict:
    for s in _SCENARIOS:
        if s["scenario_id"] == sid:
            return s
    return {}
