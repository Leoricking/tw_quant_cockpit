"""
tests/test_operational_integration_component_registry_v168.py — Component Registry tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.component_registry_v168 import (
    ComponentRegistry, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)
from paper_trading.operational_integration.models_v168 import ComponentDescriptor


class TestComponentRegistrySafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestComponentRegistryCore:
    def setup_method(self):
        self.registry = ComponentRegistry()

    def test_list_components_returns_list(self):
        result = self.registry.list_components()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_list_components_sorted(self):
        result = self.registry.list_components()
        assert result == sorted(result)

    def test_get_component_market_data(self):
        comp = self.registry.get_component("market_data_session")
        assert comp is not None
        assert comp.component_id == "market_data_session"

    def test_get_component_paper_trading(self):
        comp = self.registry.get_component("live_paper_trading")
        assert comp is not None

    def test_get_component_unknown_returns_none(self):
        comp = self.registry.get_component("nonexistent_component_xyz")
        assert comp is None

    def test_component_paper_only(self):
        comp = self.registry.get_component("market_data_session")
        assert comp.paper_only is True

    def test_component_research_only(self):
        comp = self.registry.get_component("market_data_session")
        assert comp.research_only is True

    def test_validate_component_valid(self):
        result = self.registry.validate_component("market_data_session")
        assert result["valid"] is True
        assert result["paper_only"] is True

    def test_validate_component_unknown(self):
        result = self.registry.validate_component("unknown_comp")
        assert result["valid"] is False

    def test_validate_capabilities_all_valid(self):
        result = self.registry.validate_capabilities()
        assert result["all_valid"] is True
        assert result["paper_only"] is True

    def test_list_dependencies_market_data(self):
        deps = self.registry.list_dependencies("market_data_session")
        assert isinstance(deps, list)
        assert deps == []

    def test_list_dependencies_unknown(self):
        deps = self.registry.list_dependencies("nonexistent")
        assert deps == []

    def test_list_dependents_returns_list(self):
        dependents = self.registry.list_dependents("market_data_session")
        assert isinstance(dependents, list)

    def test_detect_cycles_none(self):
        cycles = self.registry.detect_cycles()
        assert isinstance(cycles, list)

    def test_detect_missing_dependencies(self):
        missing = self.registry.detect_missing_dependencies()
        assert isinstance(missing, dict)

    def test_component_health_summary(self):
        summary = self.registry.component_health_summary()
        assert "total_components" in summary
        assert summary["paper_only"] is True
        assert summary["research_only"] is True

    def test_component_health_total_positive(self):
        summary = self.registry.component_health_summary()
        assert summary["total_components"] > 0

    def test_register_new_component(self):
        reg = ComponentRegistry()
        d = ComponentDescriptor(
            component_id="test_comp_new",
            component_name="Test Component",
            component_version="1.0.0",
        )
        reg.register_component(d)
        assert reg.get_component("test_comp_new") is not None

    def test_register_duplicate_raises(self):
        reg = ComponentRegistry()
        d = ComponentDescriptor(
            component_id="market_data_session",
            component_name="Dup",
            component_version="1.0.0",
        )
        with pytest.raises(ValueError):
            reg.register_component(d)

    def test_validate_contracts_returns_dict(self):
        result = self.registry.validate_contracts("market_data_session")
        assert result["valid"] is True
        assert "contracts" in result

    def test_validate_version_match(self):
        comp = self.registry.get_component("market_data_session")
        assert self.registry.validate_version("market_data_session", comp.component_version) is True

    def test_validate_version_mismatch(self):
        assert self.registry.validate_version("market_data_session", "9.9.9") is False

    def test_paper_attribution_component_exists(self):
        comp = self.registry.get_component("paper_attribution")
        assert comp is not None
        assert "attribution_run" in comp.capabilities
