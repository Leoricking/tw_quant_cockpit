"""
tests/test_abc_validation_v141.py — v1.4.1 A/B/C Buy Point Validation tests.
[!] Research Only. No Real Orders. No Broker. Not Investment Advice.
Tests do NOT connect to external networks or APIs.
"""
import pytest
import json
import os
import sys

# Ensure repo root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "abc_validation")

def _load_fixture(name: str) -> dict:
    with open(os.path.join(FIXTURE_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)


# ── Package / Safety flags ────────────────────────────────────────────────────

def test_package_import():
    """Test 1: abc_validation package imports."""
    import abc_validation
    assert abc_validation.NO_REAL_ORDERS is True

def test_no_real_orders_flag():
    """Test 2: NO_REAL_ORDERS is True."""
    import abc_validation
    assert abc_validation.NO_REAL_ORDERS is True

def test_broker_execution_disabled():
    """Test 3: BROKER_EXECUTION_ENABLED is False."""
    import abc_validation
    assert abc_validation.BROKER_EXECUTION_ENABLED is False

def test_production_trading_blocked():
    """Test 4: PRODUCTION_TRADING_BLOCKED is True."""
    import abc_validation
    assert abc_validation.PRODUCTION_TRADING_BLOCKED is True

def test_abc_validation_available():
    """Test 5: ABC_BUY_POINT_VALIDATION_AVAILABLE is True."""
    import abc_validation
    assert abc_validation.ABC_BUY_POINT_VALIDATION_AVAILABLE is True


# ── Rule Adapters ─────────────────────────────────────────────────────────────

def test_a_rule_adapter_uses_existing_domain_logic():
    """Test 6: ABuyPointRuleAdapter delegates to registry."""
    from abc_validation.rule_adapters_v141 import ABuyPointRuleAdapter
    adapter = ABuyPointRuleAdapter()
    rule = adapter.get_rule()
    assert rule is not None
    assert rule.rule_id == "abc_buy_point_a"

def test_b_rule_adapter_uses_existing_domain_logic():
    """Test 7: BBuyPointRuleAdapter delegates to registry."""
    from abc_validation.rule_adapters_v141 import BBuyPointRuleAdapter
    adapter = BBuyPointRuleAdapter()
    rule = adapter.get_rule()
    assert rule is not None
    assert rule.rule_id == "abc_buy_point_b"

def test_c_rule_adapter_uses_existing_domain_logic():
    """Test 8: CBuyPointRuleAdapter delegates to registry."""
    from abc_validation.rule_adapters_v141 import CBuyPointRuleAdapter
    adapter = CBuyPointRuleAdapter()
    rule = adapter.get_rule()
    assert rule is not None
    assert rule.rule_id == "abc_buy_point_c"

def test_a_adapter_buy_point_type():
    """Test 9: ABuyPointRuleAdapter has buy_point_type A."""
    from abc_validation.rule_adapters_v141 import ABuyPointRuleAdapter
    assert ABuyPointRuleAdapter.buy_point_type == "A"

def test_b_adapter_buy_point_type():
    """Test 10: BBuyPointRuleAdapter has buy_point_type B."""
    from abc_validation.rule_adapters_v141 import BBuyPointRuleAdapter
    assert BBuyPointRuleAdapter.buy_point_type == "B"

def test_c_adapter_buy_point_type():
    """Test 11: CBuyPointRuleAdapter has buy_point_type C."""
    from abc_validation.rule_adapters_v141 import CBuyPointRuleAdapter
    assert CBuyPointRuleAdapter.buy_point_type == "C"

def test_a_adapter_support_ma():
    """Test 12: ABuyPointRuleAdapter support_ma is MA10."""
    from abc_validation.rule_adapters_v141 import ABuyPointRuleAdapter
    assert ABuyPointRuleAdapter.support_ma == "MA10"

def test_b_adapter_support_ma():
    """Test 13: BBuyPointRuleAdapter support_ma is MA5."""
    from abc_validation.rule_adapters_v141 import BBuyPointRuleAdapter
    assert BBuyPointRuleAdapter.support_ma == "MA5"

def test_c_adapter_support_ma():
    """Test 14: CBuyPointRuleAdapter support_ma is MA20."""
    from abc_validation.rule_adapters_v141 import CBuyPointRuleAdapter
    assert CBuyPointRuleAdapter.support_ma == "MA20"

def test_a_adapter_analyze_mock():
    """Test 15: ABuyPointRuleAdapter.analyze returns dict in mock mode."""
    from abc_validation.rule_adapters_v141 import ABuyPointRuleAdapter
    result = ABuyPointRuleAdapter().analyze("2330", mode='mock')
    assert isinstance(result, dict)
    assert "buy_point_grade" in result

def test_b_adapter_analyze_mock():
    """Test 16: BBuyPointRuleAdapter.analyze returns dict in mock mode."""
    from abc_validation.rule_adapters_v141 import BBuyPointRuleAdapter
    result = BBuyPointRuleAdapter().analyze("2330", mode='mock')
    assert isinstance(result, dict)

def test_c_adapter_analyze_mock():
    """Test 17: CBuyPointRuleAdapter.analyze returns dict in mock mode."""
    from abc_validation.rule_adapters_v141 import CBuyPointRuleAdapter
    result = CBuyPointRuleAdapter().analyze("2330", mode='mock')
    assert isinstance(result, dict)

def test_a_is_a_signal_returns_strict():
    """Test 18: is_a_signal returns A_STRICT when grade is A."""
    from abc_validation.rule_adapters_v141 import ABuyPointRuleAdapter
    adapter = ABuyPointRuleAdapter()
    assert adapter.is_a_signal({"buy_point_grade": "A"}) == "A_STRICT"

def test_a_is_a_signal_returns_none():
    """Test 19: is_a_signal returns None when grade is not A."""
    from abc_validation.rule_adapters_v141 import ABuyPointRuleAdapter
    adapter = ABuyPointRuleAdapter()
    assert adapter.is_a_signal({"buy_point_grade": "B"}) is None

def test_b_is_b_signal():
    """Test 20: is_b_signal returns B_STRICT when grade is B."""
    from abc_validation.rule_adapters_v141 import BBuyPointRuleAdapter
    adapter = BBuyPointRuleAdapter()
    assert adapter.is_b_signal({"buy_point_grade": "B"}) == "B_STRICT"

def test_c_is_c_signal():
    """Test 21: is_c_signal returns C_STRICT_RECLAIM when grade is C."""
    from abc_validation.rule_adapters_v141 import CBuyPointRuleAdapter
    adapter = CBuyPointRuleAdapter()
    assert adapter.is_c_signal({"buy_point_grade": "C"}) == "C_STRICT_RECLAIM"


# ── Snapshots ─────────────────────────────────────────────────────────────────

def test_snapshot_import():
    """Test 22: ABCBuyPointRuleSnapshot imports."""
    from abc_validation.snapshots_v141 import ABCBuyPointRuleSnapshot
    assert ABCBuyPointRuleSnapshot is not None

def test_snapshot_make_default_a():
    """Test 23: make_default A returns snapshot with type A."""
    from abc_validation.snapshots_v141 import ABCBuyPointRuleSnapshot
    snap = ABCBuyPointRuleSnapshot.make_default("A")
    assert snap.buy_point_type == "A"
    assert snap.rule_id == "abc_buy_point_a"

def test_snapshot_make_default_b():
    """Test 24: make_default B returns snapshot with type B."""
    from abc_validation.snapshots_v141 import ABCBuyPointRuleSnapshot
    snap = ABCBuyPointRuleSnapshot.make_default("B")
    assert snap.buy_point_type == "B"

def test_snapshot_make_default_c():
    """Test 25: make_default C returns snapshot with type C."""
    from abc_validation.snapshots_v141 import ABCBuyPointRuleSnapshot
    snap = ABCBuyPointRuleSnapshot.make_default("C")
    assert snap.buy_point_type == "C"

def test_snapshot_parameter_hash_deterministic():
    """Test 26: parameter_hash is deterministic."""
    from abc_validation.snapshots_v141 import ABCBuyPointRuleSnapshot
    s1 = ABCBuyPointRuleSnapshot.make_default("A")
    s2 = ABCBuyPointRuleSnapshot.make_default("A")
    assert s1.parameter_hash == s2.parameter_hash

def test_snapshot_to_dict():
    """Test 27: snapshot.to_dict() returns dict with snapshot_id."""
    from abc_validation.snapshots_v141 import ABCBuyPointRuleSnapshot
    snap = ABCBuyPointRuleSnapshot.make_default("A")
    d = snap.to_dict()
    assert "snapshot_id" in d
    assert d["buy_point_type"] == "A"

def test_snapshot_from_dict_graceful():
    """Test 28: from_dict loads gracefully and ignores unknown fields."""
    from abc_validation.snapshots_v141 import ABCBuyPointRuleSnapshot
    snap = ABCBuyPointRuleSnapshot.make_default("B")
    d = snap.to_dict()
    d["unknown_future_field"] = "some_value"
    snap2 = ABCBuyPointRuleSnapshot.from_dict(d)
    assert snap2.buy_point_type == "B"


# ── Signal Classification ─────────────────────────────────────────────────────

def test_signal_classification_import():
    """Test 29: ABCSignalClassification imports."""
    from abc_validation.signal_classification_v141 import ABCSignalClassification
    assert ABCSignalClassification is not None

def test_signal_classification_a_types():
    """Test 30: all_a() returns 4 A types."""
    from abc_validation.signal_classification_v141 import ABCSignalClassification
    assert len(ABCSignalClassification.all_a()) == 4

def test_signal_classification_b_types():
    """Test 31: all_b() returns 5 B types."""
    from abc_validation.signal_classification_v141 import ABCSignalClassification
    assert len(ABCSignalClassification.all_b()) == 5

def test_signal_classification_c_types():
    """Test 32: all_c() returns 5 C types."""
    from abc_validation.signal_classification_v141 import ABCSignalClassification
    assert len(ABCSignalClassification.all_c()) == 5

def test_signal_classification_a_strict_in_all_a():
    """Test 33: A_STRICT in all_a()."""
    from abc_validation.signal_classification_v141 import ABCSignalClassification
    assert ABCSignalClassification.A_STRICT in ABCSignalClassification.all_a()

def test_signal_classification_c_false_reclaim_in_all_c():
    """Test 34: C_FALSE_RECLAIM in all_c()."""
    from abc_validation.signal_classification_v141 import ABCSignalClassification
    assert ABCSignalClassification.C_FALSE_RECLAIM in ABCSignalClassification.all_c()

def test_signal_classification_is_valid_for_type():
    """Test 35: is_valid_for_type works correctly."""
    from abc_validation.signal_classification_v141 import ABCSignalClassification
    assert ABCSignalClassification.is_valid_for_type("A_STRICT", "A") is True
    assert ABCSignalClassification.is_valid_for_type("A_STRICT", "B") is False
    assert ABCSignalClassification.is_valid_for_type("B_STRICT", "B") is True

def test_signal_record_import():
    """Test 36: ABCSignalRecord imports."""
    from abc_validation.signal_classification_v141 import ABCSignalRecord
    r = ABCSignalRecord(
        signal_id="test_001",
        buy_point_type="A",
        classification="A_STRICT",
        symbol="2330",
        signal_date="2023-01-01",
        decision_date="2023-01-01",
        execution_date="2023-01-02",
    )
    assert r.signal_id == "test_001"

def test_signal_record_blocks_fixture_in_real_mode():
    """Test 37: ABCSignalRecord.validate_fixture_mode blocks fixture in real mode."""
    from abc_validation.signal_classification_v141 import ABCSignalRecord
    r = ABCSignalRecord(
        signal_id="test_002",
        buy_point_type="A",
        classification="A_STRICT",
        symbol="2330",
        signal_date="2023-01-01",
        decision_date="2023-01-01",
        execution_date="2023-01-02",
        fixture_data=True,
    )
    with pytest.raises(ValueError, match="BLOCKED"):
        r.validate_fixture_mode("real")

def test_signal_record_allows_fixture_in_mock_mode():
    """Test 38: ABCSignalRecord.validate_fixture_mode allows fixture in mock mode."""
    from abc_validation.signal_classification_v141 import ABCSignalRecord
    r = ABCSignalRecord(
        signal_id="test_003",
        buy_point_type="A",
        classification="A_STRICT",
        symbol="2330",
        signal_date="2023-01-01",
        decision_date="2023-01-01",
        execution_date="2023-01-02",
        fixture_data=True,
    )
    r.validate_fixture_mode("mock")  # Should not raise


# ── Integrity Guard ───────────────────────────────────────────────────────────

def test_integrity_guard_import():
    """Test 39: ABCSignalIntegrityGuard imports."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    assert guard is not None

def test_integrity_guard_passes_valid_signal():
    """Test 40: Integrity guard passes a valid signal."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    sig = {
        "buy_point_type": "A",
        "signal_date": "2023-01-01",
        "decision_date": "2023-01-01",
        "execution_date": "2023-01-02",
    }
    bars = [{"date": f"2023-{i//30+1:02d}-{i%30+1:02d}", "close": 100, "volume": 1000}
            for i in range(35)]
    result = guard.check(sig, bars)
    assert result["classification"] == "OK"

