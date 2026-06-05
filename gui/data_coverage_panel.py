"""
gui/data_coverage_panel.py — DataCoveragePanel for TW Quant Cockpit v0.6.2.

PySide6 GUI panel for data coverage scanning, matrix display, and gap reporting.

[!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
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
        QTextEdit, QHeaderView, QSplitter, QSizePolicy,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor, QFont
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — DataCoveragePanel will not render.")

_SAFETY_BANNER = "[!] Data Coverage Only | Research Only | No Real Orders | Production BLOCKED"

_STATUS_COLORS = {
    "READY":            "#33CC66",
    "PARTIAL":          "#AACC00",
    "ENV_LIMITED":      "#FFAA00",
    "NOT_GENERATED":    "#FFCC44",
    "MISSING_OPTIONAL": "#FF8800",
    "MISSING_REQUIRED": "#FF4444",
    "STALE":            "#AAAAAA",
    "FAILED":           "#FF2222",
    "UNKNOWN":          "#888888",
}


if _PYSIDE6_OK:
    class DataCoverageWorker(QThread):
        """Background thread that runs the coverage scan."""

        finished = Signal(list, object)  # items, summary
        error    = Signal(str)

        def __init__(self, mode: str = "real", project_root: str = ".") -> None:
            super().__init__()
            self.mode         = mode
            self.project_root = project_root

        def run(self) -> None:
            try:
                from data_coverage.data_coverage_engine import DataCoverageEngine
                engine = DataCoverageEngine(project_root=self.project_root)
                items, summary = engine.run(mode=self.mode)
                self.finished.emit(items, summary)
            except Exception as exc:
                self.error.emit(str(exc))

    class DataCoveragePanel(QWidget):
        """Data Coverage Expansion panel.

        [!] Data Coverage Only. Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(
            self,
            parent: Optional[QWidget] = None,
            project_root: str = ".",
            report_dir: str = "reports",
        ) -> None:
            super().__init__(parent)
            self.project_root = project_root
            self.report_dir   = report_dir
            self._worker: Optional[DataCoverageWorker] = None
            self._items: List = []
            self._summary = None
            self._setup_ui()

        def _setup_ui(self) -> None:
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            # Safety banner
            banner = QLabel(_SAFETY_BANNER)
            banner.setStyleSheet(
                "background:#3A1A00; color:#FFAA44; font-weight:bold; "
                "padding:6px; border-radius:4px;"
            )
            banner.setWordWrap(True)
            root.addWidget(banner)

            # Title
            title = QLabel("Data Coverage Expansion — v0.6.2")
            title.setStyleSheet("font-size:14px; font-weight:bold; color:#AAAAFF;")
            root.addWidget(title)

            # Summary Cards row
            summary_box = QGroupBox("Coverage Summary")
            summary_box.setStyleSheet("QGroupBox { color:#AAAAFF; font-weight:bold; }")
            summary_layout = QHBoxLayout(summary_box)
            self._lbl_total    = self._card("Total", "—")
            self._lbl_ready    = self._card("Ready", "—", "#33CC66")
            self._lbl_env_lim  = self._card("ENV Limited", "—", "#FFAA00")
            self._lbl_not_gen  = self._card("Not Generated", "—", "#FFCC44")
            self._lbl_miss_req = self._card("Missing Required", "—", "#FF4444")
            self._lbl_score    = self._card("Score", "—", "#AAAAFF")
            for card in [
                self._lbl_total, self._lbl_ready, self._lbl_env_lim,
                self._lbl_not_gen, self._lbl_miss_req, self._lbl_score,
            ]:
                summary_layout.addWidget(card)
            root.addWidget(summary_box)

            # Controls row
            ctrl_row = QHBoxLayout()
            self._mode_combo = QComboBox()
            self._mode_combo.addItems(["real", "mock"])
            ctrl_row.addWidget(QLabel("Mode:"))
            ctrl_row.addWidget(self._mode_combo)

            self._domain_combo = QComboBox()
            self._domain_combo.addItem("All Domains", "")
            for d in [
                "provider", "daily_data", "intraday", "financial",
                "chip", "feature_store", "replay", "experiment",
                "rule_governance", "report_pack", "regression", "stable_release",
            ]:
                self._domain_combo.addItem(d, d)
            self._domain_combo.currentIndexChanged.connect(self._filter_table)
            ctrl_row.addWidget(QLabel("Domain:"))
            ctrl_row.addWidget(self._domain_combo)

            ctrl_row.addStretch()

            btn_scan = QPushButton("Run Scan")
            btn_scan.setStyleSheet("background:#334488; color:#FFFFFF; padding:4px 12px;")
            btn_scan.clicked.connect(self._run_scan)
            ctrl_row.addWidget(btn_scan)

            btn_report = QPushButton("Generate Report")
            btn_report.setStyleSheet("background:#225533; color:#FFFFFF; padding:4px 12px;")
            btn_report.clicked.connect(self._generate_report)
            ctrl_row.addWidget(btn_report)

            root.addLayout(ctrl_row)

            # Main table
            self._table = QTableWidget()
            self._table.setColumnCount(6)
            self._table.setHorizontalHeaderLabels([
                "Domain", "Item", "Status", "Required", "Suggested Command", "Warning",
            ])
            self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._table.horizontalHeader().setStretchLastSection(True)
            self._table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._table.setAlternatingRowColors(True)
            self._table.setSelectionBehavior(QTableWidget.SelectRows)
            self._table.setStyleSheet("""
                QTableWidget { background:#12121E; color:#EEEEEE; gridline-color:#333355; }
                QTableWidget::item:alternate { background:#1A1A2E; }
                QHeaderView::section { background:#252540; color:#AAAAFF; font-weight:bold; }
            """)

            # Gaps panel
            self._gaps_text = QTextEdit()
            self._gaps_text.setReadOnly(True)
            self._gaps_text.setMaximumHeight(120)
            self._gaps_text.setStyleSheet(
                "background:#0A0A14; color:#FF8888; font-family:monospace; font-size:11px"
            )
            self._gaps_text.setPlainText("尚未執行掃描，請點擊 Run Scan")

            splitter = QSplitter(Qt.Vertical)
            splitter.addWidget(self._table)
            splitter.addWidget(self._gaps_text)
            splitter.setStretchFactor(0, 3)
            splitter.setStretchFactor(1, 1)
            root.addWidget(splitter)

            # Status label
            self._status_lbl = QLabel("尚未執行掃描，請點擊 Run Scan")
            self._status_lbl.setStyleSheet("color:#AAAAAA; font-size:11px;")
            root.addWidget(self._status_lbl)

        def _card(self, label: str, value: str, color: str = "#DDDDDD") -> QGroupBox:
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

        def _run_scan(self) -> None:
            mode = self._mode_combo.currentText()
            self._status_lbl.setText(f"掃描中 (mode={mode})…")
            self._worker = DataCoverageWorker(mode=mode, project_root=self.project_root)
            self._worker.finished.connect(self._on_scan_done)
            self._worker.error.connect(self._on_scan_error)
            self._worker.start()

        def _on_scan_done(self, items: list, summary) -> None:
            self._items   = items
            self._summary = summary
            self._update_summary_cards(summary)
            self._update_table(items)
            self._update_gaps(items, summary)
            self._status_lbl.setText(
                f"掃描完成: {summary.total_items} items, score={summary.coverage_score:.1f}"
            )

        def _on_scan_error(self, msg: str) -> None:
            self._status_lbl.setText(f"掃描失敗: {msg}")
            logger.error("DataCoveragePanel scan error: %s", msg)

        def _update_summary_cards(self, summary) -> None:
            self._set_card(self._lbl_total,    str(summary.total_items))
            self._set_card(self._lbl_ready,    str(summary.ready_count))
            self._set_card(self._lbl_env_lim,  str(summary.env_limited_count))
            self._set_card(self._lbl_not_gen,  str(summary.not_generated_count))
            self._set_card(self._lbl_miss_req, str(summary.missing_required_count))
            self._set_card(self._lbl_score,    f"{summary.coverage_score:.1f}")

        def _filter_table(self) -> None:
            if self._items:
                self._update_table(self._items)

        def _update_table(self, items: list) -> None:
            domain_filter = self._domain_combo.currentData() or ""
            filtered = [
                i for i in items
                if not domain_filter or i.domain == domain_filter
            ]

            self._table.setRowCount(len(filtered))
            for row, item in enumerate(filtered):
                d = item.to_dict() if hasattr(item, "to_dict") else item
                status  = d.get("status", "UNKNOWN")
                color   = _STATUS_COLORS.get(status, "#888888")
                req_str = "Required" if d.get("required") else "Optional"
                cmd     = d.get("suggested_command", "") or "—"
                warn    = d.get("warning", "") or d.get("missing_reason", "") or ""

                def cell(text: str, fg: str = "#EEEEEE") -> QTableWidgetItem:
                    item_ = QTableWidgetItem(str(text))
                    item_.setForeground(QColor(fg))
                    item_.setTextAlignment(Qt.AlignCenter)
                    return item_

                self._table.setItem(row, 0, cell(d.get("domain", "")))
                self._table.setItem(row, 1, cell(d.get("dataset_name", "")))
                status_cell = QTableWidgetItem(status)
                status_cell.setForeground(QColor(color))
                status_cell.setFont(QFont("Consolas", 9, QFont.Bold))
                status_cell.setTextAlignment(Qt.AlignCenter)
                self._table.setItem(row, 2, status_cell)
                self._table.setItem(row, 3, cell(req_str))
                cmd_cell = QTableWidgetItem(cmd)
                cmd_cell.setForeground(QColor("#88CCFF"))
                self._table.setItem(row, 4, cmd_cell)
                warn_cell = QTableWidgetItem(warn)
                warn_cell.setForeground(QColor("#FFAA44" if warn else "#AAAAAA"))
                self._table.setItem(row, 5, warn_cell)

        def _update_gaps(self, items: list, summary) -> None:
            lines = [_SAFETY_BANNER, ""]
            if summary.blockers:
                lines.append("BLOCKERS (Missing Required):")
                for b in summary.blockers:
                    lines.append(f"  ! {b}")
                lines.append("")
            if summary.warnings:
                lines.append("Warnings:")
                for w in summary.warnings[:10]:
                    lines.append(f"  ~ {w}")
            if not summary.blockers and not summary.warnings:
                lines.append("No blockers or warnings. Coverage looks healthy.")
            self._gaps_text.setPlainText("\n".join(lines))

        def _generate_report(self) -> None:
            mode = self._mode_combo.currentText()
            try:
                from reports.data_coverage_report import DataCoverageReport
                reporter = DataCoverageReport(
                    project_root=self.project_root,
                    report_dir=self.report_dir,
                )
                path = reporter.run(mode=mode)
                self._status_lbl.setText(f"Report saved: {path}")
                logger.info("DataCoveragePanel: report saved to %s", path)
            except Exception as exc:
                self._status_lbl.setText(f"Report failed: {exc}")
                logger.error("DataCoveragePanel generate_report error: %s", exc)

        def _get_status_color(self, status: str) -> str:
            return _STATUS_COLORS.get(status, "#888888")

else:
    # Fallback stub when PySide6 is not available
    class DataCoverageWorker:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class DataCoveragePanel:  # type: ignore[no-redef]
        read_only          = True
        no_real_orders     = True
        production_blocked = True

        def __init__(self, *a, **kw):
            logger.warning("DataCoveragePanel: PySide6 not available — stub mode.")
