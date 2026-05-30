"""
gui/portfolio_widgets.py - Reusable portfolio GUI widgets (v0.3.13).

Components:
  - MetricCard          : KPI display card (label + value + optional unit)
  - StatusBadge         : Confidence/status colored badge
  - RiskBadge           : Risk warning label
  - DataFrameTableModel : Qt table model backed by pandas DataFrame
  - PortfolioTableView  : Sortable QTableView with proxy model
  - EmptyStateWidget    : Placeholder when no data is available

Design rules:
  - PySide6 availability guarded — safe to import even without PySide6.
  - No emojis. Text-only warnings.
  - Missing values displayed as "—".
  - Numbers formatted as percentage / NTD / ratio.
"""

from __future__ import annotations

import logging
from typing import Any, List, Optional

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
        QTableView, QHeaderView, QSizePolicy, QAbstractItemView,
        QApplication,
    )
    from PySide6.QtCore import (
        Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel,
    )
    from PySide6.QtGui import QColor, QFont, QBrush
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.warning("PySide6 not available — portfolio_widgets will be stubs.")

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _fmt_pct(val, decimals=2, suffix="%") -> str:
    """Format a float as percentage string. val=0.15 → '15.00%'."""
    if val is None:
        return "—"
    try:
        v = float(val)
        return f"{v * 100:.{decimals}f}{suffix}"
    except (TypeError, ValueError):
        return "—"


def _fmt_ratio(val, decimals=3) -> str:
    if val is None:
        return "—"
    try:
        return f"{float(val):.{decimals}f}"
    except (TypeError, ValueError):
        return "—"


def _fmt_ntd(val) -> str:
    if val is None:
        return "—"
    try:
        return f"{float(val):,.0f}"
    except (TypeError, ValueError):
        return "—"


def _fmt_any(val) -> str:
    """Format any value for table display. Returns '—' for None/NaN."""
    if val is None:
        return "—"
    try:
        import math
        if isinstance(val, float) and math.isnan(val):
            return "—"
    except Exception:
        pass
    if isinstance(val, float):
        # If looks like a ratio (not percentage raw)
        return f"{val:.4g}"
    return str(val)


# ---------------------------------------------------------------------------
# MetricCard
# ---------------------------------------------------------------------------