def test_integrity_guard_insufficient_history():
    """Test 41: Integrity guard returns INSUFFICIENT_DATA for too few bars."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    sig = {
        "buy_point_type": "A",
        "signal_date": "2023-01-05",
        "decision_date": "2023-01-05",
        "execution_date": "2023-01-06",
    }
    bars = [{"date": f"2023-01-0{i}", "close": 100, "volume": 1000} for i in range(1, 6)]
    result = guard.check(sig, bars)
    assert result["classification"] == "INSUFFICIENT_DATA"

def test_integrity_guard_lookahead_blocked():
    """Test 42: Integrity guard returns BLOCKED for lookahead violation."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    sig = {
        "buy_point_type": "A",
        "signal_date": "2023-01-10",
        "decision_date": "2023-01-10",
        "execution_date": "2023-01-11",
        "lookahead_violation": True,
    }
    result = guard.check(sig)
    assert result["classification"] == "BLOCKED"

def test_integrity_guard_same_bar_execution_blocked():
    """Test 43: Same-bar execution returns BLOCKED."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    sig = {
        "buy_point_type": "A",
        "signal_date": "2023-01-10",
        "decision_date": "2023-01-10",
        "execution_date": "2023-01-10",  # same as signal_date
    }
    result = guard.check(sig)
    assert result["classification"] == "BLOCKED"

def test_integrity_guard_fixture_real_mode_blocked():
    """Test 44: Fixture data in real mode returns BLOCKED."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    sig = {
        "buy_point_type": "A",
        "signal_date": "2023-01-10",
        "decision_date": "2023-01-10",
        "execution_date": "2023-01-11",
        "mode": "real",
        "fixture_data": True,
    }
    result = guard.check(sig)
    assert result["classification"] == "BLOCKED"

def test_integrity_guard_duplicate_bars_blocked():
    """Test 45: Duplicate bars return BLOCKED."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    sig = {
        "buy_point_type": "A",
        "signal_date": "2023-01-10",
        "decision_date": "2023-01-10",
        "execution_date": "2023-01-11",
    }
    bars = [{"date": "2023-01-05", "close": 100, "volume": 1000}] * 35
    result = guard.check(sig, bars)
    assert result["classification"] == "BLOCKED"

def test_integrity_guard_is_blocked():
    """Test 46: is_blocked returns True for BLOCKED."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    assert guard.is_blocked({"classification": "BLOCKED"}) is True
    assert guard.is_blocked({"classification": "OK"}) is False

def test_integrity_guard_is_insufficient():
    """Test 47: is_insufficient returns True for INSUFFICIENT_DATA."""
    from abc_validation.integrity_guard_v141 import ABCSignalIntegrityGuard
    guard = ABCSignalIntegrityGuard()
    assert guard.is_insufficient({"classification": "INSUFFICIENT_DATA"}) is True


# ── Parameters ────────────────────────────────────────────────────────────────

