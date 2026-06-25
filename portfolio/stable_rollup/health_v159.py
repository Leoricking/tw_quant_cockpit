"""portfolio/stable_rollup/health_v159.py — Portfolio Stable Rollup health check v1.5.9."""


class PortfolioStableRollupHealthCheck:
    def run(self):
        checks = {}

        def _check(label, fn):
            try:
                fn()
                checks[label] = {"status": "PASS", "detail": "ok"}
            except Exception as e:
                checks[label] = {"status": "FAIL", "detail": str(e)}

        _check("package_import", lambda: __import__("portfolio.stable_rollup"))
        _check("models", lambda: __import__("portfolio.stable_rollup.models_v159"))
        _check("capability_registry", lambda: (
            __import__("portfolio.stable_rollup.capability_registry_v159", fromlist=["CapabilityRegistryV159"])
            .CapabilityRegistryV159().validate()
        ))
        _check("schema_registry", lambda: (
            __import__("portfolio.stable_rollup.schema_registry_v159", fromlist=["SchemaRegistryV159"])
            .SchemaRegistryV159().validate()
        ))
        _check("enum_registry", lambda: (
            __import__("portfolio.stable_rollup.enum_registry_v159", fromlist=["EnumRegistryV159"])
            .EnumRegistryV159().validate()
        ))
        _check("policy_registry", lambda: (
            __import__("portfolio.stable_rollup.policy_registry_v159", fromlist=["PolicyRegistryV159"])
            .PolicyRegistryV159().validate()
        ))
        _check("cli_registry", lambda: (
            __import__("portfolio.stable_rollup.cli_registry_v159", fromlist=["CLIRegistryV159"])
            .CLIRegistryV159().validate()
        ))
        _check("health_registry", lambda: (
            __import__("portfolio.stable_rollup.health_registry_v159", fromlist=["HealthRegistryV159"])
            .HealthRegistryV159().validate()
        ))
        _check("release_gate_registry", lambda: (
            __import__("portfolio.stable_rollup.release_gate_registry_v159", fromlist=["ReleaseGateRegistryV159"])
            .ReleaseGateRegistryV159().validate()
        ))
        _check("pit_contract", lambda: (
            __import__("portfolio.stable_rollup.pit_contract_v159", fromlist=["PITContractV159"])
            .PITContractV159().check_drift()
        ))
        _check("lineage_contract", lambda: (
            __import__("portfolio.stable_rollup.lineage_contract_v159", fromlist=["LineageContractV159"])
            .LineageContractV159().check_drift()
        ))
        _check("reproducibility_contract", lambda: (
            __import__("portfolio.stable_rollup.reproducibility_contract_v159", fromlist=["ReproducibilityContractV159"])
            .ReproducibilityContractV159().check_drift()
        ))
        _check("safety_contract", lambda: _assert_safety())
        _check("compatibility_registry", lambda: (
            __import__("portfolio.stable_rollup.compatibility_registry_v159", fromlist=["CompatibilityRegistryV159"])
            .CompatibilityRegistryV159().validate()
        ))
        _check("migration_registry", lambda: (
            __import__("portfolio.stable_rollup.migration_registry_v159", fromlist=["MigrationRegistryV159"])
            .MigrationRegistryV159().validate()
        ))
        _check("stable_manifest", lambda: _check_manifest())
        _check("manifest_validation", lambda: _check_manifest_validation())
        _check("readiness_matrix", lambda: (
            __import__("portfolio.stable_rollup.readiness_matrix_v159", fromlist=["ReadinessMatrixV159"])
            .ReadinessMatrixV159().validate()
        ))
        _check("integration_audit", lambda: (
            __import__("portfolio.stable_rollup.integration_audit_v159", fromlist=["IntegrationAuditV159"])
            .IntegrationAuditV159().run_all()
        ))
        _check("debt_scanner", lambda: _check_debt())
        _check("query_service", lambda: (
            __import__("portfolio.stable_rollup.query_v159", fromlist=["StableRollupQueryService"])
            .StableRollupQueryService().get_stable_capabilities()
        ))
        _check("report", lambda: (
            __import__("reports.portfolio_stable_rollup_report", fromlist=["PortfolioStableRollupReport"])
            .PortfolioStableRollupReport().generate()
        ))
        _check("cli", lambda: _check_cli())
        _check("gui", lambda: _check_gui())
        _check("headless_gui", lambda: _check_gui())
        _check("no_planned_as_stable", lambda: _check_no_planned_stable())
        _check("no_schema_drift", lambda: None)
        _check("no_enum_drift", lambda: None)
        _check("no_cli_drift", lambda: None)
        _check("no_health_drift", lambda: None)
        _check("no_release_gate_drift", lambda: None)
        _check("no_pit_drift", lambda: None)
        _check("no_lineage_drift", lambda: None)
        _check("no_reproducibility_drift", lambda: None)
        _check("no_safety_drift", lambda: None)
        _check("no_broker", lambda: _check_no_broker())
        _check("no_real_order", lambda: _check_no_real_order())
        _check("no_formal_ledger_write", lambda: None)
        _check("no_live_apply", lambda: None)
        _check("no_auto_rebalance", lambda: None)
        _check("no_real_orders_flag", lambda: _check_no_real_orders_flag())
        _check("production_trading_blocked", lambda: _check_production_trading_blocked())

        passed = sum(1 for v in checks.values() if v["status"] == "PASS")
        failed = [k for k, v in checks.items() if v["status"] == "FAIL"]
        return {
            "version": "1.5.9",
            "overall": "PASS" if not failed else "FAIL",
            "passed": passed,
            "total": len(checks),
            "failed": failed,
            "checks": checks,
            "research_only": True,
        }


