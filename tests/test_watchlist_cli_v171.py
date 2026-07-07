"""tests/test_watchlist_cli_v171.py — CLI command tests for v1.7.1 watchlist commands."""
import pytest
import io
import sys
from main import (
    cmd_watchlist_version,
    cmd_watchlist_profile,
    cmd_watchlist_candidates,
    cmd_watchlist_score,
    cmd_watchlist_rank,
    cmd_watchlist_filter,
    cmd_watchlist_tier,
    cmd_watchlist_theme,
    cmd_watchlist_liquidity,
    cmd_watchlist_revenue,
    cmd_watchlist_technical,
    cmd_watchlist_institutional,
    cmd_watchlist_financing,
    cmd_watchlist_overdiversification,
    cmd_watchlist_top_focus,
    cmd_watchlist_top_tradable,
    cmd_watchlist_report,
    cmd_watchlist_fixtures,
    cmd_watchlist_scenarios,
    cmd_watchlist_health,
    cmd_watchlist_gate,
    cmd_watchlist_safety_audit,
    _WATCHLIST_BANNER,
)


def _capture(fn):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    fn()
    sys.stdout = old
    return buf.getvalue()


def test_banner_has_research_only():
    assert "Research Only" in _WATCHLIST_BANNER


def test_banner_has_paper_only():
    assert "Paper Only" in _WATCHLIST_BANNER


def test_banner_has_no_real_orders():
    assert "No Real Orders" in _WATCHLIST_BANNER


def test_banner_has_not_investment_advice():
    assert "Not Investment Advice" in _WATCHLIST_BANNER


def test_banner_has_version_171():
    assert "1.7.1" in _WATCHLIST_BANNER


def test_cmd_watchlist_version_runs():
    out = _capture(cmd_watchlist_version)
    assert "1.7.1" in out


def test_cmd_watchlist_profile_runs():
    out = _capture(cmd_watchlist_profile)
    assert "30" in out  # default watchlist size


def test_cmd_watchlist_candidates_runs():
    out = _capture(cmd_watchlist_candidates)
    assert "symbol" in out


def test_cmd_watchlist_score_runs():
    out = _capture(cmd_watchlist_score)
    assert "100" in out  # weights sum to 100


def test_cmd_watchlist_rank_runs():
    out = _capture(cmd_watchlist_rank)
    assert len(out) > 0


def test_cmd_watchlist_filter_runs():
    out = _capture(cmd_watchlist_filter)
    assert len(out) > 0


def test_cmd_watchlist_tier_runs():
    out = _capture(cmd_watchlist_tier)
    assert len(out) > 0


def test_cmd_watchlist_theme_runs():
    out = _capture(cmd_watchlist_theme)
    assert len(out) > 0


def test_cmd_watchlist_liquidity_runs():
    out = _capture(cmd_watchlist_liquidity)
    assert len(out) > 0


def test_cmd_watchlist_revenue_runs():
    out = _capture(cmd_watchlist_revenue)
    assert len(out) > 0


def test_cmd_watchlist_technical_runs():
    out = _capture(cmd_watchlist_technical)
    assert len(out) > 0


def test_cmd_watchlist_institutional_runs():
    out = _capture(cmd_watchlist_institutional)
    assert len(out) > 0


def test_cmd_watchlist_financing_runs():
    out = _capture(cmd_watchlist_financing)
    assert len(out) > 0


def test_cmd_watchlist_overdiversification_runs():
    out = _capture(cmd_watchlist_overdiversification)
    assert len(out) > 0


def test_cmd_watchlist_top_focus_runs():
    out = _capture(cmd_watchlist_top_focus)
    assert len(out) > 0


def test_cmd_watchlist_top_tradable_runs():
    out = _capture(cmd_watchlist_top_tradable)
    assert len(out) > 0


def test_cmd_watchlist_report_runs():
    out = _capture(cmd_watchlist_report)
    assert len(out) > 0


def test_cmd_watchlist_fixtures_runs():
    out = _capture(cmd_watchlist_fixtures)
    assert "73" in out or "valid" in out


def test_cmd_watchlist_scenarios_runs():
    out = _capture(cmd_watchlist_scenarios)
    assert "70" in out or "wl_sc_" in out


def test_cmd_watchlist_health_runs():
    out = _capture(cmd_watchlist_health)
    assert "all_passed=True" in out or "passed" in out


def test_cmd_watchlist_gate_runs():
    out = _capture(cmd_watchlist_gate)
    assert "gate_passed=True" in out or "passed" in out


def test_cmd_watchlist_safety_audit_runs():
    out = _capture(cmd_watchlist_safety_audit)
    assert len(out) > 0


def test_all_cli_commands_have_banner():
    cmds = [
        cmd_watchlist_version, cmd_watchlist_profile, cmd_watchlist_candidates,
        cmd_watchlist_score, cmd_watchlist_rank, cmd_watchlist_filter,
        cmd_watchlist_tier, cmd_watchlist_theme, cmd_watchlist_liquidity,
        cmd_watchlist_revenue, cmd_watchlist_technical, cmd_watchlist_institutional,
        cmd_watchlist_financing, cmd_watchlist_overdiversification,
        cmd_watchlist_top_focus, cmd_watchlist_top_tradable, cmd_watchlist_report,
        cmd_watchlist_fixtures, cmd_watchlist_scenarios, cmd_watchlist_health,
        cmd_watchlist_gate, cmd_watchlist_safety_audit,
    ]
    for fn in cmds:
        out = _capture(fn)
        assert "Research Only" in out, f"{fn.__name__} missing banner"
