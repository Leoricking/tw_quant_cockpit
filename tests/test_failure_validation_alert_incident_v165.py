"""
tests/test_failure_validation_alert_incident_v165.py — Alert & Incident tests v1.6.5
[!] Research Only. No Real Orders. No Real Failure Injection.
"""
import pytest

from paper_trading.failure_validation.enums_v165 import FailureSeverity
from paper_trading.failure_validation.alert_v165 import (
    AlertRegistry,
    SimulatedAlert,
    EXTERNAL_NOTIFICATION_ENABLED,
    PAPER_ONLY as ALERT_PAPER_ONLY,
    RESEARCH_ONLY as ALERT_RESEARCH_ONLY,
    generate_alert,
)
from paper_trading.failure_validation.incident_v165 import (
    IncidentRegistry,
    SimulatedIncident,
    PAPER_ONLY as INC_PAPER_ONLY,
    RESEARCH_ONLY as INC_RESEARCH_ONLY,
)


# ---------------------------------------------------------------------------
# Safety flags
# ---------------------------------------------------------------------------

class TestAlertIncidentSafetyFlags:
    def test_external_notification_disabled(self):
        assert EXTERNAL_NOTIFICATION_ENABLED is False

    def test_alert_paper_only_true(self):
        assert ALERT_PAPER_ONLY is True

    def test_alert_research_only_true(self):
        assert ALERT_RESEARCH_ONLY is True

    def test_incident_paper_only_true(self):
        assert INC_PAPER_ONLY is True

    def test_incident_research_only_true(self):
        assert INC_RESEARCH_ONLY is True


# ---------------------------------------------------------------------------
# SimulatedAlert
# ---------------------------------------------------------------------------

class TestSimulatedAlert:
    def test_alert_has_uuid_id(self):
        a = SimulatedAlert(title="Test Alert", severity=FailureSeverity.LOW)
        assert len(a.alert_id) == 36

    def test_alert_default_not_acknowledged(self):
        a = SimulatedAlert(title="Test Alert", severity=FailureSeverity.MEDIUM)
        assert a.acknowledged is False

    def test_acknowledge_sets_flag(self):
        a = SimulatedAlert(title="Test Alert", severity=FailureSeverity.HIGH)
        a.acknowledge()
        assert a.acknowledged is True

    def test_acknowledge_sets_acknowledged_at(self):
        a = SimulatedAlert(title="Test Alert", severity=FailureSeverity.LOW)
        a.acknowledge()
        assert a.acknowledged_at is not None

    def test_as_dict_has_required_keys(self):
        a = SimulatedAlert(title="Test", severity=FailureSeverity.CRITICAL, scenario_id="scen_1")
        d = a.as_dict()
        assert "alert_id" in d
        assert "title" in d
        assert "severity" in d
        assert "scenario_id" in d
        assert "acknowledged" in d

    def test_as_dict_severity_is_string_value(self):
        a = SimulatedAlert(title="X", severity=FailureSeverity.HIGH)
        assert a.as_dict()["severity"] == "HIGH"

    def test_two_alerts_different_ids(self):
        a1 = SimulatedAlert(title="A1", severity=FailureSeverity.LOW)
        a2 = SimulatedAlert(title="A2", severity=FailureSeverity.LOW)
        assert a1.alert_id != a2.alert_id


# ---------------------------------------------------------------------------
# generate_alert function
# ---------------------------------------------------------------------------

class TestGenerateAlert:
    def test_generate_alert_returns_simulated_alert(self):
        a = generate_alert("scen_1", "Market data stale", FailureSeverity.MEDIUM)
        assert isinstance(a, SimulatedAlert)

    def test_generate_alert_title_set(self):
        a = generate_alert("scen_1", "My Title", FailureSeverity.LOW)
        assert a.title == "My Title"

    def test_generate_alert_severity_set(self):
        a = generate_alert("scen_1", "X", FailureSeverity.CRITICAL)
        assert a.severity == FailureSeverity.CRITICAL

    def test_generate_alert_scenario_id_set(self):
        a = generate_alert("my_scenario", "X", FailureSeverity.HIGH)
        assert a.scenario_id == "my_scenario"


# ---------------------------------------------------------------------------
# AlertRegistry
# ---------------------------------------------------------------------------