class MetricCard(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    A compact KPI card: title on top, large value in middle, optional sub-text.

    Usage:
        card = MetricCard("Sharpe Ratio", "1.685", sub="target > 1.5")
    """

    def __init__(self, title: str = "", value: str = "—", sub: str = "", color: str = "#EEEEEE"):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__()
        self._build(title, value, sub, color)

    def _build(self, title, value, sub, color):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        self._title_lbl = QLabel(title)
        self._title_lbl.setStyleSheet("color:#AAAAAA; font-size:11px;")
        layout.addWidget(self._title_lbl, alignment=Qt.AlignCenter)

        self._value_lbl = QLabel(value)
        self._value_lbl.setStyleSheet(f"color:{color}; font-size:20px; font-weight:bold;")
        layout.addWidget(self._value_lbl, alignment=Qt.AlignCenter)

        if sub:
            self._sub_lbl = QLabel(sub)
            self._sub_lbl.setStyleSheet("color:#777777; font-size:10px;")
            layout.addWidget(self._sub_lbl, alignment=Qt.AlignCenter)
        else:
            self._sub_lbl = None

        self.setStyleSheet("""
            MetricCard {
                background: #1E1E30;
                border: 1px solid #333355;
                border-radius: 6px;
            }
        """)
        self.setMinimumWidth(130)
        self.setMinimumHeight(80)

    def set_value(self, value: str, color: str = None):
        if not _PYSIDE6_AVAILABLE:
            return
        self._value_lbl.setText(value)
        if color:
            self._value_lbl.setStyleSheet(f"color:{color}; font-size:20px; font-weight:bold;")

    def set_sub(self, sub: str):
        if not _PYSIDE6_AVAILABLE:
            return
        if self._sub_lbl:
            self._sub_lbl.setText(sub)


# ---------------------------------------------------------------------------
# StatusBadge
# ---------------------------------------------------------------------------

_CONFIDENCE_COLORS = {
    "RELIABLE":      "#33CC66",
    "OBSERVATIONAL": "#FF8800",
    "INSUFFICIENT":  "#FF4444",
    "UNKNOWN":       "#888888",
}

_STATUS_COLORS = {
    "OK":       "#33CC66",
    "WARNING":  "#FF8800",
    "ERROR":    "#FF4444",
    "DISABLED": "#888888",
    "ENABLED":  "#FF4444",   # red = enabled real order (dangerous)
}


class StatusBadge(QLabel if _PYSIDE6_AVAILABLE else object):
    """
    A colored label badge for confidence levels and status indicators.

    Usage:
        badge = StatusBadge("OBSERVATIONAL")
        badge = StatusBadge("DISABLED", kind="status")
    """

    def __init__(self, text: str = "", kind: str = "confidence"):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(text)
        self._kind = kind
        self._apply_style(text)

    def _apply_style(self, text: str):
        upper = text.upper()
        if self._kind == "confidence":
            color = _CONFIDENCE_COLORS.get(upper, "#888888")
        else:
            color = _STATUS_COLORS.get(upper, "#888888")
        self.setStyleSheet(
            f"color:{color}; font-weight:bold; font-size:12px; "
            f"background:#1E1E30; border:1px solid {color}; "
            f"border-radius:3px; padding:2px 6px;"
        )
        self.setText(text)

    def set_status(self, text: str):
        if not _PYSIDE6_AVAILABLE:
            return
        self._apply_style(text)


# ---------------------------------------------------------------------------
# RiskBadge
# ---------------------------------------------------------------------------

class RiskBadge(QLabel if _PYSIDE6_AVAILABLE else object):
    """
    A text-only warning label for risk messages.
    No emojis — plain text, red/orange color.
    """

    def __init__(self, text: str = "", level: str = "warning"):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(text)
        color = "#FF8800" if level == "warning" else "#FF4444"
        self.setStyleSheet(
            f"color:{color}; font-size:11px; "
            f"background:#201008; border-left:3px solid {color}; "
            f"padding:3px 6px;"
        )
        self.setWordWrap(True)


# ---------------------------------------------------------------------------
# DataFrameTableModel
# ---------------------------------------------------------------------------

class DataFrameTableModel(QAbstractTableModel if _PYSIDE6_AVAILABLE else object):
    """
    Qt table model backed by a pandas DataFrame.

    Supports:
    - Column header display names (headers dict)
    - Custom cell formatters (formatters dict: col_name -> callable)
    - Sort proxy via PortfolioTableView
    """

    def __init__(self, df=None, headers: dict = None, formatters: dict = None):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__()
        import pandas as pd
        self._df = df if df is not None else pd.DataFrame()
        self._headers = headers or {}       # col_name -> display_name
        self._formatters = formatters or {} # col_name -> callable(val) -> str

    def rowCount(self, parent=QModelIndex()):
        if not _PYSIDE6_AVAILABLE:
            return 0
        return len(self._df)

    def columnCount(self, parent=QModelIndex()):
        if not _PYSIDE6_AVAILABLE:
            return 0
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not _PYSIDE6_AVAILABLE or not index.isValid():
            return None
        col = self._df.columns[index.column()]
        val = self._df.iloc[index.row(), index.column()]

        if role == Qt.DisplayRole:
            fmt = self._formatters.get(col)
            if fmt:
                return fmt(val)
            return _fmt_any(val)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role == Qt.ForegroundRole:
            return self._color_for(col, val)

        return None

    def _color_for(self, col: str, val) -> Optional[QBrush]:
        """Apply coloring rules for known column types."""
        try:
            col_l = col.lower()
            if "drawdown" in col_l or "loss" in col_l:
                if isinstance(val, float) and val < 0:
                    if val < -0.2:
                        return QBrush(QColor("#FF4444"))
                    return QBrush(QColor("#FF8800"))
            if "sharpe" in col_l:
                if isinstance(val, float):
                    if val >= 1.5:
                        return QBrush(QColor("#33CC66"))
                    if val >= 1.0:
                        return QBrush(QColor("#FF8800"))
                    return QBrush(QColor("#FF4444"))
            if "return" in col_l:
                if isinstance(val, float):
                    return QBrush(QColor("#33CC66") if val > 0 else QColor("#FF4444"))
            if "confidence" in col_l:
                c = _CONFIDENCE_COLORS.get(str(val).upper(), "#888888")
                return QBrush(QColor(c))
            if "profit_factor" in col_l or "profit factor" in col_l:
                if isinstance(val, float):
                    if val >= 1.5:
                        return QBrush(QColor("#33CC66"))
                    if val >= 1.0:
                        return QBrush(QColor("#FF8800"))
                    return QBrush(QColor("#FF4444"))
        except Exception:
            pass
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if not _PYSIDE6_AVAILABLE:
            return None
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            col = self._df.columns[section]
            return self._headers.get(col, col)
        return str(section + 1)

    def set_dataframe(self, df):
        if not _PYSIDE6_AVAILABLE:
            return
        self.beginResetModel()
        self._df = df if df is not None else __import__('pandas').DataFrame()
        self.endResetModel()


# ---------------------------------------------------------------------------
# PortfolioTableView
# ---------------------------------------------------------------------------

class PortfolioTableView(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Sortable table view backed by DataFrameTableModel + QSortFilterProxyModel.

    Usage:
        view = PortfolioTableView()
        view.load_dataframe(df, headers={...}, formatters={...})
    """

    def __init__(self, title: str = ""):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        if title:
            lbl = QLabel(title)
            lbl.setStyleSheet("font-weight:bold; color:#AAAAFF; font-size:12px; padding:2px 0;")
            layout.addWidget(lbl)

        self._model = DataFrameTableModel()
        self._proxy = QSortFilterProxyModel()
        self._proxy.setSourceModel(self._model)
        self._proxy.setSortRole(Qt.DisplayRole)

        self._view = QTableView()
        self._view.setModel(self._proxy)
        self._view.setSortingEnabled(True)
        self._view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._view.setAlternatingRowColors(True)
        self._view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._view.horizontalHeader().setStretchLastSection(True)
        self._view.setStyleSheet("""
            QTableView {
                background: #12121E;
                color: #EEEEEE;
                gridline-color: #333355;
                border: 1px solid #333355;
            }
            QTableView::item:alternate { background: #1A1A2E; }
            QHeaderView::section {
                background: #252540;
                color: #AAAAFF;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #333355;
            }
        """)
        layout.addWidget(self._view)

    def load_dataframe(self, df, headers: dict = None, formatters: dict = None):
        if not _PYSIDE6_AVAILABLE:
            return
        self._model = DataFrameTableModel(df=df, headers=headers or {}, formatters=formatters or {})
        self._proxy.setSourceModel(self._model)
        self._view.setModel(self._proxy)

    def row_count(self) -> int:
        if not _PYSIDE6_AVAILABLE:
            return 0
        return self._model.rowCount()


# ---------------------------------------------------------------------------
# EmptyStateWidget
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# RecommendationBadge (v0.3.14)
# ---------------------------------------------------------------------------

_REC_COLORS = {
    "BOOST":               "#33CC66",
    "KEEP":                "#AAAAFF",
    "REDUCE":              "#FF8800",
    "DISABLE":             "#FF4444",
    "INSUFFICIENT_SAMPLE": "#888888",
}


class RecommendationBadge(QLabel if _PYSIDE6_AVAILABLE else object):
    """
    Colored badge for BOOST / KEEP / REDUCE / DISABLE / INSUFFICIENT_SAMPLE.
    """

    def __init__(self, text: str = ""):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__(text)
        self._apply_style(text)

    def _apply_style(self, text: str):
        upper = text.strip().upper()
        color = _REC_COLORS.get(upper, "#888888")
        self.setStyleSheet(
            f"color:{color}; font-weight:bold; font-size:11px; "
            f"background:#1A1A2A; border:1px solid {color}; "
            f"border-radius:3px; padding:1px 5px;"
        )
        self.setText(text)

    def set_recommendation(self, text: str):
        if not _PYSIDE6_AVAILABLE:
            return
        self._apply_style(text)


class EmptyStateWidget(QWidget if _PYSIDE6_AVAILABLE else object):
    """
    Placeholder widget shown when no portfolio simulation data exists.
    Displays an informational message and instructions.
    """

    def __init__(
        self,
        message: str = "No portfolio simulation results found.",
        hint: str = "Click Refresh Portfolio Simulation to run balanced scenario.",
    ):
        if not _PYSIDE6_AVAILABLE:
            return
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        lbl_msg = QLabel(message)
        lbl_msg.setStyleSheet("color:#888888; font-size:14px; font-weight:bold;")
        lbl_msg.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_msg)

        lbl_hint = QLabel(hint)
        lbl_hint.setStyleSheet("color:#666666; font-size:12px;")
        lbl_hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_hint)

        lbl_safe = QLabel("Simulation Only  |  Real Order Execution: DISABLED  |  No real orders will be sent")
        lbl_safe.setStyleSheet("color:#FF8800; font-size:11px; margin-top:12px;")
        lbl_safe.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_safe)
