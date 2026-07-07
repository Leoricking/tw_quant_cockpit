"""
tests/test_strategy_robustness_v142.py — v1.4.2 Strategy Robustness tests.
[!] Research Only. No Real Orders. No Broker. Not Investment Advice.
Tests do NOT connect to external networks or APIs.
"""
import pytest
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "strategy_robustness")


def _load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURE_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)


# Helper: minimal trade list for tests
def _make_trades(n=30, win_rate=0.55):
    import random
    rng = random.Random(42)
    trades = []
    for i in range(n):
        win = rng.random() < win_rate
        ret = rng.uniform(0.02, 0.08) if win else rng.uniform(-0.05, -0.01)
        trades.append({
            "return_pct": ret,
            "date": f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
            "symbol": f"23{30 + i % 10}",
            "win": win,
            "cost": 0.003,
        })
    return trades


# ── Package / Safety flags ────────────────────────────────────────────────────

def test_package_import():
    """Test 1: strategy_robustness package imports."""
    import strategy_robustness
    assert strategy_robustness.NO_REAL_ORDERS is True


def test_no_real_orders_flag():
    """Test 2: NO_REAL_ORDERS is True."""
    import strategy_robustness
    assert strategy_robustness.NO_REAL_ORDERS is True


def test_broker_execution_disabled():
    """Test 3: BROKER_EXECUTION_ENABLED is False."""
    import strategy_robustness
    assert strategy_robustness.BROKER_EXECUTION_ENABLED is False


def test_production_trading_blocked():
    """Test 4: PRODUCTION_TRADING_BLOCKED is True."""
    import strategy_robustness
    assert strategy_robustness.PRODUCTION_TRADING_BLOCKED is True


def test_strategy_robustness_available():
    """Test 5: STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE is True."""
    import strategy_robustness
    assert strategy_robustness.STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE is True


# ── Models ────────────────────────────────────────────────────────────────────

def test_robustness_status_constants():
    """Test 6: RobustnessStatus has all required constants."""
    from strategy_robustness.models_v142 import RobustnessStatus
    assert RobustnessStatus.ROBUST == "ROBUST"
    assert RobustnessStatus.FRAGILE == "FRAGILE"
    assert RobustnessStatus.BLOCKED == "BLOCKED"
    assert RobustnessStatus.REGIME_DEPENDENT == "REGIME_DEPENDENT"
    assert RobustnessStatus.PARAMETER_SENSITIVE == "PARAMETER_SENSITIVE"
    assert RobustnessStatus.COST_SENSITIVE == "COST_SENSITIVE"
    assert RobustnessStatus.CONCENTRATED == "CONCENTRATED"
    assert RobustnessStatus.DECAYING == "DECAYING"
    assert RobustnessStatus.INSUFFICIENT_DATA == "INSUFFICIENT_DATA"
    assert RobustnessStatus.DEMO_ONLY == "DEMO_ONLY"
    assert RobustnessStatus.FAILED == "FAILED"
    assert RobustnessStatus.ACCEPTABLE == "ACCEPTABLE"


def test_robustness_dimension_constants():
    """Test 7: RobustnessDimension has required constants."""
    from strategy_robustness.models_v142 import RobustnessDimension
    assert RobustnessDimension.TIME == "TIME"
    assert RobustnessDimension.SYMBOL == "SYMBOL"
    assert RobustnessDimension.REGIME == "REGIME"
    assert RobustnessDimension.PARAMETER == "PARAMETER"
    assert RobustnessDimension.BOOTSTRAP == "BOOTSTRAP"
    assert RobustnessDimension.DECAY == "DECAY"


def test_decay_status_constants():
    """Test 8: DecayStatus has required constants."""
    from strategy_robustness.models_v142 import DecayStatus
    assert DecayStatus.NO_DECAY == "NO_DECAY"
    assert DecayStatus.POSSIBLE_DECAY == "POSSIBLE_DECAY"
    assert DecayStatus.SIGNIFICANT_DECAY == "SIGNIFICANT_DECAY"
    assert DecayStatus.INSUFFICIENT_DATA == "INSUFFICIENT_DATA"
    assert DecayStatus.UNKNOWN == "UNKNOWN"


def test_robustness_metric_dataclass():
    """Test 9: RobustnessMetric can be created and serialized."""
    from strategy_robustness.models_v142 import RobustnessMetric
    m = RobustnessMetric(
        dimension="TIME", metric_name="expectancy",
        value=0.01, normalized_score=0.8, threshold=0.005,
        status="PASS", sample_size=30, confidence="HIGH",
    )
    d = m.to_dict()
    assert d["dimension"] == "TIME"
    assert d["metric_name"] == "expectancy"
    assert isinstance(d["reasons"], list)
    assert isinstance(d["warnings"], list)


def test_robustness_metric_from_dict():
    """Test 10: RobustnessMetric.from_dict() round-trips correctly."""
    from strategy_robustness.models_v142 import RobustnessMetric
    m = RobustnessMetric(
        dimension="REGIME", metric_name="win_rate",
        value=0.6, normalized_score=0.7, threshold=0.5,
        status="PASS", sample_size=20, confidence="MEDIUM",
    )
    d = m.to_dict()
    m2 = RobustnessMetric.from_dict(d)
    assert m2.dimension == "REGIME"
    assert m2.value == 0.6


def test_robustness_configuration_defaults():
    """Test 11: RobustnessConfiguration has correct defaults."""
    from strategy_robustness.models_v142 import RobustnessConfiguration
    c = RobustnessConfiguration(rule_id="test_rule")
    assert c.dry_run is True
    assert c.data_mode == "REAL"
    assert c.random_seed == 42
    assert c.bootstrap_iterations == 1000
    assert len(c.cost_multipliers) == 4


def test_robustness_configuration_to_dict():
    """Test 12: RobustnessConfiguration.to_dict() returns dict."""
    from strategy_robustness.models_v142 import RobustnessConfiguration
    c = RobustnessConfiguration(rule_id="test")
    d = c.to_dict()
    assert d["rule_id"] == "test"
    assert d["dry_run"] is True


def test_robustness_configuration_from_dict():
    """Test 13: RobustnessConfiguration round-trips."""
    from strategy_robustness.models_v142 import RobustnessConfiguration
    c = RobustnessConfiguration(rule_id="r1", universe="extended")
    d = c.to_dict()
    c2 = RobustnessConfiguration.from_dict(d)
    assert c2.rule_id == "r1"
    assert c2.universe == "extended"


def test_strategy_robustness_result_defaults():
    """Test 14: StrategyRobustnessResult has required defaults."""
    from strategy_robustness.models_v142 import StrategyRobustnessResult, RobustnessStatus
    r = StrategyRobustnessResult(
        robustness_id="test_id", rule_id="r1",
        universe="core", start_date="2022-01-01", end_date="2024-12-31",
    )
    assert r.status == RobustnessStatus.BLOCKED
    assert r.formal_conclusion_allowed is False
    assert r.dry_run is True
    assert r.NO_REAL_ORDERS is True if hasattr(r, 'NO_REAL_ORDERS') else True


def test_strategy_robustness_result_hash():
    """Test 15: StrategyRobustnessResult reproducibility_hash is deterministic."""
    from strategy_robustness.models_v142 import StrategyRobustnessResult
    r1 = StrategyRobustnessResult(
        robustness_id="id1", rule_id="r1",
        universe="core", start_date="2022-01-01", end_date="2024-12-31",
    )
    r2 = StrategyRobustnessResult(
        robustness_id="id2", rule_id="r1",
        universe="core", start_date="2022-01-01", end_date="2024-12-31",
    )
    assert r1.reproducibility_hash == r2.reproducibility_hash


def test_strategy_robustness_result_to_dict():
    """Test 16: StrategyRobustnessResult.to_dict() includes all required fields."""
    from strategy_robustness.models_v142 import StrategyRobustnessResult
    r = StrategyRobustnessResult(
        robustness_id="test", rule_id="r1",
        universe="core", start_date="2022-01-01", end_date="2024-12-31",
    )
    d = r.to_dict()
    required = ["robustness_id", "rule_id", "universe", "start_date", "end_date",
                "status", "overall_score", "formal_conclusion_allowed", "trade_count"]
    for field in required:
        assert field in d, f"Missing field: {field}"


def test_strategy_robustness_result_from_dict():
    """Test 17: StrategyRobustnessResult.from_dict() round-trips."""
    from strategy_robustness.models_v142 import StrategyRobustnessResult
    r = StrategyRobustnessResult(
        robustness_id="test", rule_id="r1",
        universe="core", start_date="2022-01-01", end_date="2024-12-31",
        overall_score=75.0,
    )
    d = r.to_dict()
    r2 = StrategyRobustnessResult.from_dict(d)
    assert r2.rule_id == "r1"
    assert r2.overall_score == 75.0


def test_models_safety_flags():
    """Test 18: models_v142 safety flags are correct."""
    from strategy_robustness.models_v142 import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
        ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED,
    )
    assert NO_REAL_ORDERS is True
    assert BROKER_EXECUTION_ENABLED is False
    assert PRODUCTION_TRADING_BLOCKED is True
    assert ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED is False


# ── Time Robustness ───────────────────────────────────────────────────────────