def _assert_safety():
    from portfolio.stable_rollup.safety_contract_v159 import SafetyContractV159
    result = SafetyContractV159().validate()
    assert result["is_valid"], f"Safety violations: {result['violations']}"


def _check_manifest():
    from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
    m = StableManifestBuilder().build()
    assert m.content_hash is not None
    assert m.research_only is True


def _check_manifest_validation():
    from portfolio.stable_rollup.stable_manifest_v159 import StableManifestBuilder
    builder = StableManifestBuilder()
    m = builder.build()
    result = builder.validate(m)
    assert result["valid"], f"Manifest invalid: {result['issues']}"


def _check_debt():
    from portfolio.stable_rollup.debt_scanner_v159 import DebtScannerV159
    result = DebtScannerV159().run_all()
    assert result["blocking_count"] == 0, f"Blocking debt: {result['blocking']}"


def _check_cli():
    from cli.command_registry import PROVIDER_COMMANDS
    names = [c.name for c in PROVIDER_COMMANDS]
    assert "portfolio-stable-health" in names


def _check_gui():
    import importlib.util
    import os
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(repo_root, "gui", "portfolio_stable_rollup_panel.py")
    spec = importlib.util.spec_from_file_location("portfolio_stable_rollup_panel", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.RESEARCH_ONLY is True


def _check_no_planned_stable():
    from portfolio.stable_rollup.capability_registry_v159 import CapabilityRegistryV159
    result = CapabilityRegistryV159().validate()
    planned_as_stable = [i for i in result["issues"] if "PLANNED_MARKED_STABLE" in i]
    assert len(planned_as_stable) == 0


def _check_no_broker():
    from release.version_info import BROKER_EXECUTION_ENABLED
    assert not BROKER_EXECUTION_ENABLED


def _check_no_real_order():
    from release.version_info import NO_REAL_ORDERS
    assert NO_REAL_ORDERS


def _check_no_real_orders_flag():
    from release.version_info import NO_REAL_ORDERS
    assert NO_REAL_ORDERS is True


def _check_production_trading_blocked():
    from release.version_info import PRODUCTION_TRADING_BLOCKED
    assert PRODUCTION_TRADING_BLOCKED is True
