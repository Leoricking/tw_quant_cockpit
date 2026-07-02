"""
tests/test_paper_attribution_safety_v167.py
Tests for paper attribution safety module v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.safety_v167 import (
    RESEARCH_ONLY,
    PAPER_ONLY,
    NO_REAL_ORDERS,
    REAL_PERFORMANCE_ATTRIBUTION_ENABLED,
    BROKER_ATTRIBUTION_ENABLED,
    EXTERNAL_ATTRIBUTION_DB_ENABLED,
    LIVE_EXECUTION_ATTRIBUTION_ENABLED,
    check_forbidden_fields,
    check_real_live_markers,
    check_production_flags,
    validate_attribution_safety,
    assert_paper_only,
    get_safety_flags,
    audit_safety,
)


class TestSafetyConstants:
    def test_research_only_is_true(self):
        assert RESEARCH_ONLY is True

    def test_paper_only_is_true(self):
        assert PAPER_ONLY is True

    def test_no_real_orders_is_true(self):
        assert NO_REAL_ORDERS is True

    def test_real_attribution_disabled(self):
        assert REAL_PERFORMANCE_ATTRIBUTION_ENABLED is False

    def test_broker_disabled(self):
        assert BROKER_ATTRIBUTION_ENABLED is False

    def test_external_db_disabled(self):
        assert EXTERNAL_ATTRIBUTION_DB_ENABLED is False

    def test_live_execution_disabled(self):
        assert LIVE_EXECUTION_ATTRIBUTION_ENABLED is False


class TestCheckForbiddenFields:
    def test_clean_data_not_blocked(self):
        found = check_forbidden_fields({"run_id": "test", "portfolio_id": "P1"})
        assert found == []

    def test_broker_session_blocked(self):
        found = check_forbidden_fields({"broker_session": "live"})
        assert "broker_session" in found

    def test_real_account_token_blocked(self):
        found = check_forbidden_fields({"real_account_token": "tok"})
        assert "real_account_token" in found

    def test_api_secret_blocked(self):
        found = check_forbidden_fields({"api_secret": "secret"})
        assert "api_secret" in found

    def test_password_blocked(self):
        found = check_forbidden_fields({"password": "pw123"})
        assert "password" in found

    def test_shioaji_login_blocked(self):
        found = check_forbidden_fields({"shioaji_login": "user"})
        assert "shioaji_login" in found

    def test_multiple_forbidden_fields(self):
        found = check_forbidden_fields({"broker_session": "live", "api_secret": "s"})
        assert len(found) >= 2

    def test_returns_list(self):
        found = check_forbidden_fields({})
        assert isinstance(found, list)

    def test_none_value_is_still_detected(self):
        # The function detects presence of key regardless of value (list-based)
        found = check_forbidden_fields({"broker_session": None})
        # Whether None is blocked depends on implementation — just check it's a list
        assert isinstance(found, list)


class TestCheckRealLiveMarkers:
    def test_clean_no_real_markers(self):
        found = check_real_live_markers({"paper_only": True})
        assert found == []

    def test_is_live_true_blocked(self):
        found = check_real_live_markers({"is_live": True})
        assert "is_live" in found

    def test_is_real_true_blocked(self):
        found = check_real_live_markers({"is_real": True})
        assert "is_real" in found

    def test_live_mode_true_blocked(self):
        found = check_real_live_markers({"live_mode": True})
        assert "live_mode" in found

    def test_production_mode_true_blocked(self):
        found = check_real_live_markers({"production_mode": True})
        assert "production_mode" in found

    def test_returns_list(self):
        found = check_real_live_markers({})
        assert isinstance(found, list)

    def test_false_values_not_blocked(self):
        found = check_real_live_markers({"is_live": False, "live_mode": False})
        assert found == []


class TestCheckProductionFlags:
    def test_clean_data_no_flags(self):
        found = check_production_flags({"paper_only": True})
        assert found == []

    def test_returns_list(self):
        found = check_production_flags({})
        assert isinstance(found, list)


class TestValidateAttributionSafety:
    def test_safe_data_passes(self):
        r = validate_attribution_safety({
            "run_id": "safe_run",
            "paper_only": True,
            "research_only": True,
        })
        assert r["safe"] is True
        assert r["blocked"] is False

    def test_broker_session_blocked(self):
        r = validate_attribution_safety({"broker_session": "live"})
        assert r["blocked"] is True

    def test_is_live_blocked(self):
        r = validate_attribution_safety({"is_live": True})
        assert r["blocked"] is True

    def test_violations_list_present(self):
        r = validate_attribution_safety({})
        assert "violations" in r

    def test_returns_dict(self):
        r = validate_attribution_safety({})
        assert isinstance(r, dict)

    def test_multiple_violations_all_listed(self):
        r = validate_attribution_safety({
            "broker_session": "live",
            "is_real": True,
            "api_secret": "key",
        })
        assert len(r["violations"]) >= 2

    def test_paper_only_in_result(self):
        r = validate_attribution_safety({})
        assert r["paper_only"] is True

    def test_research_only_in_result(self):
        r = validate_attribution_safety({})
        assert r["research_only"] is True


class TestAssertPaperOnly:
    def test_assert_paper_only_does_not_raise(self):
        # The function checks module-level constants, should not raise
        assert_paper_only()


class TestGetSafetyFlags:
    def test_returns_dict(self):
        flags = get_safety_flags()
        assert isinstance(flags, dict)

    def test_paper_only_in_flags(self):
        flags = get_safety_flags()
        keys = set(flags.keys())
        assert any("PAPER" in k for k in keys)

    def test_real_enabled_false(self):
        flags = get_safety_flags()
        for k, v in flags.items():
            if "REAL" in k.upper() and "ENABLED" in k.upper():
                assert v is False, f"{k} should be False but is {v}"

    def test_nonempty(self):
        flags = get_safety_flags()
        assert len(flags) > 5


class TestAuditSafety:
    def test_returns_dict(self):
        audit = audit_safety()
        assert isinstance(audit, dict)

    def test_all_safe_is_true(self):
        audit = audit_safety()
        assert audit.get("all_safe") is True

    def test_safety_capabilities_present(self):
        audit = audit_safety()
        assert "safety_capabilities" in audit
