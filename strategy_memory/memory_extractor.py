"""
memory_extractor.py — Strategy Research Memory Extractor v0.7.2

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations
import os
import json
import csv
import glob
from typing import List
from datetime import datetime

from strategy_memory.strategy_memory_schema import (
    StrategyMemoryItem,
    MEMORY_TYPE_STRATEGY_HYPOTHESIS, MEMORY_TYPE_RULE_CANDIDATE,
    MEMORY_TYPE_REPLAY_MISTAKE_PATTERN, MEMORY_TYPE_JOURNAL_PATTERN,
    MEMORY_TYPE_DATA_GAP, MEMORY_TYPE_REPORT_GAP,
    MEMORY_TYPE_REGRESSION_RISK, MEMORY_TYPE_PROVIDER_LIMITATION,
    MEMORY_TYPE_RESEARCH_CONCLUSION, MEMORY_TYPE_FOLLOW_UP_TASK,
    STATUS_NEW, PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    SOURCE_RESEARCH_INTELLIGENCE, SOURCE_STRATEGY_KNOWLEDGE,
    SOURCE_RULE_GOVERNANCE, SOURCE_REPLAY_TRAINING,
    SOURCE_PORTFOLIO_JOURNAL, SOURCE_DATA_COVERAGE, SOURCE_REPORT_PACK,
)

import logging
logger = logging.getLogger(__name__)


class StrategyMemoryExtractor:
    """
    Extracts strategy memory candidates from Research OS module outputs.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, project_root: str = "."):
        self._root = project_root
        self._ri_dir   = os.path.join(project_root, "data", "backtest_results", "research_intelligence")
        self._sk_dir   = os.path.join(project_root, "data", "backtest_results", "strategy_knowledge")
        self._rg_dir   = os.path.join(project_root, "data", "backtest_results", "rule_governance")
        self._rt_dir   = os.path.join(project_root, "data", "backtest_results", "replay_training")
        self._pj_dir   = os.path.join(project_root, "data", "backtest_results", "portfolio_journal")
        self._dc_dir   = os.path.join(project_root, "data", "backtest_results", "data_coverage")
        self._rp_dir   = os.path.join(project_root, "data", "backtest_results", "report_pack")

    def _make_item(self, **kwargs) -> StrategyMemoryItem:
        """Create a StrategyMemoryItem safely, filtering forbidden kwargs."""
        valid_fields = StrategyMemoryItem.__dataclass_fields__.keys()
        safe_kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}
        try:
            return StrategyMemoryItem(**safe_kwargs)
        except Exception as exc:
            logger.warning("StrategyMemoryExtractor._make_item failed: %s", exc)
            return StrategyMemoryItem(
                title=safe_kwargs.get("title", "Untitled"),
                memory_type=safe_kwargs.get("memory_type", MEMORY_TYPE_FOLLOW_UP_TASK),
                source_module=safe_kwargs.get("source_module", SOURCE_RESEARCH_INTELLIGENCE),
            )

    def extract_all(self, mode: str = "real") -> List[StrategyMemoryItem]:
        """Extract memory candidates from all sources."""
        items: List[StrategyMemoryItem] = []
        for extractor in [
            self.extract_from_research_intelligence,
            self.extract_from_strategy_knowledge,
            self.extract_from_rule_governance,
            self.extract_from_replay_training,
            self.extract_from_portfolio_journal,
            self.extract_from_data_coverage,
            self.extract_from_report_pack,
        ]:
            try:
                items.extend(extractor())
            except Exception as exc:
                logger.warning("StrategyMemoryExtractor: extractor %s failed: %s",
                               extractor.__name__, exc)
        return items

    def extract_from_research_intelligence(self) -> List[StrategyMemoryItem]:
        """Extract from research_intelligence outputs."""
        items: List[StrategyMemoryItem] = []
        if not os.path.isdir(self._ri_dir):
            return items

        # Try recommendations CSV first
        rec_files = glob.glob(os.path.join(self._ri_dir, "research_intelligence_recommendations*.csv"))
        for path in rec_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            cat = row.get("category", "")
                            pri = row.get("priority", "P2")
                            title = row.get("title", "")
                            rationale = row.get("rationale", "") or row.get("why_now", "")
                            cmds = row.get("suggested_commands", "")

                            # Map category to memory_type
                            if cat in ("DATA_GAP", "data_gap"):
                                mtype = MEMORY_TYPE_DATA_GAP
                            elif cat in ("REPORT_GAP", "report_gap"):
                                mtype = MEMORY_TYPE_REPORT_GAP
                            elif cat in ("REPLAY_MISTAKE", "replay_mistake"):
                                mtype = MEMORY_TYPE_REPLAY_MISTAKE_PATTERN
                            elif cat in ("RULE_REVIEW", "rule_review"):
                                mtype = MEMORY_TYPE_RULE_CANDIDATE
                            elif "strategy" in cat.lower():
                                mtype = MEMORY_TYPE_STRATEGY_HYPOTHESIS
                            elif pri in ("P0", "P1"):
                                mtype = MEMORY_TYPE_FOLLOW_UP_TASK
                            else:
                                mtype = MEMORY_TYPE_FOLLOW_UP_TASK

                            if not title:
                                continue

                            priority = PRIORITY_P0 if pri == "P0" else (
                                PRIORITY_P1 if pri == "P1" else (
                                    PRIORITY_P2 if pri == "P2" else PRIORITY_P3
                                )
                            )
                            suggested = [c for c in (cmds or "").split("|") if c.strip()]

                            items.append(self._make_item(
                                memory_type=mtype,
                                title=title[:200],
                                summary=rationale[:300] if rationale else "",
                                priority=priority,
                                source_module=SOURCE_RESEARCH_INTELLIGENCE,
                                suggested_commands=suggested[:3],
                            ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("RI recommendations file error %s: %s", path, exc)

        # Try summary JSON
        summary_files = glob.glob(os.path.join(self._ri_dir, "research_intelligence_summary*.json"))
        for path in summary_files:
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                top_p0 = data.get("top_p0_title") or data.get("top_priority", "")
                if top_p0:
                    items.append(self._make_item(
                        memory_type=MEMORY_TYPE_FOLLOW_UP_TASK,
                        title=str(top_p0)[:200],
                        summary="From research intelligence summary (P0)",
                        priority=PRIORITY_P0,
                        source_module=SOURCE_RESEARCH_INTELLIGENCE,
                    ))
            except Exception as exc:
                logger.debug("RI summary JSON error %s: %s", path, exc)

        return items

    def extract_from_strategy_knowledge(self) -> List[StrategyMemoryItem]:
        """Extract from strategy_knowledge outputs."""
        items: List[StrategyMemoryItem] = []
        if not os.path.isdir(self._sk_dir):
            return items

        for path in glob.glob(os.path.join(self._sk_dir, "*.csv")):
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            item_type = row.get("item_type", "") or row.get("type", "")
                            title = row.get("title", "") or row.get("name", "")
                            if not title:
                                continue
                            if "rule" in item_type.lower():
                                mtype = MEMORY_TYPE_RULE_CANDIDATE
                            else:
                                mtype = MEMORY_TYPE_STRATEGY_HYPOTHESIS
                            items.append(self._make_item(
                                memory_type=mtype,
                                title=title[:200],
                                summary=row.get("summary", "") or row.get("description", ""),
                                priority=PRIORITY_P2,
                                source_module=SOURCE_STRATEGY_KNOWLEDGE,
                                evidence=row.get("evidence", "") or row.get("source", ""),
                            ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("SK file error %s: %s", path, exc)

        for path in glob.glob(os.path.join(self._sk_dir, "*.json")):
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        title = item.get("title", "") or item.get("name", "")
                        if not title:
                            continue
                        items.append(self._make_item(
                            memory_type=MEMORY_TYPE_STRATEGY_HYPOTHESIS,
                            title=str(title)[:200],
                            summary=str(item.get("summary", ""))[:300],
                            priority=PRIORITY_P2,
                            source_module=SOURCE_STRATEGY_KNOWLEDGE,
                        ))
            except Exception as exc:
                logger.debug("SK JSON file error %s: %s", path, exc)

        return items

    def extract_from_rule_governance(self) -> List[StrategyMemoryItem]:
        """Extract from rule_governance outputs."""
        items: List[StrategyMemoryItem] = []
        if not os.path.isdir(self._rg_dir):
            return items

        for path in glob.glob(os.path.join(self._rg_dir, "*.csv")):
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            rule_name = row.get("rule_name", "") or row.get("name", "")
                            if not rule_name:
                                continue
                            confidence = float(row.get("confidence", 0.5) or 0.5)
                            status_val = row.get("status", "") or row.get("governance_status", "")
                            if "deprecated" in str(status_val).lower():
                                mtype = MEMORY_TYPE_REGRESSION_RISK
                                priority = PRIORITY_P1
                            elif confidence < 0.4:
                                mtype = MEMORY_TYPE_RULE_CANDIDATE
                                priority = PRIORITY_P1
                            else:
                                mtype = MEMORY_TYPE_RULE_CANDIDATE
                                priority = PRIORITY_P2
                            items.append(self._make_item(
                                memory_type=mtype,
                                title=f"Rule governance: {rule_name}"[:200],
                                summary=f"Confidence={confidence:.2f}, Status={status_val}",
                                priority=priority,
                                source_module=SOURCE_RULE_GOVERNANCE,
                                related_rules=[rule_name],
                                confidence=confidence,
                            ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("RG file error %s: %s", path, exc)

        return items

    def extract_from_replay_training(self) -> List[StrategyMemoryItem]:
        """Extract from replay_training outputs."""
        items: List[StrategyMemoryItem] = []
        if not os.path.isdir(self._rt_dir):
            return items

        score_files = glob.glob(os.path.join(self._rt_dir, "replay_scores*.csv"))
        for path in score_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    mistake_counts: dict = {}
                    low_scores = []
                    for row in reader:
                        try:
                            mistake = row.get("mistake_type", "") or row.get("mistake", "")
                            score = float(row.get("score", 0) or 0)
                            session = row.get("session_id", "")
                            if mistake:
                                mistake_counts[mistake] = mistake_counts.get(mistake, 0) + 1
                            if score < 50:
                                low_scores.append((session, score))
                        except Exception:
                            pass

                    for mistake, count in mistake_counts.items():
                        if count >= 2:
                            items.append(self._make_item(
                                memory_type=MEMORY_TYPE_REPLAY_MISTAKE_PATTERN,
                                title=f"Repeated replay mistake: {mistake}"[:200],
                                summary=f"Seen {count} times in replay sessions",
                                priority=PRIORITY_P1 if count >= 3 else PRIORITY_P2,
                                source_module=SOURCE_REPLAY_TRAINING,
                                evidence=f"count={count}",
                            ))

                    if low_scores:
                        items.append(self._make_item(
                            memory_type=MEMORY_TYPE_FOLLOW_UP_TASK,
                            title="Low replay training scores detected",
                            summary=f"{len(low_scores)} sessions with score < 50",
                            priority=PRIORITY_P1,
                            source_module=SOURCE_REPLAY_TRAINING,
                            suggested_commands=["python main.py replay-training-drills"],
                        ))
            except Exception as exc:
                logger.debug("RT scores file error %s: %s", path, exc)

        return items

    def extract_from_portfolio_journal(self) -> List[StrategyMemoryItem]:
        """Extract from portfolio_journal outputs."""
        items: List[StrategyMemoryItem] = []
        if not os.path.isdir(self._pj_dir):
            return items

        journal_files = glob.glob(os.path.join(self._pj_dir, "*.csv"))
        for path in journal_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    mistake_counts: dict = {}
                    for row in reader:
                        try:
                            mistake = row.get("mistake_type", "") or row.get("mistake_tag", "")
                            if mistake:
                                mistake_counts[mistake] = mistake_counts.get(mistake, 0) + 1
                        except Exception:
                            pass

                    for mistake, count in mistake_counts.items():
                        if count >= 2:
                            items.append(self._make_item(
                                memory_type=MEMORY_TYPE_JOURNAL_PATTERN,
                                title=f"Recurring journal pattern: {mistake}"[:200],
                                summary=f"This mistake appears {count} times in the journal",
                                priority=PRIORITY_P1 if count >= 3 else PRIORITY_P2,
                                source_module=SOURCE_PORTFOLIO_JOURNAL,
                                evidence=f"journal_count={count}",
                            ))
            except Exception as exc:
                logger.debug("PJ file error %s: %s", path, exc)

        return items

    def extract_from_data_coverage(self) -> List[StrategyMemoryItem]:
        """Extract from data_coverage outputs."""
        items: List[StrategyMemoryItem] = []
        if not os.path.isdir(self._dc_dir):
            return items

        coverage_files = glob.glob(os.path.join(self._dc_dir, "data_coverage_items*.csv"))
        for path in coverage_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            item_id = row.get("item_id", "") or row.get("dataset_name", "")
                            status_val = row.get("status", "")
                            env_limited = str(row.get("environment_limited", "")).lower() in ("true", "1", "yes")
                            required = str(row.get("required", "")).lower() in ("true", "1", "yes")
                            cmd = row.get("suggested_command", "")

                            if not item_id:
                                continue

                            if status_val in ("MISSING_REQUIRED", "MISSING") and required:
                                items.append(self._make_item(
                                    memory_type=MEMORY_TYPE_DATA_GAP,
                                    title=f"Data gap: {item_id}"[:200],
                                    summary=f"Required data item missing: {item_id}",
                                    priority=PRIORITY_P1,
                                    source_module=SOURCE_DATA_COVERAGE,
                                    suggested_commands=[cmd] if cmd else [],
                                ))
                            elif env_limited:
                                items.append(self._make_item(
                                    memory_type=MEMORY_TYPE_PROVIDER_LIMITATION,
                                    title=f"Provider limitation: {item_id}"[:200],
                                    summary=f"Data item is environment-limited: {item_id}",
                                    priority=PRIORITY_P2,
                                    source_module=SOURCE_DATA_COVERAGE,
                                    suggested_commands=[cmd] if cmd else [],
                                ))
                            elif status_val in ("NOT_GENERATED",):
                                items.append(self._make_item(
                                    memory_type=MEMORY_TYPE_FOLLOW_UP_TASK,
                                    title=f"Not yet generated: {item_id}"[:200],
                                    summary=f"Coverage item not yet generated: {item_id}",
                                    priority=PRIORITY_P3,
                                    source_module=SOURCE_DATA_COVERAGE,
                                    suggested_commands=[cmd] if cmd else [],
                                ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("DC file error %s: %s", path, exc)

        return items

    def extract_from_report_pack(self) -> List[StrategyMemoryItem]:
        """Extract from report_pack outputs."""
        items: List[StrategyMemoryItem] = []
        if not os.path.isdir(self._rp_dir):
            return items

        pack_files = glob.glob(os.path.join(self._rp_dir, "*.csv"))
        for path in pack_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            report_type = row.get("report_type", "")
                            status_val = row.get("status", "")
                            if not report_type:
                                continue
                            if status_val in ("MISSING_REQUIRED", "MISSING"):
                                items.append(self._make_item(
                                    memory_type=MEMORY_TYPE_REPORT_GAP,
                                    title=f"Report gap: {report_type}"[:200],
                                    summary=f"Required report type missing: {report_type}",
                                    priority=PRIORITY_P1,
                                    source_module=SOURCE_REPORT_PACK,
                                    suggested_commands=[f"python main.py report-pack --type full"],
                                ))
                            elif status_val in ("NOT_GENERATED", "MISSING_OPTIONAL"):
                                items.append(self._make_item(
                                    memory_type=MEMORY_TYPE_FOLLOW_UP_TASK,
                                    title=f"Optional report not generated: {report_type}"[:200],
                                    summary=f"Optional report type not yet generated: {report_type}",
                                    priority=PRIORITY_P3,
                                    source_module=SOURCE_REPORT_PACK,
                                ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("RP file error %s: %s", path, exc)

        return items
