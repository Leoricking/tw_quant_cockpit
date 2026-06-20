"""
reports/data_gov_tw_provider_report.py — data.gov.tw Provider Report v1.4.3.
[!] Research Only. No Real Orders. Not Investment Advice.
[!] Official data.gov.tw Public Data. Government Statistical/Macro Data Only.
[!] formal_use_allowed=False by default. Allowlist Required.
[!] Cannot Override TWSE/TPEx/MOPS. No Auto-Discovery. No Auto-Download.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NO_REAL_ORDERS = True
BROKER_EXECUTION_ENABLED = False
PRODUCTION_TRADING_BLOCKED = True
DATA_GOV_TW_MOCK_FALLBACK_ENABLED = False
DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED = False
DATA_GOV_TW_AUTO_DISCOVERY_ENABLED = False
DATA_GOV_TW_ALLOWLIST_REQUIRED = True
DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER = False


class DataGovTwProviderReport:
    """
    Builds data.gov.tw Provider Report v1.4.3 in Markdown.

    Sections:
    1. Overview
    2. Dataset Catalog
    3. Allowlist Status
    4. License Validation
    5. Schema Contracts
    6. Resources
    7. Fetch Summary
    8. Data Quality
    9. Freshness
    10. Revisions
    11. Lineage
    12. Safety Invariants
    """

    REPORT_TITLE = "data.gov.tw Provider Report"
    REPORT_VERSION = "v1.4.3"

    def __init__(
        self,
        report_date: Optional[str] = None,
        mode: str = "real",
        health_data: Optional[dict] = None,
        allowlist_data: Optional[dict] = None,
        catalog_data: Optional[list] = None,
        fetch_run_data: Optional[dict] = None,
        quality_data: Optional[dict] = None,
        freshness_data: Optional[dict] = None,
        revision_data: Optional[list] = None,
        lineage_data: Optional[dict] = None,
        schema_data: Optional[list] = None,
        resource_data: Optional[list] = None,
        license_data: Optional[list] = None,
    ):
        self.report_date = report_date or datetime.now().strftime("%Y-%m-%d")
        self.mode = mode
        self.health_data = health_data or {}
        self.allowlist_data = allowlist_data or {}
        self.catalog_data = catalog_data or []
        self.fetch_run_data = fetch_run_data or {}
        self.quality_data = quality_data or {}
        self.freshness_data = freshness_data or {}
        self.revision_data = revision_data or []
        self.lineage_data = lineage_data or {}
        self.schema_data = schema_data or []
        self.resource_data = resource_data or []
        self.license_data = license_data or []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self, output_dir: Optional[str] = None) -> str:
        """Build report, write to disk, return output path."""
        out_dir = output_dir or os.path.join(_BASE_DIR, "reports")
        os.makedirs(out_dir, exist_ok=True)
        filename = f"data_gov_tw_provider_report_{self.report_date}.md"
        out_path = os.path.join(out_dir, filename)
        content = self.render()
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            logger.info("DataGovTwProviderReport: wrote %s", out_path)
        except Exception as exc:
            logger.error("DataGovTwProviderReport: write failed: %s", exc)
            raise
        return out_path

    def render(self) -> str:
        """Return full Markdown report as string."""
        sections = [
            self._section_header(),
            self._section_overview(),
            self._section_catalog(),
            self._section_allowlist(),
            self._section_license(),
            self._section_schema_contracts(),
            self._section_resources(),
            self._section_fetch_summary(),
            self._section_data_quality(),
            self._section_freshness(),
            self._section_revisions(),
            self._section_lineage(),
            self._section_safety(),
        ]
        return "\n\n".join(s for s in sections if s)

    def get_summary(self) -> dict:
        """Return structured summary dict for programmatic use."""
        health = self.health_data
        return {
            "report_title": self.REPORT_TITLE,
            "report_version": self.REPORT_VERSION,
            "report_date": self.report_date,
            "mode": self.mode,
            "provider_id": "data_gov_tw_official",
            "official_source": True,
            "no_real_orders": NO_REAL_ORDERS,
            "broker_execution_enabled": BROKER_EXECUTION_ENABLED,
            "production_trading_blocked": PRODUCTION_TRADING_BLOCKED,
            "mock_fallback_enabled": DATA_GOV_TW_MOCK_FALLBACK_ENABLED,
            "auto_download_enabled": DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED,
            "auto_discovery_enabled": DATA_GOV_TW_AUTO_DISCOVERY_ENABLED,
            "allowlist_required": DATA_GOV_TW_ALLOWLIST_REQUIRED,
            "can_override_primary_provider": DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER,
            "health_all_pass": health.get("all_pass", False),
            "health_passed": health.get("passed", 0),
            "health_total": health.get("total_checks", 0),
            "catalog_count": len(self.catalog_data),
            "resource_count": len(self.resource_data),
            "revision_count": len(self.revision_data),
            "schema_count": len(self.schema_data),
        }

    # ------------------------------------------------------------------
    # Private section builders
    # ------------------------------------------------------------------

    def _section_header(self) -> str:
        lines = [
            f"# {self.REPORT_TITLE} {self.REPORT_VERSION}",
            "",
            f"> **Date:** {self.report_date}  |  **Mode:** {self.mode}",
            f"> **Provider:** data_gov_tw_official (Official data.gov.tw Public Data)",
            f"> **Track:** public_data_provider",
            ">",
            "> **[!] Research Only. No Real Orders. Not Investment Advice.**",
            "> **[!] Official data.gov.tw Public Data. Government Statistical/Macro Data Only.**",
            "> **[!] formal_use_allowed=False by default. Allowlist Required.**",
            "> **[!] Cannot Override TWSE/TPEx/MOPS Primary Provider Status.**",
            "> **[!] No Auto-Discovery. No Auto-Download. No Wildcard Allowlist.**",
        ]
        return "\n".join(lines)

    def _section_overview(self) -> str:
        health = self.health_data
        all_pass = health.get("all_pass", False)
        passed = health.get("passed", 0)
        total = health.get("total_checks", 0)
        status_str = "PASS" if all_pass else "FAIL"
        lines = [
            "## 1. Overview",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Provider ID | `data_gov_tw_official` |",
            f"| Report Version | {self.REPORT_VERSION} |",
            f"| Report Date | {self.report_date} |",
            f"| Mode | {self.mode} |",
            f"| Official Source | Yes |",
            f"| Data Domain | Government Statistical / Macro / Policy |",
            f"| Health Status | **{status_str}** ({passed}/{total} checks passed) |",
            f"| No Real Orders | {NO_REAL_ORDERS} |",
            f"| Broker Execution | {BROKER_EXECUTION_ENABLED} |",
            f"| Production Trading | BLOCKED |",
            f"| Mock Fallback | {DATA_GOV_TW_MOCK_FALLBACK_ENABLED} |",
            f"| Auto-Discovery | {DATA_GOV_TW_AUTO_DISCOVERY_ENABLED} |",
            f"| Auto-Download | {DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED} |",
            f"| Allowlist Required | {DATA_GOV_TW_ALLOWLIST_REQUIRED} |",
            f"| Can Override Primary | {DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER} |",
        ]
        return "\n".join(lines)

    def _section_catalog(self) -> str:
        lines = ["## 2. Dataset Catalog", ""]
        if not self.catalog_data:
            lines.append("_No catalog data provided._")
            return "\n".join(lines)
        lines.append(f"Total datasets in catalog: **{len(self.catalog_data)}**")
        lines.append("")
        lines.append("| Dataset ID | Title | Status | Allowlisted |")
        lines.append("|-----------|-------|--------|-------------|")
        for ds in self.catalog_data[:50]:
            ds_id = ds.get("dataset_id", "N/A")
            title = ds.get("title", "N/A")
            status = ds.get("status", "N/A")
            allowlisted = ds.get("allowlisted", False)
            lines.append(f"| `{ds_id}` | {title} | {status} | {allowlisted} |")
        if len(self.catalog_data) > 50:
            lines.append(f"| ... | _(+{len(self.catalog_data) - 50} more)_ | | |")
        return "\n".join(lines)

    def _section_allowlist(self) -> str:
        lines = ["## 3. Allowlist Status", ""]
        al = self.allowlist_data
        if not al:
            lines.append("_No allowlist data provided._")
            return "\n".join(lines)
        lines += [
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Total Entries | {al.get('total_entries', 0)} |",
            f"| Approved | {al.get('approved_count', 0)} |",
            f"| Planned | {al.get('planned_count', 0)} |",
            f"| Blocked | {al.get('blocked_count', 0)} |",
            f"| Disabled | {al.get('disabled_count', 0)} |",
            f"| Wildcard Allowed | **{al.get('wildcard_allowed', False)}** |",
            f"| Allow All Mode | **{al.get('allow_all_mode', False)}** |",
            f"| Allowlist Required | {al.get('allowlist_required', True)} |",
        ]
        return "\n".join(lines)

    def _section_license(self) -> str:
        lines = ["## 4. License Validation", ""]
        if not self.license_data:
            lines.append("_No license validation data provided._")
            return "\n".join(lines)
        lines.append(f"Total license records examined: **{len(self.license_data)}**")
        lines.append("")
        lines.append("| Dataset ID | License Status | Formal Use Allowed |")
        lines.append("|-----------|---------------|-------------------|")
        for rec in self.license_data[:30]:
            ds_id = rec.get("dataset_id", "N/A")
            status = rec.get("license_status", "N/A")
            allowed = rec.get("formal_use_allowed", False)
            lines.append(f"| `{ds_id}` | {status} | {allowed} |")
        if len(self.license_data) > 30:
            lines.append(f"| ... | _(+{len(self.license_data) - 30} more)_ | |")
        return "\n".join(lines)

    def _section_schema_contracts(self) -> str:
        lines = ["## 5. Schema Contracts", ""]
        if not self.schema_data:
            lines.append("_No schema contract data provided._")
            return "\n".join(lines)
        lines.append(f"Total schema contracts: **{len(self.schema_data)}**")
        lines.append("")
        lines.append("| Resource ID | Schema Status | Fields | Hash |")
        lines.append("|------------|--------------|--------|------|")
        for sc in self.schema_data[:30]:
            res_id = sc.get("resource_id", "N/A")
            status = sc.get("schema_status", "N/A")
            fields = len(sc.get("required_fields", []))
            h = (sc.get("contract_hash") or "")[:12]
            lines.append(f"| `{res_id}` | {status} | {fields} | `{h}...` |")
        return "\n".join(lines)

    def _section_resources(self) -> str:
        lines = ["## 6. Resources", ""]
        if not self.resource_data:
            lines.append("_No resource data provided._")
            return "\n".join(lines)
        lines.append(f"Total resources: **{len(self.resource_data)}**")
        lines.append("")
        lines.append("| Resource ID | Format | Size | Status |")
        lines.append("|------------|--------|------|--------|")
        for res in self.resource_data[:30]:
            res_id = res.get("resource_id", "N/A")
            fmt = res.get("format", "N/A")
            size = res.get("file_size_bytes", None)
            size_str = f"{size:,}" if size else "N/A"
            status = res.get("status", "N/A")
            lines.append(f"| `{res_id}` | {fmt} | {size_str} | {status} |")
        return "\n".join(lines)

    def _section_fetch_summary(self) -> str:
        lines = ["## 7. Fetch Summary", ""]
        fr = self.fetch_run_data
        if not fr:
            lines.append("_No fetch run data provided._")
            return "\n".join(lines)
        lines += [
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Run ID | `{fr.get('run_id', 'N/A')}` |",
            f"| Dataset ID | `{fr.get('dataset_id', 'N/A')}` |",
            f"| Status | {fr.get('status', 'N/A')} |",
            f"| Dry Run | {fr.get('dry_run', True)} |",
            f"| Fetched At | {fr.get('fetched_at', 'N/A')} |",
            f"| Records Fetched | {fr.get('records_fetched', 0)} |",
            f"| Records Stored | {fr.get('records_stored', 0)} |",
            f"| Error Message | {fr.get('error_message') or 'None'} |",
        ]
        return "\n".join(lines)

    def _section_data_quality(self) -> str:
        lines = ["## 8. Data Quality", ""]
        dq = self.quality_data
        if not dq:
            lines.append("_No data quality information provided._")
            return "\n".join(lines)
        lines += [
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Quality Score | {dq.get('quality_score', 'N/A')} / 100 |",
            f"| Total Records | {dq.get('total_records', 0)} |",
            f"| Valid Records | {dq.get('valid_records', 0)} |",
            f"| Malformed Records | {dq.get('malformed_records', 0)} |",
            f"| Missing Fields | {dq.get('missing_fields', 0)} |",
            f"| Formal Use Allowed | {dq.get('formal_use_allowed', False)} |",
        ]
        return "\n".join(lines)

    def _section_freshness(self) -> str:
        lines = ["## 9. Freshness", ""]
        fn = self.freshness_data
        if not fn:
            lines.append("_No freshness data provided._")
            return "\n".join(lines)
        lines += [
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Freshness Status | {fn.get('freshness_status', 'N/A')} |",
            f"| Update Frequency | {fn.get('update_frequency', 'N/A')} |",
            f"| Source Timestamp | {fn.get('source_timestamp', 'N/A')} |",
            f"| Grace Period (days) | {fn.get('grace_period_days', 'N/A')} |",
            f"| Near Stale | {fn.get('is_near_stale', False)} |",
            f"| Future Timestamp Blocked | {fn.get('future_blocked', True)} |",
        ]
        return "\n".join(lines)

    def _section_revisions(self) -> str:
        lines = ["## 10. Revisions", ""]
        if not self.revision_data:
            lines.append("_No revision data provided._")
            return "\n".join(lines)
        lines.append(f"Total revisions tracked: **{len(self.revision_data)}**")
        lines.append("")
        lines.append("| Revision ID | Dataset ID | Revision Type | Detected At | Severity |")
        lines.append("|------------|-----------|--------------|------------|---------|")
        for rev in self.revision_data[:20]:
            rev_id = (rev.get("revision_id") or "")[:12]
            ds_id = rev.get("dataset_id", "N/A")
            rev_type = rev.get("revision_type", "N/A")
            detected = rev.get("detected_at", "N/A")
            sev = rev.get("severity", "N/A")
            lines.append(f"| `{rev_id}...` | `{ds_id}` | {rev_type} | {detected} | {sev} |")
        if len(self.revision_data) > 20:
            lines.append(f"| ... | _(+{len(self.revision_data) - 20} more)_ | | | |")
        return "\n".join(lines)

    def _section_lineage(self) -> str:
        lines = ["## 11. Lineage", ""]
        ln = self.lineage_data
        if not ln:
            lines.append("_No lineage data provided._")
            return "\n".join(lines)
        lines += [
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Platform | {ln.get('platform', 'data.gov.tw')} |",
            f"| Dataset ID | `{ln.get('catalog_dataset_id', 'N/A')}` |",
            f"| Provider Agency | {ln.get('provider_agency', 'N/A')} |",
            f"| Authoritative Level | {ln.get('authoritative_level', 'N/A')} |",
            f"| Original Resource URL | {ln.get('original_resource_url_identifier', 'N/A')} |",
            f"| Lineage Valid | {ln.get('lineage_valid', False)} |",
        ]
        return "\n".join(lines)

    def _section_safety(self) -> str:
        lines = [
            "## 12. Safety Invariants",
            "",
            "All safety invariants are hard-coded and cannot be overridden at runtime.",
            "",
            "| Invariant | Status |",
            "|-----------|--------|",
            f"| NO_REAL_ORDERS | **{NO_REAL_ORDERS}** |",
            f"| BROKER_EXECUTION_ENABLED | **{BROKER_EXECUTION_ENABLED}** |",
            f"| PRODUCTION_TRADING_BLOCKED | **{PRODUCTION_TRADING_BLOCKED}** |",
            f"| DATA_GOV_TW_MOCK_FALLBACK_ENABLED | **{DATA_GOV_TW_MOCK_FALLBACK_ENABLED}** |",
            f"| DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED | **{DATA_GOV_TW_AUTO_DOWNLOAD_ENABLED}** |",
            f"| DATA_GOV_TW_AUTO_DISCOVERY_ENABLED | **{DATA_GOV_TW_AUTO_DISCOVERY_ENABLED}** |",
            f"| DATA_GOV_TW_ALLOWLIST_REQUIRED | **{DATA_GOV_TW_ALLOWLIST_REQUIRED}** |",
            f"| DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER | **{DATA_GOV_TW_CAN_OVERRIDE_PRIMARY_PROVIDER}** |",
            "| formal_use_allowed (default) | **False** |",
            "| wildcard_allowlist | **NOT ALLOWED** |",
            "| allow_all_mode | **NOT ALLOWED** |",
            "| TWSE/TPEx/MOPS override | **BLOCKED** |",
            "| Broker capability | **NOT DECLARED** |",
            "| Order execution | **NOT DECLARED** |",
            "| Real-time feed | **NOT AVAILABLE** |",
            "",
            "---",
            "",
            "_[!] This report is for research and informational purposes only._",
            "_[!] Not investment advice. No trading decisions should be based on this report._",
            "_[!] All data.gov.tw data is subject to the Government Data Open License._",
        ]
        return "\n".join(lines)
