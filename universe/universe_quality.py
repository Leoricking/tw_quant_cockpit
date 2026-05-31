"""
universe/universe_quality.py - Universe coverage / readiness evaluation (v0.3.25).

Scores a universe on coverage, freshness, provider reliability,
sector balance, liquidity, and backtest sample readiness.

[!] Research Only. Not investment advice.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_READINESS_LEVELS = [
    (90, "STRONG_RESEARCH_UNIVERSE"),
    (75, "BACKTEST_READY"),
    (60, "RESEARCH_READY"),
    (40, "OBSERVATIONAL"),
    (0,  "INSUFFICIENT"),
]


class UniverseQualityAnalyzer:
    """
    Evaluates universe quality and readiness.

    Parameters
    ----------
    universe_name : universe group name (e.g., 'core_50')
    import_root   : data/import/ path
    results_dir   : data/backtest_results/ path
    config_dir    : config/universe/ path
    """

    read_only         = True
    no_real_orders    = True
    production_blocked = True

    def __init__(
        self,
        universe_name: str = "core_50",
        import_root:   str = "data/import",
        results_dir:   str = "data/backtest_results",
        config_dir:    str = "config/universe",
    ):
        self.universe_name = universe_name
        self._import_root  = os.path.join(_BASE_DIR, import_root) if not os.path.isabs(import_root) else import_root
        self._results_dir  = os.path.join(_BASE_DIR, results_dir) if not os.path.isabs(results_dir) else results_dir
        self._config_dir   = os.path.join(_BASE_DIR, config_dir)  if not os.path.isabs(config_dir)  else config_dir

        self._symbols:  List[str] = []
        self._rows:     List[dict] = []
        self._scores:   Dict[str, float] = {}

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Run full quality analysis and return result dict."""
        from universe.universe_registry import UniverseRegistry
        reg = UniverseRegistry(config_dir=self._config_dir, import_root=self._import_root)
        self._rows    = reg.load_universe(self.universe_name)
        self._symbols = [r["symbol"] for r in self._rows if r.get("symbol")]

        if not self._symbols:
            return {
                "universe_name":    self.universe_name,
                "symbol_count":     0,
                "overall_universe_score": 0.0,
                "readiness_level":  "INSUFFICIENT",
                "error":            "Universe not found or empty — run universe-build-defaults first",
                "read_only":        True,
                "no_real_orders":   True,
            }

        coverage  = self.calculate_coverage()
        freshness = self.calculate_freshness()
        prov_rel  = self.calculate_provider_reliability()
        sec_bal   = self.calculate_sector_balance()
        liq       = self.calculate_liquidity_readiness()
        bt_samp   = self.calculate_backtest_sample_readiness()
        overall   = self.calculate_overall_universe_score()

        missing  = self._find_missing_symbols()
        weak_sec = self._find_weak_sectors()
        recs     = self._build_recommendations(overall, coverage, freshness, prov_rel)

        return {
            "universe_name":               self.universe_name,
            "symbol_count":                len(self._symbols),
            "coverage_score":              coverage,
            "freshness_score":             freshness,
            "provider_reliability_score":  prov_rel,
            "sector_balance_score":        sec_bal,
            "liquidity_readiness_score":   liq,
            "backtest_sample_readiness_score": bt_samp,
            "overall_universe_score":      overall,
            "readiness_level":             self._classify(overall),
            "missing_symbols":             missing,
            "weak_sectors":                weak_sec,
            "recommendations":             recs,
            "generated_at":                datetime.now().isoformat(),
            "read_only":                   True,
            "no_real_orders":              True,
            "not_investment_advice":       True,
        }

    # ------------------------------------------------------------------
    # Component scores
    # ------------------------------------------------------------------

    def calculate_coverage(self) -> float:
        """Score based on how much import data exists for universe symbols."""
        if not self._symbols:
            return 0.0
        datasets = {
            "daily_k":        "data/import/daily/daily_k.csv",
            "monthly_revenue":"data/import/monthly_revenue/monthly_revenue.csv",
            "institutional":  "data/import/institutional/institutional.csv",
            "margin":         "data/import/margin/margin.csv",
        }
        covered_symbols_total = 0
        checked_datasets = 0
        for ds_name, rel_path in datasets.items():
            abs_path = os.path.join(_BASE_DIR, rel_path)
            if not os.path.isfile(abs_path):
                continue
            checked_datasets += 1
            try:
                import pandas as pd
                df = pd.read_csv(abs_path, low_memory=False, usecols=["symbol"])
                present = set(df["symbol"].dropna().astype(str).unique())
                covered = len([s for s in self._symbols if str(s) in present])
                covered_symbols_total += covered
            except Exception:
                pass
        if checked_datasets == 0:
            return 0.0
        avg = covered_symbols_total / (checked_datasets * len(self._symbols))
        score = round(min(100.0, avg * 100), 1)
        self._scores["coverage"] = score
        return score

    def calculate_freshness(self) -> float:
        """Score based on data freshness from DataFreshnessChecker."""
        try:
            from data.providers.data_freshness import DataFreshnessChecker
            checker = DataFreshnessChecker(import_root=_BASE_DIR)
            result  = checker.run_all()
            datasets = result.get("datasets", {})
            fresh_count = sum(1 for d in datasets.values() if d.get("status") in ("FRESH", "PARTIAL"))
            total_count = len([d for d in datasets.values() if d.get("status") != "UNKNOWN"])
            score = round((fresh_count / total_count) * 100, 1) if total_count else 50.0
        except Exception:
            score = 50.0
        self._scores["freshness"] = score
        return score

    def calculate_provider_reliability(self) -> float:
        """Score based on provider reliability matrix."""
        try:
            from data.providers.reliability_matrix import ProviderReliabilityMatrix
            matrix = ProviderReliabilityMatrix(mode="real")
            result = matrix.run()
            score = result.get("reliability_summary", {}).get("overall_reliability_score") or 60.0
            score = float(score)
        except Exception:
            score = 60.0
        self._scores["provider_reliability"] = score
        return score

    def calculate_sector_balance(self) -> float:
        """Score based on sector diversity (penalize concentration)."""
        if not self._rows:
            return 0.0
        from collections import Counter
        sectors = [r.get("sector", "other") for r in self._rows]
        counts = Counter(sectors)
        total = len(sectors)
        n_sectors = len(counts)
        max_pct = max(counts.values()) / total if total else 1.0
        # Perfect balance = many sectors, no single sector > 30%
        diversity_score = min(100.0, (n_sectors / max(1, total * 0.3)) * 50)
        concentration_penalty = max(0.0, (max_pct - 0.30) * 100)
        score = round(max(0.0, min(100.0, diversity_score - concentration_penalty)), 1)
        self._scores["sector_balance"] = score
        return score

    def calculate_liquidity_readiness(self) -> float:
        """Score based on liquidity tier of symbols."""
        if not self._rows:
            return 0.0
        tiers = [r.get("liquidity_tier", "UNKNOWN") for r in self._rows]
        large = tiers.count("LARGE")
        mid   = tiers.count("MID")
        known = large + mid
        if not known:
            return 50.0  # optimistic if unknown
        score = round(min(100.0, (large * 100 + mid * 60) / len(tiers)), 1)
        self._scores["liquidity"] = score
        return score

    def calculate_backtest_sample_readiness(self) -> float:
        """Score based on symbol count for backtesting."""
        n = len(self._symbols)
        if n >= 100:
            return 100.0
        if n >= 50:
            return 80.0
        if n >= 30:
            return 60.0
        if n >= 14:
            return 40.0
        return 20.0

    def calculate_overall_universe_score(self) -> float:
        """Compute weighted overall score."""
        coverage  = self._scores.get("coverage",             self.calculate_coverage())
        freshness = self._scores.get("freshness",            self.calculate_freshness())
        prov_rel  = self._scores.get("provider_reliability", self.calculate_provider_reliability())
        sec_bal   = self._scores.get("sector_balance",       self.calculate_sector_balance())
        liq       = self._scores.get("liquidity",            self.calculate_liquidity_readiness())
        bt_samp   = self.calculate_backtest_sample_readiness()

        raw = (
            0.25 * coverage +
            0.20 * freshness +
            0.20 * prov_rel +
            0.15 * sec_bal +
            0.10 * liq +
            0.10 * bt_samp
        )

        # Degradation caps
        n = len(self._symbols)
        if n < 30:
            raw = min(raw, 59.0)   # max OBSERVATIONAL
        if coverage < 60:
            raw = min(raw, 59.0)
        if freshness < 60:
            raw = min(raw, 74.0)   # max RESEARCH_READY
        if prov_rel < 60:
            raw = min(raw, 74.0)

        return round(min(100.0, max(0.0, raw)), 1)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _classify(self, score: float) -> str:
        for threshold, level in _READINESS_LEVELS:
            if score >= threshold:
                return level
        return "INSUFFICIENT"

    def _find_missing_symbols(self) -> List[str]:
        try:
            import pandas as pd
            daily_path = os.path.join(_BASE_DIR, "data", "import", "daily", "daily_k.csv")
            if not os.path.isfile(daily_path):
                return self._symbols[:10]
            df = pd.read_csv(daily_path, low_memory=False, usecols=["symbol"])
            present = set(df["symbol"].dropna().astype(str).unique())
            return [s for s in self._symbols if str(s) not in present][:20]
        except Exception:
            return []

    def _find_weak_sectors(self) -> List[str]:
        from collections import Counter
        sectors = [r.get("sector", "other") for r in self._rows]
        counts = Counter(sectors)
        total = len(sectors)
        weak = [sec for sec, cnt in counts.items() if cnt / total < 0.05]
        return weak

    def _build_recommendations(self, overall, coverage, freshness, prov_rel) -> List[str]:
        recs = []
        if len(self._symbols) < 30:
            recs.append(f"Expand universe to >=30 symbols (currently {len(self._symbols)}) for RESEARCH_READY level")
        if coverage < 60:
            recs.append("Run provider-auto-fetch to improve data coverage")
        if freshness < 60:
            recs.append("Run update-data to refresh stale datasets")
        if prov_rel < 60:
            recs.append("Check provider health and configure FINMIND_TOKEN")
        recs.append(f"Current readiness: {self._classify(overall)} — not for production trading")
        return recs