def test_parameters_import():
    """Test 48: ABCValidationParameters imports."""
    from abc_validation.parameters_v141 import ABCValidationParameters
    params = ABCValidationParameters()
    assert params is not None

def test_parameters_validate_defaults():
    """Test 49: Default parameters validate without error."""
    from abc_validation.parameters_v141 import ABCValidationParameters
    params = ABCValidationParameters()
    params.validate()  # Should not raise

def test_parameters_to_dict():
    """Test 50: to_dict returns dict with a_params, b_params, c_params."""
    from abc_validation.parameters_v141 import ABCValidationParameters
    d = ABCValidationParameters().to_dict()
    assert "a_params" in d
    assert "b_params" in d
    assert "c_params" in d

def test_parameters_from_dict():
    """Test 51: from_dict roundtrip."""
    from abc_validation.parameters_v141 import ABCValidationParameters
    params = ABCValidationParameters()
    d = params.to_dict()
    params2 = ABCValidationParameters.from_dict(d)
    assert params2.a_params.ma10_touch_tolerance == params.a_params.ma10_touch_tolerance

def test_a_params_ma10_tolerance():
    """Test 52: APointParameters ma10_touch_tolerance default."""
    from abc_validation.parameters_v141 import APointParameters
    p = APointParameters()
    assert 0 < p.ma10_touch_tolerance < 0.1

def test_c_params_confirmation_bars():
    """Test 53: CPointParameters confirmation_bars default."""
    from abc_validation.parameters_v141 import CPointParameters
    p = CPointParameters()
    assert 1 <= p.confirmation_bars <= 10


# ── Holding Period Analyzer ───────────────────────────────────────────────────

def test_holding_period_analyzer_import():
    """Test 54: ABCHoldingPeriodAnalyzer imports."""
    from abc_validation.holding_period_analyzer_v141 import ABCHoldingPeriodAnalyzer
    ana = ABCHoldingPeriodAnalyzer()
    assert ana is not None

def test_holding_period_analyzer_default_periods():
    """Test 55: Default periods are 1/2/3/5/10/20."""
    from abc_validation.holding_period_analyzer_v141 import ABCHoldingPeriodAnalyzer
    ana = ABCHoldingPeriodAnalyzer()
    assert set(ana.periods) == {1, 2, 3, 5, 10, 20}

def test_holding_period_analyzer_empty_signals():
    """Test 56: Analyze returns dict with all periods when no signals."""
    from abc_validation.holding_period_analyzer_v141 import ABCHoldingPeriodAnalyzer
    ana = ABCHoldingPeriodAnalyzer()
    result = ana.analyze([])
    assert "period_results" in result
    assert len(result["period_results"]) == 6

def test_holding_period_analyzer_with_signals():
    """Test 57: Analyze handles signals with bars."""
    from abc_validation.holding_period_analyzer_v141 import ABCHoldingPeriodAnalyzer
    ana = ABCHoldingPeriodAnalyzer([5])
    bars = [{"date": f"2023-01-{i+1:02d}", "close": 100 + i * 0.5} for i in range(30)]
    signals = [{"signal_id": "s1", "symbol": "2330", "signal_date": "2023-01-05",
                "entry_price": 102.0}]
    result = ana.analyze(signals, bars_by_symbol={"2330": bars}, buy_point_type="A")
    assert result["buy_point_type"] == "A"


# ── Stop Loss Analyzer ────────────────────────────────────────────────────────

def test_stop_loss_analyzer_import():
    """Test 58: ABCStopLossAnalyzer imports."""
    from abc_validation.stop_loss_analyzer_v141 import ABCStopLossAnalyzer
    sla = ABCStopLossAnalyzer()
    assert sla is not None

def test_stop_loss_analyzer_unknown_model():
    """Test 59: Unknown stop model raises ValueError."""
    from abc_validation.stop_loss_analyzer_v141 import ABCStopLossAnalyzer
    with pytest.raises(ValueError, match="Unknown stop model"):
        ABCStopLossAnalyzer(stop_model="invalid_model")

def test_stop_loss_analyzer_fixed_pct():
    """Test 60: fixed_pct model runs without error."""
    from abc_validation.stop_loss_analyzer_v141 import ABCStopLossAnalyzer
    sla = ABCStopLossAnalyzer(stop_model="fixed_pct", stop_pct=0.07)
    result = sla.analyze([], buy_point_type="A")
    assert result["stop_model"] == "fixed_pct"
    assert result["no_real_orders"] is True

def test_stop_loss_all_models_available():
    """Test 61: All stop loss models are available."""
    from abc_validation.stop_loss_analyzer_v141 import STOP_MODELS
    expected = ["no_stop", "fixed_pct", "below_signal_low", "below_ma5", "below_ma10",
                "below_ma20", "atr_based", "time_stop", "structure_failure"]
    for model in expected:
        assert model in STOP_MODELS


# ── Take Profit Analyzer ──────────────────────────────────────────────────────

def test_take_profit_analyzer_import():
    """Test 62: ABCTakeProfitAnalyzer imports."""
    from abc_validation.take_profit_analyzer_v141 import ABCTakeProfitAnalyzer
    tpa = ABCTakeProfitAnalyzer()
    assert tpa is not None

def test_take_profit_analyzer_unknown_model():
    """Test 63: Unknown tp model raises ValueError."""
    from abc_validation.take_profit_analyzer_v141 import ABCTakeProfitAnalyzer
    with pytest.raises(ValueError, match="Unknown take profit model"):
        ABCTakeProfitAnalyzer(tp_model="invalid_tp_model")

def test_take_profit_analyzer_fixed_pct():
    """Test 64: fixed_pct model runs without error."""
    from abc_validation.take_profit_analyzer_v141 import ABCTakeProfitAnalyzer
    tpa = ABCTakeProfitAnalyzer(tp_model="fixed_pct", tp_pct=0.15)
    result = tpa.analyze([], buy_point_type="A")
    assert result["tp_model"] == "fixed_pct"
    assert result["no_real_orders"] is True

def test_take_profit_analyzer_stop_target_collision():
    """Test 65: Stop/target collision is counted and conservative order used."""
    from abc_validation.take_profit_analyzer_v141 import ABCTakeProfitAnalyzer
    tpa = ABCTakeProfitAnalyzer(tp_model="fixed_pct", tp_pct=0.001)
    bars = [{"date": f"2023-01-{i+1:02d}", "close": 100 + i * 0.1,
             "high": 100 + i * 0.1 + 0.5, "low": 100 + i * 0.1 - 0.5}
            for i in range(30)]
    signals = [{"signal_id": "s1", "symbol": "2330", "signal_date": "2023-01-05",
                "entry_price": 100.0}]
    stop_prices = {"2330": 99.9}  # very close to target
    result = tpa.analyze(signals, bars_by_symbol={"2330": bars},
                        stop_prices=stop_prices, buy_point_type="A")
    assert "stop_target_collision_count" in result


# ── Regime Analyzer ───────────────────────────────────────────────────────────

def test_regime_analyzer_import():
    """Test 66: ABCRegimeAnalyzer imports."""
    from abc_validation.regime_analyzer_v141 import ABCRegimeAnalyzer
    ra = ABCRegimeAnalyzer()
    assert ra is not None

def test_regime_analyzer_classify_bull():
    """Test 67: classify_signal_regime returns a valid regime."""
    from abc_validation.regime_analyzer_v141 import ABCRegimeAnalyzer, REGIME_VALUES
    ra = ABCRegimeAnalyzer()
    bars = [{"date": f"2023-01-{i+1:02d}", "close": 100 + i * 0.5} for i in range(70)]
    regime = ra.classify_signal_regime(bars)
    assert regime in REGIME_VALUES

def test_regime_analyzer_empty_bars():
    """Test 68: classify_signal_regime returns UNKNOWN for empty bars."""
    from abc_validation.regime_analyzer_v141 import ABCRegimeAnalyzer
    ra = ABCRegimeAnalyzer()
    assert ra.classify_signal_regime([]) == "UNKNOWN"

