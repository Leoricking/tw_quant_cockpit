"""
tests/test_operational_integration_integration_contract_v168.py — Integration Contract tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_contract_v168 import (
    INTEGRATION_CONTRACTS, validate_contract_payload, check_schema_compatibility,
    PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)


class TestContractSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestIntegrationContractCore:
    def test_contracts_dict_not_empty(self):
        assert len(INTEGRATION_CONTRACTS) > 0

    def test_market_data_to_session_exists(self):
        assert "MarketDataToSession" in INTEGRATION_CONTRACTS

    def test_session_to_strategy_exists(self):
        assert "SessionToStrategy" in INTEGRATION_CONTRACTS

    def test_strategy_to_portfolio_exists(self):
        assert "StrategyToPortfolio" in INTEGRATION_CONTRACTS

    def test_portfolio_to_execution_exists(self):
        assert "PortfolioToExecution" in INTEGRATION_CONTRACTS

    def test_execution_to_analytics_exists(self):
        assert "ExecutionToAnalytics" in INTEGRATION_CONTRACTS

    def test_analytics_to_attribution_exists(self):
        assert "AnalyticsToAttribution" in INTEGRATION_CONTRACTS

    def test_all_contracts_have_paper_only(self):
        for name, contract in INTEGRATION_CONTRACTS.items():
            assert contract.get("paper_only") is True, f"{name} missing paper_only"

    def test_all_contracts_have_required_fields(self):
        for name, contract in INTEGRATION_CONTRACTS.items():
            assert "required_fields" in contract, f"{name} missing required_fields"
            assert isinstance(contract["required_fields"], list)

    def test_all_contracts_have_forbidden_fields(self):
        for name, contract in INTEGRATION_CONTRACTS.items():
            assert "forbidden_fields" in contract, f"{name} missing forbidden_fields"
            assert len(contract["forbidden_fields"]) > 0

    def test_all_contracts_deterministic(self):
        for name, contract in INTEGRATION_CONTRACTS.items():
            assert contract.get("deterministic") is True, f"{name} not deterministic"

    def test_market_data_required_fields(self):
        contract = INTEGRATION_CONTRACTS["MarketDataToSession"]
        assert "symbol" in contract["required_fields"]
        assert "timestamp" in contract["required_fields"]

    def test_execution_to_analytics_simulated(self):
        contract = INTEGRATION_CONTRACTS["ExecutionToAnalytics"]
        assert "simulated" in contract["required_fields"]

    def test_validate_contract_payload_valid(self):
        payload = {
            "symbol": "2330.TW",
            "timestamp": "2026-01-02T09:00:00Z",
            "open": 560.0, "high": 565.0, "low": 558.0, "close": 562.0,
            "volume": 1000, "source_lineage": "L001",
        }
        result = validate_contract_payload("MarketDataToSession", payload)
        assert result["valid"] is True

    def test_validate_contract_payload_missing_required(self):
        result = validate_contract_payload("MarketDataToSession", {"open": 560.0})
        assert result["valid"] is False
        assert len(result["missing_required"]) > 0

    def test_validate_contract_payload_forbidden_field(self):
        payload = {
            "symbol": "2330.TW", "timestamp": "2026-01-02T09:00:00Z",
            "open": 560.0, "high": 565.0, "low": 558.0, "close": 562.0,
            "volume": 1000, "source_lineage": "L001",
            "broker_session": "BLOCKED",
        }
        result = validate_contract_payload("MarketDataToSession", payload)
        assert result["valid"] is False
        assert len(result["forbidden_found"]) > 0

    def test_check_schema_compatibility_valid_contract(self):
        payload_schema = {"symbol": "str", "timestamp": "str", "open": "float",
                          "high": "float", "low": "float", "close": "float",
                          "volume": "int", "source_lineage": "str"}
        result = check_schema_compatibility("MarketDataToSession", payload_schema)
        assert isinstance(result, dict)
        assert "compatible" in result

    def test_check_schema_compatibility_unknown_contract(self):
        result = check_schema_compatibility("UnknownContract", {})
        assert isinstance(result, dict)

    def test_validate_contract_payload_unknown_contract(self):
        result = validate_contract_payload("UnknownContract", {})
        assert result["valid"] is False

    def test_contracts_have_schema_version(self):
        for name, contract in INTEGRATION_CONTRACTS.items():
            assert "schema_version" in contract, f"{name} missing schema_version"

    def test_contracts_read_only(self):
        for name, contract in INTEGRATION_CONTRACTS.items():
            assert contract.get("read_only") is True, f"{name} not read_only"

    def test_attribution_to_coordination_exists(self):
        assert "AttributionToCoordination" in INTEGRATION_CONTRACTS

    def test_health_to_report_exists(self):
        assert "HealthToReport" in INTEGRATION_CONTRACTS