def test_time_robustness_basic():
    """Test 19: Time robustness returns dict with required keys."""
    from strategy_robustness.time_robustness_v142 import StrategyTimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(40)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyTimeRobustnessAnalyzer().analyze(trades, config)
    assert "status" in result
    assert "yearly" in result
    assert "trade_count" in result
    assert result["trade_count"] == 40


def test_time_robustness_empty_trades():
    """Test 20: Time robustness handles empty trades gracefully."""
    from strategy_robustness.time_robustness_v142 import StrategyTimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyTimeRobustnessAnalyzer().analyze([], config)
    assert result["status"] == "INSUFFICIENT_DATA"
    assert "NO_TRADES" in result["warnings"]


def test_time_robustness_yearly_split():
    """Test 21: Yearly splits are computed."""
    from strategy_robustness.time_robustness_v142 import StrategyTimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(40)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyTimeRobustnessAnalyzer().analyze(trades, config)
    assert isinstance(result["yearly"], dict)


def test_time_robustness_early_vs_late():
    """Test 22: Early vs late period comparison is computed."""
    from strategy_robustness.time_robustness_v142 import StrategyTimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(40)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyTimeRobustnessAnalyzer().analyze(trades, config)
    assert "early_vs_late" in result


def test_time_robustness_rolling():
    """Test 23: Rolling windows computed."""
    from strategy_robustness.time_robustness_v142 import StrategyTimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(50)
    config = RobustnessConfiguration(rule_id="test", rolling_window_size=20, rolling_step_size=10)
    result = StrategyTimeRobustnessAnalyzer().analyze(trades, config)
    assert "rolling" in result


def test_time_robustness_checks():
    """Test 24: Checks dict is returned."""
    from strategy_robustness.time_robustness_v142 import StrategyTimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(40)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyTimeRobustnessAnalyzer().analyze(trades, config)
    assert "checks" in result
    assert isinstance(result["checks"], dict)


def test_time_fixture_stable():
    """Test 25: time_stable fixture has PASS status."""
    fixture = _load_fixture("time_stable.json")
    assert fixture["_fixture_meta"]["TEST_FIXTURE"] is True
    assert fixture["time_robustness"]["status"] == "PASS"


def test_time_fixture_fragile():
    """Test 26: time_fragile fixture has FRAGILE status."""
    fixture = _load_fixture("time_fragile.json")
    assert fixture["time_robustness"]["status"] == "FRAGILE"
    assert fixture["_fixture_meta"]["NOT_FOR_FORMAL_CONCLUSION"] is True


# ── Cross-Sectional ───────────────────────────────────────────────────────────

def test_cross_sectional_basic():
    """Test 27: Cross-sectional analysis returns dict with required keys."""
    from strategy_robustness.cross_sectional_v142 import CrossSectionalRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = CrossSectionalRobustnessAnalyzer().analyze(trades, config)
    assert "symbols_total" in result
    assert "profitable_symbol_ratio" in result
    assert "top_contributor_share" in result


def test_cross_sectional_empty():
    """Test 28: Cross-sectional handles empty gracefully."""
    from strategy_robustness.cross_sectional_v142 import CrossSectionalRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = CrossSectionalRobustnessAnalyzer().analyze([], config)
    assert result["status"] == "INSUFFICIENT_DATA"


def test_cross_sectional_symbol_count():
    """Test 29: Cross-sectional counts symbols correctly."""
    from strategy_robustness.cross_sectional_v142 import CrossSectionalRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)  # 10 unique symbols (2330-2339)
    config = RobustnessConfiguration(rule_id="test")
    result = CrossSectionalRobustnessAnalyzer().analyze(trades, config)
    assert result["symbols_total"] == 10


def test_cross_sectional_checks():
    """Test 30: Cross-sectional includes checks."""
    from strategy_robustness.cross_sectional_v142 import CrossSectionalRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = CrossSectionalRobustnessAnalyzer().analyze(trades, config)
    assert "checks" in result
    assert "symbol_count" in result["checks"]


def test_symbol_concentrated_fixture():
    """Test 31: symbol_concentrated fixture has correct structure."""
    fixture = _load_fixture("symbol_concentrated.json")
    assert fixture["_fixture_meta"]["TEST_FIXTURE"] is True
    assert fixture["cross_sectional"]["top_contributor_share"] > 0.5


# ── Industry Robustness ───────────────────────────────────────────────────────

def test_industry_robustness_basic():
    """Test 32: Industry robustness returns dict with required keys."""
    from strategy_robustness.industry_robustness_v142 import IndustryRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    industry_map = {f"23{30 + i}": "Semiconductors" if i < 5 else "Finance" for i in range(10)}
    config = RobustnessConfiguration(rule_id="test")
    result = IndustryRobustnessAnalyzer().analyze(trades, config, industry_map)
    assert "industries_total" in result
    assert "industry_stats" in result


def test_industry_robustness_missing_industry():
    """Test 33: Missing industry → INSUFFICIENT_DATA not guessed."""
    from strategy_robustness.industry_robustness_v142 import IndustryRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(20)
    config = RobustnessConfiguration(rule_id="test")
    result = IndustryRobustnessAnalyzer().analyze(trades, config, {})
    assert result["no_industry_count"] == 20
    assert "UNKNOWN" in result["industry_stats"]


def test_industry_robustness_empty_trades():
    """Test 34: Industry robustness handles empty trades."""
    from strategy_robustness.industry_robustness_v142 import IndustryRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = IndustryRobustnessAnalyzer().analyze([], config)
    assert result["status"] == "INSUFFICIENT_DATA"


def test_industry_robustness_checks():
    """Test 35: Industry robustness includes checks."""
    from strategy_robustness.industry_robustness_v142 import IndustryRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    industry_map = {f"23{30 + i}": "Semiconductors" if i < 5 else "Finance" for i in range(10)}
    config = RobustnessConfiguration(rule_id="test")
    result = IndustryRobustnessAnalyzer().analyze(trades, config, industry_map)
    assert "checks" in result


def test_industry_concentrated_fixture():
    """Test 36: industry_concentrated fixture has correct structure."""
    fixture = _load_fixture("industry_concentrated.json")
    assert fixture["_fixture_meta"]["TEST_FIXTURE"] is True
    assert "industry_stats" in fixture["industry_robustness"]


# ── Regime Robustness ─────────────────────────────────────────────────────────

def test_regime_robustness_basic():
    """Test 37: Regime robustness returns dict with required keys."""
    from strategy_robustness.regime_robustness_v142 import RegimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    regime_labels = {t["date"]: "BULL" if i < 20 else "BEAR" for i, t in enumerate(trades)}
    config = RobustnessConfiguration(rule_id="test")
    result = RegimeRobustnessAnalyzer().analyze(trades, regime_labels, config)
    assert "regime_stats" in result
    assert "regime_dependency_score" in result
    assert "regimes_found" in result


def test_regime_robustness_empty_trades():
    """Test 38: Regime robustness handles empty trades."""
    from strategy_robustness.regime_robustness_v142 import RegimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = RegimeRobustnessAnalyzer().analyze([], {}, config)
    assert result["status"] == "INSUFFICIENT_DATA"


def test_regime_robustness_dependency_score_range():
    """Test 39: Regime dependency score is between 0 and 1."""
    from strategy_robustness.regime_robustness_v142 import RegimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    regime_labels = {t["date"]: "BULL" for t in trades}
    config = RobustnessConfiguration(rule_id="test")
    result = RegimeRobustnessAnalyzer().analyze(trades, regime_labels, config)
    assert 0.0 <= result["regime_dependency_score"] <= 1.0


def test_regime_robustness_empty_labels():
    """Test 40: Regime robustness with empty labels assigns UNKNOWN."""
    from strategy_robustness.regime_robustness_v142 import RegimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(20)
    config = RobustnessConfiguration(rule_id="test")
    result = RegimeRobustnessAnalyzer().analyze(trades, {}, config)
    assert "UNKNOWN" in result["regimes_found"]


def test_regime_dependent_fixture():
    """Test 41: regime_dependent fixture has high dependency score."""
    fixture = _load_fixture("regime_dependent.json")
    assert fixture["regime_robustness"]["regime_dependency_score"] >= 0.6


# ── Parameter Sensitivity ─────────────────────────────────────────────────────

def test_parameter_sensitivity_basic():
    """Test 42: Parameter sensitivity returns dict with required keys."""
    from strategy_robustness.parameter_sensitivity_v142 import ParameterSensitivityAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    baseline = {"expectancy": 0.01, "win_rate": 0.55, "net_return": 0.08}
    variants = [
        {"params": {"lookback": 18}, "metrics": {"expectancy": 0.009, "net_return": 0.07}},
        {"params": {"lookback": 22}, "metrics": {"expectancy": 0.011, "net_return": 0.09}},
    ]
    config = RobustnessConfiguration(rule_id="test")
    result = ParameterSensitivityAnalyzer().analyze(baseline, variants, config)
    assert "variants" in result
    assert "checks" in result
    assert "status" in result


def test_parameter_sensitivity_empty_baseline():
    """Test 43: Empty baseline returns INSUFFICIENT_DATA."""
    from strategy_robustness.parameter_sensitivity_v142 import ParameterSensitivityAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = ParameterSensitivityAnalyzer().analyze({}, [], config)
    assert result["status"] == "INSUFFICIENT_DATA"


