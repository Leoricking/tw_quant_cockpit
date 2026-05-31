"""
gui/release_status_panel.py — ReleaseStatusPanel: GUI panel for v0.4.0 Release Status tab.
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations
import logging
import os

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# PySide6 guarded import
# ---------------------------------------------------------------------------
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
        QHeaderView, QGroupBox, QFrame, QSizePolicy, QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal, QObject
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False


# ---------------------------------------------------------------------------
# Fallback widget when PySide6 is absent
# ---------------------------------------------------------------------------

class _FallbackWidget:
    """Minimal no-op widget replacement when PySide6 is not available."""
    def __init__(self, *args, **kwargs):
        pass

    def show(self):
        pass


# ---------------------------------------------------------------------------
# Worker base class (no-op without PySide6)
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _WorkerBase(QObject):
        finished = Signal(dict)
        error    = Signal(str)

        def __init__(self, fn, *fn_args, **fn_kwargs):
            super().__init__()
            self._fn       = fn
            self._fn_args  = fn_args
            self._fn_kwargs = fn_kwargs

        def run(self):
            try:
                result = self._fn(*self._fn_args, **self._fn_kwargs)
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))
else:
    class _WorkerBase:  # type: ignore[no-redef]
        def __init__(self, fn, *fn_args, **fn_kwargs):
            pass


# ---------------------------------------------------------------------------
# Status colour helpers
# ---------------------------------------------------------------------------

_STATUS_COLORS = {
    "PASS":    "#33CC66",
    "PARTIAL": "#FF8800",
    "FAIL":    "#FF4444",
    "BLOCKED": "#FF0000",
    "WARN":    "#FF8800",
    "SKIP":    "#888888",
    "NOT RUN": "#888888",
    "UNKNOWN": "#888888",
}


def _status_color(status: str) -> str:
    return _STATUS_COLORS.get(status.upper(), "#AAAAAA")


# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------

_BaseClass = QWidget if _PYSIDE6_OK else object


class ReleaseStatusPanel(_BaseClass):  # type: ignore[misc]
    """GUI panel for the v0.4.0 Release Status tab.

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(self, mode: str = "real", parent=None) -> None:
        if _PYSIDE6_OK:
            super().__init__(parent)
        self.mode = mode
        self._thread: QThread | None = None  # type: ignore[name-defined]
        self._worker = None
        self._last_regression: dict | None = None

        try:
            from gui.release_status_adapter import ReleaseStatusAdapter
            self._adapter = ReleaseStatusAdapter()
        except Exception as exc:
            logger.warning("ReleaseStatusAdapter unavailable: %s", exc)
            self._adapter = None

        if _PYSIDE6_OK:
            self._build_ui()
            self._load_version_info()
        else:
            logger.warning("PySide6 not available — ReleaseStatusPanel is a no-op.")

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        # ---- A: Header ----
        header = QLabel("v0.4.0 Research Platform Stable Release")
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #E0E0E0;")
        root.addWidget(header)

        banner = QLabel(
            "\u26a0 Research Only | No Real Orders | "
            "Production BLOCKED | real_order_ready=False"
        )
        banner.setStyleSheet(
            "background-color: #3A1A00; color: #FF8800; "
            "font-weight: bold; padding: 4px 8px; border-radius: 4px;"
        )
        root.addWidget(banner)

        # ---- B: Version cards ----
        cards_box = QGroupBox("Version Information")
        cards_layout = QHBoxLayout(cards_box)
        cards_layout.setSpacing(8)

        self._card_version   = self._make_card("Current Version", "v0.4.0")
        self._card_stage     = self._make_card("Release Stage",   "stable_research")
        self._card_commit    = self._make_card("Git Commit",      "...")
        self._card_safety    = self._make_card("Safety Status",   "VERIFIED", "#33CC66")
        self._card_regression = self._make_card("Regression Status", "NOT RUN", "#888888")

        for card in (self._card_version, self._card_stage, self._card_commit,
                     self._card_safety, self._card_regression):
            cards_layout.addWidget(card)

        root.addWidget(cards_box)

        # ---- C: Feature coverage table ----
        feat_box = QGroupBox("Feature Coverage (v0.4.0)")
        feat_layout = QVBoxLayout(feat_box)
        self._feat_table = QTableWidget(0, 3)
        self._feat_table.setHorizontalHeaderLabels(["Feature", "Status", "Notes"])
        self._feat_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self._feat_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self._feat_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self._feat_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._feat_table.setAlternatingRowColors(True)
        self._feat_table.setMaximumHeight(280)
        feat_layout.addWidget(self._feat_table)
        root.addWidget(feat_box)

        # ---- D: Regression results table ----
        reg_box = QGroupBox("Regression Results")
        reg_layout = QVBoxLayout(reg_box)
        self._reg_empty_label = QLabel(
            "No regression results yet. Click 'Run Quick Regression' to start."
        )
        self._reg_empty_label.setStyleSheet("color: #888888; font-style: italic;")
        reg_layout.addWidget(self._reg_empty_label)

        self._reg_table = QTableWidget(0, 4)
        self._reg_table.setHorizontalHeaderLabels(["Test", "Status", "Duration (ms)", "Detail"])
        self._reg_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._reg_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self._reg_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self._reg_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self._reg_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._reg_table.setAlternatingRowColors(True)
        self._reg_table.setMaximumHeight(200)
        self._reg_table.hide()
        reg_layout.addWidget(self._reg_table)
        root.addWidget(reg_box)

        # ---- E: Actions ----
        actions_box = QGroupBox("Actions")
        actions_layout = QHBoxLayout(actions_box)

        self._btn_quick_reg = QPushButton("Run Quick Regression")
        self._btn_quick_reg.clicked.connect(self._on_run_quick_regression)

        self._btn_full_reg = QPushButton("Run Full Regression")
        self._btn_full_reg.clicked.connect(self._on_run_full_regression)

        self._btn_checklist = QPushButton("Run Checklist")
        self._btn_checklist.clicked.connect(self._on_run_checklist)

        self._btn_report = QPushButton("Generate Release Report")
        self._btn_report.clicked.connect(self._on_generate_report)

        self._btn_notes = QPushButton("Open Release Notes")
        self._btn_notes.clicked.connect(self._on_open_release_notes)

        for btn in (self._btn_quick_reg, self._btn_full_reg, self._btn_checklist,
                    self._btn_report, self._btn_notes):
            btn.setMinimumWidth(120)
            actions_layout.addWidget(btn)

        actions_layout.addStretch()
        root.addWidget(actions_box)

        # ---- Status label ----
        self._status_label = QLabel("")
        self._status_label.setStyleSheet("color: #888888; font-style: italic;")
        root.addWidget(self._status_label)

        root.addStretch()

    def _make_card(self, label: str, value: str,
                   value_color: str = "#E0E0E0") -> QFrame:
        """Create a small card widget with a label and value."""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet(
            "QFrame { background: #1E1E1E; border: 1px solid #333; border-radius: 6px; }"
        )
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #888888; font-size: 10px;")
        lbl.setAlignment(Qt.AlignCenter)

        val = QLabel(value)
        val_font = QFont()
        val_font.setPointSize(10)
        val_font.setBold(True)
        val.setFont(val_font)
        val.setStyleSheet(f"color: {value_color};")
        val.setAlignment(Qt.AlignCenter)

        # Store reference so we can update value later
        frame._value_label = val  # type: ignore[attr-defined]

        layout.addWidget(lbl)
        layout.addWidget(val)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return frame

    def _update_card(self, card: QFrame, value: str,
                     color: str | None = None) -> None:
        val_lbl = getattr(card, "_value_label", None)
        if val_lbl is None:
            return
        val_lbl.setText(value)
        if color:
            val_lbl.setStyleSheet(f"color: {color};")

    # ------------------------------------------------------------------
    # Load version info on init
    # ------------------------------------------------------------------

    def _load_version_info(self) -> None:
        if not self._adapter:
            return
        try:
            info = self._adapter.get_version_info()
            self._populate_feature_table(info.get("major_features", []))

            # Try to get git commit via adapter or subprocess
            import subprocess
            try:
                res = subprocess.run(
                    ["git", "-C", BASE_DIR, "rev-parse", "--short", "HEAD"],
                    capture_output=True, text=True, timeout=5,
                )
                commit = res.stdout.strip() or "unknown"
            except Exception:
                commit = "unknown"

            self._update_card(self._card_commit, commit)
        except Exception as exc:
            logger.warning("_load_version_info failed: %s", exc)
            self._populate_feature_table([])

    def _populate_feature_table(self, features: list[str]) -> None:
        self._feat_table.setRowCount(0)
        for feat in features:
            row = self._feat_table.rowCount()
            self._feat_table.insertRow(row)
            self._feat_table.setItem(row, 0, QTableWidgetItem(feat))

            status_item = QTableWidgetItem("Available")
            status_item.setForeground(QColor("#33CC66"))
            self._feat_table.setItem(row, 1, status_item)
            self._feat_table.setItem(row, 2, QTableWidgetItem("—"))

    # ------------------------------------------------------------------
    # Thread management
    # ------------------------------------------------------------------

    def _stop_thread(self) -> None:
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(3000)
        self._thread = None
        self._worker = None

    def _run_in_thread(self, fn, *args, **kwargs) -> None:
        if not _PYSIDE6_OK:
            return
        self._stop_thread()
        self._set_buttons_enabled(False)
        self._status_label.setText("Running...")

        thread = QThread()
        worker = _WorkerBase(fn, *args, **kwargs)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self._on_worker_finished)
        worker.error.connect(self._on_worker_error)
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        thread.finished.connect(thread.deleteLater)

        self._thread = thread
        self._worker = worker
        thread.start()

    def _set_buttons_enabled(self, enabled: bool) -> None:
        for btn in (self._btn_quick_reg, self._btn_full_reg,
                    self._btn_checklist, self._btn_report):
            btn.setEnabled(enabled)

    # ------------------------------------------------------------------
    # Action handlers
    # ------------------------------------------------------------------

    def _on_run_quick_regression(self) -> None:
        if not self._adapter:
            self._show_error("Adapter not available.")
            return
        self._run_in_thread(self._adapter.run_quick_regression, self.mode)

    def _on_run_full_regression(self) -> None:
        if not self._adapter:
            self._show_error("Adapter not available.")
            return
        self._run_in_thread(self._adapter.run_full_regression, self.mode)

    def _on_run_checklist(self) -> None:
        if not self._adapter:
            self._show_error("Adapter not available.")
            return
        self._run_in_thread(self._adapter.run_checklist, self.mode)

    def _on_generate_report(self) -> None:
        if not self._adapter:
            self._show_error("Adapter not available.")
            return
        self._run_in_thread(
            self._adapter.generate_report,
            self.mode,
            self._last_regression,
            None,
        )

    def _on_open_release_notes(self) -> None:
        notes_path = os.path.join(BASE_DIR, "docs", "release_v0.4.0.md")
        if os.path.exists(notes_path):
            try:
                os.startfile(notes_path)
            except Exception as exc:
                self._show_error(f"Could not open release notes: {exc}")
        else:
            self._show_error(f"Release notes not found: {notes_path}")

    # ------------------------------------------------------------------
    # Worker callbacks
    # ------------------------------------------------------------------

    def _on_worker_finished(self, result: dict) -> None:
        self._set_buttons_enabled(True)
        self._status_label.setText("Done.")

        # Detect result type by keys present
        if "tests" in result:
            # Regression result
            self._last_regression = result
            self._populate_regression_table(result)
            status = result.get("status", "UNKNOWN")
            color = _status_color(status)
            self._update_card(self._card_regression, status, color)
        elif "items" in result:
            # Checklist result
            status = result.get("status", "UNKNOWN")
            color = _status_color(status)
            passed  = result.get("passed", 0)
            failed  = result.get("failed", 0)
            self._status_label.setText(
                f"Checklist: {status} | Passed: {passed} | Failed: {failed}"
            )
        elif "path" in result:
            # Report generation result
            path = result.get("path") or "(none)"
            err  = result.get("error")
            if err:
                self._status_label.setText(f"Report failed: {err}")
            else:
                self._status_label.setText(f"Report saved: {path}")

    def _on_worker_error(self, error_msg: str) -> None:
        self._set_buttons_enabled(True)
        self._status_label.setText(f"Error: {error_msg}")
        logger.error("ReleaseStatusPanel worker error: %s", error_msg)

    # ------------------------------------------------------------------
    # Regression table population
    # ------------------------------------------------------------------

    def _populate_regression_table(self, result: dict) -> None:
        tests = result.get("tests", [])
        if not tests:
            self._reg_table.hide()
            self._reg_empty_label.show()
            return

        self._reg_empty_label.hide()
        self._reg_table.show()
        self._reg_table.setRowCount(0)

        for test in tests:
            row = self._reg_table.rowCount()
            self._reg_table.insertRow(row)

            name_item = QTableWidgetItem(test.get("name", ""))
            self._reg_table.setItem(row, 0, name_item)

            status = test.get("status", "UNKNOWN")
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(_status_color(status)))
            self._reg_table.setItem(row, 1, status_item)

            dur_item = QTableWidgetItem(f"{test.get('duration_ms', 0):.1f}")
            dur_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self._reg_table.setItem(row, 2, dur_item)

            detail = str(test.get("detail", ""))[:200]
            self._reg_table.setItem(row, 3, QTableWidgetItem(detail))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _show_error(self, msg: str) -> None:
        if _PYSIDE6_OK:
            QMessageBox.warning(self, "Release Status", msg)
        else:
            logger.warning("ReleaseStatusPanel: %s", msg)

    # ------------------------------------------------------------------
    # Close event
    # ------------------------------------------------------------------

    def closeEvent(self, event) -> None:
        self._stop_thread()
        if _PYSIDE6_OK:
            super().closeEvent(event)
