"""
gui/strategy_lab_panel.py — StrategyLabPanel v0.9.0

PySide6 GUI tab for Strategy Lab Stable.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
[!] Not Investment Advice. No BUY/SELL/ORDER output.
[!] Does NOT modify any module status, weights, memory, coach tasks,
    metrics, or evidence graph.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    from PySide6.QtWidgets import (
        QGroupBox, QHBoxLayout, QHeaderView, QLabel, QMessageBox,
        QPushButton, QSplitter, QTableWidget, QTableWidgetItem,
        QTextEdit, QVBoxLayout, QWidget,
    )
    _PYSIDE6 = True
except ImportError:
    _PYSIDE6 = False
    # Stub base class so the module still imports
    class QWidget:  # type: ignore
        pass
    class QThread:  # type: ignore
        pass

_SAFE_STATUS_COLORS = {
    "STABLE":  "#27ae60",
    "USABLE":  "#2980b9",
    "PARTIAL": "#f39c12",
    "WARNING": "#e67e22",
    "BLOCKED": "#e74c3c",
    "PASS":    "#27ae60",
    "WARN":    "#f39c12",
    "FAIL":    "#e74c3c",
    "INFO":    "#95a5a6",
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ===========================================================================
# Background workers
# ===========================================================================

if _PYSIDE6:
    class _ValidationWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, mode: str = "real") -> None:
            super().__init__()
            self._mode = mode

        def run(self) -> None:
            try:
                from gui.strategy_lab_adapter import StrategyLabAdapter
                adapter = StrategyLabAdapter()
                result  = adapter.run_validation(mode=self._mode)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ReportWorker(QThread):
        finished = Signal(str)
        error    = Signal(str)

        def __init__(self, mode: str = "real") -> None:
            super().__init__()
            self._mode = mode

        def run(self) -> None:
            try:
                from gui.strategy_lab_adapter import StrategyLabAdapter
                adapter = StrategyLabAdapter()
                path    = adapter.generate_report(mode=self._mode)
                self.finished.emit(path)
            except Exception as exc:
                self.error.emit(str(exc))

    class _ManifestWorker(QThread):
        finished = Signal(dict)
        error    = Signal(str)

        def run(self) -> None:
            try:
                from gui.strategy_lab_adapter import StrategyLabAdapter
                adapter = StrategyLabAdapter()
                result  = adapter.build_manifest()
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))


# ===========================================================================
# Main Panel
# ===========================================================================

class StrategyLabPanel(QWidget):
    """Strategy Lab Stable GUI tab — v0.9.0.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    if _PYSIDE6:
        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self._validation_worker: "_ValidationWorker | None" = None
            self._report_worker:     "_ReportWorker | None"     = None
            self._manifest_worker:   "_ManifestWorker | None"   = None
            self._setup_ui()
            self._load_existing()

        def _setup_ui(self) -> None:
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            # A. Header / Safety Banner
            root.addWidget(self._build_header())

            # B. Summary Cards
            self._cards_widget = self._build_cards_placeholder()
            root.addWidget(self._cards_widget)

            # C-F. Main splitter: left=tabs, right=detail
            splitter = QSplitter(Qt.Horizontal)

            left = QWidget()
            left_layout = QVBoxLayout(left)
            left_layout.setContentsMargins(0, 0, 0, 0)
            left_layout.setSpacing(4)

            # C. Capability Matrix table
            cap_group = QGroupBox("Capability Matrix")
            cap_vbox  = QVBoxLayout(cap_group)
            self._cap_table = self._make_table(
                ["Capability", "Category", "Status", "Maturity", "CLI", "GUI", "Limitation"])
            cap_vbox.addWidget(self._cap_table)
            left_layout.addWidget(cap_group)

            # D. Checklist table
            chk_group = QGroupBox("Stable Checklist")
            chk_vbox  = QVBoxLayout(chk_group)
            self._chk_table = self._make_table(
                ["Category", "Check", "Status", "Severity", "Message", "Suggested Fix"])
            chk_vbox.addWidget(self._chk_table)
            left_layout.addWidget(chk_group)

            splitter.addWidget(left)

            # Right panel
            right       = QWidget()
            right_layout = QVBoxLayout(right)
            right_layout.setContentsMargins(0, 0, 0, 0)
            right_layout.setSpacing(4)

            # E. Safety Audit
            safety_group = QGroupBox("Safety Audit")
            safety_vbox  = QVBoxLayout(safety_group)
            self._safety_text = QTextEdit()
            self._safety_text.setReadOnly(True)
            self._safety_text.setMaximumHeight(140)
            self._safety_text.setPlaceholderText(
                "Run Strategy Lab Validation to populate safety audit.")
            safety_vbox.addWidget(self._safety_text)
            right_layout.addWidget(safety_group)

            # F. Layer Status Panel
            layer_group = QGroupBox("Layer Status")
            layer_vbox  = QVBoxLayout(layer_group)
            self._layer_text = QTextEdit()
            self._layer_text.setReadOnly(True)
            self._layer_text.setMaximumHeight(160)
            self._layer_text.setPlaceholderText("Layer status will appear after validation.")
            layer_vbox.addWidget(self._layer_text)
            right_layout.addWidget(layer_group)

            # G. Report / Manifest Panel
            rpt_group = QGroupBox("Reports & Manifest")
            rpt_vbox  = QVBoxLayout(rpt_group)
            self._rpt_text = QTextEdit()
            self._rpt_text.setReadOnly(True)
            self._rpt_text.setMaximumHeight(100)
            self._rpt_text.setPlaceholderText("Report and manifest paths will appear here.")
            rpt_vbox.addWidget(self._rpt_text)
            right_layout.addWidget(rpt_group)
            right_layout.addStretch()

            splitter.addWidget(right)
            splitter.setStretchFactor(0, 3)
            splitter.setStretchFactor(1, 2)
            root.addWidget(splitter)

            # H. Actions bar
            root.addWidget(self._build_actions())

        def _build_header(self) -> QWidget:
            w = QWidget()
            w.setStyleSheet("background: #1a1a2e; border-radius: 4px;")
            h = QVBoxLayout(w)
            h.setContentsMargins(12, 8, 12, 8)

            title_lbl = QLabel("Strategy Lab Stable  v0.9.0")
            title_font = QFont()
            title_font.setBold(True)
            title_font.setPointSize(13)
            title_lbl.setFont(title_font)
            title_lbl.setStyleSheet("color: #ecf0f1;")

            banner = QLabel(
                "[!] Research Only  |  No Real Orders  |  Production Trading BLOCKED  "
                "|  Not Investment Advice"
            )
            banner.setStyleSheet("color: #e74c3c; font-size: 11px;")

            h.addWidget(title_lbl)
            h.addWidget(banner)
            return w

        def _build_cards_placeholder(self) -> QWidget:
            w = QWidget()
            h = QHBoxLayout(w)
            h.setContentsMargins(0, 0, 0, 0)
            h.setSpacing(4)
            self._card_labels: dict = {}
            card_defs = [
                ("overall_status", "Overall Status", "—"),
                ("total_capabilities", "Capabilities", "—"),
                ("stable_count", "Stable", "—"),
                ("pass_count", "Checks PASS", "—"),
                ("warn_count", "Warnings", "—"),
                ("forbidden_action_count", "Forbidden Actions", "0"),
                ("no_real_orders", "No Real Orders", "YES"),
                ("production_blocked", "Production Blocked", "YES"),
            ]
            for key, title, default in card_defs:
                card = QGroupBox(title)
                card.setFixedWidth(105)
                vbox = QVBoxLayout(card)
                lbl  = QLabel(default)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFont(QFont("monospace", 10, QFont.Bold))
                vbox.addWidget(lbl)
                h.addWidget(card)
                self._card_labels[key] = lbl
            h.addStretch()
            return w

        def _update_cards(self, summary) -> None:
            if summary is None:
                return
            mapping = {
                "overall_status":         str(getattr(summary, "overall_status", "—")),
                "total_capabilities":     str(getattr(summary, "total_capabilities", "—")),
                "stable_count":           str(getattr(summary, "stable_count", "—")),
                "pass_count":             str(getattr(summary, "pass_count", "—")),
                "warn_count":             str(getattr(summary, "warn_count", "—")),
                "forbidden_action_count": str(getattr(summary, "forbidden_action_count", 0)),
                "no_real_orders":         "YES" if getattr(summary, "no_real_orders", True) else "NO",
                "production_blocked":     "YES" if getattr(summary, "production_blocked", True) else "NO",
            }
            for key, val in mapping.items():
                if key in self._card_labels:
                    self._card_labels[key].setText(val)
                    color = _SAFE_STATUS_COLORS.get(val, "#ecf0f1")
                    self._card_labels[key].setStyleSheet(f"color: {color};")

        def _make_table(self, headers: list) -> QTableWidget:
            t = QTableWidget(0, len(headers))
            t.setHorizontalHeaderLabels(headers)
            t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            t.setEditTriggers(QTableWidget.NoEditTriggers)
            t.setAlternatingRowColors(True)
            t.setSelectionBehavior(QTableWidget.SelectRows)
            return t

        def _build_actions(self) -> QWidget:
            w = QWidget()
            h = QHBoxLayout(w)
            h.setContentsMargins(0, 0, 0, 0)

            self._run_btn    = QPushButton("Run Strategy Lab Validation")
            self._report_btn = QPushButton("Generate Stable Report")
            self._manifest_btn = QPushButton("Build Manifest")
            self._refresh_btn = QPushButton("Refresh")
            self._open_rpt_btn = QPushButton("Open Latest Report")

            self._run_btn.clicked.connect(self._on_run_validation)
            self._report_btn.clicked.connect(self._on_generate_report)
            self._manifest_btn.clicked.connect(self._on_build_manifest)
            self._refresh_btn.clicked.connect(self._load_existing)
            self._open_rpt_btn.clicked.connect(self._on_open_report)

            for btn in [self._run_btn, self._report_btn, self._manifest_btn,
                        self._refresh_btn, self._open_rpt_btn]:
                h.addWidget(btn)
            h.addStretch()

            safety = QLabel("[!] No Real Orders  |  Research Only  |  Not Investment Advice")
            safety.setStyleSheet("color: #e74c3c; font-size: 10px;")
            h.addWidget(safety)
            return w

        # ------------------------------------------------------------------
        # Action handlers
        # ------------------------------------------------------------------

        def _on_run_validation(self) -> None:
            self._run_btn.setEnabled(False)
            self._run_btn.setText("Running…")
            self._validation_worker = _ValidationWorker(mode="real")
            self._validation_worker.finished.connect(self._on_validation_done)
            self._validation_worker.error.connect(self._on_worker_error)
            self._validation_worker.start()

        def _on_validation_done(self, result: dict) -> None:
            self._run_btn.setEnabled(True)
            self._run_btn.setText("Run Strategy Lab Validation")
            summary = result.get("summary")
            caps    = result.get("capabilities", [])
            checks  = result.get("checks", [])
            self._update_cards(summary)
            self._populate_cap_table(caps)
            self._populate_chk_table(checks)
            self._update_safety_text(summary)
            self._update_layer_text(caps)
            self._update_report_text()

        def _on_generate_report(self) -> None:
            self._report_btn.setEnabled(False)
            self._report_btn.setText("Generating…")
            self._report_worker = _ReportWorker(mode="real")
            self._report_worker.finished.connect(self._on_report_done)
            self._report_worker.error.connect(self._on_worker_error)
            self._report_worker.start()

        def _on_report_done(self, path: str) -> None:
            self._report_btn.setEnabled(True)
            self._report_btn.setText("Generate Stable Report")
            self._update_report_text()
            if path:
                QMessageBox.information(self, "Report Generated", f"Report saved:\n{path}")

        def _on_build_manifest(self) -> None:
            self._manifest_btn.setEnabled(False)
            self._manifest_btn.setText("Building…")
            self._manifest_worker = _ManifestWorker()
            self._manifest_worker.finished.connect(self._on_manifest_done)
            self._manifest_worker.error.connect(self._on_worker_error)
            self._manifest_worker.start()

        def _on_manifest_done(self, result: dict) -> None:
            self._manifest_btn.setEnabled(True)
            self._manifest_btn.setText("Build Manifest")
            self._update_report_text()

        def _on_open_report(self) -> None:
            try:
                from gui.strategy_lab_adapter import StrategyLabAdapter
                path = StrategyLabAdapter().load_latest_report_path()
                if path and os.path.isfile(path):
                    import subprocess, sys
                    if sys.platform == "win32":
                        os.startfile(path)
                    else:
                        subprocess.Popen(["xdg-open", path])
                else:
                    QMessageBox.information(self, "No Report",
                        "No report found. Run 'Generate Stable Report' first.")
            except Exception as exc:
                QMessageBox.warning(self, "Error", str(exc))

        def _on_worker_error(self, msg: str) -> None:
            self._run_btn.setEnabled(True)
            self._run_btn.setText("Run Strategy Lab Validation")
            self._report_btn.setEnabled(True)
            self._report_btn.setText("Generate Stable Report")
            self._manifest_btn.setEnabled(True)
            self._manifest_btn.setText("Build Manifest")
            QMessageBox.warning(self, "Worker Error", f"Error: {msg}")

        # ------------------------------------------------------------------
        # Populate helpers
        # ------------------------------------------------------------------

        def _load_existing(self) -> None:
            try:
                from gui.strategy_lab_adapter import StrategyLabAdapter
                adapter = StrategyLabAdapter()
                summary = adapter.load_latest_summary()
                caps    = adapter.load_capabilities()
                checks  = adapter.load_checks()
                if summary:
                    self._update_cards(summary)
                if caps:
                    self._populate_cap_table(caps)
                if checks:
                    self._populate_chk_table(checks)
                self._update_safety_text(summary)
                self._update_layer_text(caps)
                self._update_report_text()
            except Exception as exc:
                logger.debug("StrategyLabPanel._load_existing: %s", exc)

        def _populate_cap_table(self, capabilities: list) -> None:
            self._cap_table.setRowCount(0)
            for cap in capabilities:
                row = self._cap_table.rowCount()
                self._cap_table.insertRow(row)
                name = getattr(cap, "name", str(cap))
                cat  = getattr(cap, "category", "")
                st   = getattr(cap, "stable_status", "")
                mat  = getattr(cap, "maturity", "")
                cli  = (getattr(cap, "cli_commands", [""])[0][:30]
                        if getattr(cap, "cli_commands", []) else "—")
                gui_ = (getattr(cap, "gui_tabs", [""])[0][:20]
                        if getattr(cap, "gui_tabs", []) else "—")
                lim  = (getattr(cap, "known_limitations", [""])[0][:40]
                        if getattr(cap, "known_limitations", []) else "—")
                for col, val in enumerate([name, cat, st, mat, cli, gui_, lim]):
                    item = QTableWidgetItem(str(val))
                    if col == 2:
                        color = _SAFE_STATUS_COLORS.get(val, "#ecf0f1")
                        item.setForeground(QColor(color))
                    self._cap_table.setItem(row, col, item)

        def _populate_chk_table(self, checks: list) -> None:
            self._chk_table.setRowCount(0)
            for chk in checks:
                row = self._chk_table.rowCount()
                self._chk_table.insertRow(row)
                cat  = getattr(chk, "category", "")
                name = getattr(chk, "name", str(chk))
                st   = getattr(chk, "status", "")
                sev  = getattr(chk, "severity", "")
                msg  = getattr(chk, "message", "")[:80]
                fix  = getattr(chk, "suggested_fix", "")[:60]
                for col, val in enumerate([cat, name, st, sev, msg, fix]):
                    item = QTableWidgetItem(str(val))
                    if col == 2:
                        color = _SAFE_STATUS_COLORS.get(val, "#ecf0f1")
                        item.setForeground(QColor(color))
                    self._chk_table.setItem(row, col, item)

        def _update_safety_text(self, summary) -> None:
            if summary is None:
                self._safety_text.setPlaceholderText(
                    "No data — run: python main.py strategy-lab --mode real")
                return
            lines = [
                f"Recommendations Safe:    {getattr(summary, 'recommendations_safe', True)}",
                f"Memories Safe:           {getattr(summary, 'memories_safe', True)}",
                f"Coach Tasks Safe:        {getattr(summary, 'coach_tasks_safe', True)}",
                f"Training Metrics Safe:   {getattr(summary, 'metrics_safe', True)}",
                f"Evidence Graph Safe:     {getattr(summary, 'evidence_graph_safe', True)}",
                f"Forbidden Actions Count: {getattr(summary, 'forbidden_action_count', 0)}",
                f"Broker Execution:        DISABLED",
                f"Real Orders:             BLOCKED",
                f"Production Trading:      BLOCKED",
                f"No Real Orders:          {getattr(summary, 'no_real_orders', True)}",
            ]
            self._safety_text.setPlainText("\n".join(lines))

        def _update_layer_text(self, capabilities: list) -> None:
            from collections import Counter
            if not capabilities:
                self._layer_text.setPlaceholderText(
                    "Layer status will appear after validation.")
                return
            cats = Counter(getattr(c, "category", "") for c in capabilities)
            lines = []
            layer_map = [
                ("research_intelligence", "Research Intelligence"),
                ("strategy_memory",       "Strategy Memory"),
                ("backtest_coach",        "Backtest Coach"),
                ("training_metrics",      "Training Metrics"),
                ("evidence_graph",        "Evidence Graph"),
                ("data_coverage",         "Data Coverage"),
                ("report_pack",           "Report Pack"),
                ("regression",            "Regression"),
                ("stable_release",        "Stable Release"),
                ("safety",                "Safety"),
            ]
            for cat_key, cat_display in layer_map:
                n = cats.get(cat_key, 0)
                if n > 0:
                    stable = sum(
                        1 for c in capabilities
                        if getattr(c, "category", "") == cat_key
                        and getattr(c, "stable_status", "") == "STABLE"
                    )
                    lines.append(f"{cat_display:<28} {stable}/{n} STABLE")
            self._layer_text.setPlainText("\n".join(lines) if lines else "No layer data.")

        def _update_report_text(self) -> None:
            try:
                from gui.strategy_lab_adapter import StrategyLabAdapter
                adapter = StrategyLabAdapter()
                rpt     = adapter.load_latest_report_path()
                mft     = adapter.load_latest_manifest_path()
                smr     = adapter.load_latest_summary()
                smr_path = ""
                if smr:
                    from strategy_lab.strategy_lab_store import StrategyLabStore
                    smr_path = StrategyLabStore().load_latest_summary_path()
                lines = []
                if rpt:
                    lines.append(f"Report:   {rpt}")
                if mft:
                    lines.append(f"Manifest: {mft}")
                if smr_path:
                    lines.append(f"Summary:  {smr_path}")
                self._rpt_text.setPlainText(
                    "\n".join(lines) if lines else "No reports yet. Run validation or generate report.")
            except Exception as exc:
                logger.debug("StrategyLabPanel._update_report_text: %s", exc)

        # ------------------------------------------------------------------
        # closeEvent — clean up workers
        # ------------------------------------------------------------------

        def closeEvent(self, event) -> None:
            for worker in [self._validation_worker, self._report_worker, self._manifest_worker]:
                if worker is not None and worker.isRunning():
                    worker.quit()
                    worker.wait(2000)
            super().closeEvent(event)

    else:
        # PySide6 not available — stub class
        def __init__(self, parent=None) -> None:
            logger.warning("StrategyLabPanel: PySide6 not available.")
