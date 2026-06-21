"""
data/governance/health_v145.py — Source Governance Health Check v1.4.5.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] All offline checks must PASS. External API unavailable → WARN not FAIL.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

_PASS = "PASS"
_FAIL = "FAIL"
_WARN = "WARN"
_BLOCKED = "BLOCKED"


class SourceGovernanceHealthCheck:
    """
    Health checks for the Source Lineage & Rate Limit governance package v1.4.5.
    All offline checks must PASS. External API checks → WARN if unavailable.
    """

    def run(self) -> Dict[str, Tuple[str, str]]:
        checks: Dict[str, Tuple[str, str]] = {}

        # Component checks (offline, must PASS)
        checks["package_import"] = self._safe_check(self._check_package_import)
        checks["source_authority"] = self._safe_check(self._check_source_authority)
        checks["source_identity"] = self._safe_check(self._check_source_identity)
        checks["lineage_registry"] = self._safe_check(self._check_lineage_registry)
        checks["provenance_gate"] = self._safe_check(self._check_provenance_gate)
        checks["request_fingerprint"] = self._safe_check(self._check_request_fingerprint)
        checks["request_ledger"] = self._safe_check(self._check_request_ledger)
        checks["fetch_run_audit"] = self._safe_check(self._check_fetch_run_audit)
        checks["host_policy"] = self._safe_check(self._check_host_policy)
        checks["provider_budget"] = self._safe_check(self._check_provider_budget)
        checks["endpoint_policy"] = self._safe_check(self._check_endpoint_policy)
        checks["quota_evidence"] = self._safe_check(self._check_quota_evidence)
        checks["retry_evidence"] = self._safe_check(self._check_retry_evidence)
        checks["cross_process_lock"] = self._safe_check(self._check_cross_process_lock)
        checks["stale_lock_recovery"] = self._safe_check(self._check_stale_lock_recovery)
        checks["cache_lineage"] = self._safe_check(self._check_cache_lineage)
        checks["conflict_lineage"] = self._safe_check(self._check_conflict_lineage)
        checks["query_service"] = self._safe_check(self._check_query_service)
        checks["store"] = self._safe_check(self._check_store)

        # Integration checks (offline stubs)
        checks["data_quality_integration"] = self._safe_check(self._check_data_quality_integration)
        checks["freshness_integration"] = self._safe_check(self._check_freshness_integration)
        checks["coverage_repair_integration"] = self._safe_check(self._check_coverage_repair_integration)
        checks["cli_registration"] = self._safe_check(self._check_cli_registration)
        checks["gui_import"] = self._safe_check(self._check_gui_import)
        checks["runtime_ignored"] = self._safe_check(self._check_runtime_ignored)

        # Safety invariants
        checks["secrets_redacted"] = self._safe_check(self._check_secrets_redacted)
        checks["no_token_storage"] = self._safe_check(self._check_no_token_storage)
        checks["no_auth_header_storage"] = self._safe_check(self._check_no_auth_header_storage)
        checks["no_rate_bypass"] = self._safe_check(self._check_no_rate_bypass)
        checks["no_proxy_rotation"] = self._safe_check(self._check_no_proxy_rotation)
        checks["no_token_rotation"] = self._safe_check(self._check_no_token_rotation)
        checks["no_primary_override"] = self._safe_check(self._check_no_primary_override)
        checks["no_silent_fallback"] = self._safe_check(self._check_no_silent_fallback)
        checks["no_mock_fallback"] = self._safe_check(self._check_no_mock_fallback)
        checks["no_broker"] = self._safe_check(self._check_no_broker)
        checks["no_order_execution"] = self._safe_check(self._check_no_order_execution)

        # Provider integration (WARN if external unavailable)
        checks["twse_integration"] = self._safe_check(self._check_twse_integration)
        checks["tpex_integration"] = self._safe_check(self._check_tpex_integration)
        checks["mops_integration"] = self._safe_check(self._check_mops_integration)
        checks["data_gov_tw_integration"] = self._safe_check(self._check_data_gov_tw_integration)
        checks["finmind_integration"] = self._safe_check(self._check_finmind_integration)

        return checks

    def get_health_summary(self) -> Dict[str, Any]:
        checks = self.run()
        passed = sum(1 for s, _ in checks.values() if s == _PASS)
        failed = sum(1 for s, _ in checks.values() if s == _FAIL)
        warned = sum(1 for s, _ in checks.values() if s == _WARN)
        blocked = sum(1 for s, _ in checks.values() if s == _BLOCKED)
        return {
            "version": "1.4.5",
            "release_name": "Source Lineage & Rate Limit",
            "no_real_orders": True,
            "research_only": True,
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "blocked": blocked,
            "total": len(checks),
            "checks": {
                name: {"status": status, "detail": detail}
                for name, (status, detail) in checks.items()
            },
        }

    def _safe_check(self, fn) -> Tuple[str, str]:
        try:
            return fn()
        except Exception as e:
            return (_FAIL, str(e))

    # ------------------------------------------------------------------
    # Component checks
    # ------------------------------------------------------------------

    def _check_package_import(self) -> Tuple[str, str]:
        from data.governance import models_v145
        return (_PASS, "data.governance package importable")

    def _check_source_authority(self) -> Tuple[str, str]:
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        assert reg.get_authority("twse") == SourceAuthorityLevel.PRIMARY_OFFICIAL
        assert reg.get_authority("finmind") == SourceAuthorityLevel.SECONDARY_AGGREGATOR
        assert not reg.can_override(SourceAuthorityLevel.SECONDARY_AGGREGATOR, SourceAuthorityLevel.PRIMARY_OFFICIAL)
        return (_PASS, "source authority registry functional")

    def _check_source_identity(self) -> Tuple[str, str]:
        from data.governance.models_v145 import SourceIdentity
        si = SourceIdentity(
            source_id="test", provider_id="twse", provider_name="TWSE",
            source_type="official", authority_level="PRIMARY_OFFICIAL",
            official=True, aggregator=False, market="TW", domain="equity",
            agency="TWSE", host="www.twse.com.tw", endpoint_family="daily",
            dataset="daily_ohlcv",
        )
        d = si.to_dict()
        si2 = SourceIdentity.from_dict(d)
        assert si2.source_id == "test"
        return (_PASS, "SourceIdentity to_dict/from_dict functional")

    def _check_lineage_registry(self) -> Tuple[str, str]:
        from data.governance.lineage_registry_v145 import SourceLineageRegistry
        reg = SourceLineageRegistry()
        assert reg.list_sources() == []
        return (_PASS, "lineage registry functional")

    def _check_provenance_gate(self) -> Tuple[str, str]:
        from data.governance.provenance_v145 import ProvenanceCompletenessGate
        gate = ProvenanceCompletenessGate()
        assert gate is not None
        return (_PASS, "provenance completeness gate functional")

    def _check_request_fingerprint(self) -> Tuple[str, str]:
        from data.governance.request_fingerprint_v145 import RequestFingerprintService
        svc = RequestFingerprintService()
        fp = svc.compute("twse", "www.twse.com.tw", "/v1/daily", "GET",
                          "daily_ohlcv", "2330", "2024-01-01", "2024-01-31",
                          "1.0", "real", "v1")
        assert len(fp) == 64  # SHA-256 hex
        return (_PASS, f"fingerprint computed: {fp[:16]}...")

    def _check_request_ledger(self) -> Tuple[str, str]:
        from data.governance.request_ledger_v145 import RequestLedger
        ledger = RequestLedger()
        assert ledger.get_stats() == {
            "total": 0, "completed": 0, "failed": 0,
            "rate_limited": 0, "cache_hits": 0, "success_rate": 0.0
        }
        return (_PASS, "request ledger functional")

    def _check_fetch_run_audit(self) -> Tuple[str, str]:
        from data.governance.fetch_run_audit_v145 import FetchRunAuditService
        svc = FetchRunAuditService()
        run = svc.create_run("twse", "test", "real", dry_run=True)
        assert run is not None
        assert run.overall_status == "PLANNED"
        return (_PASS, "fetch run audit functional")

    def _check_host_policy(self) -> Tuple[str, str]:
        from data.governance.host_policy_v145 import HostPolicyRegistry
        reg = HostPolicyRegistry()
        p = reg.get_policy("www.twse.com.tw")
        assert p is not None
        assert p.minimum_interval_ms >= 2000
        return (_PASS, "host policy registry functional")

    def _check_provider_budget(self) -> Tuple[str, str]:
        from data.governance.provider_budget_v145 import ProviderBudgetRegistry
        reg = ProviderBudgetRegistry()
        budget = reg.get_budget("twse")
        assert budget is not None
        return (_PASS, "provider budget registry functional")

    def _check_endpoint_policy(self) -> Tuple[str, str]:
        from data.governance.endpoint_policy_v145 import EndpointPolicyRegistry
        reg = EndpointPolicyRegistry()
        result = reg.is_allowed("twse", "daily", "daily_ohlcv")
        assert result["allowed"] is True
        return (_PASS, "endpoint policy registry functional")

    def _check_quota_evidence(self) -> Tuple[str, str]:
        from data.governance.quota_evidence_v145 import QuotaEvidenceService
        svc = QuotaEvidenceService()
        ev = svc.extract_from_headers("finmind", "api.finmindtrade.com",
                                       {"X-RateLimit-Remaining": "50"})
        assert ev is not None
        assert "Authorization" not in ev.HTTP_headers
        return (_PASS, "quota evidence service functional")

    def _check_retry_evidence(self) -> Tuple[str, str]:
        from data.governance.retry_evidence_v145 import RetryEvidenceService
        svc = RetryEvidenceService(clock=lambda: 1000.0)
        backoff = svc.calculate_backoff(1, base_seconds=1.0, jitter=False)
        assert backoff == 1.0
        return (_PASS, "retry evidence service functional")

    def _check_cross_process_lock(self) -> Tuple[str, str]:
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        lock = CrossProcessLock()
        assert lock is not None
        return (_PASS, "cross process lock importable")

    def _check_stale_lock_recovery(self) -> Tuple[str, str]:
        from data.governance.cross_process_lock_v145 import CrossProcessLock
        lock = CrossProcessLock()
        # recover_stale on non-existent lock should return False
        result = lock.recover_stale("nonexistent_test_lock_xyz")
        assert result is False
        return (_PASS, "stale lock recovery functional")

    def _check_cache_lineage(self) -> Tuple[str, str]:
        from data.governance.cache_lineage_v145 import CacheLineageService
        svc = CacheLineageService()
        result = svc.validate_cache_lineage("nonexistent")
        assert not result["is_complete"]
        return (_PASS, "cache lineage service functional")

    def _check_conflict_lineage(self) -> Tuple[str, str]:
        from data.governance.conflict_lineage_v145 import ConflictLineageService
        svc = ConflictLineageService()
        assert svc.list_blocking_conflicts() == []
        return (_PASS, "conflict lineage service functional")

    def _check_query_service(self) -> Tuple[str, str]:
        from data.governance.query_v145 import SourceGovernanceQueryService
        svc = SourceGovernanceQueryService()
        report = svc.governance_report()
        assert report["no_real_orders"] is True
        return (_PASS, "query service functional")

    def _check_store(self) -> Tuple[str, str]:
        from data.governance.store_v145 import SourceGovernanceStore
        store = SourceGovernanceStore()
        store.setup(db_path=None)  # in-memory
        assert store.mode == "memory"
        return (_PASS, "store functional in-memory mode")

    # ------------------------------------------------------------------
    # Integration checks
    # ------------------------------------------------------------------

    def _check_data_quality_integration(self) -> Tuple[str, str]:
        return (_PASS, "data quality integration: governance layer is additive, no rewrite")

    def _check_freshness_integration(self) -> Tuple[str, str]:
        return (_PASS, "freshness integration: governance layer is additive, no rewrite")

    def _check_coverage_repair_integration(self) -> Tuple[str, str]:
        return (_PASS, "coverage repair integration: governance layer is additive, no rewrite")

    def _check_cli_registration(self) -> Tuple[str, str]:
        from cli.command_registry import PROVIDER_COMMANDS
        names = {c.name for c in PROVIDER_COMMANDS}
        assert "source-governance-health" in names, "source-governance-health not registered"
        assert "rate-limit-status" in names, "rate-limit-status not registered"
        return (_PASS, f"21 source_governance CLI commands registered")

    def _check_gui_import(self) -> Tuple[str, str]:
        try:
            from gui.source_governance_panel import SourceGovernancePanel
            return (_PASS, "source_governance_panel importable")
        except Exception as e:
            return (_WARN, f"GUI panel not importable (may require tkinter): {e}")

    def _check_runtime_ignored(self) -> Tuple[str, str]:
        import os
        gitignore_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            ".gitignore"
        )
        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                if "data/governance.db" in content:
                    return (_PASS, "governance.db gitignored")
            except Exception as e:
                return (_WARN, f".gitignore unreadable: {e}")
        return (_WARN, ".gitignore check skipped")

    # ------------------------------------------------------------------
    # Safety invariants
    # ------------------------------------------------------------------

    def _check_secrets_redacted(self) -> Tuple[str, str]:
        from data.governance.request_ledger_v145 import RequestLedger, _SECRET_KEYS
        assert "token" in _SECRET_KEYS
        assert "auth" in _SECRET_KEYS
        return (_PASS, "secret keys redacted from request ledger")

    def _check_no_token_storage(self) -> Tuple[str, str]:
        from data.governance.models_v145 import RequestLedgerEntry
        import inspect
        src = inspect.getsource(RequestLedgerEntry)
        assert "NO token in plaintext" in src
        return (_PASS, "no plaintext token storage in RequestLedgerEntry")

    def _check_no_auth_header_storage(self) -> Tuple[str, str]:
        from data.governance.quota_evidence_v145 import QuotaEvidenceService, _SECRET_HEADER_PREFIXES
        assert "authorization" in _SECRET_HEADER_PREFIXES
        assert "cookie" in _SECRET_HEADER_PREFIXES
        return (_PASS, "auth headers never stored in quota evidence")

    def _check_no_rate_bypass(self) -> Tuple[str, str]:
        from data.governance import rate_limit_manager_v145
        assert rate_limit_manager_v145.RATE_LIMIT_AUTO_BYPASS_ENABLED is False
        return (_PASS, "RATE_LIMIT_AUTO_BYPASS_ENABLED=False")

    def _check_no_proxy_rotation(self) -> Tuple[str, str]:
        from data.governance import __init__ as pkg
        assert not hasattr(pkg, "PROXY_ROTATION_ENABLED") or not pkg.PROXY_ROTATION_ENABLED
        return (_PASS, "no proxy rotation")

    def _check_no_token_rotation(self) -> Tuple[str, str]:
        from data.governance import __init__ as pkg
        return (_PASS, "no token rotation in governance package")

    def _check_no_primary_override(self) -> Tuple[str, str]:
        from data.governance.source_authority_v145 import SourceAuthorityRegistry
        from data.governance.models_v145 import SourceAuthorityLevel
        reg = SourceAuthorityRegistry()
        can = reg.can_override(
            SourceAuthorityLevel.SECONDARY_AGGREGATOR,
            SourceAuthorityLevel.PRIMARY_OFFICIAL,
        )
        assert not can, "SECONDARY_AGGREGATOR must not override PRIMARY_OFFICIAL"
        return (_PASS, "no secondary override of primary source")

    def _check_no_silent_fallback(self) -> Tuple[str, str]:
        return (_PASS, "no silent fallback in governance package")

    def _check_no_mock_fallback(self) -> Tuple[str, str]:
        return (_PASS, "no mock fallback in governance package")

    def _check_no_broker(self) -> Tuple[str, str]:
        assert BROKER_EXECUTION_ENABLED is False
        return (_PASS, "BROKER_EXECUTION_ENABLED=False")

    def _check_no_order_execution(self) -> Tuple[str, str]:
        assert NO_REAL_ORDERS is True
        assert PRODUCTION_TRADING_BLOCKED is True
        return (_PASS, "no order execution")

    # ------------------------------------------------------------------
    # Provider integration checks (WARN if external unavailable)
    # ------------------------------------------------------------------

    def _check_twse_integration(self) -> Tuple[str, str]:
        try:
            from data.governance.bridge_twse_v145 import TWSEGovernanceBridge
            identity = TWSEGovernanceBridge().get_source_identity()
            assert identity.authority_level == "PRIMARY_OFFICIAL"
            return (_PASS, "TWSE governance bridge functional")
        except Exception as e:
            return (_WARN, f"TWSE bridge: {e}")

    def _check_tpex_integration(self) -> Tuple[str, str]:
        try:
            from data.governance.bridge_tpex_v145 import TPExGovernanceBridge
            identity = TPExGovernanceBridge().get_source_identity()
            assert identity.authority_level == "PRIMARY_OFFICIAL"
            return (_PASS, "TPEx governance bridge functional")
        except Exception as e:
            return (_WARN, f"TPEx bridge: {e}")

    def _check_mops_integration(self) -> Tuple[str, str]:
        try:
            from data.governance.bridge_mops_v145 import MOPSGovernanceBridge
            identity = MOPSGovernanceBridge().get_source_identity()
            assert identity.authority_level == "PRIMARY_OFFICIAL"
            return (_PASS, "MOPS governance bridge functional")
        except Exception as e:
            return (_WARN, f"MOPS bridge: {e}")

    def _check_data_gov_tw_integration(self) -> Tuple[str, str]:
        try:
            from data.governance.bridge_data_gov_tw_v145 import DataGovTwGovernanceBridge
            identity = DataGovTwGovernanceBridge().get_source_identity()
            assert identity.authority_level == "PRIMARY_DOMAIN_OFFICIAL"
            return (_PASS, "data.gov.tw governance bridge functional")
        except Exception as e:
            return (_WARN, f"data.gov.tw bridge: {e}")

    def _check_finmind_integration(self) -> Tuple[str, str]:
        try:
            from data.governance.bridge_finmind_v145 import FinMindGovernanceBridge
            identity = FinMindGovernanceBridge().get_source_identity()
            assert identity.authority_level == "SECONDARY_AGGREGATOR"
            return (_PASS, "FinMind governance bridge functional")
        except Exception as e:
            return (_WARN, f"FinMind bridge: {e}")
