"""
backtest_coach/backtest_signal_extractor.py — BacktestSignalExtractor v0.7.3

Extracts backtest weakness signals from all Research OS module outputs.

[!] Research Only. No Real Orders. Production Trading BLOCKED.
"""
from __future__ import annotations

import csv
import glob
import json
import logging
import os
import uuid
from datetime import datetime
from typing import List

from backtest_coach.backtest_coach_schema import (
    BacktestCoachSignal,
    ISSUE_LOW_WIN_RATE, ISSUE_HIGH_DRAWDOWN, ISSUE_POOR_RISK_REWARD,
    ISSUE_OVERTRADING, ISSUE_SAMPLE_TOO_SMALL, ISSUE_DATA_INSUFFICIENT,
    ISSUE_RULE_LOW_CONFIDENCE, ISSUE_JOURNAL_REPEAT_MISTAKE,
    ISSUE_REPLAY_SCORE_LOW, ISSUE_FAKE_BREAKOUT, ISSUE_STOP_LOSS_DISCIPLINE,
    SEV_CRITICAL, SEV_HIGH, SEV_MEDIUM, SEV_LOW,
    PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3,
    SRC_BACKTEST, SRC_STRATEGY_MEMORY, SRC_REPLAY_TRAINING,
    SRC_PORTFOLIO_JOURNAL, SRC_RESEARCH_INTELLIGENCE,
    SRC_RULE_GOVERNANCE, SRC_DATA_COVERAGE,
)

logger = logging.getLogger(__name__)


