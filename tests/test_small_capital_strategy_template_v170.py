"""tests/test_small_capital_strategy_template_v170.py — strategy template tests for v1.7.0."""
import pytest
from paper_trading.small_capital_strategy.enums_v170 import MarketRegime, StrategyTemplateStatus
from paper_trading.small_capital_strategy.strategy_template_v170 import (
    build_300k_template, validate_strategy_template, get_template_summary,
)


def test_build_300k_template_bull():
    tmpl = build_300k_template(regime=MarketRegime.BULL)
    assert tmpl is not None


def test_build_300k_template_bear():
    tmpl = build_300k_template(regime=MarketRegime.BEAR)
    assert tmpl is not None


def test_build_300k_template_template_id():
    tmpl = build_300k_template()
    assert tmpl.template_id == "small_capital_300k_v170"


def test_build_300k_template_paper_only():
    tmpl = build_300k_template()
    assert tmpl.paper_only is True


def test_build_300k_template_research_only():
    tmpl = build_300k_template()
    assert tmpl.research_only is True


def test_build_300k_template_no_real_orders():
    tmpl = build_300k_template()
    assert tmpl.no_real_orders is True


def test_build_300k_template_not_investment_advice():
    tmpl = build_300k_template()
    assert tmpl.not_investment_advice is True


def test_build_300k_template_status_active():
    tmpl = build_300k_template()
    assert tmpl.status == StrategyTemplateStatus.ACTIVE


def test_build_300k_template_capital_300k():
    tmpl = build_300k_template()
    assert tmpl.capital_profile.capital_twd == 300000.0


def test_build_300k_template_max_loss_3000():
    tmpl = build_300k_template()
    assert tmpl.risk_budget.max_loss_per_trade == 3000.0


def test_validate_strategy_template_pass():
    tmpl = build_300k_template()
    result = validate_strategy_template(tmpl)
    assert result["valid"] is True


def test_validate_strategy_template_returns_dict():
    tmpl = build_300k_template()
    result = validate_strategy_template(tmpl)
    assert isinstance(result, dict)
    assert "valid" in result
    assert "issues" in result
    assert "template_id" in result


def test_validate_strategy_template_no_issues():
    tmpl = build_300k_template()
    result = validate_strategy_template(tmpl)
    assert result["issues"] == []


def test_get_template_summary_returns_dict():
    tmpl = build_300k_template()
    summary = get_template_summary(tmpl)
    assert isinstance(summary, dict)


def test_get_template_summary_template_id():
    tmpl = build_300k_template()
    summary = get_template_summary(tmpl)
    assert summary["template_id"] == "small_capital_300k_v170"


def test_get_template_summary_capital():
    tmpl = build_300k_template()
    summary = get_template_summary(tmpl)
    assert summary["capital_twd"] == 300000.0


def test_get_template_summary_paper_only():
    tmpl = build_300k_template()
    summary = get_template_summary(tmpl)
    assert summary["paper_only"] is True


def test_build_with_max_loss_override():
    tmpl = build_300k_template(max_loss_override=2400.0)
    assert tmpl.risk_budget.max_loss_per_trade == 2400.0


def test_template_schema_version():
    tmpl = build_300k_template()
    assert tmpl.schema_version == "170"
