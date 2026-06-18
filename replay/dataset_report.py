"""
replay/dataset_report.py — ReplayDatasetReport v1.2.8

Generates markdown reports for dataset registry state.

[!] Research Only. No Real Orders. Dataset Registry Only. No Broker.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

NO_REAL_ORDERS = True
RESEARCH_ONLY = True


def _now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


class ReplayDatasetReport:
    """
    Generates dataset registry markdown reports.

    [!] Research Only. No Real Orders. Not Investment Advice.
    """

    RESEARCH_ONLY  = True
    NO_REAL_ORDERS = True

    def __init__(self, registry=None):
        self._registry = registry

    def generate(self) -> str:
        today = _now_date()
        datasets = self._registry.list_datasets() if self._registry else []
        lines = [
            f"# Replay Dataset Registry Report v1.2.8",
            f"",
            f"**Date:** {today}  ",
            f"**Research Only. No Real Orders. Not Investment Advice.**",
            f"",
            f"---",
            f"",
            f"## 一、Overview",
            f"",
            f"- Total datasets: {len(datasets)}",
            f"- REAL: {sum(1 for d in datasets if d.mode == 'REAL')}",
            f"- MOCK: {sum(1 for d in datasets if d.mode == 'MOCK')}",
            f"",
            f"## 二、Datasets",
            f"",
        ]
        if not datasets:
            lines.append("*(no datasets registered)*")
        else:
            lines.append("| ID | Version | Mode | Qualification | Status | Symbols | Frozen |")
            lines.append("|----|---------|------|---------------|--------|---------|--------|")
            for d in datasets:
                frozen = "Yes" if d.frozen_at else "No"
                syms = ",".join(d.symbols[:3])
                lines.append(
                    f"| {d.dataset_id} | {d.dataset_version} | {d.mode} "
                    f"| {d.qualification} | {d.status} | {syms} | {frozen} |"
                )
        lines += [
            f"",
            f"## 三、Versions",
            f"",
            f"*(version history stored in data/replay_registry/dataset_versions.jsonl)*",
            f"",
            f"## 四、Qualification",
            f"",
            f"- VERIFIED_REAL: point-in-time verified real data",
            f"- REAL_UNVERIFIED: real data without PIT verification",
            f"- MOCK_DEMO_ONLY: demo/mock data — training use only",
            f"- INSUFFICIENT: too few rows or missing coverage",
            f"- BLOCKED: missing required files or mock contamination",
            f"- INCOMPATIBLE: schema mismatch",
            f"",
            f"## 五、Coverage",
            f"",
            f"*(see per-dataset details for symbol/timeframe/field coverage)*",
            f"",
            f"## 六、Fingerprints",
            f"",
            f"- Fingerprints are deterministic and path-independent.",
            f"- Same content on two machines => same fingerprint.",
            f"",
            f"## 七、Lineage",
            f"",
            f"*(lineage stored in data/replay_registry/dataset_lineage.jsonl)*",
            f"",
            f"## 八、Integrity",
            f"",
            f"- MISSING: required file not found => BLOCKED",
            f"- CORRUPTED: hash mismatch",
            f"- INCOMPATIBLE: schema mismatch",
            f"",
            f"## 九、Frozen Datasets",
            f"",
            f"- Frozen: {sum(1 for d in datasets if d.frozen_at)}",
            f"",
            f"## 十、Missing / Corrupted",
            f"",
            f"- Missing: {sum(1 for d in datasets if d.status == 'MISSING')}",
            f"- Corrupted: {sum(1 for d in datasets if d.status == 'CORRUPTED')}",
            f"",
            f"## 十一、Portability",
            f"",
            f"- All portable packages use RELATIVE_ONLY paths.",
            f"- No absolute paths, secrets, .env, broker credentials.",
            f"",
            f"## 十二、Limitations",
            f"",
            f"- This registry records metadata only, not raw data.",
            f"- PIT verification must be done separately.",
            f"",
            f"## 十三、安全聲明",
            f"",
            f"**Dataset Registry Only. No Real Orders. No Broker.**  ",
            f"**Registry operations do not execute trades.**  ",
            f"**Not Investment Advice.**",
        ]
        return "\n".join(lines)
