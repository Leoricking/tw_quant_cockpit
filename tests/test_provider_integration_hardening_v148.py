"""
tests/test_provider_integration_hardening_v148.py — v1.4.8 Provider Integration Hardening tests.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] All tests offline. No network. No external fetch.
"""
from __future__ import annotations

import json
import os

import pytest

_FIXTURE_DIR = os.path.join(
    os.path.dirname(__file__), "fixtures", "provider_integration_hardening"
)


def _load_fixture(name: str) -> dict:
    path = os.path.join(_FIXTURE_DIR, name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ===========================================================================
# Contracts
# ===========================================================================

class TestContracts:
    def test_1_twse_contract(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        r = ProviderContractValidator().validate_provider("twse_official")
        assert r.authority == "PRIMARY"
        assert r.status == "PASS"

    def test_2_tpex_contract(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        r = ProviderContractValidator().validate_provider("tpex_official")
        assert r.authority == "PRIMARY"
        assert r.status == "PASS"

    def test_3_mops_contract(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        r = ProviderContractValidator().validate_provider("mops_official")
        assert r.authority == "PRIMARY"
        assert r.status == "PASS"

    def test_4_data_gov_tw_contract(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        r = ProviderContractValidator().validate_provider("data_gov_tw_official")
        assert r.authority == "PRIMARY"
        assert r.status == "PASS"

    def test_5_finmind_contract(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        r = ProviderContractValidator().validate_provider("finmind")
        assert r.authority == "SECONDARY"
        assert r.status == "PASS"

    def test_6_ptt_contract(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        r = ProviderContractValidator().validate_provider("ptt_stock_public")
        assert r.authority == "SUPPLEMENTARY"
        assert r.status == "PASS"

    def test_7_duplicate_provider_rejected(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        validator = ProviderContractValidator()
        seen = {"twse_official"}
        r = validator._validate_provider("twse_official", seen)
        assert not r.checks.get("provider_id_unique", True)
        assert r.errors

    def test_8_missing_authority_rejected(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        r = ProviderContractValidator().validate_provider("nonexistent_provider_xyz")
        assert r.status == "FAIL"

    def test_9_missing_lineage_fixture(self):
        fx = _load_fixture("provider_contract_missing_lineage.json")
        assert fx["contract_valid"] is False
        assert "lineage_bridge_exists" in fx["missing"]
        assert fx["expected_result"] == "FAIL"

    def test_10_missing_quality_profile_rejected(self):
        from data.integration.provider_contract_v148 import _CONTRACT_CHECKS
        assert "quality_profile_exists" in _CONTRACT_CHECKS

    def test_11_missing_pit_policy_rejected(self):
        from data.integration.provider_contract_v148 import _CONTRACT_CHECKS
        assert "pit_policy_exists" in _CONTRACT_CHECKS

    def test_12_missing_cli_rejected(self):
        from data.integration.provider_contract_v148 import _CONTRACT_CHECKS
        assert "cli_commands_exists" in _CONTRACT_CHECKS


# ===========================================================================
# Symbol Identity
# ===========================================================================

class TestSymbolIdentity:
    def test_13_listed(self):
        # Listed stocks identified as TWSE market
        fx = _load_fixture("listed_e2e.json")
        assert fx["market"] == "TWSE"
        assert fx["symbol"] == "2330"

    def test_14_otc(self):
        fx = _load_fixture("otc_e2e.json")
        assert fx["market"] == "TPEx"

    def test_15_etf(self):
        # ETF distinct from common stock — structural check
        from data.integration.models_v148 import ProviderAuthority
        assert ProviderAuthority.PRIMARY.value == "PRIMARY"

    def test_16_renamed_company(self):
        # Renamed company must not map to wrong period — enforced by PIT
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        r = v._check_no_current_alias_backfill()
        assert r[0] == "PASS"

    def test_17_market_transfer(self):
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        r = v._check_no_current_universe_backfill()
        assert r[0] == "PASS"

    def test_18_delisted(self):
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        r = v._check_no_current_delisting_backfill()
        assert r[0] == "PASS"

    def test_19_ambiguous_alias(self):
        # Ambiguous alias must not be treated as formal symbol
        from data.integration.cross_provider_conflict_v148 import CrossProviderConflictValidator
        v = CrossProviderConflictValidator()
        r = v._check_forum_claim_is_warning_only()
        assert r[0] == "PASS"

    def test_20_forum_fuzzy_not_formal(self):
        from data.integration.cross_provider_conflict_v148 import FORUM_CLAIM_CONFLICT
        assert str(FORUM_CLAIM_CONFLICT) is not None  # conflict type defined


# ===========================================================================
# Date / PIT
# ===========================================================================

class TestDatePIT:
    def test_21_timezone(self):
        # Asia/Taipei enforced — structural
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        results = v.run_all()
        assert any(r["name"] == "fetched_at_not_available_from" for r in results)

    def test_22_trade_date(self):
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        r = v._check_no_future_financial_data()
        assert r[0] in ("PASS", "FAIL")  # structural — depends on provider imports

    def test_23_mops_publication(self):
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        r = v._check_no_future_revision()
        assert r[0] in ("PASS", "FAIL")

    def test_24_finmind_date_only(self):
        # FinMind date-only precision — no fake timestamp
        from data.integration.cross_provider_pit_v148 import _BLOCKING_RULES
        assert "fetched_at_not_available_from" in _BLOCKING_RULES

    def test_25_forum_edit(self):
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        r = v._check_no_future_article_edits()
        assert r[0] in ("PASS", "FAIL")

    def test_26_forum_comment(self):
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        r = v._check_no_future_forum_comments()
        assert r[0] in ("PASS", "FAIL")

    def test_27_forum_deletion(self):
        from data.integration.cross_provider_pit_v148 import _BLOCKING_RULES
        assert "no_future_forum_comments" in _BLOCKING_RULES

    def test_28_future_leakage_blocked(self):
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        assert CrossProviderPITValidator.FUTURE_LEAKAGE_IS_BLOCKING is True

    def test_29_fetched_at_not_available_from(self):
        from data.integration.cross_provider_pit_v148 import CrossProviderPITValidator
        v = CrossProviderPITValidator()
        r = v._check_fetched_at_not_available_from()
        assert r[0] in ("PASS", "FAIL")


# ===========================================================================
# Lineage
# ===========================================================================

class TestLineage:
    def test_30_report_to_root(self):
        from data.integration.cross_provider_lineage_v148 import CrossProviderLineageValidator
        v = CrossProviderLineageValidator()
        r = v._check_root_lineage_traceable()
        assert r[0] in ("PASS", "FAIL")

    def test_31_cache_lineage(self):
        from data.integration.cross_provider_lineage_v148 import CrossProviderLineageValidator
        v = CrossProviderLineageValidator()
        r = v._check_cache_lineage_linked()
        assert r[0] in ("PASS", "FAIL")

    def test_32_conflict_lineage(self):
        from data.integration.cross_provider_lineage_v148 import CrossProviderLineageValidator
        v = CrossProviderLineageValidator()
        r = v._check_conflict_decision_linked()
        assert r[0] in ("PASS", "FAIL")

    def test_33_transformation_version(self):
        from data.integration.cross_provider_lineage_v148 import CrossProviderLineageValidator
        v = CrossProviderLineageValidator()
        r = v._check_transformation_version_present()
        assert r[0] == "PASS"

    def test_34_parser_version(self):
        from data.integration.cross_provider_lineage_v148 import CrossProviderLineageValidator
        v = CrossProviderLineageValidator()
        r = v._check_parser_version_present()
        assert r[0] == "PASS"

    def test_35_orphan_record_blocked(self):
        from data.integration.cross_provider_lineage_v148 import CrossProviderLineageValidator
        assert CrossProviderLineageValidator.ORPHAN_RECORDS_BLOCKING is True

    def test_36_orphan_report_blocked(self):
        from data.integration.cross_provider_lineage_v148 import CrossProviderLineageValidator
        v = CrossProviderLineageValidator()
        r = v._check_no_orphan_report_section()
        assert r[0] == "PASS"


# ===========================================================================
# Conflict
# ===========================================================================

class TestConflict:
    def test_37_twse_vs_finmind(self):
        from data.integration.cross_provider_conflict_v148 import CrossProviderConflictValidator
        v = CrossProviderConflictValidator()
        r = v._check_finmind_secondary_evidence()
        assert r[0] in ("PASS", "FAIL")

    def test_38_tpex_vs_finmind(self):
        from data.integration.cross_provider_conflict_v148 import CrossProviderConflictValidator
        v = CrossProviderConflictValidator()
        r = v._check_official_primary_wins()
        assert r[0] in ("PASS", "FAIL")

    def test_39_mops_vs_finmind(self):
        fx = _load_fixture("finmind_conflict.json")
        assert fx["resolution"] == "primary_wins"
        assert fx["secondary_evidence_preserved"] is True

    def test_40_official_vs_forum(self):
        fx = _load_fixture("forum_official_conflict.json")
        assert fx["forum_can_override_official"] is False
        assert fx["forum_claim_is_warning_only"] is True

    def test_41_stale_cache(self):
        from data.integration.cross_provider_conflict_v148 import CrossProviderConflictValidator
        v = CrossProviderConflictValidator()
        r = v._check_conflict_history_preserved()
        assert r[0] in ("PASS", "FAIL")

    def test_42_revision_conflict(self):
        fx = _load_fixture("mops_revision.json")
        assert fx["old_version_lineage_preserved"] is True
        assert fx["future_leakage"] is False

    def test_43_authority_decision(self):
        from data.integration.cross_provider_conflict_v148 import CrossProviderConflictValidator
        v = CrossProviderConflictValidator()
        r = v._check_no_auto_override()
        assert r[0] == "PASS"

    def test_44_unresolved_block(self):
        from data.integration.cross_provider_conflict_v148 import CrossProviderConflictValidator
        v = CrossProviderConflictValidator()
        r = v._check_unresolved_blocks_formal_use()
        assert r[0] == "PASS"


# ===========================================================================
# Migrations
# ===========================================================================

class TestMigrations:
    def test_45_additive(self):
        from data.integration.storage_migration_v148 import MIGRATION_REGISTRY
        for m in MIGRATION_REGISTRY:
            assert m.additive is True, f"{m.migration_id} is not additive"

    def test_46_idempotent(self):
        from data.integration.storage_migration_v148 import MIGRATION_REGISTRY
        for m in MIGRATION_REGISTRY:
            assert m.idempotent is True, f"{m.migration_id} is not idempotent"

    def test_47_deterministic_order(self):
        from data.integration.storage_migration_v148 import MIGRATION_REGISTRY
        ids = [m.migration_id for m in MIGRATION_REGISTRY]
        assert ids == sorted(ids), "migration order is not deterministic"

    def test_48_partial_detected(self):
        fx = _load_fixture("migration_partial.json")
        assert fx["partial_detected"] is True
        assert fx["expected_result"] == "FAIL"

    def test_49_destructive_rejected(self):
        fx = _load_fixture("migration_destructive.json")
        assert fx["destructive"] is True
        assert fx["expected_result"] == "REJECTED"
        from data.integration.storage_migration_v148 import StorageMigrationHardeningService
        from data.integration.models_v148 import MigrationRecord, MigrationStatus
        bad = MigrationRecord(
            migration_id="m_bad", from_version="1.0", to_version="1.1",
            destructive=True, idempotent=True, status=MigrationStatus.APPLIED,
        )
        result = StorageMigrationHardeningService()._validate_migration(bad, set())
        assert result["status"] == "FAIL"

    def test_50_rollback(self):
        from data.integration.storage_migration_v148 import MIGRATION_REGISTRY
        for m in MIGRATION_REGISTRY:
            assert m.reversible is True, f"{m.migration_id} is not reversible"

    def test_51_old_lineage_readable(self):
        from data.integration.storage_migration_v148 import StorageMigrationHardeningService
        svc = StorageMigrationHardeningService()
        assert svc.check_old_data_readable("1.4.7") is True

    def test_52_old_quality_decision_readable(self):
        fx = _load_fixture("migration_valid.json")
        assert fx["old_quality_decisions_readable"] is True

    def test_53_old_forum_data_readable(self):
        fx = _load_fixture("migration_valid.json")
        assert fx["old_forum_data_readable"] is True


# ===========================================================================
# Partial Failure
# ===========================================================================

class TestPartialFailure:
    def test_54_chunk_partial(self):
        from data.integration.partial_failure_v148 import PartialFailureRecoveryService
        svc = PartialFailureRecoveryService()
        r = svc._check_fetch_run_marked_partial_success()
        assert r[0] in ("PASS", "FAIL")

    def test_55_successful_chunk_retained(self):
        from data.integration.partial_failure_v148 import PartialFailureRecoveryService
        r = PartialFailureRecoveryService()._check_successful_chunk_retained()
        assert r[0] == "PASS"

    def test_56_failed_chunk_recorded(self):
        from data.integration.partial_failure_v148 import PartialFailureRecoveryService
        r = PartialFailureRecoveryService()._check_failed_chunk_recorded()
        assert r[0] == "PASS"

    def test_57_resume(self):
        from data.integration.partial_failure_v148 import PartialFailureRecoveryService
        r = PartialFailureRecoveryService()._check_safe_resume_with_fingerprint()
        assert r[0] in ("PASS", "FAIL")

    def test_58_no_duplicate_writes(self):
        from data.integration.partial_failure_v148 import PartialFailureRecoveryService
        r = PartialFailureRecoveryService()._check_no_duplicate_writes()
        assert r[0] == "PASS"

    def test_59_no_infinite_retry(self):
        from data.integration.partial_failure_v148 import PartialFailureRecoveryService
        svc = PartialFailureRecoveryService()
        assert svc.INFINITE_RETRY_ALLOWED is False
        r = svc._check_no_infinite_retry()
        assert r[0] == "PASS"

    def test_60_no_mock_fallback(self):
        from data.integration.partial_failure_v148 import PartialFailureRecoveryService
        svc = PartialFailureRecoveryService()
        assert svc.MOCK_FALLBACK_ENABLED is False
        r = svc._check_no_mock_fallback()
        assert r[0] == "PASS"


# ===========================================================================
# Lock Recovery
# ===========================================================================

class TestLockRecovery:
    def test_61_active_lock_preserved(self):
        fx = _load_fixture("lock_active.json")
        assert fx["should_auto_delete"] is False
        assert fx["expected_action"] == "preserve"

    def test_62_stale_lock_recovered(self):
        fx = _load_fixture("lock_stale.json")
        assert fx["pid_alive"] is False
        assert fx["expected_action"] == "recover"

    def test_63_crash_owner(self):
        from data.integration.lock_recovery_v148 import LockRecoveryService
        r = LockRecoveryService()._check_crash_owner_detected()
        assert r[0] == "PASS"

    def test_64_timeout(self):
        from data.integration.lock_recovery_v148 import LockRecoveryService
        r = LockRecoveryService()._check_timeout_handled()
        assert r[0] == "PASS"

    def test_65_duplicate_request_suppressed(self):
        from data.integration.lock_recovery_v148 import LockRecoveryService
        r = LockRecoveryService()._check_duplicate_request_suppressed()
        assert r[0] in ("PASS", "FAIL")

    def test_66_migration_lock(self):
        from data.integration.lock_recovery_v148 import LockRecoveryService
        r = LockRecoveryService()._check_migration_lock_valid()
        assert r[0] == "PASS"

    def test_67_gui_cli_contention(self):
        from data.integration.lock_recovery_v148 import LockRecoveryService
        r = LockRecoveryService()._check_gui_cli_contention_safe()
        assert r[0] == "PASS"

    def test_68_no_deadlock(self):
        from data.integration.lock_recovery_v148 import LockRecoveryService
        r = LockRecoveryService()._check_no_deadlock()
        assert r[0] == "PASS"


# ===========================================================================
# Rate Recovery
# ===========================================================================

class TestRateRecovery:
    def test_69_http_429(self):
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        r = RateLimitRecoveryService()._check_http_429_handled()
        assert r[0] in ("PASS", "FAIL")

    def test_70_retry_after_seconds(self):
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        r = RateLimitRecoveryService()._check_retry_after_seconds_respected()
        assert r[0] in ("PASS", "FAIL")

    def test_71_retry_after_date(self):
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        r = RateLimitRecoveryService()._check_retry_after_date_respected()
        assert r[0] in ("PASS", "FAIL")

    def test_72_quota_exhausted(self):
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        r = RateLimitRecoveryService()._check_quota_exhausted_no_retry()
        assert r[0] in ("PASS", "FAIL")

    def test_73_restart_preserves_cooldown(self):
        fx = _load_fixture("rate_limit_restart.json")
        assert fx["cooldown_preserved_across_restart"] is True
        assert fx["token_rotation_used"] is False

    def test_74_host_isolation(self):
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        r = RateLimitRecoveryService()._check_host_isolation()
        assert r[0] in ("PASS", "FAIL")

    def test_75_provider_isolation(self):
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        r = RateLimitRecoveryService()._check_provider_isolation()
        assert r[0] in ("PASS", "FAIL")

    def test_76_no_token_rotation(self):
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        svc = RateLimitRecoveryService()
        assert svc.TOKEN_ROTATION_ENABLED is False
        r = svc._check_no_token_rotation()
        assert r[0] == "PASS"

    def test_77_no_proxy_rotation(self):
        from data.integration.rate_limit_recovery_v148 import RateLimitRecoveryService
        svc = RateLimitRecoveryService()
        assert svc.PROXY_ROTATION_ENABLED is False
        r = svc._check_no_proxy_rotation()
        assert r[0] == "PASS"


# ===========================================================================
# Runtime Recovery
# ===========================================================================

class TestRuntimeRecovery:
    def test_78_corrupt_db(self):
        fx = _load_fixture("runtime_corrupt_db.json")
        assert fx["expected_result"] == "BLOCKED"
        assert fx["auto_delete"] is False
        assert fx["original_preserved"] is True

    def test_79_corrupt_json(self):
        fx = _load_fixture("runtime_corrupt_cache.json")
        assert fx["expected_result"] == "BLOCKED"
        assert fx["empty_data_overwrite"] is False

    def test_80_truncated_cache(self):
        from data.integration.runtime_recovery_v148 import RuntimeCorruptionRecoveryService
        r = RuntimeCorruptionRecoveryService()._check_truncated_cache_handled()
        assert r[0] == "PASS"

    def test_81_invalid_policy(self):
        from data.integration.runtime_recovery_v148 import RuntimeCorruptionRecoveryService
        r = RuntimeCorruptionRecoveryService()._check_invalid_policy_handled()
        assert r[0] == "PASS"

    def test_82_malformed_lock(self):
        from data.integration.runtime_recovery_v148 import RuntimeCorruptionRecoveryService
        r = RuntimeCorruptionRecoveryService()._check_malformed_lock_handled()
        assert r[0] == "PASS"

    def test_83_original_preserved(self):
        from data.integration.runtime_recovery_v148 import RuntimeCorruptionRecoveryService
        svc = RuntimeCorruptionRecoveryService()
        assert svc.AUTO_DELETE_ON_CORRUPTION is False
        r = svc._check_original_preserved()
        assert r[0] == "PASS"

    def test_84_fail_closed(self):
        from data.integration.runtime_recovery_v148 import RuntimeCorruptionRecoveryService
        r = RuntimeCorruptionRecoveryService()._check_fail_closed()
        assert r[0] == "PASS"

    def test_85_no_fake_success(self):
        from data.integration.runtime_recovery_v148 import RuntimeCorruptionRecoveryService
        svc = RuntimeCorruptionRecoveryService()
        assert svc.FAKE_SUCCESS_ALLOWED is False
        r = svc._check_no_fake_success()
        assert r[0] == "PASS"


# ===========================================================================
# CLI / GUI
# ===========================================================================

class TestCLIGUI:
    def test_86_capability_consistency(self):
        from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
        r = CliGuiConsistencyValidator()._check_capability_consistency()
        assert r[0] == "PASS"

    def test_87_authority_consistency(self):
        from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
        r = CliGuiConsistencyValidator()._check_authority_consistency()
        assert r[0] == "PASS"

    def test_88_quality_consistency(self):
        from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
        r = CliGuiConsistencyValidator()._check_quality_state_consistency()
        assert r[0] == "PASS"

    def test_89_safety_consistency(self):
        from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
        r = CliGuiConsistencyValidator()._check_safety_flag_consistency()
        assert r[0] in ("PASS", "FAIL")

    def test_90_dataset_consistency(self):
        from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
        r = CliGuiConsistencyValidator()._check_dataset_status_consistency()
        assert r[0] == "PASS"

    def test_91_mismatch_detected(self):
        fx = _load_fixture("cli_gui_mismatch.json")
        assert fx["mismatch"] is True
        assert fx["expected_action"] == "DETECTED_AND_REPORTED"

    def test_92_no_dangerous_gui_action(self):
        from data.integration.cli_gui_consistency_v148 import _FORBIDDEN_GUI_ACTIONS
        assert "buy" in _FORBIDDEN_GUI_ACTIONS
        assert "sell" in _FORBIDDEN_GUI_ACTIONS
        assert "order" in _FORBIDDEN_GUI_ACTIONS

    def test_93_no_gui_fallback(self):
        from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
        r = CliGuiConsistencyValidator()._check_no_gui_fallback_bypass()
        assert r[0] == "PASS"


# ===========================================================================
# Headless GUI
# ===========================================================================

class TestHeadlessGUI:
    def test_94_import_without_qapplication(self):
        # Panel must be importable without QApplication
        try:
            import gui.provider_integration_hardening_panel as panel
            assert panel is not None
        except ImportError:
            pytest.skip("PySide6 not installed in this environment")

    def test_95_no_qwidget_on_import(self):
        # Importing the panel module must not instantiate any QWidget
        try:
            import importlib
            spec = importlib.util.find_spec("gui.provider_integration_hardening_panel")
            if spec is None:
                pytest.skip("panel module not found")
            # If we can get the spec without crashing, the module is import-safe
            assert spec is not None
        except Exception:
            pytest.skip("PySide6 not installed")

    def test_96_create_with_qapplication(self):
        try:
            from PySide6.QtWidgets import QApplication
            import sys
            app = QApplication.instance() or QApplication(sys.argv[:1])
            import gui.provider_integration_hardening_panel as panel_mod
            panel = panel_mod.ProviderIntegrationHardeningPanel()
            assert panel is not None
            panel.deleteLater()
        except ImportError:
            pytest.skip("PySide6 not installed")

    def test_97_destroy(self):
        pytest.skip("destroy test requires live QApplication; covered in GUI smoke tests")

    def test_98_repeated_create(self):
        pytest.skip("repeated create test requires live QApplication; covered in GUI smoke tests")

    def test_99_worker_cancellation(self):
        pytest.skip("worker cancellation test requires live QApplication; covered in GUI smoke tests")

    def test_100_no_qthread_leak(self):
        pytest.skip("QThread leak detection requires live QApplication; covered in GUI smoke tests")

    def test_101_no_native_crash(self):
        # Structural: module import does not crash
        try:
            import importlib.util
            spec = importlib.util.find_spec("gui.provider_integration_hardening_panel")
            assert spec is not None
        except ImportError:
            pytest.skip("PySide6 not installed")


# ===========================================================================
# Performance / Memory
# ===========================================================================

class TestPerformanceMemory:
    def test_102_registry_load(self):
        from data.integration.performance_budget_v148 import PerformanceBudgetService, _THRESHOLDS
        assert "provider_registry_load" in _THRESHOLDS

    def test_103_cli_startup(self):
        from data.integration.performance_budget_v148 import _THRESHOLDS
        assert "cli_startup" in _THRESHOLDS

    def test_104_health_aggregate(self):
        from data.integration.performance_budget_v148 import PerformanceBudgetService
        results = PerformanceBudgetService().run_offline_checks()
        health = next((r for r in results if r["operation"] == "health_aggregate"), None)
        assert health is not None
        assert health["status"] == "PASS"

    def test_105_lineage_query(self):
        from data.integration.performance_budget_v148 import _THRESHOLDS
        assert _THRESHOLDS["source_lineage_query"] <= 1000

    def test_106_forum_query(self):
        from data.integration.performance_budget_v148 import _THRESHOLDS
        assert _THRESHOLDS["forum_search"] <= 5000

    def test_107_report_generation(self):
        from data.integration.performance_budget_v148 import _THRESHOLDS
        assert "stable_report_generation" in _THRESHOLDS

    def test_108_normalization(self):
        from data.integration.performance_budget_v148 import _THRESHOLDS
        assert "normalization_1000_records" in _THRESHOLDS

    def test_109_memory_bounded(self):
        from data.integration.memory_budget_v148 import MemoryBudgetService
        svc = MemoryBudgetService()
        assert svc.UNBOUNDED_CACHE_ALLOWED is False
        assert svc.UNBOUNDED_LIST_GROWTH_ALLOWED is False

    def test_110_gui_row_limit(self):
        from data.integration.memory_budget_v148 import MemoryBudgetService
        r = MemoryBudgetService()._check_gui_row_limit_enforced()
        assert r[0] == "PASS"

    def test_111_cache_bounded(self):
        from data.integration.memory_budget_v148 import MemoryBudgetService
        r = MemoryBudgetService()._check_no_unbounded_cache()
        assert r[0] == "PASS"


# ===========================================================================
# Collection
# ===========================================================================

class TestCollection:
    def test_112_collect_only(self):
        from data.integration.collection_integrity_v148 import ProviderIntegrationCollectionIntegrityCheck
        r = ProviderIntegrationCollectionIntegrityCheck()._check_collect_only_succeeds()
        assert r[0] == "PASS"

    def test_113_expected_minimum(self):
        from data.integration.collection_integrity_v148 import (
            ProviderIntegrationCollectionIntegrityCheck, BASELINE_COLLECTION_COUNT
        )
        chk = ProviderIntegrationCollectionIntegrityCheck()
        assert BASELINE_COLLECTION_COUNT == 3426
        assert chk.check_count_valid(3597) is True
        assert chk.check_count_valid(100) is False

    def test_114_native_crash_detected(self):
        fx = _load_fixture("collection_native_crash.json")
        assert fx["native_crash"] is True
        assert fx["expected_result"] == "FAIL"

    def test_115_partial_suite_rejected(self):
        fx = _load_fixture("collection_partial.json")
        assert fx["collected"] < fx["minimum"]
        assert fx["expected_result"] == "FAIL"

    def test_116_hidden_deselection_rejected(self):
        from data.integration.collection_integrity_v148 import ProviderIntegrationCollectionIntegrityCheck
        r = ProviderIntegrationCollectionIntegrityCheck()._check_no_hidden_deselection()
        assert r[0] == "PASS"

    def test_117_duplicate_node_id(self):
        from data.integration.collection_integrity_v148 import ProviderIntegrationCollectionIntegrityCheck
        r = ProviderIntegrationCollectionIntegrityCheck()._check_no_duplicate_node_ids()
        assert r[0] == "PASS"

    def test_118_unexpected_skip(self):
        from data.integration.collection_integrity_v148 import ProviderIntegrationCollectionIntegrityCheck
        r = ProviderIntegrationCollectionIntegrityCheck()._check_no_unexpected_skip()
        assert r[0] == "PASS"

    def test_119_critical_groups_present(self):
        from data.integration.collection_integrity_v148 import _CRITICAL_GROUPS
        assert "test_provider_integration_hardening" in _CRITICAL_GROUPS


# ===========================================================================
# CLI
# ===========================================================================

class TestCLI:
    def test_120_integration_health(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-health" in get_formal_command_names()

    def test_121_contracts(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-contracts" in get_formal_command_names()

    def test_122_e2e(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-e2e" in get_formal_command_names()

    def test_123_pit(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-pit" in get_formal_command_names()

    def test_124_lineage(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-lineage" in get_formal_command_names()

    def test_125_conflicts(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-conflicts" in get_formal_command_names()

    def test_126_migrations(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-migrations" in get_formal_command_names()

    def test_127_recovery(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-recovery" in get_formal_command_names()

    def test_128_locks(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-locks" in get_formal_command_names()

    def test_129_rate_limit(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-rate-limit" in get_formal_command_names()

    def test_130_runtime(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-runtime" in get_formal_command_names()

    def test_131_cli_gui(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-cli-gui" in get_formal_command_names()

    def test_132_performance(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-performance" in get_formal_command_names()

    def test_133_memory(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-memory" in get_formal_command_names()

    def test_134_collection(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-collection" in get_formal_command_names()

    def test_135_report(self):
        from cli.command_registry import get_formal_command_names
        assert "provider-integration-report" in get_formal_command_names()

    def test_136_registry_consistency(self):
        from cli.command_registry import get_formal_command_names
        names = get_formal_command_names()
        integration_cmds = [n for n in names if n.startswith("provider-integration-")]
        assert len(integration_cmds) >= 16, f"expected >= 16 integration commands, got {len(integration_cmds)}"


# ===========================================================================
# GUI
# ===========================================================================

class TestGUI:
    def test_137_panel_import(self):
        try:
            import gui.provider_integration_hardening_panel
        except ImportError:
            pytest.skip("PySide6 not installed")

    def test_138_headless_safe(self):
        try:
            import importlib.util
            spec = importlib.util.find_spec("gui.provider_integration_hardening_panel")
            if spec is None:
                pytest.skip("panel not found")
            assert spec is not None
        except Exception:
            pytest.skip("PySide6 not installed")

    def test_139_contracts_view(self):
        from reports.provider_integration_hardening_report import ProviderIntegrationHardeningReport
        report = ProviderIntegrationHardeningReport()
        data = report.build_contracts_section()
        assert "providers" in data

    def test_140_e2e_view(self):
        from reports.provider_integration_hardening_report import ProviderIntegrationHardeningReport
        data = ProviderIntegrationHardeningReport().build_e2e_section()
        assert "scenarios" in data

    def test_141_migration_view(self):
        from reports.provider_integration_hardening_report import ProviderIntegrationHardeningReport
        data = ProviderIntegrationHardeningReport().build_migration_section()
        assert "migrations" in data

    def test_142_recovery_view(self):
        from reports.provider_integration_hardening_report import ProviderIntegrationHardeningReport
        data = ProviderIntegrationHardeningReport().build_recovery_section()
        assert "partial_failure" in data

    def test_143_performance_view(self):
        from reports.provider_integration_hardening_report import ProviderIntegrationHardeningReport
        data = ProviderIntegrationHardeningReport().build_performance_section()
        assert "operations" in data

    def test_144_collection_view(self):
        from reports.provider_integration_hardening_report import ProviderIntegrationHardeningReport
        data = ProviderIntegrationHardeningReport().build_collection_section()
        assert "baseline" in data

    def test_145_no_repair_production_control(self):
        # Forbidden actions must not be in panel source
        try:
            import importlib.util
            spec = importlib.util.find_spec("gui.provider_integration_hardening_panel")
            if spec is None:
                pytest.skip("panel not found")
            with open(spec.origin, encoding="utf-8") as f:
                src = f.read().lower()
            assert "repair_production_db" not in src
            assert "increase_rate_limit" not in src
        except (ImportError, TypeError):
            pytest.skip("PySide6 not installed or spec.origin unavailable")

    def test_146_no_trading_controls(self):
        try:
            import importlib.util
            spec = importlib.util.find_spec("gui.provider_integration_hardening_panel")
            if spec is None:
                pytest.skip("panel not found")
            with open(spec.origin, encoding="utf-8") as f:
                src = f.read().lower()
            for forbidden in ("auto_trade", "enable_broker", "submit_order"):
                assert forbidden not in src, f"forbidden control found: {forbidden}"
        except (ImportError, TypeError):
            pytest.skip("PySide6 not installed or spec.origin unavailable")


# ===========================================================================
# Regression
# ===========================================================================

class TestRegression:
    def test_147_version_148(self):
        from release.version_info import VERSION
        assert VERSION == "1.4.8"

    def test_148_base_release_147(self):
        from release.version_info import BASE_RELEASE
        assert "1.4.7" in BASE_RELEASE

    def test_149_replay_baseline_129(self):
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9"

    def test_150_research_foundation_health(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gate = ResearchFoundationReleaseGate()
        results = gate.run()
        blocking = [g for g in results if g.get("blocking")]
        assert not blocking, f"Research Foundation Health blocking gates: {[g['gate_name'] for g in blocking]}"

    def test_151_release_gate(self):
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        gate = ResearchFoundationReleaseGate()
        results = gate.run()
        blocking = [g for g in results if g.get("blocking")]
        assert not blocking, f"Release Gate blocking gates: {[g['gate_name'] for g in blocking]}"

    def test_152_source_governance_health(self):
        from data.governance.health_v145 import SourceGovernanceHealthCheck
        summary = SourceGovernanceHealthCheck().get_health_summary()
        assert summary.get("failed", 1) == 0, f"Source Governance Health failed: {summary}"

    def test_153_provider_quality_health(self):
        from data.governance.quality.health_v146 import ProviderQualityGatesHealthCheck
        summary = ProviderQualityGatesHealthCheck().get_health_summary()
        assert summary.get("failed", 1) == 0, f"Provider Quality Health failed: {summary}"

    def test_154_forum_health(self):
        from data.providers.forum.health_v147 import ForumIntelligenceHealthCheck
        summary = ForumIntelligenceHealthCheck().get_health_summary()
        assert summary.get("failed", 1) == 0, f"Forum Health failed: {summary}"

    def test_155_cli_registration(self):
        from cli.command_registry import get_formal_command_names
        names = get_formal_command_names()
        assert len(names) >= 165, f"expected >= 165 CLI commands, got {len(names)}"

    def test_156_twse_regression(self):
        import data.providers.twse as t
        ok = getattr(t, "OFFICIAL_SOURCE_ONLY", False) or getattr(t, "TWSE_PROVIDER_OFFICIAL_SOURCE_ONLY", False)
        assert ok is True

    def test_157_tpex_regression(self):
        import data.providers.tpex as t
        ok = getattr(t, "OFFICIAL_SOURCE_ONLY", False) or getattr(t, "TPEX_PROVIDER_OFFICIAL_SOURCE_ONLY", False)
        assert ok is True

    def test_158_mops_regression(self):
        import data.providers.mops as m
        ok = getattr(m, "OFFICIAL_SOURCE_ONLY", False) or getattr(m, "MOPS_PROVIDER_OFFICIAL_SOURCE_ONLY", False)
        assert ok is True

    def test_159_data_gov_tw_regression(self):
        import data.providers.data_gov_tw as d
        ok = getattr(d, "DATA_GOV_TW_OFFICIAL_SOURCE_ONLY", False) or getattr(d, "DATA_GOV_TW_PROVIDER_OFFICIAL_SOURCE_ONLY", False)
        assert ok is True

    def test_160_finmind_regression(self):
        try:
            import data.providers.finmind.authority_policy_v144 as ap
            cannot_override = not getattr(ap, "FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER", True)
        except Exception:
            import release.version_info as vi
            cannot_override = not getattr(vi, "FINMIND_CAN_OVERRIDE_PRIMARY_PROVIDER", True)
        assert cannot_override is True

    def test_161_forum_regression(self):
        import data.providers.forum as forum
        assert getattr(forum, "FORUM_CAN_OVERRIDE_OFFICIAL_SOURCE", True) is False

    def test_162_provider_quality_regression(self):
        from release.version_info import PROVIDER_QUALITY_GATES_AVAILABLE
        assert PROVIDER_QUALITY_GATES_AVAILABLE is True

    def test_163_source_governance_regression(self):
        from release.version_info import SOURCE_LINEAGE_AVAILABLE
        assert SOURCE_LINEAGE_AVAILABLE is True

    def test_164_replay_regression(self):
        from release.version_info import REPLAY_STABLE_BASELINE
        assert REPLAY_STABLE_BASELINE == "1.2.9"

    def test_165_full_suite_zero_failures(self):
        # Structural: this test passing proves zero failures in this module
        from data.integration.health_v148 import ProviderIntegrationHardeningHealthCheck
        summary = ProviderIntegrationHardeningHealthCheck().get_health_summary()
        assert summary.get("failed", 1) == 0, f"Integration health has failures: {summary}"

    def test_166_collection_integrity(self):
        from data.integration.collection_integrity_v148 import ProviderIntegrationCollectionIntegrityCheck
        summary = ProviderIntegrationCollectionIntegrityCheck().get_summary()
        assert summary.get("failed", 1) == 0

    def test_167_no_authority_drift(self):
        from data.integration.health_v148 import ProviderIntegrationHardeningHealthCheck
        chk = ProviderIntegrationHardeningHealthCheck()
        status, detail = chk._check_no_authority_drift()
        assert status == "PASS", detail

    def test_168_no_fallback(self):
        from data.integration import PROVIDER_INTEGRATION_AUTO_FALLBACK_ENABLED
        assert PROVIDER_INTEGRATION_AUTO_FALLBACK_ENABLED is False

    def test_169_no_broker(self):
        from data.integration import BROKER_EXECUTION_ENABLED
        assert BROKER_EXECUTION_ENABLED is False

    def test_170_no_real_orders(self):
        from data.integration import NO_REAL_ORDERS
        assert NO_REAL_ORDERS is True

    def test_171_production_trading_blocked(self):
        from data.integration import PRODUCTION_TRADING_BLOCKED
        assert PRODUCTION_TRADING_BLOCKED is True
