"""
tests/test_operational_integration_compatibility_v168.py — Compatibility Checker tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.compatibility_checker_v168 import (
    CompatibilityChecker, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import CompatibilityResult


class TestCompatibilitySafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestCompatibilityCheckerCore:
    def setup_method(self):
        self.checker = CompatibilityChecker()

    def test_check_exact_same_version(self):
        result = self.checker.check_exact("1.6.8", "1.6.8")
        assert result is True

    def test_check_exact_different_version(self):
        result = self.checker.check_exact("1.6.8", "1.6.7")
        assert result is False

    def test_check_backward_compatible_same_minor(self):
        result = self.checker.check_backward_compatible("1.6.8", "1.6.7")
        assert result is True

    def test_check_backward_compatible_different_minor(self):
        result = self.checker.check_backward_compatible("1.7.0", "1.6.8")
        assert result is False

    def test_check_schema_compatible_same_schema(self):
        s1 = {"field_a": "value_a", "field_b": "value_b"}
        s2 = {"field_a": "value_a"}
        result = self.checker.check_schema_compatible(s1, s2)
        assert result is True

    def test_check_schema_compatible_missing_required(self):
        s1 = {"field_a": "value_a"}
        s2 = {"field_a": "value_a", "field_b": "required_value"}
        result = self.checker.check_schema_compatible(s1, s2)
        assert result is False

    def test_check_full_compatibility(self):
        result = self.checker.check(
            from_component="market_data",
            to_component="session",
            from_version="1.6.8",
            to_version="1.6.8",
            from_schema={"symbol": "str", "price": "float"},
            to_schema={"symbol": "str"},
        )
        assert isinstance(result, CompatibilityResult)

    def test_check_exact_status(self):
        result = self.checker.check(
            from_component="A", to_component="B",
            from_version="1.6.8", to_version="1.6.8",
            from_schema={}, to_schema={},
        )
        assert result.status == "EXACT"

    def test_check_backward_compatible_status(self):
        result = self.checker.check(
            from_component="A", to_component="B",
            from_version="1.6.8", to_version="1.6.7",
            from_schema={}, to_schema={},
        )
        assert result.status == "BACKWARD_COMPATIBLE"

    def test_compatibility_result_has_check_id(self):
        result = self.checker.check(
            from_component="comp_a", to_component="comp_b",
            from_version="1.6.8", to_version="1.6.8",
            from_schema={}, to_schema={},
        )
        assert "comp_a" in result.check_id or "compat" in result.check_id

    def test_compatibility_result_paper_only(self):
        result = self.checker.check(
            from_component="A", to_component="B",
            from_version="1.6.8", to_version="1.6.8",
            from_schema={}, to_schema={},
        )
        assert result.paper_only is True

    def test_summarize_returns_dict(self):
        result = self.checker.check(
            from_component="A", to_component="B",
            from_version="1.6.8", to_version="1.6.8",
            from_schema={}, to_schema={},
        )
        summary = self.checker.summarize([result])
        assert isinstance(summary, dict)

    def test_summarize_paper_only(self):
        result = self.checker.check(
            from_component="A", to_component="B",
            from_version="1.6.8", to_version="1.6.8",
            from_schema={}, to_schema={},
        )
        summary = self.checker.summarize([result])
        assert summary.get("paper_only") is True

    def test_summarize_empty(self):
        summary = self.checker.summarize([])
        assert isinstance(summary, dict)

    def test_check_capability_returns_bool(self):
        result = self.checker.check_capability("market_data_session", "market_data_feed")
        assert isinstance(result, bool)

    def test_check_safety_compatible_clean(self):
        s1 = {"paper_only": True, "research_only": True}
        s2 = {"paper_only": True}
        result = self.checker.check_safety_compatible(s1, s2)
        assert isinstance(result, bool)

    def test_check_exact_empty_versions(self):
        result = self.checker.check_exact("", "")
        assert result is True

    def test_result_details_has_versions(self):
        result = self.checker.check(
            from_component="A", to_component="B",
            from_version="1.6.8", to_version="1.6.8",
            from_schema={}, to_schema={},
        )
        assert "from_version" in result.details

    def test_check_backward_same_patch(self):
        result = self.checker.check_backward_compatible("1.6.8", "1.6.8")
        assert result is True

    def test_check_forward_incompatible_status(self):
        result = self.checker.check(
            from_component="A", to_component="B",
            from_version="1.6.0", to_version="1.7.0",
            from_schema={}, to_schema={},
        )
        assert result.status in ("FORWARD_INCOMPATIBLE", "SCHEMA_INCOMPATIBLE")
