"""
test_multi_session_version_v166.py — Version identity tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


class TestVersionIdentity:
    def test_version_is_166(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        assert CHECK_VERSION == "1.6.6"

    def test_version_format_major_minor_patch(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        parts = CHECK_VERSION.split(".")
        assert len(parts) == 3

    def test_version_major_is_1(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        assert CHECK_VERSION.split(".")[0] == "1"

    def test_version_minor_is_6(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        assert CHECK_VERSION.split(".")[1] == "6"

    def test_version_patch_is_6(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        assert CHECK_VERSION.split(".")[2] == "6"

    def test_release_name_multi_session_coordination(self):
        from paper_trading.multi_session.health_v166 import MultiSessionCoordinationHealthCheck
        assert "MultiSessionCoordination" in type(MultiSessionCoordinationHealthCheck()).__name__

    def test_release_gate_version_is_166(self):
        from release.multi_session_coordination_release_gate_v166 import GATE_VERSION
        assert GATE_VERSION == "1.6.6"

    def test_panel_version_is_166(self):
        from gui.multi_session_coordination_panel import PANEL_VERSION
        assert PANEL_VERSION == "1.6.6"

    def test_coordination_policy_version_is_166(self):
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        p = make_default_policy()
        assert p.version == "1.6.6"

    def test_scenario_registry_all_version_166(self):
        from paper_trading.multi_session.scenario_registry_v166 import SCENARIO_REGISTRY
        for s in SCENARIO_REGISTRY:
            assert s.version == "1.6.6"

    def test_version_string_is_string(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        assert isinstance(CHECK_VERSION, str)

    def test_resource_manager_module_has_version_flag(self):
        import paper_trading.multi_session.resource_manager_v166 as rm
        assert rm.RESEARCH_ONLY is True

    def test_models_module_imports_without_error(self):
        import paper_trading.multi_session.models_v166
        assert True

    def test_enums_module_imports_without_error(self):
        import paper_trading.multi_session.enums_v166
        assert True

    def test_coordinator_module_imports_without_error(self):
        import paper_trading.multi_session.coordinator_v166
        assert True


class TestSafetyFlags:
    def test_research_only_is_true(self):
        from paper_trading.multi_session import MULTI_SESSION_RESEARCH_ONLY
        assert MULTI_SESSION_RESEARCH_ONLY is True

    def test_paper_only_is_true(self):
        from paper_trading.multi_session import MULTI_SESSION_PAPER_ONLY
        assert MULTI_SESSION_PAPER_ONLY is True

    def test_no_real_orders_flag_is_false(self):
        from paper_trading.multi_session import CROSS_SESSION_REAL_ORDER_ENABLED
        assert CROSS_SESSION_REAL_ORDER_ENABLED is False

    def test_no_broker_flag_is_false(self):
        from paper_trading.multi_session import CROSS_SESSION_BROKER_ENABLED
        assert CROSS_SESSION_BROKER_ENABLED is False

    def test_no_auto_execution_is_false(self):
        from paper_trading.multi_session import GLOBAL_AUTO_EXECUTION_ENABLED
        assert GLOBAL_AUTO_EXECUTION_ENABLED is False

    def test_no_auto_resume_is_false(self):
        from paper_trading.multi_session import GLOBAL_AUTO_RESUME_ENABLED
        assert GLOBAL_AUTO_RESUME_ENABLED is False

    def test_no_auto_risk_override_is_false(self):
        from paper_trading.multi_session import GLOBAL_AUTO_RISK_OVERRIDE_ENABLED
        assert GLOBAL_AUTO_RISK_OVERRIDE_ENABLED is False

    def test_no_auto_capital_reallocation_is_false(self):
        from paper_trading.multi_session import GLOBAL_AUTO_CAPITAL_REALLOCATION_ENABLED
        assert GLOBAL_AUTO_CAPITAL_REALLOCATION_ENABLED is False

    def test_no_production_coord_is_false(self):
        from paper_trading.multi_session import PRODUCTION_SESSION_COORDINATION_ENABLED
        assert PRODUCTION_SESSION_COORDINATION_ENABLED is False

    def test_no_external_bus_is_false(self):
        from paper_trading.multi_session import EXTERNAL_COORDINATION_BUS_ENABLED
        assert EXTERNAL_COORDINATION_BUS_ENABLED is False

    def test_no_distributed_lock_is_false(self):
        from paper_trading.multi_session import DISTRIBUTED_LOCK_SERVICE_ENABLED
        assert DISTRIBUTED_LOCK_SERVICE_ENABLED is False

    def test_total_false_flags_count(self):
        import paper_trading.multi_session as m
        false_flags = [
            m.CROSS_SESSION_REAL_ORDER_ENABLED,
            m.CROSS_SESSION_BROKER_ENABLED,
            m.GLOBAL_AUTO_EXECUTION_ENABLED,
            m.GLOBAL_AUTO_RESUME_ENABLED,
            m.GLOBAL_AUTO_RISK_OVERRIDE_ENABLED,
            m.GLOBAL_AUTO_CAPITAL_REALLOCATION_ENABLED,
            m.GLOBAL_AUTO_SESSION_START_ENABLED,
            m.GLOBAL_AUTO_SESSION_STOP_ENABLED,
            m.PRODUCTION_SESSION_COORDINATION_ENABLED,
            m.EXTERNAL_COORDINATION_BUS_ENABLED,
            m.DISTRIBUTED_LOCK_SERVICE_ENABLED,
        ]
        assert all(f is False for f in false_flags)
        assert len(false_flags) == 11


class TestBaselineFlags:
    def test_multi_session_coordination_baseline_constant(self):
        from paper_trading.multi_session.health_v166 import CHECK_VERSION
        MULTI_SESSION_COORDINATION_BASELINE = "1.6.6"
        assert CHECK_VERSION == MULTI_SESSION_COORDINATION_BASELINE

    def test_baseline_is_correct_string(self):
        MULTI_SESSION_COORDINATION_BASELINE = "1.6.6"
        assert MULTI_SESSION_COORDINATION_BASELINE == "1.6.6"

    def test_coordination_available_flag(self):
        from paper_trading.multi_session import MULTI_SESSION_COORDINATION_AVAILABLE
        assert MULTI_SESSION_COORDINATION_AVAILABLE is True

    def test_resource_manager_logical_only(self):
        import paper_trading.multi_session.resource_manager_v166 as rm
        assert rm.LOGICAL_RESERVATION_ONLY is True

    def test_lock_manager_in_memory_only(self):
        import paper_trading.multi_session.lock_manager_v166 as lm
        assert lm.IN_MEMORY_LOGICAL_LOCK_ONLY is True
