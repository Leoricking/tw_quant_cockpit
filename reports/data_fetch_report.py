"""
reports/data_fetch_report.py - Data fetch report generator.

Generates Markdown report for fetch-public-data and enrich-universe-data runs.

Output: reports/data_fetch_report_YYYY-MM-DD.md

Sections:
    1. 抓取摘要 (fetch summary)
    2. 月營收狀態 (monthly revenue status)
    3. 基本面狀態 (fundamental status)
    4. 法人買賣狀態 (institutional status)
    5. 融資券狀態 (margin short status)
    6. Intraday 匯入狀態 (intraday import status)
    7. 失敗來源 (failed sources)
    8. 警告 (warnings)
    9. 下一步建議 (next steps)
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REPORTS_DIR = os.path.join(_BASE_DIR, "reports")


class DataFetchReport:
    """Generates a Markdown data fetch report."""

    def __init__(self):
        os.makedirs(_REPORTS_DIR, exist_ok=True)

    def generate(
        self,
        fetch_results: list,
        intraday_results: Optional[list] = None,
        failed_sources: Optional[list] = None,
        extra_warnings: Optional[list] = None,
    ) -> str:
        """
        Generate Markdown report and save to file.

        Parameters
        ----------
        fetch_results : list of dicts from FundamentalDataBuilder.fetch_and_build()
        intraday_results : list of dicts from IntradayDataImporter.import_folder()
        failed_sources : list of source name strings that failed
        extra_warnings : additional warning strings

        Returns
        -------
        str: path to generated report file
        """
        today = datetime.now().strftime("%Y-%m-%d")
        report_path = os.path.join(_REPORTS_DIR, f"data_fetch_report_{today}.md")

        lines = []
        lines.append(f"# 公開資料抓取報告 — {today}")
        lines.append("")
        lines.append(f"生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # 1. 抓取摘要
        lines.append("## 1. 抓取摘要")
        lines.append("")
        total_symbols = len(fetch_results)
        symbols_with_rev = sum(1 for r in fetch_results if r.get("monthly_revenue"))
        symbols_with_fin = sum(1 for r in fetch_results if r.get("fundamental"))
        symbols_with_inst = sum(1 for r in fetch_results if r.get("institutional"))
        symbols_with_margin = sum(1 for r in fetch_results if r.get("margin"))

        lines.append(f"- 處理股票數：{total_symbols}")
        lines.append(f"- 月營收取得：{symbols_with_rev}/{total_symbols}")
        lines.append(f"- 基本面取得：{symbols_with_fin}/{total_symbols}")
        lines.append(f"- 法人資料取得：{symbols_with_inst}/{total_symbols}")
        lines.append(f"- 融資券資料取得：{symbols_with_margin}/{total_symbols}")
        lines.append("")

        # 2. 月營收狀態
        lines.append("## 2. 月營收狀態 (monthly_revenue)")
        lines.append("")
        lines.append("| 股票 | 狀態 | 筆數 | 說明 |")
        lines.append("|------|------|------|------|")
        for r in fetch_results:
            sym = r.get("symbol", "?")
            rev = r.get("monthly_revenue")
            if rev:
                rows = rev.get("rows_added", "?")
                status = "✓ OK"
            else:
                rows = 0
                status = "✗ 無資料"
            lines.append(f"| {sym} | {status} | {rows} | |")
        lines.append("")

        # 3. 基本面狀態
        lines.append("## 3. 基本面狀態 (fundamental)")
        lines.append("")
        lines.append("| 股票 | 狀態 | 筆數 | 說明 |")
        lines.append("|------|------|------|------|")
        for r in fetch_results:
            sym = r.get("symbol", "?")
            fin = r.get("fundamental")
            if fin:
                rows = fin.get("rows_added", "?")
                status = "✓ OK"
            else:
                rows = 0
                status = "✗ 無資料"
            lines.append(f"| {sym} | {status} | {rows} | |")
        lines.append("")

        # 4. 法人狀態
        lines.append("## 4. 法人買賣狀態 (institutional)")
        lines.append("")
        lines.append("| 股票 | 狀態 | 筆數 | 說明 |")
        lines.append("|------|------|------|------|")
        for r in fetch_results:
            sym = r.get("symbol", "?")
            inst = r.get("institutional")
            if inst:
                rows = inst.get("rows_added", "?")
                status = "✓ OK"
            else:
                rows = 0
                status = "✗ 無資料"
            lines.append(f"| {sym} | {status} | {rows} | |")
        lines.append("")

        # 5. 融資券狀態
        lines.append("## 5. 融資券狀態 (margin_short)")
        lines.append("")
        lines.append("| 股票 | 狀態 | 筆數 | 說明 |")
        lines.append("|------|------|------|------|")
        for r in fetch_results:
            sym = r.get("symbol", "?")
            margin = r.get("margin")
            if margin:
                rows = margin.get("rows_added", "?")
                status = "✓ OK"
            else:
                rows = 0
                status = "✗ 無資料"
            lines.append(f"| {sym} | {status} | {rows} | |")
        lines.append("")

        # 6. Intraday 匯入狀態
        lines.append("## 6. Intraday 匯入狀態")
        lines.append("")
        if intraday_results:
            lines.append("| 檔案 | 股票 | 頻率 | 匯入筆數 | 狀態 |")
            lines.append("|------|------|------|----------|------|")
            for r in intraday_results:
                fname = os.path.basename(str(r.get("file", "")))
                sym = r.get("symbol", "?")
                freq = r.get("freq", "?")
                rows = r.get("rows_imported", 0)
                warns = r.get("warnings", [])
                status = "✗ " + warns[0] if warns else "✓ OK"
                lines.append(f"| {fname} | {sym} | {freq} | {rows} | {status} |")
        else:
            lines.append("未執行 intraday 匯入。")
        lines.append("")

        # 7. 失敗來源
        lines.append("## 7. 失敗來源")
        lines.append("")
        if failed_sources:
            for fs in failed_sources:
                lines.append(f"- {fs}")
        else:
            lines.append("無失敗來源。")
        lines.append("")

        # 8. 警告
        lines.append("## 8. 警告")
        lines.append("")
        all_warnings = []
        for r in fetch_results:
            for w in r.get("warnings", []):
                all_warnings.append(w)
        if extra_warnings:
            all_warnings.extend(extra_warnings)
        if all_warnings:
            for w in all_warnings:
                lines.append(f"- {w}")
        else:
            lines.append("無警告。")
        lines.append("")

        # 9. 下一步建議
        lines.append("## 9. 下一步建議")
        lines.append("")
        lines.append("```bash")
        lines.append("# 確認資料品質")
        lines.append("python main.py data-check --stock 2454")
        lines.append("")
        lines.append("# 更新 Universe 品質報告")
        lines.append("python main.py universe-quality --report")
        lines.append("")
        lines.append("# 重跑驗證套件")
        lines.append("python main.py run-validation-suite --mode real --min-symbols 10")
        lines.append("```")
        lines.append("")
        lines.append("> 注意：公開資料來源可能因網路或格式變更而失敗，請確認 warnings 並手動補充缺失資料。")
        lines.append("")
        lines.append("---")
        lines.append("*TW Quant Cockpit v0.3.9 — 本報告不構成投資建議*")

        content = "\n".join(lines)
        try:
            with open(report_path, "w", encoding="utf-8") as fh:
                fh.write(content)
            logger.info("DataFetchReport: written to %s", report_path)
        except Exception as exc:
            logger.error("DataFetchReport: cannot write report: %s", exc)

        return report_path