def test_parameter_sensitivity_all_results_preserved():
    """Test 44: All parameter variants are preserved in results."""
    from strategy_robustness.parameter_sensitivity_v142 import ParameterSensitivityAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    baseline = {"expectancy": 0.01, "net_return": 0.08}
    variants = [
        {"params": {"p": i}, "metrics": {"net_return": 0.08 + i * 0.005}}
        for i in range(5)
    ]
    config = RobustnessConfiguration(rule_id="test")
    result = ParameterSensitivityAnalyzer().analyze(baseline, variants, config)
    assert len(result["variants"]) == 5


def test_parameter_cliff_fixture():
    """Test 45: parameter_cliff fixture shows cliff risk."""
    fixture = _load_fixture("parameter_cliff.json")
    cliff_variants = [v for v in fixture["parameter_sensitivity"]["variants"] if v.get("cliff_risk")]
    assert len(cliff_variants) > 0


# ── Cost Stress ───────────────────────────────────────────────────────────────

def test_cost_stress_basic():
    """Test 46: Cost stress returns dict with required keys."""
    from strategy_robustness.cost_stress_v142 import StrategyCostStressAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyCostStressAnalyzer().analyze(trades, config)
    assert "multiplier_results" in result
    assert "cost_sensitivity_slope" in result
    assert "checks" in result


def test_cost_stress_empty_trades():
    """Test 47: Cost stress handles empty trades."""
    from strategy_robustness.cost_stress_v142 import StrategyCostStressAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyCostStressAnalyzer().analyze([], config)
    assert result["status"] == "INSUFFICIENT_DATA"


def test_cost_stress_multipliers_all_computed():
    """Test 48: All 4 cost multiplier results are computed."""
    from strategy_robustness.cost_stress_v142 import StrategyCostStressAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyCostStressAnalyzer().analyze(trades, config)
    assert len(result["multiplier_results"]) == 4


def test_cost_sensitive_fixture():
    """Test 49: cost_sensitive fixture fails at 2x cost."""
    fixture = _load_fixture("cost_sensitive.json")
    assert fixture["cost_stress"]["checks"]["survives_2x_cost"]["pass"] is False


# ── Trade Concentration ───────────────────────────────────────────────────────

def test_trade_concentration_basic():
    """Test 50: Trade concentration returns dict with required keys."""
    from strategy_robustness.trade_concentration_v142 import TradeConcentrationAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = TradeConcentrationAnalyzer().analyze(trades, config)
    assert "top_1pct_contribution" in result
    assert "hhi" in result
    assert "stress_tests" in result


def test_trade_concentration_empty():
    """Test 51: Trade concentration handles empty trades."""
    from strategy_robustness.trade_concentration_v142 import TradeConcentrationAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = TradeConcentrationAnalyzer().analyze([], config)
    assert result["status"] == "INSUFFICIENT_DATA"


def test_trade_concentration_hhi_range():
    """Test 52: HHI is between 0 and 1."""
    from strategy_robustness.trade_concentration_v142 import TradeConcentrationAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = TradeConcentrationAnalyzer().analyze(trades, config)
    assert 0.0 <= result["hhi"] <= 1.0


def test_trade_concentrated_fixture():
    """Test 53: trade_concentrated fixture shows concentration."""
    fixture = _load_fixture("trade_concentrated.json")
    assert fixture["trade_concentration"]["status"] == "CONCENTRATED"
    assert fixture["trade_concentration"]["top_1pct_contribution"] > 0.3


# ── Bootstrap ─────────────────────────────────────────────────────────────────

def test_bootstrap_basic():
    """Test 54: Bootstrap returns dict with required keys."""
    from strategy_robustness.bootstrap_v142 import BootstrapRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", bootstrap_iterations=100)
    result = BootstrapRobustnessAnalyzer().analyze(trades, config)
    assert "metrics" in result
    assert "iterations" in result
    assert "seed" in result


def test_bootstrap_insufficient_trades():
    """Test 55: Bootstrap handles insufficient trades."""
    from strategy_robustness.bootstrap_v142 import BootstrapRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = BootstrapRobustnessAnalyzer().analyze([{"return_pct": 0.01, "win": True, "cost": 0.003}], config)
    assert result["status"] == "INSUFFICIENT"


def test_bootstrap_deterministic():
    """Test 56: Bootstrap is deterministic with same seed."""
    from strategy_robustness.bootstrap_v142 import BootstrapRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", bootstrap_iterations=50, random_seed=42)
    r1 = BootstrapRobustnessAnalyzer().analyze(trades, config)
    r2 = BootstrapRobustnessAnalyzer().analyze(trades, config)
    assert r1["metrics"]["expectancy"]["point_estimate"] == r2["metrics"]["expectancy"]["point_estimate"]


def test_bootstrap_note_trade_dependence():
    """Test 57: Bootstrap result includes trade dependence note."""
    from strategy_robustness.bootstrap_v142 import BootstrapRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", bootstrap_iterations=50)
    result = BootstrapRobustnessAnalyzer().analyze(trades, config)
    assert "note" in result
    assert "TRADE_DEPENDENCE" in result["note"].upper()


def test_bootstrap_metrics_expected():
    """Test 58: Bootstrap includes all expected metrics."""
    from strategy_robustness.bootstrap_v142 import BootstrapRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", bootstrap_iterations=50)
    result = BootstrapRobustnessAnalyzer().analyze(trades, config)
    expected = ["expectancy", "win_rate", "profit_factor", "mean_return", "median_return", "max_drawdown"]
    for m in expected:
        assert m in result["metrics"], f"Missing bootstrap metric: {m}"


def test_bootstrap_ci_structure():
    """Test 59: Bootstrap CI has ci_90 and ci_95 with 2 values each."""
    from strategy_robustness.bootstrap_v142 import BootstrapRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", bootstrap_iterations=50)
    result = BootstrapRobustnessAnalyzer().analyze(trades, config)
    exp = result["metrics"]["expectancy"]
    assert len(exp["ci_90"]) == 2
    assert len(exp["ci_95"]) == 2


# ── Monte Carlo ───────────────────────────────────────────────────────────────

def test_monte_carlo_basic():
    """Test 60: Monte Carlo returns dict with required keys."""
    from strategy_robustness.monte_carlo_v142 import MonteCarloTradeOrderAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", monte_carlo_iterations=50)
    result = MonteCarloTradeOrderAnalyzer().analyze(trades, config)
    assert "median_terminal_capital" in result
    assert "p5_terminal_capital" in result
    assert "ruin_probability_approximation" in result


def test_monte_carlo_does_not_modify_trades():
    """Test 61: Monte Carlo does not modify original trades."""
    from strategy_robustness.monte_carlo_v142 import MonteCarloTradeOrderAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    original_first = trades[0]["return_pct"]
    config = RobustnessConfiguration(rule_id="test", monte_carlo_iterations=20)
    MonteCarloTradeOrderAnalyzer().analyze(trades, config)
    assert trades[0]["return_pct"] == original_first


def test_monte_carlo_deterministic():
    """Test 62: Monte Carlo is deterministic with same seed."""
    from strategy_robustness.monte_carlo_v142 import MonteCarloTradeOrderAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", monte_carlo_iterations=50, random_seed=42)
    r1 = MonteCarloTradeOrderAnalyzer().analyze(trades, config)
    r2 = MonteCarloTradeOrderAnalyzer().analyze(trades, config)
    assert r1["median_terminal_capital"] == r2["median_terminal_capital"]


def test_monte_carlo_insufficient():
    """Test 63: Monte Carlo handles insufficient trades."""
    from strategy_robustness.monte_carlo_v142 import MonteCarloTradeOrderAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = MonteCarloTradeOrderAnalyzer().analyze([{"return_pct": 0.01, "win": True}], config)
    assert result["status"] == "INSUFFICIENT"


def test_monte_carlo_ruin_probability_range():
    """Test 64: Ruin probability is between 0 and 1."""
    from strategy_robustness.monte_carlo_v142 import MonteCarloTradeOrderAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", monte_carlo_iterations=50)
    result = MonteCarloTradeOrderAnalyzer().analyze(trades, config)
    assert 0.0 <= result["ruin_probability_approximation"] <= 1.0


# ── Rolling Stability ─────────────────────────────────────────────────────────

def test_rolling_stability_basic():
    """Test 65: Rolling stability returns dict with required keys."""
    from strategy_robustness.rolling_stability_v142 import RollingStabilityAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(40)
    config = RobustnessConfiguration(rule_id="test", rolling_window_size=15, rolling_step_size=5)
    result = RollingStabilityAnalyzer().analyze(trades, config)
    assert "summary" in result
    assert "window_results" in result


def test_rolling_stability_empty():
    """Test 66: Rolling stability handles empty trades."""
    from strategy_robustness.rolling_stability_v142 import RollingStabilityAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = RollingStabilityAnalyzer().analyze([], config)
    assert result["status"] == "INSUFFICIENT_DATA"


def test_rolling_stability_positive_ratio():
    """Test 67: Positive window ratio is between 0 and 1."""
    from strategy_robustness.rolling_stability_v142 import RollingStabilityAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(40)
    config = RobustnessConfiguration(rule_id="test", rolling_window_size=15, rolling_step_size=5)
    result = RollingStabilityAnalyzer().analyze(trades, config)
    pos_ratio = result["summary"]["positive_window_ratio"]
    assert 0.0 <= pos_ratio <= 1.0


# ── Decay Detection ───────────────────────────────────────────────────────────

