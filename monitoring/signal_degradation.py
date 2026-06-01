"""
monitoring/signal_degradation.py — Signal Degradation Monitor for v0.4.3 Model Monitoring.

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Status thresholds
_STABLE_THRESHOLD   = 0.05   # <5% drop → STABLE
_WATCH_THRESHOLD    = 0.10   # 10% drop → WATCH
_DEGRADED_THRESHOLD = 0.20   # 20% drop → DEGRADED
_SEVERE_THRESHOLD   = 0.40   # 40% drop → SEVERE


class SignalDegradationMonitor:
    """
    Detect degradation in signal quality, rule confidence, and portfolio metrics.

    [!] Monitoring Only. Read Only. No Real Orders.
    No crash on missing files.
    """

    read_only      = True
    no_real_orders = True

    _SAFETY = {
        "research_only":      True,
        "no_real_orders":     True,
        "monitoring_only":    True,
        "production_blocked": True,
        "real_order_ready":   False,
    }

    def __init__(self, results_dir: str = "data/backtest_results"):
        if os.path.isabs(results_dir):
            self._results_dir = results_dir
        else:
            self._results_dir = os.path.join(_BASE_DIR, results_dir)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Load available data and run all degradation checks."""
        warnings: list = []

        rule_deg    = {}
        signal_deg  = {}
        port_deg    = {}

        try:
            rule_deg = self.detect_rule_degradation()
        except Exception as exc:
            logger.warning("SignalDegradationMonitor.detect_rule_degradation: %s", exc)
            warnings.append(f"rule_degradation error: {exc}")
            rule_deg = {"status": "INSUFFICIENT_DATA", "note": str(exc)}

        try:
            signal_deg = self.detect_signal_quality_degradation()
        except Exception as exc:
            logger.warning("SignalDegradationMonitor.detect_signal_quality_degradation: %s", exc)
            warnings.append(f"signal_quality error: {exc}")
            signal_deg = {"status": "INSUFFICIENT_DATA", "note": str(exc)}

        try:
            port_deg = self.detect_portfolio_degradation()
        except Exception as exc:
            logger.warning("SignalDegradationMonitor.detect_portfolio_degradation: %s", exc)
            warnings.append(f"portfolio_degradation error: {exc}")
            port_deg = {"status": "INSUFFICIENT_DATA", "note": str(exc)}

        # Aggregate status — take worst
        statuses = [
            rule_deg.get("status",   "INSUFFICIENT_DATA"),
            signal_deg.get("status", "INSUFFICIENT_DATA"),
            port_deg.get("status",   "INSUFFICIENT_DATA"),
        ]
        overall = self._aggregate_status(statuses)

        return {
            "status":                      overall,
            "rule_degradation":            rule_deg,
            "signal_quality_degradation":  signal_deg,
            "portfolio_degradation":       port_deg,
            "warnings":                    warnings,
            **self._SAFETY,
        }

    # ------------------------------------------------------------------
    # Sub-checks
    # ------------------------------------------------------------------

    def compare_recent_vs_baseline(self, records: list) -> dict:
        """Compare most recent N records to baseline N (N = min(20, len/2))."""
        if not records:
            return {"status": "INSUFFICIENT_DATA", "note": "no records"}
        n = max(1, min(20, len(records) // 2))
        baseline = records[:n]
        recent   = records[-n:]

        def avg_return(recs):
            vals = [r.get("return", r.get("total_return", 0)) or 0 for r in recs]
            return sum(vals) / len(vals) if vals else 0.0

        b_ret = avg_return(baseline)
        r_ret = avg_return(recent)
        change = (r_ret - b_ret) / (abs(b_ret) + 1e-9) if b_ret != 0 else 0.0

        status = self._classify_change(abs(change))
        return {
            "status":          status,
            "baseline_avg":    b_ret,
            "recent_avg":      r_ret,
            "relative_change": change,
            "n_baseline":      n,
            "n_recent":        n,
        }

    def detect_rule_degradation(self) -> dict:
        """Read rule governance data if available; check rule confidence drops."""
        # Try to find rule governance CSVs
        candidates = [
            os.path.join(_BASE_DIR, "data", "governance", "rule_performance.csv"),
            os.path.join(_BASE_DIR, "data", "rule_governance", "performance.csv"),
            os.path.join(self._results_dir, "rule_performance.csv"),
        ]
        for path in candidates:
            if os.path.isfile(path):
                try:
                    rows = self._load_csv(path)
                    if rows:
                        return self._analyze_rule_rows(rows)
                except Exception as exc:
                    logger.warning("detect_rule_degradation load %s: %s", path, exc)

        # Try governance module
        try:
            from governance.rule_governance import RuleGovernance
            rg    = RuleGovernance()
            rules = rg.list_rules() if hasattr(rg, "list_rules") else []
            if rules:
                return self._analyze_rule_objects(rules)
        except Exception:
            pass

        return {"status": "INSUFFICIENT_DATA", "note": "no rule governance data found", "degraded_rules": []}

    def detect_signal_quality_degradation(self) -> dict:
        """Read signal quality CSV if available; check boost/reduce/disable counts."""
        candidates = [
            os.path.join(_BASE_DIR, "data", "signal_quality", "signal_quality.csv"),
            os.path.join(_BASE_DIR, "data", "quality", "signal_quality.csv"),
            os.path.join(self._results_dir, "signal_quality.csv"),
        ]
        for path in candidates:
            if os.path.isfile(path):
                try:
                    rows = self._load_csv(path)
                    if rows:
                        return self._analyze_signal_rows(rows)
                except Exception as exc:
                    logger.warning("detect_signal_quality_degradation load %s: %s", path, exc)

        return {"status": "INSUFFICIENT_DATA", "note": "no signal quality data found", "degraded_signals": []}

    def detect_portfolio_degradation(self) -> dict:
        """Read portfolio CSV if available; check return/drawdown."""
        candidates = [
            os.path.join(self._results_dir, "portfolio_summary.csv"),
            os.path.join(_BASE_DIR, "data", "backtest_results", "portfolio_summary.csv"),
            os.path.join(_BASE_DIR, "reports", "portfolio_summary.csv"),
        ]
        for path in candidates:
            if os.path.isfile(path):
                try:
                    rows = self._load_csv(path)
                    if rows:
                        return self.compare_recent_vs_baseline(rows)
                except Exception as exc:
                    logger.warning("detect_portfolio_degradation load %s: %s", path, exc)

        return {"status": "INSUFFICIENT_DATA", "note": "no portfolio data found"}

    # ------------------------------------------------------------------
    # Analysis helpers
    # ------------------------------------------------------------------

    def _analyze_rule_rows(self, rows: list) -> dict:
        degraded = []
        for r in rows:
            conf = r.get("confidence", r.get("win_rate", None))
            if conf is None:
                continue
            try:
                conf = float(conf)
            except (ValueError, TypeError):
                continue
            if conf < 0.40:
                degraded.append({"rule_id": r.get("rule_id", "?"), "confidence": conf, "status": "LOW"})

        n = len(degraded)
        if n == 0:
            status = "STABLE"
        elif n <= 2:
            status = "WATCH"
        elif n <= 5:
            status = "DEGRADED"
        else:
            status = "SEVERE"

        return {"status": status, "degraded_rules": degraded, "total_rules": len(rows)}

    def _analyze_rule_objects(self, rules: list) -> dict:
        degraded = []
        for r in rules:
            d = r if isinstance(r, dict) else (r.to_dict() if hasattr(r, "to_dict") else {})
            conf = d.get("confidence", d.get("win_rate", None))
            if conf is not None:
                try:
                    if float(conf) < 0.40:
                        degraded.append({"rule_id": d.get("rule_id", "?"), "confidence": float(conf)})
                except (ValueError, TypeError):
                    pass
        n = len(degraded)
        status = "STABLE" if n == 0 else ("WATCH" if n <= 2 else ("DEGRADED" if n <= 5 else "SEVERE"))
        return {"status": status, "degraded_rules": degraded, "total_rules": len(rules)}

    def _analyze_signal_rows(self, rows: list) -> dict:
        boost_count   = sum(1 for r in rows if str(r.get("action", "")).upper() == "BOOST")
        reduce_count  = sum(1 for r in rows if str(r.get("action", "")).upper() == "REDUCE")
        disable_count = sum(1 for r in rows if str(r.get("action", "")).upper() in ("DISABLE", "DISABLED"))
        total         = len(rows)

        degraded_ratio = (reduce_count + disable_count) / total if total > 0 else 0.0
        status = self._classify_change(degraded_ratio)

        return {
            "status":               status,
            "total_signals":        total,
            "boost_count":          boost_count,
            "reduce_count":         reduce_count,
            "disable_count":        disable_count,
            "degraded_ratio":       degraded_ratio,
            "degraded_signals":     [r for r in rows if str(r.get("action", "")).upper() in ("REDUCE", "DISABLE", "DISABLED")],
        }

    # ------------------------------------------------------------------
    # Status classification
    # ------------------------------------------------------------------

    def _classify_change(self, magnitude: float) -> str:
        if magnitude >= _SEVERE_THRESHOLD:
            return "SEVERE"
        elif magnitude >= _DEGRADED_THRESHOLD:
            return "DEGRADED"
        elif magnitude >= _WATCH_THRESHOLD:
            return "WATCH"
        else:
            return "STABLE"

    def _aggregate_status(self, statuses: list) -> str:
        rank = {"SEVERE": 4, "DEGRADED": 3, "WATCH": 2, "STABLE": 1, "INSUFFICIENT_DATA": 0}
        best = max(statuses, key=lambda s: rank.get(s, 0), default="INSUFFICIENT_DATA")
        return best

    # ------------------------------------------------------------------
    # CSV loader
    # ------------------------------------------------------------------

    def _load_csv(self, path: str) -> list:
        """Load a CSV file as list of dicts — no pandas required."""
        import csv
        rows = []
        with open(path, "r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append(dict(row))
        return rows
