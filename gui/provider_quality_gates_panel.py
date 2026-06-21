"""
gui/provider_quality_gates_panel.py — Provider Quality Gates GUI Panel v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Read-only. No override/promote/release-all/buy/sell/order/auto-trade controls.
[!] QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False (always).
[!] No QThread leak.
"""
from __future__ import annotations

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False

TAB_ID = "provider_quality_gates"
TAB_GROUP = "data"
TAB_PRIORITY = "P1"

_SAFETY_BANNER = (
    "[!] RESEARCH ONLY | No Real Orders | No Quality Override | "
    "No Trading | QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE=False"
)


class ProviderQualityGatesPanel:
    """
    Read-only GUI panel for Provider Quality Gates v1.4.6.
    7 sections: Overview, Provider Profiles, Dataset Profiles, Gate Results,
                Quarantine, Decisions, Audit.
    Actions: Refresh, Evaluate Provider/Dataset/Endpoint/Fetch Run,
             Explain Decision, View Audit, Export Report.
    NO override/promote/release-all/buy/sell/order/auto-trade controls.
    """

    tab_id = TAB_ID
    group = TAB_GROUP
    priority = TAB_PRIORITY
    read_only = True
    no_real_orders = True
    production_blocked = True
    quality_score_can_override_blocking = False

    def __init__(self, parent=None) -> None:
        self._parent = parent
        self._sections = [
            "Overview",
            "Provider Profiles",
            "Dataset Profiles",
            "Gate Results",
            "Quarantine",
            "Decisions",
            "Audit",
        ]
        self._actions = [
            "refresh",
            "evaluate_provider",
            "evaluate_dataset",
            "evaluate_endpoint",
            "evaluate_fetch_run",
            "explain_decision",
            "view_audit",
            "export_report",
        ]

    def get_sections(self) -> list:
        return list(self._sections)

    def get_actions(self) -> list:
        return list(self._actions)

    def get_safety_banner(self) -> str:
        return _SAFETY_BANNER

    def render_overview(self) -> dict:
        """Render overview section (read-only)."""
        try:
            from data.governance.quality.health_v146 import ProviderQualityGatesHealthCheck
            hc = ProviderQualityGatesHealthCheck()
            summary = hc.get_health_summary()
        except Exception as exc:
            summary = {"error": str(exc)}
        return {
            "section": "Overview",
            "safety_banner": _SAFETY_BANNER,
            "health_summary": summary,
            "read_only": True,
            "no_real_orders": True,
        }

    def render_provider_profiles(self) -> dict:
        """Render provider profiles section."""
        try:
            from data.governance.quality.provider_gate_v146 import ProviderOperationalGate
            gate = ProviderOperationalGate()
            providers = ["twse_official", "tpex_official", "mops_official",
                         "data_gov_tw", "finmind"]
            profiles = [gate.evaluate(p).to_dict() for p in providers]
        except Exception as exc:
            profiles = [{"error": str(exc)}]
        return {
            "section": "Provider Profiles",
            "profiles": profiles,
            "read_only": True,
        }

    def render_quarantine(self) -> dict:
        """Render quarantine section."""
        return {
            "section": "Quarantine",
            "quarantined": [],
            "auto_release_allowed": False,
            "note": "Manual human review required for any release",
            "read_only": True,
        }

    def render_audit(self) -> dict:
        """Render audit section."""
        return {
            "section": "Audit",
            "note": "Append-only audit. No credentials stored.",
            "read_only": True,
        }

    def on_refresh(self) -> dict:
        """Refresh all panel data (read-only action)."""
        return self.render_overview()

    def on_evaluate_provider(self, provider_id: str) -> dict:
        """Evaluate provider quality gates (read-only action)."""
        try:
            from data.governance.quality.provider_gate_v146 import ProviderOperationalGate
            gate = ProviderOperationalGate()
            profile = gate.evaluate(provider_id)
            return {"status": "ok", "profile": profile.to_dict()}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

    def on_explain_decision(self, decision_id: str) -> dict:
        """Explain a quality decision (read-only action)."""
        from data.governance.quality.query_v146 import ProviderQualityQueryService
        svc = ProviderQualityQueryService()
        return svc.explain_decision(decision_id)

    def on_export_report(self) -> str:
        """Export quality gates report (read-only action)."""
        try:
            from reports.provider_quality_gates_report import ProviderQualityGatesReport
            return ProviderQualityGatesReport().render()
        except Exception as exc:
            return f"Error generating report: {exc}"
