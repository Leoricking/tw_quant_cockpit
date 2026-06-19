"""
gui/real_data_provider_panel.py — Real Data Provider Panel for v1.3.2.
[!] Research Only. No Real Orders. No Broker. Not Investment Advice.
[!] No order buttons. No credential input. Worker thread safety.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety constants
# ---------------------------------------------------------------------------
NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True

# ---------------------------------------------------------------------------
# PySide6 optional import — graceful degradation
# ---------------------------------------------------------------------------
_PYSIDE6_AVAILABLE = False
try:
    from PySide6.QtCore import Qt, QThread, Signal, Slot
    from PySide6.QtGui import QColor, QFont
    from PySide6.QtWidgets import (
        QCheckBox,
        QComboBox,
        QFormLayout,
        QGroupBox,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QLineEdit,
        QPushButton,
        QSizePolicy,
        QSplitter,
        QTabWidget,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
    _PYSIDE6_AVAILABLE = True
except ImportError:
    pass

try:
    from data.providers.real_data_provider_models import (
        ProviderCapability,
        ProviderStatus,
        ProviderType,
    )
    from data.providers.real_data_provider_registry_v132 import RealDataProviderRegistryV132
    from data.providers.real_data_provider_service import RealDataProviderService
    _MODELS_AVAILABLE = True
except ImportError:
    _MODELS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Stub for no-PySide6 environment
# ---------------------------------------------------------------------------

if not _PYSIDE6_AVAILABLE:

    class RealDataProviderPanel:  # type: ignore[no-redef]
        """Stub when PySide6 is not available."""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "PySide6 is required for RealDataProviderPanel. "
                "Install it with: pip install PySide6"
            )

else:
    # -----------------------------------------------------------------------
    # Worker thread for non-blocking provider requests
    # -----------------------------------------------------------------------

    class _ProviderRequestWorker(QThread):
        """Runs a provider request in a background thread."""
        result_ready = Signal(dict)
        error_occurred = Signal(str)

        def __init__(self, service, provider_id: str, capability: str,
                     symbol: str, start_date: str, end_date: str,
                     force_refresh: bool) -> None:
            super().__init__()
            self._service = service
            self._provider_id = provider_id
            self._capability = capability
            self._symbol = symbol
            self._start_date = start_date
            self._end_date = end_date
            self._force_refresh = force_refresh
            self._stopped = False

        def stop(self) -> None:
            self._stopped = True

        def run(self) -> None:
            if self._stopped:
                return
            try:
                from data.providers.real_data_provider_models import ProviderRequest
                req = ProviderRequest(
                    provider_id=self._provider_id,
                    capability=self._capability,
                    symbols=[self._symbol] if self._symbol else [],
                    start_date=self._start_date,
                    end_date=self._end_date,
                    force_refresh=self._force_refresh,
                )
                if self._service is not None:
                    resp = self._service.request(req)
                    self.result_ready.emit(resp.to_dict())
                else:
                    self.result_ready.emit({
                        "status": "UNAVAILABLE",
                        "errors": ["No provider service configured."],
                        "records": [],
                        "record_count": 0,
                    })
            except Exception as exc:
                if not self._stopped:
                    self.error_occurred.emit(str(exc))

    # -----------------------------------------------------------------------
    # Main panel
    # -----------------------------------------------------------------------

    class RealDataProviderPanel(QWidget):
        """
        Real Data Provider status and inspection panel for v1.3.2.

        [!] No order buttons. No credential input fields.
        [!] Worker thread for requests — no UI freeze.
        [!] FHD/4K compatible (no fixed sizes).
        """

        SAFETY_BANNER = (
            "Research Only | No Real Orders | Broker Execution DISABLED | "
            "Production Trading BLOCKED | Data Provider != Broker | "
            "Real Mode Never Falls Back To Mock"
        )

        _PROVIDER_COLUMNS = [
            "Provider", "Type", "Enabled", "Status", "Markets",
            "Capabilities", "Auth Required", "Batch", "Historical",
            "Intraday", "Cache", "Last Success", "Last Failure", "Warning",
        ]

        def __init__(
            self,
            registry=None,
            service=None,
            parent=None,
        ) -> None:
            super().__init__(parent)
            self._registry = registry
            self._service = service
            self._worker: "_ProviderRequestWorker | None" = None
            self._setup_ui()

        def _setup_ui(self) -> None:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(8, 8, 8, 8)
            layout.setSpacing(6)

            # Safety banner
            banner = QLabel(self.SAFETY_BANNER)
            banner.setWordWrap(True)
            banner.setStyleSheet(
                "background-color: #8B0000; color: white; "
                "font-weight: bold; padding: 6px; border-radius: 3px;"
            )
            banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout.addWidget(banner)

            # Tab widget
            tabs = QTabWidget()
            tabs.addTab(self._build_provider_status_tab(), "Provider Status")
            tabs.addTab(self._build_capability_matrix_tab(), "Capability Matrix")
            tabs.addTab(self._build_request_inspector_tab(), "Request Inspector")
            layout.addWidget(tabs)

        # ------------------------------------------------------------------
        # Tab builders
        # ------------------------------------------------------------------

        def _build_provider_status_tab(self) -> QWidget:
            w = QWidget()
            vl = QVBoxLayout(w)
            vl.setContentsMargins(4, 4, 4, 4)

            refresh_btn = QPushButton("Refresh Provider Status")
            refresh_btn.clicked.connect(self._refresh_provider_status)
            vl.addWidget(refresh_btn)

            self._provider_table = QTableWidget(0, len(self._PROVIDER_COLUMNS))
            self._provider_table.setHorizontalHeaderLabels(self._PROVIDER_COLUMNS)
            self._provider_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._provider_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._provider_table.setAlternatingRowColors(True)
            vl.addWidget(self._provider_table)

            self._refresh_provider_status()
            return w

        def _build_capability_matrix_tab(self) -> QWidget:
            w = QWidget()
            vl = QVBoxLayout(w)
            vl.setContentsMargins(4, 4, 4, 4)

            refresh_btn = QPushButton("Refresh Capability Matrix")
            refresh_btn.clicked.connect(self._refresh_capability_matrix)
            vl.addWidget(refresh_btn)

            self._matrix_table = QTableWidget(0, 0)
            self._matrix_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._matrix_table.setAlternatingRowColors(True)
            vl.addWidget(self._matrix_table)

            self._refresh_capability_matrix()
            return w

        def _build_request_inspector_tab(self) -> QWidget:
            w = QWidget()
            vl = QVBoxLayout(w)
            vl.setContentsMargins(4, 4, 4, 4)

            form = QFormLayout()
            self._provider_combo = QComboBox()
            self._provider_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
            self._capability_combo = QComboBox()
            if _MODELS_AVAILABLE:
                caps = ProviderCapability.all_capabilities()
                self._capability_combo.addItems(caps)
            self._symbol_input = QLineEdit()
            self._symbol_input.setPlaceholderText("e.g. 2330")
            self._start_date_input = QLineEdit()
            self._start_date_input.setPlaceholderText("YYYY-MM-DD")
            self._end_date_input = QLineEdit()
            self._end_date_input.setPlaceholderText("YYYY-MM-DD")
            self._force_refresh_check = QCheckBox()

            form.addRow("Provider:", self._provider_combo)
            form.addRow("Capability:", self._capability_combo)
            form.addRow("Symbol:", self._symbol_input)
            form.addRow("Start Date:", self._start_date_input)
            form.addRow("End Date:", self._end_date_input)
            form.addRow("Force Refresh:", self._force_refresh_check)
            vl.addLayout(form)

            btn_row = QHBoxLayout()
            self._execute_btn = QPushButton("Execute Read-Only Request")
            self._execute_btn.clicked.connect(self._execute_request)
            self._stop_btn = QPushButton("Stop")
            self._stop_btn.setEnabled(False)
            self._stop_btn.clicked.connect(self._stop_worker)
            btn_row.addWidget(self._execute_btn)
            btn_row.addWidget(self._stop_btn)
            btn_row.addStretch()
            vl.addLayout(btn_row)

            self._status_label = QLabel("Ready.")
            vl.addWidget(self._status_label)

            self._results_display = QTextEdit()
            self._results_display.setReadOnly(True)
            self._results_display.setPlaceholderText("Request results will appear here.")
            vl.addWidget(self._results_display)

            extra_btn_row = QHBoxLayout()
            prov_btn = QPushButton("View Provenance")
            prov_btn.clicked.connect(self._view_provenance)
            err_btn = QPushButton("View Errors")
            err_btn.clicked.connect(self._view_errors)
            extra_btn_row.addWidget(prov_btn)
            extra_btn_row.addWidget(err_btn)
            extra_btn_row.addStretch()
            vl.addLayout(extra_btn_row)

            self._last_response: dict = {}
            self._populate_provider_combo()
            return w

        # ------------------------------------------------------------------
        # Refresh methods
        # ------------------------------------------------------------------

        def _refresh_provider_status(self) -> None:
            self._provider_table.setRowCount(0)
            if self._registry is None:
                return
            try:
                providers = self._registry.list()
            except Exception as exc:
                logger.warning("Failed to list providers: %s", exc)
                return

            for meta in providers:
                row = self._provider_table.rowCount()
                self._provider_table.insertRow(row)
                adapter = self._registry.get(meta.provider_id)
                try:
                    status = adapter.get_status() if adapter else ProviderStatus.UNAVAILABLE
                except Exception:
                    status = ProviderStatus.UNAVAILABLE

                cells = [
                    meta.provider_id,
                    meta.provider_type,
                    "Yes" if meta.enabled else "No",
                    status,
                    ", ".join(meta.markets) if meta.markets else "(all)",
                    ", ".join(meta.capabilities[:3]) + ("..." if len(meta.capabilities) > 3 else ""),
                    "Yes" if meta.requires_auth else "No",
                    "Yes" if meta.supports_batch else "No",
                    "Yes" if meta.supports_historical else "No",
                    "Yes" if meta.supports_intraday else "No",
                    str(meta.cache_policy) if meta.cache_policy else "-",
                    "-",  # Last success (not tracked here)
                    "-",  # Last failure
                    "AUTH_REQUIRED" if meta.requires_auth else "",
                ]
                for col, val in enumerate(cells):
                    item = QTableWidgetItem(str(val))
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self._provider_table.setItem(row, col, item)

        def _refresh_capability_matrix(self) -> None:
            if self._registry is None:
                return
            try:
                matrix = self._registry.get_capability_matrix()
            except Exception as exc:
                logger.warning("Failed to build capability matrix: %s", exc)
                return

            provider_ids = sorted(matrix.keys())
            if not provider_ids:
                return
            caps = list(next(iter(matrix.values())).keys()) if matrix else []

            self._matrix_table.setColumnCount(len(provider_ids))
            self._matrix_table.setRowCount(len(caps))
            self._matrix_table.setHorizontalHeaderLabels(provider_ids)
            self._matrix_table.setVerticalHeaderLabels(caps)

            for col, pid in enumerate(provider_ids):
                for row, cap in enumerate(caps):
                    val = matrix.get(pid, {}).get(cap, "UNKNOWN")
                    item = QTableWidgetItem(str(val))
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self._matrix_table.setItem(row, col, item)

            self._matrix_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        def _populate_provider_combo(self) -> None:
            self._provider_combo.clear()
            self._provider_combo.addItem("(auto-resolve)")
            if self._registry is not None:
                try:
                    for meta in self._registry.list():
                        self._provider_combo.addItem(meta.provider_id)
                except Exception:
                    pass

        # ------------------------------------------------------------------
        # Request execution
        # ------------------------------------------------------------------

        def _execute_request(self) -> None:
            self._stop_worker()
            provider_id = self._provider_combo.currentText()
            if provider_id == "(auto-resolve)":
                provider_id = ""
            capability = self._capability_combo.currentText()
            symbol = self._symbol_input.text().strip()
            start_date = self._start_date_input.text().strip()
            end_date = self._end_date_input.text().strip()
            force_refresh = self._force_refresh_check.isChecked()

            self._status_label.setText("Executing read-only request...")
            self._execute_btn.setEnabled(False)
            self._stop_btn.setEnabled(True)

            self._worker = _ProviderRequestWorker(
                self._service, provider_id, capability,
                symbol, start_date, end_date, force_refresh,
            )
            self._worker.result_ready.connect(self._on_result_ready)
            self._worker.error_occurred.connect(self._on_worker_error)
            self._worker.finished.connect(self._on_worker_finished)
            self._worker.start()

        def _stop_worker(self) -> None:
            if self._worker is not None:
                self._worker.stop()
                self._worker.wait(2000)
                self._worker = None
            self._execute_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)

        @Slot(dict)
        def _on_result_ready(self, result: dict) -> None:
            self._last_response = result
            import json
            try:
                text = json.dumps(result, indent=2, default=str)
            except Exception:
                text = str(result)
            self._results_display.setPlainText(text)
            status = result.get("status", "UNKNOWN")
            count = result.get("record_count", 0)
            self._status_label.setText(f"Done. Status: {status} | Records: {count}")

        @Slot(str)
        def _on_worker_error(self, msg: str) -> None:
            self._results_display.setPlainText(f"[ERROR] {msg}")
            self._status_label.setText(f"Error: {msg[:80]}")

        def _on_worker_finished(self) -> None:
            self._execute_btn.setEnabled(True)
            self._stop_btn.setEnabled(False)

        def _view_provenance(self) -> None:
            import json
            provenance = self._last_response.get("provenance", {})
            text = json.dumps(provenance, indent=2, default=str) if provenance else "(no provenance)"
            self._results_display.setPlainText(f"=== Provenance ===\n{text}")

        def _view_errors(self) -> None:
            errors = self._last_response.get("errors", [])
            warnings = self._last_response.get("warnings", [])
            lines = ["=== Errors ==="] + (errors or ["(none)"]) + ["", "=== Warnings ==="] + (warnings or ["(none)"])
            self._results_display.setPlainText("\n".join(lines))

        # ------------------------------------------------------------------
        # Cleanup
        # ------------------------------------------------------------------

        def closeEvent(self, event) -> None:
            self._stop_worker()
            super().closeEvent(event)