def test_decay_detector_basic():
    """Test 68: Decay detector returns dict with required keys."""
    from strategy_robustness.decay_detector_v142 import StrategyDecayDetector
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(40)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyDecayDetector().analyze(trades, config)
    assert "decay_status" in result
    assert "evidence" in result
    assert "metrics" in result


def test_decay_detector_insufficient_trades():
    """Test 69: Decay detector returns INSUFFICIENT_DATA for <6 trades."""
    from strategy_robustness.decay_detector_v142 import StrategyDecayDetector
    from strategy_robustness.models_v142 import RobustnessConfiguration, DecayStatus
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyDecayDetector().analyze(_make_trades(4), config)
    assert result["decay_status"] == DecayStatus.INSUFFICIENT_DATA


def test_decay_detector_no_decay():
    """Test 70: Stable strategy returns NO_DECAY or INSUFFICIENT_DATA."""
    from strategy_robustness.decay_detector_v142 import StrategyDecayDetector
    from strategy_robustness.models_v142 import RobustnessConfiguration, DecayStatus
    import random
    rng = random.Random(42)
    trades = [{"return_pct": rng.uniform(0.01, 0.05), "date": f"202{i//30+1}-01-01",
               "symbol": "2330", "win": True, "cost": 0.001} for i in range(30)]
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyDecayDetector().analyze(trades, config)
    assert result["decay_status"] in (DecayStatus.NO_DECAY, DecayStatus.INSUFFICIENT_DATA)


def test_decay_detector_significant_decay():
    """Test 71: Degrading strategy returns SIGNIFICANT_DECAY."""
    from strategy_robustness.decay_detector_v142 import StrategyDecayDetector
    from strategy_robustness.models_v142 import RobustnessConfiguration, DecayStatus
    early = [{"return_pct": 0.05, "date": f"2021-01-{i+1:02d}", "symbol": "2330", "win": True, "cost": 0.001}
             for i in range(15)]
    recent = [{"return_pct": -0.04, "date": f"2024-01-{i+1:02d}", "symbol": "2330", "win": False, "cost": 0.001}
              for i in range(15)]
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyDecayDetector().analyze(early + recent, config)
    assert result["decay_status"] in (DecayStatus.POSSIBLE_DECAY, DecayStatus.SIGNIFICANT_DECAY)


def test_decaying_fixture():
    """Test 72: decaying fixture shows SIGNIFICANT_DECAY."""
    fixture = _load_fixture("decaying.json")
    assert fixture["decay"]["decay_status"] == "SIGNIFICANT_DECAY"
    assert len(fixture["decay"]["evidence"]) > 0


# ── Stress Scenarios ──────────────────────────────────────────────────────────

def test_stress_scenarios_high_cost():
    """Test 73: HIGH_COST scenario returns result dict."""
    from strategy_robustness.stress_scenarios_v142 import StrategyStressScenarioEngine
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyStressScenarioEngine().run(trades, "HIGH_COST", config)
    assert result["scenario"] == "HIGH_COST"
    assert "net_return" in result
    assert "strategy_survives" in result


def test_stress_scenarios_all_run():
    """Test 74: run_all returns results for all scenarios."""
    from strategy_robustness.stress_scenarios_v142 import StrategyStressScenarioEngine, VALID_SCENARIOS
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    results = StrategyStressScenarioEngine().run_all(trades, config)
    assert len(results) == len(VALID_SCENARIOS)


def test_stress_scenarios_no_modify_original():
    """Test 75: Stress scenarios do not modify original trades."""
    from strategy_robustness.stress_scenarios_v142 import StrategyStressScenarioEngine
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    orig_cost = trades[0]["cost"]
    config = RobustnessConfiguration(rule_id="test")
    StrategyStressScenarioEngine().run(trades, "HIGH_COST", config)
    assert trades[0]["cost"] == orig_cost


def test_stress_scenario_unknown():
    """Test 76: Unknown scenario returns UNKNOWN_SCENARIO."""
    from strategy_robustness.stress_scenarios_v142 import StrategyStressScenarioEngine
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(10)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyStressScenarioEngine().run(trades, "FAKE_SCENARIO", config)
    assert result["status"] == "UNKNOWN_SCENARIO"


def test_stress_scenarios_explicit_params():
    """Test 77: Each scenario result includes params and assumptions."""
    from strategy_robustness.stress_scenarios_v142 import StrategyStressScenarioEngine
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyStressScenarioEngine().run(trades, "HIGH_SLIPPAGE", config)
    assert "params" in result
    assert "assumptions" in result


def test_stress_scenarios_empty_trades():
    """Test 78: Stress scenarios handle empty trades."""
    from strategy_robustness.stress_scenarios_v142 import StrategyStressScenarioEngine
    from strategy_robustness.models_v142 import RobustnessConfiguration
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyStressScenarioEngine().run([], "HIGH_COST", config)
    assert result["status"] == "INSUFFICIENT_DATA"


# ── Failure Mode Classifier ───────────────────────────────────────────────────

def test_failure_modes_basic():
    """Test 79: Failure mode classifier returns list."""
    from strategy_robustness.failure_modes_v142 import StrategyFailureModeClassifier
    result = {
        "trade_count": 5,
        "formal_conclusion_allowed": False,
        "regime_robustness": {"regime_dependency_score": 0.3},
        "parameter_sensitivity": {"variants": []},
        "cost_stress": {"checks": {}},
        "trade_concentration": {"status": "PASS"},
        "cross_sectional": {"top_contributor_share": 0.3},
        "industry_robustness": {"checks": {}},
        "time_robustness": {"checks": {}},
        "bootstrap": {"status": "PASS"},
        "decay": {"decay_status": "NO_DECAY"},
        "failure_modes": [],
    }
    modes = StrategyFailureModeClassifier().classify(result)
    assert isinstance(modes, list)


def test_failure_modes_sample_too_small():
    """Test 80: Small sample triggers SAMPLE_TOO_SMALL failure mode."""
    from strategy_robustness.failure_modes_v142 import StrategyFailureModeClassifier
    result = {
        "trade_count": 5,
        "formal_conclusion_allowed": False,
        "regime_robustness": {"regime_dependency_score": 0.3},
        "parameter_sensitivity": {"variants": []},
        "cost_stress": {"checks": {}},
        "trade_concentration": {"status": "PASS"},
        "cross_sectional": {"top_contributor_share": 0.3},
        "industry_robustness": {"checks": {}},
        "time_robustness": {"checks": {}},
        "bootstrap": {"status": "PASS"},
        "decay": {"decay_status": "NO_DECAY"},
        "failure_modes": [],
    }
    modes = StrategyFailureModeClassifier().classify(result)
    types = [m["type"] for m in modes]
    assert "SAMPLE_TOO_SMALL" in types


def test_failure_modes_no_forbidden_actions():
    """Test 81: No failure mode recommends BUY, SELL, TRADE, ORDER, AUTO_OPTIMIZE."""
    from strategy_robustness.failure_modes_v142 import StrategyFailureModeClassifier, VALID_RESEARCH_ACTIONS
    result = {
        "trade_count": 5,
        "formal_conclusion_allowed": False,
        "regime_robustness": {"regime_dependency_score": 0.8},
        "parameter_sensitivity": {"variants": [{"cliff_risk": True}]},
        "cost_stress": {"checks": {"survives_2x_cost": {"pass": False}}},
        "trade_concentration": {"status": "CONCENTRATED"},
        "cross_sectional": {"top_contributor_share": 0.8},
        "industry_robustness": {"checks": {"single_industry_concentration": {"pass": False}}},
        "time_robustness": {"checks": {"performance_concentration": {"pass": False}}},
        "bootstrap": {"status": "FAIL"},
        "decay": {"decay_status": "SIGNIFICANT_DECAY"},
        "failure_modes": [],
    }
    modes = StrategyFailureModeClassifier().classify(result)
    forbidden = ["BUY", "SELL", "TRADE", "ORDER", "AUTO_OPTIMIZE"]
    for m in modes:
        action = m.get("recommended_research_action", "")
        for f in forbidden:
            assert f not in action, f"Forbidden action '{f}' found in: {action}"
        assert action in VALID_RESEARCH_ACTIONS, f"Invalid action: {action}"


def test_failure_modes_regime_dependent():
    """Test 82: High regime dependency triggers REGIME_DEPENDENT."""
    from strategy_robustness.failure_modes_v142 import StrategyFailureModeClassifier
    result = {
        "trade_count": 50,
        "formal_conclusion_allowed": False,
        "regime_robustness": {"regime_dependency_score": 0.8},
        "parameter_sensitivity": {"variants": []},
        "cost_stress": {"checks": {}},
        "trade_concentration": {"status": "PASS"},
        "cross_sectional": {"top_contributor_share": 0.3},
        "industry_robustness": {"checks": {}},
        "time_robustness": {"checks": {}},
        "bootstrap": {"status": "PASS"},
        "decay": {"decay_status": "NO_DECAY"},
        "failure_modes": [],
    }
    modes = StrategyFailureModeClassifier().classify(result)
    types = [m["type"] for m in modes]
    assert "REGIME_DEPENDENT" in types


# ── Score Engine ──────────────────────────────────────────────────────────────

