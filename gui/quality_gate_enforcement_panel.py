"""
gui/quality_gate_enforcement_panel.py — QualityGateEnforcementPanel v1.1.5

Quality Gate Enforcement & Audit GUI panel.
Research Only. No Real Orders. No broker. No trading.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] Gate bypass DISABLED. Override is research-only.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_DISABLED = True
RESEARCH_ONLY = True

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QTextEdit, QGroupBox,
        QComboBox, QLineEdit, QHeaderView, QSplitter, QFrame,
        QScrollArea,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — QualityGateEnforcementPanel will be stub only")


if _PYSIDE6_AVAILABLE:

    class _EnforcementWorker(QThread):
        """Background worker for enforcement operations."""
        finished = Signal(dict)
        error = Signal(str)

        def __init__(self, operation: str, params: dict):
            super().__init__()
            self._operation = operation
            self._params = params

        def run(self):
            try:
                result = self._execute()
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

        def _execute(self) -> dict:
            op = self._operation
            if op == "health":
                from gate_enforcement.enforcement_health import QualityGateEnforcementHealthCheck
                checker = QualityGateEnforcementHealthCheck()
                checks = checker.run()
                return {"type": "health", "checks": checks}
            elif op == "preview":
                from gate_enforcement.enforcement_policy import QualityGateEnforcementPolicy
                policy = QualityGateEnforcementPolicy()
                command = self._params.get("command", "validate-score")
                mode = self._params.get("mode", "real")
                return {
                    "type": "preview",
                    "gate": policy.resolve_gate(command),
                    "default_level": policy.resolve_default_level(command, mode),
                    "allow_observational": policy.allow_observational(command),
                    "allow_demo": policy.allow_demo(command),
                    "policy_version": policy.POLICY_VERSION,
                }
            elif op == "latest_runs":
                from gate_enforcement.enforcement_query import EnforcementQuery
                query = EnforcementQuery()
                return {"type": "runs", "runs": query.latest_runs()}
            elif op == "audit":
                from gate_enforcement.audit_log import QualityGateAuditLog
                log = QualityGateAuditLog()
                events = log.list_events()
                chain = log.verify_chain()
                return {"type": "audit", "events": events, "chain": chain}
            return {"type": "unknown"}

    class QualityGateEnforcementPanel(QWidget):
        """
        Quality Gate Enforcement & Audit panel.

        Sections:
        A. Safety Banner
        B. Run Selector
        C. Enforcement Summary
        D. Exclusion Table
        E. Snapshot
        F. Audit Timeline
        G. Reproducibility
        H. Action Buttons

        [!] NO broker functionality. NO trading. NO bypass.
        """

        def __init__(self, parent=None, mode: str = "real"):
            super().__init__(parent)
            self._mode = mode
            self._worker = None
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setSpacing(6)
            layout.setContentsMargins(8, 8, 8, 8)

            # ---- A. Safety Banner ----
            banner = QGroupBox("Safety Banner")
            banner_layout = QVBoxLayout(banner)
            safety_text = (
                "[!] Research Only | No Real Orders | "
                "Quality Gate Does NOT Enable Trading | "
                "Gate Bypass: DISABLED | Override: Research-Only"
            )
            banner_label = QLabel(safety_text)
            banner_label.setWordWrap(True)
            banner_label.setStyleSheet("color: #FF9900; font-weight: bold;")
            banner_layout.addWidget(banner_label)
            layout.addWidget(banner)

            # ---- B. Run Selector ----
            selector_group = QGroupBox("B. Run Selector")
            selector_layout = QHBoxLayout(selector_group)

            selector_layout.addWidget(QLabel("Command:"))
            self._command_combo = QComboBox()
            self._command_combo.addItems([
                "validate-score", "backtest-buy-points", "backtest-screener",
                "backtest-strategy-knowledge", "strategy-validation", "stock-report",
            ])
            selector_layout.addWidget(self._command_combo)

            selector_layout.addWidget(QLabel("Tier:"))
            self._tier_edit = QLineEdit("core10")
            self._tier_edit.setFixedWidth(100)
            selector_layout.addWidget(self._tier_edit)

            selector_layout.addWidget(QLabel("Gate Level:"))
            self._level_combo = QComboBox()
            self._level_combo.addItems(["auto", "formal", "observational", "demo", "off"])
            selector_layout.addWidget(self._level_combo)

            selector_layout.addWidget(QLabel("Gate Mode:"))
            self._mode_combo = QComboBox()
            self._mode_combo.addItems(["enforce", "audit-only", "off"])
            selector_layout.addWidget(self._mode_combo)

            selector_layout.addStretch()
            layout.addWidget(selector_group)

            # ---- C. Enforcement Summary ----
            summary_group = QGroupBox("C. Enforcement Summary")
            summary_layout = QVBoxLayout(summary_group)
            self._summary_label = QLabel("No enforcement run loaded. Use buttons below to run.")
            self._summary_label.setWordWrap(True)
            summary_layout.addWidget(self._summary_label)
            layout.addWidget(summary_group)

            # ---- D. Exclusion Table ----
            exclusion_group = QGroupBox("D. Exclusion Audit")
            exclusion_layout = QVBoxLayout(exclusion_group)
            self._exclusion_table = QTableWidget(0, 5)
            self._exclusion_table.setHorizontalHeaderLabels([
                "Symbol", "Decision", "Reason Codes", "Required Actions", "Override"
            ])
            self._exclusion_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            exclusion_layout.addWidget(self._exclusion_table)
            layout.addWidget(exclusion_group)

            # ---- E. Snapshot ----
            snap_group = QGroupBox("E. Snapshot")
            snap_layout = QVBoxLayout(snap_group)
            self._snapshot_text = QTextEdit()
            self._snapshot_text.setReadOnly(True)
            self._snapshot_text.setMaximumHeight(100)
            self._snapshot_text.setText("No snapshot loaded.")
            snap_layout.addWidget(self._snapshot_text)
            layout.addWidget(snap_group)

            # ---- F. Audit Timeline ----
            audit_group = QGroupBox("F. Audit Timeline")
            audit_layout = QVBoxLayout(audit_group)
            self._audit_table = QTableWidget(0, 5)
            self._audit_table.setHorizontalHeaderLabels([
                "Time", "Event", "Symbol", "State", "Reason"
            ])
            self._audit_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            audit_layout.addWidget(self._audit_table)
            layout.addWidget(audit_group)

            # ---- G. Reproducibility ----
            repro_group = QGroupBox("G. Reproducibility")
            repro_layout = QVBoxLayout(repro_group)
            self._repro_label = QLabel("No hash loaded.")
            repro_layout.addWidget(self._repro_label)
            layout.addWidget(repro_group)

            # ---- H. Buttons ----
            btn_layout = QHBoxLayout()
            buttons = [
                ("Preview Enforcement", self._on_preview),
                ("Load Latest Runs", self._on_load_runs),
                ("Health Check", self._on_health),
                ("Verify Audit", self._on_verify_audit),
                ("Build Audit Report", self._on_build_report),
            ]
            for label, handler in buttons:
                btn = QPushButton(label)
                btn.clicked.connect(handler)
                btn_layout.addWidget(btn)
            layout.addLayout(btn_layout)

        # ---- Button handlers ----

        def _on_preview(self):
            self._run_worker("preview", {
                "command": self._command_combo.currentText(),
                "mode": self._mode,
            })

        def _on_load_runs(self):
            self._run_worker("latest_runs", {})

        def _on_health(self):
            self._run_worker("health", {})

        def _on_verify_audit(self):
            self._run_worker("audit", {})

        def _on_build_report(self):
            try:
                from reports.quality_gate_enforcement_audit_report import QualityGateEnforcementAuditReportBuilder
                builder = QualityGateEnforcementAuditReportBuilder()
                path = builder.build()
                self._summary_label.setText(f"Report saved: {path}")
            except Exception as exc:
                self._summary_label.setText(f"Report failed: {exc}")

        def _run_worker(self, operation: str, params: dict):
            if self._worker and self._worker.isRunning():
                return
            self._worker = _EnforcementWorker(operation, params)
            self._worker.finished.connect(self._on_worker_finished)
            self._worker.error.connect(self._on_worker_error)
            self._worker.start()

        def _on_worker_finished(self, result: dict):
            op = result.get("type", "")
            if op == "health":
                checks = result.get("checks", [])
                passed = sum(1 for _, s, _ in checks if s == "PASS")
                self._summary_label.setText(
                    f"Health: {passed}/{len(checks)} PASS\n" +
                    "\n".join(f"[{s}] {n}: {m}" for n, s, m in checks[:10])
                )
            elif op == "preview":
                self._summary_label.setText(
                    f"Gate: {result.get('gate')} | Level: {result.get('default_level')} | "
                    f"Policy: {result.get('policy_version')}"
                )
            elif op == "runs":
                runs = result.get("runs", [])
                if runs:
                    self._summary_label.setText(f"Latest {len(runs)} runs loaded.")
                else:
                    self._summary_label.setText("No runs found.")
            elif op == "audit":
                events = result.get("events", [])
                chain = result.get("chain", {})
                self._audit_table.setRowCount(0)
                for ev in events[:50]:
                    row = self._audit_table.rowCount()
                    self._audit_table.insertRow(row)
                    self._audit_table.setItem(row, 0, QTableWidgetItem(ev.get("timestamp", "")))
                    self._audit_table.setItem(row, 1, QTableWidgetItem(ev.get("event_type", "")))
                    self._audit_table.setItem(row, 2, QTableWidgetItem(ev.get("symbol", "")))
                    self._audit_table.setItem(row, 3, QTableWidgetItem(ev.get("new_state", "")))
                    self._audit_table.setItem(row, 4, QTableWidgetItem(ev.get("reason", "")))
                valid = chain.get("valid", False)
                self._summary_label.setText(
                    f"Audit: {len(events)} events | Chain valid: {'YES' if valid else 'NO'}"
                )

        def _on_worker_error(self, error_msg: str):
            self._summary_label.setText(f"[ERROR] {error_msg}")


else:
    # Stub when PySide6 not available
    class QualityGateEnforcementPanel:
        """Stub panel when PySide6 is not available."""
        NO_REAL_ORDERS = True
        BROKER_DISABLED = True
        RESEARCH_ONLY = True

        def __init__(self, parent=None, mode: str = "real"):
            logger.warning("QualityGateEnforcementPanel: PySide6 not available")
