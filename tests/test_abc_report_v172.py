"""tests/test_abc_report_v172.py — Execution report tests for v1.7.2."""
import pytest
from paper_trading.small_capital_strategy.abc_execution_report_v172 import (
    build_report, render_markdown, render_json, render_csv, render_console_summary,
    get_section_names, SECTION_NAMES,
)
from paper_trading.small_capital_strategy.abc_execution_plan_builder_v172 import (
    build_execution_plan,
)
from paper_trading.small_capital_strategy.abc_execution_models_v172 import ABCSignalInput
from paper_trading.small_capital_strategy.abc_execution_enums_v172 import ABCBuyPointType


def _make_sig():
    return ABCSignalInput(
        symbol="2330", buy_point_type=ABCBuyPointType.A_10MA_PULLBACK,
        close=100.0, ma5=99.0, ma10=98.0, ma20=95.0, ma60=85.0,
        volume=700_000, avg_volume_20d=1_000_000, volume_ratio=0.7, atr_pct=0.05,
        kd_k=60.0, kd_d=50.0, kd_dead_cross=False, financing_ratio=0.10,
        institutional_net_buy_days=5, theme_strength="STRONG",
        consolidation_weeks=3, prior_platform_high=95.0,
        had_first_wave=True, pullback_completed=True,
        volume_dry_up_before_reclaim=True, kd_golden_cross=True,
        institutional_reaccumulation=True, tier="MAIN_THEME", market_regime="BULL",
    )


def _make_report():
    sig = _make_sig()
    plan = build_execution_plan(sig, 0)
    return build_report(plan)


def test_section_names_count_16():
    assert len(get_section_names()) == 16


def test_section_names_has_summary():
    assert "abc_execution_summary" in get_section_names()


def test_section_names_has_not_investment_advice():
    assert "not_investment_advice" in get_section_names()


def test_build_report_returns_report():
    report = _make_report()
    assert report is not None


def test_report_has_all_16_sections():
    report = _make_report()
    for name in SECTION_NAMES:
        assert name in report.sections


def test_report_paper_only():
    report = _make_report()
    assert report.paper_only is True


def test_render_markdown_nonempty():
    report = _make_report()
    md = render_markdown(report)
    assert len(md) > 100


def test_render_markdown_has_symbol():
    report = _make_report()
    md = render_markdown(report)
    assert "2330" in md


def test_render_json_valid():
    import json
    report = _make_report()
    j = render_json(report)
    data = json.loads(j)
    assert data["symbol"] == "2330"


def test_render_json_paper_only():
    import json
    report = _make_report()
    j = render_json(report)
    data = json.loads(j)
    assert data["paper_only"] is True


def test_render_json_no_real_orders():
    import json
    report = _make_report()
    j = render_json(report)
    data = json.loads(j)
    assert data["no_real_orders"] is True


def test_render_csv_has_header():
    report = _make_report()
    csv_str = render_csv(report)
    assert "symbol" in csv_str
    assert "grade" in csv_str


def test_render_console_summary_has_symbol():
    report = _make_report()
    s = render_console_summary(report)
    assert "2330" in s


def test_render_console_summary_paper_only():
    report = _make_report()
    s = render_console_summary(report)
    assert "PaperOnly=True" in s


def test_render_console_summary_no_real_orders():
    report = _make_report()
    s = render_console_summary(report)
    assert "NoRealOrders=True" in s


def test_report_sections_summary_paper_only():
    report = _make_report()
    assert report.sections["abc_execution_summary"]["paper_only"] is True


def test_report_sections_not_investment_advice():
    report = _make_report()
    assert report.sections["not_investment_advice"]["not_investment_advice"] is True


def test_report_sections_paper_order_intent_no_real():
    report = _make_report()
    assert report.sections["paper_order_intent"]["no_real_orders"] is True


def test_report_sections_paper_order_intent_broker_disabled():
    report = _make_report()
    assert report.sections["paper_order_intent"]["broker_execution_enabled"] is False


def test_report_symbol_correct():
    report = _make_report()
    assert report.symbol == "2330"


def test_render_json_not_investment_advice():
    import json
    report = _make_report()
    j = render_json(report)
    data = json.loads(j)
    assert data["not_investment_advice"] is True


def test_render_markdown_has_disclaimer():
    report = _make_report()
    md = render_markdown(report)
    assert "Research Only" in md or "Paper Only" in md


def test_report_no_real_orders():
    report = _make_report()
    assert report.no_real_orders is True
