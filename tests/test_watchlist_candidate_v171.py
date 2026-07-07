"""tests/test_watchlist_candidate_v171.py — candidate construction tests for v1.7.1."""
import pytest
from paper_trading.small_capital_strategy.watchlist_enums_v171 import (
    WatchlistTier, ThemeStrength, ThemeCategory,
)
from paper_trading.small_capital_strategy.watchlist_candidate_v171 import (
    make_sample_candidate, build_candidate, validate_candidate_fields,
    get_required_candidate_fields, REQUIRED_CANDIDATE_FIELDS,
)


def test_make_sample_paper_only():
    c = make_sample_candidate()
    assert c.paper_only is True


def test_make_sample_research_only():
    c = make_sample_candidate()
    assert c.research_only is True


def test_make_sample_no_real_orders():
    c = make_sample_candidate()
    assert c.no_real_orders is True


def test_make_sample_not_investment_advice():
    c = make_sample_candidate()
    assert c.not_investment_advice is True


def test_make_sample_default_symbol():
    c = make_sample_candidate()
    assert c.symbol == "2330"


def test_make_sample_custom_symbol():
    c = make_sample_candidate("9999")
    assert c.symbol == "9999"


def test_make_sample_tier():
    c = make_sample_candidate(tier=WatchlistTier.TRAINING)
    assert c.watchlist_tier == WatchlistTier.TRAINING


def test_make_sample_score():
    c = make_sample_candidate(total_score=75.0)
    assert c.total_score == 75.0


def test_validate_candidate_valid():
    c = make_sample_candidate()
    result = validate_candidate_fields(c)
    assert result["valid"] is True
    assert result["issues"] == []


def test_validate_candidate_invalid_score():
    c = make_sample_candidate(total_score=150.0)
    result = validate_candidate_fields(c)
    assert result["valid"] is False


def test_get_required_fields_is_list():
    fields = get_required_candidate_fields()
    assert isinstance(fields, list)


def test_required_fields_has_symbol():
    assert "symbol" in REQUIRED_CANDIDATE_FIELDS


def test_required_fields_has_theme():
    assert "theme" in REQUIRED_CANDIDATE_FIELDS


def test_required_fields_has_total_score():
    assert "total_score" in REQUIRED_CANDIDATE_FIELDS


def test_build_candidate_from_dict():
    data = {
        "symbol": "1234", "name": "Test", "market": "TWSE",
        "sector": "Tech", "industry": "Semi",
        "theme": "AI", "theme_category": "AI_SEMICONDUCTOR",
        "theme_strength": "STRONG",
        "liquidity_score": 80.0, "revenue_growth_score": 70.0,
        "technical_score": 75.0, "institutional_score": 65.0,
        "financing_score": 60.0, "volatility_risk_score": 70.0,
        "concentration_risk_score": 80.0, "small_capital_fit_score": 75.0,
        "total_score": 72.0, "watchlist_tier": "CORE",
    }
    c = build_candidate(data)
    assert c.symbol == "1234"
    assert c.paper_only is True


def test_build_candidate_missing_field_raises():
    data = {"symbol": "X"}
    with pytest.raises(ValueError):
        build_candidate(data)


def test_candidate_exclusion_reasons_empty():
    c = make_sample_candidate()
    assert c.exclusion_reasons == []


def test_candidate_schema_version():
    c = make_sample_candidate()
    assert c.schema_version == "171"
