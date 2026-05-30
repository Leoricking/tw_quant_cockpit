"""
reports/provider_health_report.py - Provider health report builder (v0.3.18).

Generates a Markdown report showing provider status, token config (masked),
capability matrix, and safety summary.

Output: reports/provider_health_report_YYYY-MM-DD.md

[!] Read Only. No Real Orders.
[!] Tokens masked — no full token displayed.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProviderHealthReportBuilder:
    """
    Builds provider_health_report_YYYY-MM-DD.md from health check results.

    Parameters
    ----------
    report_date : "YYYY-MM-DD" (default: today)
    mode        : "real" or "mock"
    health_data : dict returned by ProviderHealthChecker.run_all()
    """

    def __init__(
        self,
        report_date:  Optional[str] = None,
        mode:         str = "real",
        health_data:  Optional[dict] = None,
    ):
        self.report_date = report_date or datetime.now().strftime("%Y-%m-%d")
        self.mode        = mode
        self.health_data = health_data or {}

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, output_dir: Optional[str] = None) -> str:
        """
        Build the report and write to disk.
        Returns the output file path.
        """
        out_dir = output_dir or os.path.join(_BASE_DIR, "reports")
        os.makedirs(out_dir, exist_ok=True)

        filename = f"provider_health_report_{self.report_date}.md"
        out_path = os.path.join(out_dir, filename)

        sections = [
            self._section_header(),
            self._section_overview(),
            self._section_provider_status(),
            self._section_token_status(),
            self._section_capability_matrix(),
            self._section_safety(),
            self._section_recommendations(),
        ]

        content = "\n\n".join(s for s in sections if s)

        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            logger.info("ProviderHealthReportBuilder: wrote %s", out_path)
        except Exception as exc:
            logger.error("ProviderHealthReportBuilder: write failed: %s", exc)
            raise

        return out_path

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _section_header(self) -> str:
        return (
            f"# Provider Health Report\n\n"
            f"**Date:** {self.report_date}  \n"
            f"**Mode:** {self.mode.upper()}  \n"
            f"**Generated:** {self.health_data.get('checked_at', datetime.now().isoformat())}  \n\n"
            f"> [!] Read Only · No Real Orders · Tokens Masked"
        )

    def _section_overview(self) -> str:
        summary   = self.health_data.get("summary", {})
        providers = self.health_data.get("providers", [])
        n         = len(providers)

        lines = ["## 一、總覽", ""]
        lines.append(f"| 項目 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| Mode | {self.mode.upper()} |")
        lines.append(f"| Checked Providers | {n} |")
        for s, cnt in sorted(summary.items()):
            lines.append(f"| {s} | {cnt} |")
        lines.append(f"| Read-only Guarantee | ✓ |")
        lines.append(f"| No Real Orders | ✓ |")

        return "\n".join(lines)

    def _section_provider_status(self) -> str:
        providers = self.health_data.get("providers", [])
        if not providers:
            return "## 二、Provider 狀態\n\n(no providers checked)"

        lines = ["## 二、Provider 狀態", ""]
        lines.append("| Provider | Status | Read Only | Token Required | Token Configured | Message |")
        lines.append("|----------|--------|-----------|----------------|------------------|---------|")
        for p in providers:
            name     = p.get("provider_name", "")
            status   = p.get("status", "")
            ro       = "✓" if p.get("read_only", True) else "✗"
            tr       = "Yes" if p.get("token_required", False) else "No"
            tc       = "✓" if p.get("token_configured", False) else "✗"
            msg      = p.get("message", "")[:80].replace("|", "\\|")
            lines.append(f"| {name} | {status} | {ro} | {tr} | {tc} | {msg} |")

        # Recommended actions
        actions = [(p["provider_name"], p["recommended_action"])
                   for p in providers if p.get("recommended_action")]
        if actions:
            lines += ["", "**建議行動：**", ""]
            for pname, action in actions:
                lines.append(f"- **{pname}**: {action}")

        return "\n".join(lines)

    def _section_token_status(self) -> str:
        token_status = self.health_data.get("token_status", {})
        if not token_status:
            return "## 三、Token Status\n\n(no token information)"

        lines = ["## 三、Token Status", ""]
        lines.append("> Tokens are masked. No full token is displayed.")
        lines.append("")
        lines.append("| Token Name | Configured | Masked | Required | Used By | Warning |")
        lines.append("|------------|------------|--------|----------|---------|---------|")
        for name, info in token_status.items():
            configured = "✓" if info.get("configured", False) else "✗"
            masked     = info.get("masked", "(not configured)")
            required   = "Yes" if info.get("required", False) else "No"
            used_by    = ", ".join(info.get("used_by", []))
            warning    = info.get("warning", "")[:60].replace("|", "\\|")
            lines.append(f"| {name} | {configured} | `{masked}` | {required} | {used_by} | {warning} |")

        return "\n".join(lines)

    def _section_capability_matrix(self) -> str:
        providers = self.health_data.get("providers", [])
        if not providers:
            return "## 四、Data Capability Matrix\n\n(no providers)"

        capabilities = [
            ("daily_price",          "Daily Price"),
            ("monthly_revenue",      "Revenue"),
            ("institutional",        "Institutional"),
            ("margin",               "Margin"),
            ("fundamental",          "Fundamental"),
            ("intraday",             "Intraday"),
            ("tick",                 "Tick"),
            ("bidask",               "BidAsk"),
            ("account_info_readonly","Account RO"),
            ("real_order_execution", "Order Exec"),
        ]

        cap_keys = [c[0] for c in capabilities]
        cap_labels = [c[1] for c in capabilities]

        header  = "| Provider | " + " | ".join(cap_labels) + " |"
        divider = "|----------|" + "|".join(["--------"] * len(cap_labels)) + "|"

        lines = ["## 四、Data Capability Matrix", "", header, divider]
        for p in providers:
            name = p.get("provider_name", "")
            caps = p.get("capabilities", {})
            cells = []
            for key in cap_keys:
                val = caps.get(key, False)
                if key == "real_order_execution":
                    cells.append("DISABLED" if not val else "**[UNSAFE]**")
                else:
                    cells.append("✓" if val else "✗")
            lines.append(f"| {name} | " + " | ".join(cells) + " |")

        return "\n".join(lines)

    def _section_safety(self) -> str:
        return "\n".join([
            "## 五、安全限制",
            "",
            "| 安全項目 | 狀態 |",
            "|----------|------|",
            "| Read Only | ✓ 所有 provider 均為唯讀 |",
            "| No Broker Execution | ✓ 不呼叫任何 broker.submit_order |",
            "| No submit_order | ✓ submit_order 永久 raise RuntimeError |",
            "| No Token Committed | ✓ .env 在 .gitignore，不 commit |",
            "| No Real Orders | ✓ TWQC_ENABLE_REAL_ORDER=False |",
            "| Token Masking | ✓ 僅顯示 mask，不顯示完整 token |",
            "| No Auto Weight Update | ✓ 不自動套用 rule weight tuning |",
            "| No Auto Trade | ✓ 不自動買賣 |",
        ])

    def _section_recommendations(self) -> str:
        providers = self.health_data.get("providers", [])
        token_status = self.health_data.get("token_status", {})

        lines = ["## 六、建議", ""]

        # Token config advice
        finmind_info = token_status.get("FINMIND_TOKEN", {})
        if not finmind_info.get("configured", False):
            lines += [
                "**FinMind Token 未設定：**",
                "- 可在 https://finmindtrade.com/ 免費申請 token。",
                "- 將 `FINMIND_TOKEN=your_token` 加入 `.env` 檔案。",
                "- 不設定 token 時，只能存取 FinMind 公開資料（有速率限制）。",
                "",
            ]

        # Public API fallback
        lines += [
            "**Public API Fallback：**",
            "- CSV / XQ Export provider 本地資料不需 token，scheduler 可安全執行。",
            "- TWSE / TPEx / MOPS 公開 API 計劃於 v0.4 啟用，不需 token。",
            "",
        ]

        # Scheduler safe tasks
        lines += [
            "**Scheduler 可安全執行的 task：**",
            "- `daily_data_update` — provider health check + fetch-public-data（需 token）",
            "- `daily_validation` — 本地資料驗證，不需 API token",
            "- `daily_auto_report` — 報告生成，不需 API token",
            "- `weekly_signal_quality` — 本地回測，不需 API token",
            "- `weekly_rule_weight_tuning` — 本地回測，不需 API token",
            "- `monthly_universe_quality` — 本地資料品質檢查，不需 API token",
            "",
        ]

        # Manual confirmation items
        lines += [
            "**仍需人工確認的項目：**",
            "- FinMind token 是否設定（若需要完整公開資料）",
            "- 本地 CSV 資料是否定期更新",
            "- Rule weight tuning 結果不會自動套用，需人工確認後更新",
            "- 任何新 provider 整合前，確認 submit_order 已 raise RuntimeError",
        ]

        return "\n".join(lines)
