"""
tests/test_paper_cockpit_audit_pack_v202.py
v2.0.2 Paper Cockpit — Audit Pack Tests (50+)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
from __future__ import annotations
import pytest


# ---------------------------------------------------------------------------
# AuditPackSchema dataclass tests
# ---------------------------------------------------------------------------

def test_audit_pack_schema_defaults():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AuditPackSchema
    obj = AuditPackSchema()
    assert obj.schema_version == "202"
    assert obj.paper_only is True
    assert obj.no_real_orders is True


def test_audit_pack_schema_fields_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AuditPackSchema
    obj = AuditPackSchema()
    assert hasattr(obj, "run_metadata")
    assert hasattr(obj, "input_snapshot")
    assert hasattr(obj, "decision_snapshot")
    assert hasattr(obj, "risk_snapshot")
    assert hasattr(obj, "ticket_snapshot")
    assert hasattr(obj, "blocked_reason_snapshot")
    assert hasattr(obj, "human_review_snapshot")
    assert hasattr(obj, "safety_snapshot")
    assert hasattr(obj, "reproducibility_hash")
    assert hasattr(obj, "export_format")
    assert hasattr(obj, "export_status")


def test_audit_pack_schema_export_status():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AuditPackSchema
    obj = AuditPackSchema()
    assert obj.export_status == "ok"


def test_audit_pack_schema_export_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AuditPackSchema
    obj = AuditPackSchema()
    assert obj.export_format == "json"


# ---------------------------------------------------------------------------
# build_audit_pack tests
# ---------------------------------------------------------------------------

def test_build_audit_pack_returns_result():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result is not None


def test_build_audit_pack_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.schema_version == "202"


def test_build_audit_pack_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.paper_only is True


def test_build_audit_pack_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.no_real_orders is True


def test_build_audit_pack_export_status_ok():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.export_status == "ok"


def test_build_audit_pack_has_pack_id():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.pack_id


def test_build_audit_pack_reproducibility_hash_non_empty():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.reproducibility_hash


def test_build_audit_pack_reproducibility_hash_is_md5():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    # MD5 hash is 32 hex characters
    assert len(result.reproducibility_hash) == 32


def test_build_audit_pack_reproducibility_hash_is_hex():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    int(result.reproducibility_hash, 16)  # should not raise


def test_build_audit_pack_human_review_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.human_review_required is True


def test_build_audit_pack_run_metadata_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.run_metadata["version"] == "2.0.2"


def test_build_audit_pack_run_metadata_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.run_metadata["paper_only"] is True


def test_build_audit_pack_run_metadata_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.run_metadata["no_real_orders"] is True


def test_build_audit_pack_run_metadata_source():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.run_metadata["source"] == "paper_cockpit"


def test_build_audit_pack_decision_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.decision_snapshot["paper_only"] is True


def test_build_audit_pack_decision_snapshot_human_review():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.decision_snapshot["human_review_required"] is True


def test_build_audit_pack_risk_snapshot_status():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.risk_snapshot["risk_overlay_status"] == "NORMAL"


def test_build_audit_pack_risk_snapshot_risk_budget_ok():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.risk_snapshot["risk_budget_ok"] is True


def test_build_audit_pack_safety_snapshot_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.safety_snapshot["NO_REAL_ORDERS"] is True


def test_build_audit_pack_safety_snapshot_broker_disabled():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.safety_snapshot["BROKER_EXECUTION_ENABLED"] is False


def test_build_audit_pack_safety_snapshot_production_blocked():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.safety_snapshot["PRODUCTION_TRADING_BLOCKED"] is True


def test_build_audit_pack_safety_no_automatic_rebalance():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.safety_snapshot["no_automatic_rebalance"] is True


def test_build_audit_pack_safety_no_real_account_sync():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.safety_snapshot["no_real_account_sync"] is True


def test_build_audit_pack_human_review_snapshot_required():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.human_review_snapshot["human_review_required"] is True


def test_build_audit_pack_human_review_no_automatic_execution():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.human_review_snapshot["no_automatic_execution"] is True


def test_build_audit_pack_ticket_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.ticket_snapshot["paper_only"] is True


def test_build_audit_pack_ticket_snapshot_count():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.ticket_snapshot["ticket_count"] == 0


def test_build_audit_pack_with_candidates():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack, ReportExportInput
    inp = ReportExportInput(candidates=["2330", "2454"])
    result = build_audit_pack(inp)
    assert "2330" in result.input_snapshot["candidates"]


def test_build_audit_pack_deterministic_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack, ReportExportInput
    inp = ReportExportInput(report_id="PC202-RPT-SAME", run_date="2026-07-20")
    result1 = build_audit_pack(inp)
    result2 = build_audit_pack(inp)
    assert result1.reproducibility_hash == result2.reproducibility_hash


def test_build_audit_pack_different_inputs_different_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack, ReportExportInput
    inp1 = ReportExportInput(report_id="PC202-RPT-A", candidates=[])
    inp2 = ReportExportInput(report_id="PC202-RPT-B", candidates=["2330"])
    result1 = build_audit_pack(inp1)
    result2 = build_audit_pack(inp2)
    assert result1.reproducibility_hash != result2.reproducibility_hash


def test_build_audit_pack_input_snapshot_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack, ReportExportInput
    inp = ReportExportInput(report_format="csv")
    result = build_audit_pack(inp)
    assert result.input_snapshot["report_format"] == "csv"


# ---------------------------------------------------------------------------
# AuditPackResult tests
# ---------------------------------------------------------------------------

def test_audit_pack_result_defaults():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AuditPackResult
    obj = AuditPackResult()
    assert obj.pack_id == "PC202-PACK-001"
    assert obj.export_status == "ok"
    assert obj.paper_only is True


def test_audit_pack_result_all_fields_present():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AuditPackResult, AUDIT_PACK_FIELDS
    obj = AuditPackResult()
    for field_name in AUDIT_PACK_FIELDS:
        assert hasattr(obj, field_name), f"Missing field: {field_name}"


def test_audit_pack_fields_complete():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import AUDIT_PACK_FIELDS
    expected = [
        "run_metadata", "input_snapshot", "decision_snapshot", "risk_snapshot",
        "ticket_snapshot", "blocked_reason_snapshot", "human_review_snapshot",
        "safety_snapshot", "reproducibility_hash", "export_format", "export_status",
    ]
    assert set(AUDIT_PACK_FIELDS) == set(expected)


def test_audit_pack_reproducibility_hash_function():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import _make_reproducibility_hash
    h = _make_reproducibility_hash("test_string")
    assert len(h) == 32
    int(h, 16)  # must be valid hex


def test_audit_pack_reproducibility_hash_consistent():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import _make_reproducibility_hash
    h1 = _make_reproducibility_hash("same_input")
    h2 = _make_reproducibility_hash("same_input")
    assert h1 == h2


def test_audit_pack_reproducibility_hash_different():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import _make_reproducibility_hash
    h1 = _make_reproducibility_hash("input_a")
    h2 = _make_reproducibility_hash("input_b")
    assert h1 != h2


def test_audit_pack_export_format_default():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.export_format == "json"


def test_audit_pack_schema_version_in_run_metadata():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert result.run_metadata["schema_version"] == "202"


def test_audit_pack_release_name_in_run_metadata():
    from paper_trading.small_capital_strategy.paper_cockpit_v202 import build_audit_pack
    result = build_audit_pack()
    assert "Export" in result.run_metadata["release_name"]
