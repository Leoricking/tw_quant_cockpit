"""[!] Research Only. Paper Only. No Real Orders."""
import pytest
from paper_trading.performance_attribution.session_attribution_v167 import SessionAttributionEngine


def _engine():
    return SessionAttributionEngine()


def _compute(**kwargs):
    defaults = dict(
        session_id="sess-001",
        session_return=0.02,
        session_pnl=2000.0,
        session_risk=0.01,
        session_cost=100.0,
        session_slippage=50.0,
        session_turnover=0.3,
        capital_usage=0.7,
        symbol_overlap=["AAPL"],
        strategy_overlap=["mean_reversion"],
    )
    defaults.update(kwargs)
    return _engine().compute(**defaults)


def test_session_engine_instantiates():
    assert _engine() is not None


def test_session_engine_has_compute():
    assert callable(getattr(_engine(), "compute", None))


def test_session_engine_has_compare_sessions():
    assert callable(getattr(_engine(), "compare_sessions", None))


def test_session_compute_returns_dict():
    result = _compute()
    assert isinstance(result, dict)


def test_session_compute_session_id_stored():
    result = _compute(session_id="my-session")
    assert result.get("session_id") == "my-session"


def test_session_compute_session_return_stored():
    result = _compute(session_return=0.03)
    assert isinstance(result.get("session_return"), float)


def test_session_compute_paper_only_true():
    result = _compute()
    assert result.get("paper_only") is True


def test_session_compute_research_only_true():
    result = _compute()
    assert result.get("research_only") is True


def test_session_compute_no_real_orders_true():
    result = _compute()
    assert result.get("no_real_orders") is True


def test_session_compute_stale_session_flag():
    result = _compute(stale_session=True)
    assert isinstance(result, dict)


def test_session_compute_failed_session_flag():
    result = _compute(failed_session=True)
    assert isinstance(result, dict)


def test_session_compute_empty_overlaps():
    result = _compute(symbol_overlap=[], strategy_overlap=[])
    assert isinstance(result, dict)


def test_session_compute_with_contributions():
    result = _compute(
        recovery_contribution=0.001,
        leader_contribution=0.002,
        follower_contribution=-0.001,
    )
    assert isinstance(result, dict)
