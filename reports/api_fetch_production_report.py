"""
reports/api_fetch_production_report.py - API Fetch Productionization Report (v0.4.1).

Generates: reports/api_fetch_production_report_YYYY-MM-DD.md

[!] Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] Never displays full token. Never commits to git.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class APIFetchProductionReportBuilder:
    """
    API Fetch Productionization Report builder.

    Parameters
    ----------
    report_dir : Output directory for reports (default: reports/)
    mode       : "real" or "mock"
    """

    VERSION = "v0.4.1"

    # Safety flags — always included in every report
    _SAFETY_FLAGS = {
        "research_only":              True,
        "read_only":                  True,
        "no_real_orders":             True,
        "production_trading_blocked": True,
        "no_token_displayed":         True,
        "no_real_env_modified":       True,
    }

    def __init__(
        self,
        report_dir: str = "reports",
        mode:       str = "real",
    ):
        self.mode       = mode
        self._report_dir = os.path.join(_BASE_DIR, report_dir) if not os.path.isabs(report_dir) else report_dir
        os.makedirs(self._report_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def build(
        self,
        token_status:      Optional[dict] = None,
        diagnostics:       Optional[dict] = None,
        cache_stats:       Optional[dict] = None,
        lineage_summary:   Optional[dict] = None,
        parser_health:     Optional[dict] = None,
    ) -> str:
        """
        Build and save the report. Returns the output file path.

        Parameters
        ----------
        token_status    : From TokenSetupAssistant.inspect()
        diagnostics     : From APIFetchDiagnostics.summarize()
        cache_stats     : From APICache.stats()
        lineage_summary : From DataLineageTracker.export_lineage_summary()
        parser_health   : Dict with TWSE/TPEx/MOPS parser health info
        """
        today    = datetime.now().strftime("%Y-%m-%d")
        sections = self._build_sections(
            today, token_status, diagnostics, cache_stats, lineage_summary, parser_health
        )
        content = "\n\n".join(sections)

        out_path = os.path.join(self._report_dir, f"api_fetch_production_report_{today}.md")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as exc:
            logger.warning("APIFetchProductionReportBuilder: cannot write %s: %s", out_path, exc)

        return out_path

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _build_sections(self, today, token_status, diagnostics, cache_stats, lineage_summary, parser_health):
        sections = []

        # Header
        sections.append(
            f"# API Fetch Productionization Report\n\n"
            f"**Version:** {self.VERSION}  \n"
            f"**Date:** {today}  \n"
            f"**Mode:** {self.mode}  \n"
            f"**Generated:** {datetime.now().isoformat()}"
        )

        # 一、總覽
        sections.append(self._section_overview(today, diagnostics, cache_stats, lineage_summary))

        # 二、Token Setup
        sections.append(self._section_token_setup(token_status))

        # 三、Provider Diagnostics
        sections.append(self._section_provider_diagnostics(diagnostics))

        # 四、Retry / Timeout
        sections.append(self._section_retry(diagnostics))

        # 五、Cache
        sections.append(self._section_cache(cache_stats))

        # 六、Data Lineage
        sections.append(self._section_lineage(lineage_summary))

        # 七、Parser Health
        sections.append(self._section_parser_health(parser_health))

        # 八、安全聲明
        sections.append(self._section_safety())

        return sections

    def _section_overview(self, today, diagnostics, cache_stats, lineage_summary):
        d = diagnostics or {}
        c = cache_stats or {}
        l = lineage_summary or {}
        lines = [
            "## 一、總覽",
            "",
            f"- **Mode:** {self.mode}",
            "- **Read Only:** True",
            "- **No Real Orders:** True",
            f"- **Providers checked:** {d.get('total_providers_checked', '—')}",
            f"- **Datasets fetched:** {d.get('total_datasets_checked', '—')}",
            f"- **Cache status:** enabled={c.get('enabled', '—')} hits={c.get('hits', 0)} misses={c.get('misses', 0)}",
            f"- **Retry total:** {d.get('retry_total', 0)}",
            f"- **Lineage records:** {l.get('total_records', 0)}",
        ]
        return "\n".join(lines)

    def _section_token_setup(self, token_status):
        ts = token_status or {}
        lines = ["## 二、Token Setup", ""]
        req = ts.get("required_tokens", {})
        finmind = req.get("FINMIND_TOKEN", {})
        lines.append(f"- **FINMIND_TOKEN:** {'Configured' if finmind.get('configured') else 'MISSING'}")
        if finmind.get("configured"):
            lines.append(f"- **Token (masked):** `{finmind.get('masked_value', '****')}`")
        else:
            next_step = finmind.get("next_step", "")
            if next_step:
                lines.append(f"- **Next Step:** {next_step}")
        safety = ts.get("env_safety", {})
        lines.append(f"- **.env safe:** {safety.get('safe', '—')}")
        lines.append(f"- **.env.example exists:** {safety.get('env_example_exists', '—')}")
        issues = safety.get("issues", [])
        for issue in issues:
            lines.append(f"- **⚠ Issue:** {issue}")
        return "\n".join(lines)

    def _section_provider_diagnostics(self, diagnostics):
        d = diagnostics or {}
        lines = ["## 三、Provider Diagnostics", ""]
        records = d.get("records", [])
        if not records:
            lines.append("*No diagnostics recorded.*")
            return "\n".join(lines)

        lines.append("| Provider | Dataset | Status | Rows | Latency | Retries | Cache | Warning |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for r in records:
            lines.append(
                f"| {r.get('provider','')} | {r.get('dataset','')} | {r.get('status','')} "
                f"| {r.get('rows',0)} | {r.get('latency_ms',0):.0f}ms "
                f"| {r.get('retry_attempts',1)} | {'HIT' if r.get('cache_hit') else 'MISS'} "
                f"| {r.get('warning','')[:50]} |"
            )
        return "\n".join(lines)

    def _section_retry(self, diagnostics):
        d = diagnostics or {}
        records = d.get("records", [])
        total_retries = sum(max(0, r.get("retry_attempts", 1) - 1) for r in records)
        ok_n      = d.get("ok_count", 0)
        failed_n  = d.get("failed_count", 0)
        lines = [
            "## 四、Retry / Timeout",
            "",
            f"- **Total retry attempts:** {total_retries}",
            f"- **OK fetches:** {ok_n}",
            f"- **Failed fetches:** {failed_n}",
        ]
        for r in records:
            if r.get("retry_attempts", 1) > 1:
                lines.append(
                    f"- `{r.get('provider')}/{r.get('dataset')}`: "
                    f"{r.get('retry_attempts')} attempts — {r.get('error_type','')}"
                )
        return "\n".join(lines)

    def _section_cache(self, cache_stats):
        c = cache_stats or {}
        lines = [
            "## 五、Cache",
            "",
            f"- **Enabled:** {c.get('enabled', '—')}",
            f"- **Cache root:** `{c.get('cache_root', '—')}`",
            f"- **Total entries:** {c.get('total_entries', 0)}",
            f"- **Active (non-expired):** {c.get('active', 0)}",
            f"- **Expired:** {c.get('expired', 0)}",
            f"- **Hits / Misses:** {c.get('hits', 0)} / {c.get('misses', 0)}",
            f"- **Hit rate:** {c.get('hit_rate', 0):.1%}",
            f"- **Size:** {c.get('size_bytes', 0):,} bytes",
            "- **No token in keys:** True",
        ]
        return "\n".join(lines)

    def _section_lineage(self, lineage_summary):
        l = lineage_summary or {}
        lines = ["## 六、Data Lineage", ""]
        records = l.get("records", [])
        if not records:
            lines.append("*No lineage records.*")
            return "\n".join(lines)

        lines.append("| Dataset | Provider | Rows | Output | Fetched At | Lineage ID |")
        lines.append("|---|---|---|---|---|---|")
        for r in records[:20]:
            lines.append(
                f"| {r.get('dataset','')} | {r.get('provider','')} "
                f"| {r.get('rows_fetched',0)} "
                f"| `{str(r.get('output_path',''))[-40:]}` "
                f"| {str(r.get('fetched_at',''))[:19]} "
                f"| `{r.get('lineage_id','')}` |"
            )
        if len(records) > 20:
            lines.append(f"*... and {len(records) - 20} more records*")
        return "\n".join(lines)

    def _section_parser_health(self, parser_health):
        ph = parser_health or {}
        lines = ["## 七、Parser Health", ""]
        if not ph:
            lines.append("*No parser health data recorded.*")
            return "\n".join(lines)

        for parser_name, info in ph.items():
            schema_status = info.get("schema_status", "—") if isinstance(info, dict) else str(info)
            timing = info.get("timing_quality", "—") if isinstance(info, dict) else "—"
            lines.append(f"- **{parser_name}:** schema={schema_status}  timing={timing}")

        return "\n".join(lines)

    def _section_safety(self):
        return (
            "## 八、安全聲明\n\n"
            "- **Research Only:** True\n"
            "- **Read Only:** True\n"
            "- **No Real Orders:** True\n"
            "- **No token displayed in this report:** True\n"
            "- **Production Trading:** BLOCKED\n"
            "- **REAL_ORDER_READY:** False\n"
            "- **Auto weight apply:** DISABLED\n"
            "- **No real .env modified:** True\n\n"
            "> This report is generated for research and monitoring purposes only.  \n"
            "> It does not constitute investment advice.  \n"
            "> All trading is permanently blocked in this version."
        )
