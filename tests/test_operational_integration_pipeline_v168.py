"""
tests/test_operational_integration_pipeline_v168.py — Pipeline tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_pipeline_v168 import (
    IntegrationPipeline, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import IntegrationContext
from paper_trading.operational_integration.enums_v168 import IntegrationStage, IntegrationMode


def _make_context(**kwargs):
    defaults = dict(
        run_id="R001",
        session_id="S001",
        component_id="market_data_session",
        period_start="2026-01-02",
        period_end="2026-01-03",
    )
    defaults.update(kwargs)
    return IntegrationContext(**defaults)


class TestPipelineSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestPipelineCore:
    def setup_method(self):
        self.pipeline = IntegrationPipeline()

    def test_run_returns_dict(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert isinstance(result, dict)

    def test_run_paper_only_flag(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["paper_only"] is True

    def test_run_research_only_flag(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["research_only"] is True

    def test_run_no_real_orders_flag(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["no_real_orders"] is True

    def test_run_has_run_id(self):
        ctx = _make_context(run_id="TestRun001")
        result = self.pipeline.run(ctx)
        assert result["run_id"] == "TestRun001"

    def test_run_has_status(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert "status" in result

    def test_run_has_stages(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert "stages" in result
        assert isinstance(result["stages"], list)

    def test_run_stages_not_empty(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["stage_count"] > 0

    def test_run_complete_status(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["status"] == "COMPLETE"

    def test_run_not_for_production(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert result["not_for_production"] is True

    def test_validate_context_valid(self):
        ctx = _make_context()
        result = self.pipeline.validate_context(ctx)
        assert result["valid"] is True
        assert result["errors"] == []

    def test_integration_stages_iterable(self):
        stages = list(IntegrationStage)
        assert len(stages) > 5

    def test_stages_include_context_load(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        stage_names = [s.get("stage") for s in result["stages"]]
        assert "CONTEXT_LOAD" in stage_names

    def test_stages_include_contract_validate(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        stage_names = [s.get("stage") for s in result["stages"]]
        assert "CONTRACT_VALIDATE" in stage_names

    def test_stages_include_complete(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        stage_names = [s.get("stage") for s in result["stages"]]
        assert "COMPLETE" in stage_names

    def test_run_has_session_id(self):
        ctx = _make_context(session_id="SESS_ABC")
        result = self.pipeline.run(ctx)
        assert result["session_id"] == "SESS_ABC"

    def test_run_has_mode(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        assert "mode" in result
        assert result["mode"] == "RESEARCH_ONLY"

    def test_run_period_in_result(self):
        ctx = _make_context(period_start="2026-01-02", period_end="2026-01-05")
        result = self.pipeline.run(ctx)
        assert result["period_start"] == "2026-01-02"
        assert result["period_end"] == "2026-01-05"

    def test_each_stage_has_paper_only(self):
        ctx = _make_context()
        result = self.pipeline.run(ctx)
        for stage in result["stages"]:
            assert stage.get("paper_only") is True, f"Stage {stage.get('stage')} missing paper_only"

    def test_validate_registry_returns_dict(self):
        result = self.pipeline.validate_registry()
        assert isinstance(result, dict)

    def test_multiple_runs_consistent(self):
        ctx = _make_context(run_id="R_MULTI")
        r1 = self.pipeline.run(ctx)
        r2 = self.pipeline.run(ctx)
        assert r1["status"] == r2["status"]
        assert len(r1["stages"]) == len(r2["stages"])