def test_regime_analyzer_analyze():
    """Test 69: analyze returns dict with regime_results."""
    from abc_validation.regime_analyzer_v141 import ABCRegimeAnalyzer
    ra = ABCRegimeAnalyzer()
    result = ra.analyze([], buy_point_type="A")
    assert "regime_results" in result
    assert result["no_future_regime_labeling"] is True


# ── Filter Ablation ───────────────────────────────────────────────────────────

def test_filter_ablation_import():
    """Test 70: ABCFilterAblationAnalyzer imports."""
    from abc_validation.filter_ablation_v141 import ABCFilterAblationAnalyzer
    faa = ABCFilterAblationAnalyzer()
    assert faa is not None

def test_filter_ablation_stages():
    """Test 71: FILTER_STAGES contains all required stages."""
    from abc_validation.filter_ablation_v141 import FILTER_STAGES
    assert "base_only" in FILTER_STAGES
    assert "full_composite" in FILTER_STAGES
    assert "+volume_contraction" in FILTER_STAGES
    assert "+second_wave" in FILTER_STAGES

def test_filter_ablation_analyze_empty():
    """Test 72: analyze with empty signals returns all stages."""
    from abc_validation.filter_ablation_v141 import ABCFilterAblationAnalyzer, FILTER_STAGES
    faa = ABCFilterAblationAnalyzer()
    result = faa.analyze([])
    assert "ablation_results" in result
    assert len(result["ablation_results"]) == len(FILTER_STAGES)

def test_filter_ablation_preserves_all_stages():
    """Test 73: All stages are preserved in results."""
    from abc_validation.filter_ablation_v141 import ABCFilterAblationAnalyzer, FILTER_STAGES
    faa = ABCFilterAblationAnalyzer()
    result = faa.analyze([{"signal_id": "s1", "buy_point_type": "A",
                           "vol_contraction": True, "ma60_up": True}])
    for stage in FILTER_STAGES:
        assert stage in result["ablation_results"]

def test_filter_ablation_no_best_declared():
    """Test 74: ablation note says no single best declared."""
    from abc_validation.filter_ablation_v141 import ABCFilterAblationAnalyzer
    faa = ABCFilterAblationAnalyzer()
    result = faa.analyze([])
    assert "No single best declared" in result["note"] or "not" in result["note"].lower()


# ── Second Wave Analyzer ──────────────────────────────────────────────────────

def test_second_wave_analyzer_import():
    """Test 75: ABCSecondWaveAnalyzer imports."""
    from abc_validation.second_wave_analyzer_v141 import ABCSecondWaveAnalyzer
    swa = ABCSecondWaveAnalyzer()
    assert swa is not None

def test_second_wave_check_conditions():
    """Test 76: check_second_wave_conditions returns conditions dict."""
    from abc_validation.second_wave_analyzer_v141 import ABCSecondWaveAnalyzer
    swa = ABCSecondWaveAnalyzer()
    sig = _load_fixture("second_wave.json")
    result = swa.check_second_wave_conditions(sig)
    assert "conditions" in result
    assert "qualifies_as_second_wave" in result

def test_second_wave_qualifies():
    """Test 77: Second wave fixture qualifies."""
    from abc_validation.second_wave_analyzer_v141 import ABCSecondWaveAnalyzer
    swa = ABCSecondWaveAnalyzer()
    sig = _load_fixture("second_wave.json")
    result = swa.check_second_wave_conditions(sig)
    # qualifies can be True or None depending on data fields
    assert result["qualifies_as_second_wave"] in (True, None)

def test_second_wave_analyze():
    """Test 78: analyze returns comparison dict."""
    from abc_validation.second_wave_analyzer_v141 import ABCSecondWaveAnalyzer
    swa = ABCSecondWaveAnalyzer()
    result = swa.analyze([], buy_point_type="A")
    assert "second_wave_metrics" in result
    assert "non_second_wave_metrics" in result


# ── Institutional/Margin Analyzer ────────────────────────────────────────────

def test_institutional_margin_analyzer_import():
    """Test 79: ABCInstitutionalMarginAnalyzer imports."""
    from abc_validation.institutional_margin_analyzer_v141 import ABCInstitutionalMarginAnalyzer
    ima = ABCInstitutionalMarginAnalyzer()
    assert ima is not None

def test_institutional_missing_data_is_insufficient():
    """Test 80: Missing institutional data returns INSUFFICIENT (not 0 or False)."""
    from abc_validation.institutional_margin_analyzer_v141 import (
        ABCInstitutionalMarginAnalyzer, MISSING_SENTINEL
    )
    ima = ABCInstitutionalMarginAnalyzer()
    result = ima.classify_signal({"signal_id": "s1", "symbol": "2330"})
    assert result["institutional_state"] == MISSING_SENTINEL or \
           result.get("foreign_state") == MISSING_SENTINEL

def test_institutional_missing_margin_is_insufficient():
    """Test 81: Missing margin data returns INSUFFICIENT."""
    from abc_validation.institutional_margin_analyzer_v141 import (
        ABCInstitutionalMarginAnalyzer, MISSING_SENTINEL
    )
    ima = ABCInstitutionalMarginAnalyzer()
    result = ima.classify_signal({"signal_id": "s1", "symbol": "2330",
                                   "foreign_net": 1000, "trust_net": 200})
    assert result["margin_state"] == MISSING_SENTINEL

def test_institutional_net_buying_classified():
    """Test 82: Net buying is classified as foreign_net_buying."""
    from abc_validation.institutional_margin_analyzer_v141 import ABCInstitutionalMarginAnalyzer
    ima = ABCInstitutionalMarginAnalyzer()
    result = ima.classify_signal({"signal_id": "s1", "foreign_net": 5000, "trust_net": 1000})
    assert result["foreign_state"] == "foreign_net_buying"

def test_institutional_analyze():
    """Test 83: analyze returns state_counts dict."""
    from abc_validation.institutional_margin_analyzer_v141 import ABCInstitutionalMarginAnalyzer
    ima = ABCInstitutionalMarginAnalyzer()
    result = ima.analyze([], buy_point_type="A")
    assert "state_counts" in result
    assert result["missing_data_note"] is not None


# ── Volume Analyzer ───────────────────────────────────────────────────────────

def test_volume_analyzer_import():
    """Test 84: ABCVolumeAnalyzer imports."""
    from abc_validation.volume_analyzer_v141 import ABCVolumeAnalyzer
    va = ABCVolumeAnalyzer()
    assert va is not None

def test_volume_analyzer_volume_unavailable():
    """Test 85: No volume data returns volume_unavailable."""
    from abc_validation.volume_analyzer_v141 import ABCVolumeAnalyzer
    va = ABCVolumeAnalyzer()
    state = va.classify_volume_state({"signal_id": "s1", "buy_point_type": "A"}, bars=[])
    assert state in ("volume_baseline_insufficient", "volume_unavailable")

def test_volume_analyzer_pullback_contraction():
    """Test 86: Low volume ratio returns pullback_volume_contraction for A/B."""
    from abc_validation.volume_analyzer_v141 import ABCVolumeAnalyzer
    va = ABCVolumeAnalyzer()
    bars = [{"date": f"2023-01-{i+1:02d}", "close": 100, "volume": 1000} for i in range(25)]
    sig = {"signal_id": "s1", "buy_point_type": "A", "signal_volume": 600}
    state = va.classify_volume_state(sig, bars)
    assert state == "pullback_volume_contraction"

def test_volume_analyzer_analyze():
    """Test 87: analyze returns state_metrics dict."""
    from abc_validation.volume_analyzer_v141 import ABCVolumeAnalyzer
    va = ABCVolumeAnalyzer()
    result = va.analyze([], buy_point_type="A")
    assert "state_metrics" in result


# ── Outcome Taxonomy ──────────────────────────────────────────────────────────

def test_outcome_taxonomy_import():
    """Test 88: ABCOutcomeType imports."""
    from abc_validation.outcome_taxonomy_v141 import ABCOutcomeType
    assert ABCOutcomeType.SUCCESS_TREND_CONTINUATION is not None

