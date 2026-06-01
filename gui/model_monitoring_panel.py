"""
gui/model_monitoring_panel.py — Model Monitoring GUI panel (v0.4.3).

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
[!] Actions run in QThread to avoid GUI freeze.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QFrame,
        QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox,
        QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QColor
    _PYSIDE6_OK = True
except ImportError:
    _PYSIDE6_OK = False
    logger.warning("PySide6 not available — ModelMonitoringPanel will be a stub")


# ---------------------------------------------------------------------------
# Worker threads
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _MonitoringWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode: str = "real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.model_monitoring_adapter import ModelMonitoringAdapter
                result = ModelMonitoringAdapter().refresh_summary(mode=self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _DriftWorker(QThread):
        finished = Signal(dict)

        def run(self):
            try:
                from gui.model_monitoring_adapter import ModelMonitoringAdapter
                result = ModelMonitoringAdapter().run_drift_check()
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _HitMissWorker(QThread):
        finished = Signal(dict)

        def __init__(self, horizon: int = 5):
            super().__init__()
            self._horizon = horizon

        def run(self):
            try:
                from gui.model_monitoring_adapter import ModelMonitoringAdapter
                result = ModelMonitoringAdapter().run_hit_miss_review(horizon=self._horizon)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _ReportWorker(QThread):
        finished = Signal(dict)

        def __init__(self, mode: str = "real"):
            super().__init__()
            self._mode = mode

        def run(self):
            try:
                from gui.model_monitoring_adapter import ModelMonitoringAdapter
                result = ModelMonitoringAdapter().generate_report(mode=self._mode)
            except Exception as exc:
                result = {"ok": False, "error": str(exc)}
            self.finished.emit(result)

    class _ModelsWorker(QThread):
        finished = Signal(dict)

        def run(self):
            try:
                from gui.model_monitoring_adapter import ModelMonitoringAdapter
                result = ModelMonitoringAdapter().list_models()
            except Exception as exc:
                result = {"ok": False, "error": str(exc), "models": []}
            self.finished.emit(result)

    class _PredictionsWorker(QThread):
        finished = Signal(dict)

        def run(self):
            try:
                from gui.model_monitoring_adapter import ModelMonitoringAdapter
                result = ModelMonitoringAdapter().list_predictions()
            except Exception as exc:
                result = {"ok": False, "error": str(exc), "predictions": []}
            self.finished.emit(result)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lbl(text, bold=False, color=None, size=None):
    if not _PYSIDE6_OK:
        return None
    lbl = QLabel(text)
    parts = []
    if bold:
        parts.append("font-weight:bold")
    if color:
        parts.append(f"color:{color}")
    if size:
        parts.append(f"font-size:{size}px")
    if parts:
        lbl.setStyleSheet(";".join(parts))
    return lbl


def _make_table(headers):
    if not _PYSIDE6_OK:
        return None
    t = QTableWidget()
    t.setColumnCount(len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.setEditTriggers(QTableWidget.NoEditTriggers)
    t.setAlternatingRowColors(True)
    t.setStyleSheet("""
        QTableWidget { background:#12121E; color:#EEEEEE; gridline-color:#333355; }
        QTableWidget::item:alternate { background:#1A1A2E; }
        QHeaderView::section { background:#252540; color:#AAFFAA; font-weight:bold; }
    """)
    return t


_BTN_STYLE = (
    "QPushButton { background:#252540; color:#CCCCFF; border:1px solid #444488; "
    "border-radius:3px; padding:4px 10px; } "
    "QPushButton:hover { background:#334466; } "
    "QPushButton:disabled { color:#555555; }"
)

_GRP_STYLE = (
    "QGroupBox { color:#AAFFAA; font-weight:bold; border:1px solid #335533; "
    "border-radius:4px; margin-top:6px; } "
    "QGroupBox::title { subcontrol-origin:margin; padding:0 4px; }"
)


# ---------------------------------------------------------------------------
# Register Model Dialog
# ---------------------------------------------------------------------------

if _PYSIDE6_OK:
    class _RegisterModelDialog(QDialog):
        """Simple dialog to register a model metadata entry."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Register Model Metadata")
            self.setMinimumWidth(480)
            layout = QVBoxLayout(self)

            form = QFormLayout()
            self._fields = {}
            field_defs = [
                ("model_id",            "Model ID"),
                ("model_name",          "Model Name"),
                ("model_type",          "Model Type (e.g. RandomForest)"),
                ("version",             "Version (e.g. v1.0)"),
                ("created_at",          "Created At (YYYY-MM-DD)"),
                ("feature_snapshot_id", "Feature Snapshot ID"),
                ("dataset_path",        "Dataset Path"),
                ("target_label",        "Target Label"),
                ("train_start",         "Train Start (YYYY-MM-DD)"),
                ("train_end",           "Train End (YYYY-MM-DD)"),
                ("validation_start",    "Validation Start"),
                ("validation_end",      "Validation End"),
                ("feature_count",       "Feature Count"),
                ("row_count",           "Row Count"),
                ("leakage_status",      "Leakage Status (CLEAN/WARNING/CRITICAL)"),
                ("notes",               "Notes"),
            ]
            for key, label in field_defs:
                edit = QLineEdit()
                edit.setStyleSheet("background:#1A1A2E; color:#EEEEEE; border:1px solid #444488;")
                self._fields[key] = edit
                form.addRow(QLabel(label), edit)

            layout.addLayout(form)

            btns = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self
            )
            btns.accepted.connect(self.accept)
            btns.rejected.connect(self.reject)
            layout.addWidget(btns)

        def get_values(self) -> dict:
            return {k: v.text().strip() for k, v in self._fields.items()}


# ---------------------------------------------------------------------------
# Main Panel
# ---------------------------------------------------------------------------

class ModelMonitoringPanel(QWidget if _PYSIDE6_OK else object):
    """
    Model Monitoring panel.

    [!] Monitoring Only. No Real Orders. No live prediction. No auto-trading.
    """

    def __init__(self, mode: str = "real", parent=None):
        if not _PYSIDE6_OK:
            return
        super().__init__(parent)
        self._mode    = mode
        self._workers = []
        self._build_ui()

    def _build_ui(self):
        if not _PYSIDE6_OK:
            return

        root = QVBoxLayout(self)
        root.setSpacing(6)
        root.setContentsMargins(8, 8, 8, 8)

        # ── A. Header / Safety Banner ──────────────────────────────────
        banner = QFrame()
        banner.setStyleSheet(
            "background:#0A1A0A; border:1px solid #335533; border-radius:4px; padding:4px"
        )
        ban_layout = QHBoxLayout(banner)
        ban_layout.addWidget(_lbl("Model Monitoring", bold=True, color="#AAFFAA", size=13))
        ban_layout.addSpacing(12)
        for text, color in [
            ("Monitoring Only",         "#AAFFAA"),
            ("No Live Prediction",      "#FFDDAA"),
            ("No Real Orders",          "#FFAAAA"),
            ("Production Trading BLOCKED", "#FF6666"),
        ]:
            tag = QLabel(f"[{text}]")
            tag.setStyleSheet(f"color:{color};font-weight:bold;font-size:11px")
            ban_layout.addWidget(tag)
        ban_layout.addStretch()
        root.addWidget(banner)

        # ── B. Summary Cards ──────────────────────────────────────────
        card_box = QGroupBox("Summary")
        card_box.setStyleSheet(_GRP_STYLE)
        card_layout = QHBoxLayout(card_box)
        self._lbl_model_count  = _lbl("Model Count: —",      color="#AAAAAA")
        self._lbl_pred_count   = _lbl("Predictions: —",      color="#AAAAAA")
        self._lbl_reviewed     = _lbl("Reviewed: —",         color="#AAAAAA")
        self._lbl_hit_rate     = _lbl("Hit Rate: —",         color="#AAAAAA")
        self._lbl_drift        = _lbl("Drift: —",            color="#AAAAAA")
        self._lbl_degradation  = _lbl("Degradation: —",      color="#AAAAAA")
        for lbl in [
            self._lbl_model_count, self._lbl_pred_count, self._lbl_reviewed,
            self._lbl_hit_rate, self._lbl_drift, self._lbl_degradation,
        ]:
            card_layout.addWidget(lbl)
        card_layout.addStretch()
        root.addWidget(card_box)

        # ── C. Actions ────────────────────────────────────────────────
        act_box = QGroupBox("Actions")
        act_box.setStyleSheet(_GRP_STYLE)
        act_layout = QHBoxLayout(act_box)

        self._btn_refresh     = QPushButton("Refresh Monitoring")
        self._btn_register    = QPushButton("Register Model Metadata")
        self._btn_actuals     = QPushButton("Update Actuals")
        self._btn_drift       = QPushButton("Run Drift Check")
        self._btn_report      = QPushButton("Generate Report")
        self._btn_open        = QPushButton("Open Latest Report")

        for btn in [
            self._btn_refresh, self._btn_register, self._btn_actuals,
            self._btn_drift, self._btn_report, self._btn_open,
        ]:
            btn.setStyleSheet(_BTN_STYLE)
            act_layout.addWidget(btn)
        act_layout.addStretch()
        root.addWidget(act_box)

        # ── D. Model Registry Table ────────────────────────────────────
        reg_box = QGroupBox("Model Registry")
        reg_box.setStyleSheet(_GRP_STYLE)
        reg_layout = QVBoxLayout(reg_box)
        self._reg_table = _make_table([
            "Model ID", "Name", "Type", "Target",
            "Feature Snapshot", "Leakage Status", "Monitoring Status"
        ])
        self._reg_table.setMaximumHeight(160)
        self._reg_empty = _lbl(
            "No models registered — click 'Register Model Metadata' to add one.",
            color="#888888"
        )
        reg_layout.addWidget(self._reg_table)
        reg_layout.addWidget(self._reg_empty)
        root.addWidget(reg_box)

        # ── E. Prediction Log Table ────────────────────────────────────
        pred_box = QGroupBox("Prediction Log")
        pred_box.setStyleSheet(_GRP_STYLE)
        pred_layout = QVBoxLayout(pred_box)
        self._pred_table = _make_table([
            "Prediction ID", "Symbol", "Date", "Source",
            "Horizon", "Predicted", "Actual", "Hit", "Reviewed"
        ])
        self._pred_table.setMaximumHeight(140)
        self._pred_empty = _lbl("No predictions logged yet.", color="#888888")
        pred_layout.addWidget(self._pred_table)
        pred_layout.addWidget(self._pred_empty)
        root.addWidget(pred_box)

        # ── F. Drift Table ─────────────────────────────────────────────
        drift_box = QGroupBox("Drift Detection")
        drift_box.setStyleSheet(_GRP_STYLE)
        drift_layout = QVBoxLayout(drift_box)
        self._drift_table = _make_table([
            "Feature/Label", "Baseline", "Current", "Drift Score", "Status", "Warning"
        ])
        self._drift_table.setMaximumHeight(130)
        self._drift_empty = _lbl("No drift data — click 'Run Drift Check'.", color="#888888")
        drift_layout.addWidget(self._drift_table)
        drift_layout.addWidget(self._drift_empty)
        root.addWidget(drift_box)

        # ── G. Degradation Table ───────────────────────────────────────
        deg_box = QGroupBox("Signal Degradation")
        deg_box.setStyleSheet(_GRP_STYLE)
        deg_layout = QVBoxLayout(deg_box)
        self._deg_table = _make_table([
            "Signal/Rule", "Baseline", "Recent", "Change", "Status", "Next Step"
        ])
        self._deg_table.setMaximumHeight(130)
        self._deg_empty = _lbl("No degradation data — run Refresh Monitoring.", color="#888888")
        deg_layout.addWidget(self._deg_table)
        deg_layout.addWidget(self._deg_empty)
        root.addWidget(deg_box)

        # ── H. Rule vs ML Table ────────────────────────────────────────
        rml_box = QGroupBox("Rule vs ML Comparison")
        rml_box.setStyleSheet(_GRP_STYLE)
        rml_layout = QVBoxLayout(rml_box)
        self._rml_table = _make_table([
            "Symbol", "Rule Signal", "ML Signal", "Actual", "Agreement", "Result"
        ])
        self._rml_table.setMaximumHeight(120)
        self._rml_empty = _lbl(
            "ML predictions not available — log ML predictions to enable comparison.",
            color="#888888"
        )
        rml_layout.addWidget(self._rml_table)
        rml_layout.addWidget(self._rml_empty)
        root.addWidget(rml_box)

        # ── Status line ───────────────────────────────────────────────
        self._status_lbl = _lbl(
            "Ready — Monitoring Only. No Real Orders.", color="#888888"
        )
        root.addWidget(self._status_lbl)
        root.addStretch()

        # ── Wire signals ──────────────────────────────────────────────
        self._btn_refresh.clicked.connect(self._on_refresh)
        self._btn_register.clicked.connect(self._on_register_model)
        self._btn_actuals.clicked.connect(self._on_update_actuals)
        self._btn_drift.clicked.connect(self._on_drift_check)
        self._btn_report.clicked.connect(self._on_generate_report)
        self._btn_open.clicked.connect(self._on_open_report)

    # ------------------------------------------------------------------
    # Action handlers
    # ------------------------------------------------------------------

    def _on_refresh(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Refreshing monitoring summary...")
        self._btn_refresh.setEnabled(False)
        worker = _MonitoringWorker(mode=self._mode)
        worker.finished.connect(self._on_summary_done)
        worker.finished.connect(lambda: self._btn_refresh.setEnabled(True))
        self._workers.append(worker)
        worker.start()

        # Also reload models and predictions
        self._load_models()
        self._load_predictions()

    def _on_summary_done(self, result: dict):
        if not _PYSIDE6_OK:
            return
        if result.get("ok"):
            s = result.get("summary", {})
            self._update_summary_cards(s)

            # Populate degradation table from result
            deg = s.get("details", {}).get("degradation_result", {})
            self._populate_degradation_table(deg)

            # Populate rule vs ML table
            rml = s.get("details", {}).get("rule_vs_ml_result", {})
            self._populate_rml_table(rml)

            self._set_status(
                f"Monitoring refreshed — models={s.get('model_count', 0)}, "
                f"predictions={s.get('prediction_count', 0)}, "
                f"drift={s.get('drift_status', 'N/A')}"
            )
        else:
            self._set_status(f"Refresh error: {result.get('error', '')}")

    def _on_register_model(self):
        if not _PYSIDE6_OK:
            return
        dlg = _RegisterModelDialog(parent=self)
        dlg.setStyleSheet("background:#12121E; color:#EEEEEE;")
        if dlg.exec() != QDialog.Accepted:
            return
        values = dlg.get_values()
        if not values.get("model_id"):
            self._set_status("Register model: model_id is required.")
            return
        try:
            from monitoring.model_registry import ModelRegistry, ModelMetadata
            meta = ModelMetadata(
                model_id=values.get("model_id", ""),
                model_name=values.get("model_name", ""),
                model_type=values.get("model_type", ""),
                version=values.get("version", "v1.0"),
                created_at=values.get("created_at", ""),
                feature_snapshot_id=values.get("feature_snapshot_id", ""),
                dataset_path=values.get("dataset_path", ""),
                target_label=values.get("target_label", ""),
                train_start=values.get("train_start", ""),
                train_end=values.get("train_end", ""),
                validation_start=values.get("validation_start", ""),
                validation_end=values.get("validation_end", ""),
                feature_count=int(values.get("feature_count", 0) or 0),
                row_count=int(values.get("row_count", 0) or 0),
                leakage_status=values.get("leakage_status", "UNKNOWN"),
                notes=values.get("notes", ""),
            )
            reg    = ModelRegistry()
            result = reg.register_model(meta)
            if result.get("ok"):
                self._set_status(f"Model registered: {values.get('model_id')}")
                self._load_models()
            else:
                self._set_status(f"Register error: {result.get('error', '')}")
        except Exception as exc:
            self._set_status(f"Register error: {exc}")

    def _on_update_actuals(self):
        self._set_status("Update Actuals: use PredictionLog.update_actuals() with price data.")

    def _on_drift_check(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Running drift check...")
        self._btn_drift.setEnabled(False)
        worker = _DriftWorker()
        worker.finished.connect(self._on_drift_done)
        worker.finished.connect(lambda: self._btn_drift.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_drift_done(self, result: dict):
        if not _PYSIDE6_OK:
            return
        if result.get("ok"):
            dr = result.get("drift_result", {})
            self._populate_drift_table(dr)
            status = dr.get("status", "N/A")
            color  = "#FF6666" if "CRITICAL" in status else ("#FFAA44" if "WARNING" in status or status == "WATCH" else "#44CC88")
            self._lbl_drift.setText(f"Drift: {status}")
            self._lbl_drift.setStyleSheet(f"color:{color};font-weight:bold")
            self._set_status(f"Drift check done: {status}")
        else:
            self._set_status(f"Drift check error: {result.get('error', '')}")

    def _on_generate_report(self):
        if not _PYSIDE6_OK:
            return
        self._set_status("Generating monitoring report...")
        self._btn_report.setEnabled(False)
        worker = _ReportWorker(mode=self._mode)
        worker.finished.connect(self._on_report_done)
        worker.finished.connect(lambda: self._btn_report.setEnabled(True))
        self._workers.append(worker)
        worker.start()

    def _on_report_done(self, result: dict):
        if not _PYSIDE6_OK:
            return
        if result.get("ok"):
            self._set_status(f"Report: {result.get('report_path', '')}")
        else:
            self._set_status(f"Report error: {result.get('error', '')}")

    def _on_open_report(self):
        if not _PYSIDE6_OK:
            return
        try:
            from gui.model_monitoring_adapter import ModelMonitoringAdapter
            path = ModelMonitoringAdapter().load_latest_report_path()
            if path and os.path.isfile(path):
                import subprocess, sys
                if sys.platform == "win32":
                    os.startfile(path)
                else:
                    subprocess.Popen(["xdg-open", path])
                self._set_status(f"Opened: {path}")
            else:
                self._set_status("No report found — click 'Generate Report' first.")
        except Exception as exc:
            self._set_status(f"Open report error: {exc}")

    # ------------------------------------------------------------------
    # Data loaders
    # ------------------------------------------------------------------

    def _load_models(self):
        if not _PYSIDE6_OK:
            return
        worker = _ModelsWorker()
        worker.finished.connect(self._on_models_loaded)
        self._workers.append(worker)
        worker.start()

    def _on_models_loaded(self, result: dict):
        if not _PYSIDE6_OK:
            return
        models = result.get("models", [])
        if not models:
            self._reg_empty.show()
            self._reg_table.setRowCount(0)
            return
        self._reg_empty.hide()
        self._reg_table.setRowCount(len(models))
        for row, m in enumerate(models[:100]):
            for col, val in enumerate([
                m.get("model_id", ""),
                m.get("model_name", ""),
                m.get("model_type", ""),
                m.get("target_label", ""),
                m.get("feature_snapshot_id", ""),
                m.get("leakage_status", ""),
                m.get("monitoring_status", ""),
            ]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                if col == 5:  # leakage_status
                    color = "#FF8888" if val == "CRITICAL" else ("#FFAA44" if val == "WARNING" else "#44CC88")
                    item.setForeground(QColor(color))
                if col == 6:  # monitoring_status
                    color = "#FFAA44" if val != "ACTIVE" else "#44CC88"
                    item.setForeground(QColor(color))
                self._reg_table.setItem(row, col, item)

    def _load_predictions(self):
        if not _PYSIDE6_OK:
            return
        worker = _PredictionsWorker()
        worker.finished.connect(self._on_predictions_loaded)
        self._workers.append(worker)
        worker.start()

    def _on_predictions_loaded(self, result: dict):
        if not _PYSIDE6_OK:
            return
        preds = result.get("predictions", [])
        if not preds:
            self._pred_empty.show()
            self._pred_table.setRowCount(0)
            return
        self._pred_empty.hide()
        self._pred_table.setRowCount(len(preds))
        for row, p in enumerate(preds[:200]):
            hit_val = p.get("hit")
            hit_str = ("✓" if hit_val is True else ("✗" if hit_val is False else "—"))
            for col, val in enumerate([
                p.get("prediction_id", "")[:20],
                p.get("symbol", ""),
                p.get("date", ""),
                p.get("source", ""),
                str(p.get("horizon", "")),
                str(p.get("predicted_label", "") or p.get("predicted_score", "")),
                str(p.get("actual_return", "—") if p.get("actual_return") is not None else "—"),
                hit_str,
                str(p.get("reviewed", False)),
            ]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                if col == 7:  # hit
                    color = "#44CC88" if val == "✓" else ("#FF6666" if val == "✗" else "#888888")
                    item.setForeground(QColor(color))
                self._pred_table.setItem(row, col, item)

    # ------------------------------------------------------------------
    # Table population
    # ------------------------------------------------------------------

    def _populate_drift_table(self, drift_result: dict):
        if not _PYSIDE6_OK:
            return
        rows = []
        pf = drift_result.get("feature_drift", {}).get("per_feature", {})
        for col, d in list(pf.items())[:30]:
            chg = d.get("mean_change", 0) or 0
            st  = ("CRITICAL" if chg >= 0.5 else
                   "WARNING"  if chg >= 0.25 else
                   "WATCH"    if chg >= 0.10 else "STABLE")
            rows.append([col, f"{d.get('baseline_mean', 0):.4f}", f"{d.get('current_mean', 0):.4f}",
                         f"{chg:.1%}", st, ""])

        ld = drift_result.get("label_drift", {})
        if ld.get("label_col"):
            dv = ld.get("drift_value", 0) or 0
            st = "CRITICAL" if dv >= 0.5 else ("WARNING" if dv >= 0.25 else ("WATCH" if dv >= 0.10 else "STABLE"))
            rows.append([f"[label] {ld.get('label_col', '')}", "—", "—", f"{dv:.1%}", st,
                         "Label shift detected" if st != "STABLE" else ""])

        if not rows:
            self._drift_empty.show()
            self._drift_table.setRowCount(0)
            return

        self._drift_empty.hide()
        self._drift_table.setRowCount(len(rows))
        for r, cells in enumerate(rows):
            for c, val in enumerate(cells):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                if c == 4:  # Status
                    color = ("#FF6666" if val == "CRITICAL" else
                             "#FFAA44" if val in ("WARNING", "WATCH") else "#44CC88")
                    item.setForeground(QColor(color))
                self._drift_table.setItem(r, c, item)

    def _populate_degradation_table(self, deg_result: dict):
        if not _PYSIDE6_OK:
            return
        rows = []

        rd = deg_result.get("rule_degradation", {})
        for rule in rd.get("degraded_rules", [])[:10]:
            rows.append([
                rule.get("rule_id", "?"),
                "—", "—",
                f"{rule.get('confidence', 0):.2f}",
                "DEGRADED",
                "Review rule confidence",
            ])

        sqd = deg_result.get("signal_quality_degradation", {})
        for sig in sqd.get("degraded_signals", [])[:10]:
            rows.append([
                sig.get("signal_id", sig.get("rule_id", "?")),
                "—", "—",
                str(sig.get("action", "")),
                sqd.get("status", "?"),
                "Signal quality reduced",
            ])

        if not rows:
            self._deg_empty.show()
            self._deg_table.setRowCount(0)
            return

        self._deg_empty.hide()
        self._deg_table.setRowCount(len(rows))
        for r, cells in enumerate(rows):
            for c, val in enumerate(cells):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                if c == 4:  # Status
                    color = ("#FF6666" if val in ("SEVERE", "DEGRADED") else
                             "#FFAA44" if val == "WATCH" else "#44CC88")
                    item.setForeground(QColor(color))
                self._deg_table.setItem(r, c, item)

    def _populate_rml_table(self, rml_result: dict):
        if not _PYSIDE6_OK:
            return
        if not rml_result.get("ml_available"):
            self._rml_empty.show()
            self._rml_table.setRowCount(0)
            return

        cases = rml_result.get("disagreement_cases", [])
        if not cases:
            self._rml_empty.setText("Agreement HIGH — no significant disagreements found.")
            self._rml_empty.show()
            self._rml_table.setRowCount(0)
            return

        self._rml_empty.hide()
        self._rml_table.setRowCount(len(cases[:50]))
        for r, c in enumerate(cases[:50]):
            r_sig = c.get("rule_signal", "")
            m_sig = c.get("ml_signal", "")
            for col, val in enumerate([
                c.get("symbol", ""),
                r_sig,
                m_sig,
                "—",
                "DISAGREE",
                "Review",
            ]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                if col == 4:
                    item.setForeground(QColor("#FFAA44"))
                self._rml_table.setItem(r, col, item)

    # ------------------------------------------------------------------
    # Summary cards update
    # ------------------------------------------------------------------

    def _update_summary_cards(self, s: dict):
        if not _PYSIDE6_OK:
            return
        self._lbl_model_count.setText(f"Model Count: {s.get('model_count', 0)}")
        self._lbl_pred_count.setText(f"Predictions: {s.get('prediction_count', 0)}")
        self._lbl_reviewed.setText(f"Reviewed: {s.get('reviewed_count', 0)}")
        hr = s.get("hit_rate")
        self._lbl_hit_rate.setText(f"Hit Rate: {hr:.1%}" if hr is not None else "Hit Rate: N/A")

        drift = s.get("drift_status", "N/A")
        drift_color = ("#FF6666" if "CRITICAL" in drift else
                       "#FFAA44" if "WARNING" in drift or drift == "WATCH" else
                       "#44CC88" if drift == "STABLE" else "#AAAAAA")
        self._lbl_drift.setText(f"Drift: {drift}")
        self._lbl_drift.setStyleSheet(f"color:{drift_color};font-weight:bold")

        deg = s.get("degradation_status", "N/A")
        deg_color = ("#FF6666" if deg in ("SEVERE", "DEGRADED") else
                     "#FFAA44" if deg == "WATCH" else
                     "#44CC88" if deg == "STABLE" else "#AAAAAA")
        self._lbl_degradation.setText(f"Degradation: {deg}")
        self._lbl_degradation.setStyleSheet(f"color:{deg_color};font-weight:bold")

    # ------------------------------------------------------------------
    # Status line
    # ------------------------------------------------------------------

    def _set_status(self, msg: str):
        if not _PYSIDE6_OK:
            return
        logger.info("ModelMonitoringPanel: %s", msg)
        self._status_lbl.setText(msg)

    # ------------------------------------------------------------------
    # Close event — stop all workers
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        if not _PYSIDE6_OK:
            return
        for w in self._workers:
            try:
                if w.isRunning():
                    w.quit()
                    w.wait(2000)
            except Exception:
                pass
        super().closeEvent(event)
