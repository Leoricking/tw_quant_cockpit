"""
gui/provider_integration_hardening_panel.py — Provider Integration Hardening Panel v1.4.8.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No silent fallback. No mock fallback. No auto repair. No dangerous actions.

Navigation:
  tab_id      = provider_integration_hardening
  display_name = Provider Integration Hardening
  group       = data
  priority    = P1
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_PANEL_VERSION = "1.4.8"
_SAFETY_FLAGS = {
    "cross_provider_stability_verification": True,
    "primary_authority_preserved":            True,
    "no_silent_fallback":                     True,
    "no_mock_fallback":                       True,
    "no_auto_repair":                         True,
    "no_real_orders":                         True,
    "production_trading_blocked":             True,
}


def _is_qt_available() -> bool:
    try:
        from PySide6.QtWidgets import QWidget  # noqa: F401
        return True
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# Headless-safe data model (no Qt dependency)
# ---------------------------------------------------------------------------

class ProviderIntegrationHardeningModel:
    """Pure-Python model; safe to create without QApplication."""

    VERSION = _PANEL_VERSION
    SAFETY_FLAGS = _SAFETY_FLAGS

    def get_contracts(self):
        from data.integration.provider_contract_v148 import ProviderContractValidator
        return ProviderContractValidator().validate_all()

    def get_e2e_results(self):
        from data.integration.cross_provider_e2e_v148 import CrossProviderE2EValidator
        return CrossProviderE2EValidator().run_all()

    def get_migrations(self):
        from data.integration.storage_migration_v148 import StorageMigrationHardeningService
        return StorageMigrationHardeningService().validate_all()

    def get_recovery(self):
        from data.integration.query_v148 import IntegrationQueryService
        return IntegrationQueryService().query_recovery_status()

    def get_cli_gui(self):
        from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
        return CliGuiConsistencyValidator().run_all()

    def get_performance(self):
        from data.integration.performance_budget_v148 import PerformanceBudgetService
        return PerformanceBudgetService().run_offline_checks()

    def get_memory(self):
        from data.integration.memory_budget_v148 import MemoryBudgetService
        return MemoryBudgetService().run_offline_checks()

    def get_collection(self):
        from data.integration.collection_integrity_v148 import ProviderIntegrationCollectionIntegrityCheck
        return ProviderIntegrationCollectionIntegrityCheck().run_all()

    def get_health_summary(self):
        from data.integration.health_v148 import ProviderIntegrationHardeningHealthCheck
        return ProviderIntegrationHardeningHealthCheck().get_health_summary()


# ---------------------------------------------------------------------------
# Qt panel (conditional import)
# ---------------------------------------------------------------------------

if _is_qt_available():
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QTableWidget, QTableWidgetItem, QPushButton,
        QTabWidget, QGroupBox, QScrollArea, QSizePolicy,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from gui.common.safety_banner import make_safety_banner

    class _RefreshWorker(QThread):
        finished = Signal(dict)

        def __init__(self, model: ProviderIntegrationHardeningModel):
            super().__init__()
            self._model = model
            self._cancelled = False

        def cancel(self):
            self._cancelled = True

        def run(self):
            if self._cancelled:
                return
            try:
                summary = self._model.get_health_summary()
                self.finished.emit(summary)
            except Exception as exc:
                self.finished.emit({"error": str(exc)})

    class ProviderIntegrationHardeningPanel(QWidget):
        """Provider Integration Hardening panel (v1.4.8)."""

        PANEL_VERSION = _PANEL_VERSION

        def __init__(self, parent=None):
            super().__init__(parent)
            self._model = ProviderIntegrationHardeningModel()
            self._worker = None
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)

            # Safety banner
            try:
                banner = make_safety_banner(
                    title="Provider Integration Hardening v1.4.8",
                    flags=_SAFETY_FLAGS,
                )
                layout.addWidget(banner)
            except Exception:
                banner_label = QLabel(
                    "[!] Research Only. No Real Orders. Production Trading: BLOCKED.\n"
                    "[!] Primary Authority Preserved. No Silent Fallback. No Mock Fallback.\n"
                    "[!] No Auto Repair. No Dangerous Actions."
                )
                banner_label.setWordWrap(True)
                layout.addWidget(banner_label)

            # Tabs
            self._tabs = QTabWidget()
            layout.addWidget(self._tabs)

            self._tabs.addTab(self._make_contracts_tab(),   "Provider Contracts")
            self._tabs.addTab(self._make_e2e_tab(),         "E2E Scenarios")
            self._tabs.addTab(self._make_migrations_tab(),  "Migrations")
            self._tabs.addTab(self._make_recovery_tab(),    "Recovery")
            self._tabs.addTab(self._make_cli_gui_tab(),     "CLI/GUI")
            self._tabs.addTab(self._make_performance_tab(), "Performance")
            self._tabs.addTab(self._make_memory_tab(),      "Memory")
            self._tabs.addTab(self._make_collection_tab(),  "Collection")

            # Actions toolbar (safe actions only)
            action_bar = QHBoxLayout()
            for label, slot in [
                ("Refresh",              self._on_refresh),
                ("Validate Contracts",   self._on_validate_contracts),
                ("Run Offline E2E",      self._on_run_e2e),
                ("Validate Migrations",  self._on_validate_migrations),
                ("Validate Recovery",    self._on_validate_recovery),
                ("Validate CLI/GUI",     self._on_validate_cli_gui),
                ("Validate Collection",  self._on_validate_collection),
                ("Export Report",        self._on_export_report),
            ]:
                btn = QPushButton(label)
                btn.clicked.connect(slot)
                action_bar.addWidget(btn)
            action_bar.addStretch()
            layout.addLayout(action_bar)

        # --- Tab builders ---

        def _make_contracts_tab(self):
            w = QWidget()
            layout = QVBoxLayout(w)
            self._contracts_table = QTableWidget(0, 6)
            self._contracts_table.setHorizontalHeaderLabels(
                ["Provider", "Authority", "Contract", "Lineage", "Quality", "Status"]
            )
            layout.addWidget(self._contracts_table)
            return w

        def _make_e2e_tab(self):
            w = QWidget()
            layout = QVBoxLayout(w)
            self._e2e_table = QTableWidget(0, 6)
            self._e2e_table.setHorizontalHeaderLabels(
                ["Scenario", "Providers", "PIT", "Lineage", "Conflict", "Result"]
            )
            layout.addWidget(self._e2e_table)
            return w

        def _make_migrations_tab(self):
            w = QWidget()
            layout = QVBoxLayout(w)
            self._migrations_table = QTableWidget(0, 5)
            self._migrations_table.setHorizontalHeaderLabels(
                ["Migration", "From", "To", "Idempotent", "Status"]
            )
            layout.addWidget(self._migrations_table)
            return w

        def _make_recovery_tab(self):
            w = QWidget()
            layout = QVBoxLayout(w)
            self._recovery_table = QTableWidget(0, 5)
            self._recovery_table.setHorizontalHeaderLabels(
                ["Recovery", "Partial Failure", "Lock", "Rate Limit", "Corruption"]
            )
            layout.addWidget(self._recovery_table)
            return w

        def _make_cli_gui_tab(self):
            w = QWidget()
            layout = QVBoxLayout(w)
            self._cli_gui_table = QTableWidget(0, 4)
            self._cli_gui_table.setHorizontalHeaderLabels(
                ["Capability", "CLI", "GUI", "Mismatch"]
            )
            layout.addWidget(self._cli_gui_table)
            return w

        def _make_performance_tab(self):
            w = QWidget()
            layout = QVBoxLayout(w)
            self._perf_table = QTableWidget(0, 4)
            self._perf_table.setHorizontalHeaderLabels(
                ["Operation", "Baseline (ms)", "Current", "Status"]
            )
            layout.addWidget(self._perf_table)
            return w

        def _make_memory_tab(self):
            w = QWidget()
            layout = QVBoxLayout(w)
            self._mem_table = QTableWidget(0, 4)
            self._mem_table.setHorizontalHeaderLabels(
                ["Operation", "Peak (MB)", "Threshold (MB)", "Status"]
            )
            layout.addWidget(self._mem_table)
            return w

        def _make_collection_tab(self):
            w = QWidget()
            layout = QVBoxLayout(w)
            self._collection_table = QTableWidget(0, 5)
            self._collection_table.setHorizontalHeaderLabels(
                ["Check", "Collected", "Minimum", "Crash", "Status"]
            )
            layout.addWidget(self._collection_table)
            return w

        # --- Action handlers (read-only / dry-run / offline) ---

        def _on_refresh(self):
            if self._worker and self._worker.isRunning():
                return
            self._worker = _RefreshWorker(self._model)
            self._worker.finished.connect(self._on_refresh_done)
            self._worker.start()

        def _on_refresh_done(self, summary: dict):
            logger.info("Provider Integration panel refreshed: overall=%s", summary.get("overall"))

        def _on_validate_contracts(self):
            from data.integration.provider_contract_v148 import ProviderContractValidator
            ProviderContractValidator().validate_all()

        def _on_run_e2e(self):
            from data.integration.cross_provider_e2e_v148 import CrossProviderE2EValidator
            CrossProviderE2EValidator().run_all()

        def _on_validate_migrations(self):
            from data.integration.storage_migration_v148 import StorageMigrationHardeningService
            StorageMigrationHardeningService().validate_all()

        def _on_validate_recovery(self):
            from data.integration.query_v148 import IntegrationQueryService
            IntegrationQueryService().query_recovery_status()

        def _on_validate_cli_gui(self):
            from data.integration.cli_gui_consistency_v148 import CliGuiConsistencyValidator
            CliGuiConsistencyValidator().run_all()

        def _on_validate_collection(self):
            from data.integration.collection_integrity_v148 import ProviderIntegrationCollectionIntegrityCheck
            ProviderIntegrationCollectionIntegrityCheck().run_all()

        def _on_export_report(self):
            from reports.provider_integration_hardening_report import ProviderIntegrationHardeningReport
            ProviderIntegrationHardeningReport().build_full_report()

        def closeEvent(self, event):
            if self._worker and self._worker.isRunning():
                self._worker.cancel()
                self._worker.wait(2000)
            super().closeEvent(event)

else:
    # Headless stub — importable without Qt
    class ProviderIntegrationHardeningPanel:  # type: ignore[no-redef]
        """Headless stub when PySide6 is not installed."""

        PANEL_VERSION = _PANEL_VERSION

        def __init__(self, parent=None):
            self._model = ProviderIntegrationHardeningModel()
            logger.debug("ProviderIntegrationHardeningPanel: headless stub created")
