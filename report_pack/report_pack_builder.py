"""report_pack/report_pack_builder.py — ReportPackBuilder for TW Quant Cockpit v0.5.4.

Assembles a ReportPack: collects report items, writes index.md and manifest.json.
Output root: data/backtest_results/report_pack/{pack_type}_YYYY-MM-DD/

[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import List, Optional

from report_pack.report_pack_schema import (
    ReportPack, ReportPackItem,
    PACK_DAILY, PACK_WEEKLY, PACK_FULL,
    STATUS_READY, STATUS_PARTIAL, STATUS_MISSING,
)
from report_pack.report_registry import ReportRegistry
from report_pack.report_collector import ReportCollector

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_OUTPUT_ROOT = os.path.join(BASE_DIR, "data", "backtest_results", "report_pack")


class ReportPackBuilder:
    """Builds a consolidated ReportPack for a given pack type and date.

    Parameters
    ----------
    pack_type        : 'daily' | 'weekly' | 'full' | 'custom'
    report_date      : YYYY-MM-DD string; defaults to today
    output_root      : root folder for output (default: data/backtest_results/report_pack)
    generate_missing : if True, attempt to generate missing reports (default: False)

    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True
    real_order_ready   = False

    def __init__(
        self,
        pack_type: str = PACK_DAILY,
        report_date: Optional[str] = None,
        output_root: Optional[str] = None,
        generate_missing: bool = False,
    ) -> None:
        self.pack_type       = pack_type
        self.report_date     = report_date or datetime.now().strftime("%Y-%m-%d")
        self.output_root     = output_root or _DEFAULT_OUTPUT_ROOT
        self.generate_missing = generate_missing  # default False — do NOT auto-generate

        self._registry  = ReportRegistry()
        self._collector = ReportCollector()

    def build(self) -> ReportPack:
        """Build and return the ReportPack. Writes index.md and manifest.json."""
        logger.info(
            "ReportPackBuilder.build [pack=%s date=%s generate_missing=%s]",
            self.pack_type, self.report_date, self.generate_missing,
        )

        report_types = self._registry.get_report_types(self.pack_type)
        items = self._collector.collect(report_types, self.report_date)

        # Determine overall status
        ready   = sum(1 for i in items if i.status == STATUS_READY)
        total   = len(items)
        missing = sum(1 for i in items if i.status == STATUS_MISSING)

        if ready == total:
            status = STATUS_READY
        elif ready > 0:
            status = STATUS_PARTIAL
        else:
            status = STATUS_MISSING

        health_score = (ready / total * 100.0) if total > 0 else 0.0

        # Create output directory
        out_dir = os.path.join(
            self.output_root, f"{self.pack_type}_{self.report_date}"
        )
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception as exc:
            logger.warning("ReportPackBuilder: cannot create output dir: %s", exc)

        pack = ReportPack(
            pack_type=self.pack_type,
            report_date=self.report_date,
            status=status,
            items=items,
            output_dir=out_dir,
            health_score=round(health_score, 1),
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        pack.index_path    = self._write_index(pack)
        pack.manifest_path = self._write_manifest(pack)

        return pack

    # ------------------------------------------------------------------
    # Writers
    # ------------------------------------------------------------------

    def _write_index(self, pack: ReportPack) -> str:
        """Write index.md to the pack output directory."""
        try:
            lines = [
                f"# TW Quant Cockpit — {self._registry.pack_type_display(pack.pack_type)}",
                f"",
                f"> **v0.5.4** | Report Date: {pack.report_date} | Pack Type: {pack.pack_type.upper()}",
                f">",
                f"> [!] Research Only. No Real Orders. Production Trading: BLOCKED.",
                f"",
                f"---",
                f"",
                f"## 一、Pack Summary",
                f"",
                f"| 項目 | 值 |",
                f"|------|---|",
                f"| Pack Type | {pack.pack_type.upper()} |",
                f"| Report Date | {pack.report_date} |",
                f"| Status | {pack.status} |",
                f"| Health Score | {pack.health_score:.1f}% |",
                f"| Ready | {pack.ready_count} / {len(pack.items)} |",
                f"| Missing | {pack.missing_count} |",
                f"| Failed | {pack.failed_count} |",
                f"| Generated At | {pack.generated_at} |",
                f"",
                f"---",
                f"",
                f"## 二、Report Items",
                f"",
                f"| Report Type | Status | Size (bytes) | Path |",
                f"|-------------|--------|-------------|------|",
            ]
            for item in pack.items:
                rel_path = os.path.relpath(item.path, BASE_DIR) if item.path else "—"
                lines.append(
                    f"| {item.report_type} | {item.status} | {item.size_bytes} | `{rel_path}` |"
                )
            lines += [
                f"",
                f"---",
                f"",
                f"## 三、Missing Reports",
                f"",
            ]
            missing_items = [i for i in pack.items if i.status != STATUS_READY]
            if missing_items:
                for item in missing_items:
                    lines.append(f"- **{item.report_type}** — {item.status}: {item.notes or item.error or 'No output found'}")
            else:
                lines.append("All reports are READY.")
            lines += [
                f"",
                f"---",
                f"",
                f"*TW Quant Cockpit v0.5.4 — Research Only — Not Investment Advice*",
            ]
            path = os.path.join(pack.output_dir, "index.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            logger.info("ReportPackBuilder: index.md → %s", path)
            return path
        except Exception as exc:
            logger.warning("ReportPackBuilder._write_index() failed: %s", exc)
            return ""

    def _write_manifest(self, pack: ReportPack) -> str:
        """Write manifest.json to the pack output directory."""
        try:
            manifest = {
                "version":          "v0.5.4",
                "pack_type":        pack.pack_type,
                "report_date":      pack.report_date,
                "status":           pack.status,
                "health_score":     pack.health_score,
                "ready_count":      pack.ready_count,
                "missing_count":    pack.missing_count,
                "failed_count":     pack.failed_count,
                "generated_at":     pack.generated_at,
                "output_dir":       pack.output_dir,
                "safety": {
                    "research_only":      True,
                    "no_real_orders":     True,
                    "production_blocked": True,
                },
                "items": [i.to_dict() for i in pack.items],
            }
            path = os.path.join(pack.output_dir, "manifest.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            logger.info("ReportPackBuilder: manifest.json → %s", path)
            return path
        except Exception as exc:
            logger.warning("ReportPackBuilder._write_manifest() failed: %s", exc)
            return ""
