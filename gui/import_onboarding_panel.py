"""
gui/import_onboarding_panel.py — Data Import & Batch Onboarding panel for TW Quant Cockpit v1.1.1.

[!] Research Only. No Real Orders. dry_run=True default.
[!] REPLACE_EXPLICIT and destructive import are disabled.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_PYSIDE6_AVAILABLE = False
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem,
        QHeaderView, QTextEdit, QFrame, QFileDialog,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QFont, QColor
    _PYSIDE6_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Stub classes when PySide6 is unavailable
# ---------------------------------------------------------------------------

if not _PYSIDE6_AVAILABLE:
    class ImportOnboardingPanel:  # type: ignore
        """Stub ImportOnboardingPanel — PySide6 not available."""
        research_only  = True
        no_real_orders = True

        def __init__(self, *args, **kwargs):
            logger.warning("ImportOnboardingPanel: PySide6 not available — stub only")

else:
    # ---------------------------------------------------------------------------
    # Worker thread for long operations
    # ---------------------------------------------------------------------------
    class _OnboardingWorker(QThread):
        """QThread worker for discover / validate / plan / execute operations."""
        finished = Signal(object)
        error    = Signal(str)

        def __init__(self, task: str, path: str = "", mode: str = "MERGE_SAFE",
                     dry_run: bool = True, allow_write: bool = False, parent=None):
            super().__init__(parent)
            self._task       = task
            self._path       = path
            self._mode       = mode
            self._dry_run    = dry_run
            self._allow_write = allow_write

        def run(self):
            try:
                from gui.import_onboarding_adapter import ImportOnboardingAdapter
                adapter = ImportOnboardingAdapter()
                if self._task == "discover":
                    result = adapter.discover(self._path)
                elif self._task == "validate":
                    result = adapter.validate(self._path)
                elif self._task == "plan":
                    result = adapter.build_plan(self._path, mode=self._mode, dry_run=self._dry_run)
                elif self._task == "execute":
                    result = adapter.execute("", allow_write=self._allow_write)
                elif self._task == "coverage":
                    result = adapter.refresh_coverage()
                elif self._task == "report":
                    result = adapter.build_report()
                else:
                    result = {"error": f"Unknown task: {self._task}"}
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    # ---------------------------------------------------------------------------
    # Main panel
    # ---------------------------------------------------------------------------
    class ImportOnboardingPanel(QWidget):
        """
        Data Import & Batch Onboarding panel for TW Quant Cockpit v1.1.1.

        Sections:
        A. Safety Banner
        B. Source Path + Browse
        C. Summary Cards
        D. Plan Table
        E. Action Buttons
        F. Status Log

        [!] Research Only. No Real Orders. dry_run=True default.
        [!] Destructive import DISABLED.
        """

        research_only  = True
        no_real_orders = True

        def __init__(self, mode: str = "real", parent=None) -> None:
            super().__init__(parent)
            self._mode   = mode
            self._worker = None
            self._plan   = None
            self._setup_ui()

        # ------------------------------------------------------------------
        # UI Setup
        # ------------------------------------------------------------------

        def _setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setSpacing(6)

            # A. Safety Banner
            banner = QLabel(
                "Research Only | No Real Orders | Dry Run Default | Destructive Import DISABLED"
            )
            banner.setStyleSheet(
                "background-color: #cc0000; color: white; font-weight: bold; "
                "padding: 6px; border-radius: 3px;"
            )
            banner.setAlignment(Qt.AlignCenter)
            layout.addWidget(banner)

            # B. Source Path
            path_row = QHBoxLayout()
            self._path_edit = QLineEdit()
            self._path_edit.setPlaceholderText("Source directory or file path…")
            browse_btn = QPushButton("Browse")
            browse_btn.clicked.connect(self._on_browse)
            path_row.addWidget(QLabel("Source:"))
            path_row.addWidget(self._path_edit, 1)
            path_row.addWidget(browse_btn)
            layout.addLayout(path_row)

            # C. Summary Cards
            cards_row = QHBoxLayout()
            self._card_total     = self._make_card("Total Files", "0")
            self._card_xq_excel  = self._make_card("XQ Excel",   "0")
            self._card_xq_csv    = self._make_card("XQ CSV",     "0")
            self._card_csv       = self._make_card("CSV",        "0")
            self._card_conflicts = self._make_card("Conflicts",  "0")
            self._card_blocked   = self._make_card("Blocked",    "0")
            for card in (self._card_total, self._card_xq_excel, self._card_xq_csv,
                         self._card_csv, self._card_conflicts, self._card_blocked):
                cards_row.addWidget(card)
            layout.addLayout(cards_row)

            # D. Plan Table
            self._table = QTableWidget(0, 7)
            self._table.setHorizontalHeaderLabels(
                ["File", "Symbol", "Dataset", "Action", "Mode", "Rows", "Status"]
            )
            self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            for col in range(1, 7):
                self._table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
            layout.addWidget(self._table)

            # E. Buttons
            btn_row = QHBoxLayout()
            self._btn_discover = QPushButton("Discover")
            self._btn_validate = QPushButton("Validate")
            self._btn_plan     = QPushButton("Build Plan")
            self._btn_execute  = QPushButton("Execute Safe")
            self._btn_execute.setEnabled(False)
            self._btn_conflicts = QPushButton("Export Conflicts")
            self._btn_coverage  = QPushButton("Refresh Coverage")
            self._btn_report    = QPushButton("Build Report")

            self._btn_discover.clicked.connect(self._on_discover)
            self._btn_validate.clicked.connect(self._on_validate)
            self._btn_plan.clicked.connect(self._on_plan)
            self._btn_execute.clicked.connect(self._on_execute)
            self._btn_conflicts.clicked.connect(self._on_export_conflicts)
            self._btn_coverage.clicked.connect(self._on_coverage)
            self._btn_report.clicked.connect(self._on_report)

            for btn in (self._btn_discover, self._btn_validate, self._btn_plan,
                        self._btn_execute, self._btn_conflicts, self._btn_coverage, self._btn_report):
                btn_row.addWidget(btn)
            layout.addLayout(btn_row)

            # Mode selector
            mode_row = QHBoxLayout()
            mode_row.addWidget(QLabel("Import Mode:"))
            self._mode_combo = QComboBox()
            self._mode_combo.addItems(["MERGE_SAFE", "APPEND_SAFE"])
            # NOTE: REPLACE_EXPLICIT intentionally NOT listed (disabled)
            mode_row.addWidget(self._mode_combo)
            mode_row.addStretch()
            layout.addLayout(mode_row)

            # F. Status Log
            self._log = QTextEdit()
            self._log.setReadOnly(True)
            self._log.setMaximumHeight(140)
            self._log.setPlaceholderText("Status log…")
            layout.addWidget(self._log)

            self._log_msg("Panel ready. Research Only | No Real Orders | Dry Run Default.")

        def _make_card(self, title: str, value: str) -> QFrame:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Box | QFrame.Plain)
            vl = QVBoxLayout(frame)
            lbl_title = QLabel(title)
            lbl_title.setAlignment(Qt.AlignCenter)
            lbl_val = QLabel(value)
            lbl_val.setAlignment(Qt.AlignCenter)
            f = QFont()
            f.setBold(True)
            f.setPointSize(14)
            lbl_val.setFont(f)
            vl.addWidget(lbl_title)
            vl.addWidget(lbl_val)
            frame.setProperty("_val_label", lbl_val)
            return frame

        def _set_card(self, card: QFrame, value: str):
            lbl = card.property("_val_label")
            if lbl:
                lbl.setText(value)

        def _log_msg(self, msg: str):
            self._log.append(msg)

        # ------------------------------------------------------------------
        # Handlers
        # ------------------------------------------------------------------

        def _on_browse(self):
            path = QFileDialog.getExistingDirectory(self, "Select Source Directory")
            if path:
                self._path_edit.setText(path)

        def _on_discover(self):
            path = self._path_edit.text().strip()
            if not path:
                self._log_msg("[ERROR] Enter a source path first.")
                return
            self._log_msg(f"Discovering files in: {path}")
            self._run_worker("discover", path=path)

        def _on_validate(self):
            path = self._path_edit.text().strip()
            if not path:
                self._log_msg("[ERROR] Enter a source path first.")
                return
            self._log_msg(f"Validating files in: {path}")
            self._run_worker("validate", path=path)

        def _on_plan(self):
            path = self._path_edit.text().strip()
            if not path:
                self._log_msg("[ERROR] Enter a source path first.")
                return
            mode = self._mode_combo.currentText()
            self._log_msg(f"Building import plan for: {path} | mode={mode}")
            self._run_worker("plan", path=path, mode=mode)

        def _on_execute(self):
            self._log_msg("[INFO] Executing SAFE import (dry_run=True, allow_write=False)...")
            self._run_worker("execute", allow_write=False)

        def _on_export_conflicts(self):
            self._log_msg("[INFO] Exporting conflicts list…")
            try:
                from data_onboarding.onboarding_store import OnboardingStore
                store = OnboardingStore()
                plan = store.load_latest_plan()
                if plan:
                    conflicts = [i for i in plan.items if i.action == "REVIEW"]
                    self._log_msg(f"[INFO] {len(conflicts)} conflict file(s) require review.")
                else:
                    self._log_msg("[INFO] No plan loaded.")
            except Exception as exc:
                self._log_msg(f"[ERROR] {exc}")

        def _on_coverage(self):
            self._log_msg("[INFO] Refreshing universe coverage…")
            self._run_worker("coverage")

        def _on_report(self):
            self._log_msg("[INFO] Building onboarding report…")
            self._run_worker("report")

        # ------------------------------------------------------------------
        # Worker
        # ------------------------------------------------------------------

        def _run_worker(self, task: str, path: str = "", mode: str = "MERGE_SAFE",
                        dry_run: bool = True, allow_write: bool = False):
            if self._worker and self._worker.isRunning():
                self._log_msg("[WARN] Another operation is in progress.")
                return
            self._worker = _OnboardingWorker(
                task=task, path=path, mode=mode,
                dry_run=dry_run, allow_write=allow_write,
            )
            self._worker.finished.connect(self._on_worker_finished)
            self._worker.error.connect(self._on_worker_error)
            self._worker.start()

        def _on_worker_finished(self, result):
            if isinstance(result, list):
                self._handle_list_result(result)
            elif isinstance(result, dict):
                self._handle_dict_result(result)
            elif isinstance(result, str):
                self._log_msg(f"[OK] {result}")
            else:
                self._log_msg(f"[OK] Operation complete: {type(result).__name__}")

        def _on_worker_error(self, error_msg: str):
            self._log_msg(f"[ERROR] {error_msg}")

        def _handle_list_result(self, items: list):
            """Handle discover/validate results."""
            if not items:
                self._log_msg("[OK] No items found.")
                return

            # Count by file type or status
            total = len(items)
            self._set_card(self._card_total, str(total))

            if items and "file_type" in items[0]:
                from collections import Counter
                types = Counter(i.get("file_type", "UNKNOWN") for i in items)
                self._set_card(self._card_xq_excel, str(types.get("XQ_EXCEL", 0)))
                self._set_card(self._card_xq_csv,   str(types.get("XQ_CSV", 0)))
                self._set_card(self._card_csv,       str(types.get("STANDARD_CSV", 0)))
                self._log_msg(f"[OK] Discovered {total} file(s).")
            else:
                blocked = sum(1 for i in items if i.get("status") in ("FAIL", "BLOCKED"))
                self._set_card(self._card_blocked, str(blocked))
                self._log_msg(f"[OK] Validated {total} file(s). {blocked} blocked/failed.")

        def _handle_dict_result(self, result: dict):
            """Handle plan/execute/coverage results."""
            if "error" in result:
                self._log_msg(f"[ERROR] {result['error']}")
                return

            if "items" in result:
                # Import plan
                self._plan = result
                items = result.get("items", [])
                self._table.setRowCount(0)
                conflicts = 0
                blocked   = 0
                for item in items:
                    row = self._table.rowCount()
                    self._table.insertRow(row)
                    fn = os.path.basename(item.get("file_path", ""))
                    cells = [
                        fn,
                        item.get("symbol") or "-",
                        item.get("dataset", "-"),
                        item.get("action", "-"),
                        item.get("import_mode", "-"),
                        str(item.get("expected_new_rows", 0)),
                        item.get("validation_status", "-"),
                    ]
                    for col, val in enumerate(cells):
                        self._table.setItem(row, col, QTableWidgetItem(val))
                    if item.get("action") == "REVIEW":
                        conflicts += 1
                    if item.get("action") == "BLOCKED":
                        blocked += 1

                self._set_card(self._card_total,     str(len(items)))
                self._set_card(self._card_conflicts,  str(conflicts))
                self._set_card(self._card_blocked,    str(blocked))
                self._btn_execute.setEnabled(True)
                total = result.get("total_files", len(items))
                merge = result.get("merge_safe_count", 0)
                self._log_msg(
                    f"[OK] Plan built: {total} files | MERGE_SAFE={merge} | "
                    f"REVIEW={conflicts} | BLOCKED={blocked}"
                )
            elif "succeeded" in result:
                # Batch summary
                self._log_msg(
                    f"[OK] Batch done: succeeded={result.get('succeeded',0)} "
                    f"failed={result.get('failed',0)} skipped={result.get('skipped',0)} "
                    f"blocked={result.get('blocked',0)} dry_run={result.get('dry_run',True)}"
                )
            else:
                self._log_msg(f"[OK] Operation complete: {result}")
