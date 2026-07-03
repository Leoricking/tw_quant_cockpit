"""
tests/test_operational_integration_failure_isolation_v168.py — Failure Isolator tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.failure_isolation_v168 import (
    FailureIsolator, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import IntegrationFailure
from paper_trading.operational_integration.enums_v168 import (
    IntegrationStage, FailureDomain, FailureSeverity,
)


def _make_failure(**kwargs):
    defaults = dict(
        failure_id="F001",
        component_id="market_data",
        stage=IntegrationStage.CONTRACT_VALIDATE,
        domain=FailureDomain.CONTRACT,
        severity=FailureSeverity.HIGH,
        message="Test failure",
    )
    defaults.update(kwargs)
    return IntegrationFailure(**defaults)


class TestIsolationSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestFailureIsolatorCore:
    def setup_method(self):
        self.isolator = FailureIsolator()

    def test_isolate_returns_dict(self):
        failure = _make_failure()
        result = self.isolator.isolate(failure)
        assert isinstance(result, dict)

    def test_isolate_paper_only(self):
        failure = _make_failure()
        result = self.isolator.isolate(failure)
        assert result["paper_only"] is True

    def test_isolate_isolated_flag(self):
        failure = _make_failure()
        result = self.isolator.isolate(failure)
        assert result["isolated"] is True

    def test_isolate_has_failure_id(self):
        failure = _make_failure(failure_id="F_TEST")
        result = self.isolator.isolate(failure)
        assert result["failure_id"] == "F_TEST"

    def test_isolate_has_domain(self):
        failure = _make_failure(domain=FailureDomain.DATA_FLOW)
        result = self.isolator.isolate(failure)
        assert result["domain"] == "DATA_FLOW"

    def test_isolate_critical_severity(self):
        failure = _make_failure(severity=FailureSeverity.CRITICAL)
        result = self.isolator.isolate(failure)
        assert result["critical"] is True

    def test_isolate_non_critical_severity(self):
        failure = _make_failure(
            domain=FailureDomain.UNKNOWN,
            severity=FailureSeverity.LOW,
        )
        result = self.isolator.isolate(failure)
        assert result["critical"] is False

    def test_isolate_safety_domain_is_critical(self):
        failure = _make_failure(
            domain=FailureDomain.SAFETY,
            severity=FailureSeverity.LOW,
        )
        result = self.isolator.isolate(failure)
        assert result["critical"] is True

    def test_isolate_contract_domain_is_critical(self):
        failure = _make_failure(
            domain=FailureDomain.CONTRACT,
            severity=FailureSeverity.LOW,
        )
        result = self.isolator.isolate(failure)
        assert result["critical"] is True

    def test_check_is_critical_critical_sev(self):
        failure = _make_failure(severity=FailureSeverity.CRITICAL)
        assert self.isolator.check_is_critical(failure) is True

    def test_check_is_critical_low_sev_unknown_domain(self):
        failure = _make_failure(
            severity=FailureSeverity.LOW,
            domain=FailureDomain.UNKNOWN,
        )
        assert self.isolator.check_is_critical(failure) is False

    def test_block_downstream_critical(self):
        failure = _make_failure(severity=FailureSeverity.CRITICAL)
        blocked = self.isolator.block_downstream(failure, ["comp_b", "comp_c"])
        assert len(blocked) == 2

    def test_block_downstream_non_critical(self):
        failure = _make_failure(
            severity=FailureSeverity.INFO,
            domain=FailureDomain.UNKNOWN,
        )
        blocked = self.isolator.block_downstream(failure, ["comp_b"])
        assert blocked == []

    def test_get_failure_domain(self):
        failure = _make_failure(domain=FailureDomain.LINEAGE)
        domain = self.isolator.get_failure_domain(failure)
        assert domain == FailureDomain.LINEAGE

    def test_summarize_returns_dict(self):
        failures = [_make_failure(), _make_failure(failure_id="F002")]
        summary = self.isolator.summarize(failures)
        assert isinstance(summary, dict)

    def test_summarize_paper_only(self):
        summary = self.isolator.summarize([])
        assert summary.get("paper_only") is True

    def test_summarize_total_count(self):
        failures = [_make_failure(failure_id=f"F{i:03d}") for i in range(5)]
        summary = self.isolator.summarize(failures)
        assert summary["total_failures"] == 5

    def test_summarize_critical_count(self):
        failures = [
            _make_failure(failure_id="F001", severity=FailureSeverity.CRITICAL),
            _make_failure(failure_id="F002", severity=FailureSeverity.LOW,
                          domain=FailureDomain.UNKNOWN),
        ]
        summary = self.isolator.summarize(failures)
        assert summary["critical_count"] == 1

    def test_summarize_domain_distribution(self):
        failures = [
            _make_failure(failure_id="F001", domain=FailureDomain.DATA_FLOW),
            _make_failure(failure_id="F002", domain=FailureDomain.LINEAGE),
        ]
        summary = self.isolator.summarize(failures)
        assert "domain_distribution" in summary

    def test_safety_related_is_critical(self):
        failure = _make_failure(
            severity=FailureSeverity.LOW,
            domain=FailureDomain.UNKNOWN,
            safety_related=True,
        )
        assert self.isolator.check_is_critical(failure) is True