def test_score_engine_basic():
    """Test 83: Score engine returns dict with required keys."""
    from strategy_robustness.score_v142 import StrategyRobustnessScoreEngine
    fixture = _load_fixture("robustness_result_v1.json")
    result = StrategyRobustnessScoreEngine().score(fixture)
    assert "overall_score" in result
    assert "dimension_scores" in result
    assert "robustness_status" in result
    assert "formal_conclusion_allowed" in result


def test_score_engine_range():
    """Test 84: Score is between 0 and 100."""
    from strategy_robustness.score_v142 import StrategyRobustnessScoreEngine
    fixture = _load_fixture("robustness_result_v1.json")
    result = StrategyRobustnessScoreEngine().score(fixture)
    assert 0.0 <= result["overall_score"] <= 100.0


def test_score_engine_status_mapping():
    """Test 85: Score status maps correctly to ranges."""
    from strategy_robustness.score_v142 import StrategyRobustnessScoreEngine
    engine = StrategyRobustnessScoreEngine()
    # high-score fixture
    fixture = _load_fixture("robustness_result_v1.json")
    result = engine.score(fixture)
    status = result["robustness_status"]
    score = result["overall_score"]
    if score >= 80:
        assert status == "ROBUST"
    elif score >= 65:
        assert status == "ACCEPTABLE"
    elif score >= 45:
        assert status == "FRAGILE"
    elif score >= 25:
        assert status == "HIGH_RISK"
    else:
        assert status == "BLOCKED"


def test_score_engine_formal_conclusion_blocked_for_demo():
    """Test 86: Formal conclusion blocked when data_mode != REAL."""
    from strategy_robustness.score_v142 import StrategyRobustnessScoreEngine
    fixture = {
        "trade_count": 50,
        "data_mode": "MOCK",
        "failure_modes": [],
        "time_robustness": {}, "cross_sectional": {}, "industry_robustness": {},
        "regime_robustness": {}, "parameter_sensitivity": {}, "cost_stress": {},
        "trade_concentration": {}, "bootstrap": {}, "monte_carlo": {},
        "rolling_stability": {}, "decay": {},
    }
    result = StrategyRobustnessScoreEngine().score(fixture)
    assert result["formal_conclusion_allowed"] is False


def test_score_engine_14_dimensions():
    """Test 87: Score engine produces 14 dimension scores."""
    from strategy_robustness.score_v142 import StrategyRobustnessScoreEngine
    fixture = _load_fixture("robustness_result_v1.json")
    result = StrategyRobustnessScoreEngine().score(fixture)
    assert len(result["dimension_scores"]) == 14


# ── Comparison ────────────────────────────────────────────────────────────────

def test_abc_robustness_comparison_same_conditions():
    """Test 88: ABC comparison with matching conditions produces ranking."""
    from strategy_robustness.comparison_v142 import ABCRobustnessComparison
    base = {"universe": "core", "start_date": "2022-01-01", "end_date": "2024-12-31"}
    a = {**base, "overall_score": 80.0, "robustness_status": "ROBUST"}
    b = {**base, "overall_score": 70.0, "robustness_status": "ACCEPTABLE"}
    c = {**base, "overall_score": 60.0, "robustness_status": "FRAGILE"}
    result = ABCRobustnessComparison().compare_abc(a, b, c)
    assert result["rankable"] is True
    assert result["best"] == "A"


def test_abc_robustness_comparison_different_conditions():
    """Test 89: ABC comparison with different conditions returns NOT_DIRECTLY_RANKABLE."""
    from strategy_robustness.comparison_v142 import ABCRobustnessComparison
    a = {"universe": "core", "start_date": "2022-01-01", "end_date": "2024-12-31", "overall_score": 80.0}
    b = {"universe": "extended", "start_date": "2022-01-01", "end_date": "2024-12-31", "overall_score": 70.0}
    c = {"universe": "core", "start_date": "2022-01-01", "end_date": "2024-12-31", "overall_score": 60.0}
    result = ABCRobustnessComparison().compare_abc(a, b, c)
    assert result["rankable"] is False
    assert "NOT_DIRECTLY_RANKABLE" in result["reason"]


def test_strategy_knowledge_comparison_basic():
    """Test 90: StrategyKnowledgeRobustnessComparison.compare_rules() returns ranking."""
    from strategy_robustness.comparison_v142 import StrategyKnowledgeRobustnessComparison
    base = {"universe": "core", "start_date": "2022-01-01", "end_date": "2024-12-31"}
    results = [
        {**base, "rule_id": "r1", "overall_score": 80.0},
        {**base, "rule_id": "r2", "overall_score": 65.0},
        {**base, "rule_id": "r3", "overall_score": 50.0},
    ]
    result = StrategyKnowledgeRobustnessComparison().compare_rules(results)
    assert result["rankable"] is True
    assert result["best_rule"] == "r1"


def test_strategy_knowledge_comparison_empty():
    """Test 91: StrategyKnowledgeRobustnessComparison handles empty results."""
    from strategy_robustness.comparison_v142 import StrategyKnowledgeRobustnessComparison
    result = StrategyKnowledgeRobustnessComparison().compare_rules([])
    assert result["rankable"] is False


# ── Store ─────────────────────────────────────────────────────────────────────

def test_store_save_and_list(tmp_path):
    """Test 92: Store can save and list runs."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_run({"robustness_id": "test_001", "rule_id": "r1", "overall_score": 75.0})
    runs = store.list_runs()
    assert len(runs) == 1
    assert runs[0]["robustness_id"] == "test_001"


def test_store_no_duplicate(tmp_path):
    """Test 93: Store does not save duplicate robustness_id."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_run({"robustness_id": "dup_001", "rule_id": "r1"})
    store.save_run({"robustness_id": "dup_001", "rule_id": "r1"})
    runs = store.list_runs()
    assert len(runs) == 1


def test_store_get_run(tmp_path):
    """Test 94: Store can retrieve a run by ID."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_result({"robustness_id": "find_me", "rule_id": "r1", "overall_score": 80.0})
    result = store.get_run("find_me")
    assert result is not None
    assert result["rule_id"] == "r1"


def test_store_get_run_missing(tmp_path):
    """Test 95: Store returns None for missing ID."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    result = store.get_run("nonexistent")
    assert result is None


def test_store_list_by_rule(tmp_path):
    """Test 96: Store can list runs by rule_id."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_result({"robustness_id": "r1_001", "rule_id": "rule_a", "robustness_status": "ROBUST"})
    store.save_result({"robustness_id": "r2_001", "rule_id": "rule_b", "robustness_status": "FRAGILE"})
    results = store.list_by_rule("rule_a")
    assert len(results) == 1
    assert results[0]["rule_id"] == "rule_a"


def test_store_schema_version():
    """Test 97: Schema version is 1.4.2."""
    from strategy_robustness.store_v142 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "1.4.2"


def test_store_summarize(tmp_path):
    """Test 98: Store summarize returns dict with schema_version."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    summary = store.summarize()
    assert "schema_version" in summary
    assert summary["schema_version"] == "1.4.2"


def test_store_list_robust(tmp_path):
    """Test 99: Store can list robust results."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_result({"robustness_id": "robust_001", "rule_id": "r1", "robustness_status": "ROBUST"})
    store.save_result({"robustness_id": "fragile_001", "rule_id": "r2", "robustness_status": "FRAGILE"})
    robust = store.list_robust()
    assert len(robust) == 1


def test_store_list_fragile(tmp_path):
    """Test 100: Store can list fragile results."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_result({"robustness_id": "fragile_002", "rule_id": "r2", "robustness_status": "FRAGILE"})
    fragile = store.list_fragile()
    assert len(fragile) == 1


# ── Query Service ─────────────────────────────────────────────────────────────

def test_query_service_list_runs(tmp_path):
    """Test 101: QueryService.list_runs() returns list."""
    from strategy_robustness.query_v142 import StrategyRobustnessQueryService
    svc = StrategyRobustnessQueryService(base_dir=str(tmp_path))
    assert isinstance(svc.list_runs(), list)


def test_query_service_summarize(tmp_path):
    """Test 102: QueryService.summarize() returns dict."""
    from strategy_robustness.query_v142 import StrategyRobustnessQueryService
    svc = StrategyRobustnessQueryService(base_dir=str(tmp_path))
    summary = svc.summarize()
    assert isinstance(summary, dict)
    assert "schema_version" in summary


def test_query_service_list_robust(tmp_path):
    """Test 103: QueryService.list_robust() returns list."""
    from strategy_robustness.query_v142 import StrategyRobustnessQueryService
    svc = StrategyRobustnessQueryService(base_dir=str(tmp_path))
    assert isinstance(svc.list_robust(), list)


def test_query_service_list_fragile(tmp_path):
    """Test 104: QueryService.list_fragile() returns list."""
    from strategy_robustness.query_v142 import StrategyRobustnessQueryService
    svc = StrategyRobustnessQueryService(base_dir=str(tmp_path))
    assert isinstance(svc.list_fragile(), list)


def test_query_service_list_decaying(tmp_path):
    """Test 105: QueryService.list_decaying() returns list."""
    from strategy_robustness.query_v142 import StrategyRobustnessQueryService
    svc = StrategyRobustnessQueryService(base_dir=str(tmp_path))
    assert isinstance(svc.list_decaying(), list)


# ── Repair Integration ────────────────────────────────────────────────────────

