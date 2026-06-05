"""
gui/research_intelligence_panel.py — ResearchIntelligencePanel v0.7.1.

PySide6 GUI tab for Research Intelligence: signals, priority board,
daily/weekly plans, and report generation.

[!] Research Intelligence Only. Research Only. No Real Orders.
[!] Production Trading: BLOCKED. Not investment advice.
[!] All recommendations are research actions only (REVIEW / RESEARCH / PRACTICE / FIX_DATA).
[!] NO BUY / SELL / ORDER output.
"""
from __future__ import annotations

import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
        QTextEdit, QHeaderView, QSplitter, QTabWidget, QSizePolicy,
        QLineEdit, QApplication,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — ResearchIntelligencePanel will not render.")

_SAFETY_BANNER = (
    "[!] Research Intelligence Only | Research Only | No Real Orders | "
    "Production Trading BLOCKED | No BUY/SELL/ORDER"
)

_PRI_COLORS = {
    "P0": "#FF4444",
    "P1": "#FFAA00",
    "P2": "#AACC00",
    "P3": "#4488FF",
}

_SEV_COLORS = {
    "CRITICAL": "#FF2222",
    "HIGH":     "#FF8800",
    "MEDIUM":   "#FFCC44",
    "LOW":      "#88CC88",
    "INFO":     "#AAAAAA",
}


