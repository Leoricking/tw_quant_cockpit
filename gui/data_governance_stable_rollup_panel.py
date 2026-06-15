"""
gui/data_governance_stable_rollup_panel.py — DataGovernanceStableRollupPanel v1.1.9

PySide6 panel for Data Governance Stable Rollup.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NO Execute Recovery, NO Execute Migration, NO Auto Repair,
    NO Auto Import, NO Broker, NO Trading buttons.
[!] Preview only for recovery and migration.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QTabWidget, QGroupBox,
        QSplitter, QScrollArea, QMessageBox, QHeaderView,
        QApplication, QFrame, QTextEdit,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QTimer
    from PySide6.QtGui import QColor, QFont, QPalette
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


def _make_stub_panel(title: str = "Data Governance Stable Rollup"):
    """Return a stub panel class when PySide6 is unavailable."""
    class StubPanel:
        def __init__(self, *args, **kwargs):
            logger.info("%s: PySide6 not available, panel is a stub.", title)
    return StubPanel


if not _PYSIDE6_AVAILABLE:
    DataGovernanceStableRollupPanel = _make_stub_panel()
else:
    class _RollupWorker(QThread):
        """Background worker for long-running rollup operations."""
        finished = Signal(object)
        error = Signal(str)

        def __init__(self, task_fn, *args, **kwargs):
            super().__init__()
            self._task_fn = task_fn
            self._args = args
            self._kwargs = kwargs

        def run(self):
            try:
                result = self._task_fn(*self._args, **self._kwargs)
                self.finished.emit(result)
            except Exception as exc:
                logger.error("_RollupWorker error: %s", exc)
                self.error.emit(str(exc))

    class DataGovernanceStableRollupPanel(QWidget):
        """
        Data Governance Stable Rollup panel.
        Read-only operations. Preview only for recovery/migration.
        NO execute recovery, NO execute migration, NO auto repair, NO trading.
        """

        NO_REAL_ORDERS = True
        RESEARCH_ONLY = True

        def __init__(self, parent=None):
            super().__init__(parent)
            self._adapter = None
            self._worker = None
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(8, 8, 8, 8)

            # Safety banner
            banner = self._make_safety_banner()
            layout.addWidget(banner)

            # Tabs
            self._tabs = QTabWidget()
            layout.addWidget(self._tabs)

            self._tabs.addTab(self._make_summary_tab(), "Summary")
            self._tabs.addTab(self._make_health_matrix_tab(), "Health Matrix")
            self._tabs.addTab(self._make_store_inventory_tab(), "Store Inventory")
            self._tabs.addTab(self._make_consistency_tab(), "Consistency")
            self._tabs.addTab(self._make_recovery_preview_tab(), "Recovery Preview")
            self._tabs.addTab(self._make_migration_preview_tab(), "Migration Preview")
            self._tabs.addTab(self._make_release_gate_tab(), "Release Gate")

            # Buttons
            btn_bar = self._make_button_bar()
            layout.addWidget(btn_bar)

        def _make_safety_banner(self) -> QFrame:
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            lay = QHBoxLayout(frame)
            label = QLabel(
                "[!] Research Only | No Real Orders | Production BLOCKED | "
                "v1.1.9 Data Governance Stable Rollup | Not Investment Advice"
            )
            label.setStyleSheet("color: #b05000; font-weight: bold; font-size: 11px;")
            lay.addWidget(label)
            return frame

        def _make_summary_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            self._summary_text = QTextEdit()
            self._summary_text.setReadOnly(True)
            self._summary_text.setPlaceholderText(
                "Click 'Run Stable Rollup' to generate summary..."
            )
            lay.addWidget(QLabel("Stable Rollup Summary"))
            lay.addWidget(self._summary_text)
            return w

        def _make_health_matrix_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.addWidget(QLabel("Module Health Matrix"))
            self._health_table = self._make_table(
                ["Module", "Status", "Available", "Checks Passed", "Checks Failed"]
            )
            lay.addWidget(self._health_table)
            return w

        def _make_store_inventory_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.addWidget(QLabel("Store Inventory"))
            self._inventory_table = self._make_table(
                ["Store ID", "Module", "Type", "Exists", "Size", "Status", "Reason"]
            )
            lay.addWidget(self._inventory_table)

            # Corrupted store warning label
            self._store_warning = QLabel("")
            self._store_warning.setStyleSheet("color: #b05000; font-weight: bold;")
            lay.addWidget(self._store_warning)
            return w

        def _make_consistency_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.addWidget(QLabel("Cross-Module Consistency Issues"))
            self._consistency_table = self._make_table(
                ["Module", "Issue Type", "Detail", "Severity"]
            )
            lay.addWidget(self._consistency_table)
            return w

        def _make_recovery_preview_tab(self) -> QWidget:
            """Preview only — NO Execute button."""
            w = QWidget()
            lay = QVBoxLayout(w)
            info = QLabel(
                "[!] Recovery Preview Only — No execute button. "
                "Use CLI: python main.py governance-store-recovery-execute --plan-id <id> --allow-write"
            )
            info.setStyleSheet("color: #b05000;")
            info.setWordWrap(True)
            lay.addWidget(info)
            lay.addWidget(QLabel("Recovery Plans (Preview)"))
            self._recovery_table = self._make_table(
                ["Plan ID", "Store ID", "Issue Type", "Proposed Action",
                 "Destructive", "Safe", "Status"]
            )
            lay.addWidget(self._recovery_table)
            return w

        def _make_migration_preview_tab(self) -> QWidget:
            """Preview only — NO Execute button."""
            w = QWidget()
            lay = QVBoxLayout(w)
            info = QLabel(
                "[!] Migration Preview Only — No execute button. "
                "Use CLI: python main.py governance-metadata-migrate --module <name> --execute --allow-write"
            )
            info.setStyleSheet("color: #b05000;")
            info.setWordWrap(True)
            lay.addWidget(info)
            lay.addWidget(QLabel("Migration Plans (Preview)"))
            self._migration_table = self._make_table(
                ["Module", "From Version", "To Version", "File Count",
                 "Change Count", "Status"]
            )
            lay.addWidget(self._migration_table)
            return w

        def _make_release_gate_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.addWidget(QLabel("Release Gate Summary"))
            self._gate_text = QTextEdit()
            self._gate_text.setReadOnly(True)
            self._gate_text.setPlaceholderText(
                "Run stable rollup to see release gate status..."
            )
            lay.addWidget(self._gate_text)
            return w

        def _make_button_bar(self) -> QWidget:
            w = QWidget()
            lay = QHBoxLayout(w)
            lay.setContentsMargins(0, 0, 0, 0)

            # Safe read-only buttons only
            buttons = [
                ("Run Stable Rollup",    self._on_run_rollup),
                ("Refresh",              self._on_refresh),
                ("Validate Stores",      self._on_validate_stores),
                ("Audit Consistency",    self._on_audit_consistency),
                ("Audit Paths",          self._on_audit_paths),
                ("Audit Indexes",        self._on_audit_indexes),
                ("Audit CLI",            self._on_audit_cli),
                ("Audit GUI",            self._on_audit_gui),
                ("Audit Docs",           self._on_audit_docs),
                ("Preview Recovery",     self._on_preview_recovery),
                ("Preview Migration",    self._on_preview_migration),
                ("Build Rollup Report",  self._on_build_report),
            ]
            for label, handler in buttons:
                btn = QPushButton(label)
                btn.clicked.connect(handler)
                lay.addWidget(btn)

            lay.addStretch()
            # FORBIDDEN buttons are NOT added:
            # NO: Execute Recovery, Execute Migration, Auto Repair, Auto Import,
            #     Broker, Trading buttons
            return w

        # ------------------------------------------------------------------
        # Button handlers — all read-only operations
        # ------------------------------------------------------------------

        def _on_run_rollup(self):
            self._run_task("Running Stable Rollup...", self._do_run_rollup)

        def _on_refresh(self):
            self._run_task("Refreshing...", self._do_refresh)

        def _on_validate_stores(self):
            self._run_task("Validating Stores...", self._do_validate_stores)

        def _on_audit_consistency(self):
            self._run_task("Auditing Consistency...", self._do_audit_consistency)

        def _on_audit_paths(self):
            self._run_task("Auditing Paths...", self._do_audit_paths)

        def _on_audit_indexes(self):
            self._run_task("Auditing Indexes...", self._do_audit_indexes)

        def _on_audit_cli(self):
            self._run_task("Auditing CLI Surface...", self._do_audit_cli)

        def _on_audit_gui(self):
            self._run_task("Auditing GUI Surface...", self._do_audit_gui)

        def _on_audit_docs(self):
            self._run_task("Auditing Docs...", self._do_audit_docs)

        def _on_preview_recovery(self):
            self._run_task("Previewing Recovery Plans...", self._do_preview_recovery)

        def _on_preview_migration(self):
            self._run_task("Previewing Migration Plans...", self._do_preview_migration)

        def _on_build_report(self):
            self._run_task("Building Rollup Report...", self._do_build_report)

        # ------------------------------------------------------------------
        # Task implementations (no GUI freezing — uses QThread)
        # ------------------------------------------------------------------

        def _run_task(self, status_msg: str, task_fn):
            """Run a task in background thread to avoid GUI freeze."""
            self._summary_text.setPlaceholderText(f"{status_msg}")
            self._worker = _RollupWorker(task_fn)
            self._worker.finished.connect(self._on_task_done)
            self._worker.error.connect(self._on_task_error)
            self._worker.start()

        def _on_task_done(self, result: Any):
            if isinstance(result, dict):
                self._update_display(result)

        def _on_task_error(self, error_msg: str):
            self._summary_text.setPlainText(f"Error: {error_msg}")
            if "corrupt" in error_msg.lower() or "corruption" in error_msg.lower():
                self._store_warning.setText(
                    f"[!] Corrupted store detected: {error_msg[:120]}\n"
                    "Run 'Preview Recovery' to see recovery plans."
                )

        def _update_display(self, result: Dict[str, Any]):
            """Update panel display with result data."""
            summary_text = []
            for k, v in result.items():
                if isinstance(v, (str, int, float, bool)):
                    summary_text.append(f"{k}: {v}")
            self._summary_text.setPlainText("\n".join(summary_text))

        def _do_run_rollup(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.run_rollup()

        def _do_refresh(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.latest_summary() or {}

        def _do_validate_stores(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.validate_stores()

        def _do_audit_consistency(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.check_consistency()

        def _do_audit_paths(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.verify_paths()

        def _do_audit_indexes(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.verify_indexes()

        def _do_audit_cli(self) -> Dict[str, Any]:
            from governance_rollup.stable_rollup_engine import DataGovernanceStableRollupEngine
            engine = DataGovernanceStableRollupEngine()
            return engine.verify_cli_surface()

        def _do_audit_gui(self) -> Dict[str, Any]:
            from governance_rollup.gui_surface_audit import GovernanceGUISurfaceAuditor
            auditor = GovernanceGUISurfaceAuditor()
            return auditor.run()

        def _do_audit_docs(self) -> Dict[str, Any]:
            from governance_rollup.docs_surface_audit import GovernanceDocsSurfaceAuditor
            auditor = GovernanceDocsSurfaceAuditor()
            return auditor.run()

        def _do_preview_recovery(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.preview_recovery()

        def _do_preview_migration(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.preview_migration()

        def _do_build_report(self) -> Dict[str, Any]:
            from gui.data_governance_stable_rollup_adapter import DataGovernanceStableRollupAdapter
            adapter = DataGovernanceStableRollupAdapter()
            return adapter.build_report()

        def _make_table(self, headers: List[str]) -> QTableWidget:
            table = QTableWidget(0, len(headers))
            table.setHorizontalHeaderLabels(headers)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectRows)
            return table
