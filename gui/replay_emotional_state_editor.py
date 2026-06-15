"""
gui/replay_emotional_state_editor.py — ReplayEmotionalStateEditor v1.2.2
[!] Research Only. No Real Orders.
[!] Self-reported emotional state only. NOT a psychological assessment.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)
NO_REAL_ORDERS = True

try:
    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
        QSlider, QTextEdit, QCheckBox, QGroupBox,
    )
    from PyQt5.QtCore import Qt
    HAS_QT = True
except ImportError:
    HAS_QT = False

if HAS_QT:
    class ReplayEmotionalStateEditor(QWidget):
        """
        Emotional state editor widget.
        [!] Self-reported only. NOT a psychological assessment.
        """
        def __init__(self, parent=None):
            super().__init__(parent)
            self._build_ui()

        def _build_ui(self):
            layout = QVBoxLayout(self)

            disclaimer = QLabel("Self-reported emotional state only. Not a psychological assessment.")
            disclaimer.setStyleSheet("color: #aaa; font-size: 10px; font-style: italic;")
            layout.addWidget(disclaimer)

            row = QHBoxLayout()
            row.addWidget(QLabel("Primary Emotion:"))
            self._emotion_combo = QComboBox()
            self._emotion_combo.addItems([
                "NEUTRAL", "CALM", "CONFIDENT", "UNCERTAIN",
                "ANXIOUS", "FEARFUL", "GREEDY", "FRUSTRATED",
                "IMPATIENT", "EXCITED", "FATIGUED", "OTHER",
            ])
            row.addWidget(self._emotion_combo)
            layout.addLayout(row)

            def _make_slider(label: str):
                grp = QHBoxLayout()
                grp.addWidget(QLabel(f"{label} (0-100):"))
                slider = QSlider(Qt.Horizontal)
                slider.setRange(0, 100)
                slider.setValue(50)
                val_label = QLabel("50")
                slider.valueChanged.connect(lambda v: val_label.setText(str(v)))
                grp.addWidget(slider)
                grp.addWidget(val_label)
                return grp, slider

            conf_row, self._confidence_slider = _make_slider("Confidence")
            layout.addLayout(conf_row)
            anx_row, self._anxiety_slider = _make_slider("Anxiety")
            layout.addLayout(anx_row)
            foc_row, self._focus_slider = _make_slider("Focus")
            layout.addLayout(foc_row)

            # Bias flags
            bias_grp = QGroupBox("Self-Reported Cognitive Bias Flags")
            bias_layout = QVBoxLayout(bias_grp)
            from replay.cognitive_bias import CognitiveBiasRegistry
            self._bias_checks: Dict[str, QCheckBox] = {}
            reg = CognitiveBiasRegistry()
            for bias in reg.KNOWN_BIASES[:10]:  # Show top 10
                cb = QCheckBox(bias)
                self._bias_checks[bias] = cb
                bias_layout.addWidget(cb)
            layout.addWidget(bias_grp)

            layout.addWidget(QLabel("Notes:"))
            self._notes = QTextEdit()
            self._notes.setMaximumHeight(60)
            layout.addWidget(self._notes)

        def get_data(self) -> Dict[str, Any]:
            return {
                "primary_emotion": self._emotion_combo.currentText(),
                "confidence_level": self._confidence_slider.value(),
                "anxiety_level": self._anxiety_slider.value(),
                "focus_level": self._focus_slider.value(),
                "cognitive_bias_flags": [
                    bias for bias, cb in self._bias_checks.items() if cb.isChecked()
                ],
                "notes": self._notes.toPlainText(),
                "self_reported": True,
                "simulation_only": True,
            }
else:
    class ReplayEmotionalStateEditor:
        no_real_orders = True
        def __init__(self, *args, **kwargs): pass
