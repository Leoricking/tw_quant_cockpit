"""
reports/provider_quality_gates_report.py — Provider Quality Gates Report v1.4.6.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Read-only. No override controls.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


class ProviderQualityGatesReport:
    """
    Generates the provider quality gates report.
    Sections: Header, Safety Banner, Health Summary, Provider Profiles,
              Dataset Profiles, Gate Registry, Quarantine Status,
              Decision Summary, Audit Summary, Score Summary,
              Policy Summary, Safety Invariants, Footer.
    """

    VERSION = "1.4.6"

    def render(self) -> str:
        lines = []
        lines.extend(self._render_header())
        lines.extend(self._render_safety_banner())
        lines.extend(self._render_health_summary())
        lines.extend(self._render_provider_profiles())
        lines.extend(self._render_gate_registry())
        lines.extend(self._render_quarantine_status())
        lines.extend(self._render_decision_summary())
        lines.extend(self._render_score_summary())
        lines.extend(self._render_policy_summary())
        lines.extend(self._render_safety_invariants())
        lines.extend(self._render_footer())
        return "\n".join(lines)

    def _render_header(self) -> List[str]:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        return [
            "=" * 70,
            f"  TW Quant Cockpit — Provider Quality Gates Report v{self.VERSION}",
            f"  Generated: {now}",
            "=" * 70,
            "",
        ]

    def _render_safety_banner(self) -> List[str]:
        return [
            "  [!] RESEARCH ONLY | No Real Orders | No Quality Override",
            "  [!] QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = False",
            "  [!] AUTO_PROVIDER_PROMOTION_ENABLED = False",
            "  [!] AUTO_QUARANTINE_RELEASE_ENABLED = False",
            "  [!] MOCK_FALLBACK_ENABLED = False",
            "",
        ]

    def _render_health_summary(self) -> List[str]:
        lines = ["  SECTION 1: Health Summary", "  " + "-" * 50]
        try:
            from data.governance.quality.health_v146 import ProviderQualityGatesHealthCheck
            hc = ProviderQualityGatesHealthCheck()
            summary = hc.get_health_summary()
            lines.append(f"  Total checks: {summary['total']}")
            lines.append(f"  Passed:       {summary['passed']}")
            lines.append(f"  Failed:       {summary['failed']}")
            lines.append(f"  Warned:       {summary['warned']}")
        except Exception as exc:
            lines.append(f"  Health check error: {exc}")
        lines.append("")
        return lines

    def _render_provider_profiles(self) -> List[str]:
        lines = ["  SECTION 2: Provider Quality Profiles", "  " + "-" * 50]
        try:
            from data.governance.quality.provider_gate_v146 import ProviderOperationalGate
            gate = ProviderOperationalGate()
            for p in ["twse_official", "tpex_official", "mops_official", "data_gov_tw", "finmind"]:
                profile = gate.evaluate(p)
                lines.append(
                    f"  {p}: {profile.quality_state} | auth={profile.authority_level} | "
                    f"research={profile.formal_research_allowed}"
                )
        except Exception as exc:
            lines.append(f"  Provider profiles error: {exc}")
        lines.append("")
        return lines

    def _render_gate_registry(self) -> List[str]:
        lines = ["  SECTION 3: Gate Registry", "  " + "-" * 50]
        try:
            from data.governance.quality.gate_registry_v146 import QualityGateRegistry
            reg = QualityGateRegistry()
            lines.append(f"  Total gates: {len(reg.list_gates())}")
            lines.append(f"  Mandatory:   {len(reg.list_mandatory_gates())}")
            lines.append(f"  Policy:      {reg.get_policy_version()}")
            result = reg.validate_registry()
            lines.append(f"  Valid:       {result['valid']}")
        except Exception as exc:
            lines.append(f"  Gate registry error: {exc}")
        lines.append("")
        return lines

    def _render_quarantine_status(self) -> List[str]:
        return [
            "  SECTION 4: Quarantine Status",
            "  " + "-" * 50,
            "  No providers currently quarantined (in-memory store).",
            "  auto_release_allowed = False always.",
            "",
        ]

    def _render_decision_summary(self) -> List[str]:
        return [
            "  SECTION 5: Decision Summary",
            "  " + "-" * 50,
            "  No decisions recorded in current session.",
            "  Blocking failures always override quality score.",
            "",
        ]

    def _render_score_summary(self) -> List[str]:
        lines = ["  SECTION 6: Quality Score Summary", "  " + "-" * 50]
        try:
            from data.governance.quality.score_v146 import QualityScoreEngine, _DEFAULT_WEIGHTS
            lines.append("  Score weights (v1.4.6):")
            for k, v in _DEFAULT_WEIGHTS.items():
                lines.append(f"    {k}: {v:.0f}")
            lines.append("  [!] Score CANNOT override blocking failures.")
        except Exception as exc:
            lines.append(f"  Score error: {exc}")
        lines.append("")
        return lines

    def _render_policy_summary(self) -> List[str]:
        lines = ["  SECTION 7: Policy Summary", "  " + "-" * 50]
        try:
            from data.governance.quality.policy_v146 import QualityPolicyManager
            mgr = QualityPolicyManager()
            lines.append(f"  Policy version: {mgr.get_policy_version()}")
            lines.append(f"  Provider policies: {mgr.list_provider_policies()}")
        except Exception as exc:
            lines.append(f"  Policy error: {exc}")
        lines.append("")
        return lines

    def _render_safety_invariants(self) -> List[str]:
        from data.governance.quality import (
            NO_REAL_ORDERS as _NRO,
            BROKER_EXECUTION_ENABLED as _BEE,
            PRODUCTION_TRADING_BLOCKED as _PTB,
            QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE as _QSCO,
            AUTO_PROVIDER_PROMOTION_ENABLED as _APE,
            AUTO_QUARANTINE_RELEASE_ENABLED as _AQR,
            MOCK_FALLBACK_ENABLED as _MFE,
        )
        return [
            "  SECTION 8: Safety Invariants",
            "  " + "-" * 50,
            f"  NO_REAL_ORDERS = {_NRO}",
            f"  BROKER_EXECUTION_ENABLED = {_BEE}",
            f"  PRODUCTION_TRADING_BLOCKED = {_PTB}",
            f"  QUALITY_SCORE_CAN_OVERRIDE_BLOCKING_FAILURE = {_QSCO}",
            f"  AUTO_PROVIDER_PROMOTION_ENABLED = {_APE}",
            f"  AUTO_QUARANTINE_RELEASE_ENABLED = {_AQR}",
            f"  MOCK_FALLBACK_ENABLED = {_MFE}",
            "",
        ]

    def _render_footer(self) -> List[str]:
        return [
            "=" * 70,
            "  [!] Research Only. No Real Orders. Not Investment Advice.",
            "  [!] This report does NOT enable trading or override gates.",
            "=" * 70,
        ]