class BacktestSignalExtractor:
    """
    Extracts backtest weakness signals from Research OS module outputs.

    [!] Research Only. No Real Orders. Production Trading BLOCKED.
    [!] Does NOT modify any data, strategies, or rules.
    """

    read_only          = True
    no_real_orders     = True
    production_blocked = True

    def __init__(self, project_root: str = "."):
        self._root   = project_root
        self._bt_dir = os.path.join(project_root, "data", "backtest_results")
        self._sm_dir = os.path.join(project_root, "data", "backtest_results", "strategy_memory")
        self._rt_dir = os.path.join(project_root, "data", "backtest_results", "replay_training")
        self._pj_dir = os.path.join(project_root, "data", "backtest_results", "portfolio_journal")
        self._ri_dir = os.path.join(project_root, "data", "backtest_results", "research_intelligence")
        self._rg_dir = os.path.join(project_root, "data", "backtest_results", "rule_governance")
        self._dc_dir = os.path.join(project_root, "data", "backtest_results", "data_coverage")

    def _make_signal(self, **kwargs) -> BacktestCoachSignal:
        """Create a BacktestCoachSignal safely."""
        valid_fields = BacktestCoachSignal.__dataclass_fields__.keys()
        safe_kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}
        try:
            return BacktestCoachSignal(**safe_kwargs)
        except Exception as exc:
            logger.warning("BacktestSignalExtractor._make_signal failed: %s", exc)
            return BacktestCoachSignal(
                source_module=safe_kwargs.get("source_module", SRC_BACKTEST),
                issue_type=safe_kwargs.get("issue_type", ISSUE_LOW_WIN_RATE),
                description=safe_kwargs.get("description", "Signal extraction error")[:200],
            )

    def extract_all(self, mode: str = "real") -> List[BacktestCoachSignal]:
        """Extract signals from all sources. Returns combined list."""
        signals: List[BacktestCoachSignal] = []
        extractors = [
            self.extract_from_backtest_results,
            self.extract_from_strategy_memory,
            self.extract_from_replay_training,
            self.extract_from_portfolio_journal,
            self.extract_from_research_intelligence,
            self.extract_from_rule_governance,
            self.extract_from_data_coverage,
        ]
        for extractor in extractors:
            try:
                signals.extend(extractor())
            except Exception as exc:
                logger.warning("BacktestSignalExtractor: %s failed: %s", extractor.__name__, exc)
        return signals

    def extract_from_backtest_results(self) -> List[BacktestCoachSignal]:
        """Scan data/backtest_results/ for CSV/JSON backtest summary files."""
        signals: List[BacktestCoachSignal] = []
        if not os.path.isdir(self._bt_dir):
            return signals

        # Try common backtest summary file patterns
        patterns = [
            os.path.join(self._bt_dir, "hardened_backtest_summary*.csv"),
            os.path.join(self._bt_dir, "backtest_summary*.csv"),
            os.path.join(self._bt_dir, "backtest_results*.csv"),
            os.path.join(self._bt_dir, "hardened_backtest*.csv"),
        ]

        for pattern in patterns:
            for path in glob.glob(pattern):
                try:
                    with open(path, newline="", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            try:
                                strategy = row.get("strategy_name", "") or row.get("strategy", "")
                                symbol   = row.get("symbol", "") or row.get("stock", "")

                                # win rate
                                wr_raw = row.get("win_rate", "") or row.get("winning_rate", "")
                                if wr_raw:
                                    try:
                                        wr = float(wr_raw)
                                        if wr < 0.45:
                                            signals.append(self._make_signal(
                                                source_module=SRC_BACKTEST,
                                                issue_type=ISSUE_LOW_WIN_RATE,
                                                severity=SEV_HIGH,
                                                priority=PRIORITY_P1,
                                                strategy_name=strategy,
                                                symbol=symbol,
                                                metric_name="win_rate",
                                                metric_value=wr,
                                                threshold=0.45,
                                                description=f"Win rate {wr:.1%} below threshold 45%",
                                                evidence=f"win_rate={wr:.3f}",
                                                suggested_action="Run more backtests to validate strategy edge",
                                                suggested_command="python main.py backtest-hardened --mode real",
                                            ))
                                    except (ValueError, TypeError):
                                        pass

                                # max drawdown
                                dd_raw = row.get("max_drawdown", "") or row.get("max_dd", "")
                                if dd_raw:
                                    try:
                                        dd = float(dd_raw)
                                        if dd > 0.15:
                                            signals.append(self._make_signal(
                                                source_module=SRC_BACKTEST,
                                                issue_type=ISSUE_HIGH_DRAWDOWN,
                                                severity=SEV_HIGH,
                                                priority=PRIORITY_P1,
                                                strategy_name=strategy,
                                                symbol=symbol,
                                                metric_name="max_drawdown",
                                                metric_value=dd,
                                                threshold=0.15,
                                                description=f"Max drawdown {dd:.1%} exceeds threshold 15%",
                                                evidence=f"max_drawdown={dd:.3f}",
                                                suggested_action="Review risk rules and position sizing",
                                                suggested_command="python main.py rule-governance --mode real --snapshot",
                                            ))
                                    except (ValueError, TypeError):
                                        pass

                                # reward/risk
                                rr_raw = row.get("avg_reward_risk", "") or row.get("reward_risk", "")
                                if rr_raw:
                                    try:
                                        rr = float(rr_raw)
                                        if rr < 1.2:
                                            signals.append(self._make_signal(
                                                source_module=SRC_BACKTEST,
                                                issue_type=ISSUE_POOR_RISK_REWARD,
                                                severity=SEV_MEDIUM,
                                                priority=PRIORITY_P1,
                                                strategy_name=strategy,
                                                symbol=symbol,
                                                metric_name="avg_reward_risk",
                                                metric_value=rr,
                                                threshold=1.2,
                                                description=f"Avg reward/risk {rr:.2f} below threshold 1.2",
                                                evidence=f"avg_reward_risk={rr:.3f}",
                                                suggested_action="Review exit rules to improve reward/risk",
                                                suggested_command="python main.py rule-governance --mode real",
                                            ))
                                    except (ValueError, TypeError):
                                        pass

                                # sample size
                                tc_raw = row.get("trade_count", "") or row.get("total_trades", "")
                                if tc_raw:
                                    try:
                                        tc = int(float(tc_raw))
                                        if tc < 30:
                                            signals.append(self._make_signal(
                                                source_module=SRC_BACKTEST,
                                                issue_type=ISSUE_SAMPLE_TOO_SMALL,
                                                severity=SEV_MEDIUM,
                                                priority=PRIORITY_P2,
                                                strategy_name=strategy,
                                                symbol=symbol,
                                                metric_name="trade_count",
                                                metric_value=float(tc),
                                                threshold=30.0,
                                                description=f"Sample too small: {tc} trades (need >= 30)",
                                                evidence=f"trade_count={tc}",
                                                suggested_action="Run backtest over longer period",
                                                suggested_command="python main.py backtest-hardened --mode real",
                                            ))
                                    except (ValueError, TypeError):
                                        pass

                            except Exception:
                                pass
                except Exception as exc:
                    logger.debug("BacktestSignalExtractor backtest file %s: %s", path, exc)

        return signals

    def extract_from_strategy_memory(self) -> List[BacktestCoachSignal]:
        """Extract signals from strategy_memory outputs."""
        signals: List[BacktestCoachSignal] = []
        if not os.path.isdir(self._sm_dir):
            return signals

        mem_files = glob.glob(os.path.join(self._sm_dir, "strategy_memory_items*.csv"))
        mem_files += glob.glob(os.path.join(self._sm_dir, "strategy_memories.csv"))

        for path in mem_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            mtype  = row.get("memory_type", "")
                            status = row.get("status", "")
                            title  = row.get("title", "")
                            if not title:
                                continue

                            if mtype == "RULE_CANDIDATE" and status == "NEEDS_MORE_EVIDENCE":
                                signals.append(self._make_signal(
                                    source_module=SRC_STRATEGY_MEMORY,
                                    issue_type=ISSUE_SAMPLE_TOO_SMALL,
                                    severity=SEV_MEDIUM,
                                    priority=PRIORITY_P2,
                                    description=f"Rule candidate needs more evidence: {title[:100]}",
                                    evidence=f"memory_type={mtype}, status={status}",
                                    suggested_action="Run more backtests for this rule candidate",
                                    suggested_command="python main.py backtest-hardened --mode real",
                                ))
                            elif mtype == "REPLAY_MISTAKE_PATTERN":
                                signals.append(self._make_signal(
                                    source_module=SRC_STRATEGY_MEMORY,
                                    issue_type=ISSUE_REPLAY_SCORE_LOW,
                                    severity=SEV_MEDIUM,
                                    priority=PRIORITY_P2,
                                    description=f"Replay mistake pattern: {title[:100]}",
                                    evidence=f"memory_type={mtype}",
                                    suggested_action="Practice replay drill to address mistake pattern",
                                    suggested_command="python main.py replay-training-drills --session-id latest",
                                ))
                            elif mtype == "DATA_GAP":
                                signals.append(self._make_signal(
                                    source_module=SRC_STRATEGY_MEMORY,
                                    issue_type=ISSUE_DATA_INSUFFICIENT,
                                    severity=SEV_MEDIUM,
                                    priority=PRIORITY_P2,
                                    description=f"Data gap in memory: {title[:100]}",
                                    evidence=f"memory_type={mtype}",
                                    suggested_action="Fix data coverage gap",
                                    suggested_command="python main.py data-coverage --mode real",
                                ))
                            elif mtype == "JOURNAL_PATTERN":
                                signals.append(self._make_signal(
                                    source_module=SRC_STRATEGY_MEMORY,
                                    issue_type=ISSUE_JOURNAL_REPEAT_MISTAKE,
                                    severity=SEV_LOW,
                                    priority=PRIORITY_P3,
                                    description=f"Journal pattern in memory: {title[:100]}",
                                    evidence=f"memory_type={mtype}",
                                    suggested_action="Review journal for recurring patterns",
                                    suggested_command="python main.py strategy-memory-list --memory-type JOURNAL_PATTERN",
                                ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("BacktestSignalExtractor strategy_memory %s: %s", path, exc)

        return signals

    def extract_from_replay_training(self) -> List[BacktestCoachSignal]:
        """Extract signals from replay_training outputs."""
        signals: List[BacktestCoachSignal] = []
        if not os.path.isdir(self._rt_dir):
            return signals

        # Check replay score files
        score_files = glob.glob(os.path.join(self._rt_dir, "replay_scores*.csv"))
        score_files += glob.glob(os.path.join(self._rt_dir, "replay_training_summary*.csv"))

        for path in score_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            session_id = row.get("session_id", "") or row.get("latest_session_id", "")
                            score_raw  = row.get("score", "") or row.get("latest_score", "")
                            symbol     = row.get("symbol", "") or row.get("latest_symbol", "")
                            mistake    = row.get("mistake_type", "") or row.get("mistake", "")

                            if score_raw:
                                try:
                                    score = float(score_raw)
                                    if score < 60:
                                        signals.append(self._make_signal(
                                            source_module=SRC_REPLAY_TRAINING,
                                            issue_type=ISSUE_REPLAY_SCORE_LOW,
                                            severity=SEV_MEDIUM,
                                            priority=PRIORITY_P1,
                                            symbol=symbol,
                                            metric_name="replay_score",
                                            metric_value=score,
                                            threshold=60.0,
                                            description=f"Replay score {score:.0f} below threshold 60",
                                            evidence=f"session_id={session_id}, score={score:.1f}",
                                            suggested_action="Practice replay drills to improve score",
                                            suggested_command="python main.py replay-training-drills --session-id latest",
                                        ))
                                except (ValueError, TypeError):
                                    pass

                            if mistake:
                                if "fake" in mistake.lower() or "breakout" in mistake.lower():
                                    signals.append(self._make_signal(
                                        source_module=SRC_REPLAY_TRAINING,
                                        issue_type=ISSUE_FAKE_BREAKOUT,
                                        severity=SEV_HIGH,
                                        priority=PRIORITY_P1,
                                        symbol=symbol,
                                        description=f"Fake breakout mistake: {mistake[:80]}",
                                        evidence=f"session={session_id}, mistake={mistake}",
                                        suggested_action="Practice fake breakout recognition drill",
                                        suggested_command="python main.py replay-training-drills --session-id latest",
                                    ))
                                elif "stop" in mistake.lower() or "loss" in mistake.lower():
                                    signals.append(self._make_signal(
                                        source_module=SRC_REPLAY_TRAINING,
                                        issue_type=ISSUE_STOP_LOSS_DISCIPLINE,
                                        severity=SEV_HIGH,
                                        priority=PRIORITY_P1,
                                        symbol=symbol,
                                        description=f"Stop loss discipline issue: {mistake[:80]}",
                                        evidence=f"session={session_id}, mistake={mistake}",
                                        suggested_action="Practice stop loss discipline drill",
                                        suggested_command="python main.py replay-training-drills --session-id latest",
                                    ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("BacktestSignalExtractor replay_training %s: %s", path, exc)

        # Check for drill files
        drill_files = glob.glob(os.path.join(self._rt_dir, "*drill*.csv"))
        for path in drill_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    count = sum(1 for _ in reader)
                    if count > 0:
                        signals.append(self._make_signal(
                            source_module=SRC_REPLAY_TRAINING,
                            issue_type=ISSUE_REPLAY_SCORE_LOW,
                            severity=SEV_LOW,
                            priority=PRIORITY_P3,
                            description=f"Replay drills available ({count} records)",
                            evidence=f"drill_file={os.path.basename(path)}",
                            suggested_action="Complete replay training drills",
                            suggested_command="python main.py replay-training-drills --session-id latest",
                        ))
            except Exception as exc:
                logger.debug("BacktestSignalExtractor drill file %s: %s", path, exc)

        return signals

    def extract_from_portfolio_journal(self) -> List[BacktestCoachSignal]:
        """Extract signals from portfolio_journal outputs."""
        signals: List[BacktestCoachSignal] = []
        if not os.path.isdir(self._pj_dir):
            return signals

        journal_files = glob.glob(os.path.join(self._pj_dir, "*.csv"))
        for path in journal_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    mistake_counts: dict = {}
                    low_process: int = 0

                    for row in reader:
                        try:
                            mistake = row.get("mistake_type", "") or row.get("mistake_tag", "")
                            if mistake:
                                mistake_counts[mistake] = mistake_counts.get(mistake, 0) + 1

                            pq_raw = row.get("process_quality", "") or row.get("quality_score", "")
                            if pq_raw:
                                try:
                                    pq = float(pq_raw)
                                    if pq < 60:
                                        low_process += 1
                                except (ValueError, TypeError):
                                    pass
                        except Exception:
                            pass

                    for mistake, count in mistake_counts.items():
                        if count >= 2:
                            sev = SEV_HIGH if count >= 3 else SEV_MEDIUM
                            pri = PRIORITY_P1 if count >= 3 else PRIORITY_P2
                            signals.append(self._make_signal(
                                source_module=SRC_PORTFOLIO_JOURNAL,
                                issue_type=ISSUE_JOURNAL_REPEAT_MISTAKE,
                                severity=sev,
                                priority=pri,
                                description=f"Recurring journal mistake: {mistake} (seen {count}x)",
                                evidence=f"journal_count={count}, mistake={mistake}",
                                suggested_action="Review journal to address recurring mistake",
                                suggested_command="python main.py strategy-memory-list --memory-type JOURNAL_PATTERN",
                            ))

                    if low_process >= 3:
                        signals.append(self._make_signal(
                            source_module=SRC_PORTFOLIO_JOURNAL,
                            issue_type=ISSUE_JOURNAL_REPEAT_MISTAKE,
                            severity=SEV_MEDIUM,
                            priority=PRIORITY_P2,
                            description=f"Low process quality in {low_process} journal entries",
                            evidence=f"low_process_count={low_process}",
                            suggested_action="Review journal process quality patterns",
                            suggested_command="python main.py strategy-memory-list --memory-type JOURNAL_PATTERN",
                        ))

            except Exception as exc:
                logger.debug("BacktestSignalExtractor portfolio_journal %s: %s", path, exc)

        return signals

    def extract_from_research_intelligence(self) -> List[BacktestCoachSignal]:
        """Extract signals from research_intelligence outputs."""
        signals: List[BacktestCoachSignal] = []
        if not os.path.isdir(self._ri_dir):
            return signals

        # Recommendations CSV
        rec_files = glob.glob(os.path.join(self._ri_dir, "research_intelligence_recommendations*.csv"))
        for path in rec_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            cat   = row.get("category", "")
                            pri   = row.get("priority", "P2")
                            title = row.get("title", "")
                            if not title:
                                continue

                            if cat in ("DATA_GAP", "data_gap") and pri in ("P0", "P1"):
                                signals.append(self._make_signal(
                                    source_module=SRC_RESEARCH_INTELLIGENCE,
                                    issue_type=ISSUE_DATA_INSUFFICIENT,
                                    severity=SEV_HIGH if pri == "P0" else SEV_MEDIUM,
                                    priority=PRIORITY_P0 if pri == "P0" else PRIORITY_P1,
                                    description=f"Data gap: {title[:100]}",
                                    evidence=f"category={cat}, priority={pri}",
                                    suggested_action="Fix data gap",
                                    suggested_command="python main.py data-coverage --mode real",
                                ))
                            elif cat in ("REPLAY_MISTAKE", "replay_mistake") and pri in ("P0", "P1"):
                                signals.append(self._make_signal(
                                    source_module=SRC_RESEARCH_INTELLIGENCE,
                                    issue_type=ISSUE_REPLAY_SCORE_LOW,
                                    severity=SEV_MEDIUM,
                                    priority=PRIORITY_P1,
                                    description=f"Replay issue: {title[:100]}",
                                    evidence=f"category={cat}, priority={pri}",
                                    suggested_action="Practice replay drill",
                                    suggested_command="python main.py replay-training-drills --session-id latest",
                                ))
                            elif cat in ("RULE_REVIEW", "rule_review"):
                                signals.append(self._make_signal(
                                    source_module=SRC_RESEARCH_INTELLIGENCE,
                                    issue_type=ISSUE_RULE_LOW_CONFIDENCE,
                                    severity=SEV_MEDIUM,
                                    priority=PRIORITY_P2,
                                    description=f"Rule review needed: {title[:100]}",
                                    evidence=f"category={cat}, priority={pri}",
                                    suggested_action="Review rule governance",
                                    suggested_command="python main.py rule-governance --mode real",
                                ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("BacktestSignalExtractor RI recommendations %s: %s", path, exc)

        # Summary JSON
        summary_files = glob.glob(os.path.join(self._ri_dir, "research_intelligence_summary*.json"))
        for path in summary_files:
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                data_gaps = data.get("data_gap_count", 0)
                if data_gaps and int(data_gaps) > 0:
                    signals.append(self._make_signal(
                        source_module=SRC_RESEARCH_INTELLIGENCE,
                        issue_type=ISSUE_DATA_INSUFFICIENT,
                        severity=SEV_MEDIUM,
                        priority=PRIORITY_P1,
                        metric_name="data_gap_count",
                        metric_value=float(data_gaps),
                        description=f"Research intelligence: {data_gaps} data gaps detected",
                        evidence=f"data_gap_count={data_gaps}",
                        suggested_action="Fix data gaps detected by research intelligence",
                        suggested_command="python main.py data-coverage --mode real",
                    ))
            except Exception as exc:
                logger.debug("BacktestSignalExtractor RI summary %s: %s", path, exc)

        return signals

    def extract_from_rule_governance(self) -> List[BacktestCoachSignal]:
        """Extract signals from rule_governance outputs."""
        signals: List[BacktestCoachSignal] = []
        if not os.path.isdir(self._rg_dir):
            return signals

        for path in glob.glob(os.path.join(self._rg_dir, "*.csv")):
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            rule_name  = row.get("rule_name", "") or row.get("name", "")
                            if not rule_name:
                                continue
                            conf_raw   = row.get("confidence", "") or row.get("confidence_score", "")
                            status_val = row.get("status", "") or row.get("governance_status", "")

                            if conf_raw:
                                try:
                                    conf = float(conf_raw)
                                    if conf < 0.4:
                                        signals.append(self._make_signal(
                                            source_module=SRC_RULE_GOVERNANCE,
                                            issue_type=ISSUE_RULE_LOW_CONFIDENCE,
                                            severity=SEV_HIGH,
                                            priority=PRIORITY_P1,
                                            metric_name="rule_confidence",
                                            metric_value=conf,
                                            threshold=0.4,
                                            description=f"Low confidence rule: {rule_name} ({conf:.2f})",
                                            evidence=f"rule={rule_name}, confidence={conf:.3f}",
                                            suggested_action="Review rule governance for low confidence rule",
                                            suggested_command="python main.py rule-governance --mode real --snapshot",
                                        ))
                                    elif conf < 0.6 and status_val.upper() in ("CANDIDATE", "EXPERIMENTAL"):
                                        signals.append(self._make_signal(
                                            source_module=SRC_RULE_GOVERNANCE,
                                            issue_type=ISSUE_SAMPLE_TOO_SMALL,
                                            severity=SEV_MEDIUM,
                                            priority=PRIORITY_P2,
                                            metric_name="rule_confidence",
                                            metric_value=conf,
                                            description=f"Rule candidate needs more backtest data: {rule_name}",
                                            evidence=f"rule={rule_name}, confidence={conf:.3f}, status={status_val}",
                                            suggested_action="Run backtest for this rule candidate",
                                            suggested_command="python main.py backtest-hardened --mode real",
                                        ))
                                except (ValueError, TypeError):
                                    pass
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("BacktestSignalExtractor rule_governance %s: %s", path, exc)

        return signals

    def extract_from_data_coverage(self) -> List[BacktestCoachSignal]:
        """Extract signals from data_coverage outputs."""
        signals: List[BacktestCoachSignal] = []
        if not os.path.isdir(self._dc_dir):
            return signals

        coverage_files = glob.glob(os.path.join(self._dc_dir, "data_coverage_items*.csv"))
        for path in coverage_files:
            try:
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            item_id    = row.get("item_id", "") or row.get("dataset_name", "")
                            status_val = row.get("status", "")
                            env_lim    = str(row.get("environment_limited", "")).lower() in ("true", "1", "yes")
                            required   = str(row.get("required", "")).lower() in ("true", "1", "yes")
                            cmd        = row.get("suggested_command", "")

                            if not item_id:
                                continue

                            if status_val in ("MISSING_REQUIRED", "MISSING") and required:
                                signals.append(self._make_signal(
                                    source_module=SRC_DATA_COVERAGE,
                                    issue_type=ISSUE_DATA_INSUFFICIENT,
                                    severity=SEV_HIGH,
                                    priority=PRIORITY_P1,
                                    description=f"Required data missing: {item_id}",
                                    evidence=f"item_id={item_id}, status={status_val}",
                                    suggested_action="Fix missing required data",
                                    suggested_command=cmd or "python main.py data-coverage --mode real",
                                ))
                            elif status_val in ("NOT_GENERATED",):
                                signals.append(self._make_signal(
                                    source_module=SRC_DATA_COVERAGE,
                                    issue_type=ISSUE_DATA_INSUFFICIENT,
                                    severity=SEV_LOW,
                                    priority=PRIORITY_P3,
                                    description=f"Data not yet generated: {item_id}",
                                    evidence=f"item_id={item_id}, status={status_val}",
                                    suggested_action="Generate missing data or read report",
                                    suggested_command=cmd or "python main.py data-coverage --mode real",
                                ))
                            elif env_lim:
                                signals.append(self._make_signal(
                                    source_module=SRC_DATA_COVERAGE,
                                    issue_type=ISSUE_DATA_INSUFFICIENT,
                                    severity=SEV_LOW,
                                    priority=PRIORITY_P3,
                                    description=f"Environment-limited data: {item_id}",
                                    evidence=f"item_id={item_id}, environment_limited=True",
                                    suggested_action="Wait for environment setup or use available data",
                                    suggested_command=cmd or "",
                                ))
                        except Exception:
                            pass
            except Exception as exc:
                logger.debug("BacktestSignalExtractor data_coverage %s: %s", path, exc)

        return signals
