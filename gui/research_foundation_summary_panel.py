"""
gui/research_foundation_summary_panel.py — Research Foundation Summary Panel for v1.3.9.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] No trading controls. No Buy/Sell. No Broker connect.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Navigation metadata
# ---------------------------------------------------------------------------
TAB_ID       = "research_foundation"
DISPLAY_NAME = "Research Foundation"
GROUP        = "system"
PRIORITY     = "P1"

# Safety flags — never change
NO_REAL_ORDERS          = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True


def _try_import_qt():
    try:
        from PyQt5.QtWidgets import (
            QWidget, QVBoxLayout, QHBoxLayout, QLabel,
            QGroupBox, QScrollArea, QFrame, QSizePolicy,
        )
        from PyQt5.QtCore import Qt, QThread, pyqtSignal
        from PyQt5.QtGui import QFont
        return True, None
    except ImportError as e:
        return False, str(e)


_QT_AVAILABLE, _QT_ERROR = _try_import_qt()


def _get_health_data() -> dict:
    try:
        from release.research_foundation_health_v139 import ResearchFoundationStableHealthCheck
        return ResearchFoundationStableHealthCheck().get_health_summary()
    except Exception as exc:
        return {"error": str(exc), "all_pass": False, "passed": 0, "failed": 0, "total_checks": 0}


def _get_gate_data() -> dict:
    try:
        from release.research_foundation_release_gate_v139 import ResearchFoundationReleaseGate
        return ResearchFoundationReleaseGate().get_gate_summary()
    except Exception as exc:
        return {"error": str(exc), "overall": "ERROR", "total_gates": 0}


def _get_capabilities_data() -> dict:
    try:
        from release.capability_registry import build_capability_summary
        return build_capability_summary()
    except Exception as exc:
        return {"error": str(exc)}


def get_panel_data() -> dict:
    """
    Return all panel data without requiring Qt.
    Safe to call in any environment.
    """
    try:
        from release.version_info import VERSION, RELEASE_NAME, REPLAY_STABLE_BASELINE
    except Exception:
        VERSION = "unknown"
        RELEASE_NAME = "unknown"
        REPLAY_STABLE_BASELINE = "unknown"

    return {
        "version": VERSION,
        "release": RELEASE_NAME,
        "replay_baseline": REPLAY_STABLE_BASELINE,
        "health": _get_health_data(),
        "gate": _get_gate_data(),
        "capabilities": _get_capabilities_data(),
        "no_real_orders": NO_REAL_ORDERS,
        "broker_execution_enabled": BROKER_EXECUTION_ENABLED,
        "production_trading_blocked": PRODUCTION_TRADING_BLOCKED,
    }


if _QT_AVAILABLE:
    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QGroupBox, QScrollArea, QFrame, QSizePolicy,
    )
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    from PyQt5.QtGui import QFont

    class _DataWorker(QThread):
        data_ready = pyqtSignal(dict)
        error_occurred = pyqtSignal(str)

        def run(self):
            try:
                data = get_panel_data()
                self.data_ready.emit(data)
            except Exception as exc:
                self.error_occurred.emit(str(exc))

    class ResearchFoundationSummaryPanel(QWidget):
        """
        Research Foundation Summary Panel.
        [!] No trading controls. [!] Research Only.
        """
        TAB_ID       = TAB_ID
        DISPLAY_NAME = DISPLAY_NAME
        GROUP        = GROUP
        PRIORITY     = PRIORITY

        def __init__(self, parent=None):
            super().__init__(parent)
            self._worker = None
            self._setup_ui()
            self.refresh()

        def _setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(12, 12, 12, 12)

            # Header
            header = QLabel(f"Research Foundation Stable Rollup — v1.3.9")
            font = QFont()
            font.setBold(True)
            font.setPointSize(12)
            header.setFont(font)
            layout.addWidget(header)

            safety_label = QLabel(
                "[!] Research Only  |  No Real Orders  |  Production Trading BLOCKED"
            )
            safety_label.setStyleSheet("color: #c0392b; font-size: 10px;")
            layout.addWidget(safety_label)

            # Status area
            self._status_label = QLabel("Loading...")
            self._status_label.setWordWrap(True)
            layout.addWidget(self._status_label)

            # Scroll area for details
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            inner = QWidget()
            self._detail_layout = QVBoxLayout(inner)
            self._detail_layout.setAlignment(Qt.AlignTop)
            scroll.setWidget(inner)
            layout.addWidget(scroll)

        def refresh(self):
            if self._worker and self._worker.isRunning():
                return
            self._status_label.setText("Refreshing...")
            self._worker = _DataWorker()
            self._worker.data_ready.connect(self._on_data_ready)
            self._worker.error_occurred.connect(self._on_error)
            self._worker.start()

        def _on_data_ready(self, data: dict):
            self._status_label.setText(
                f"Version: {data.get('version', 'N/A')}  |  "
                f"Release: {data.get('release', 'N/A')}  |  "
                f"Replay Baseline: {data.get('replay_baseline', 'N/A')}"
            )
            # Clear old widgets
            while self._detail_layout.count():
                item = self._detail_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            health = data.get("health", {})
            health_box = QGroupBox("Health Summary")
            health_layout = QVBoxLayout(health_box)
            health_status = "PASS" if health.get("all_pass") else "FAIL"
            health_layout.addWidget(QLabel(
                f"Status: {health_status}  |  "
                f"Passed: {health.get('passed', 0)}/{health.get('total_checks', 0)}"
            ))
            self._detail_layout.addWidget(health_box)

            caps = data.get("capabilities", {})
            caps_box = QGroupBox("Capabilities")
            caps_layout = QVBoxLayout(caps_box)
            caps_layout.addWidget(QLabel(
                f"Stable: {caps.get('stable_count', 0)}  |  "
                f"Available: {caps.get('available_count', 0)}  |  "
                f"Planned: {caps.get('planned_count', 0)}"
            ))
            self._detail_layout.addWidget(caps_box)

            gate = data.get("gate", {})
            gate_box = QGroupBox("Release Gate")
            gate_layout = QVBoxLayout(gate_box)
            gate_layout.addWidget(QLabel(
                f"Overall: {gate.get('overall', 'N/A')}  |  "
                f"Blocking Failures: {gate.get('blocking_failures', 0)}"
            ))
            self._detail_layout.addWidget(gate_box)

            safety_box = QGroupBox("Safety")
            safety_layout = QVBoxLayout(safety_box)
            safety_layout.addWidget(QLabel(
                f"No Real Orders: {data.get('no_real_orders', True)}  |  "
                f"Broker Enabled: {data.get('broker_execution_enabled', False)}  |  "
                f"Production BLOCKED: {data.get('production_trading_blocked', True)}"
            ))
            self._detail_layout.addWidget(safety_box)

        def _on_error(self, msg: str):
            self._status_label.setText(f"Error: {msg}")

        def closeEvent(self, event):
            if self._worker and self._worker.isRunning():
                self._worker.quit()
                self._worker.wait(2000)
            super().closeEvent(event)

else:
    # Headless fallback — importable without Qt
    class ResearchFoundationSummaryPanel:  # type: ignore[no-redef]
        """Headless stub when PyQt5 is unavailable."""
        TAB_ID       = TAB_ID
        DISPLAY_NAME = DISPLAY_NAME
        GROUP        = GROUP
        PRIORITY     = PRIORITY
        NO_REAL_ORDERS = True
        BROKER_EXECUTION_ENABLED = False
        PRODUCTION_TRADING_BLOCKED = True

        def __init__(self, *args, **kwargs):
            self._qt_error = _QT_ERROR

        def get_panel_data(self):
            return get_panel_data()
