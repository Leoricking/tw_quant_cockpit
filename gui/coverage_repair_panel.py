"""
gui/coverage_repair_panel.py — CoverageRepairPanel for TW Quant Cockpit v1.3.3.

GUI panel for the Coverage Repair Workflow.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True default. Destructive repair disabled.
[!] All actions are read-only from GUI. No auto-execution.
"""
from __future__ import annotations

import logging
import threading
from typing import Any, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
COVERAGE_REPAIR_AUTO_EXECUTION_ENABLED = False
COVERAGE_REPAIR_DESTRUCTIVE_ACTIONS_ENABLED = False

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTextEdit, QSplitter, QTabWidget,
        QTableWidget, QTableWidgetItem, QHeaderView,
        QLineEdit, QComboBox, QGroupBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


class CoverageRepairPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """GUI panel for the Coverage Repair Workflow v1.3.3.

    Tabs: Queue | Scan | Plan | Execute | Health | Report

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    [!] dry_run=True default. Destructive repair DISABLED.
    [!] Auto Execution DISABLED.
    """

    research_only = True
    no_real_orders = True
    production_trading_blocked = True

    def __init__(self, mode: str = "real", parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
        self._mode = mode
        self._worker: Optional[Any] = None
        if _PYSIDE6_AVAILABLE:
            self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Safety banner
        banner = QLabel(
            "<b>[!] Coverage Repair Workflow v1.3.3</b> — Research Only. "
            "No Real Orders. dry_run=True default.<br>"
            "Destructive Repair DISABLED. Conflict resolution is MANUAL. "
            "Auto Execution DISABLED. Production Trading BLOCKED."
        )
        banner.setWordWrap(True)
        banner.setStyleSheet("color: #FF8888; background: #1A0A0A; padding: 6px;")
        layout.addWidget(banner)

        # Filters row
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.addWidget(QLabel("Symbol:"))
        self._filter_symbol = QLineEdit()
        self._filter_symbol.setPlaceholderText("e.g. 2330")
        filter_layout.addWidget(self._filter_symbol)
        filter_layout.addWidget(QLabel("Profile:"))
        self._filter_profile = QComboBox()
        self._filter_profile.addItems(["(all)", "research", "backtest", "precise_price", "fundamental"])
        filter_layout.addWidget(self._filter_profile)
        filter_layout.addWidget(QLabel("Status:"))
        self._filter_status = QComboBox()
        self._filter_status.addItems(["(all)", "OPEN", "BLOCKED", "RESOLVED", "FAILED",
                                       "CONFLICT_REVIEW", "WAITING_SOURCE", "WAITING_AUTH"])
        filter_layout.addWidget(self._filter_status)
        layout.addWidget(filter_group)

        # Tabs
        tabs = QTabWidget()

        # --- Queue tab ---
        queue_widget = QWidget()
        queue_layout = QVBoxLayout(queue_widget)

        # Action buttons row
        btn_row = QHBoxLayout()
        for label, handler in [
            ("Scan Issues", self._on_scan),
            ("Build Tasks", self._on_build_tasks),
            ("Refresh Queue", self._on_refresh_queue),
            ("View Task", self._on_view_task),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            btn_row.addWidget(btn)
        queue_layout.addLayout(btn_row)

        btn_row2 = QHBoxLayout()
        for label, handler in [
            ("Build Dry Run Plan", self._on_plan),
            ("Run Safe Repair", self._on_run_repair),
            ("Retry", self._on_retry),
            ("Revalidate", self._on_revalidate),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            btn_row2.addWidget(btn)
        queue_layout.addLayout(btn_row2)

        btn_row3 = QHBoxLayout()
        for label, handler in [
            ("Mark Resolved", self._on_resolve),
            ("Ignore", self._on_ignore),
            ("Reopen", self._on_reopen),
            ("View History", self._on_history),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            btn_row3.addWidget(btn)
        queue_layout.addLayout(btn_row3)

        # Task table
        self._task_table = QTableWidget(0, 7)
        self._task_table.setHorizontalHeaderLabels([
            "Symbol", "Profile", "Issue Type", "Priority", "Status", "Provider", "Task ID"
        ])
        self._task_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        queue_layout.addWidget(self._task_table)
        tabs.addTab(queue_widget, "Queue")

        # --- Scan tab ---
        scan_widget = QWidget()
        scan_layout = QVBoxLayout(scan_widget)
        scan_btn = QPushButton("Scan for Coverage Issues")
        self._scan_output = QTextEdit()
        self._scan_output.setReadOnly(True)
        scan_btn.clicked.connect(self._on_scan)
        scan_layout.addWidget(scan_btn)
        scan_layout.addWidget(self._scan_output)
        tabs.addTab(scan_widget, "Scan")

        # --- Plan tab ---
        plan_widget = QWidget()
        plan_layout = QVBoxLayout(plan_widget)
        plan_btn = QPushButton("Build Repair Plan (dry_run=True)")
        self._plan_output = QTextEdit()
        self._plan_output.setReadOnly(True)
        plan_btn.clicked.connect(self._on_plan)
        plan_layout.addWidget(plan_btn)
        plan_layout.addWidget(self._plan_output)
        tabs.addTab(plan_widget, "Plan")

        # --- Execute tab ---
        execute_widget = QWidget()
        execute_layout = QVBoxLayout(execute_widget)
        exec_note = QLabel(
            "[!] Execute is dry-run only from GUI. "
            "Auto Execution DISABLED. No Real Orders. Production Trading BLOCKED."
        )
        exec_note.setWordWrap(True)
        exec_note.setStyleSheet("color: #FF8888;")
        execute_btn = QPushButton("Execute Plan (dry-run, read-only)")
        self._execute_output = QTextEdit()
        self._execute_output.setReadOnly(True)
        execute_btn.clicked.connect(self._on_run_repair)
        execute_layout.addWidget(exec_note)
        execute_layout.addWidget(execute_btn)
        execute_layout.addWidget(self._execute_output)
        tabs.addTab(execute_widget, "Execute")

        # --- Health tab ---
        health_widget = QWidget()
        health_layout = QVBoxLayout(health_widget)
        health_btn = QPushButton("Run Health Check")
        self._health_output = QTextEdit()
        self._health_output.setReadOnly(True)
        health_btn.clicked.connect(self._on_health)
        health_layout.addWidget(health_btn)
        health_layout.addWidget(self._health_output)
        tabs.addTab(health_widget, "Health")

        # --- Report tab ---
        report_widget = QWidget()
        report_layout = QVBoxLayout(report_widget)
        report_btn = QPushButton("Build Coverage Repair Report")
        self._report_output = QTextEdit()
        self._report_output.setReadOnly(True)
        report_btn.clicked.connect(self._on_report)
        report_layout.addWidget(report_btn)
        report_layout.addWidget(self._report_output)
        tabs.addTab(report_widget, "Report")

        layout.addWidget(tabs)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_scan(self) -> None:
        output = getattr(self, "_scan_output", None)
        try:
            from coverage_repair.issue_mapper import CoverageRepairIssueMapper
            mapper = CoverageRepairIssueMapper()
            msg = (
                "[!] Research Only. No Real Orders.\n"
                "[!] Auto Execution DISABLED. dry_run=True.\n"
                "Scan initiated. Connect coverage data source for full scan.\n"
                "No tasks auto-added to queue from GUI scan."
            )
            if output:
                output.setPlainText(msg)
        except Exception as exc:
            if output:
                output.setPlainText(f"[ERROR] {exc}")

    def _on_build_tasks(self) -> None:
        try:
            from coverage_repair.queue import CoverageRepairQueue
            q = CoverageRepairQueue()
            summary = q.summarize()
            msg = (
                f"[!] Research Only. No Real Orders.\n"
                f"Queue Summary:\n"
                f"  Total: {summary['total']}\n"
                f"  Open: {summary['open']}\n"
                f"  Blocked: {summary['blocked']}\n"
                f"  Resolved: {summary['resolved']}\n"
                "No tasks auto-built from GUI. Use CLI coverage-repair-scan."
            )
            if hasattr(self, "_scan_output"):
                self._scan_output.setPlainText(msg)
        except Exception as exc:
            if hasattr(self, "_scan_output"):
                self._scan_output.setPlainText(f"[ERROR] {exc}")

    def _on_refresh_queue(self) -> None:
        try:
            from coverage_repair.queue import CoverageRepairQueue
            q = CoverageRepairQueue()
            tasks = q.list_tasks()
            if hasattr(self, "_task_table"):
                self._task_table.setRowCount(len(tasks))
                for row, t in enumerate(tasks[:200]):
                    self._task_table.setItem(row, 0, QTableWidgetItem(t.symbol))
                    self._task_table.setItem(row, 1, QTableWidgetItem(t.profile))
                    self._task_table.setItem(row, 2, QTableWidgetItem(t.issue_type))
                    self._task_table.setItem(row, 3, QTableWidgetItem(t.priority))
                    self._task_table.setItem(row, 4, QTableWidgetItem(t.status))
                    self._task_table.setItem(row, 5, QTableWidgetItem(t.provider_id or ""))
                    self._task_table.setItem(row, 6, QTableWidgetItem(t.task_id))
        except Exception as exc:
            logger.warning("_on_refresh_queue: %s", exc)

    def _on_view_task(self) -> None:
        try:
            from coverage_repair.queue import CoverageRepairQueue
            q = CoverageRepairQueue()
            tasks = q.list_tasks()
            if not tasks:
                if hasattr(self, "_plan_output"):
                    self._plan_output.setPlainText("No tasks in queue.")
                return
            t = tasks[0]  # view first
            lines = [
                f"[!] Research Only. No Real Orders.",
                f"Task ID        : {t.task_id}",
                f"Symbol         : {t.symbol}",
                f"Issue Type     : {t.issue_type}",
                f"Priority       : {t.priority}",
                f"Status         : {t.status}",
                f"Provider       : {t.provider_id or '(none)'}",
                f"Selected Action: {t.selected_action}",
                f"Retryable      : {t.retryable}",
                f"No Real Orders : True",
                f"Prod Blocked   : True",
            ]
            if hasattr(self, "_plan_output"):
                self._plan_output.setPlainText("\n".join(lines))
        except Exception as exc:
            if hasattr(self, "_plan_output"):
                self._plan_output.setPlainText(f"[ERROR] {exc}")

    def _on_plan(self) -> None:
        output = getattr(self, "_plan_output", None)
        try:
            from coverage_repair.queue import CoverageRepairQueue
            from coverage_repair.planner import CoverageRepairPlanner
            q = CoverageRepairQueue()
            tasks = q.list_open()
            if not tasks:
                if output:
                    output.setPlainText("[!] No open tasks. Run scan first.\n[!] Research Only.")
                return
            planner = CoverageRepairPlanner()
            plan = planner.build_plan(tasks[0])
            summary = planner.summarize_plan(plan)
            if output:
                output.setPlainText(f"[!] dry_run=True | No Real Orders\n\n{summary}")
        except Exception as exc:
            if output:
                output.setPlainText(f"[ERROR] {exc}")

    def _on_run_repair(self) -> None:
        output = getattr(self, "_execute_output", None)
        try:
            from coverage_repair.queue import CoverageRepairQueue
            from coverage_repair.planner import CoverageRepairPlanner
            from coverage_repair.executor import CoverageRepairExecutor
            q = CoverageRepairQueue()
            tasks = q.list_open()
            if not tasks:
                if output:
                    output.setPlainText("[!] No open tasks to execute.\n[!] Research Only.")
                return
            planner = CoverageRepairPlanner()
            executor = CoverageRepairExecutor()
            plan = planner.build_plan(tasks[0])
            result = executor.execute(plan)
            lines = [
                "[!] DRY RUN. No data modified.",
                "[!] Research Only. No Real Orders.",
                f"Execution ID   : {result.execution_id}",
                f"Status         : {result.status}",
                f"Action         : {result.action}",
                f"Resolved       : {result.resolved}",
                f"Dry Run        : True",
                f"No Real Orders : True",
                f"Prod Blocked   : True",
            ]
            if result.errors:
                for e in result.errors:
                    lines.append(f"[ERROR] {e}")
            if result.warnings:
                for w in result.warnings:
                    lines.append(f"[WARN] {w}")
            if output:
                output.setPlainText("\n".join(lines))
        except Exception as exc:
            if output:
                output.setPlainText(f"[ERROR] {exc}")

    def _on_retry(self) -> None:
        if hasattr(self, "_execute_output"):
            self._execute_output.setPlainText(
                "[!] Retry: Select a task in the queue and use CLI coverage-repair-retry --task-id ...\n"
                "[!] Research Only. No Real Orders."
            )

    def _on_revalidate(self) -> None:
        if hasattr(self, "_execute_output"):
            self._execute_output.setPlainText(
                "[!] Revalidate: Use CLI coverage-repair-revalidate --task-id ...\n"
                "[!] Research Only. No Real Orders."
            )

    def _on_resolve(self) -> None:
        if hasattr(self, "_execute_output"):
            self._execute_output.setPlainText(
                "[!] Mark Resolved: Use CLI coverage-repair-resolve --task-id ...\n"
                "[!] Research Only. No Real Orders."
            )

    def _on_ignore(self) -> None:
        if hasattr(self, "_execute_output"):
            self._execute_output.setPlainText(
                "[!] Ignore: Use CLI coverage-repair-ignore --task-id ...\n"
                "[!] Research Only. No Real Orders."
            )

    def _on_reopen(self) -> None:
        if hasattr(self, "_execute_output"):
            self._execute_output.setPlainText(
                "[!] Reopen: Use CLI coverage-repair-reopen --task-id ...\n"
                "[!] Research Only. No Real Orders."
            )

    def _on_history(self) -> None:
        if hasattr(self, "_execute_output"):
            self._execute_output.setPlainText(
                "[!] History: Use CLI coverage-repair-history --task-id ...\n"
                "[!] Research Only. No Real Orders."
            )

    def _on_health(self) -> None:
        output = getattr(self, "_health_output", None)
        try:
            from coverage_repair.health import CoverageRepairHealthV133
            hc = CoverageRepairHealthV133()
            summary = hc.get_health_summary()
            lines = [
                f"Overall  : {'PASS' if summary.get('all_pass') else 'FAIL'}",
                f"Total    : {summary.get('total_checks', 0)}",
                f"Passed   : {summary.get('passed', 0)}",
                f"Failed   : {summary.get('failed', 0)}",
                "",
            ]
            for check, info in (summary.get("results") or {}).items():
                st = info.get("status", "?")
                icon = "[PASS]" if st == "PASS" else "[FAIL]"
                lines.append(f"  {icon} {check}")
            lines.append("")
            lines.append("[!] Research Only. No Real Orders.")
            if output:
                output.setPlainText("\n".join(lines))
        except Exception as exc:
            if output:
                output.setPlainText(f"[ERROR] {exc}")

    def _on_report(self) -> None:
        output = getattr(self, "_report_output", None)
        try:
            from coverage_repair.queue import CoverageRepairQueue
            from coverage_repair.report import CoverageRepairReport
            q = CoverageRepairQueue()
            reporter = CoverageRepairReport()
            report_dict = reporter.generate(queue=q)
            text = reporter.format_text(report_dict)
            if output:
                output.setPlainText(text)
        except Exception as exc:
            if output:
                output.setPlainText(f"[ERROR] {exc}")

    def closeEvent(self, event) -> None:
        """Ensure no QThread leaks on close."""
        if self._worker is not None:
            try:
                if hasattr(self._worker, "quit"):
                    self._worker.quit()
                if hasattr(self._worker, "wait"):
                    self._worker.wait(2000)
            except Exception:
                pass
            self._worker = None
        if _PYSIDE6_AVAILABLE:
            super().closeEvent(event)
