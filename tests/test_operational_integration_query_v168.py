"""
tests/test_operational_integration_query_v168.py — Integration Query Service tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_query_v168 import (
    IntegrationQueryService, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.integration_store_v168 import IntegrationStore
from paper_trading.operational_integration.models_v168 import IntegrationRun
from paper_trading.operational_integration.enums_v168 import (
    IntegrationMode, IntegrationStatus,
)


def _make_run(run_id="R001", session_id="S001"):
    return IntegrationRun(
        run_id=run_id,
        session_id=session_id,
        mode=IntegrationMode.RESEARCH_ONLY,
        status=IntegrationStatus.COMPLETE,
    )


class TestQuerySafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestIntegrationQueryServiceCore:
    def setup_method(self):
        self.store = IntegrationStore()
        self.service = IntegrationQueryService(self.store)

    def test_get_integration_run_existing(self):
        run = _make_run("R_QUERY_001")
        self.store.save_run(run)
        result = self.service.get_integration_run("R_QUERY_001")
        assert result is not None
        assert result["run_id"] == "R_QUERY_001"

    def test_get_integration_run_missing_returns_none(self):
        result = self.service.get_integration_run("NONEXISTENT_RUN")
        assert result is None

    def test_get_integration_run_paper_only(self):
        run = _make_run("R_QUERY_002")
        self.store.save_run(run)
        result = self.service.get_integration_run("R_QUERY_002")
        assert result["paper_only"] is True

    def test_get_integration_run_has_session_id(self):
        run = _make_run("R_QUERY_003", "SESS_XYZ")
        self.store.save_run(run)
        result = self.service.get_integration_run("R_QUERY_003")
        assert result["session_id"] == "SESS_XYZ"

    def test_get_integration_run_has_status(self):
        run = _make_run("R_QUERY_004")
        self.store.save_run(run)
        result = self.service.get_integration_run("R_QUERY_004")
        assert result["status"] == "COMPLETE"

    def test_get_component_status_returns_dict(self):
        run = _make_run("R_COMP_001")
        run.components = ["market_data_session"]
        self.store.save_run(run)
        result = self.service.get_component_status("R_COMP_001", "market_data_session")
        assert isinstance(result, dict)
        assert result["paper_only"] is True

    def test_get_component_status_missing_run(self):
        result = self.service.get_component_status("MISSING_RUN", "comp_a")
        assert "error" in result

    def test_get_pipeline_status_returns_dict(self):
        run = _make_run("R_PIPE_001")
        self.store.save_run(run)
        result = self.service.get_pipeline_status("R_PIPE_001")
        assert isinstance(result, dict)
        assert result["paper_only"] is True

    def test_get_pipeline_status_missing_run(self):
        result = self.service.get_pipeline_status("MISSING_PIPE")
        assert "error" in result

    def test_get_contract_status_returns_dict(self):
        result = self.service.get_contract_status("R001")
        assert isinstance(result, dict)
        assert result["paper_only"] is True

    def test_get_data_flow_returns_dict(self):
        result = self.service.get_data_flow("R001")
        assert isinstance(result, dict)
        assert result["paper_only"] is True

    def test_get_lineage_chain_returns_dict(self):
        result = self.service.get_lineage_chain("LIN_001")
        assert isinstance(result, dict)
        assert result["paper_only"] is True

    def test_get_timestamp_issues_returns_dict(self):
        result = self.service.get_timestamp_issues("R001")
        assert isinstance(result, dict)
        assert result["paper_only"] is True

    def test_get_identity_issues_returns_dict(self):
        result = self.service.get_identity_issues("R001")
        assert isinstance(result, dict)
        assert result["paper_only"] is True

    def test_service_default_store(self):
        svc = IntegrationQueryService()
        assert svc._store is not None

    def test_get_integration_run_mode(self):
        run = _make_run("R_MODE_001")
        self.store.save_run(run)
        result = self.service.get_integration_run("R_MODE_001")
        assert result["mode"] == "RESEARCH_ONLY"

    def test_get_component_status_in_run(self):
        run = _make_run("R_COMP_002")
        run.components = ["paper_attribution"]
        self.store.save_run(run)
        result = self.service.get_component_status("R_COMP_002", "paper_attribution")
        assert result["in_run"] is True

    def test_get_component_status_not_in_run(self):
        run = _make_run("R_COMP_003")
        run.components = []
        self.store.save_run(run)
        result = self.service.get_component_status("R_COMP_003", "unknown_component")
        assert result["in_run"] is False

    def test_get_pipeline_status_stage_count(self):
        run = _make_run("R_PIPE_002")
        run.stages = [{"stage": "CONTEXT_LOAD"}]
        self.store.save_run(run)
        result = self.service.get_pipeline_status("R_PIPE_002")
        assert result["stage_count"] == 1

    def test_query_service_read_only(self):
        # Verify the service doesn't expose write operations directly
        assert not hasattr(self.service, 'save_run')
        assert not hasattr(self.service, 'delete_run')
