"""
gui/coverage_repair_panel.py — CoverageRepairPanel for TW Quant Cockpit v1.1.2.

GUI panel for the Coverage Repair Workflow.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] dry_run=True default. Destructive repair disabled.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTextEdit, QSplitter, QTabWidget,
        QTableWidget, QTableWidgetItem, QHeaderView,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


class CoverageRepairPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """GUI panel for the Coverage Repair Workflow.

    Tabs: Detect | Plan | Execute | Health | Report

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    research_only  = True
    no_real_orders = True

    def __init__(self, mode: str = "real", parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
        self._mode = mode
        self._adapter = None
        if _PYSIDE6_AVAILABLE:
            self._init_ui()

    def _get_adapter(self):
        if self._adapter is None:
            try:
                from gui.coverage_repair_adapter import CoverageRepairAdapter
                self._adapter = CoverageRepairAdapter()
            except Exception as exc:
                logger.warning("CoverageRepairPanel: adapter unavailable: %s", exc)
        return self._adapter

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Safety banner
        banner = QLabel(
            "<b>[!] Coverage Repair Workflow v1.1.2</b> — Research Only. "
            "No Real Orders. dry_run=True default.<br>"
            "Destructive repair DISABLED. Conflict resolution is MANUAL. "
            "Synthetic OHLC repair DISABLED."
        )
        banner.setWordWrap(True)
        banner.setStyleSheet("color: #FF8888; background: #1A0A0A; padding: 4px;")
        layout.addWidget(banner)

        # Tabs
        tabs = QTabWidget()

        # --- Detect tab ---
        detect_widget = QWidget()
        detect_layout = QVBoxLayout(detect_widget)
        detect_btn = QPushButton("Detect Coverage Issues")
        self._detect_output = QTextEdit()
        self._detect_output.setReadOnly(True)
        detect_btn.clicked.connect(self._on_detect)
        detect_layout.addWidget(detect_btn)
        detect_layout.addWidget(self._detect_output)
        tabs.addTab(detect_widget, "Detect")

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
            "Use CLI with --allow-write to write data."
        )
        exec_note.setWordWrap(True)
        exec_note.setStyleSheet("color: #FF8888;")
        execute_btn = QPushButton("Execute Plan (dry-run)")
        self._execute_output = QTextEdit()
        self._execute_output.setReadOnly(True)
        execute_btn.clicked.connect(self._on_execute)
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

    # ----------------------------------------------------------------
    # Event handlers
    # ----------------------------------------------------------------

    def _on_detect(self) -> None:
        adapter = self._get_adapter()
        if adapter is None:
            self._detect_output.setPlainText("Coverage repair adapter unavailable.")
            return
        try:
            issues = adapter.detect()
            lines = [
                f"[!] Research Only. No Real Orders.",
                f"Issues detected: {len(issues)}",
                "",
            ]
            for issue in issues[:50]:
                lines.append(
                    f"  [{issue.get('issue_type')}] {issue.get('symbol')}/{issue.get('dataset')} "
                    f"— rows={issue.get('row_count')} — {issue.get('description', '')[:80]}"
                )
            if len(issues) > 50:
                lines.append(f"  ... ({len(issues) - 50} more)")
            self._detect_output.setPlainText("\n".join(lines))
        except Exception as exc:
            self._detect_output.setPlainText(f"[ERROR] {exc}")

    def _on_plan(self) -> None:
        adapter = self._get_adapter()
        if adapter is None:
            self._plan_output.setPlainText("Coverage repair adapter unavailable.")
            return
        try:
            plan = adapter.build_plan(dry_run=True)
            lines = [
                f"[!] Research Only. No Real Orders. dry_run=True",
                f"Plan ID:          {plan.get('plan_id', 'N/A')}",
                f"Total Issues:     {plan.get('total_issues', 0)}",
                f"Total Tasks:      {plan.get('total_tasks', 0)}",
                f"P0 (Critical):    {plan.get('p0_count', 0)}",
                f"P1 (High):        {plan.get('p1_count', 0)}",
                f"P2 (Medium):      {plan.get('p2_count', 0)}",
                f"P3 (Low):         {plan.get('p3_count', 0)}",
                f"AUTO_SAFE:        {plan.get('auto_safe_count', 0)}",
                f"MANUAL_REVIEW:    {plan.get('manual_review_count', 0)}",
                f"SOURCE_REQUIRED:  {plan.get('source_required_count', 0)}",
                f"BLOCKED:          {plan.get('blocked_count', 0)}",
            ]
            self._plan_output.setPlainText("\n".join(lines))
        except Exception as exc:
            self._plan_output.setPlainText(f"[ERROR] {exc}")

    def _on_execute(self) -> None:
        adapter = self._get_adapter()
        if adapter is None:
            self._execute_output.setPlainText("Coverage repair adapter unavailable.")
            return
        try:
            summary = adapter.execute(allow_write=False)  # GUI always dry-run
            lines = [
                f"[!] DRY RUN. No data modified.",
                f"[!] Research Only. No Real Orders.",
                f"Total Tasks:   {summary.get('total_tasks', 0)}",
                f"Succeeded:     {summary.get('succeeded', 0)}",
                f"Failed:        {summary.get('failed', 0)}",
                f"Skipped:       {summary.get('skipped', 0)}",
                f"Blocked:       {summary.get('blocked', 0)}",
                f"Manual Review: {summary.get('manual_review', 0)}",
                f"Dry Run:       {summary.get('dry_run', True)}",
            ]
            self._execute_output.setPlainText("\n".join(lines))
        except Exception as exc:
            self._execute_output.setPlainText(f"[ERROR] {exc}")

    def _on_health(self) -> None:
        adapter = self._get_adapter()
        if adapter is None:
            self._health_output.setPlainText("Coverage repair adapter unavailable.")
            return
        try:
            result = adapter.get_health()
            lines = [
                f"Overall: {result.get('overall', 'FAIL')}",
                f"Total:   {result.get('total', 0)}",
                f"Passed:  {result.get('passed', 0)}",
                f"Warned:  {result.get('warned', 0)}",
                f"Failed:  {result.get('failed', 0)}",
                "",
            ]
            for check, status in result.get("results", {}).items():
                icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}.get(status, "[?]")
                lines.append(f"  {icon} {check}")
            lines.append("")
            lines.append("[!] Research Only. No Real Orders.")
            self._health_output.setPlainText("\n".join(lines))
        except Exception as exc:
            self._health_output.setPlainText(f"[ERROR] {exc}")

    def _on_report(self) -> None:
        adapter = self._get_adapter()
        if adapter is None:
            self._report_output.setPlainText("Coverage repair adapter unavailable.")
            return
        try:
            path = adapter.build_report(mode=self._mode)
            if path:
                self._report_output.setPlainText(f"Report saved to:\n{path}\n\n[!] Research Only.")
            else:
                self._report_output.setPlainText("Report generation failed.")
        except Exception as exc:
            self._report_output.setPlainText(f"[ERROR] {exc}")
