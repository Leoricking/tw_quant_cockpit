"""
tests/test_operational_integration_contract_registry_v168.py — Contract Registry tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.contract_registry_v168 import (
    ContractRegistry, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)


class TestContractRegistrySafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestContractRegistryCore:
    def setup_method(self):
        self.registry = ContractRegistry()

    def test_list_names_returns_list(self):
        names = self.registry.list_names()
        assert isinstance(names, list)

    def test_list_names_not_empty(self):
        names = self.registry.list_names()
        assert len(names) > 0

    def test_list_names_sorted(self):
        names = self.registry.list_names()
        assert names == sorted(names)

    def test_get_market_data_to_session(self):
        contract = self.registry.get("MarketDataToSession")
        assert isinstance(contract, dict)
        assert "required_fields" in contract

    def test_get_session_to_strategy(self):
        contract = self.registry.get("SessionToStrategy")
        assert contract["paper_only"] is True

    def test_get_missing_contract_raises(self):
        with pytest.raises(KeyError):
            self.registry.get("NonExistentContract")

    def test_count_returns_int(self):
        count = self.registry.count()
        assert isinstance(count, int)
        assert count > 0

    def test_validate_all_returns_all_valid(self):
        result = self.registry.validate_all()
        assert result["paper_only"] is True
        assert isinstance(result["total"], int)

    def test_validate_all_has_details(self):
        result = self.registry.validate_all()
        assert "details" in result
        assert isinstance(result["details"], dict)

    def test_check_compatibility_returns_dict(self):
        result = self.registry.check_compatibility("market_data_session", "live_paper_trading")
        assert "compatible" in result
        assert result["paper_only"] is True

    def test_validate_payload_valid(self):
        payload = {
            "symbol": "2330.TW",
            "timestamp": "2026-01-02T09:00:00Z",
            "open": 560.0,
            "high": 565.0,
            "low": 558.0,
            "close": 562.0,
            "volume": 1000,
            "source_lineage": "L001",
        }
        result = self.registry.validate_payload("MarketDataToSession", payload)
        assert result["valid"] is True
        assert result["paper_only"] is True

    def test_validate_payload_missing_required(self):
        result = self.registry.validate_payload("MarketDataToSession", {"open": 560.0})
        assert result["valid"] is False
        assert len(result["missing_required"]) > 0

    def test_validate_payload_forbidden_field(self):
        payload = {
            "symbol": "2330.TW", "timestamp": "2026-01-02T09:00:00Z",
            "open": 560.0, "high": 565.0, "low": 558.0, "close": 562.0,
            "volume": 1000, "source_lineage": "L001",
            "broker_session": "FORBIDDEN",
        }
        result = self.registry.validate_payload("MarketDataToSession", payload)
        assert result["valid"] is False
        assert len(result["forbidden_found"]) > 0

    def test_validate_payload_unknown_contract(self):
        result = self.registry.validate_payload("UnknownContract", {})
        assert result["valid"] is False

    def test_register_new_contract(self):
        reg = ContractRegistry()
        reg.register("TestContract", {
            "required_fields": ["a"],
            "optional_fields": [],
            "forbidden_fields": [],
            "paper_only": True,
        })
        assert "TestContract" in reg.list_names()

    def test_register_duplicate_raises(self):
        reg = ContractRegistry()
        reg.register("TestContract2", {
            "required_fields": [], "optional_fields": [],
            "forbidden_fields": [], "paper_only": True,
        })
        with pytest.raises(ValueError):
            reg.register("TestContract2", {"required_fields": [], "optional_fields": [],
                                           "forbidden_fields": [], "paper_only": True})

    def test_contract_has_forbidden_fields(self):
        contract = self.registry.get("MarketDataToSession")
        assert "forbidden_fields" in contract
        assert len(contract["forbidden_fields"]) > 0

    def test_contract_paper_only(self):
        for name in self.registry.list_names():
            contract = self.registry.get(name)
            assert contract.get("paper_only") is True, f"Contract {name} missing paper_only"

    def test_portfolio_to_execution_exists(self):
        contract = self.registry.get("PortfolioToExecution")
        assert "quantity" in contract["required_fields"]

    def test_execution_to_analytics_exists(self):
        contract = self.registry.get("ExecutionToAnalytics")
        assert "simulated" in contract["required_fields"]

    def test_analytics_to_attribution_exists(self):
        contract = self.registry.get("AnalyticsToAttribution")
        assert "pnl" in contract["required_fields"]