if _PYSIDE6_OK:

    class ResearchIntelligenceWorker(QThread):
        """Background thread that runs the research intelligence pipeline."""

        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, mode: str = "real", period: str = "daily") -> None:
            super().__init__()
            self.mode   = mode
            self.period = period

        def run(self) -> None:
            try:
                from gui.research_intelligence_adapter import ResearchIntelligenceAdapter
                adapter = ResearchIntelligenceAdapter()
                result = adapter.run_intelligence(mode=self.mode, period=self.period)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class ResearchIntelligencePanel(QWidget):
        """Research Intelligence panel — signals, priority board, daily/weekly plans.

        [!] Research Intelligence Only. Research Only. No Real Orders.
        [!] Production Trading: BLOCKED. Not investment advice.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(
            self,
            parent: Optional[QWidget] = None,
            project_root: str = ".",
            report_dir: str = "reports",
        ) -> None:
            super().__init__(parent)
            self.project_root = project_root
            self.report_dir   = report_dir
            self._worker: Optional[ResearchIntelligenceWorker] = None
            self._last_result: dict = {}
            self._setup_ui()

        # ------------------------------------------------------------------
        # UI setup
        # ------------------------------------------------------------------

        def _setup_ui(self) -> None:
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setStyleSheet(
                "background:#3A0000; color:#FF8888; font-weight:bold; "
                "padding:6px; border-radius:4px;"
            )
            banner.setWordWrap(True)
            root.addWidget(banner)

            # Title
            title = QLabel("Research Intelligence — v0.7.1")
            title.setStyleSheet("font-size:14px; font-weight:bold; color:#AAAAFF;")
            root.addWidget(title)

            # Summary cards row
            summary_box = QGroupBox("Intelligence Summary")
            summary_box.setStyleSheet("QGroupBox { color:#AAAAFF; font-weight:bold; }")
            summary_layout = QHBoxLayout(summary_box)
            self._card_focus   = self._make_card("Today Focus", "—", "#FFDD88")
            self._card_total   = self._make_card("Total Signals", "—")
            self._card_p0      = self._make_card("P0 Critical", "—", "#FF4444")
            self._card_p1      = self._make_card("P1 High", "—", "#FFAA00")
            self._card_safe    = self._make_card("Safe Commands", "—", "#88CC88")
            self._card_blocked = self._make_card("Blocked Trading", "0", "#FF8888")
            self._card_recs    = self._make_card("Recommendations", "—", "#88CCFF")
            self._card_status  = self._make_card("Overall Status", "—", "#AAAAFF")
            for card in [
                self._card_focus, self._card_total, self._card_p0, self._card_p1,
                self._card_safe, self._card_blocked, self._card_recs, self._card_status,
            ]:
                summary_layout.addWidget(card)
            root.addWidget(summary_box)

            # Controls row
            ctrl = QHBoxLayout()
            self._mode_combo = QComboBox()
            self._mode_combo.addItems(["real", "mock"])
            ctrl.addWidget(QLabel("Mode:"))
            ctrl.addWidget(self._mode_combo)

            self._period_combo = QComboBox()
            self._period_combo.addItems(["daily", "weekly"])
            ctrl.addWidget(QLabel("Period:"))
            ctrl.addWidget(self._period_combo)

            # Filter controls
            ctrl.addWidget(QLabel("  Priority:"))
            self._filter_pri = QComboBox()
            self._filter_pri.addItems(["All", "P0", "P1", "P2", "P3"])
            self._filter_pri.currentTextChanged.connect(self._apply_filters)
            ctrl.addWidget(self._filter_pri)

            ctrl.addWidget(QLabel("Category:"))
            self._filter_cat = QComboBox()
            self._filter_cat.addItems(["All"])
            self._filter_cat.currentTextChanged.connect(self._apply_filters)
            ctrl.addWidget(self._filter_cat)

            ctrl.addWidget(QLabel("Source:"))
            self._filter_src = QComboBox()
            self._filter_src.addItems(["All"])
            self._filter_src.currentTextChanged.connect(self._apply_filters)
            ctrl.addWidget(self._filter_src)

            ctrl.addStretch()

            btn_run = QPushButton("Run Intelligence")
            btn_run.setStyleSheet("background:#334488; color:#FFFFFF; padding:4px 14px;")
            btn_run.clicked.connect(self._run_intelligence)
            ctrl.addWidget(btn_run)

            btn_report = QPushButton("Generate Report")
            btn_report.setStyleSheet("background:#225533; color:#FFFFFF; padding:4px 14px;")
            btn_report.clicked.connect(self._generate_report)
            ctrl.addWidget(btn_report)

            root.addLayout(ctrl)

            # Copy command bar
            cmd_bar = QHBoxLayout()
            cmd_bar.addWidget(QLabel("Selected Command:"))
            self._cmd_display = QLineEdit()
            self._cmd_display.setReadOnly(True)
            self._cmd_display.setStyleSheet(
                "background:#0E1020; color:#88CCFF; font-family:Consolas; padding:2px 6px;"
            )
            self._cmd_display.setPlaceholderText("Select a row to see the command here")
            cmd_bar.addWidget(self._cmd_display, stretch=1)
            btn_copy = QPushButton("Copy Command")
            btn_copy.setStyleSheet("background:#334455; color:#FFFFFF; padding:4px 10px;")
            btn_copy.clicked.connect(self._copy_command)
            cmd_bar.addWidget(btn_copy)
            root.addLayout(cmd_bar)

            # Tabbed content
            self._tabs = QTabWidget()
            self._tabs.setStyleSheet(
                "QTabBar::tab { background:#1A1A2E; color:#AAAAAA; padding:6px 14px; }"
                "QTabBar::tab:selected { background:#252540; color:#FFFFFF; font-weight:bold; }"
            )

            self._tabs.addTab(self._build_priority_tab(), "Priority Board")
            self._tabs.addTab(self._build_daily_tab(),    "Daily Plan")
            self._tabs.addTab(self._build_weekly_tab(),   "Weekly Plan")
            self._tabs.addTab(self._build_signals_tab(),  "All Signals")

            root.addWidget(self._tabs)

            # Status bar
            self._status_lbl = QLabel("尚未執行，請點擊 Run Intelligence")
            self._status_lbl.setStyleSheet("color:#AAAAAA; font-size:11px;")
            root.addWidget(self._status_lbl)

        def _make_card(self, label: str, value: str, color: str = "#DDDDDD") -> QGroupBox:
            box = QGroupBox(label)
            box.setStyleSheet(f"QGroupBox {{ color:{color}; font-size:11px; }}")
            lay = QVBoxLayout(box)
            lbl = QLabel(value)
            lbl.setStyleSheet(f"color:{color}; font-size:14px; font-weight:bold;")
            lbl.setAlignment(Qt.AlignCenter)
            lay.addWidget(lbl)
            box.setProperty("_value_lbl", lbl)
            return box

        def _set_card(self, box: QGroupBox, value: str) -> None:
            lbl = box.property("_value_lbl")
            if lbl:
                lbl.setText(str(value))

        # ------------------------------------------------------------------
        # Tab builders
        # ------------------------------------------------------------------

        def _build_priority_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.setContentsMargins(4, 4, 4, 4)

            self._priority_tabs = QTabWidget()
            self._priority_tabs.setStyleSheet(
                "QTabBar::tab { background:#121220; color:#AAAAAA; padding:4px 10px; }"
                "QTabBar::tab:selected { background:#1E1E3A; color:#FFFFFF; }"
            )

            self._pri_tables: dict = {}
            for pri, label in [
                ("P0", "P0 — 必修"),
                ("P1", "P1 — 高優先"),
                ("P2", "P2 — 中優先"),
                ("P3", "P3 — 低優先"),
            ]:
                tbl = self._make_board_table()
                self._pri_tables[pri] = tbl
                self._priority_tabs.addTab(tbl, label)

            lay.addWidget(self._priority_tabs)
            return w

        def _make_board_table(self) -> QTableWidget:
            tbl = QTableWidget()
            tbl.setColumnCount(7)
            tbl.setHorizontalHeaderLabels(
                ["Priority", "Title", "Why Now", "Risk If Ignored", "Safe Command", "Safety", "Due"]
            )
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            tbl.horizontalHeader().setStretchLastSection(True)
            tbl.setEditTriggers(QTableWidget.NoEditTriggers)
            tbl.setAlternatingRowColors(True)
            tbl.setSelectionBehavior(QTableWidget.SelectRows)
            tbl.setStyleSheet(_TABLE_STYLE)
            tbl.itemSelectionChanged.connect(lambda: self._on_board_selection(tbl))
            return tbl

        def _build_plan_table(self) -> QTableWidget:
            tbl = QTableWidget()
            tbl.setColumnCount(7)
            tbl.setHorizontalHeaderLabels(
                ["#", "Title", "Category", "Command", "Safety", "Why Now", "Risk If Ignored"]
            )
            tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            tbl.horizontalHeader().setStretchLastSection(True)
            tbl.setEditTriggers(QTableWidget.NoEditTriggers)
            tbl.setAlternatingRowColors(True)
            tbl.setSelectionBehavior(QTableWidget.SelectRows)
            tbl.setStyleSheet(_TABLE_STYLE)
            tbl.itemSelectionChanged.connect(lambda: self._on_plan_selection(tbl))
            return tbl

        def _build_daily_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.setContentsMargins(4, 4, 4, 4)
            lbl = QLabel("Today's Research Plan (up to 7 items)")
            lbl.setStyleSheet("color:#AAAAFF; font-weight:bold;")
            lay.addWidget(lbl)
            self._daily_table = self._build_plan_table()
            lay.addWidget(self._daily_table)
            return w

        def _build_weekly_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.setContentsMargins(4, 4, 4, 4)
            lbl = QLabel("Weekly Research Plan (up to 12 items)")
            lbl.setStyleSheet("color:#AAAAFF; font-weight:bold;")
            lay.addWidget(lbl)
            self._weekly_table = self._build_plan_table()
            lay.addWidget(self._weekly_table)
            return w

        def _build_signals_tab(self) -> QWidget:
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.setContentsMargins(4, 4, 4, 4)
            self._signals_table = QTableWidget()
            self._signals_table.setColumnCount(7)
            self._signals_table.setHorizontalHeaderLabels([
                "Source", "Category", "Severity", "Priority", "Title", "Command", "Evidence",
            ])
            self._signals_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._signals_table.horizontalHeader().setStretchLastSection(True)
            self._signals_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._signals_table.setAlternatingRowColors(True)
            self._signals_table.setSelectionBehavior(QTableWidget.SelectRows)
            self._signals_table.setStyleSheet(_TABLE_STYLE)
            lay.addWidget(self._signals_table)
            return w

        # ------------------------------------------------------------------
        # Actions
        # ------------------------------------------------------------------

        def _run_intelligence(self) -> None:
            mode   = self._mode_combo.currentText()
            period = self._period_combo.currentText()
            self._status_lbl.setText(f"Running research intelligence (mode={mode}, period={period})…")
            self._worker = ResearchIntelligenceWorker(mode=mode, period=period)
            self._worker.finished.connect(self._on_run_done)
            self._worker.error.connect(self._on_run_error)
            self._worker.start()

        def _on_run_done(self, result: dict) -> None:
            self._last_result = result
            summary = result.get("summary", {})
            signals = result.get("signals", [])
            self._update_cards(summary)
            self._update_priority_board(result.get("priority_board", []))
            self._update_plan_table(self._daily_table, result.get("daily_plan", []))
            self._update_plan_table(self._weekly_table, result.get("weekly_plan", []))
            self._update_signals_table(signals)
            self._populate_filter_options(signals)
            status = summary.get("overall_status", "—")
            total  = summary.get("total_signals", 0)
            recs   = summary.get("recommendations_count", 0)
            safe   = summary.get("safe_command_count", 0)
            self._status_lbl.setText(
                f"完成: {total} signals, {recs} recommendations, {safe} safe commands, status={status}"
            )

        def _on_run_error(self, msg: str) -> None:
            self._status_lbl.setText(f"執行失敗: {msg}")
            logger.error("ResearchIntelligencePanel run error: %s", msg)

        def _generate_report(self) -> None:
            mode = self._mode_combo.currentText()
            self._status_lbl.setText("Generating report…")
            try:
                from gui.research_intelligence_adapter import ResearchIntelligenceAdapter
                adapter = ResearchIntelligenceAdapter(report_dir=self.report_dir)
                path = adapter.generate_report(mode=mode)
                self._status_lbl.setText(f"Report saved: {path}")
                logger.info("ResearchIntelligencePanel: report saved → %s", path)
            except Exception as exc:
                self._status_lbl.setText(f"Report failed: {exc}")
                logger.error("ResearchIntelligencePanel generate_report error: %s", exc)

        # ------------------------------------------------------------------
        # Update helpers
        # ------------------------------------------------------------------

        def _update_cards(self, summary: dict) -> None:
            focus   = summary.get("today_focus", "—") or "—"
            self._set_card(self._card_focus,   focus[:60] + ("…" if len(focus) > 60 else ""))
            self._set_card(self._card_total,   str(summary.get("total_signals", 0)))
            p0_cnt = summary.get("system_risk_count", 0) or len(self._last_result.get("priority_board", []))
            # Count P0 items from board
            board_rows = self._last_result.get("priority_board", [])
            p0_count = sum(1 for r in board_rows if isinstance(r, dict) and r.get("priority") == "P0")
            p1_count = sum(1 for r in board_rows if isinstance(r, dict) and r.get("priority") == "P1")
            self._set_card(self._card_p0,      str(p0_count))
            self._set_card(self._card_p1,      str(p1_count))
            self._set_card(self._card_safe,    str(summary.get("safe_command_count", 0)))
            self._set_card(self._card_blocked, str(summary.get("blocked_trading_action_count", 0)))
            self._set_card(self._card_recs,    str(summary.get("recommendations_count", 0)))
            self._set_card(self._card_status,  summary.get("overall_status", "—"))

        def _update_priority_board(self, rows: list) -> None:
            # rows is a flat list with "priority" key per item
            board: dict = {"P0": [], "P1": [], "P2": [], "P3": []}
            for row in rows:
                pri = row.get("priority", "P3") if isinstance(row, dict) else "P3"
                if pri in board:
                    board[pri].append(row)

            for pri, items in board.items():
                tbl = self._pri_tables.get(pri)
                if tbl is None:
                    continue
                tbl.setRowCount(len(items))
                color = _PRI_COLORS.get(pri, "#DDDDDD")
                for r, item in enumerate(items):
                    if not isinstance(item, dict):
                        continue
                    title    = item.get("title", "")
                    why_now  = item.get("why_now", "") or item.get("why", "")
                    risk     = item.get("risk_if_ignored", "")
                    cmd      = item.get("command", "") or item.get("safe_command", "") or "—"
                    safety   = item.get("safe_command_label", "")
                    due      = item.get("due_hint", "")

                    def _cell(text: str, fg: str = "#EEEEEE") -> QTableWidgetItem:
                        c = QTableWidgetItem(str(text))
                        c.setForeground(QColor(fg))
                        c.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                        return c

                    pri_cell = QTableWidgetItem(pri)
                    pri_cell.setForeground(QColor(color))
                    pri_cell.setFont(QFont("Consolas", 9, QFont.Bold))
                    pri_cell.setTextAlignment(Qt.AlignCenter)
                    tbl.setItem(r, 0, pri_cell)
                    tbl.setItem(r, 1, _cell(title))
                    tbl.setItem(r, 2, _cell(why_now, "#DDCC88"))
                    tbl.setItem(r, 3, _cell(risk, "#FF9988"))
                    cmd_cell = QTableWidgetItem(cmd)
                    cmd_cell.setForeground(QColor("#88CCFF"))
                    tbl.setItem(r, 4, cmd_cell)
                    tbl.setItem(r, 5, _cell(safety, "#88CC88"))
                    tbl.setItem(r, 6, _cell(due, "#AAAAAA"))

        def _update_plan_table(self, tbl: QTableWidget, items: list) -> None:
            tbl.setRowCount(len(items))
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    continue
                title    = item.get("title", "")
                cat      = item.get("category", "")
                cmds     = item.get("suggested_commands", "") or item.get("command", "")
                if isinstance(cmds, list):
                    cmd = cmds[0] if cmds else ""
                else:
                    cmd = str(cmds).split("|")[0] if cmds else ""
                safety   = item.get("command_safety", "") or item.get("safe_command_label", "")
                why_now  = item.get("why_now", "")
                risk     = item.get("risk_if_ignored", "")
                pri      = item.get("priority", "P3")
                color    = _PRI_COLORS.get(pri, "#DDDDDD")

                def _cell(text: str, fg: str = "#EEEEEE") -> QTableWidgetItem:
                    c = QTableWidgetItem(str(text))
                    c.setForeground(QColor(fg))
                    c.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    return c

                tbl.setItem(i, 0, _cell(str(i + 1), color))
                tbl.setItem(i, 1, _cell(title))
                tbl.setItem(i, 2, _cell(cat, "#AAAAAA"))
                cmd_cell = QTableWidgetItem(cmd if cmd else "—")
                cmd_cell.setForeground(QColor("#88CCFF"))
                tbl.setItem(i, 3, cmd_cell)
                tbl.setItem(i, 4, _cell(safety, "#88CC88"))
                tbl.setItem(i, 5, _cell(why_now, "#DDCC88"))
                tbl.setItem(i, 6, _cell(risk, "#FF9988"))

        def _update_signals_table(self, signals: list) -> None:
            self._signals_table.setRowCount(len(signals))
            for r, sig in enumerate(signals):
                if not isinstance(sig, dict):
                    continue
                src   = sig.get("source_module", "")
                cat   = sig.get("category", "")
                sev   = sig.get("severity", "")
                pri   = sig.get("priority", "")
                title = sig.get("title", "")
                cmd   = sig.get("suggested_command", "") or "—"
                ev    = sig.get("evidence", "") or ""

                sev_color = _SEV_COLORS.get(sev, "#AAAAAA")
                pri_color = _PRI_COLORS.get(pri, "#DDDDDD")

                def _cell(text: str, fg: str = "#EEEEEE") -> QTableWidgetItem:
                    c = QTableWidgetItem(str(text))
                    c.setForeground(QColor(fg))
                    c.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    return c

                self._signals_table.setItem(r, 0, _cell(src, "#AAAAFF"))
                self._signals_table.setItem(r, 1, _cell(cat, "#AAAAAA"))

                sev_cell = QTableWidgetItem(sev)
                sev_cell.setForeground(QColor(sev_color))
                sev_cell.setFont(QFont("Consolas", 9, QFont.Bold))
                sev_cell.setTextAlignment(Qt.AlignCenter)
                self._signals_table.setItem(r, 2, sev_cell)

                pri_cell = QTableWidgetItem(pri)
                pri_cell.setForeground(QColor(pri_color))
                pri_cell.setFont(QFont("Consolas", 9, QFont.Bold))
                pri_cell.setTextAlignment(Qt.AlignCenter)
                self._signals_table.setItem(r, 3, pri_cell)

                self._signals_table.setItem(r, 4, _cell(title))

                cmd_cell = QTableWidgetItem(cmd)
                cmd_cell.setForeground(QColor("#88CCFF"))
                self._signals_table.setItem(r, 5, cmd_cell)
                self._signals_table.setItem(r, 6, _cell(ev, "#AAAAAA"))

        def _on_board_selection(self, tbl: QTableWidget) -> None:
            rows = tbl.selectedItems()
            if not rows:
                return
            row_idx = tbl.currentRow()
            cmd_item = tbl.item(row_idx, 4)  # Safe Command column
            if cmd_item:
                self._cmd_display.setText(cmd_item.text())

        def _on_plan_selection(self, tbl: QTableWidget) -> None:
            rows = tbl.selectedItems()
            if not rows:
                return
            row_idx = tbl.currentRow()
            cmd_item = tbl.item(row_idx, 3)  # Command column
            if cmd_item:
                self._cmd_display.setText(cmd_item.text())

        def _copy_command(self) -> None:
            text = self._cmd_display.text()
            if text and text != "—":
                QApplication.clipboard().setText(text)
                self._status_lbl.setText(f"Copied: {text}")

        def _apply_filters(self) -> None:
            """Filter signals table by priority/category/source."""
            pri_filter = self._filter_pri.currentText()
            cat_filter = self._filter_cat.currentText()
            src_filter = self._filter_src.currentText()
            for row in range(self._signals_table.rowCount()):
                src_item = self._signals_table.item(row, 0)
                cat_item = self._signals_table.item(row, 1)
                pri_item = self._signals_table.item(row, 3)
                src_val = src_item.text() if src_item else ""
                cat_val = cat_item.text() if cat_item else ""
                pri_val = pri_item.text() if pri_item else ""
                visible = (
                    (pri_filter == "All" or pri_val == pri_filter)
                    and (cat_filter == "All" or cat_val == cat_filter)
                    and (src_filter == "All" or src_val == src_filter)
                )
                self._signals_table.setRowHidden(row, not visible)

        def _populate_filter_options(self, signals: list) -> None:
            cats = sorted({s.get("category", "") for s in signals if isinstance(s, dict) and s.get("category")})
            srcs = sorted({s.get("source_module", "") for s in signals if isinstance(s, dict) and s.get("source_module")})
            for combo, values in [(self._filter_cat, cats), (self._filter_src, srcs)]:
                combo.blockSignals(True)
                current = combo.currentText()
                combo.clear()
                combo.addItem("All")
                combo.addItems(values)
                idx = combo.findText(current)
                combo.setCurrentIndex(max(0, idx))
                combo.blockSignals(False)

        def closeEvent(self, event) -> None:
            if self._worker and self._worker.isRunning():
                self._worker.quit()
                self._worker.wait(2000)
            super().closeEvent(event)

    _TABLE_STYLE = """
        QTableWidget { background:#12121E; color:#EEEEEE; gridline-color:#333355; }
        QTableWidget::item:alternate { background:#1A1A2E; }
        QHeaderView::section { background:#252540; color:#AAAAFF; font-weight:bold; }
    """

else:
    # Fallback stubs when PySide6 is not available
    class ResearchIntelligenceWorker:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class ResearchIntelligencePanel:  # type: ignore[no-redef]
        read_only          = True
        no_real_orders     = True
        production_blocked = True
        real_order_ready   = False

        def __init__(self, *a, **kw):
            logger.warning("ResearchIntelligencePanel: PySide6 not available — stub mode.")
