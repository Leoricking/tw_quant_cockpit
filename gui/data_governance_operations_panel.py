"""
gui.data_governance_operations_panel — DataGovernanceOperationsPanel v1.1.6

PySide6/PyQt5 panel for Data Governance Operations Dashboard.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NO Run Repair, NO Auto Import, NO Gate Override, NO broker, NO trading.
[!] Copy Suggested Command only copies safe CLI commands.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QTabWidget, QGroupBox,
        QSplitter, QScrollArea, QMessageBox, QHeaderView,
        QApplication, QFrame,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QTimer
    from PySide6.QtGui import QColor, QFont, QPalette
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


def _make_stub_panel(title: str = "Data Governance Operations Dashboard"):
    """Return a stub panel class when PySide6 is unavailable."""
    class StubPanel:
        def __init__(self, *args, **kwargs):
            logger.info("%s: PySide6 not available, panel is a stub.", title)
    return StubPanel


if not _PYSIDE6_AVAILABLE:
    DataGovernanceOperationsPanel = _make_stub_panel()
else:
    class _RefreshWorker(QThread):
        """Background worker for governance data refresh."""

        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, mode: str = "real", tier: str = "research30", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._tier = tier

        def run(self):
            try:
                from governance_ops.operations_engine import DataGovernanceOperationsEngine
                engine = DataGovernanceOperationsEngine()
                summary = engine.run(mode=self._mode, tier=self._tier)
                module_health = engine.build_module_health()
                symbol_matrix = engine.build_symbol_matrix(tier=self._tier)
                actions = engine.build_action_queue_from_data(symbol_matrix, module_health)
                runs = engine.build_run_audit_summary()
                self.finished.emit({
                    "summary": summary,
                    "module_health": module_health,
                    "symbol_matrix": symbol_matrix,
                    "actions": actions,
                    "runs": runs,
                })
            except Exception as exc:
                logger.warning("_RefreshWorker error: %s", exc)
                self.error.emit(str(exc))

    class DataGovernanceOperationsPanel(QWidget):
        """
        Data Governance Operations Dashboard panel.

        Sections:
        A. Safety Banner
        B. Overall Health Header
        C. Summary Cards
        D. Module Health Grid
        E. Action Queue
        F. Symbol Governance Matrix
        G. Recent Research Runs
        H. Source Health

        [!] Research Only. No Real Orders.
        [!] NO Run Repair, NO Auto Import, NO Gate Override, NO broker, NO trading.
        """

        def __init__(self, mode: str = "real", tier: str = "research30", parent=None):
            super().__init__(parent)
            self._mode = mode
            self._tier = tier
            self._worker = None
            self._current_actions = []
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(8, 8, 8, 8)
            layout.setSpacing(6)

            # Section A: Safety Banner
            safety_frame = QFrame()
            safety_frame.setStyleSheet(
                "background-color: #1A0A0A; border: 1px solid #FF4444; border-radius: 4px; padding: 4px;"
            )
            safety_layout = QHBoxLayout(safety_frame)
            safety_label = QLabel(
                "[!] RESEARCH ONLY — No Real Orders — No Broker — No Auto Repair — "
                "No Auto Download — No Gate Override — No Trading"
            )
            safety_label.setStyleSheet("color: #FF8888; font-weight: bold; font-size: 11px;")
            safety_label.setWordWrap(True)
            safety_layout.addWidget(safety_label)
            layout.addWidget(safety_frame)

            # Section B: Overall Health Header
            header_group = QGroupBox("Overall Governance Health")
            header_layout = QHBoxLayout(header_group)
            self._overall_status_label = QLabel("Overall: UNKNOWN")
            self._overall_status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            self._confidence_label = QLabel("Confidence: —")
            self._last_refresh_label = QLabel("Last Refresh: —")
            self._p0_label = QLabel("P0: 0")
            self._p0_label.setStyleSheet("color: #FF4444;")
            self._p1_label = QLabel("P1: 0")
            self._p1_label.setStyleSheet("color: #FF8800;")
            for lbl in [self._overall_status_label, self._confidence_label,
                        self._last_refresh_label, self._p0_label, self._p1_label]:
                header_layout.addWidget(lbl)
            header_layout.addStretch()
            refresh_btn = QPushButton("Refresh Dashboard")
            refresh_btn.clicked.connect(self._on_refresh)
            refresh_btn.setToolTip("[!] Read-only refresh. Does NOT repair or modify data.")
            header_layout.addWidget(refresh_btn)
            export_btn = QPushButton("Export Report")
            export_btn.clicked.connect(self._on_export_report)
            header_layout.addWidget(export_btn)
            layout.addWidget(header_group)

            # Tabs for sections C-H
            self._tabs = QTabWidget()
            layout.addWidget(self._tabs)

            # Tab: Summary Cards (Section C)
            summary_tab = QWidget()
            summary_layout = QVBoxLayout(summary_tab)
            self._summary_table = QTableWidget(0, 2)
            self._summary_table.setHorizontalHeaderLabels(["Metric", "Value"])
            self._summary_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self._summary_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            summary_layout.addWidget(self._summary_table)

            # v1.1.7 Governance Alerts summary sub-section
            alerts_group = QGroupBox("Governance Alerts Summary (v1.1.7)")
            alerts_group.setStyleSheet("QGroupBox { font-weight: bold; }")
            alerts_layout = QHBoxLayout(alerts_group)
            self._ga_open_label = QLabel("Open: —")
            self._ga_p0_label = QLabel("P0: —")
            self._ga_p0_label.setStyleSheet("color: #FF4444;")
            self._ga_p1_label = QLabel("P1: —")
            self._ga_p1_label.setStyleSheet("color: #FF8800;")
            self._ga_escalated_label = QLabel("Escalated: —")
            self._ga_snoozed_label = QLabel("Snoozed: —")
            self._ga_reopened_label = QLabel("Reopened Today: —")
            self._ga_checklist_label = QLabel("Checklist: —")
            self._ga_digest_label = QLabel("Latest Digest: —")
            self._ga_digest_label.setWordWrap(True)
            for lbl in [
                self._ga_open_label, self._ga_p0_label, self._ga_p1_label,
                self._ga_escalated_label, self._ga_snoozed_label, self._ga_reopened_label,
                self._ga_checklist_label,
            ]:
                alerts_layout.addWidget(lbl)
            alerts_layout.addStretch()
            open_alerts_btn = QPushButton("Open Governance Alerts")
            open_alerts_btn.setToolTip("Open the Governance Alerts & Daily Operations tab")
            open_alerts_btn.clicked.connect(self._on_open_governance_alerts)
            checklist_btn = QPushButton("Open Daily Checklist")
            checklist_btn.setToolTip("Run: python main.py governance-checklist")
            checklist_btn.clicked.connect(self._on_open_daily_checklist)
            digest_btn = QPushButton("Open Latest Digest")
            digest_btn.setToolTip("Run: python main.py governance-digest --type daily")
            digest_btn.clicked.connect(self._on_open_latest_digest)
            for btn in [open_alerts_btn, checklist_btn, digest_btn]:
                alerts_layout.addWidget(btn)
            summary_layout.addWidget(alerts_group)
            summary_layout.addWidget(self._ga_digest_label)
            self._tabs.addTab(summary_tab, "Summary")

            # Tab: Module Health (Section D)
            module_tab = QWidget()
            module_layout = QVBoxLayout(module_tab)
            self._module_table = QTableWidget(0, 7)
            self._module_table.setHorizontalHeaderLabels(
                ["Module", "Available", "Status", "PASS", "WARN", "FAIL", "Version"]
            )
            self._module_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            for i in range(1, 7):
                self._module_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            module_layout.addWidget(self._module_table)
            self._tabs.addTab(module_tab, "Module Health")

            # Tab: Action Queue (Section E)
            action_tab = QWidget()
            action_layout = QVBoxLayout(action_tab)
            action_header = QHBoxLayout()
            action_header_label = QLabel("[!] Action metadata only. Dashboard does NOT execute actions.")
            action_header_label.setStyleSheet("color: #FF8888; font-size: 10px;")
            action_header.addWidget(action_header_label)
            ack_btn = QPushButton("Acknowledge")
            ack_btn.clicked.connect(self._on_acknowledge_action)
            defer_btn = QPushButton("Defer")
            defer_btn.clicked.connect(self._on_defer_action)
            copy_btn = QPushButton("Copy Suggested Command")
            copy_btn.clicked.connect(self._on_copy_suggested_command)
            copy_btn.setToolTip("Copies safe CLI command only. Does NOT execute.")
            action_header.addWidget(ack_btn)
            action_header.addWidget(defer_btn)
            action_header.addWidget(copy_btn)
            action_layout.addLayout(action_header)
            self._action_table = QTableWidget(0, 8)
            self._action_table.setHorizontalHeaderLabels(
                ["Priority", "Type", "Symbol/Source", "Title", "Reason", "Safe Action", "Status", "Age"]
            )
            self._action_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
            action_layout.addWidget(self._action_table)
            self._tabs.addTab(action_tab, "Action Queue")

            # Tab: Symbol Matrix (Section F)
            symbol_tab = QWidget()
            symbol_layout = QVBoxLayout(symbol_tab)
            self._symbol_table = QTableWidget(0, 9)
            self._symbol_table.setHorizontalHeaderLabels(
                ["Symbol", "Tier", "Coverage", "Freshness", "Gate", "Qualification",
                 "Repair", "Source Health", "Priority"]
            )
            self._symbol_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            symbol_layout.addWidget(self._symbol_table)
            self._tabs.addTab(symbol_tab, "Symbol Matrix")

            # Tab: Recent Runs (Section G)
            runs_tab = QWidget()
            runs_layout = QVBoxLayout(runs_tab)
            self._runs_table = QTableWidget(0, 9)
            self._runs_table.setHorizontalHeaderLabels(
                ["Run ID", "Command", "Qualification", "Included", "Excluded",
                 "Override", "Audit OK", "Reproducible", "Time"]
            )
            self._runs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            runs_layout.addWidget(self._runs_table)
            self._tabs.addTab(runs_tab, "Recent Runs")

        def _on_refresh(self):
            """Refresh dashboard in background thread."""
            if self._worker and self._worker.isRunning():
                return
            self._last_refresh_label.setText("Refreshing...")
            self._worker = _RefreshWorker(mode=self._mode, tier=self._tier, parent=self)
            self._worker.finished.connect(self._on_refresh_done)
            self._worker.error.connect(self._on_refresh_error)
            self._worker.start()

        def _on_refresh_done(self, data: dict):
            """Update UI with refreshed data."""
            try:
                summary = data.get("summary")
                module_health = data.get("module_health", {})
                symbol_matrix = data.get("symbol_matrix", [])
                actions = data.get("actions", [])
                runs = data.get("runs", [])
                self._current_actions = actions

                if summary:
                    self._overall_status_label.setText(f"Overall: {summary.overall_status}")
                    self._confidence_label.setText(f"Confidence: {summary.confidence:.0%}")
                    self._last_refresh_label.setText(f"Last Refresh: {summary.generated_at[:19]}")
                    self._p0_label.setText(f"P0: {summary.p0_actions}")
                    self._p1_label.setText(f"P1: {summary.p1_actions}")
                    self._update_summary_table(summary)

                self._update_module_table(module_health)
                self._update_action_table(actions)
                self._update_symbol_table(symbol_matrix)
                self._update_runs_table(runs)
                self._refresh_governance_alerts_summary()
            except Exception as exc:
                logger.warning("_on_refresh_done error: %s", exc)

        def _on_refresh_error(self, error_msg: str):
            self._last_refresh_label.setText(f"Refresh Error: {error_msg[:60]}")
            logger.warning("Governance dashboard refresh error: %s", error_msg)

        def _update_summary_table(self, summary):
            try:
                rows = [
                    ("Registered Symbols", str(summary.registered_symbols)),
                    ("Ready Symbols", str(summary.ready_symbols)),
                    ("Partial Symbols", str(summary.partial_symbols)),
                    ("Stale Symbols", str(summary.stale_symbols)),
                    ("Missing Symbols", str(summary.missing_symbols)),
                    ("Formal Eligible", str(summary.formal_eligible)),
                    ("Observational Eligible", str(summary.observational_eligible)),
                    ("Blocked Symbols", str(summary.blocked_symbols)),
                    ("Source Interruptions", str(summary.source_interruptions)),
                    ("Audit Chain Failures", str(summary.audit_chain_failures)),
                    ("Open Actions", str(summary.open_actions)),
                    ("P0 Actions", str(summary.p0_actions)),
                    ("P1 Actions", str(summary.p1_actions)),
                    ("Non-qualified Runs", str(summary.non_qualified_runs)),
                    ("Overall Status", summary.overall_status),
                    ("Research Only", "True"),
                    ("No Real Orders", "True"),
                ]
                self._summary_table.setRowCount(len(rows))
                for row_idx, (k, v) in enumerate(rows):
                    self._summary_table.setItem(row_idx, 0, QTableWidgetItem(k))
                    self._summary_table.setItem(row_idx, 1, QTableWidgetItem(v))
            except Exception as exc:
                logger.warning("_update_summary_table error: %s", exc)

        def _update_module_table(self, module_health: dict):
            try:
                self._module_table.setRowCount(0)
                for name, status in (module_health or {}).items():
                    row = self._module_table.rowCount()
                    self._module_table.insertRow(row)
                    self._module_table.setItem(row, 0, QTableWidgetItem(str(name)))
                    self._module_table.setItem(row, 1, QTableWidgetItem(str(getattr(status, "available", "?"))))
                    h_status = getattr(status, "health_status", "?")
                    item = QTableWidgetItem(h_status)
                    if h_status == "PASS":
                        item.setForeground(QColor("#33CC66"))
                    elif h_status in ("FAIL", "BLOCKED", "UNAVAILABLE"):
                        item.setForeground(QColor("#FF4444"))
                    else:
                        item.setForeground(QColor("#FF8800"))
                    self._module_table.setItem(row, 2, item)
                    self._module_table.setItem(row, 3, QTableWidgetItem(str(getattr(status, "pass_count", 0))))
                    self._module_table.setItem(row, 4, QTableWidgetItem(str(getattr(status, "warn_count", 0))))
                    self._module_table.setItem(row, 5, QTableWidgetItem(str(getattr(status, "fail_count", 0))))
                    self._module_table.setItem(row, 6, QTableWidgetItem(str(getattr(status, "version", ""))))
            except Exception as exc:
                logger.warning("_update_module_table error: %s", exc)

        def _update_action_table(self, actions: list):
            try:
                self._action_table.setRowCount(0)
                for action in (actions or [])[:50]:
                    row = self._action_table.rowCount()
                    self._action_table.insertRow(row)
                    prio = getattr(action, "priority", "P3")
                    prio_item = QTableWidgetItem(prio)
                    if prio == "P0":
                        prio_item.setForeground(QColor("#FF4444"))
                    elif prio == "P1":
                        prio_item.setForeground(QColor("#FF8800"))
                    elif prio == "P2":
                        prio_item.setForeground(QColor("#CCCC00"))
                    self._action_table.setItem(row, 0, prio_item)
                    self._action_table.setItem(row, 1, QTableWidgetItem(str(getattr(action, "action_type", ""))))
                    sym = getattr(action, "symbol", "") or getattr(action, "source", "") or "(system)"
                    self._action_table.setItem(row, 2, QTableWidgetItem(str(sym)))
                    self._action_table.setItem(row, 3, QTableWidgetItem(str(getattr(action, "title", ""))[:60]))
                    rc = getattr(action, "reason_codes", [])
                    self._action_table.setItem(row, 4, QTableWidgetItem(", ".join(rc[:2] if rc else [])))
                    self._action_table.setItem(row, 5, QTableWidgetItem(str(getattr(action, "safe_action", "REVIEW"))))
                    self._action_table.setItem(row, 6, QTableWidgetItem(str(getattr(action, "status", "OPEN"))))
                    self._action_table.setItem(row, 7, QTableWidgetItem(str(getattr(action, "created_at", ""))[:10]))
            except Exception as exc:
                logger.warning("_update_action_table error: %s", exc)

        def _update_symbol_table(self, symbol_statuses: list):
            try:
                self._symbol_table.setRowCount(0)
                for s in (symbol_statuses or [])[:100]:
                    row = self._symbol_table.rowCount()
                    self._symbol_table.insertRow(row)
                    self._symbol_table.setItem(row, 0, QTableWidgetItem(str(getattr(s, "symbol", ""))))
                    self._symbol_table.setItem(row, 1, QTableWidgetItem(str(getattr(s, "tier", ""))))
                    self._symbol_table.setItem(row, 2, QTableWidgetItem(str(getattr(s, "coverage_status", ""))))
                    self._symbol_table.setItem(row, 3, QTableWidgetItem(str(getattr(s, "freshness_status", ""))))
                    self._symbol_table.setItem(row, 4, QTableWidgetItem(str(getattr(s, "quality_gate_level", ""))[:15]))
                    self._symbol_table.setItem(row, 5, QTableWidgetItem(str(getattr(s, "qualification", ""))))
                    self._symbol_table.setItem(row, 6, QTableWidgetItem(str(getattr(s, "open_repair_issues", 0))))
                    self._symbol_table.setItem(row, 7, QTableWidgetItem(str(getattr(s, "source_health", ""))))
                    self._symbol_table.setItem(row, 8, QTableWidgetItem(str(getattr(s, "priority", "P3"))))
            except Exception as exc:
                logger.warning("_update_symbol_table error: %s", exc)

        def _update_runs_table(self, runs: list):
            try:
                self._runs_table.setRowCount(0)
                for r in (runs or [])[:20]:
                    row = self._runs_table.rowCount()
                    self._runs_table.insertRow(row)
                    self._runs_table.setItem(row, 0, QTableWidgetItem(str(getattr(r, "run_id", ""))[:20]))
                    self._runs_table.setItem(row, 1, QTableWidgetItem(str(getattr(r, "command_name", ""))))
                    self._runs_table.setItem(row, 2, QTableWidgetItem(str(getattr(r, "qualification", ""))))
                    self._runs_table.setItem(row, 3, QTableWidgetItem(str(getattr(r, "included_count", 0))))
                    self._runs_table.setItem(row, 4, QTableWidgetItem(str(getattr(r, "excluded_count", 0))))
                    self._runs_table.setItem(row, 5, QTableWidgetItem(str(getattr(r, "override_used", False))))
                    self._runs_table.setItem(row, 6, QTableWidgetItem(str(getattr(r, "audit_chain_valid", True))))
                    self._runs_table.setItem(row, 7, QTableWidgetItem(str(getattr(r, "reproducibility_verified", False))))
                    self._runs_table.setItem(row, 8, QTableWidgetItem(str(getattr(r, "created_at", ""))[:19]))
            except Exception as exc:
                logger.warning("_update_runs_table error: %s", exc)

        def _on_export_report(self):
            """Export governance report."""
            try:
                from reports.data_governance_operations_report import DataGovernanceOperationsReportBuilder
                builder = DataGovernanceOperationsReportBuilder()
                path = builder.build(tier=self._tier, mode=self._mode)
                QMessageBox.information(self, "Report Exported", f"Report saved to:\n{path}")
            except Exception as exc:
                QMessageBox.warning(self, "Export Error", f"Report export failed: {exc}")

        def _on_acknowledge_action(self):
            """Acknowledge selected action (metadata only)."""
            row = self._action_table.currentRow()
            if row < 0 or row >= len(self._current_actions):
                QMessageBox.information(self, "No Selection", "Please select an action to acknowledge.")
                return
            action = self._current_actions[row]
            from governance_ops.action_queue import GovernanceActionQueue
            q = GovernanceActionQueue()
            q._actions = self._current_actions
            ok = q.acknowledge(action.action_id)
            if ok:
                self._action_table.setItem(row, 6, QTableWidgetItem("ACKNOWLEDGED"))

        def _on_defer_action(self):
            """Defer selected action (metadata only)."""
            row = self._action_table.currentRow()
            if row < 0 or row >= len(self._current_actions):
                QMessageBox.information(self, "No Selection", "Please select an action to defer.")
                return
            action = self._current_actions[row]
            from governance_ops.action_queue import GovernanceActionQueue
            q = GovernanceActionQueue()
            q._actions = self._current_actions
            ok = q.defer(action.action_id, "Deferred via GUI")
            if ok:
                self._action_table.setItem(row, 6, QTableWidgetItem("DEFERRED"))

        def _on_copy_suggested_command(self):
            """Copy safe CLI command to clipboard (does NOT execute)."""
            row = self._action_table.currentRow()
            if row < 0 or row >= len(self._current_actions):
                QMessageBox.information(self, "No Selection", "Please select an action to copy its suggested command.")
                return
            action = self._current_actions[row]
            cmd = action.suggested_command or ""
            if not cmd:
                QMessageBox.information(self, "No Command", "No suggested command for this action.")
                return
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(cmd)
            QMessageBox.information(
                self, "Command Copied",
                f"Safe CLI command copied to clipboard:\n{cmd}\n\n"
                "[!] This only copies the command. It does NOT execute it."
            )

        def _refresh_governance_alerts_summary(self):
            """Refresh governance alerts summary sub-section (v1.1.7, read-only)."""
            try:
                from gui.governance_alerts_adapter import GovernanceAlertsAdapter
                adapter = GovernanceAlertsAdapter()
                s = adapter.summary()
                self._ga_open_label.setText(f"Open: {s.get('open', 0)}")
                self._ga_p0_label.setText(f"P0: {s.get('p0', 0)}")
                self._ga_p1_label.setText(f"P1: {s.get('p1', 0)}")
                self._ga_escalated_label.setText(f"Escalated: {s.get('escalated', 0)}")
                self._ga_snoozed_label.setText(f"Snoozed: {s.get('snoozed', 0)}")
                self._ga_reopened_label.setText(f"Reopened Today: {s.get('reopened_today', 0)}")
                cr = s.get("checklist_completion", 0.0)
                self._ga_checklist_label.setText(f"Checklist: {cr:.0%}")
                digest_txt = adapter.latest_digest_summary()
                self._ga_digest_label.setText(f"Latest Digest: {digest_txt}")
            except Exception as exc:
                logger.debug("_refresh_governance_alerts_summary: %s", exc)

        def _on_open_governance_alerts(self):
            """Navigate to Governance Alerts tab via informational message."""
            QMessageBox.information(
                self, "Governance Alerts",
                "Open the 'Governance Alerts' tab in the main dashboard.\n\n"
                "Or run: python main.py governance-alerts\n\n"
                "[!] Research Only. No Real Orders."
            )

        def _on_open_daily_checklist(self):
            """Show daily checklist command info."""
            QMessageBox.information(
                self, "Daily Checklist",
                "Run: python main.py governance-checklist\n\n"
                "[!] Research Only. No Real Orders."
            )

        def _on_open_latest_digest(self):
            """Show latest digest command info."""
            QMessageBox.information(
                self, "Latest Digest",
                "Run: python main.py governance-digest --type daily\n\n"
                "[!] Research Only. No Real Orders."
            )