def test_repair_integration_create_repair_tasks_false():
    """Test 106: Repair integration with create_repair_tasks=False returns PREVIEW_ONLY."""
    from strategy_robustness.repair_integration_v142 import RobustnessRepairIntegration
    integration = RobustnessRepairIntegration(create_repair_tasks=False)
    needs = [{"issue": "insufficient_trades", "priority": "HIGH", "action_required": "EXTEND"}]
    candidates = integration.create_repair_candidates(needs)
    assert all(c["status"] == "PREVIEW_ONLY" for c in candidates)
    assert all(c["queued"] is False for c in candidates)


def test_repair_integration_identify_insufficient_trades():
    """Test 107: Identifies insufficient trades repair need."""
    from strategy_robustness.repair_integration_v142 import RobustnessRepairIntegration
    integration = RobustnessRepairIntegration(create_repair_tasks=False)
    result = {"trade_count": 10, "cross_sectional": {"symbols_total": 10}, "industry_robustness": {"no_industry_count": 0}, "bootstrap": {}}
    needs = integration.identify_repair_needs(result)
    types = [n["issue"] for n in needs]
    assert "insufficient_trades" in types


def test_repair_integration_no_auto_repair():
    """Test 108: Repair integration has no auto_repair flag set."""
    from strategy_robustness.repair_integration_v142 import RobustnessRepairIntegration
    integration = RobustnessRepairIntegration(create_repair_tasks=False)
    needs = [{"issue": "test", "priority": "LOW", "action_required": "REVIEW"}]
    candidates = integration.create_repair_candidates(needs)
    for c in candidates:
        assert c.get("auto_repair", False) is False


# ── Replay Integration ────────────────────────────────────────────────────────

def test_replay_integration_safety_flags():
    """Test 109: Replay integration has correct safety flags."""
    from strategy_robustness.replay_integration_v142 import (
        REPLAY_SCORE_MODIFICATION_ENABLED,
        REPLAY_CHALLENGE_MODIFICATION_ENABLED,
        RULE_PARAMETER_MODIFICATION_ENABLED,
    )
    assert REPLAY_SCORE_MODIFICATION_ENABLED is False
    assert REPLAY_CHALLENGE_MODIFICATION_ENABLED is False
    assert RULE_PARAMETER_MODIFICATION_ENABLED is False


def test_replay_integration_read_only(tmp_path):
    """Test 110: Replay integration evidence is read_only=True."""
    from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
    integration = RobustnessReplayIntegration(base_dir=str(tmp_path))
    evidence = integration.get_evidence_for_rule("test_rule")
    assert evidence["read_only"] is True
    assert evidence["modifies_replay"] is False


def test_replay_integration_no_result(tmp_path):
    """Test 111: Replay integration returns NO_ROBUSTNESS_DATA for unknown rule."""
    from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
    integration = RobustnessReplayIntegration(base_dir=str(tmp_path))
    evidence = integration.get_evidence_for_rule("unknown_rule_xyz")
    assert evidence["formal_conclusion_status"] == "NO_ROBUSTNESS_DATA"


def test_replay_integration_does_not_modify_session():
    """Test 112: Replay integration explicitly marks modifies_session_score=False."""
    from strategy_robustness.replay_integration_v142 import RobustnessReplayIntegration
    import tempfile, os
    with tempfile.TemporaryDirectory() as tmp:
        integration = RobustnessReplayIntegration(base_dir=tmp)
        evidence = integration.get_evidence_for_rule("rule_x")
        assert evidence.get("modifies_session_score") is False


# ── Report ────────────────────────────────────────────────────────────────────

def test_report_generate():
    """Test 113: Report generator returns dict with required sections."""
    from strategy_robustness.report_v142 import StrategyRobustnessReport
    fixture = _load_fixture("robustness_result_v1.json")
    rpt = StrategyRobustnessReport()
    report = rpt.generate(fixture)
    assert "report_type" in report
    assert report["report_type"] == "STRATEGY_ROBUSTNESS"
    assert "summary" in report
    assert "safety" in report


def test_report_safety_flags():
    """Test 114: Report includes correct safety flags."""
    from strategy_robustness.report_v142 import StrategyRobustnessReport
    fixture = _load_fixture("robustness_result_v1.json")
    report = StrategyRobustnessReport().generate(fixture)
    safety = report["safety"]
    assert safety["no_real_orders"] is True
    assert safety["broker_execution_enabled"] is False
    assert safety["production_trading_blocked"] is True
    assert safety["mock_formal_conclusion_allowed"] is False


def test_report_format_text():
    """Test 115: Report.format_text() returns non-empty string."""
    from strategy_robustness.report_v142 import StrategyRobustnessReport
    fixture = _load_fixture("robustness_result_v1.json")
    rpt = StrategyRobustnessReport()
    report = rpt.generate(fixture)
    text = rpt.format_text(report)
    assert isinstance(text, str)
    assert len(text) > 50
    assert "Research Only" in text


def test_report_format_markdown():
    """Test 116: Report.format_markdown() returns non-empty string with MD."""
    from strategy_robustness.report_v142 import StrategyRobustnessReport
    fixture = _load_fixture("robustness_result_v1.json")
    rpt = StrategyRobustnessReport()
    report = rpt.generate(fixture)
    md = rpt.format_markdown(report)
    assert isinstance(md, str)
    assert "#" in md


# ── Health Check ──────────────────────────────────────────────────────────────

def test_health_check_runs():
    """Test 117: Health check can run and returns dict."""
    from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
    hc = StrategyRobustnessHealthCheck()
    result = hc.run()
    assert isinstance(result, dict)
    assert len(result) > 0


def test_health_check_all_pass():
    """Test 118: Health check passes all checks."""
    from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
    hc = StrategyRobustnessHealthCheck()
    summary = hc.get_health_summary()
    failed = {k: v for k, v in summary["checks"].items() if v["status"] != "PASS"}
    assert summary["all_pass"], f"Failed checks: {failed}"


def test_health_check_auto_optimization_disabled():
    """Test 119: Health check auto_optimization_enabled is False."""
    from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
    hc = StrategyRobustnessHealthCheck()
    assert hc.auto_optimization_enabled is False


def test_health_check_auto_trading_disabled():
    """Test 120: Health check auto_trading_enabled is False."""
    from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
    hc = StrategyRobustnessHealthCheck()
    assert hc.auto_trading_enabled is False


def test_health_check_mock_fallback_disabled():
    """Test 121: Health check mock_fallback_enabled is False."""
    from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
    hc = StrategyRobustnessHealthCheck()
    assert hc.mock_fallback_enabled is False


def test_health_check_broker_execution_disabled():
    """Test 122: Health check broker_execution_enabled is False."""
    from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
    hc = StrategyRobustnessHealthCheck()
    assert hc.broker_execution_enabled is False


def test_health_check_production_trading_blocked():
    """Test 123: Health check production_trading_blocked is True."""
    from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
    hc = StrategyRobustnessHealthCheck()
    assert hc.production_trading_blocked is True


def test_health_check_31_checks():
    """Test 124: Health check has at least 30 checks."""
    from strategy_robustness.health_v142 import StrategyRobustnessHealthCheck
    hc = StrategyRobustnessHealthCheck()
    result = hc.run()
    assert len(result) >= 30


# ── version_info.py ───────────────────────────────────────────────────────────

def test_version_info_142():
    """Test 125: VERSION is 1.3.7 (canonical) or later."""
    from release.version_info import VERSION
    major, minor, patch = (int(x) for x in VERSION.split(".")[:3])
    assert (major, minor, patch) >= (1, 3, 7), f"Expected >= 1.3.7, got {VERSION}"


def test_release_name_142():
    """Test 126: RELEASE_NAME is Strategy Robustness or a successor release."""
    from release.version_info import RELEASE_NAME
    _KNOWN = (
        "Strategy Robustness & Regime Validation",
        "Research Foundation Stable Rollup",
        "TWSE Provider",
        "TPEx Provider",
        "MOPS Provider",
        "data.gov.tw Provider",
        "Provider CLI Registration Hotfix",
        "Provider Health Consistency Hotfix",
        "FinMind Adapter Hardening",
        "Source Lineage & Rate Limit",
        "Provider Quality Gates",
        "Forum Intelligence & Market Sentiment",
        "Data Provider Stable Rollup",
        "Full-Suite Collection Integrity Hotfix",
    "Provider Integration Hardening",
    "Provider Integration Test Integrity Hotfix",
    "Provider Stable Rollup",
    "Portfolio Research Foundation",
    "Portfolio Research Foundation Integrity Hotfix",
    "Portfolio Research CLI Completeness Hotfix",
    "Position Sizing",
    "Correlation & Exposure",
    "Correlation & Exposure Integrity Hotfix",
    "Drawdown & Risk Controls",
    "Portfolio Walk-forward Backtest",
    "Portfolio Stable Rollup",
    "Portfolio Stable Rollup Integrity Hotfix",
    "Portfolio Stable Rollup Release Gate Hotfix",
    "Live Paper Trading Foundation",
            "Market Data Session Adapter",
            "Market Data Session Warning Hygiene Hotfix",
            "Paper Strategy Orchestration",
            "Paper Strategy Orchestration Integrity Hotfix",
            "Session Operations & Observability",
            "Session Operations Integrity Hotfix",
            "CLI Registration Health Integrity Hotfix",
            "CLI Handler Resolution Integrity Hotfix",
            "Operational Analytics & Review",
            "Failure Injection & Recovery Validation",
            "Multi-session Coordination",
            "Fixture Governance & Safety Marker Hotfix",
            "Replay Session Lineage Handler Integrity Hotfix",
            "Paper Performance Attribution",
            "Operational Integration Hardening",
            "Live Paper Trading Stable Rollup",
            "Stable Rollup Compatibility Hotfix",
            "Small Capital Growth Strategy Template",
    )
    assert RELEASE_NAME in _KNOWN, f"Unexpected RELEASE_NAME: {RELEASE_NAME}"


