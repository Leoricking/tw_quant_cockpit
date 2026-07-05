"""
tests/test_stable_rollup_gate_v169.py
Tests for the release gate.
"""
import pytest
from release.live_paper_trading_stable_rollup_release_gate_v169 import (
    StableRollupReleaseGate, TARGET_VERSION, RELEASE_NAME, BASE_RELEASE,
    RESEARCH_ONLY, PAPER_ONLY, NO_REAL_ORDERS,
)


def test_target_version():
    assert TARGET_VERSION == "1.6.9"


def test_release_name():
    assert RELEASE_NAME == "Live Paper Trading Stable Rollup"


def test_base_release():
    assert BASE_RELEASE == "1.6.8 Operational Integration Hardening"


def test_safety_flags():
    assert RESEARCH_ONLY is True
    assert PAPER_ONLY is True
    assert NO_REAL_ORDERS is True


def test_gate_instantiable():
    g = StableRollupReleaseGate()
    assert g is not None


def test_run_returns_dict():
    g = StableRollupReleaseGate()
    result = g.run()
    assert isinstance(result, dict)


def test_run_has_gate():
    g = StableRollupReleaseGate()
    result = g.run()
    assert result["gate"] == "live_paper_trading_stable_rollup_release_gate_v169"


def test_run_target_version():
    g = StableRollupReleaseGate()
    result = g.run()
    assert result["target_version"] == "1.6.9"


def test_run_release_name():
    g = StableRollupReleaseGate()
    result = g.run()
    assert result["release_name"] == "Live Paper Trading Stable Rollup"


def test_run_has_status():
    g = StableRollupReleaseGate()
    result = g.run()
    assert "status" in result
    assert result["status"] in ("PASS", "FAIL")


def test_run_gate_passed():
    g = StableRollupReleaseGate()
    result = g.run()
    assert result["gate_passed"] is True, \
        f"Gate failed! failed_checks={[c for c in result['checks'] if c['status']=='FAIL']}"


def test_run_total_ge_70():
    g = StableRollupReleaseGate()
    result = g.run()
    assert result["total"] >= 70


def test_run_no_failed():
    g = StableRollupReleaseGate()
    result = g.run()
    failed = [c["check"] for c in result["checks"] if c["status"] == "FAIL"]
    assert len(failed) == 0, f"Failed: {failed}"


def test_run_paper_only():
    g = StableRollupReleaseGate()
    result = g.run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    g = StableRollupReleaseGate()
    result = g.run()
    assert result.get("no_real_orders") is True


def test_run_not_for_production():
    g = StableRollupReleaseGate()
    result = g.run()
    assert result.get("not_for_production") is True


def test_run_has_checks_list():
    g = StableRollupReleaseGate()
    result = g.run()
    assert isinstance(result["checks"], list)
    assert len(result["checks"]) >= 70
