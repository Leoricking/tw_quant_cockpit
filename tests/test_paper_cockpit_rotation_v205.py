"""
tests/test_paper_cockpit_rotation_v205.py
v2.0.5 Watchlist Rotation Engine Deep Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


def _make_item(symbol, score=60.0, trend=60.0, volume=60.0, chip=60.0, risk=60.0,
               no_entry=None, promo=None, demotion=None, review=None):
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistItem
    return WatchlistItem(
        symbol=symbol, score=score,
        trend_quality=trend, volume_quality=volume, chip_quality=chip, risk_quality=risk,
        no_entry_reasons=no_entry or [],
        promotion_reasons=promo or [],
        demotion_reasons=demotion or [],
        human_review_reasons=review or [],
    )


# -------------------------------------------------------------------------
# Keep logic
# -------------------------------------------------------------------------
def test_keep_logic_middle_score_no_issues():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("KEEP1", score=60.0, trend=60.0, volume=60.0, chip=60.0, risk=60.0)
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    all_symbols = (
        [d.symbol for d in result.promotion_queue]
        + [d.symbol for d in result.demotion_queue]
        + [d.symbol for d in result.remove_queue]
        + [i.symbol for i in result.keep_queue]
        + [i.symbol for i in result.human_review_queue]
        + [i.symbol for i in result.quarantine_queue]
    )
    assert "KEEP1" in all_symbols

def test_keep_returns_paper_only_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[_make_item("K2")])
    result = run_watchlist_rotation(inp)
    assert result.paper_only is True

# -------------------------------------------------------------------------
# Promote logic
# -------------------------------------------------------------------------
def test_promote_logic_high_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("PROMO1", score=90.0, trend=90.0, volume=88.0, chip=85.0, risk=80.0,
                      promo=["strong_trend", "volume_confirmation", "chip_buy"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    promo_syms = [d.symbol for d in result.promotion_queue]
    assert "PROMO1" in promo_syms

def test_promote_decision_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("PROMO2", score=90.0, trend=90.0, volume=88.0, chip=85.0, risk=80.0,
                      promo=["strong_trend", "volume_ok", "chip_ok"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    for dec in result.promotion_queue:
        assert dec.should_auto_apply is False

def test_promote_decision_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("PROMO3", score=90.0, trend=92.0, volume=88.0, chip=85.0, risk=80.0,
                      promo=["strong_trend", "volume_ok", "chip_ok"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    for dec in result.promotion_queue:
        assert dec.paper_only is True

def test_promote_to_status_is_promoted_candidate():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("PROMO4", score=90.0, trend=91.0, volume=88.0, chip=85.0, risk=80.0,
                      promo=["strong_trend", "volume_ok", "chip_ok"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    if result.promotion_queue:
        assert result.promotion_queue[0].to_status == "promoted_candidate"

# -------------------------------------------------------------------------
# Demote logic
# -------------------------------------------------------------------------
def test_demote_logic_low_score_with_demotion_reasons():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("DEMOTE1", score=20.0, trend=20.0, volume=18.0, chip=22.0, risk=20.0,
                      demotion=["weak_volume", "trend_broken"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    all_neg = [d.symbol for d in result.demotion_queue] + [d.symbol for d in result.remove_queue]
    assert "DEMOTE1" in all_neg

def test_demote_decision_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("DEMOTE2", score=20.0, trend=20.0, volume=18.0, chip=22.0, risk=20.0,
                      demotion=["weak_volume"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    for dec in result.demotion_queue:
        assert dec.should_auto_apply is False

# -------------------------------------------------------------------------
# Remove logic
# -------------------------------------------------------------------------
def test_remove_logic_very_low_score():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("REMOVE1", score=5.0, trend=5.0, volume=5.0, chip=5.0, risk=5.0)
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    all_neg = [d.symbol for d in result.remove_queue] + [d.symbol for d in result.demotion_queue]
    assert "REMOVE1" in all_neg

# -------------------------------------------------------------------------
# Quarantine logic
# -------------------------------------------------------------------------
def test_quarantine_logic_three_no_entry_reasons():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("QUARANTINE1", no_entry=["trend_broken", "below_20ma", "volume_dry_up_failed"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    quarantine_syms = [i.symbol for i in result.quarantine_queue]
    assert "QUARANTINE1" in quarantine_syms

def test_quarantine_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("QUARANTINE2", no_entry=["trend_broken", "below_20ma", "risk_budget_exceeded"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    assert result.paper_only is True

# -------------------------------------------------------------------------
# Human review logic
# -------------------------------------------------------------------------
def test_human_review_logic():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("HREVIEW1", review=["low_liquidity"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    review_syms = [i.symbol for i in result.human_review_queue]
    assert "HREVIEW1" in review_syms

def test_human_review_no_auto_apply():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("HREVIEW2", review=["unusual_volume"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    assert result.should_auto_apply is False

# -------------------------------------------------------------------------
# Risk budget aware promotion
# -------------------------------------------------------------------------
def test_risk_budget_aware_promotion():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("RISK1", score=80.0, trend=82.0, volume=78.0, chip=80.0, risk=75.0,
                      promo=["strong_trend", "volume_ok"])
    inp_low = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item], risk_budget_pct=5.0)
    inp_high = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item], risk_budget_pct=30.0)
    result_low = run_watchlist_rotation(inp_low)
    result_high = run_watchlist_rotation(inp_high)
    # Both are paper-only, regardless of budget
    assert result_low.paper_only is True
    assert result_high.paper_only is True

def test_risk_score_in_promotion_decision():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    item = _make_item("RISK2", score=90.0, trend=90.0, volume=88.0, chip=85.0, risk=80.0,
                      promo=["strong_trend", "volume_ok", "chip_ok"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    result = run_watchlist_rotation(inp)
    for dec in result.promotion_queue:
        assert isinstance(dec.risk_score, float)

# -------------------------------------------------------------------------
# Simulation ranking aware
# -------------------------------------------------------------------------
def test_simulation_ranking_snapshot_stored():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    inp = WatchlistRotationInput(
        rotation_period="2026-W29",
        simulation_ranking_ids=["SIM001", "SIM002"],
    )
    result = run_watchlist_rotation(inp)
    assert result.simulation_ranking_snapshot == ["SIM001", "SIM002"]

def test_review_pack_snapshot_stored():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, WatchlistRotationInput
    inp = WatchlistRotationInput(
        rotation_period="2026-W29",
        review_pack_ids=["R001"],
    )
    result = run_watchlist_rotation(inp)
    assert result.review_pack_snapshot == ["R001"]

# -------------------------------------------------------------------------
# Strategy profile aware
# -------------------------------------------------------------------------
def test_strategy_profile_stored_in_input():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import WatchlistRotationInput
    inp = WatchlistRotationInput(rotation_period="2026-W29", strategy_profile_id="P001")
    assert inp.strategy_profile_id == "P001"