class TestAlertRegistry:
    def test_empty_registry(self):
        reg = AlertRegistry()
        assert reg.count() == 0

    def test_add_alert(self):
        reg = AlertRegistry()
        a = SimulatedAlert(title="T", severity=FailureSeverity.LOW)
        reg.add(a)
        assert reg.count() == 1

    def test_all_returns_copy(self):
        reg = AlertRegistry()
        a = SimulatedAlert(title="T", severity=FailureSeverity.LOW)
        reg.add(a)
        all1 = reg.all()
        all2 = reg.all()
        assert all1 == all2
        all1.clear()
        assert reg.count() == 1  # internal list unaffected

    def test_unacknowledged_all_initially(self):
        reg = AlertRegistry()
        reg.add(SimulatedAlert(title="A", severity=FailureSeverity.LOW))
        reg.add(SimulatedAlert(title="B", severity=FailureSeverity.MEDIUM))
        assert len(reg.unacknowledged()) == 2

    def test_acknowledge_all_clears_unacknowledged(self):
        reg = AlertRegistry()
        reg.add(SimulatedAlert(title="A", severity=FailureSeverity.LOW))
        reg.add(SimulatedAlert(title="B", severity=FailureSeverity.MEDIUM))
        count = reg.acknowledge_all()
        assert count == 2
        assert len(reg.unacknowledged()) == 0

    def test_acknowledge_all_already_acknowledged_count_zero(self):
        reg = AlertRegistry()
        a = SimulatedAlert(title="X", severity=FailureSeverity.LOW)
        a.acknowledge()
        reg.add(a)
        count = reg.acknowledge_all()
        assert count == 0


# ---------------------------------------------------------------------------
# SimulatedIncident
# ---------------------------------------------------------------------------

class TestSimulatedIncident:
    def test_incident_has_uuid_id(self):
        inc = SimulatedIncident(title="Test", severity=FailureSeverity.MEDIUM)
        assert len(inc.incident_id) == 36

    def test_incident_default_status_open(self):
        inc = SimulatedIncident(title="Test", severity=FailureSeverity.LOW)
        assert inc.status == "OPEN"

    def test_resolve_sets_resolved_status(self):
        inc = SimulatedIncident(title="Test", severity=FailureSeverity.HIGH)
        inc.resolve("issue fixed")
        assert inc.status == "RESOLVED"

    def test_resolve_sets_resolved_at(self):
        inc = SimulatedIncident(title="Test", severity=FailureSeverity.HIGH)
        inc.resolve()
        assert inc.resolved_at is not None

    def test_resolve_adds_to_timeline(self):
        inc = SimulatedIncident(title="Test", severity=FailureSeverity.LOW)
        inc.resolve("fixed")
        assert len(inc.timeline) >= 1
        assert any(e["event"] == "RESOLVED" for e in inc.timeline)

    def test_add_event_appends_to_timeline(self):
        inc = SimulatedIncident(title="Test", severity=FailureSeverity.MEDIUM)
        inc.add_event("DETECTION_CONFIRMED", "failure detected")
        assert len(inc.timeline) == 1
        assert inc.timeline[0]["event"] == "DETECTION_CONFIRMED"

    def test_as_dict_has_required_keys(self):
        inc = SimulatedIncident(title="Test", severity=FailureSeverity.HIGH)
        d = inc.as_dict()
        assert "incident_id" in d
        assert "status" in d
        assert "severity" in d
        assert "timeline_events" in d

    def test_timeline_events_count_in_dict(self):
        inc = SimulatedIncident(title="Test", severity=FailureSeverity.LOW)
        inc.add_event("A")
        inc.add_event("B")
        assert inc.as_dict()["timeline_events"] == 2


# ---------------------------------------------------------------------------
# IncidentRegistry
# ---------------------------------------------------------------------------

class TestIncidentRegistry:
    def test_empty_registry(self):
        reg = IncidentRegistry()
        assert reg.count() == 0

    def test_create_incident(self):
        reg = IncidentRegistry()
        inc = reg.create("Stale data", FailureSeverity.MEDIUM, scenario_id="s1")
        assert isinstance(inc, SimulatedIncident)
        assert reg.count() == 1

    def test_created_incident_in_open_list(self):
        reg = IncidentRegistry()
        reg.create("Test", FailureSeverity.LOW)
        assert len(reg.open_incidents()) == 1

    def test_resolved_incident_not_in_open_list(self):
        reg = IncidentRegistry()
        inc = reg.create("Test", FailureSeverity.HIGH)
        inc.resolve("fixed")
        assert len(reg.open_incidents()) == 0

    def test_all_returns_all_regardless_of_status(self):
        reg = IncidentRegistry()
        inc1 = reg.create("T1", FailureSeverity.LOW)
        inc2 = reg.create("T2", FailureSeverity.MEDIUM)
        inc1.resolve()
        assert len(reg.all()) == 2

    def test_create_with_alert_id(self):
        reg = IncidentRegistry()
        inc = reg.create("T", FailureSeverity.HIGH, scenario_id="s1", alert_id="a1")
        assert inc.alert_id == "a1"
