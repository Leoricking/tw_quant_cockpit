"""tests/test_strategy_sandbox_cli_v192.py
Tests for strategy sandbox CLI command handlers v1.9.2.
[!] Research Only. Paper Only. Sandbox Only. Shadow Only.
"""
import pytest
from main import (
    cmd_strategy_sandbox_version,
    cmd_strategy_sandbox_run,
    cmd_strategy_sandbox_compare,
    cmd_strategy_sandbox_shadow,
    cmd_strategy_sandbox_rules,
    cmd_strategy_sandbox_guardrails,
    cmd_strategy_sandbox_abc,
    cmd_strategy_sandbox_position_sizing,
    cmd_strategy_sandbox_cash_reserve,
    cmd_strategy_sandbox_concentration,
    cmd_strategy_sandbox_report,
    cmd_strategy_sandbox_dashboard,
    cmd_strategy_sandbox_export,
    cmd_strategy_sandbox_evidence,
    cmd_strategy_sandbox_audit,
    cmd_strategy_sandbox_health,
    cmd_strategy_sandbox_gate,
    cmd_strategy_sandbox_scenarios,
    cmd_strategy_sandbox_fixtures,
    cmd_strategy_sandbox_safety_audit,
)


# ── cmd_strategy_sandbox_version ──────────────────────────────────────────────

def test_cmd_strategy_sandbox_version_runs(capsys):
    cmd_strategy_sandbox_version()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_version_research_only(capsys):
    cmd_strategy_sandbox_version()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out

def test_cmd_strategy_sandbox_version_paper_only_in_output(capsys):
    cmd_strategy_sandbox_version()
    captured = capsys.readouterr()
    assert "paper_only=True" in captured.out

def test_cmd_strategy_sandbox_version_sandbox_only_in_output(capsys):
    cmd_strategy_sandbox_version()
    captured = capsys.readouterr()
    assert "sandbox_only=True" in captured.out


# ── cmd_strategy_sandbox_run ──────────────────────────────────────────────────

def test_cmd_strategy_sandbox_run_runs(capsys):
    cmd_strategy_sandbox_run()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_run_research_only(capsys):
    cmd_strategy_sandbox_run()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_compare ──────────────────────────────────────────────

def test_cmd_strategy_sandbox_compare_runs(capsys):
    cmd_strategy_sandbox_compare()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_compare_research_only(capsys):
    cmd_strategy_sandbox_compare()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_shadow ───────────────────────────────────────────────

def test_cmd_strategy_sandbox_shadow_runs(capsys):
    cmd_strategy_sandbox_shadow()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_shadow_research_only(capsys):
    cmd_strategy_sandbox_shadow()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_rules ────────────────────────────────────────────────

def test_cmd_strategy_sandbox_rules_runs(capsys):
    cmd_strategy_sandbox_rules()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_rules_research_only(capsys):
    cmd_strategy_sandbox_rules()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_guardrails ──────────────────────────────────────────

def test_cmd_strategy_sandbox_guardrails_runs(capsys):
    cmd_strategy_sandbox_guardrails()
    captured = capsys.readouterr()
    assert captured.out != ""


# ── cmd_strategy_sandbox_abc ──────────────────────────────────────────────────

def test_cmd_strategy_sandbox_abc_runs(capsys):
    cmd_strategy_sandbox_abc()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_abc_research_only(capsys):
    cmd_strategy_sandbox_abc()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_position_sizing ──────────────────────────────────────

def test_cmd_strategy_sandbox_position_sizing_runs(capsys):
    cmd_strategy_sandbox_position_sizing()
    captured = capsys.readouterr()
    assert captured.out != ""


# ── cmd_strategy_sandbox_cash_reserve ────────────────────────────────────────

def test_cmd_strategy_sandbox_cash_reserve_runs(capsys):
    cmd_strategy_sandbox_cash_reserve()
    captured = capsys.readouterr()
    assert captured.out != ""


# ── cmd_strategy_sandbox_concentration ───────────────────────────────────────

def test_cmd_strategy_sandbox_concentration_runs(capsys):
    cmd_strategy_sandbox_concentration()
    captured = capsys.readouterr()
    assert captured.out != ""


# ── cmd_strategy_sandbox_report ───────────────────────────────────────────────

def test_cmd_strategy_sandbox_report_runs(capsys):
    cmd_strategy_sandbox_report()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_report_research_only(capsys):
    cmd_strategy_sandbox_report()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_dashboard ───────────────────────────────────────────

def test_cmd_strategy_sandbox_dashboard_runs(capsys):
    cmd_strategy_sandbox_dashboard()
    captured = capsys.readouterr()
    assert captured.out != ""


# ── cmd_strategy_sandbox_export ───────────────────────────────────────────────

def test_cmd_strategy_sandbox_export_runs(capsys):
    cmd_strategy_sandbox_export()
    captured = capsys.readouterr()
    assert captured.out != ""


# ── cmd_strategy_sandbox_evidence ────────────────────────────────────────────

def test_cmd_strategy_sandbox_evidence_runs(capsys):
    cmd_strategy_sandbox_evidence()
    captured = capsys.readouterr()
    assert captured.out != ""


# ── cmd_strategy_sandbox_audit ────────────────────────────────────────────────

def test_cmd_strategy_sandbox_audit_runs(capsys):
    cmd_strategy_sandbox_audit()
    captured = capsys.readouterr()
    assert captured.out != ""


# ── cmd_strategy_sandbox_health ───────────────────────────────────────────────

def test_cmd_strategy_sandbox_health_runs(capsys):
    cmd_strategy_sandbox_health()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_health_research_only(capsys):
    cmd_strategy_sandbox_health()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_gate ─────────────────────────────────────────────────

def test_cmd_strategy_sandbox_gate_runs(capsys):
    cmd_strategy_sandbox_gate()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_gate_research_only(capsys):
    cmd_strategy_sandbox_gate()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_scenarios ───────────────────────────────────────────

def test_cmd_strategy_sandbox_scenarios_runs(capsys):
    cmd_strategy_sandbox_scenarios()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_scenarios_count_in_output(capsys):
    cmd_strategy_sandbox_scenarios()
    captured = capsys.readouterr()
    assert "count=" in captured.out

def test_cmd_strategy_sandbox_scenarios_research_only(capsys):
    cmd_strategy_sandbox_scenarios()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_fixtures ────────────────────────────────────────────

def test_cmd_strategy_sandbox_fixtures_runs(capsys):
    cmd_strategy_sandbox_fixtures()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_fixtures_count_in_output(capsys):
    cmd_strategy_sandbox_fixtures()
    captured = capsys.readouterr()
    assert "count=" in captured.out

def test_cmd_strategy_sandbox_fixtures_research_only(capsys):
    cmd_strategy_sandbox_fixtures()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out


# ── cmd_strategy_sandbox_safety_audit ────────────────────────────────────────

def test_cmd_strategy_sandbox_safety_audit_runs(capsys):
    cmd_strategy_sandbox_safety_audit()
    captured = capsys.readouterr()
    assert captured.out != ""

def test_cmd_strategy_sandbox_safety_audit_all_safe_in_output(capsys):
    cmd_strategy_sandbox_safety_audit()
    captured = capsys.readouterr()
    assert "all_safe=" in captured.out

def test_cmd_strategy_sandbox_safety_audit_research_only(capsys):
    cmd_strategy_sandbox_safety_audit()
    captured = capsys.readouterr()
    assert "RESEARCH ONLY" in captured.out
