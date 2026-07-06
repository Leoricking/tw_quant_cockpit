"""
tests/test_stable_rollup_scorecard_v169.py
Tests for stable_scorecard_v169 module.
"""
import pytest
from paper_trading.stable_rollup.stable_scorecard_v169 import (
    StableScorecard, compute_scorecard, SCORE_WEIGHTS,
)
from paper_trading.stable_rollup.enums_v169 import ConfidenceLevel


def test_score_weights_sum_100():
    assert sum(SCORE_WEIGHTS.values()) == 100


def test_score_weights_safety_20():
    assert SCORE_WEIGHTS["safety"] == 20


def test_score_weights_has_all_domains():
    expected = {
        "release_identity", "manifest", "compatibility", "capability",
        "safety", "health", "gate", "cli", "gui", "fixtures_scenarios", "determinism",
    }
    assert set(SCORE_WEIGHTS.keys()) == expected


def test_scorecard_instantiable():
    sc = StableScorecard()
    assert sc is not None


def test_compute_returns_score():
    sc = StableScorecard()
    score = sc.compute()
    assert hasattr(score, "total_score")


def test_compute_not_for_real_trading():
    sc = StableScorecard()
    score = sc.compute()
    assert score.not_for_real_trading is True


def test_safety_failure_returns_blocked():
    sc = StableScorecard()
    score = sc.compute(safety_summary={"status": "FAIL", "failed": 5})
    assert score.grade == "BLOCKED"
    assert score.total_score == 0.0


def test_safety_failure_has_blocking_issue():
    sc = StableScorecard()
    score = sc.compute(safety_summary={"status": "FAIL", "failed": 1})
    assert len(score.blocking_issues) > 0


def test_all_pass_gives_perfect_score():
    sc = StableScorecard()
    score = sc.compute(
        safety_summary={"status": "PASS", "failed": 0},
        health_summary={"status": "PASS", "all_pass": True},
        gate_summary={"status": "PASS", "all_pass": True},
        cli_summary={"status": "PASS"},
        manifest_valid=True,
        compat_valid=True,
        capability_valid=True,
        fixture_valid=True,
        scenario_valid=True,
        determinism_valid=True,
        release_identity_valid=True,
        gui_valid=True,
    )
    assert score.total_score == 100.0
    assert score.grade == "A"


def test_score_component_scores_is_dict():
    sc = StableScorecard()
    score = sc.compute()
    assert isinstance(score.component_scores, dict)


def test_compute_scorecard_returns_score():
    score = compute_scorecard()
    assert hasattr(score, "total_score")
    assert score.not_for_real_trading is True


def test_grade_function():
    sc = StableScorecard()
    assert sc._grade(100) == "A"
    assert sc._grade(95) == "A"
    assert sc._grade(90) == "A"
    assert sc._grade(80) == "B"
    assert sc._grade(70) == "C"
    assert sc._grade(60) == "D"
    assert sc._grade(50) == "F"


def test_compute_scorecard_paper_only():
    score = compute_scorecard()
    assert score.paper_only is True


def test_compute_scorecard_no_real_orders():
    score = compute_scorecard()
    assert score.no_real_orders is True
