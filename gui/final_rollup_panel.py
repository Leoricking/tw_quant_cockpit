"""
gui/final_rollup_panel.py — Final Maintenance Rollup GUI panel for TW Quant Cockpit v1.0.9.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] GUI UX only. VALIDATED does not enable trading. No external API.
"""
from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
        QGroupBox, QScrollArea, QSizePolicy,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


class FinalRollupPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Final Maintenance Rollup GUI panel.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    Displays: Safety Banner, Release History, Health Checks, Maintenance Plan.
    """

    no_real_orders = True
    production_blocked = True

    def __init__(self, parent=None, project_root: Optional[str] = None) -> None:
        if not _PYSIDE6_AVAILABLE:
            logger.warning("PySide6 not available — FinalRollupPanel running in headless mode")
            return
        super().__init__(parent)
        self._root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._adapter = None
        try:
            from gui.final_rollup_adapter import FinalRollupAdapter
            self._adapter = FinalRollupAdapter(project_root=self._root)
        except Exception as exc:
            logger.warning("FinalRollupPanel: adapter unavailable: %s", exc)
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        layout = QVBoxLayout(self)

        # A. Safety Banner
        banner = QLabel(
            "⚠ Final Maintenance Rollup  |  Research Only  |  No Real Orders  |  "
            "Production Trading BLOCKED  |  External API Disabled"
        )
        banner.setStyleSheet(
            "background: #1a1a2e; color: #e8c547; padding: 6px; font-weight: bold; font-size: 11px;"
        )
        banner.setWordWrap(True)
        layout.addWidget(banner)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self._build_history_tab(), "Release History")
        tabs.addTab(self._build_health_tab(), "Health Check")
        tabs.addTab(self._build_plan_tab(), "Maintenance Plan")
        layout.addWidget(tabs)

        # E. Buttons
        btn_layout = QHBoxLayout()
        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.refresh)
        btn_report = QPushButton("Build Report")
        btn_report.clicked.connect(self._build_report)
        btn_copy_plan = QPushButton("Copy Maintenance Plan")
        btn_copy_plan.clicked.connect(self._copy_plan)
        btn_copy_summary = QPushButton("Copy Final Summary")
        btn_copy_summary.clicked.connect(self._copy_summary)
        btn_layout.addWidget(btn_refresh)
        btn_layout.addWidget(btn_report)
        btn_layout.addWidget(btn_copy_plan)
        btn_layout.addWidget(btn_copy_summary)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _build_history_tab(self) -> QWidget:
        if not _PYSIDE6_AVAILABLE:
            return None
        w = QWidget()
        layout = QVBoxLayout(w)
        # B. Release History Table
        cols = ["Version", "Title", "Commit", "Tag", "Summary", "Safety"]
        self._history_table = QTableWidget(0, len(cols))
        self._history_table.setHorizontalHeaderLabels(cols)
        self._history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self._history_table)
        return w

    def _build_health_tab(self) -> QWidget:
        if not _PYSIDE6_AVAILABLE:
            return None
        w = QWidget()
        layout = QVBoxLayout(w)
        # C. Final Health Table
        cols = ["Check", "Status", "Reason"]
        self._health_table = QTableWidget(0, len(cols))
        self._health_table.setHorizontalHeaderLabels(cols)
        self._health_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._health_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self._health_table)
        return w

    def _build_plan_tab(self) -> QWidget:
        if not _PYSIDE6_AVAILABLE:
            return None
        w = QWidget()
        layout = QVBoxLayout(w)
        # D. Maintenance Plan Table
        cols = ["Cadence", "Task", "Command", "Expected Result", "Safe Action"]
        self._plan_table = QTableWidget(0, len(cols))
        self._plan_table.setHorizontalHeaderLabels(cols)
        self._plan_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._plan_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self._plan_table)
        return w

    def refresh(self) -> None:
        if not _PYSIDE6_AVAILABLE or self._adapter is None:
            return
        try:
            # Update history
            history = self._adapter.get_release_history()
            self._history_table.setRowCount(len(history))
            for i, e in enumerate(history):
                self._history_table.setItem(i, 0, QTableWidgetItem(e.get("version", "")))
                self._history_table.setItem(i, 1, QTableWidgetItem(e.get("title", "")))
                self._history_table.setItem(i, 2, QTableWidgetItem(e.get("commit", "")))
                self._history_table.setItem(i, 3, QTableWidgetItem(e.get("tag", "")))
                self._history_table.setItem(i, 4, QTableWidgetItem(e.get("summary", "")[:60]))
                self._history_table.setItem(i, 5, QTableWidgetItem(e.get("safety_status", "")))
            # Update health
            checks = self._adapter.get_health_checks()
            self._health_table.setRowCount(len(checks))
            for i, c in enumerate(checks):
                self._health_table.setItem(i, 0, QTableWidgetItem(c.get("name", "")))
                self._health_table.setItem(i, 1, QTableWidgetItem(c.get("status", "")))
                self._health_table.setItem(i, 2, QTableWidgetItem((c.get("detail") or "")[:80]))
            # Update plan
            plan = self._adapter.get_maintenance_plan()
            self._plan_table.setRowCount(len(plan))
            for i, t in enumerate(plan):
                self._plan_table.setItem(i, 0, QTableWidgetItem(t.get("cadence", "")))
                self._plan_table.setItem(i, 1, QTableWidgetItem(t.get("title", "")))
                self._plan_table.setItem(i, 2, QTableWidgetItem(t.get("command", "")))
                self._plan_table.setItem(i, 3, QTableWidgetItem(t.get("expected_result", "")))
                self._plan_table.setItem(i, 4, QTableWidgetItem(t.get("safe_action", "")))
        except Exception as exc:
            logger.warning("FinalRollupPanel.refresh: %s", exc)

    def _build_report(self) -> None:
        try:
            from reports.final_maintenance_rollup_report import FinalMaintenanceRollupReportBuilder
            builder = FinalMaintenanceRollupReportBuilder(project_root=self._root)
            path = builder.save()
            logger.info("Final rollup report saved: %s", path)
        except Exception as exc:
            logger.warning("FinalRollupPanel._build_report: %s", exc)

    def _copy_plan(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        try:
            from PySide6.QtWidgets import QApplication
            plan = self._adapter.get_maintenance_plan() if self._adapter else []
            lines = []
            for t in plan:
                lines.append(f"[{t.get('cadence','')}] {t.get('title','')}: {t.get('command','')}")
            QApplication.clipboard().setText("\n".join(lines))
        except Exception as exc:
            logger.warning("FinalRollupPanel._copy_plan: %s", exc)

    def _copy_summary(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        try:
            from PySide6.QtWidgets import QApplication
            summary = self._adapter.get_summary() if self._adapter else {}
            lines = [
                "TW Quant Cockpit — Final Maintenance Rollup",
                f"Version: {summary.get('version', '1.0.9')}",
                f"Release: {summary.get('release', 'Final Maintenance Rollup')}",
                f"Research Only: True",
                f"No Real Orders: True",
                f"Production Trading BLOCKED: True",
                f"v1.0 Maintenance Line Complete: True",
                f"Long-term Maintenance Ready: True",
            ]
            QApplication.clipboard().setText("\n".join(lines))
        except Exception as exc:
            logger.warning("FinalRollupPanel._copy_summary: %s", exc)
