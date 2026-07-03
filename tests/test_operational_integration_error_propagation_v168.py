"""
tests/test_operational_integration_error_propagation_v168.py — Error Propagator tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.error_propagation_v168 import (
    ErrorPropagator, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import IntegrationFailure
from paper_trading.operational_integration.enums_v168 import (
    IntegrationStage, FailureDomain, FailureSeverity,
)


class TestErrorPropagationSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestErrorPropagatorCore:
    def setup_method(self):
        self.propagator = ErrorPropagator()

    def test_create_error_returns_failure(self):
        failure = self.propagator.create_error(
            component="market_data",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="Contract validation failed",
        )
        assert isinstance(failure, IntegrationFailure)

    def test_create_error_paper_only(self):
        failure = self.propagator.create_error(
            component="session",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="test",
        )
        assert failure.paper_only is True

    def test_create_error_component_stored(self):
        failure = self.propagator.create_error(
            component="my_component",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="test",
        )
        assert failure.component_id == "my_component"

    def test_create_error_message_stored(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="specific message here",
        )
        assert "specific message here" in failure.message

    def test_create_error_high_severity(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="test",
        )
        assert failure.severity == FailureSeverity.HIGH

    def test_create_error_critical_severity(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="CONTRACT_VALIDATE",
            category="SAFETY",
            severity="CRITICAL",
            message="safety violation",
        )
        assert failure.severity == FailureSeverity.CRITICAL

    def test_create_error_contract_domain(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="test",
        )
        assert failure.domain == FailureDomain.CONTRACT

    def test_create_error_data_flow_domain(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="STAGE_VALIDATE",
            category="DATA_FLOW",
            severity="MEDIUM",
            message="data flow issue",
        )
        assert failure.domain == FailureDomain.DATA_FLOW

    def test_create_error_invalid_stage_fallback(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="INVALID_STAGE",
            category="CONTRACT",
            severity="HIGH",
            message="test",
        )
        assert failure.stage == IntegrationStage.STAGE_VALIDATE

    def test_create_error_invalid_domain_fallback(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="CONTRACT_VALIDATE",
            category="INVALID_DOMAIN",
            severity="HIGH",
            message="test",
        )
        assert failure.domain == FailureDomain.UNKNOWN

    def test_propagate_creates_new_failure(self):
        original = self.propagator.create_error(
            component="upstream",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="original error",
        )
        propagated = self.propagator.propagate(original, "downstream")
        assert propagated.component_id == "downstream"
        assert propagated.failure_id != original.failure_id

    def test_propagate_preserves_domain(self):
        original = self.propagator.create_error(
            component="upstream",
            stage="CONTRACT_VALIDATE",
            category="LINEAGE",
            severity="MEDIUM",
            message="lineage error",
        )
        propagated = self.propagator.propagate(original, "downstream")
        assert propagated.domain == FailureDomain.LINEAGE

    def test_wrap_exception_returns_failure(self):
        exc = ValueError("test exception")
        failure = self.propagator.wrap_exception(exc, "comp1", "CONTRACT_VALIDATE")
        assert isinstance(failure, IntegrationFailure)
        assert "ValueError" in failure.message

    def test_wrap_exception_paper_only(self):
        exc = RuntimeError("runtime error")
        failure = self.propagator.wrap_exception(exc, "comp1", "CONTRACT_VALIDATE")
        assert failure.paper_only is True

    def test_summarize_returns_dict(self):
        failures = [
            self.propagator.create_error("c1", "CONTRACT_VALIDATE", "CONTRACT", "HIGH", "msg1"),
            self.propagator.create_error("c2", "STAGE_VALIDATE", "DATA_FLOW", "MEDIUM", "msg2"),
        ]
        summary = self.propagator.summarize(failures)
        assert isinstance(summary, dict)

    def test_summarize_paper_only(self):
        summary = self.propagator.summarize([])
        assert summary.get("paper_only") is True

    def test_create_error_no_real_orders(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="test",
        )
        assert failure.no_real_orders is True

    def test_create_error_has_failure_id(self):
        failure = self.propagator.create_error(
            component="comp_test",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="test error",
        )
        assert failure.failure_id is not None
        assert len(failure.failure_id) > 0

    def test_create_error_recoverable_flag(self):
        failure = self.propagator.create_error(
            component="c1",
            stage="CONTRACT_VALIDATE",
            category="CONTRACT",
            severity="HIGH",
            message="test",
            recoverable=True,
        )
        assert failure.recoverable is True
