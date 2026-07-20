"""
tests/test_paper_cockpit_strategy_profile_v203.py
v2.0.3 Strategy Profile Schema Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# StrategyProfile model
# ---------------------------------------------------------------------------

def test_strategy_profile_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert obj is not None

def test_strategy_profile_has_profile_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "profile_id")

def test_strategy_profile_has_profile_name():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "profile_name")

def test_strategy_profile_has_entry_style():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "entry_style")

def test_strategy_profile_has_risk_budget_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "risk_budget_pct")

def test_strategy_profile_has_max_position_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "max_position_count")

def test_strategy_profile_has_max_single_position_pct():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "max_single_position_pct")

def test_strategy_profile_has_stop_loss_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "stop_loss_policy")

def test_strategy_profile_has_add_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "add_policy")

def test_strategy_profile_has_reduce_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "reduce_policy")

def test_strategy_profile_has_exit_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "exit_policy")

def test_strategy_profile_has_no_entry_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "no_entry_policy")

def test_strategy_profile_has_human_review_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert hasattr(obj, "human_review_policy")

def test_strategy_profile_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert obj.paper_only is True

def test_strategy_profile_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile()
    assert obj.no_real_orders is True

def test_strategy_profile_custom_entry_style():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile(entry_style="conservative")
    assert obj.entry_style == "conservative"

def test_strategy_profile_aggressive_style():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile(entry_style="aggressive")
    assert obj.entry_style == "aggressive"

def test_strategy_profile_abc_pullback_style():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile(entry_style="abc_pullback")
    assert obj.entry_style == "abc_pullback"

def test_strategy_profile_risk_first_style():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile(entry_style="risk_first")
    assert obj.entry_style == "risk_first"

def test_strategy_profile_breakout_only_style():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile(entry_style="breakout_only")
    assert obj.entry_style == "breakout_only"

# ---------------------------------------------------------------------------
# STRATEGY_PROFILE_FIELDS constant
# ---------------------------------------------------------------------------

def test_strategy_profile_fields_is_list():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    assert isinstance(STRATEGY_PROFILE_FIELDS, list)

def test_strategy_profile_fields_profile_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    assert "profile_id" in STRATEGY_PROFILE_FIELDS

def test_strategy_profile_fields_entry_style():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    assert "entry_style" in STRATEGY_PROFILE_FIELDS

def test_strategy_profile_fields_stop_loss_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    assert "stop_loss_policy" in STRATEGY_PROFILE_FIELDS

def test_strategy_profile_fields_human_review_policy():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    assert "human_review_policy" in STRATEGY_PROFILE_FIELDS

def test_strategy_profile_fields_unique():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import STRATEGY_PROFILE_FIELDS
    assert len(STRATEGY_PROFILE_FIELDS) == len(set(STRATEGY_PROFILE_FIELDS))

# ---------------------------------------------------------------------------
# entry styles coverage
# ---------------------------------------------------------------------------

def test_all_entry_styles_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import ENTRY_STYLES, StrategyProfile
    for style in ENTRY_STYLES:
        obj = StrategyProfile(entry_style=style)
        assert obj.entry_style == style
        assert obj.paper_only is True

def test_conservative_profile():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile(entry_style="conservative", risk_budget_pct=0.02)
    assert obj.entry_style == "conservative"

def test_balanced_profile():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile(entry_style="balanced", max_position_count=4)
    assert obj.entry_style == "balanced"

def test_second_wave_profile():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import StrategyProfile
    obj = StrategyProfile(entry_style="second_wave")
    assert obj.paper_only is True

# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

def test_fixtures_v203_import():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    assert FIXTURES is not None

def test_fixtures_v203_count():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    assert len(FIXTURES) == 80

def test_fixtures_v203_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    for f in FIXTURES:
        assert f["schema_version"] == "203"

def test_fixtures_v203_have_fixture_id():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    for f in FIXTURES:
        assert "fixture_id" in f

def test_fixtures_v203_unique_ids():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    ids = {f["id"] for f in FIXTURES}
    assert len(ids) == 80

def test_fixtures_v203_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    for f in FIXTURES:
        assert f.get("paper_only") is True

def test_fixtures_v203_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    for f in FIXTURES:
        assert f.get("no_real_orders") is True

def test_fixtures_v203_ids_start_with_pc203_f():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    for f in FIXTURES:
        assert f["id"].startswith("PC203-F")

def test_fixtures_v203_have_name():
    from paper_trading.small_capital_strategy.paper_cockpit_fixtures_v203 import FIXTURES
    for f in FIXTURES:
        assert "name" in f