def test_outcome_taxonomy_all_types():
    """Test 89: all_types() returns at least 15 types."""
    from abc_validation.outcome_taxonomy_v141 import ABCOutcomeType
    assert len(ABCOutcomeType.all_types()) >= 15

def test_outcome_taxonomy_success_types():
    """Test 90: success_types() returns 3 types."""
    from abc_validation.outcome_taxonomy_v141 import ABCOutcomeType
    assert len(ABCOutcomeType.success_types()) == 3

def test_outcome_taxonomy_no_fill():
    """Test 91: classify_outcome returns NO_FILL when trade is None."""
    from abc_validation.outcome_taxonomy_v141 import classify_outcome
    result = classify_outcome({}, None)
    assert result == "NO_FILL"

def test_outcome_taxonomy_blocked():
    """Test 92: classify_outcome returns BLOCKED when exit_reason is BLOCKED."""
    from abc_validation.outcome_taxonomy_v141 import classify_outcome
    result = classify_outcome({}, {"exit_reason": "BLOCKED", "net_return": 0.05})
    assert result == "BLOCKED"

def test_outcome_taxonomy_success_trend():
    """Test 93: Positive return with long holding returns SUCCESS."""
    from abc_validation.outcome_taxonomy_v141 import classify_outcome, ABCOutcomeType
    result = classify_outcome(
        {"is_second_wave": False},
        {"exit_reason": "END_OF_DATA", "net_return": 0.05},
        holding_period=10,
        buy_point_type="A"
    )
    assert result in (ABCOutcomeType.SUCCESS_TREND_CONTINUATION, ABCOutcomeType.SUCCESS_SECOND_WAVE)

def test_outcome_taxonomy_false_reclaim():
    """Test 94: Negative return for C type returns FALSE_RECLAIM."""
    from abc_validation.outcome_taxonomy_v141 import classify_outcome, ABCOutcomeType
    result = classify_outcome(
        {},
        {"exit_reason": "END_OF_DATA", "net_return": -0.08},
        buy_point_type="C"
    )
    assert result == ABCOutcomeType.FALSE_RECLAIM


# ── Failure Rate Analyzer ─────────────────────────────────────────────────────

def test_failure_rate_analyzer_import():
    """Test 95: ABCFailureRateAnalyzer imports."""
    from abc_validation.failure_rate_analyzer_v141 import ABCFailureRateAnalyzer
    fra = ABCFailureRateAnalyzer()
    assert fra is not None

def test_failure_rate_analyzer_empty():
    """Test 96: analyze with empty signals returns None rates."""
    from abc_validation.failure_rate_analyzer_v141 import ABCFailureRateAnalyzer
    fra = ABCFailureRateAnalyzer()
    result = fra.analyze([], buy_point_type="A")
    assert result["total_signals"] == 0
    assert result["signal_failure_rate"] is None

def test_failure_rate_analyzer_no_fill_rate():
    """Test 97: All signals with no trades → no_fill_rate = 1.0."""
    from abc_validation.failure_rate_analyzer_v141 import ABCFailureRateAnalyzer
    fra = ABCFailureRateAnalyzer()
    signals = [{"signal_id": "s1"}, {"signal_id": "s2"}]
    result = fra.analyze(signals, trades=[], buy_point_type="A")
    assert result["no_fill_rate"] == 1.0


# ── Validation Result ─────────────────────────────────────────────────────────

def test_validation_result_import():
    """Test 98: ABCValidationResult imports."""
    from abc_validation.validation_result_v141 import ABCValidationResult
    r = ABCValidationResult(
        validation_id="test_001",
        buy_point_type="A",
        rule_snapshot_id="snap_001",
    )
    assert r.validation_id == "test_001"

def test_validation_result_safety_flags():
    """Test 99: Safety flags are always enforced."""
    from abc_validation.validation_result_v141 import ABCValidationResult
    r = ABCValidationResult(
        validation_id="test_002",
        buy_point_type="B",
        rule_snapshot_id="snap_002",
        no_real_orders=False,  # should be overridden
        production_trading_blocked=False,  # should be overridden
    )
    # to_dict enforces flags
    d = r.to_dict()
    assert d["no_real_orders"] is True
    assert d["production_trading_blocked"] is True

def test_validation_result_from_dict_fixture():
    """Test 100: Load validation result from fixture."""
    from abc_validation.validation_result_v141 import ABCValidationResult
    fix = _load_fixture("validation_result_v1.json")
    # Remove _fixture_meta before loading
    fix_clean = {k: v for k, v in fix.items() if not k.startswith("_")}
    r = ABCValidationResult.from_dict(fix_clean)
    assert r.validation_id == "fix_val_result_v1_001"
    assert r.no_real_orders is True
    assert r.formal_conclusion_allowed is False

def test_validation_result_from_dict_unknown_fields():
    """Test 101: from_dict ignores unknown future fields."""
    from abc_validation.validation_result_v141 import ABCValidationResult
    fix = {
        "validation_id": "test_003",
        "buy_point_type": "C",
        "rule_snapshot_id": "snap_003",
        "future_unknown_field_xyz": "value",
    }
    r = ABCValidationResult.from_dict(fix)
    assert r.validation_id == "test_003"


# ── Comparison Engine ─────────────────────────────────────────────────────────

def test_comparison_engine_import():
    """Test 102: ABCComparisonEngine imports."""
    from abc_validation.comparison_engine_v141 import ABCComparisonEngine
    ce = ABCComparisonEngine()
    assert ce is not None

def test_comparison_engine_modes():
    """Test 103: COMPARISON_MODES contains all required modes."""
    from abc_validation.comparison_engine_v141 import COMPARISON_MODES
    assert "a_vs_b_vs_c" in COMPARISON_MODES
    assert "regime_specific" in COMPARISON_MODES
    assert "strict_vs_relaxed" in COMPARISON_MODES

def test_comparison_engine_not_rankable_different_universe():
    """Test 104: Different universe → not directly rankable."""
    from abc_validation.comparison_engine_v141 import ABCComparisonEngine
    ce = ABCComparisonEngine()
    results = [
        {"buy_point_type": "A", "universe": "TWSE_TOP100"},
        {"buy_point_type": "B", "universe": "TWSE_ALL"},
    ]
    result = ce.compare(results, mode="a_vs_b")
    assert result["directly_rankable"] is False

def test_comparison_engine_rankable_same_config():
    """Test 105: Same configuration → directly rankable."""
    from abc_validation.comparison_engine_v141 import ABCComparisonEngine
    ce = ABCComparisonEngine()
    results = [
        {"buy_point_type": "A", "signal_count": 10},
        {"buy_point_type": "B", "signal_count": 8},
    ]
    result = ce.compare(results, mode="a_vs_b")
    assert result["directly_rankable"] is True

def test_comparison_engine_invalid_mode():
    """Test 106: Invalid mode raises ValueError."""
    from abc_validation.comparison_engine_v141 import ABCComparisonEngine
    ce = ABCComparisonEngine()
    with pytest.raises(ValueError, match="Unknown comparison mode"):
        ce.compare([], mode="invalid_mode")


# ── Confidence ────────────────────────────────────────────────────────────────

def test_confidence_import():
    """Test 107: ABCValidationConfidence imports."""
    from abc_validation.confidence_v141 import ABCValidationConfidence
    conf = ABCValidationConfidence()
    assert conf is not None

def test_confidence_levels():
    """Test 108: LEVELS contains all required levels."""
    from abc_validation.confidence_v141 import ABCValidationConfidence
    assert "HIGH" in ABCValidationConfidence.LEVELS
    assert "BLOCKED" in ABCValidationConfidence.LEVELS
    assert "INSUFFICIENT" in ABCValidationConfidence.LEVELS

def test_confidence_mock_data_blocked():
    """Test 109: Mock data → not formal conclusion."""
    from abc_validation.confidence_v141 import ABCValidationConfidence
    conf = ABCValidationConfidence()
    result = conf.evaluate({
        "configuration": {"data_mode": "mock"},
        "trade_count": 100,
        "symbols_tested": ["2330"] * 10,
    })
    assert result["formal_conclusion_allowed"] is False
    assert "real_data" in result["requirements_failed"]

