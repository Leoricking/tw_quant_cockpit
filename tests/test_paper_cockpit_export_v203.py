"""
tests/test_paper_cockpit_export_v203.py
v2.0.3 Export Integration Tests (JSON / Markdown / CSV / Audit Snapshot)
[!] Paper Only. Research Only. No Real Orders. Not Investment Advice.
"""
import pytest

# ---------------------------------------------------------------------------
# SimulationExportResult model
# ---------------------------------------------------------------------------

def test_simulation_export_result_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationExportResult
    obj = SimulationExportResult()
    assert obj is not None

def test_simulation_export_result_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationExportResult
    obj = SimulationExportResult()
    assert obj.paper_only is True

def test_simulation_export_result_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationExportResult
    obj = SimulationExportResult()
    assert obj.no_real_orders is True

def test_simulation_export_result_has_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationExportResult
    obj = SimulationExportResult()
    assert hasattr(obj, "is_valid")

# ---------------------------------------------------------------------------
# SimulationAuditSnapshot model
# ---------------------------------------------------------------------------

def test_simulation_audit_snapshot_instantiable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationAuditSnapshot
    obj = SimulationAuditSnapshot()
    assert obj is not None

def test_simulation_audit_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationAuditSnapshot
    obj = SimulationAuditSnapshot()
    assert obj.paper_only is True

def test_simulation_audit_snapshot_has_reproducibility_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationAuditSnapshot
    obj = SimulationAuditSnapshot()
    assert hasattr(obj, "reproducibility_hash")

def test_simulation_audit_snapshot_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import SimulationAuditSnapshot
    obj = SimulationAuditSnapshot()
    assert obj.schema_version == "203"

# ---------------------------------------------------------------------------
# export_simulation_json
# ---------------------------------------------------------------------------

def test_export_simulation_json_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result is not None

def test_export_simulation_json_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result.is_valid is True

def test_export_simulation_json_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result.paper_only is True

def test_export_simulation_json_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result.no_real_orders is True

def test_export_simulation_json_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result.export_format == "json"

def test_export_simulation_json_has_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_json
    result = export_simulation_json(simulate_one())
    assert result.content is not None

# ---------------------------------------------------------------------------
# export_simulation_markdown
# ---------------------------------------------------------------------------

def test_export_simulation_markdown_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_markdown
    result = export_simulation_markdown(simulate_one())
    assert result is not None

def test_export_simulation_markdown_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_markdown
    result = export_simulation_markdown(simulate_one())
    assert result.is_valid is True

def test_export_simulation_markdown_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_markdown
    result = export_simulation_markdown(simulate_one())
    assert result.paper_only is True

def test_export_simulation_markdown_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_markdown
    result = export_simulation_markdown(simulate_one())
    assert result.no_real_orders is True

def test_export_simulation_markdown_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_markdown
    result = export_simulation_markdown(simulate_one())
    assert result.export_format == "markdown"

def test_export_simulation_markdown_has_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_markdown
    result = export_simulation_markdown(simulate_one())
    assert result.content is not None

# ---------------------------------------------------------------------------
# export_simulation_csv
# ---------------------------------------------------------------------------

def test_export_simulation_csv_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_csv
    result = export_simulation_csv(simulate_one())
    assert result is not None

def test_export_simulation_csv_is_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_csv
    result = export_simulation_csv(simulate_one())
    assert result.is_valid is True

def test_export_simulation_csv_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_csv
    result = export_simulation_csv(simulate_one())
    assert result.paper_only is True

def test_export_simulation_csv_no_real_orders():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_csv
    result = export_simulation_csv(simulate_one())
    assert result.no_real_orders is True

def test_export_simulation_csv_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_csv
    result = export_simulation_csv(simulate_one())
    assert result.export_format == "csv"

def test_export_simulation_csv_has_content():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, export_simulation_csv
    result = export_simulation_csv(simulate_one())
    assert result.content is not None

# ---------------------------------------------------------------------------
# build_simulation_audit_snapshot
# ---------------------------------------------------------------------------

def test_build_simulation_audit_snapshot_callable():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_simulation_audit_snapshot
    result = build_simulation_audit_snapshot(simulate_one())
    assert result is not None

def test_build_simulation_audit_snapshot_has_hash():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_simulation_audit_snapshot
    result = build_simulation_audit_snapshot(simulate_one())
    assert result.reproducibility_hash

def test_build_simulation_audit_snapshot_paper_only():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_simulation_audit_snapshot
    result = build_simulation_audit_snapshot(simulate_one())
    assert result.paper_only is True

def test_build_simulation_audit_snapshot_schema_version():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_simulation_audit_snapshot
    result = build_simulation_audit_snapshot(simulate_one())
    assert result.schema_version == "203"

def test_build_simulation_audit_snapshot_hash_is_string():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_simulation_audit_snapshot
    result = build_simulation_audit_snapshot(simulate_one())
    assert isinstance(result.reproducibility_hash, str)

def test_build_simulation_audit_snapshot_export_format():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import simulate_one, build_simulation_audit_snapshot
    result = build_simulation_audit_snapshot(simulate_one())
    assert result.export_format == "audit_snapshot"

def test_export_all_formats_valid():
    from paper_trading.small_capital_strategy.paper_cockpit_v203 import (
        simulate_one, export_simulation_json, export_simulation_markdown, export_simulation_csv
    )
    sim = simulate_one()
    assert export_simulation_json(sim).is_valid is True
    assert export_simulation_markdown(sim).is_valid is True
    assert export_simulation_csv(sim).is_valid is True
