"""
gui/governance_alerts_panel.py — GovernanceAlertsPanel for TW Quant Cockpit v1.1.7

PySide6/PyQt5 GUI panel for Governance Alerts & Daily Operations.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] NO Repair Execute, NO Import Execute, NO Gate Override, NO Send Notification.
[!] No broker. No trading. Copy Safe Command: allowlist only.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True
EXTERNAL_NOTIFICATION_SEND_ENABLED = False

_PYSIDE6_AVAILABLE = False
_PYQT5_AVAILABLE = False

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
        QComboBox, QTabWidget, QSplitter, QFrame, QGroupBox,
        QScrollArea, QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_AVAILABLE = True
except ImportError:
    try:
        from PyQt5.QtWidgets import (
            QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
            QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
            QComboBox, QTabWidget, QSplitter, QFrame, QGroupBox,
            QScrollArea, QMessageBox,
        )
        from PyQt5.QtCore import Qt, QThread, pyqtSignal as Signal
        from PyQt5.QtGui import QColor, QFont
        _PYQT5_AVAILABLE = True
    except ImportError:
        pass

if not (_PYSIDE6_AVAILABLE or _PYQT5_AVAILABLE):
    # Stub implementation for environments without Qt
    class GovernanceAlertsPanel:
        """Stub GovernanceAlertsPanel (Qt not available)."""
        def __init__(self, *args, **kwargs):
            logger.warning("GovernanceAlertsPanel: Qt (PySide6/PyQt5) not available. GUI panel is a stub.")

    class GovernanceAlertsWorker:
        pass

else:
    # ---------------------------------------------------------------------------
    # Background worker
    # ---------------------------------------------------------------------------

    class GovernanceAlertsWorker(QThread):
        """Background worker for governance alerts operations."""
        alerts_ready = Signal(list)
        digest_ready = Signal(object)
        checklist_ready = Signal(object)
        error_occurred = Signal(str)

        def __init__(self, mode: str = "real", tier: str = "research30"):
            super().__init__()
            self._mode = mode
            self._tier = tier

        def run(self):
            try:
                from governance_alerts.alert_detector import GovernanceAlertDetector
                detector = GovernanceAlertDetector(mode=self._mode, tier=self._tier)
                alerts = detector.detect_all(mode=self._mode, tier=self._tier)
                self.alerts_ready.emit(alerts)

                from governance_alerts.digest_builder import GovernanceDigestBuilder
                builder = GovernanceDigestBuilder()
                digest = builder.build_daily_digest(alerts)
                self.digest_ready.emit(digest)

                from governance_alerts.daily_checklist import GovernanceDailyChecklistBuilder
                cl_builder = GovernanceDailyChecklistBuilder()
                checklist = cl_builder.build()
                self.checklist_ready.emit(checklist)

            except Exception as exc:
                self.error_occurred.emit(str(exc))

    # ---------------------------------------------------------------------------
    # Main panel
    # ---------------------------------------------------------------------------

    class GovernanceAlertsPanel(QWidget):
        """Governance Alerts & Daily Operations panel.

        Sections:
        A. Safety Banner
        B. Summary Cards
        C. Alert Table
        D. Alert Detail
        E. Daily Checklist
        F. Digest (tabs)
        G. Trend
        H. Buttons

        [!] No Repair Execute. No Import Execute. No Gate Override.
        [!] No Send Notification. No broker. No trading.
        [!] Research Only. No Real Orders.
        """

        no_real_orders = True
        research_only = True

        _ALLOWED_COPY_COMMANDS = [
            "governance-alerts-health",
            "governance-alerts-scan",
            "governance-alerts",
            "governance-alert-escalations",
            "governance-digest --type morning",
            "governance-digest --type daily",
            "governance-checklist",
            "governance-daily-operations",
            "governance-alerts-report",
            "governance-alert-audit-verify",
            "governance-health",
            "freshness-summary",
            "quality-gate-summary",
            "gate-enforcement-verify",
        ]

        def __init__(self, parent=None):
            super().__init__(parent)
            self._alerts = []
            self._digest = None
            self._checklist = None
            self._worker = None
            self._setup_ui()

        def _setup_ui(self):
            layout = QVBoxLayout(self)

            # A. Safety Banner
            banner = QLabel(
                "[!] Research Only | No Real Orders | No Auto Repair | No Auto Import | "
                "No Gate Override | External Notification: DISABLED | Trading: DISABLED"
            )
            banner.setStyleSheet("background-color: #FFF3CD; color: #856404; font-weight: bold; padding: 6px; border-radius: 4px;")
            banner.setWordWrap(True)
            layout.addWidget(banner)

            # Tabs
            self._tabs = QTabWidget()

            # Tab 1: Alerts Overview (cards + table)
            alerts_tab = QWidget()
            alerts_layout = QVBoxLayout(alerts_tab)

            # B. Summary Cards
            cards_layout = QHBoxLayout()
            self._card_open = self._make_card("Open", "0", "#DC3545")
            self._card_p0 = self._make_card("P0 Critical", "0", "#DC3545")
            self._card_p1 = self._make_card("P1 High", "0", "#FD7E14")
            self._card_escalated = self._make_card("Escalated", "0", "#FD7E14")
            self._card_snoozed = self._make_card("Snoozed", "0", "#6C757D")
            self._card_resolved = self._make_card("Resolved Today", "0", "#28A745")
            self._card_reopened = self._make_card("Reopened", "0", "#FFC107")
            self._card_audit = self._make_card("Audit Failures", "0", "#DC3545")
            for card in [self._card_open, self._card_p0, self._card_p1, self._card_escalated,
                          self._card_snoozed, self._card_resolved, self._card_reopened, self._card_audit]:
                cards_layout.addWidget(card)
            alerts_layout.addLayout(cards_layout)

            # C. Alert Table
            self._alert_table = QTableWidget()
            self._alert_table.setColumnCount(10)
            self._alert_table.setHorizontalHeaderLabels([
                "Priority", "Severity", "Type", "Symbol/Source",
                "Title", "Status", "First Detected", "Occurrences", "Escalation", "Safe Action"
            ])
            self._alert_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._alert_table.setSelectionBehavior(QTableWidget.SelectRows)
            self._alert_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._alert_table.itemSelectionChanged.connect(self._on_alert_selected)
            alerts_layout.addWidget(self._alert_table)

            # D. Alert Detail
            self._detail_text = QTextEdit()
            self._detail_text.setReadOnly(True)
            self._detail_text.setMaximumHeight(180)
            self._detail_text.setPlaceholderText("Select an alert to see details...")
            alerts_layout.addWidget(self._detail_text)

            self._tabs.addTab(alerts_tab, "Alerts")

            # Tab 2: Daily Checklist
            checklist_tab = QWidget()
            checklist_layout = QVBoxLayout(checklist_tab)
            self._checklist_table = QTableWidget()
            self._checklist_table.setColumnCount(6)
            self._checklist_table.setHorizontalHeaderLabels([
                "Category", "Item", "Required", "Status", "Safe Action", "Suggested Command"
            ])
            self._checklist_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._checklist_table.setEditTriggers(QTableWidget.NoEditTriggers)
            checklist_layout.addWidget(self._checklist_table)
            self._tabs.addTab(checklist_tab, "Daily Checklist")

            # Tab 3: Digest
            digest_tab = QWidget()
            digest_layout = QVBoxLayout(digest_tab)
            self._digest_tabs = QTabWidget()
            for dt in ["Morning", "End of Day", "Daily", "Weekly"]:
                t = QTextEdit()
                t.setReadOnly(True)
                t.setPlaceholderText(f"No {dt} digest loaded. Click 'Build {dt} Digest'.")
                self._digest_tabs.addTab(t, dt)
            digest_layout.addWidget(self._digest_tabs)
            self._tabs.addTab(digest_tab, "Digest")

            # Tab 4: Trend
            trend_tab = QWidget()
            trend_layout = QVBoxLayout(trend_tab)
            self._trend_text = QTextEdit()
            self._trend_text.setReadOnly(True)
            self._trend_text.setPlaceholderText("No trend data. Click 'Refresh Alerts'.")
            trend_layout.addWidget(self._trend_text)
            self._tabs.addTab(trend_tab, "Trend")

            layout.addWidget(self._tabs)

            # H. Buttons
            btn_layout = QHBoxLayout()
            self._btn_refresh = QPushButton("Refresh Alerts")
            self._btn_refresh.clicked.connect(self._on_refresh)
            self._btn_ack = QPushButton("Acknowledge")
            self._btn_ack.setToolTip("Acknowledge selected alert (metadata only)")
            self._btn_snooze = QPushButton("Snooze")
            self._btn_snooze.setToolTip("Snooze selected alert (metadata only)")
            self._btn_resolve = QPushButton("Resolve")
            self._btn_resolve.setToolTip("Resolve selected alert (metadata only)")
            self._btn_morning = QPushButton("Build Morning Digest")
            self._btn_morning.clicked.connect(self._on_build_morning_digest)
            self._btn_eod = QPushButton("Build End-of-Day Digest")
            self._btn_eod.clicked.connect(self._on_build_eod_digest)
            self._btn_copy = QPushButton("Copy Safe Command")
            self._btn_copy.clicked.connect(self._on_copy_safe_command)
            self._btn_export = QPushButton("Export Report")
            self._btn_export.clicked.connect(self._on_export_report)
            self._btn_preview = QPushButton("Notification Preview")
            self._btn_preview.clicked.connect(self._on_notification_preview)

            for btn in [self._btn_refresh, self._btn_ack, self._btn_snooze, self._btn_resolve,
                         self._btn_morning, self._btn_eod, self._btn_copy, self._btn_export, self._btn_preview]:
                btn_layout.addWidget(btn)
            layout.addLayout(btn_layout)

            # Safety note at bottom
            note = QLabel("[!] Research Only. No Real Orders. Not Investment Advice.")
            note.setStyleSheet("color: #6C757D; font-size: 10px;")
            layout.addWidget(note)

        def _make_card(self, title: str, value: str, color: str) -> QFrame:
            frame = QFrame()
            frame.setStyleSheet(f"border: 1px solid {color}; border-radius: 4px; padding: 4px;")
            layout = QVBoxLayout(frame)
            layout.setContentsMargins(8, 4, 8, 4)
            val_label = QLabel(value)
            val_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 10px; color: #6C757D;")
            layout.addWidget(val_label)
            layout.addWidget(title_label)
            frame._val_label = val_label
            return frame

        def _update_card(self, card: QFrame, value: str) -> None:
            try:
                card._val_label.setText(value)
            except Exception:
                pass

        def _on_refresh(self) -> None:
            if self._worker and self._worker.isRunning():
                return
            self._worker = GovernanceAlertsWorker(mode="real", tier="research30")
            self._worker.alerts_ready.connect(self._on_alerts_ready)
            self._worker.digest_ready.connect(self._on_digest_ready)
            self._worker.checklist_ready.connect(self._on_checklist_ready)
            self._worker.error_occurred.connect(self._on_worker_error)
            self._worker.start()
            self._btn_refresh.setEnabled(False)
            self._btn_refresh.setText("Refreshing...")

        def _on_alerts_ready(self, alerts) -> None:
            self._alerts = alerts
            self._populate_alert_table(alerts)
            self._update_summary_cards(alerts)
            self._btn_refresh.setEnabled(True)
            self._btn_refresh.setText("Refresh Alerts")
            self._load_trend()

        def _on_digest_ready(self, digest) -> None:
            self._digest = digest
            if digest:
                from governance_alerts.digest_builder import GovernanceDigestBuilder
                builder = GovernanceDigestBuilder()
                text = builder.render_markdown(digest)
                daily_widget = self._digest_tabs.widget(2)
                if daily_widget:
                    daily_widget.setPlainText(text)

        def _on_checklist_ready(self, checklist) -> None:
            self._checklist = checklist
            if checklist:
                self._populate_checklist_table(checklist)

        def _on_worker_error(self, msg: str) -> None:
            self._btn_refresh.setEnabled(True)
            self._btn_refresh.setText("Refresh Alerts")
            self._detail_text.setPlainText(f"[WARN] Refresh error: {msg}\n[!] Research Only. No Real Orders.")

        def _populate_alert_table(self, alerts) -> None:
            self._alert_table.setRowCount(0)
            if not alerts:
                return
            self._alert_table.setRowCount(len(alerts))
            priority_colors = {"P0": "#DC3545", "P1": "#FD7E14", "P2": "#FFC107", "P3": "#6C757D"}
            for row, alert in enumerate(alerts):
                cols = [
                    alert.priority,
                    alert.severity,
                    alert.alert_type,
                    alert.symbol or alert.source or "(system)",
                    alert.title[:60],
                    alert.status,
                    (alert.first_detected_at or "")[:10],
                    str(alert.occurrence_count),
                    alert.escalation_level,
                    ", ".join(alert.safe_actions[:2]) if alert.safe_actions else "REVIEW",
                ]
                for col, text in enumerate(cols):
                    item = QTableWidgetItem(str(text))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    if col == 0 and text in priority_colors:
                        item.setForeground(QColor(priority_colors[text]))
                    self._alert_table.setItem(row, col, item)

        def _populate_checklist_table(self, checklist) -> None:
            self._checklist_table.setRowCount(0)
            if not checklist or not checklist.items:
                return
            items = checklist.items
            self._checklist_table.setRowCount(len(items))
            for row, item in enumerate(items):
                cols = [
                    item.category,
                    item.title[:60],
                    "Yes" if item.required else "No",
                    item.status,
                    item.safe_action,
                    item.suggested_command[:40] if item.suggested_command else "",
                ]
                for col, text in enumerate(cols):
                    wi = QTableWidgetItem(str(text))
                    wi.setFlags(wi.flags() & ~Qt.ItemIsEditable)
                    self._checklist_table.setItem(row, col, wi)

        def _update_summary_cards(self, alerts) -> None:
            open_a = [a for a in alerts if a.status not in ("RESOLVED", "SUPPRESSED")]
            self._update_card(self._card_open, str(len(open_a)))
            self._update_card(self._card_p0, str(sum(1 for a in open_a if a.priority == "P0")))
            self._update_card(self._card_p1, str(sum(1 for a in open_a if a.priority == "P1")))
            self._update_card(self._card_escalated, str(sum(1 for a in alerts if a.status == "ESCALATED")))
            self._update_card(self._card_snoozed, str(sum(1 for a in alerts if a.status == "SNOOZED")))
            self._update_card(self._card_resolved, str(sum(1 for a in alerts if a.status == "RESOLVED")))
            self._update_card(self._card_reopened, str(sum(1 for a in alerts if a.status == "REOPENED")))
            self._update_card(self._card_audit, str(sum(1 for a in open_a if a.alert_type == "AUDIT_CHAIN_FAILURE")))

        def _on_alert_selected(self) -> None:
            rows = self._alert_table.selectedItems()
            if not rows:
                return
            row = self._alert_table.currentRow()
            if row < 0 or row >= len(self._alerts):
                return
            alert = self._alerts[row]
            detail = f"Alert ID: {alert.alert_id}\n"
            detail += f"Type: {alert.alert_type}\n"
            detail += f"Priority: {alert.priority} | Severity: {alert.severity}\n"
            detail += f"Status: {alert.status} | Occurrences: {alert.occurrence_count}\n"
            detail += f"Message: {alert.message}\n"
            if alert.reason_codes:
                detail += f"Reason Codes: {', '.join(alert.reason_codes)}\n"
            if alert.previous_state:
                detail += f"Previous State: {alert.previous_state}\n"
            if alert.current_state:
                detail += f"Current State: {alert.current_state}\n"
            if alert.suggested_commands:
                detail += f"Suggested Commands:\n"
                for cmd in alert.suggested_commands:
                    detail += f"  - python main.py {cmd}\n"
            detail += "\n[!] Research Only. No Real Orders."
            self._detail_text.setPlainText(detail)

        def _on_build_morning_digest(self) -> None:
            self._build_digest("morning", 0)

        def _on_build_eod_digest(self) -> None:
            self._build_digest("end-of-day", 1)

        def _build_digest(self, digest_type: str, tab_idx: int) -> None:
            try:
                from governance_alerts.digest_builder import GovernanceDigestBuilder
                builder = GovernanceDigestBuilder()
                if digest_type == "morning":
                    digest = builder.build_morning_digest(self._alerts)
                else:
                    digest = builder.build_end_of_day_digest(self._alerts)
                text = builder.render_markdown(digest)
                widget = self._digest_tabs.widget(tab_idx)
                if widget:
                    widget.setPlainText(text)
                self._tabs.setCurrentIndex(2)
            except Exception as exc:
                logger.warning("_build_digest: %s", exc)

        def _on_copy_safe_command(self) -> None:
            """Copy a safe command to clipboard. Only allowlist commands."""
            try:
                from PySide6.QtWidgets import QApplication
                cmd = "python main.py governance-alerts-health"
                QApplication.clipboard().setText(cmd)
                self._detail_text.append(f"\n[Copied] {cmd}\n[!] Research Only. No broker commands.")
            except Exception:
                try:
                    from PyQt5.QtWidgets import QApplication
                    cmd = "python main.py governance-alerts-health"
                    QApplication.clipboard().setText(cmd)
                except Exception as exc:
                    logger.warning("_on_copy_safe_command: %s", exc)

        def _on_export_report(self) -> None:
            try:
                from reports.governance_alerts_daily_operations_report import GovernanceAlertsDailyOperationsReportBuilder
                builder = GovernanceAlertsDailyOperationsReportBuilder()
                path = builder.build()
                if path:
                    self._detail_text.append(f"\n[Report] Written: {path}\n[!] Research Only.")
                else:
                    self._detail_text.append("\n[WARN] Report not generated.\n")
            except Exception as exc:
                self._detail_text.append(f"\n[ERROR] Export failed: {exc}\n")

        def _on_notification_preview(self) -> None:
            """Show local notification preview. No external send."""
            try:
                from governance_alerts.notification_preview import GovernanceNotificationPreview
                from governance_alerts.digest_builder import GovernanceDigestBuilder
                builder = GovernanceDigestBuilder()
                digest = builder.build_daily_digest(self._alerts)
                preview = GovernanceNotificationPreview()
                text = preview.preview_digest(digest, format="markdown")
                widget = self._digest_tabs.widget(2)
                if widget:
                    widget.setPlainText(text)
                self._tabs.setCurrentIndex(2)
                self._detail_text.append("\n[!] LOCAL PREVIEW ONLY — No external notification sent.\n")
            except Exception as exc:
                self._detail_text.append(f"\n[ERROR] Preview failed: {exc}\n")

        def _load_trend(self) -> None:
            try:
                from governance_alerts.alert_query import trend
                data = trend(days=7)
                lines = ["7-Day Alert Trend:", ""]
                lines.append(f"{'Date':<12} {'Total':<8} {'P0':<5} {'P1':<5} {'Audit'}")
                lines.append("-" * 40)
                for row in data:
                    lines.append(f"{row['date']:<12} {row['total']:<8} {row['p0']:<5} {row['p1']:<5} {row['audit_failures']}")
                lines.append("")
                lines.append("[!] Research Only. No Real Orders.")
                self._trend_text.setPlainText("\n".join(lines))
            except Exception as exc:
                self._trend_text.setPlainText(f"[WARN] Trend data unavailable: {exc}\n[!] Research Only.")