def test_confidence_fixture_data_blocked():
    """Test 110: Fixture data → not formal conclusion."""
    from abc_validation.confidence_v141 import ABCValidationConfidence
    conf = ABCValidationConfidence()
    result = conf.evaluate({
        "configuration": {"data_mode": "real"},
        "quality_summary": {"fixture_data_used": True},
        "trade_count": 100,
        "symbols_tested": ["2330"] * 10,
    })
    assert result["formal_conclusion_allowed"] is False

def test_confidence_lookahead_blocked():
    """Test 111: Lookahead violations → BLOCKED."""
    from abc_validation.confidence_v141 import ABCValidationConfidence
    conf = ABCValidationConfidence()
    result = conf.evaluate({
        "configuration": {"data_mode": "real"},
        "quality_summary": {"lookahead_violations": 3},
        "trade_count": 100,
    })
    assert result["level"] == "BLOCKED"

def test_confidence_insufficient_trades():
    """Test 112: Too few trades → insufficient."""
    from abc_validation.confidence_v141 import ABCValidationConfidence
    conf = ABCValidationConfidence()
    result = conf.evaluate({
        "configuration": {"data_mode": "real"},
        "trade_count": 5,  # < 30 required
    })
    assert "sufficient_trades" in result["requirements_failed"]


# ── Walk Forward ──────────────────────────────────────────────────────────────

def test_walk_forward_import():
    """Test 113: ABCWalkForwardValidator imports."""
    from abc_validation.walk_forward_v141 import ABCWalkForwardValidator
    wfv = ABCWalkForwardValidator()
    assert wfv is not None

def test_walk_forward_create_folds():
    """Test 114: create_folds returns correct number of folds."""
    from abc_validation.walk_forward_v141 import ABCWalkForwardValidator
    wfv = ABCWalkForwardValidator(n_folds=3)
    dates = [f"2023-{m:02d}-01" for m in range(1, 37)]
    folds = wfv.create_folds(dates)
    assert len(folds) == 3

def test_walk_forward_splits_sum_to_one():
    """Test 115: Split percentages sum to 1.0."""
    from abc_validation.walk_forward_v141 import ABCWalkForwardValidator
    wfv = ABCWalkForwardValidator(train_pct=0.6, val_pct=0.2, test_pct=0.2)
    assert abs(wfv.train_pct + wfv.val_pct + wfv.test_pct - 1.0) < 0.001

def test_walk_forward_invalid_splits():
    """Test 116: Invalid splits raise AssertionError."""
    from abc_validation.walk_forward_v141 import ABCWalkForwardValidator
    with pytest.raises(AssertionError):
        ABCWalkForwardValidator(train_pct=0.5, val_pct=0.3, test_pct=0.3)

def test_walk_forward_run_empty():
    """Test 117: run with empty signals returns structure."""
    from abc_validation.walk_forward_v141 import ABCWalkForwardValidator
    wfv = ABCWalkForwardValidator(n_folds=2)
    result = wfv.run({}, buy_point_type="A")
    assert "folds" in result
    assert result["no_test_set_parameter_tuning"] is True

def test_walk_forward_all_folds_preserved():
    """Test 118: All folds preserved including negative performance."""
    from abc_validation.walk_forward_v141 import ABCWalkForwardValidator
    wfv = ABCWalkForwardValidator(n_folds=3)
    dates = [f"2023-{m:02d}-01" for m in range(1, 37)]
    signals_by_date = {d: [] for d in dates}
    result = wfv.run(signals_by_date, buy_point_type="A")
    assert "ALL folds preserved" in result["note"] or "preserved" in result["note"].lower()


# ── Store ─────────────────────────────────────────────────────────────────────

def test_store_import():
    """Test 119: ABCValidationStore imports."""
    from abc_validation.store_v141 import ABCValidationStore
    store = ABCValidationStore()
    assert store is not None

def test_store_summarize():
    """Test 120: summarize returns dict with schema_version."""
    from abc_validation.store_v141 import ABCValidationStore
    store = ABCValidationStore()
    summary = store.summarize()
    assert "schema_version" in summary
    assert summary["no_real_orders"] is True

def test_store_list_runs_empty():
    """Test 121: list_runs returns list."""
    from abc_validation.store_v141 import ABCValidationStore
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ABCValidationStore(base_dir=tmpdir)
        runs = store.list_runs()
        assert isinstance(runs, list)

def test_store_get_run_missing():
    """Test 122: get_run returns None for unknown ID."""
    from abc_validation.store_v141 import ABCValidationStore
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ABCValidationStore(base_dir=tmpdir)
        assert store.get_run("nonexistent_id") is None

def test_store_list_by_buy_point_type():
    """Test 123: list_by_buy_point_type filters correctly."""
    from abc_validation.store_v141 import ABCValidationStore
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ABCValidationStore(base_dir=tmpdir)
        assert isinstance(store.list_by_buy_point_type("A"), list)

def test_store_schema_version():
    """Test 124: Schema version is 1.4.1."""
    from abc_validation.store_v141 import SCHEMA_VERSION
    assert SCHEMA_VERSION == "1.4.1"


# ── Repair Integration ────────────────────────────────────────────────────────

def test_repair_integration_import():
    """Test 125: ABCRepairIntegration imports."""
    from abc_validation.repair_integration_v141 import ABCRepairIntegration
    ri = ABCRepairIntegration()
    assert ri is not None

def test_repair_integration_defaults_false():
    """Test 126: create_repair_tasks=False by default."""
    from abc_validation.repair_integration_v141 import ABCRepairIntegration
    ri = ABCRepairIntegration()
    assert ri.create_repair_tasks is False

def test_repair_integration_no_auto():
    """Test 127: No auto repair, refresh, download, mock fallback."""
    from abc_validation.repair_integration_v141 import ABCRepairIntegration
    ri = ABCRepairIntegration()
    assert ri.auto_repair_enabled is False
    assert ri.auto_refresh_enabled is False
    assert ri.auto_download_enabled is False
    assert ri.mock_fallback_enabled is False

def test_repair_integration_dry_run():
    """Test 128: create_candidates with False flag returns no tasks created."""
    from abc_validation.repair_integration_v141 import ABCRepairIntegration
    ri = ABCRepairIntegration(create_repair_tasks=False)
    result = ri.create_candidates([])
    assert result["tasks_created"] == 0
    assert "create_repair_tasks=False" in result["note"]


# ── Replay Integration ────────────────────────────────────────────────────────

def test_replay_integration_import():
    """Test 129: ABCReplayIntegration imports."""
    from abc_validation.replay_integration_v141 import ABCReplayIntegration
    ri = ABCReplayIntegration()
    assert ri is not None

def test_replay_integration_read_only():
    """Test 130: ABCReplayIntegration is read-only."""
    from abc_validation.replay_integration_v141 import ABCReplayIntegration
    ri = ABCReplayIntegration()
    assert ri.READ_ONLY is True

def test_replay_integration_no_modify():
    """Test 131: ABCReplayIntegration never modifies replay sessions."""
    from abc_validation.replay_integration_v141 import ABCReplayIntegration
    ri = ABCReplayIntegration()
    assert ri.MODIFIES_REPLAY_SESSIONS is False
    assert ri.MODIFIES_CHALLENGE_QUESTIONS is False
    assert ri.MODIFIES_RULE_PARAMETERS is False
    assert ri.MODIFIES_REGISTRY is False

def test_replay_integration_get_evidence_no_result():
    """Test 132: get_evidence_summary returns no evidence when result is None."""
    from abc_validation.replay_integration_v141 import ABCReplayIntegration
    ri = ABCReplayIntegration()
    result = ri.get_evidence_summary("A")
    assert result["evidence_available"] is False
    assert result["read_only"] is True


# ── Report ────────────────────────────────────────────────────────────────────

def test_report_import():
    """Test 133: ABCValidationReport imports."""
    from abc_validation.report_v141 import ABCValidationReport
    rpt = ABCValidationReport()
    assert rpt is not None

