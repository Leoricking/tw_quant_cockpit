"""
tests/test_operational_integration_safety_v168.py — Safety flag tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration import safety_v168 as S


class TestSafetyCoreFlags:
    def test_paper_only(self):
        assert S.PAPER_ONLY is True

    def test_research_only(self):
        assert S.RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert S.NO_REAL_ORDERS is True

    def test_operational_integration_available(self):
        assert S.OPERATIONAL_INTEGRATION_AVAILABLE is True

    def test_operational_integration_research_only(self):
        assert S.OPERATIONAL_INTEGRATION_RESEARCH_ONLY is True

    def test_operational_integration_paper_only(self):
        assert S.OPERATIONAL_INTEGRATION_PAPER_ONLY is True

    def test_operational_integration_read_only(self):
        assert S.OPERATIONAL_INTEGRATION_READ_ONLY is True

    def test_operational_integration_deterministic(self):
        assert S.OPERATIONAL_INTEGRATION_DETERMINISTIC is True


class TestSafetyBlockedFlags:
    def test_real_operational_disabled(self):
        assert S.REAL_OPERATIONAL_INTEGRATION_ENABLED is False

    def test_broker_integration_disabled(self):
        assert S.BROKER_INTEGRATION_ENABLED is False

    def test_real_account_disabled(self):
        assert S.REAL_ACCOUNT_INTEGRATION_ENABLED is False

    def test_real_order_disabled(self):
        assert S.REAL_ORDER_INTEGRATION_ENABLED is False

    def test_production_ledger_disabled(self):
        assert S.PRODUCTION_LEDGER_INTEGRATION_ENABLED is False

    def test_live_execution_disabled(self):
        assert S.LIVE_EXECUTION_INTEGRATION_ENABLED is False

    def test_network_disabled(self):
        assert S.NETWORK_INTEGRATION_ENABLED is False

    def test_production_trading_blocked(self):
        assert S.PRODUCTION_TRADING_BLOCKED is True

    def test_broker_execution_disabled(self):
        assert S.BROKER_EXECUTION_ENABLED is False


class TestSafetyFunctions:
    def test_validate_clean_dict_is_safe(self):
        result = S.validate_integration_safety({"run_id": "R001", "session_id": "S001"})
        assert result["safe"] is True
        assert result["blocked"] is False
        assert result["violations"] == []

    def test_validate_forbidden_field_detected(self):
        result = S.validate_integration_safety({"broker_session": "bs123"})
        assert result["safe"] is False
        assert result["blocked"] is True
        assert len(result["violations"]) > 0

    def test_validate_always_paper_only(self):
        result = S.validate_integration_safety({})
        assert result["paper_only"] is True

    def test_assert_paper_only_passes(self):
        S.assert_integration_paper_only()

    def test_get_safety_flags_returns_dict(self):
        flags = S.get_safety_flags()
        assert isinstance(flags, dict)
        assert "OPERATIONAL_INTEGRATION_AVAILABLE" in flags

    def test_audit_safety_all_safe(self):
        result = S.audit_safety()
        assert result["all_safe"] is True
        assert result["safety_capabilities"] == 0

    def test_audit_safety_paper_only_key(self):
        result = S.audit_safety()
        assert result["paper_only"] is True
        assert result["research_only"] is True
        assert result["no_real_orders"] is True

    def test_check_forbidden_fields_clean(self):
        found = S.check_forbidden_fields({"symbol": "2330.TW", "price": 560.0})
        assert found == []

    def test_check_forbidden_fields_detected(self):
        found = S.check_forbidden_fields({"api_secret": "secret123"})
        assert "api_secret" in found

    def test_check_production_flags_clean(self):
        found = S.check_production_flags({"run_id": "R001"})
        assert found == []

    def test_forbidden_fields_set_not_empty(self):
        assert len(S._FORBIDDEN_INPUT_FIELDS) > 0

    def test_real_live_markers_set_not_empty(self):
        assert len(S._REAL_LIVE_MARKERS) > 0
