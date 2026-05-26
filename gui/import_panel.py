"""
gui/import_panel.py - CSV import dialog for TW Quant Cockpit.

Opens as a modal dialog when user clicks "Import CSV" in the toolbar.
"""

import logging
import os

logger = logging.getLogger(__name__)

try:
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QComboBox, QLineEdit, QTextEdit, QCheckBox, QFileDialog,
        QDialogButtonBox,
    )
    from PySide6.QtCore import Qt
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False

_DATA_TYPES = [
    'daily', 'institutional', 'margin', 'monthly_revenue',
    'holder', 'trust_cost', 'profile',
]


class ImportPanel(QDialog if _PYSIDE6_AVAILABLE else object):
    """
    Modal dialog for importing CSV files into the standard data/import/ structure.
    """

    def __init__(self, parent=None):
        if _PYSIDE6_AVAILABLE:
            super().__init__(parent)
            self._build()

    def _build(self):
        self.setWindowTitle("匯入 CSV 資料")
        self.setMinimumWidth(560)
        self.setStyleSheet("background:#12121E; color:#DDDDDD;")

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Data type selector
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("資料類型："))
        self._type_combo = QComboBox()
        self._type_combo.addItems(_DATA_TYPES)
        self._type_combo.setStyleSheet("background:#252540; color:#FFFFFF; padding:4px;")
        row1.addWidget(self._type_combo)
        row1.addStretch()
        layout.addLayout(row1)

        # File path
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("CSV 檔案："))
        self._file_edit = QLineEdit()
        self._file_edit.setStyleSheet("background:#252540; color:#FFFFFF; padding:4px;")
        self._file_edit.setPlaceholderText("選擇或輸入檔案路徑…")
        row2.addWidget(self._file_edit)
        browse_btn = QPushButton("瀏覽…")
        browse_btn.setStyleSheet("background:#334466; color:#FFFFFF; padding:4px 8px;")
        browse_btn.clicked.connect(self._browse)
        row2.addWidget(browse_btn)
        layout.addLayout(row2)

        # Replace checkbox
        self._replace_check = QCheckBox("--replace（覆蓋既有標準 CSV，預設為 append 去重）")
        self._replace_check.setStyleSheet("color:#AAAAAA;")
        layout.addWidget(self._replace_check)

        # Import button
        import_btn = QPushButton("▶ 執行匯入")
        import_btn.setStyleSheet(
            "background:#2266AA; color:#FFFFFF; font-weight:bold; padding:6px 16px;"
        )
        import_btn.clicked.connect(self._do_import)
        layout.addWidget(import_btn)

        # Result display
        layout.addWidget(QLabel("匯入結果："))
        self._result_text = QTextEdit()
        self._result_text.setReadOnly(True)
        self._result_text.setMinimumHeight(160)
        self._result_text.setStyleSheet(
            "background:#0A0A14; color:#88FF88; font-family:monospace; font-size:11px;"
        )
        layout.addWidget(self._result_text)

        # Close button
        close_btn = QPushButton("關閉")
        close_btn.setStyleSheet("background:#333355; color:#FFFFFF; padding:4px 12px;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def _browse(self):
        if not _PYSIDE6_AVAILABLE:
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "選擇 CSV 檔案", "", "CSV Files (*.csv);;All Files (*)"
        )
        if path:
            self._file_edit.setText(path)

    def _do_import(self):
        if not _PYSIDE6_AVAILABLE:
            return

        data_type = self._type_combo.currentText()
        file_path = self._file_edit.text().strip()
        replace = self._replace_check.isChecked()

        if not file_path:
            self._result_text.setPlainText("請先選擇 CSV 檔案。")
            return

        self._result_text.setPlainText("匯入中…")

        try:
            from data.csv_importer import CSVImporter
            importer = CSVImporter()
            result = importer.import_csv(
                data_type=data_type,
                file_path=file_path,
                append=not replace,
            )
            lines = [
                f"匯入類型：{result['data_type']}",
                f"輸入檔案：{result['input_file']}",
                f"輸出檔案：{result['output_file']}",
                f"匯入筆數：{result['rows_imported']}",
                f"總筆數：  {result['rows_total']}",
                f"缺少欄位：{result.get('missing_columns', []) or '無'}",
            ]
            for w in result.get('warnings', []):
                lines.append(f"⚠ 警告：{w}")
            lines.append(f"狀態：{'✅ 成功' if result['success'] else '❌ 失敗'}")
            self._result_text.setPlainText('\n'.join(lines))

        except Exception as exc:
            self._result_text.setPlainText(f"匯入錯誤：{exc}")
            logger.error("ImportPanel._do_import error: %s", exc)
