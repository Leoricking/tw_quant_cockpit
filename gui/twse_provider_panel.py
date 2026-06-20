"""
gui/twse_provider_panel.py — TWSE Provider Panel for v1.4.0.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official Public Data. Historical Data Is Not Real-Time.
[!] No Buy/Sell/Order controls. No Broker Connect.
"""
TAB_ID = "twse_provider"
DISPLAY_NAME = "TWSE Provider"
GROUP = "data"
PRIORITY = "P1"

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
TWSE_REALTIME_AVAILABLE = False


def _try_import_qt():
    try:
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QScrollArea, QSizePolicy
        from PyQt5.QtCore import QThread, pyqtSignal
        from PyQt5.QtGui import QFont
        return True, None
    except ImportError as e:
        return False, str(e)


_QT_AVAILABLE, _QT_ERROR = _try_import_qt()


def get_panel_data() -> dict:
    try:
        from data.providers.twse.health_v140 import TWSEProviderHealthCheck
        health = TWSEProviderHealthCheck().get_health_summary()
    except Exception as exc:
        health = {"error": str(exc)}
    try:
        from data.providers.twse.endpoints_v140 import TWSEEndpointRegistry
        reg = TWSEEndpointRegistry()
        endpoints = [{"id": ep.endpoint_id, "name": ep.official_name, "enabled": ep.enabled} for ep in reg.list_all()]
    except Exception as exc:
        endpoints = [{"error": str(exc)}]
    return {
        "provider": "twse_official",
        "official_source": True,
        "no_real_orders": NO_REAL_ORDERS,
        "broker_execution_enabled": BROKER_EXECUTION_ENABLED,
        "production_trading_blocked": PRODUCTION_TRADING_BLOCKED,
        "realtime_available": TWSE_REALTIME_AVAILABLE,
        "health": health,
        "endpoints": endpoints,
    }


if _QT_AVAILABLE:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QScrollArea, QSizePolicy
    from PyQt5.QtCore import QThread, pyqtSignal, Qt
    from PyQt5.QtGui import QFont

    class _DataWorker(QThread):
        data_ready = pyqtSignal(dict)
        error_occurred = pyqtSignal(str)

        def run(self):
            try:
                self.data_ready.emit(get_panel_data())
            except Exception as exc:
                self.error_occurred.emit(str(exc))

    class TWSEProviderPanel(QWidget):
        TAB_ID = TAB_ID
        DISPLAY_NAME = DISPLAY_NAME
        GROUP = GROUP
        PRIORITY = PRIORITY

        def __init__(self, parent=None):
            from PyQt5.QtWidgets import QApplication
            if QApplication.instance() is None:
                # No QApplication — cannot create widgets; skip full init
                self._worker = None
                self._status_label = None
                self._detail_layout = None
                return
            super().__init__(parent)
            self._worker = None
            self._setup_ui()
            self.refresh()

        def _setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setContentsMargins(12, 12, 12, 12)
            header = QLabel("TWSE Official Public Data Provider — v1.4.0")
            font = QFont()
            font.setBold(True)
            font.setPointSize(12)
            header.setFont(font)
            layout.addWidget(header)
            safety = QLabel("[!] Official Public Data  |  Research Only  |  No Real Orders  |  Not Real-Time  |  Broker Disabled")
            safety.setStyleSheet("color: #c0392b; font-size: 10px;")
            safety.setWordWrap(True)
            layout.addWidget(safety)
            self._status_label = QLabel("Loading...")
            self._status_label.setWordWrap(True)
            layout.addWidget(self._status_label)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            inner = QWidget()
            self._detail_layout = QVBoxLayout(inner)
            self._detail_layout.setAlignment(Qt.AlignTop)
            scroll.setWidget(inner)
            layout.addWidget(scroll)

        def refresh(self):
            from PyQt5.QtWidgets import QApplication
            if QApplication.instance() is None:
                # No QApplication — skip worker start (test environment)
                self._status_label.setText("No QApplication (test mode)")
                return
            if self._worker and self._worker.isRunning():
                return
            self._status_label.setText("Refreshing...")
            self._worker = _DataWorker()
            self._worker.data_ready.connect(self._on_data_ready)
            self._worker.error_occurred.connect(self._on_error)
            self._worker.start()

        def _on_data_ready(self, data: dict):
            self._status_label.setText(f"Provider: {data.get('provider', 'N/A')}  |  Official Source: {data.get('official_source', True)}")
            while self._detail_layout.count():
                item = self._detail_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            health = data.get("health", {})
            hbox = QGroupBox("Provider Health")
            hlayout = QVBoxLayout(hbox)
            hlayout.addWidget(QLabel(f"Status: {'PASS' if health.get('all_pass') else 'FAIL'}  |  Passed: {health.get('passed', 0)}/{health.get('total_checks', 0)}"))
            self._detail_layout.addWidget(hbox)
            safety_box = QGroupBox("Safety")
            slayout = QVBoxLayout(safety_box)
            slayout.addWidget(QLabel(f"No Real Orders: {data.get('no_real_orders', True)}  |  Broker: {data.get('broker_execution_enabled', False)}  |  Real-Time: {data.get('realtime_available', False)}"))
            self._detail_layout.addWidget(safety_box)

        def _on_error(self, msg: str):
            self._status_label.setText(f"Error: {msg}")

        def closeEvent(self, event):
            if self._worker and self._worker.isRunning():
                self._worker.quit()
                self._worker.wait(2000)
            super().closeEvent(event)

else:
    class TWSEProviderPanel:  # type: ignore
        TAB_ID = TAB_ID
        DISPLAY_NAME = DISPLAY_NAME
        GROUP = GROUP
        PRIORITY = PRIORITY
        NO_REAL_ORDERS = True
        BROKER_EXECUTION_ENABLED = False

        def __init__(self, *args, **kwargs):
            self._qt_error = _QT_ERROR

        def get_panel_data(self):
            return get_panel_data()
