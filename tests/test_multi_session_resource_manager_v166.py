"""
test_multi_session_resource_manager_v166.py — Resource Manager tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest


def _rm():
    from paper_trading.multi_session.resource_manager_v166 import ResourceManager
    return ResourceManager()


class TestResourceManager:
    def test_instantiation(self):
        rm = _rm()
        assert rm is not None

    def test_logical_reservation_only_flag(self):
        import paper_trading.multi_session.resource_manager_v166 as m
        assert m.LOGICAL_RESERVATION_ONLY is True

    def test_research_only_flag(self):
        import paper_trading.multi_session.resource_manager_v166 as m
        assert m.RESEARCH_ONLY is True

    def test_no_real_os_resource_allocation_flag(self):
        import paper_trading.multi_session.resource_manager_v166 as m
        assert m.NO_REAL_OS_RESOURCE_ALLOCATION is True

    def test_request_returns_resource_reservation(self):
        from paper_trading.multi_session.resource_manager_v166 import ResourceManager
        from paper_trading.multi_session.models_v166 import ResourceReservation
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = ResourceManager()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_s1", 1.0)
        assert isinstance(r, ResourceReservation)

    def test_request_granted_status(self):
        from paper_trading.multi_session.enums_v166 import ResourceType, ReservationStatus
        rm = _rm()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_k", 1.0)
        assert r.status == ReservationStatus.GRANTED

    def test_request_has_reservation_id(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        r = rm.request("s1", ResourceType.STRATEGY_SLOT, "strat_k", 1.0)
        assert r.reservation_id

    def test_release_by_reservation_id(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_rel", 1.0)
        result = rm.release(r.reservation_id)
        assert result is True

    def test_release_idempotent(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_idem", 1.0)
        rm.release(r.reservation_id)
        result = rm.release(r.reservation_id)
        assert result is True

    def test_request_denied_when_over_capacity(self):
        from paper_trading.multi_session.enums_v166 import ResourceType, ReservationStatus
        rm = _rm()
        # Request more than capacity
        r = rm.request("s1", ResourceType.CAPITAL_BUDGET, "cap_k", 2_000_000.0)
        assert r.status in (ReservationStatus.DENIED, ReservationStatus.PARTIAL)

    def test_multiple_sessions_same_resource_type(self):
        from paper_trading.multi_session.enums_v166 import ResourceType, ReservationStatus
        rm = _rm()
        r1 = rm.request("s1", ResourceType.CPU_SLOT, "cpu_s1", 1.0)
        r2 = rm.request("s2", ResourceType.CPU_SLOT, "cpu_s2", 1.0)
        assert r1.status == ReservationStatus.GRANTED
        assert r2.status == ReservationStatus.GRANTED

    def test_available_decreases_after_request(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        before = rm.available(ResourceType.CPU_SLOT)
        rm.request("s1", ResourceType.CPU_SLOT, "cpu_avail", 2.0)
        after = rm.available(ResourceType.CPU_SLOT)
        assert after < before

    def test_available_increases_after_release(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_avail2", 2.0)
        before = rm.available(ResourceType.CPU_SLOT)
        rm.release(r.reservation_id)
        after = rm.available(ResourceType.CPU_SLOT)
        assert after > before

    def test_list_for_session_returns_reservations(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        rm.request("s_list", ResourceType.CPU_SLOT, "cpu_l1", 1.0)
        rm.request("s_list", ResourceType.STRATEGY_SLOT, "strat_l1", 1.0)
        result = rm.list_for_session("s_list")
        assert len(result) == 2

    def test_get_reservation_by_id(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        r = rm.request("s1", ResourceType.MEMORY_BUDGET, "mem_k", 100.0)
        fetched = rm.get_reservation(r.reservation_id)
        assert fetched is not None
        assert fetched.reservation_id == r.reservation_id

    def test_request_stores_session_id(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        r = rm.request("session_xyz", ResourceType.REPORT_SLOT, "rep_k", 1.0)
        assert r.session_id == "session_xyz"

    def test_request_stores_resource_type(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        r = rm.request("s1", ResourceType.MARKET_DATA_CHANNEL, "mdc_k", 1.0)
        assert r.resource_type == ResourceType.MARKET_DATA_CHANNEL

    def test_rollback_session_releases_all(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        rm.request("s_roll", ResourceType.CPU_SLOT, "cpu_roll", 1.0)
        rm.request("s_roll", ResourceType.STRATEGY_SLOT, "strat_roll", 1.0)
        count = rm.rollback_session("s_roll")
        assert count == 2
        assert rm.list_for_session("s_roll") == []

    def test_request_different_resource_types(self):
        from paper_trading.multi_session.enums_v166 import ResourceType, ReservationStatus
        rm = _rm()
        r1 = rm.request("s1", ResourceType.CPU_SLOT, "cpu", 1.0)
        r2 = rm.request("s1", ResourceType.MEMORY_BUDGET, "mem", 100.0)
        r3 = rm.request("s1", ResourceType.RISK_BUDGET, "risk", 5.0)
        assert r1.status == ReservationStatus.GRANTED
        assert r2.status == ReservationStatus.GRANTED
        assert r3.status == ReservationStatus.GRANTED

    def test_request_has_expires_at(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        rm = _rm()
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_exp", 1.0)
        assert r.expires_at is not None

    def test_release_nonexistent_idempotent(self):
        rm = _rm()
        result = rm.release("nonexistent_reservation_id")
        assert result is True

    def test_partial_grant_when_insufficient_capacity(self):
        from paper_trading.multi_session.enums_v166 import ResourceType, ReservationStatus
        rm = _rm()
        # Request near-full capacity first
        rm.request("s1", ResourceType.RISK_BUDGET, "risk1", 90.0)
        # Request remaining that pushes over limit
        r2 = rm.request("s2", ResourceType.RISK_BUDGET, "risk2", 50.0)
        assert r2.status in (ReservationStatus.PARTIAL, ReservationStatus.DENIED)

    def test_default_capacities_dict_exists(self):
        from paper_trading.multi_session.resource_manager_v166 import ResourceManager
        assert hasattr(ResourceManager, "DEFAULT_CAPACITIES")
        assert len(ResourceManager.DEFAULT_CAPACITIES) > 0

    def test_allocate_for_sessions_returns_dict(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        from paper_trading.multi_session.coordination_policy_v166 import make_default_policy
        rm = _rm()
        policy = make_default_policy()
        result = rm.allocate_for_sessions(["s1", "s2"], {}, policy)
        assert isinstance(result, dict)
        assert "s1" in result
        assert "s2" in result

    def test_expire_stale_returns_expired_ids(self):
        from paper_trading.multi_session.enums_v166 import ResourceType
        from datetime import datetime, timezone, timedelta
        rm = _rm()
        past = datetime.now(timezone.utc) - timedelta(seconds=1)
        r = rm.request("s1", ResourceType.CPU_SLOT, "cpu_exp2", 1.0, ttl_seconds=0.001, now=past)
        now = datetime.now(timezone.utc)
        expired = rm.expire_stale(now=now)
        assert isinstance(expired, list)
