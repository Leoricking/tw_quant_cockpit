"""
reports/portfolio_stable_rollup_report.py — Portfolio Stable Rollup Report v1.5.9.
[!] Research Only. No Real Orders. Freeze/Stabilization Release. Production Trading: BLOCKED.
[!] Never executable. No broker. No order. No ledger write.
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

RESEARCH_ONLY = True
REPORT_VERSION = "1.5.9"


class PortfolioStableRollupReport:
    """
    Generates comprehensive portfolio stable rollup reports.
    Sections: context, capabilities, schemas, enums, policies, cli, health,
              release_gates, contracts, manifest, readiness, debt, safety.
    """

    RESEARCH_ONLY = True
    REPORT_VERSION = REPORT_VERSION

    def generate(self, **kwargs) -> Dict[str, Any]:
        """
        Generate a full portfolio stable rollup report.
        Returns dict with all sections.
        Never executable. No broker. No order. No ledger write.
        """
        generated_at = datetime.datetime.utcnow().isoformat()

        from portfolio.stable_rollup.query_v159 import StableRollupQueryService
        svc = StableRollupQueryService()

        stable_caps = svc.get_stable_capabilities()
        planned_caps = svc.get_planned_capabilities()
        schemas = svc.get_schema_registry()
        enums = svc.get_enum_registry()
        policies = svc.get_policy_registry()
        cli = svc.get_cli_registry()
        health = svc.get_health_registry()
        gates = svc.get_release_gate_registry()
        manifest = svc.build_stable_manifest()
        readiness = svc.build_readiness_matrix()
        debt = svc.scan_stable_debt()
        rollup = svc.run_portfolio_stable_rollup()

        return {
            "report_version": REPORT_VERSION,
            "generated_at": generated_at,
            "research_only": True,
            "executable": False,
            "order_created": False,
            "broker_called": False,
            "ledger_write": False,
            "RESEARCH_ONLY": True,
            "NO_REAL_ORDERS": True,
            "PRODUCTION_TRADING_BLOCKED": True,
            "sections": [
                self._section_context(manifest),
                self._section_capabilities(stable_caps, planned_caps),
                self._section_schemas(schemas),
                self._section_enums(enums),
                self._section_policies(policies),
                self._section_cli(cli),
                self._section_health(health),
                self._section_release_gates(gates),
                self._section_manifest(manifest),
                self._section_readiness(readiness),
                self._section_debt(debt),
                self._section_rollup(rollup),
                self._section_safety(),
            ],
            "status": rollup.status,
            "blocking_debt": rollup.blocking_debt,
            "manifest_hash": manifest.content_hash,
        }

    def _section_context(self, manifest) -> Dict[str, Any]:
        return {
            "section": "context",
            "version": manifest.version,
            "release": manifest.release,
            "baselines": manifest.baselines,
            "research_only": True,
            "freeze_only": True,
        }

    def _section_capabilities(self, stable, planned) -> Dict[str, Any]:
        return {
            "section": "capabilities",
            "stable_count": len(stable),
            "planned_count": len(planned),
            "stable": stable,
            "planned": planned,
        }

    def _section_schemas(self, schemas) -> Dict[str, Any]:
        return {
            "section": "schemas",
            "count": len(schemas),
            "schemas": schemas,
        }

    def _section_enums(self, enums) -> Dict[str, Any]:
        return {
            "section": "enums",
            "count": len(enums),
            "enums": enums,
        }

    def _section_policies(self, policies) -> Dict[str, Any]:
        return {
            "section": "policies",
            "count": len(policies),
            "policies": policies,
        }

    def _section_cli(self, cli) -> Dict[str, Any]:
        return {
            "section": "cli",
            "count": cli.get("count", 0),
            "validation": cli.get("validation", {}),
        }

    def _section_health(self, health) -> Dict[str, Any]:
        return {
            "section": "health",
            "count": len(health),
            "health_checks": health,
        }

    def _section_release_gates(self, gates) -> Dict[str, Any]:
        return {
            "section": "release_gates",
            "count": len(gates),
            "gates": gates,
        }

    def _section_manifest(self, manifest) -> Dict[str, Any]:
        return {
            "section": "manifest",
            "version": manifest.version,
            "release": manifest.release,
            "content_hash": manifest.content_hash,
            "stable_capabilities": manifest.stable_capabilities,
            "schema_count": len(manifest.schema_fingerprints),
            "enum_count": len(manifest.enum_fingerprints),
            "cli_count": manifest.cli_count,
            "test_baseline": manifest.test_collection_baseline,
            "known_limitations": manifest.known_limitations,
            "research_only": True,
        }

    def _section_readiness(self, readiness) -> Dict[str, Any]:
        ready = [r for r in readiness if r.get("ready")]
        not_ready = [r for r in readiness if not r.get("ready")]
        return {
            "section": "readiness",
            "total": len(readiness),
            "ready_count": len(ready),
            "not_ready_count": len(not_ready),
            "items": readiness,
        }

    def _section_debt(self, debt) -> Dict[str, Any]:
        return {
            "section": "debt",
            "blocking_count": debt.get("blocking_count", 0),
            "warning_count": debt.get("warning_count", 0),
            "informational_count": debt.get("informational_count", 0),
            "blocking_debt_zero": debt.get("blocking_debt_zero", True),
            "status": debt.get("status", "PASS"),
        }

    def _section_rollup(self, rollup) -> Dict[str, Any]:
        return {
            "section": "rollup",
            "version": rollup.version,
            "release": rollup.release,
            "stable_capabilities": rollup.stable_capabilities,
            "planned_capabilities": rollup.planned_capabilities,
            "disabled_capabilities": rollup.disabled_capabilities,
            "schemas_total": rollup.schemas_total,
            "enums_total": rollup.enums_total,
            "policies_total": rollup.policies_total,
            "cli_total": rollup.cli_total,
            "blocking_debt": rollup.blocking_debt,
            "status": rollup.status,
            "manifest_hash": rollup.manifest_hash,
            "research_only": True,
        }

    def _section_safety(self) -> Dict[str, Any]:
        return {
            "section": "safety",
            "research_only": True,
            "no_real_orders": True,
            "no_broker": True,
            "no_formal_ledger_write": True,
            "no_live_rebalance": True,
            "no_auto_apply": True,
            "no_auto_rebalance": True,
            "production_trading_blocked": True,
            "freeze_only": True,
            "limitations": [
                "research-only",
                "historical-simulation-only",
                "no-broker",
                "no-real-orders",
                "no-live-trading",
                "no-auto-rebalance",
                "no-optimization",
                "past-performance-not-future-guarantee",
            ],
        }

    def render_text(self, report: Dict[str, Any]) -> str:
        lines = [
            "=" * 60,
            f"  Portfolio Stable Rollup Report v{report.get('report_version')}",
            f"  Generated: {report.get('generated_at', '')}",
            f"  Status: {report.get('status', '?')}",
            f"  Blocking Debt: {report.get('blocking_debt', 0)}",
            f"  Manifest Hash: {report.get('manifest_hash', '?')}",
            "  [!] Research Only. No Real Orders. Production Trading: BLOCKED.",
            "=" * 60,
        ]
        for section in report.get("sections", []):
            name = section.get("section", "?")
            lines.append(f"  [{name.upper()}]")
        return "\n".join(lines)
