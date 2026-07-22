"""
paper_trading/small_capital_strategy/paper_cockpit_fixtures_v208.py
v2.0.8 Paper Portfolio Exposure & Theme Concentration Risk Control — Fixtures
[!] Paper Only. Research Only. Not Investment Advice.
"""
from __future__ import annotations
from typing import Any, Dict, List

SCHEMA_VERSION = "208"

FIXTURES: List[Dict[str, Any]] = [
    # --- 1-10: exposure item fixtures (theme type) ---
    {"fixture_id": "FX208-001", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-SEMI", "exposure_name": "半導體", "candidate_count": 4, "total_candidates": 8, "cap_limit": 0.40, "expected_concentration_score": 50.0, "expected_over_limit": False, "expected_warning_level": "medium"},
    {"fixture_id": "FX208-002", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-AI", "exposure_name": "人工智慧", "candidate_count": 5, "total_candidates": 8, "cap_limit": 0.40, "expected_concentration_score": 62.5, "expected_over_limit": True, "expected_warning_level": "high"},
    {"fixture_id": "FX208-003", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-EV", "exposure_name": "電動車", "candidate_count": 2, "total_candidates": 10, "cap_limit": 0.40, "expected_concentration_score": 20.0, "expected_over_limit": False, "expected_warning_level": "none"},
    {"fixture_id": "FX208-004", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-CLOUD", "exposure_name": "雲端運算", "candidate_count": 8, "total_candidates": 10, "cap_limit": 0.40, "expected_over_limit": True, "expected_warning_level": "critical"},
    {"fixture_id": "FX208-005", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-SOLAR", "exposure_name": "太陽能", "candidate_count": 1, "total_candidates": 10, "cap_limit": 0.40, "expected_over_limit": False, "expected_warning_level": "none"},
    {"fixture_id": "FX208-006", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-BIOTECH", "exposure_name": "生技", "candidate_count": 3, "total_candidates": 8, "cap_limit": 0.40, "expected_concentration_score": 37.5, "expected_warning_level": "low"},
    {"fixture_id": "FX208-007", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-ROBOT", "exposure_name": "機器人", "candidate_count": 0, "total_candidates": 10, "cap_limit": 0.40, "expected_concentration_score": 0.0, "expected_warning_level": "none"},
    {"fixture_id": "FX208-008", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-FIN", "exposure_name": "金融", "candidate_count": 4, "total_candidates": 10, "cap_limit": 0.40, "expected_warning_level": "low"},
    {"fixture_id": "FX208-009", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-STEEL", "exposure_name": "鋼鐵", "candidate_count": 6, "total_candidates": 10, "cap_limit": 0.40, "expected_over_limit": True},
    {"fixture_id": "FX208-010", "schema_version": "208", "paper_only": True, "exposure_type": "theme", "exposure_group": "THEME-REIT", "exposure_name": "不動產", "candidate_count": 1, "total_candidates": 12, "cap_limit": 0.40, "expected_warning_level": "none"},
    # --- 11-20: sector concentration fixtures ---
    {"fixture_id": "FX208-011", "schema_version": "208", "paper_only": True, "exposure_type": "sector", "exposure_group": "SECTOR-TECH", "exposure_name": "科技業", "candidate_count": 6, "total_candidates": 8, "cap_limit": 0.45, "expected_over_limit": True, "expected_warning_level": "critical"},
    {"fixture_id": "FX208-012", "schema_version": "208", "paper_only": True, "exposure_type": "sector", "exposure_group": "SECTOR-FIN", "exposure_name": "金融業", "candidate_count": 2, "total_candidates": 10, "cap_limit": 0.45, "expected_over_limit": False},
    {"fixture_id": "FX208-013", "schema_version": "208", "paper_only": True, "exposure_type": "sector", "exposure_group": "SECTOR-ELEC", "exposure_name": "電子零組件", "candidate_count": 3, "total_candidates": 10, "cap_limit": 0.45, "expected_warning_level": "low"},
    {"fixture_id": "FX208-014", "schema_version": "208", "paper_only": True, "exposure_type": "sector", "exposure_group": "SECTOR-MFGR", "exposure_name": "製造業", "candidate_count": 4, "total_candidates": 10, "cap_limit": 0.45, "expected_warning_level": "low"},
    {"fixture_id": "FX208-015", "schema_version": "208", "paper_only": True, "exposure_type": "sector", "exposure_group": "SECTOR-CHEM", "exposure_name": "化工業", "candidate_count": 5, "total_candidates": 10, "cap_limit": 0.45, "expected_warning_level": "medium"},
    # --- 16-20: style concentration fixtures ---
    {"fixture_id": "FX208-016", "schema_version": "208", "paper_only": True, "exposure_type": "style", "exposure_group": "STYLE-GROWTH", "exposure_name": "成長型", "candidate_count": 7, "total_candidates": 10, "cap_limit": 0.50, "expected_warning_level": "high"},
    {"fixture_id": "FX208-017", "schema_version": "208", "paper_only": True, "exposure_type": "style", "exposure_group": "STYLE-VALUE", "exposure_name": "價值型", "candidate_count": 2, "total_candidates": 10, "cap_limit": 0.50, "expected_warning_level": "none"},
    {"fixture_id": "FX208-018", "schema_version": "208", "paper_only": True, "exposure_type": "style", "exposure_group": "STYLE-MOMENTUM", "exposure_name": "動能型", "candidate_count": 5, "total_candidates": 10, "cap_limit": 0.50, "expected_warning_level": "medium"},
    {"fixture_id": "FX208-019", "schema_version": "208", "paper_only": True, "exposure_type": "style", "exposure_group": "STYLE-INCOME", "exposure_name": "收益型", "candidate_count": 6, "total_candidates": 10, "cap_limit": 0.50, "expected_warning_level": "high"},
    {"fixture_id": "FX208-020", "schema_version": "208", "paper_only": True, "exposure_type": "style", "exposure_group": "STYLE-GROWTH", "exposure_name": "成長型", "candidate_count": 10, "total_candidates": 10, "cap_limit": 0.50, "expected_over_limit": True, "expected_warning_level": "critical"},
    # --- 21-30: volatility and liquidity fixtures ---
    {"fixture_id": "FX208-021", "schema_version": "208", "paper_only": True, "exposure_type": "volatility", "high_volatility_count": 2, "total_candidates": 10, "cap_limit": 0.30, "expected_over_limit": False, "expected_warning_level": "none"},
    {"fixture_id": "FX208-022", "schema_version": "208", "paper_only": True, "exposure_type": "volatility", "high_volatility_count": 4, "total_candidates": 10, "cap_limit": 0.30, "expected_warning_level": "medium"},
    {"fixture_id": "FX208-023", "schema_version": "208", "paper_only": True, "exposure_type": "volatility", "high_volatility_count": 5, "total_candidates": 10, "cap_limit": 0.30, "expected_over_limit": True},
    {"fixture_id": "FX208-024", "schema_version": "208", "paper_only": True, "exposure_type": "liquidity", "low_liquidity_count": 1, "total_candidates": 10, "cap_limit": 0.20, "expected_over_limit": False, "expected_warning_level": "none"},
    {"fixture_id": "FX208-025", "schema_version": "208", "paper_only": True, "exposure_type": "liquidity", "low_liquidity_count": 3, "total_candidates": 10, "cap_limit": 0.20, "expected_over_limit": True},
    {"fixture_id": "FX208-026", "schema_version": "208", "paper_only": True, "exposure_type": "liquidity", "low_liquidity_count": 2, "total_candidates": 10, "cap_limit": 0.20, "expected_warning_level": "medium"},
    {"fixture_id": "FX208-027", "schema_version": "208", "paper_only": True, "exposure_type": "market_regime", "risk_off_count": 1, "overheating_count": 0, "total_candidates": 10, "cap_limit": 0.10, "expected_over_limit": True},
    {"fixture_id": "FX208-028", "schema_version": "208", "paper_only": True, "exposure_type": "market_regime", "risk_off_count": 0, "overheating_count": 0, "total_candidates": 10, "cap_limit": 0.10, "expected_over_limit": False},
    {"fixture_id": "FX208-029", "schema_version": "208", "paper_only": True, "exposure_type": "candidate_pool", "dominant_count": 4, "total_candidates": 8, "cap_limit": 0.40, "expected_over_limit": True},
    {"fixture_id": "FX208-030", "schema_version": "208", "paper_only": True, "exposure_type": "promotion_queue", "dominant_in_queue": 3, "total_in_queue": 10, "cap_limit": 0.35, "expected_over_limit": False},
    # --- 31-40: risk cap policy fixtures ---
    {"fixture_id": "FX208-031", "schema_version": "208", "paper_only": True, "policy_id": "default-policy-v208", "auto_apply_enabled": False, "max_single_theme_weight": 0.40},
    {"fixture_id": "FX208-032", "schema_version": "208", "paper_only": True, "policy_id": "conservative-policy", "max_single_theme_weight": 0.30, "max_single_sector_weight": 0.35, "auto_apply_enabled": False},
    {"fixture_id": "FX208-033", "schema_version": "208", "paper_only": True, "auto_apply_enabled_forced_false": True},
    {"fixture_id": "FX208-034", "schema_version": "208", "paper_only": True, "max_high_volatility_weight": 0.30, "max_low_liquidity_weight": 0.20},
    {"fixture_id": "FX208-035", "schema_version": "208", "paper_only": True, "max_risk_off_exposure": 0.10, "max_overheating_theme_exposure": 0.25},
    {"fixture_id": "FX208-036", "schema_version": "208", "paper_only": True, "require_human_review_above_warning_level": "high"},
    {"fixture_id": "FX208-037", "schema_version": "208", "paper_only": True, "max_promotion_queue_single_theme_weight": 0.35},
    {"fixture_id": "FX208-038", "schema_version": "208", "paper_only": True, "policy_fields_count": 11},
    {"fixture_id": "FX208-039", "schema_version": "208", "paper_only": True, "policy_id": "strict-policy", "max_single_theme_weight": 0.25, "auto_apply_enabled": False},
    {"fixture_id": "FX208-040", "schema_version": "208", "paper_only": True, "policy_id": "test-policy-always-false", "auto_apply_enabled": False, "should_auto_apply": False},
    # --- 41-50: candidate exposure adjustment fixtures ---
    {"fixture_id": "FX208-041", "schema_version": "208", "paper_only": True, "symbol": "2330", "name": "台積電", "candidate_id": "CAND-2330", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "original_priority_score": 80.0, "theme_concentration_score": 75.0, "expected_theme_penalty": 10.0, "should_auto_apply": False},
    {"fixture_id": "FX208-042", "schema_version": "208", "paper_only": True, "symbol": "2454", "name": "聯發科", "candidate_id": "CAND-2454", "theme_id": "THEME-AI", "sector_id": "SECTOR-TECH", "original_priority_score": 75.0, "theme_concentration_score": 92.0, "expected_theme_penalty": 15.0, "should_auto_apply": False},
    {"fixture_id": "FX208-043", "schema_version": "208", "paper_only": True, "symbol": "2317", "name": "鴻海", "candidate_id": "CAND-2317", "theme_id": "THEME-EV", "sector_id": "SECTOR-MFGR", "original_priority_score": 58.0, "theme_concentration_score": 20.0, "expected_theme_penalty": 0.0, "should_auto_apply": False},
    {"fixture_id": "FX208-044", "schema_version": "208", "paper_only": True, "symbol": "2308", "name": "台達電", "candidate_id": "CAND-2308", "is_high_volatility": True, "original_priority_score": 62.0, "expected_volatility_penalty": 8.0, "should_auto_apply": False},
    {"fixture_id": "FX208-045", "schema_version": "208", "paper_only": True, "symbol": "2303", "name": "聯電", "candidate_id": "CAND-2303", "is_low_liquidity": True, "original_priority_score": 65.0, "expected_liquidity_penalty": 10.0, "should_auto_apply": False},
    {"fixture_id": "FX208-046", "schema_version": "208", "paper_only": True, "symbol": "2409", "name": "友達", "candidate_id": "CAND-2409", "market_state": "downtrend", "original_priority_score": 55.0, "expected_market_regime_penalty": 15.0, "should_auto_apply": False},
    {"fixture_id": "FX208-047", "schema_version": "208", "paper_only": True, "symbol": "2382", "name": "廣達", "candidate_id": "CAND-2382", "blocked_by_exposure_cap": True, "original_priority_score": 70.0, "expected_requires_human_review": True, "should_auto_apply": False},
    {"fixture_id": "FX208-048", "schema_version": "208", "paper_only": True, "symbol": "6669", "name": "緯穎", "candidate_id": "CAND-6669", "market_state": "risk_off", "original_priority_score": 70.0, "expected_requires_human_review": True, "should_auto_apply": False},
    {"fixture_id": "FX208-049", "schema_version": "208", "paper_only": True, "symbol": "3711", "name": "日月光", "candidate_id": "CAND-3711", "theme_id": "THEME-SEMI", "sector_id": "SECTOR-TECH", "original_priority_score": 72.0, "sector_concentration_score": 90.0, "expected_sector_penalty": 12.0, "should_auto_apply": False},
    {"fixture_id": "FX208-050", "schema_version": "208", "paper_only": True, "should_auto_apply_always_false": True, "auto_apply_enabled_always_false": True},
    # --- 51-60: exposure summary fixtures ---
    {"fixture_id": "FX208-051", "schema_version": "208", "paper_only": True, "total_exposure_groups": 10, "over_limit_group_count": 0, "expected_exposure_quality_grade": "A"},
    {"fixture_id": "FX208-052", "schema_version": "208", "paper_only": True, "total_exposure_groups": 10, "over_limit_group_count": 1, "expected_exposure_quality_grade": "B"},
    {"fixture_id": "FX208-053", "schema_version": "208", "paper_only": True, "total_exposure_groups": 10, "over_limit_group_count": 3, "expected_exposure_quality_grade": "C"},
    {"fixture_id": "FX208-054", "schema_version": "208", "paper_only": True, "total_exposure_groups": 10, "over_limit_group_count": 5, "expected_exposure_quality_grade": "D"},
    {"fixture_id": "FX208-055", "schema_version": "208", "paper_only": True, "critical_warning_count": 0, "high_warning_count": 0, "expected_risk_cap_grade": "A"},
    {"fixture_id": "FX208-056", "schema_version": "208", "paper_only": True, "top_concentrated_themes": ["半導體", "人工智慧"]},
    {"fixture_id": "FX208-057", "schema_version": "208", "paper_only": True, "top_concentrated_sectors": ["科技業", "電子零組件"]},
    {"fixture_id": "FX208-058", "schema_version": "208", "paper_only": True, "blocked_promotion_count": 3, "reduced_priority_count": 5},
    {"fixture_id": "FX208-059", "schema_version": "208", "paper_only": True, "human_review_count": 2},
    {"fixture_id": "FX208-060", "schema_version": "208", "paper_only": True, "diversification_grade": "A", "total_exposure_groups": 8, "over_limit_group_count": 0},
    # --- 61-70: exposure review result fixtures ---
    {"fixture_id": "FX208-061", "schema_version": "208", "paper_only": True, "review_period": "2026-W29", "expected_review_id_len": 10},
    {"fixture_id": "FX208-062", "schema_version": "208", "paper_only": True, "exposure_version": "2.0.8"},
    {"fixture_id": "FX208-063", "schema_version": "208", "paper_only": True, "should_auto_apply": False, "auto_apply_enabled": False},
    {"fixture_id": "FX208-064", "schema_version": "208", "paper_only": True, "all_passed": True},
    {"fixture_id": "FX208-065", "schema_version": "208", "paper_only": True, "paper_only_safety_snapshot": True},
    {"fixture_id": "FX208-066", "schema_version": "208", "paper_only": True, "no_real_orders": True},
    {"fixture_id": "FX208-067", "schema_version": "208", "paper_only": True, "research_only": True, "exposure_analysis_only": True},
    {"fixture_id": "FX208-068", "schema_version": "208", "paper_only": True, "human_review_required": True},
    {"fixture_id": "FX208-069", "schema_version": "208", "paper_only": True, "theme_concentration_count_min": 1},
    {"fixture_id": "FX208-070", "schema_version": "208", "paper_only": True, "sector_concentration_count_min": 1},
    # --- 71-80: export and backward compat fixtures ---
    {"fixture_id": "FX208-071", "schema_version": "208", "paper_only": True, "export_format": "json", "expected_is_valid": True},
    {"fixture_id": "FX208-072", "schema_version": "208", "paper_only": True, "export_format": "markdown", "expected_is_valid": True},
    {"fixture_id": "FX208-073", "schema_version": "208", "paper_only": True, "export_format": "csv", "expected_is_valid": True},
    {"fixture_id": "FX208-074", "schema_version": "208", "paper_only": True, "export_format": "audit_snapshot", "expected_export_status": "complete"},
    {"fixture_id": "FX208-075", "schema_version": "208", "paper_only": True, "v207_backward_compat": True, "v207_version": "2.0.7"},
    {"fixture_id": "FX208-076", "schema_version": "208", "paper_only": True, "v206_backward_compat": True, "v206_version": "2.0.6"},
    {"fixture_id": "FX208-077", "schema_version": "208", "paper_only": True, "cli_commands_count": 10},
    {"fixture_id": "FX208-078", "schema_version": "208", "paper_only": True, "gui_tabs_count": 3},
    {"fixture_id": "FX208-079", "schema_version": "208", "paper_only": True, "models_count": 14},
    {"fixture_id": "FX208-080", "schema_version": "208", "paper_only": True, "safety_flags_count": 21},
]

assert len(FIXTURES) == 80, f"Expected 80 FIXTURES, got {len(FIXTURES)}"
assert all(f["schema_version"] == "208" for f in FIXTURES)
assert all(f["paper_only"] is True for f in FIXTURES)
assert all("fixture_id" in f for f in FIXTURES)
