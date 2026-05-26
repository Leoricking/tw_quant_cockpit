"""
gui/data_status_panel.py - Data completeness status panel for TW Quant Cockpit.

Shows DataQualityChecker results for the currently selected stock.
"""

import logging

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False


def _lbl(text, bold=False, color=None, size=None):
    l = QLabel(text)
    style = []
    if bold:
        style.append("font-weight:bold")
    if color:
        style.append(f"color:{color}")
    if size:
        style.append(f"font-size:{size}px")
    if style:
        l.setStyleSheet(";".join(style))
    return l


def _ok_color(ok: bool) -> str:
    return "#44CC88" if ok else "#FF8888"


class DataStatusPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Shows DataQualityChecker.check_stock() results for the selected stock.
    """

    def __init__(self):
        self._rows = {}
        self._missing_label = None
        self._rec_label = None
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(4, 4, 4, 4)

        header = _lbl("資料完整度", bold=True, size=12, color="#AAAAFF")
        outer.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background:#0E1520; border:none;")

        content = QWidget()
        self._layout = QVBoxLayout(content)
        self._layout.setSpacing(3)
        self._layout.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(content)
        outer.addWidget(scroll)

        # Build all label pairs
        self._rows = {}
        self._add_section("資料列數")
        for key in ('Profile', 'Daily K', 'Institutional', 'Margin',
                    'Monthly Revenue', 'Holder', 'Trust Cost'):
            self._rows[key] = self._add_row(key, "—")

        self._add_section("正式判斷允許")
        for key in ('當沖', '短線', '中線', '長線'):
            self._rows[f'formal_{key}'] = self._add_row(key, "—")

        self._add_section("缺失資料")
        self._missing_label = _lbl("—", color="#FF8888")
        self._missing_label.setWordWrap(True)
        self._layout.addWidget(self._missing_label)

        self._add_section("建議")
        self._rec_label = _lbl("—", color="#AAAAAA")
        self._rec_label.setWordWrap(True)
        self._layout.addWidget(self._rec_label)

        self._layout.addStretch()

    def _add_section(self, title: str):
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#333355;")
        self._layout.addWidget(sep)
        self._layout.addWidget(_lbl(title, bold=True, color="#AAAAFF"))

    def _add_row(self, key: str, default: str) -> QLabel:
        row = QHBoxLayout()
        row.addWidget(_lbl(f"{key}：", bold=False, color="#888888"))
        val_lbl = _lbl(default)
        row.addWidget(val_lbl)
        row.addStretch()
        self._layout.addLayout(row)
        return val_lbl

    def update(self, result: dict):
        """Update panel from DataQualityChecker.check_stock() result dict."""
        if not _PYSIDE6_AVAILABLE:
            return
        if not result:
            self.clear()
            return

        try:
            r = result
            profile_ok = r.get('profile_ok', False)
            self._rows['Profile'].setText("OK" if profile_ok else "缺少")
            self._rows['Profile'].setStyleSheet(f"color:{_ok_color(profile_ok)}")

            def _row_text(key, count, threshold):
                ok = count >= threshold
                txt = f"{count} rows"
                color = _ok_color(ok)
                self._rows[key].setText(txt)
                self._rows[key].setStyleSheet(f"color:{color}")

            _row_text('Daily K',          r.get('daily_rows', 0),              20)
            _row_text('Institutional',     r.get('institutional_rows', 0),       5)
            _row_text('Margin',            r.get('margin_rows', 0),              5)
            _row_text('Monthly Revenue',   r.get('monthly_revenue_rows', 0),     6)
            _row_text('Holder',            r.get('holder_rows', 0),              2)
            _row_text('Trust Cost',        r.get('trust_cost_rows', 0),          3)

            def _bool_row(key, val):
                txt = "✓ 是" if val else "✗ 否"
                self._rows[f'formal_{key}'].setText(txt)
                self._rows[f'formal_{key}'].setStyleSheet(
                    f"color:{_ok_color(val)}"
                )

            _bool_row('當沖', r.get('daytrade_allowed', False))
            _bool_row('短線', r.get('short_allowed', False))
            _bool_row('中線', r.get('mid_allowed', False))
            _bool_row('長線', r.get('long_allowed', False))

            missing = [m for m in r.get('missing', [])
                       if m not in ('intraday', 'bidask')]
            if missing:
                self._missing_label.setText('\n'.join(f"• {m}" for m in missing))
            else:
                self._missing_label.setText("無")

            recs = r.get('recommendations', [])
            if recs:
                self._rec_label.setText('\n'.join(f"• {rc}" for rc in recs))
            else:
                self._rec_label.setText("無建議")

        except Exception as exc:
            logger.error("DataStatusPanel.update error: %s", exc)

    def clear(self):
        if not _PYSIDE6_AVAILABLE:
            return
        for lbl in self._rows.values():
            if lbl:
                lbl.setText("—")
                lbl.setStyleSheet("color:#888888")
        if self._missing_label:
            self._missing_label.setText("—")
        if self._rec_label:
            self._rec_label.setText("—")