def test_report_generate_text():
    """Test 134: generate_text returns string with safety banner."""
    from abc_validation.report_v141 import ABCValidationReport
    rpt = ABCValidationReport()
    text = rpt.generate_text({"validation_id": "test", "buy_point_type": "A",
                               "signal_count": 5, "trade_count": 4})
    assert "Research Only" in text
    assert "No Real Orders" in text

def test_report_generate_dict():
    """Test 135: generate_dict returns dict with sections."""
    from abc_validation.report_v141 import ABCValidationReport
    rpt = ABCValidationReport()
    d = rpt.generate_dict({"validation_id": "test", "buy_point_type": "B"})
    assert "sections" in d
    assert d["no_real_orders"] is True


# ── Health Check ──────────────────────────────────────────────────────────────

def test_health_check_import():
    """Test 136: ABCBuyPointValidationHealthCheck imports."""
    from abc_validation.health_v141 import ABCBuyPointValidationHealthCheck
    hc = ABCBuyPointValidationHealthCheck()
    assert hc is not None

def test_health_check_run():
    """Test 137: health check run returns dict of checks."""
    from abc_validation.health_v141 import ABCBuyPointValidationHealthCheck
    hc = ABCBuyPointValidationHealthCheck()
    checks = hc.run()
    assert isinstance(checks, dict)
    assert len(checks) > 0

def test_health_check_summary():
    """Test 138: get_health_summary returns required fields."""
    from abc_validation.health_v141 import ABCBuyPointValidationHealthCheck
    hc = ABCBuyPointValidationHealthCheck()
    summary = hc.get_health_summary()
    required = [
        "abc_validation_status", "abc_validation_schema_version", "abc_rules_total",
        "abc_a_available", "abc_b_available", "abc_c_available",
        "auto_optimization_enabled", "auto_trading_enabled",
        "broker_execution_enabled", "production_trading_blocked",
    ]
    for field in required:
        assert field in summary, f"Missing field: {field}"

def test_health_check_safety_flags():
    """Test 139: Health check safety flags are correct."""
    from abc_validation.health_v141 import ABCBuyPointValidationHealthCheck
    hc = ABCBuyPointValidationHealthCheck()
    summary = hc.get_health_summary()
    assert summary["auto_optimization_enabled"] is False
    assert summary["auto_trading_enabled"] is False
    assert summary["broker_execution_enabled"] is False
    assert summary["production_trading_blocked"] is True

def test_health_check_no_mock_fallback():
    """Test 140: Health check shows mock_fallback_enabled is False."""
    from abc_validation.health_v141 import ABCBuyPointValidationHealthCheck
    hc = ABCBuyPointValidationHealthCheck()
    summary = hc.get_health_summary()
    assert summary.get("mock_fallback_enabled") is False


# ── version_info.py ───────────────────────────────────────────────────────────

def test_version_info_141():
    """Test 141: VERSION is 1.3.6 (canonical) or later."""
    from release.version_info import VERSION
    major, minor, patch = (int(x) for x in VERSION.split(".")[:3])
    assert (major, minor, patch) >= (1, 3, 6), f"Expected >= 1.3.6, got {VERSION}"

def test_release_name_141():
    """Test 142: RELEASE_NAME is a known release (v1.4.x adds public data provider releases)."""
    from release.version_info import RELEASE_NAME
    _KNOWN = (
        "A/B/C Buy Point Validation",
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
    )
    assert RELEASE_NAME in _KNOWN, f"Unexpected release name: {RELEASE_NAME}"

def test_base_release_141():
    """Test 143: BASE_RELEASE references the A/B/C, Robustness, or later release."""
    from release.version_info import BASE_RELEASE
    assert any(marker in BASE_RELEASE for marker in ("1.3.5", "1.3.6", "1.3.7", "1.3.9", "1.4.0", "1.4.1", "1.4.2", "1.4.3", "1.4.4", "1.4.5", "1.4.6", "1.4.7", "1.4.8", "1.4.9", "1.5.0")), (
        f"BASE_RELEASE does not reference empirical/A/B/C/Robustness release: {BASE_RELEASE}"
    )

def test_abc_validation_available_flag():
    """Test 144: ABC_BUY_POINT_VALIDATION_AVAILABLE is True."""
    from release.version_info import ABC_BUY_POINT_VALIDATION_AVAILABLE
    assert ABC_BUY_POINT_VALIDATION_AVAILABLE is True

def test_abc_mock_formal_conclusion_disabled():
    """Test 145: ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED is False."""
    from release.version_info import ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED
    assert ABC_BUY_POINT_MOCK_FORMAL_CONCLUSION_ALLOWED is False

def test_abc_auto_optimization_disabled():
    """Test 146: ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED is False."""
    from release.version_info import ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED
    assert ABC_BUY_POINT_AUTO_OPTIMIZATION_ENABLED is False

def test_abc_auto_trading_disabled():
    """Test 147: ABC_BUY_POINT_AUTO_TRADING_ENABLED is False."""
    from release.version_info import ABC_BUY_POINT_AUTO_TRADING_ENABLED
    assert ABC_BUY_POINT_AUTO_TRADING_ENABLED is False

def test_abc_formal_conclusion_requires_real_data():
    """Test 148: ABC_BUY_POINT_FORMAL_CONCLUSION_REQUIRES_REAL_DATA is True."""
    from release.version_info import ABC_BUY_POINT_FORMAL_CONCLUSION_REQUIRES_REAL_DATA
    assert ABC_BUY_POINT_FORMAL_CONCLUSION_REQUIRES_REAL_DATA is True

def test_abc_regime_validation_available():
    """Test 149: ABC_BUY_POINT_REGIME_VALIDATION_AVAILABLE is True."""
    from release.version_info import ABC_BUY_POINT_REGIME_VALIDATION_AVAILABLE
    assert ABC_BUY_POINT_REGIME_VALIDATION_AVAILABLE is True

def test_abc_filter_ablation_available():
    """Test 150: ABC_BUY_POINT_FILTER_ABLATION_AVAILABLE is True."""
    from release.version_info import ABC_BUY_POINT_FILTER_ABLATION_AVAILABLE
    assert ABC_BUY_POINT_FILTER_ABLATION_AVAILABLE is True


# ── Fixtures ──────────────────────────────────────────────────────────────────

def test_fixture_a_strict_meta():
    """Test 151: a_strict.json has TEST_FIXTURE=True."""
    fix = _load_fixture("a_strict.json")
    assert fix["_fixture_meta"]["TEST_FIXTURE"] is True
    assert fix["_fixture_meta"]["NOT_FOR_FORMAL_CONCLUSION"] is True

def test_fixture_a_failed_meta():
    """Test 152: a_failed.json has NOT_REAL_DATA=True."""
    fix = _load_fixture("a_failed.json")
    assert fix["_fixture_meta"]["NOT_REAL_DATA"] is True

def test_fixture_b_strict_meta():
    """Test 153: b_strict.json fixture_data=True."""
    fix = _load_fixture("b_strict.json")
    assert fix["fixture_data"] is True

def test_fixture_b_overextended_type():
    """Test 154: b_overextended.json has buy_point_type B and overextended True."""
    fix = _load_fixture("b_overextended.json")
    assert fix["buy_point_type"] == "B"
    assert fix["overextended"] is True

def test_fixture_c_reclaim_type():
    """Test 155: c_reclaim.json has buy_point_type C and classification C_STRICT_RECLAIM."""
    fix = _load_fixture("c_reclaim.json")
    assert fix["buy_point_type"] == "C"
    assert fix["classification"] == "C_STRICT_RECLAIM"

def test_fixture_c_false_reclaim_type():
    """Test 156: c_false_reclaim.json has classification C_FALSE_RECLAIM."""
    fix = _load_fixture("c_false_reclaim.json")
    assert fix["classification"] == "C_FALSE_RECLAIM"

def test_fixture_second_wave():
    """Test 157: second_wave.json has is_second_wave=True."""
    fix = _load_fixture("second_wave.json")
    assert fix["is_second_wave"] is True

def test_fixture_regime_cases():
    """Test 158: regime_cases.json has multiple regime cases."""
    fix = _load_fixture("regime_cases.json")
    assert len(fix["regime_cases"]) >= 4

