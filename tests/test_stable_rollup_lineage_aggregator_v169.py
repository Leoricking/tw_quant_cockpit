"""
tests/test_stable_rollup_lineage_aggregator_v169.py
Tests for lineage_aggregator_v169 module.
"""
import pytest
from paper_trading.stable_rollup.lineage_aggregator_v169 import run, EXPECTED_CHAIN


def test_run_returns_dict():
    result = run()
    assert isinstance(result, dict)


def test_run_has_name():
    result = run()
    assert result["name"] == "lineage_aggregator_v169"


def test_run_has_version_chain():
    result = run()
    assert "version_chain" in result
    assert isinstance(result["version_chain"], list)


def test_run_chain_length_ge_13():
    result = run()
    assert result["chain_length"] >= 13


def test_run_intact_true():
    result = run()
    assert result["intact"] is True


def test_run_no_broken_links():
    result = run()
    assert result["broken_links"] == []


def test_run_no_cycles():
    result = run()
    assert result["cycles"] == []


def test_run_status_pass():
    result = run()
    assert result["status"] == "PASS"


def test_run_paper_only():
    result = run()
    assert result.get("paper_only") is True


def test_run_no_real_orders():
    result = run()
    assert result.get("no_real_orders") is True


def test_chain_contains_160():
    result = run()
    assert "1.6.0" in result["version_chain"]


def test_chain_contains_169():
    result = run()
    assert "1.6.9" in result["version_chain"]


def test_expected_chain_has_13():
    assert len(EXPECTED_CHAIN) == 13


def test_chain_order_root_first():
    result = run()
    chain = result["version_chain"]
    assert chain[0] == "1.6.0"
    assert chain[-1] == "1.6.9"
