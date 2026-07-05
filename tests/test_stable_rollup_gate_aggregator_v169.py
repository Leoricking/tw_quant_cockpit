"""
tests/test_stable_rollup_gate_aggregator_v169.py
Tests for gate_aggregator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.gate_aggregator_v169 import run


def test_run_returns_dict():
    result = run()
    assert isinstance(result, dict)


def test_run_has_name():
    result = run()
    assert result["name"] == "gate_aggregator_v169"


def test_run_has_version():
    result = run()
    assert result["version"] == "1.6.9"


def test_run_has_status():
    result = run()
    assert "status" in result
    assert result["status"] in ("PASS", "FAIL", "DEGRADED")


def test_run_has_summaries():
    result = run()
    assert "summaries" in result
    assert isinstance(result["summaries"], list)


def test_run_summaries_count():
    result = run()
    assert result["total_gates"] == 4


def test_run_paper_only():
    result = run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    result = run()
    assert result.get("no_real_orders") is True


def test_each_summary_has_gate_name():
    result = run()
    for s in result["summaries"]:
        assert "gate_name" in s


def test_each_summary_has_gate_passed():
    result = run()
    for s in result["summaries"]:
        assert "gate_passed" in s
        assert isinstance(s["gate_passed"], bool)


def test_run_has_all_pass():
    result = run()
    assert "all_pass" in result


def test_stable_rollup_gate_in_summaries():
    result = run()
    names = [s["gate_name"] for s in result["summaries"]]
    assert any("stable_rollup" in n for n in names)


def test_run_deterministic():
    r1 = run()
    r2 = run()
    assert r1["total_gates"] == r2["total_gates"]
    assert [s["gate_name"] for s in r1["summaries"]] == [s["gate_name"] for s in r2["summaries"]]
