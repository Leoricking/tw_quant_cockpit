"""
gui/provider_stable_rollup_panel.py — Provider Stable Rollup Panel v1.4.9.

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
[!] No silent fallback. No mock fallback. No auto repair. No dangerous actions.

Navigation:
  tab_id       = provider_stable_rollup
  display_name = Provider Stable Rollup
  group        = data
  priority     = P1
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_PANEL_VERSION = "1.4.9"
_SAFETY_FLAGS = {
    "provider_stable_certification":          True,
    "all_six_providers_stable":               True,
    "no_silent_fallback":                     True,
    "no_mock_fallback":                       True,
    "no_auto_repair":                         True,
    "no_real_orders":                         True,
    "production_trading_blocked":             True,
    "finmind_cannot_override_primary":        True,
    "ptt_no_standalone_formal_conclusion":    True,
}


def _is_qt_available() -> bool:
    try:
        from PySide6.QtWidgets import QWidget  # noqa: F401
        return True
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# Headless-safe data model (no Qt dependency)
# ---------------------------------------------------------------------------

class ProviderStableRollupModel:
    """Pure-Python model; safe to create without QApplication."""

    VERSION = _PANEL_VERSION
    SAFETY_FLAGS = _SAFETY_FLAGS

    def get_stable_manifest(self):
        from data.stable.capability_manifest_v149 import StableCapabilityManifest
        return StableCapabilityManifest().validate()

    def get_provider_registry(self):
        from data.stable.provider_registry_v149 import StableProviderRegistry
        return StableProviderRegistry().validate()

    def get_compatibility_contracts(self):
        from data.stable.compatibility_contract_v149 import CompatibilityContractRegistry
        return CompatibilityContractRegistry().validate()

    def get_schema_registry(self):
        from data.stable.schema_version_registry_v149 import SchemaVersionRegistry
        return SchemaVersionRegistry().validate()

    def get_policy_registry(self):
        from data.stable.policy_version_registry_v149 import PolicyVersionRegistry
        return PolicyVersionRegistry().validate()

    def get_baseline_snapshot(self):
        from data.stable.baseline_snapshot_v149 import StableBaselineSnapshot
        return StableBaselineSnapshot().get_summary()

    def get_provider_stable_profiles(self):
        from data.stable.provider_stable_profiles_v149 import ProviderStableProfileRegistry
        return ProviderStableProfileRegistry().get_summary()

    def get_release_gate(self):
        from release.provider_stable_release_gate_v149 import ProviderStableReleaseGate
        return ProviderStableReleaseGate().run()

    def get_health(self):
        from release.provider_stable_health_v149 import ProviderStableRollupHealthCheck
        return ProviderStableRollupHealthCheck().run()


# ---------------------------------------------------------------------------
# Qt Panel (only constructed when QApplication exists)
# ---------------------------------------------------------------------------

if _is_qt_available():
    from gui.common.safety_banner import make_safety_banner
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtWidgets import (
        QGroupBox, QHBoxLayout, QLabel, QPushButton,
        QScrollArea, QSizePolicy, QVBoxLayout, QWidget,
    )

    class _ProviderStableRollupWorker(QThread):
        finished = Signal(object)
        error    = Signal(str)

        def __init__(self, task: str, parent=None):
            super().__init__(parent)
            self._task = task

        def run(self):
            try:
                model = ProviderStableRollupModel()
                if self._task == "manifest":
                    result = model.get_stable_manifest()
                elif self._task == "registry":
                    result = model.get_provider_registry()
                elif self._task == "profiles":
                    result = model.get_provider_stable_profiles()
                elif self._task == "gate":
                    result = model.get_release_gate()
                elif self._task == "health":
                    result = model.get_health()
                else:
                    result = {"error": f"Unknown task: {self._task}"}
                self.finished.emit(result)
            except Exception as exc:
                self.error.emit(str(exc))

    class ProviderStableRollupPanel(QWidget):
        """
        Provider Stable Rollup Panel v1.4.9.
        [!] Research Only. No Real Orders. Production Trading: BLOCKED.
        """

        def __init__(self, parent=None):
            super().__init__(parent)
            self._worker = None
            self._build_ui()

        def _build_ui(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(8, 8, 8, 8)
            root.setSpacing(6)

            # Safety banner
            banner = make_safety_banner(
                "Provider Stable Rollup v1.4.9", _SAFETY_FLAGS
            )
            root.addWidget(banner)

            # Action buttons
            btn_row = QHBoxLayout()
            for label, task in [
                ("Stable Manifest",  "manifest"),
                ("Provider Registry", "registry"),
                ("Stable Profiles",  "profiles"),
                ("Release Gate",     "gate"),
                ("Health Check",     "health"),
            ]:
                btn = QPushButton(label)
                btn.setMaximumHeight(28)
                btn.clicked.connect(lambda _=False, t=task: self._run_task(t))
                btn_row.addWidget(btn)
            root.addLayout(btn_row)

            # Result area
            self._result_label = QLabel("Select an action above.")
            self._result_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self._result_label.setWordWrap(True)
            self._result_label.setStyleSheet("font-size: 11px; font-family: monospace;")

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(self._result_label)
            scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            root.addWidget(scroll)

        def _run_task(self, task: str):
            if self._worker is not None and self._worker.isRunning():
                return
            self._result_label.setText(f"Running {task}…")
            self._worker = _ProviderStableRollupWorker(task, parent=self)
            self._worker.finished.connect(self._on_finished)
            self._worker.error.connect(self._on_error)
            self._worker.start()

        def _on_finished(self, result):
            if isinstance(result, dict):
                lines = []
                for k, v in result.items():
                    if k not in ("items", "checked_at"):
                        lines.append(f"{k}: {v}")
                for item in result.get("items", []):
                    lines.append(f"  [{item[1]}] {item[0]}: {item[2] if len(item) > 2 else ''}")
                self._result_label.setText("\n".join(lines))
            elif isinstance(result, list):
                lines = []
                for g in result:
                    lines.append(f"[{g.get('status','?')}] {g.get('gate_name','?')}: "
                                 f"{g.get('evidence','')}")
                self._result_label.setText("\n".join(lines))
            else:
                self._result_label.setText(str(result))
            self._worker = None

        def _on_error(self, msg: str):
            self._result_label.setText(f"Error: {msg}")
            self._worker = None

else:
    class ProviderStableRollupPanel:  # type: ignore[no-redef]
        """Stub panel when PySide6 is not available."""

        def __init__(self, parent=None):
            raise ImportError("PySide6 not installed")