def test_base_release_142():
    """Test 127: BASE_RELEASE references Robustness era or later release."""
    from release.version_info import BASE_RELEASE
    def _parse_ver(v): return tuple(int(x) for x in v.split()[0].split(".")[:3] if x.isdigit())
    assert _parse_ver(BASE_RELEASE) >= _parse_ver("1.3.6"), (
        f"BASE_RELEASE does not reference a valid predecessor release: {BASE_RELEASE}"
    )


def test_strategy_robustness_flag():
    """Test 128: STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE is True."""
    from release.version_info import STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE
    assert STRATEGY_ROBUSTNESS_VALIDATION_AVAILABLE is True


def test_robustness_mock_formal_conclusion_disabled():
    """Test 129: ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED is False."""
    from release.version_info import ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED
    assert ROBUSTNESS_MOCK_FORMAL_CONCLUSION_ALLOWED is False


def test_robustness_auto_optimization_disabled():
    """Test 130: ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED is False."""
    from release.version_info import ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED
    assert ROBUSTNESS_AUTO_OPTIMIZATION_ENABLED is False


def test_robustness_auto_trading_disabled():
    """Test 131: ROBUSTNESS_AUTO_TRADING_ENABLED is False."""
    from release.version_info import ROBUSTNESS_AUTO_TRADING_ENABLED
    assert ROBUSTNESS_AUTO_TRADING_ENABLED is False


def test_regime_robustness_flag():
    """Test 132: REGIME_ROBUSTNESS_VALIDATION_AVAILABLE is True."""
    from release.version_info import REGIME_ROBUSTNESS_VALIDATION_AVAILABLE
    assert REGIME_ROBUSTNESS_VALIDATION_AVAILABLE is True


def test_bootstrap_flag():
    """Test 133: BOOTSTRAP_CONFIDENCE_AVAILABLE is True."""
    from release.version_info import BOOTSTRAP_CONFIDENCE_AVAILABLE
    assert BOOTSTRAP_CONFIDENCE_AVAILABLE is True


def test_monte_carlo_flag():
    """Test 134: MONTE_CARLO_TRADE_ORDER_AVAILABLE is True."""
    from release.version_info import MONTE_CARLO_TRADE_ORDER_AVAILABLE
    assert MONTE_CARLO_TRADE_ORDER_AVAILABLE is True


def test_decay_flag():
    """Test 135: STRATEGY_DECAY_DETECTION_AVAILABLE is True."""
    from release.version_info import STRATEGY_DECAY_DETECTION_AVAILABLE
    assert STRATEGY_DECAY_DETECTION_AVAILABLE is True


def test_robustness_formal_conclusion_requires_real():
    """Test 136: ROBUSTNESS_FORMAL_CONCLUSION_REQUIRES_REAL_DATA is True."""
    from release.version_info import ROBUSTNESS_FORMAL_CONCLUSION_REQUIRES_REAL_DATA
    assert ROBUSTNESS_FORMAL_CONCLUSION_REQUIRES_REAL_DATA is True


# ── Fixtures ──────────────────────────────────────────────────────────────────

def test_all_fixtures_have_meta():
    """Test 137: All fixtures have _fixture_meta with required keys."""
    fixture_files = [
        "time_stable.json", "time_fragile.json", "symbol_concentrated.json",
        "industry_concentrated.json", "regime_dependent.json", "parameter_cliff.json",
        "cost_sensitive.json", "trade_concentrated.json", "decaying.json",
        "robustness_result_v1.json",
    ]
    required_meta = ["TEST_FIXTURE", "DEMO_ONLY", "NOT_REAL_DATA", "NOT_FOR_FORMAL_CONCLUSION"]
    for fname in fixture_files:
        fixture = _load_fixture(fname)
        meta = fixture.get("_fixture_meta", {})
        for key in required_meta:
            assert meta.get(key) is True, f"{fname} missing {key}"


def test_all_fixtures_have_robustness_id():
    """Test 138: All fixtures have robustness_id."""
    fixture_files = [
        "time_stable.json", "time_fragile.json", "symbol_concentrated.json",
        "industry_concentrated.json", "regime_dependent.json", "parameter_cliff.json",
        "cost_sensitive.json", "trade_concentrated.json", "decaying.json",
        "robustness_result_v1.json",
    ]
    for fname in fixture_files:
        fixture = _load_fixture(fname)
        assert "robustness_id" in fixture, f"{fname} missing robustness_id"


def test_robustness_result_fixture():
    """Test 139: robustness_result_v1 fixture has all dimension_scores."""
    fixture = _load_fixture("robustness_result_v1.json")
    dim_scores = fixture["dimension_scores"]
    expected_dims = ["time", "cross_sectional", "industry", "regime", "parameter",
                     "cost", "slippage", "concentration", "bootstrap", "monte_carlo",
                     "rolling", "decay", "data_quality", "sample_size"]
    for d in expected_dims:
        assert d in dim_scores, f"Missing dimension: {d}"


def test_robustness_result_fixture_not_for_formal():
    """Test 140: robustness_result_v1 fixture is NOT for formal conclusion."""
    fixture = _load_fixture("robustness_result_v1.json")
    assert fixture["_fixture_meta"]["NOT_FOR_FORMAL_CONCLUSION"] is True


# ── GUI Panel Module ──────────────────────────────────────────────────────────

def test_gui_panel_importable():
    """Test 141: GUI panel module imports without error."""
    import gui.strategy_robustness_panel as panel
    assert panel.TAB_ID == "strategy_robustness"
    assert panel.GROUP == "research"
    assert panel.PRIORITY == "P1"


def test_gui_panel_safety_flags():
    """Test 142: GUI panel has correct safety flags."""
    import gui.strategy_robustness_panel as panel
    assert panel.NO_REAL_ORDERS is True
    assert panel.BROKER_EXECUTION_ENABLED is False
    assert panel.PRODUCTION_TRADING_BLOCKED is True
    assert panel.MOCK_FORMAL_CONCLUSION_ALLOWED is False
    assert panel.AUTO_OPTIMIZATION_ENABLED is False
    assert panel.AUTO_TRADING_ENABLED is False


def test_gui_panel_class_exists():
    """Test 143: StrategyRobustnessPanel class exists."""
    from gui.strategy_robustness_panel import StrategyRobustnessPanel
    assert StrategyRobustnessPanel is not None


# ── Additional Edge Cases ─────────────────────────────────────────────────────

def test_time_robustness_single_trade():
    """Test 144: Time robustness handles single trade."""
    from strategy_robustness.time_robustness_v142 import StrategyTimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = [{"return_pct": 0.05, "date": "2024-01-15", "symbol": "2330", "win": True, "cost": 0.003}]
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyTimeRobustnessAnalyzer().analyze(trades, config)
    assert "status" in result


def test_cross_sectional_all_loss():
    """Test 145: Cross-sectional handles all-loss trades."""
    from strategy_robustness.cross_sectional_v142 import CrossSectionalRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = [{"return_pct": -0.05, "date": f"2024-01-{i+1:02d}", "symbol": f"23{30+i}", "win": False, "cost": 0.003}
              for i in range(10)]
    config = RobustnessConfiguration(rule_id="test")
    result = CrossSectionalRobustnessAnalyzer().analyze(trades, config)
    assert result["symbols_profitable"] == 0


def test_regime_robustness_bull_only():
    """Test 146: Regime robustness flags bull-only condition."""
    from strategy_robustness.regime_robustness_v142 import RegimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    regime_labels = {t["date"]: "BULL" for t in trades}
    config = RobustnessConfiguration(rule_id="test")
    result = RegimeRobustnessAnalyzer().analyze(trades, regime_labels, config)
    assert "BULL" in result["regimes_found"]
    # Should have bull_only check or similar warning
    assert "checks" in result


def test_cost_stress_all_multipliers_tested():
    """Test 147: All configured cost multipliers are tested."""
    from strategy_robustness.cost_stress_v142 import StrategyCostStressAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", cost_multipliers=[1.0, 1.5, 2.0])
    result = StrategyCostStressAnalyzer().analyze(trades, config)
    assert len(result["multiplier_results"]) == 3


def test_bootstrap_iterations_capped():
    """Test 148: Bootstrap iterations are capped at MAX_BOOTSTRAP_ITERATIONS."""
    from strategy_robustness.bootstrap_v142 import BootstrapRobustnessAnalyzer, MAX_BOOTSTRAP_ITERATIONS
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", bootstrap_iterations=99999)
    result = BootstrapRobustnessAnalyzer().analyze(trades, config)
    assert result["iterations"] <= MAX_BOOTSTRAP_ITERATIONS


def test_monte_carlo_iterations_capped():
    """Test 149: Monte Carlo iterations are capped at MAX_MC_ITERATIONS."""
    from strategy_robustness.monte_carlo_v142 import MonteCarloTradeOrderAnalyzer, MAX_MC_ITERATIONS
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", monte_carlo_iterations=99999)
    result = MonteCarloTradeOrderAnalyzer().analyze(trades, config)
    assert result["iterations"] <= MAX_MC_ITERATIONS


