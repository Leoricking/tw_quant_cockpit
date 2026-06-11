"""
Table usability helpers for GUI panels.
Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
from typing import Any, List

_BOOL_TRUE = "True"
_BOOL_FALSE = "False"
_SCORE_FORMAT = "{:.1f}"
_STATUS_ALIGN_LABELS = {"PASS", "WARN", "FAIL", "BLOCKED", "VALIDATED", "REVIEW", "BACKTEST_MORE"}


def format_bool(value: Any, use_checkmark: bool = False) -> str:
    """Format a boolean value for table display."""
    if isinstance(value, bool):
        if use_checkmark:
            return "✓" if value else "—"
        return _BOOL_TRUE if value else _BOOL_FALSE
    return str(value) if value is not None else "—"


def format_score(value: Any) -> str:
    """Format a numeric score for table display."""
    try:
        return _SCORE_FORMAT.format(float(value))
    except (TypeError, ValueError):
        return str(value) if value is not None else "—"


def format_status(value: Any) -> str:
    """Format a status string for table display."""
    if value is None:
        return "—"
    s = str(value).strip().upper()
    if s in _STATUS_ALIGN_LABELS:
        return s
    return str(value).strip()


try:
    from PySide6.QtWidgets import (
        QTableWidget, QHeaderView, QAbstractItemView, QStyledItemDelegate,
        QStyleOptionViewItem, QLabel, QWidget, QVBoxLayout,
    )
    from PySide6.QtCore import Qt, QSize
    from PySide6.QtGui import QPainter, QFontMetrics

    class _EllipsisDelegate(QStyledItemDelegate):
        """Delegate that renders long text with ellipsis and sets tooltip."""
        def paint(self, painter: QPainter, option: QStyleOptionViewItem, index) -> None:
            text = index.data(Qt.DisplayRole) or ""
            fm = QFontMetrics(option.font)
            elided = fm.elidedText(text, Qt.ElideRight, option.rect.width() - 8)
            opt = QStyleOptionViewItem(option)
            opt.text = elided
            super().paint(painter, opt, index)

        def sizeHint(self, option: QStyleOptionViewItem, index) -> QSize:
            return QSize(option.rect.width(), 24)

    def set_table_defaults(table: QTableWidget) -> None:
        """Apply standard table defaults for readability."""
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setShowGrid(True)

    def autosize_table_columns(table: QTableWidget, max_width: int = 360) -> None:
        """Auto-resize columns, capping at max_width."""
        header = table.horizontalHeader()
        for col in range(table.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        table.resizeColumnsToContents()
        for col in range(table.columnCount()):
            if table.columnWidth(col) > max_width:
                table.setColumnWidth(col, max_width)
            header.setSectionResizeMode(col, QHeaderView.Interactive)

    def apply_ellipsis_delegate(table: QTableWidget) -> None:
        """Apply ellipsis delegate to all columns."""
        delegate = _EllipsisDelegate(table)
        for col in range(table.columnCount()):
            table.setItemDelegateForColumn(col, delegate)

    def set_tooltip_from_cell(table: QTableWidget) -> None:
        """Set tooltip from cell data for all items."""
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and item.text():
                    item.setToolTip(item.text())

    def safe_set_rows(table: QTableWidget, rows: List[List[Any]]) -> None:
        """Safely populate table rows, showing friendly empty row if no data."""
        from PySide6.QtWidgets import QTableWidgetItem
        table.setRowCount(0)
        if not rows:
            table.setRowCount(1)
            col_count = table.columnCount() or 1
            item = QTableWidgetItem("— No data yet —")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(0, 0, item)
            return
        table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                text = str(val) if val is not None else "—"
                item_widget = QTableWidgetItem(text)
                item_widget.setToolTip(text)
                table.setItem(r, c, item_widget)

except ImportError:
    # PySide6 not available — stubs only
    def set_table_defaults(table) -> None:
        pass

    def autosize_table_columns(table, max_width: int = 360) -> None:
        pass

    def apply_ellipsis_delegate(table) -> None:
        pass

    def set_tooltip_from_cell(table) -> None:
        pass

    def safe_set_rows(table, rows) -> None:
        pass
