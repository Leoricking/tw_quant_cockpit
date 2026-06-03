"""
gui/navigation/navigation_widgets.py — Navigation widgets for TW Quant Cockpit v0.5.2.

PySide6 widgets with import guard. If PySide6 not available, stub classes are defined.

[!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PySide6 guard
# ---------------------------------------------------------------------------
try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QListWidget, QListWidgetItem, QLineEdit, QPushButton,
        QFrame, QSizePolicy,
    )
    from PySide6.QtCore import Signal, Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

    class QWidget:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class Signal:  # type: ignore[no-redef]
        def __init__(self, *a):
            pass

    class QFrame:  # type: ignore[no-redef]
        pass

    class QLabel:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class QListWidget:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class QLineEdit:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class QPushButton:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class QVBoxLayout:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass

    class QHBoxLayout:  # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass


_SAFETY_BANNER = (
    "[!] GUI UX Only | Research Only | No Real Orders | Production Trading BLOCKED"
)


class NavigationSidebar(QWidget):
    """Sidebar widget showing tab groups with click signal.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    if _PYSIDE6_AVAILABLE:
        group_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
            self._build_ui()
        else:
            logger.warning("NavigationSidebar: PySide6 not available — stub mode")

    def _build_ui(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        banner = QLabel(_SAFETY_BANNER)
        banner.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(banner)

        title = QLabel("Tab Groups")
        title.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(title)

        self._group_list = TabGroupListWidget(self)
        layout.addWidget(self._group_list)

        if hasattr(self._group_list, "group_clicked"):
            self._group_list.group_clicked.connect(self.group_selected)

    def set_groups(self, groups: List[dict]) -> None:
        """Populate the group list."""
        if _PYSIDE6_AVAILABLE and hasattr(self, "_group_list"):
            self._group_list.set_groups(groups)


class TabGroupListWidget(QWidget):
    """List of tab groups as clickable items.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    if _PYSIDE6_AVAILABLE:
        group_clicked = Signal(str)

    def __init__(self, parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
            self._build_ui()
        else:
            logger.warning("TabGroupListWidget: PySide6 not available — stub mode")

    def _build_ui(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._list = QListWidget()
        self._list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self._list)

    def _on_item_clicked(self, item) -> None:
        if _PYSIDE6_AVAILABLE:
            self.group_clicked.emit(item.text())

    def set_groups(self, groups: List[dict]) -> None:
        """Populate the group list widget."""
        if not _PYSIDE6_AVAILABLE or not hasattr(self, "_list"):
            return
        self._list.clear()
        for g in groups:
            self._list.addItem(g.get("display_name", g.get("group_id", "")))


class TabSearchBox(QWidget):
    """Search input box with results list.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    if _PYSIDE6_AVAILABLE:
        search_triggered = Signal(str)

    def __init__(self, parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
            self._build_ui()
        else:
            logger.warning("TabSearchBox: PySide6 not available — stub mode")

    def _build_ui(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        banner = QLabel(_SAFETY_BANNER)
        banner.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(banner)

        row = QHBoxLayout()
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search tabs by keyword...")
        row.addWidget(self._search_input)
        btn = QPushButton("Search")
        btn.clicked.connect(self._on_search)
        row.addWidget(btn)
        layout.addLayout(row)

        self._results_list = QListWidget()
        layout.addWidget(self._results_list)

    def _on_search(self) -> None:
        if _PYSIDE6_AVAILABLE and hasattr(self, "_search_input"):
            query = self._search_input.text().strip()
            self.search_triggered.emit(query)

    def set_results(self, tabs: List[dict]) -> None:
        """Populate results list."""
        if not _PYSIDE6_AVAILABLE or not hasattr(self, "_results_list"):
            return
        self._results_list.clear()
        for t in tabs:
            label = f"{t.get('display_name', t.get('tab_id', ''))}  [{t.get('group', '')}]  {t.get('priority', '')}"
            self._results_list.addItem(label)


class FavoriteTabsWidget(QWidget):
    """Shows favorite tabs as a list.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    if _PYSIDE6_AVAILABLE:
        tab_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
            self._build_ui()
        else:
            logger.warning("FavoriteTabsWidget: PySide6 not available — stub mode")

    def _build_ui(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        banner = QLabel(_SAFETY_BANNER)
        banner.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(banner)

        title = QLabel("Favorites")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)

        self._list = QListWidget()
        self._list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self._list)

    def _on_item_clicked(self, item) -> None:
        if _PYSIDE6_AVAILABLE:
            self.tab_selected.emit(item.text())

    def set_favorites(self, tab_ids: List[str]) -> None:
        """Populate favorites list."""
        if not _PYSIDE6_AVAILABLE or not hasattr(self, "_list"):
            return
        self._list.clear()
        for tid in tab_ids:
            self._list.addItem(tid)


class RecentTabsWidget(QWidget):
    """Shows recently-used tabs as a list.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    if _PYSIDE6_AVAILABLE:
        tab_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
            self._build_ui()
        else:
            logger.warning("RecentTabsWidget: PySide6 not available — stub mode")

    def _build_ui(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        banner = QLabel(_SAFETY_BANNER)
        banner.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(banner)

        title = QLabel("Recently Used")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)

        self._list = QListWidget()
        self._list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self._list)

    def _on_item_clicked(self, item) -> None:
        if _PYSIDE6_AVAILABLE:
            self.tab_selected.emit(item.text())

    def set_recent(self, tab_ids: List[str]) -> None:
        """Populate recent list."""
        if not _PYSIDE6_AVAILABLE or not hasattr(self, "_list"):
            return
        self._list.clear()
        for tid in tab_ids:
            self._list.addItem(tid)


class NavigationBreadcrumb(QWidget):
    """Breadcrumb label showing current group > tab.

    [!] GUI UX Only. Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    def __init__(self, parent=None) -> None:
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
            self._build_ui()
        else:
            logger.warning("NavigationBreadcrumb: PySide6 not available — stub mode")

    def _build_ui(self) -> None:
        if not _PYSIDE6_AVAILABLE:
            return
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        self._label = QLabel("All Groups")
        self._label.setStyleSheet("color: #aaa; font-size: 11px;")
        layout.addWidget(self._label)

    def set_path(self, group: str = "", tab: str = "") -> None:
        """Update breadcrumb display."""
        if not _PYSIDE6_AVAILABLE or not hasattr(self, "_label"):
            return
        if group and tab:
            self._label.setText(f"{group}  >  {tab}")
        elif group:
            self._label.setText(group)
        else:
            self._label.setText("All Groups")
