"""
tests/test_paper_cockpit_export_v205.py
v2.0.5 Export Schema Completeness & Edge Case Tests
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest


# -------------------------------------------------------------------------
# JSON export schema completeness
# -------------------------------------------------------------------------
def test_export_json_contains_rotation_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    result = run_watchlist_rotation()
    export = export_rotation_json(result)
    assert result.rotation_id in export.content

def test_export_json_contains_paper_only_true():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert "paper_only" in export.content
    assert "true" in export.content.lower()

def test_export_json_contains_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert "should_auto_apply" in export.content
    assert "false" in export.content.lower()

def test_export_json_contains_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert "no_real_orders" in export.content

def test_export_json_contains_rotation_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert "rotation_version" in export.content

def test_export_json_rotation_id_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert export.rotation_id != ""

def test_export_json_paper_only_confirmed():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert export.paper_only_confirmed is True

def test_export_json_no_real_orders_flag():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_json
    export = export_rotation_json(run_watchlist_rotation())
    assert export.no_real_orders is True

# -------------------------------------------------------------------------
# Markdown export schema completeness
# -------------------------------------------------------------------------
def test_export_md_contains_paper_only_label():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "paper_only" in export.content

def test_export_md_contains_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "should_auto_apply" in export.content
    assert "False" in export.content

def test_export_md_contains_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "no_real_orders" in export.content

def test_export_md_contains_queue_summary_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "Queue Summary" in export.content

def test_export_md_contains_promotion_queue_section():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "Promotion Queue" in export.content

def test_export_md_contains_disclaimer():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert "Not Investment Advice" in export.content

def test_export_md_rotation_id_not_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert export.rotation_id != ""

def test_export_md_paper_only_confirmed():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_markdown
    export = export_rotation_markdown(run_watchlist_rotation())
    assert export.paper_only_confirmed is True

# -------------------------------------------------------------------------
# CSV export schema completeness
# -------------------------------------------------------------------------
def test_export_promo_csv_has_header_row():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    export = export_promotion_queue_csv(run_watchlist_rotation())
    assert "symbol" in export.csv_content
    assert "from_status" in export.csv_content

def test_export_promo_csv_has_to_status_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    export = export_promotion_queue_csv(run_watchlist_rotation())
    assert "to_status" in export.csv_content

def test_export_promo_csv_has_promotion_score_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    export = export_promotion_queue_csv(run_watchlist_rotation())
    assert "promotion_score" in export.csv_content

def test_export_promo_csv_has_should_auto_apply_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_promotion_queue_csv
    export = export_promotion_queue_csv(run_watchlist_rotation())
    assert "should_auto_apply" in export.csv_content

def test_export_promo_csv_auto_apply_always_false_in_rows():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        run_watchlist_rotation, export_promotion_queue_csv,
        WatchlistRotationInput, WatchlistItem
    )
    item = WatchlistItem(symbol="2330", score=90.0, trend_quality=90.0,
                         volume_quality=88.0, chip_quality=85.0, risk_quality=80.0,
                         promotion_reasons=["strong_trend", "volume_ok", "chip_ok"])
    inp = WatchlistRotationInput(rotation_period="2026-W29", watchlist_items=[item])
    export = export_promotion_queue_csv(run_watchlist_rotation(inp))
    if export.row_count > 0:
        assert "False" in export.csv_content

def test_export_demo_csv_has_header_row():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_demotion_queue_csv
    export = export_demotion_queue_csv(run_watchlist_rotation())
    assert "symbol" in export.csv_content

def test_export_demo_csv_has_should_auto_apply_column():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_demotion_queue_csv
    export = export_demotion_queue_csv(run_watchlist_rotation())
    assert "should_auto_apply" in export.csv_content

def test_export_demo_csv_rotation_id_set():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_demotion_queue_csv
    result = run_watchlist_rotation()
    export = export_demotion_queue_csv(result)
    assert export.rotation_id == result.rotation_id

# -------------------------------------------------------------------------
# Audit snapshot schema completeness
# -------------------------------------------------------------------------
def test_audit_snapshot_safety_snapshot_contains_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert "paper_only=True" in snap.safety_snapshot

def test_audit_snapshot_safety_snapshot_contains_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert "no_real_orders=True" in snap.safety_snapshot

def test_audit_snapshot_safety_snapshot_contains_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert "should_auto_apply=False" in snap.safety_snapshot

def test_audit_snapshot_run_metadata_contains_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert "2.0.5" in snap.run_metadata

def test_audit_snapshot_export_format_audit():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert snap.export_format == "audit_snapshot"

def test_audit_snapshot_export_status_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    snap = export_rotation_audit_snapshot(run_watchlist_rotation())
    assert snap.export_status == "complete"

def test_audit_snapshot_input_snapshot_contains_symbols():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import run_watchlist_rotation, export_rotation_audit_snapshot
    result = run_watchlist_rotation()
    snap = export_rotation_audit_snapshot(result)
    assert snap.input_snapshot != ""

# -------------------------------------------------------------------------
# Export with non-default inputs
# -------------------------------------------------------------------------
def test_export_json_with_multiple_items():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        run_watchlist_rotation, export_rotation_json,
        WatchlistRotationInput, WatchlistItem
    )
    items = [
        WatchlistItem(symbol="2330", score=85.0, trend_quality=85.0, volume_quality=80.0,
                      chip_quality=82.0, risk_quality=78.0, promotion_reasons=["strong_trend"]),
        WatchlistItem(symbol="2317", score=40.0, trend_quality=40.0, volume_quality=38.0,
                      chip_quality=42.0, risk_quality=35.0, demotion_reasons=["weak_volume"]),
    ]
    inp = WatchlistRotationInput(rotation_period="2026-W30", watchlist_items=items)
    export = export_rotation_json(run_watchlist_rotation(inp))
    assert export.is_valid is True
    assert export.paper_only is True

def test_export_md_with_multiple_items():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        run_watchlist_rotation, export_rotation_markdown,
        WatchlistRotationInput, WatchlistItem
    )
    items = [
        WatchlistItem(symbol="2454", score=80.0, trend_quality=80.0, volume_quality=78.0,
                      chip_quality=75.0, risk_quality=72.0, promotion_reasons=["ai_theme", "volume_ok"]),
    ]
    inp = WatchlistRotationInput(rotation_period="2026-W30", watchlist_items=items)
    export = export_rotation_markdown(run_watchlist_rotation(inp))
    assert export.is_valid is True
    assert "2026-W30" in export.content

def test_export_audit_with_custom_period():
    from paper_trading.small_capital_strategy.paper_cockpit_v205 import (
        run_watchlist_rotation, export_rotation_audit_snapshot,
        WatchlistRotationInput
    )
    inp = WatchlistRotationInput(rotation_period="2026-W40")
    snap = export_rotation_audit_snapshot(run_watchlist_rotation(inp))
    assert snap.paper_only is True
    assert snap.export_status == "complete"

# -------------------------------------------------------------------------
# v2.0.4 weekly improvement pack integration
# -------------------------------------------------------------------------
def test_v204_build_weekly_improvement_pack_still_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.paper_only is True

def test_v204_improvement_pack_should_auto_apply_false():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import build_weekly_improvement_pack
    pack = build_weekly_improvement_pack()
    assert pack.should_auto_apply is False

def test_v204_run_portfolio_review_still_callable_from_export_context():
    from paper_trading.small_capital_strategy.paper_cockpit_v204 import run_portfolio_review
    result = run_portfolio_review()
    assert result.paper_only is True
    assert result.all_passed is True

# -------------------------------------------------------------------------
# v201 relative-path compatibility not regressed
# -------------------------------------------------------------------------
def test_v201_health_test_file_exists():
    import os
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "..",
        "paper_trading", "small_capital_strategy",
        "paper_cockpit_health_v201.py"
    ))
    assert os.path.exists(path)

def test_v201_test_file_exists_relative():
    import os
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "test_paper_cockpit_v201.py"
    ))
    assert os.path.exists(path)

# -------------------------------------------------------------------------
# GUI render_all_tabs zero error tabs
# -------------------------------------------------------------------------
def test_render_all_tabs_zero_error_tabs_comprehensive():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    error_tabs = [k for k, v in result.items() if "error" in v]
    assert error_tabs == [], f"render_all_tabs error tabs: {error_tabs}"

def test_render_all_tabs_v205_tabs_produce_paper_only_content():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        assert result[tab].get("paper_only") is True, f"Tab {tab} missing paper_only=True"

def test_render_all_tabs_v205_tabs_produce_should_auto_apply_false():
    from gui.small_capital_strategy_panel import render_all_tabs
    result = render_all_tabs()
    for tab in ["watchlist_rotation_v205", "promotion_queue_v205", "human_review_queue_v205"]:
        assert result[tab].get("should_auto_apply") is False, f"Tab {tab} should_auto_apply not False"