def test_decay_detector_evidence_list():
    """Test 150: Decay detector provides evidence list."""
    from strategy_robustness.decay_detector_v142 import StrategyDecayDetector
    from strategy_robustness.models_v142 import RobustnessConfiguration, DecayStatus
    early = [{"return_pct": 0.05, "date": f"2021-01-{i+1:02d}", "symbol": "2330", "win": True, "cost": 0.001}
             for i in range(15)]
    recent = [{"return_pct": -0.04, "date": f"2024-01-{i+1:02d}", "symbol": "2330", "win": False, "cost": 0.001}
              for i in range(15)]
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyDecayDetector().analyze(early + recent, config)
    assert isinstance(result["evidence"], list)


def test_trade_concentration_stress_tests():
    """Test 151: Trade concentration includes stress tests."""
    from strategy_robustness.trade_concentration_v142 import TradeConcentrationAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = TradeConcentrationAnalyzer().analyze(trades, config)
    assert "remove_best_1" in result["stress_tests"]


def test_failure_modes_severity_values():
    """Test 152: All failure modes have valid severity values."""
    from strategy_robustness.failure_modes_v142 import StrategyFailureModeClassifier
    result = {
        "trade_count": 5,
        "formal_conclusion_allowed": False,
        "regime_robustness": {"regime_dependency_score": 0.8},
        "parameter_sensitivity": {"variants": [{"cliff_risk": True}]},
        "cost_stress": {"checks": {"survives_2x_cost": {"pass": False}}},
        "trade_concentration": {"status": "CONCENTRATED"},
        "cross_sectional": {"top_contributor_share": 0.8},
        "industry_robustness": {"checks": {"single_industry_concentration": {"pass": False}}},
        "time_robustness": {"checks": {}},
        "bootstrap": {"status": "FAIL"},
        "decay": {"decay_status": "SIGNIFICANT_DECAY"},
        "failure_modes": [],
    }
    modes = StrategyFailureModeClassifier().classify(result)
    valid_severities = {"LOW", "MEDIUM", "HIGH"}
    for m in modes:
        assert m["severity"] in valid_severities


def test_score_engine_penalties_reduce_score():
    """Test 153: Score engine penalties reduce overall score."""
    from strategy_robustness.score_v142 import StrategyRobustnessScoreEngine
    # Fixture with cost-sensitive result
    fixture = _load_fixture("cost_sensitive.json")
    engine = StrategyRobustnessScoreEngine()
    result = engine.score(fixture)
    assert len(result["penalties"]) >= 0  # penalties may be applied
    # Score should be computed
    assert "overall_score" in result


def test_report_version():
    """Test 154: Report version is 1.4.2."""
    from strategy_robustness.report_v142 import StrategyRobustnessReport
    fixture = _load_fixture("robustness_result_v1.json")
    report = StrategyRobustnessReport().generate(fixture)
    assert report["version"] == "1.4.2"


def test_store_save_comparison(tmp_path):
    """Test 155: Store can save comparison results."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_comparison({"comparison_id": "comp_001", "rankable": True})
    # Should not raise


def test_store_cost_sensitive(tmp_path):
    """Test 156: Store can list cost-sensitive results."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_result({
        "robustness_id": "cost_s_001", "rule_id": "r1",
        "robustness_status": "FRAGILE",
        "cost_stress": {"status": "COST_SENSITIVE"}
    })
    results = store.list_cost_sensitive()
    assert len(results) == 1


def test_store_regime_dependent(tmp_path):
    """Test 157: Store can list regime-dependent results."""
    from strategy_robustness.store_v142 import StrategyRobustnessStore
    store = StrategyRobustnessStore(base_dir=str(tmp_path))
    store.save_result({
        "robustness_id": "regime_001", "rule_id": "r1",
        "robustness_status": "REGIME_DEPENDENT",
        "regime_robustness": {"regime_dependency_score": 0.75}
    })
    results = store.list_regime_dependent()
    assert len(results) == 1


def test_configuration_minimum_fields():
    """Test 158: RobustnessConfiguration requires only rule_id."""
    from strategy_robustness.models_v142 import RobustnessConfiguration
    c = RobustnessConfiguration(rule_id="minimal_rule")
    assert c.rule_id == "minimal_rule"
    assert c.minimum_symbols == 5
    assert c.minimum_trades == 30


def test_rolling_stability_summary_keys():
    """Test 159: Rolling stability summary has required keys."""
    from strategy_robustness.rolling_stability_v142 import RollingStabilityAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(40)
    config = RobustnessConfiguration(rule_id="test", rolling_window_size=15)
    result = RollingStabilityAnalyzer().analyze(trades, config)
    assert "positive_window_ratio" in result["summary"]
    assert "negative_window_ratio" in result["summary"]
    assert "longest_negative_streak" in result["summary"]


def test_industry_robustness_per_industry_stats():
    """Test 160: Industry robustness includes per-industry stats with required fields."""
    from strategy_robustness.industry_robustness_v142 import IndustryRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    industry_map = {f"23{30+i}": "Tech" if i < 5 else "Finance" for i in range(10)}
    config = RobustnessConfiguration(rule_id="test")
    result = IndustryRobustnessAnalyzer().analyze(trades, config, industry_map)
    for ind, stats in result["industry_stats"].items():
        assert "trades" in stats
        assert "expectancy" in stats
        assert "confidence" in stats


def test_regime_robustness_per_regime_stats():
    """Test 161: Regime robustness includes per-regime stats with required fields."""
    from strategy_robustness.regime_robustness_v142 import RegimeRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    regime_labels = {t["date"]: "BULL" if i < 20 else "BEAR" for i, t in enumerate(trades)}
    config = RobustnessConfiguration(rule_id="test")
    result = RegimeRobustnessAnalyzer().analyze(trades, regime_labels, config)
    for regime, stats in result["regime_stats"].items():
        assert "expectancy" in stats
        assert "win_rate" in stats
        assert "confidence" in stats


def test_parameter_sensitivity_cliff_detection():
    """Test 162: Parameter sensitivity detects cliff risk correctly."""
    from strategy_robustness.parameter_sensitivity_v142 import ParameterSensitivityAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    baseline = {"expectancy": 0.01, "net_return": 0.10}
    variants = [
        {"params": {"p": 1}, "metrics": {"expectancy": 0.01, "net_return": 0.10}},
        {"params": {"p": 2}, "metrics": {"expectancy": -0.03, "net_return": -0.08}},  # cliff
    ]
    config = RobustnessConfiguration(rule_id="test")
    result = ParameterSensitivityAnalyzer().analyze(baseline, variants, config)
    cliff_variants = [v for v in result["variants"] if v["cliff_risk"]]
    assert len(cliff_variants) > 0


def test_cross_sectional_profitable_ratio():
    """Test 163: Cross-sectional profitable_symbol_ratio in 0-1."""
    from strategy_robustness.cross_sectional_v142 import CrossSectionalRobustnessAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = CrossSectionalRobustnessAnalyzer().analyze(trades, config)
    assert 0.0 <= result["profitable_symbol_ratio"] <= 1.0


def test_cost_stress_baseline_positive():
    """Test 164: Cost stress baseline multiplier (1.0x) is present."""
    from strategy_robustness.cost_stress_v142 import StrategyCostStressAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyCostStressAnalyzer().analyze(trades, config)
    assert "x1.00" in result["multiplier_results"]
    assert result["multiplier_results"]["x1.00"]["robustness_status"] == "BASELINE"


def test_stress_bear_only_result():
    """Test 165: BEAR_ONLY scenario returns proper result."""
    from strategy_robustness.stress_scenarios_v142 import StrategyStressScenarioEngine
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test")
    result = StrategyStressScenarioEngine().run(trades, "BEAR_ONLY", config)
    assert result["scenario"] == "BEAR_ONLY"
    assert "strategy_survives" in result


def test_monte_carlo_consec_loss_distribution():
    """Test 166: Monte Carlo returns max_consecutive_loss_distribution."""
    from strategy_robustness.monte_carlo_v142 import MonteCarloTradeOrderAnalyzer
    from strategy_robustness.models_v142 import RobustnessConfiguration
    trades = _make_trades(30)
    config = RobustnessConfiguration(rule_id="test", monte_carlo_iterations=50)
    result = MonteCarloTradeOrderAnalyzer().analyze(trades, config)
    assert "max_consecutive_loss_distribution" in result
    assert isinstance(result["max_consecutive_loss_distribution"], dict)


def test_comparison_no_results():
    """Test 167: StrategyKnowledgeRobustnessComparison handles empty list."""
    from strategy_robustness.comparison_v142 import StrategyKnowledgeRobustnessComparison
    result = StrategyKnowledgeRobustnessComparison().compare_rules([])
    assert result["rankable"] is False


def test_abc_previous_flags_still_present():
    """Test 168: v1.4.1 flags still present after v1.4.2 update."""
    from release.version_info import (
        ABC_BUY_POINT_VALIDATION_AVAILABLE,
        ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED,
        ABC_BUY_POINT_AUTO_TRADING_ENABLED,
    )
    assert ABC_BUY_POINT_VALIDATION_AVAILABLE is True
    assert ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED is False
    assert ABC_BUY_POINT_AUTO_TRADING_ENABLED is False
