"""portfolio/stable_rollup/query_v159.py — Stable rollup query service v1.5.9."""
import datetime


class StableRollupQueryService:
    def get_stable_capabilities(self):
        from .capability_registry_v159 import CapabilityRegistryV159
        return [
            {"capability_id": c.capability_id, "display_name": c.display_name, "stage": c.stage, "stable_version": c.stable_version}
            for c in CapabilityRegistryV159().get_stable()
        ]

    def get_planned_capabilities(self):
        from .capability_registry_v159 import CapabilityRegistryV159
        return [
            {"capability_id": c.capability_id, "display_name": c.display_name, "stage": c.stage}
            for c in CapabilityRegistryV159().get_planned()
            if c.stage == "PLANNED"
        ]

    def get_disabled_capabilities(self):
        from .capability_registry_v159 import CapabilityRegistryV159
        return [
            {"capability_id": c.capability_id, "display_name": c.display_name, "stage": c.stage}
            for c in CapabilityRegistryV159().get_disabled()
        ]

    def get_schema_registry(self):
        from .schema_registry_v159 import SchemaRegistryV159
        return [
            {"schema_id": s.schema_id, "version": s.schema_version, "fingerprint": s.fingerprint}
            for s in SchemaRegistryV159().get_all()
        ]

    def get_enum_registry(self):
        from .enum_registry_v159 import EnumRegistryV159
        return [
            {"enum_name": e.enum_name, "values": e.values, "fingerprint": e.fingerprint}
            for e in EnumRegistryV159().get_all()
        ]

    def get_policy_registry(self):
        from .policy_registry_v159 import PolicyRegistryV159
        return [
            {"policy_id": p.policy_id, "type": p.policy_type, "version": p.version}
            for p in PolicyRegistryV159().get_all()
        ]

    def get_cli_registry(self):
        from .cli_registry_v159 import CLIRegistryV159
        reg = CLIRegistryV159()
        return {"count": reg.get_count(), "validation": reg.validate()}

    def get_health_registry(self):
        from .health_registry_v159 import HealthRegistryV159
        return [
            {"health_id": h.health_id, "command": h.command, "expected_checks": h.expected_checks}
            for h in HealthRegistryV159().get_all()
        ]

    def get_release_gate_registry(self):
        from .release_gate_registry_v159 import ReleaseGateRegistryV159
        return [
            {"gate_id": g.gate_id, "module": g.module, "expected_checks": g.expected_checks}
            for g in ReleaseGateRegistryV159().get_all()
        ]

    def get_pit_contract(self):
        from .pit_contract_v159 import PITContractV159
        c = PITContractV159().get_contract()
        return {"contract_id": c.contract_id, "version": c.version, "rules": c.rules, "status": c.status}

    def get_lineage_contract(self):
        from .lineage_contract_v159 import LineageContractV159
        c = LineageContractV159().get_contract()
        return {"contract_id": c.contract_id, "version": c.version, "rules": c.rules, "status": c.status}

    def get_reproducibility_contract(self):
        from .reproducibility_contract_v159 import ReproducibilityContractV159
        c = ReproducibilityContractV159().get_contract()
        return {"contract_id": c.contract_id, "version": c.version, "rules": c.rules, "status": c.status}

    def get_safety_contract(self):
        from .safety_contract_v159 import SafetyContractV159
        c = SafetyContractV159().get_contract()
        return {"contract_id": c.contract_id, "version": c.version, "rules": c.rules, "status": c.status}

    def get_compatibility_registry(self):
        from .compatibility_registry_v159 import CompatibilityRegistryV159
        return CompatibilityRegistryV159().get_registry()

    def get_migration_registry(self):
        from .migration_registry_v159 import MigrationRegistryV159
        return [
            {"migration_id": m.migration_id, "source": m.source_version, "target": m.target_version, "notes": m.notes}
            for m in MigrationRegistryV159().get_all()
        ]

    def build_stable_manifest(self):
        from .stable_manifest_v159 import StableManifestBuilder
        return StableManifestBuilder().build()

    def validate_stable_manifest(self):
        from .stable_manifest_v159 import StableManifestBuilder
        m = StableManifestBuilder().build()
        return StableManifestBuilder().validate(m)

    def build_readiness_matrix(self):
        from .readiness_matrix_v159 import ReadinessMatrixV159
        items = ReadinessMatrixV159().get_all()
        return [
            {"capability": i.capability, "stage": i.stage, "ready": i.ready, "blockers": i.blockers}
            for i in items
        ]

    def run_integration_audit(self):
        from .integration_audit_v159 import IntegrationAuditV159
        return IntegrationAuditV159().run_all()

    def scan_stable_debt(self):
        from .debt_scanner_v159 import DebtScannerV159
        return DebtScannerV159().run_all()

    def run_portfolio_stable_rollup(self):
        from .models_v159 import StableRollupResult
        manifest = self.build_stable_manifest()
        audit = self.run_integration_audit()
        debt = self.scan_stable_debt()
        cap_stable = len(self.get_stable_capabilities())
        cap_planned = len(self.get_planned_capabilities())
        cap_disabled = len(self.get_disabled_capabilities())
        blocking_debt = debt.get("blocking_count", 0)
        safety = audit.get("checks", {}).get("safety", {})
        safety_violations = safety.get("violations", [])
        status = "BLOCKED" if (blocking_debt > 0 or safety_violations) else "PASS"
        return StableRollupResult(
            version=manifest.version,
            release=manifest.release,
            capabilities_total=cap_stable + cap_planned + cap_disabled,
            stable_capabilities=cap_stable,
            planned_capabilities=cap_planned,
            disabled_capabilities=cap_disabled,
            schemas_total=len(self.get_schema_registry()),
            enums_total=len(self.get_enum_registry()),
            policies_total=len(self.get_policy_registry()),
            cli_total=manifest.cli_count,
            health_checks=len(self.get_health_registry()),
            release_gates=len(self.get_release_gate_registry()),
            blocking_debt=blocking_debt,
            safety_violations=safety_violations,
            manifest_hash=manifest.content_hash,
            status=status,
            research_only=True,
            generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )

    def get_stable_rollup_result(self):
        return self.run_portfolio_stable_rollup()

    def explain_stable_rollup(self):
        result = self.run_portfolio_stable_rollup()
        return {
            "summary": f"Portfolio Stable Rollup v{result.version} — {result.stable_capabilities} stable capabilities, {result.planned_capabilities} planned.",
            "stable_capabilities": self.get_stable_capabilities(),
            "planned_capabilities": self.get_planned_capabilities(),
            "schemas": len(self.get_schema_registry()),
            "enums": len(self.get_enum_registry()),
            "cli_commands": result.cli_total,
            "blocking_debt": result.blocking_debt,
            "status": result.status,
            "safety_text": "RESEARCH_ONLY | NO_REAL_ORDER | NO_BROKER | PRODUCTION_TRADING_BLOCKED",
            "limitations": [
                "research-only", "no-broker", "no-real-orders",
                "no-live-trading", "no-auto-rebalance", "historical-simulation-only",
            ],
        }