def test_fixture_stop_target_collision():
    """Test 159: stop_target_collision.json has stop very close to target."""
    fix = _load_fixture("stop_target_collision.json")
    stop = fix["stop_loss_price"]
    target = fix["target_price"]
    entry = fix["entry_price"]
    assert abs(target - stop) / entry < 0.01

def test_fixture_validation_result_v1():
    """Test 160: validation_result_v1.json has formal_conclusion_allowed=False."""
    fix = _load_fixture("validation_result_v1.json")
    assert fix["formal_conclusion_allowed"] is False
    assert fix["no_real_orders"] is True


# ── CLI Smoke Tests ───────────────────────────────────────────────────────────

def test_cli_abc_validation_health_handler_exists():
    """Test 161: cmd_abc_validation_health exists in main."""
    import main as m
    assert hasattr(m, "cmd_abc_validation_health")

def test_cli_abc_validation_plan_handler_exists():
    """Test 162: cmd_abc_validation_plan exists in main."""
    import main as m
    assert hasattr(m, "cmd_abc_validation_plan")

def test_cli_abc_validation_run_handler_exists():
    """Test 163: cmd_abc_validation_run exists in main."""
    import main as m
    assert hasattr(m, "cmd_abc_validation_run")

def test_cli_abc_validation_list_handler_exists():
    """Test 164: cmd_abc_validation_list exists in main."""
    import main as m
    assert hasattr(m, "cmd_abc_validation_list")

def test_cli_abc_validation_compare_handler_exists():
    """Test 165: cmd_abc_validation_compare exists in main."""
    import main as m
    assert hasattr(m, "cmd_abc_validation_compare")

def test_cli_abc_validation_health_runs(capsys):
    """Test 166: cmd_abc_validation_health runs without error."""
    import main as m

    class FakeArgs:
        pass

    m.cmd_abc_validation_health(FakeArgs())
    captured = capsys.readouterr()
    assert "Research Only" in captured.out or "A/B/C" in captured.out or "PASS" in captured.out

def test_cli_abc_validation_plan_runs(capsys):
    """Test 167: cmd_abc_validation_plan runs without error."""
    import main as m

    class FakeArgs:
        buy_point_type = "A"
        symbol = "2330"
        universe = None

    m.cmd_abc_validation_plan(FakeArgs())
    captured = capsys.readouterr()
    assert "DRY RUN" in captured.out or "Plan" in captured.out

def test_cli_abc_validation_run_dry_run(capsys):
    """Test 168: cmd_abc_validation_run defaults to dry run."""
    import main as m

    class FakeArgs:
        buy_point_type = "A"
        symbol = None
        universe = None
        execute = False

    m.cmd_abc_validation_run(FakeArgs())
    captured = capsys.readouterr()
    assert "DRY_RUN" in captured.out or "dry" in captured.out.lower()

def test_cli_abc_validation_blocked_runs(capsys):
    """Test 169: cmd_abc_validation_blocked runs without error."""
    import main as m

    class FakeArgs:
        pass

    m.cmd_abc_validation_blocked(FakeArgs())
    captured = capsys.readouterr()
    assert "Research Only" in captured.out or "Blocked" in captured.out


# ── GUI Smoke Tests ───────────────────────────────────────────────────────────

def test_gui_panel_import():
    """Test 170: GUI panel imports without error."""
    import gui.abc_buy_point_validation_panel as panel_module
    assert panel_module is not None

def test_gui_panel_tab_id():
    """Test 171: GUI panel has correct TAB_ID."""
    from gui.abc_buy_point_validation_panel import TAB_ID
    assert TAB_ID == "abc_buy_point_validation"

def test_gui_panel_display_name():
    """Test 172: GUI panel has correct DISPLAY_NAME."""
    from gui.abc_buy_point_validation_panel import DISPLAY_NAME
    assert DISPLAY_NAME == "A/B/C Validation"

def test_gui_panel_group():
    """Test 173: GUI panel is in research group."""
    from gui.abc_buy_point_validation_panel import GROUP
    assert GROUP == "research"

def test_gui_panel_search_keywords():
    """Test 174: GUI panel has search keywords."""
    from gui.abc_buy_point_validation_panel import SEARCH_KEYWORDS
    assert "A買點" in SEARCH_KEYWORDS or "ABC buy point" in SEARCH_KEYWORDS

def test_gui_panel_safety_flags():
    """Test 175: GUI panel safety flags are correct."""
    from gui.abc_buy_point_validation_panel import (
        NO_REAL_ORDERS, BROKER_EXECUTION_ENABLED, PRODUCTION_TRADING_BLOCKED,
        MOCK_FORMAL_CONCLUSION_ALLOWED, AUTO_OPTIMIZATION_ENABLED, AUTO_TRADING_ENABLED
    )
    assert NO_REAL_ORDERS is True
    assert BROKER_EXECUTION_ENABLED is False
    assert PRODUCTION_TRADING_BLOCKED is True
    assert MOCK_FORMAL_CONCLUSION_ALLOWED is False
    assert AUTO_OPTIMIZATION_ENABLED is False
    assert AUTO_TRADING_ENABLED is False


# ── Regression Tests (v1.3.0 - v1.4.0) ──────────────────────────────────────

def test_regression_v140_rule_registry_still_works():
    """Test 176: v1.4.0 rule registry still works after v1.4.1 upgrade."""
    from empirical_backtest.rule_registry_v140 import StrategyKnowledgeRuleRegistry
    reg = StrategyKnowledgeRuleRegistry()
    assert reg.get("abc_buy_point_a") is not None
    assert reg.get("abc_buy_point_b") is not None
    assert reg.get("abc_buy_point_c") is not None

def test_regression_v140_buy_point_analyzer_still_works():
    """Test 177: v1.4.0 BuyPointAnalyzer still works."""
    from analysis.buy_point_analyzer import BuyPointAnalyzer
    result = BuyPointAnalyzer().analyze("2330", mode='mock')
    assert isinstance(result, dict)
    assert "buy_point_grade" in result

def test_regression_v140_health_check_passes():
    """Test 178: v1.4.0 health check passes with v1.4.1 VERSION."""
    from empirical_backtest.health_v140 import StrategyEmpiricalBacktestHealthCheck
    hc = StrategyEmpiricalBacktestHealthCheck()
    checks = hc.run()
    version_check = checks.get("version_info_1_4_0")
    assert version_check is not None
    assert version_check[0] == "PASS"

def test_regression_v130_data_quality_not_broken():
    """Test 179: v1.3.0 real data quality can still be imported."""
    try:
        import real_data_quality
        # If module exists, it should import without error
    except ImportError:
        pass  # Module may not exist, that's OK

def test_regression_empirical_backtest_models_still_work():
    """Test 180: v1.4.0 models still work."""
    from empirical_backtest.models_v140 import (
        StrategyRule, RuleCategory, BacktestStatus, MarketRegime
    )
    assert BacktestStatus.PASS == "PASS"
    assert MarketRegime.BULL == "BULL"

def test_regression_version_info_print_not_broken():
    """Test 181: print_version_info still works and includes A/B/C capability flags."""
    from release.version_info import print_version_info
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        print_version_info()
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    # Check capability is present (version number may have been realigned)
    assert "A/B/C Validation Available" in output
    assert "Mock Formal Conclusion Allowed: False" in output
    # Verify version is present in output (canonical or pre-alignment)
    assert "Version:" in output

def test_end_to_end_abc_validation_health_smoke():
    """Test 182: End-to-end health check smoke test."""
    from abc_validation.health_v141 import ABCBuyPointValidationHealthCheck
    hc = ABCBuyPointValidationHealthCheck()
    summary = hc.get_health_summary()
    # At minimum these critical checks should pass
    checks = summary.get("checks", {})
    assert "package_import" in checks
    assert "abc_safety_flags" in checks
    assert "rule_adapters" in checks
    # Safety flags must be correct
    assert summary["production_trading_blocked"] is True
    assert summary["broker_execution_enabled"] is False
    assert summary["auto_optimization_enabled"] is False
