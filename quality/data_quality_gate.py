"""
quality/data_quality_gate.py - Data Quality Gate & Production Readiness Score (v0.3.20).

Computes 10 sub-scores, two composite scores (production / backtest readiness),
and evaluates 8 gate decisions.

[!] Research Only. Simulation Only. No Real Orders.
[!] PRODUCTION_BLOCKED is always True in v1.
[!] REAL_ORDER_READY is never allowed.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DataQualityGate:
    """
    Data Quality Gate & Production Readiness Score.

    Computes:
      - 8 sub-scores (0-100 each)
      - production_readiness_score (weighted composite)
      - backtest_readiness_score (weighted composite, with capping)
      - 8 gate decisions

    Parameters
    ----------
    mode         : 'real' or 'mock'
    import_root  : path to data/import/
    results_dir  : path to data/backtest_results/
    reports_dir  : path to reports/
    portfolio_results_dir : path to data/backtest_results/ (same by default)
    freshness_result      : pre-computed freshness dict (from DataFreshnessChecker)
    health_result         : pre-computed health dict (from ProviderHealthChecker)
    """

    VERSION = "v0.3.20"

    # Hard-coded safety invariants
    read_only     = True
    no_real_orders = True
    PRODUCTION_BLOCKED: bool = True
    REAL_ORDER_READY: bool   = False

    def __init__(
        self,
        mode: str = "real",
        import_root: Optional[str] = None,
        results_dir: Optional[str] = None,
        reports_dir: Optional[str] = None,
        portfolio_results_dir: Optional[str] = None,
        freshness_result: Optional[dict] = None,
        health_result: Optional[dict] = None,
    ):
        self.mode = mode
        self.import_root = import_root or os.path.join(_BASE_DIR, "data", "import")
        self.results_dir = results_dir or os.path.join(_BASE_DIR, "data", "backtest_results")
        self.reports_dir = reports_dir or os.path.join(_BASE_DIR, "reports")
        self.portfolio_results_dir = portfolio_results_dir or self.results_dir

        # Pre-computed sub-results (avoid re-fetching if already done)
        self._freshness_result = freshness_result
        self._health_result    = health_result

        # Sub-scores (populated during run)
        self._scores: Dict[str, float] = {}
        self._score_details: Dict[str, dict] = {}

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Compute all scores and gate decisions.

        Returns dict with:
          scores              : dict of all 10 sub-scores
          production_readiness_score
          backtest_readiness_score
          production_classification
          backtest_classification
          gates               : dict of gate decisions
          details             : per-score detail dicts
          checked_at          : ISO datetime string
          mode                : 'real' or 'mock'
          production_blocked  : True (always)
          real_order_ready    : False (always)
          warnings            : list of warning strings
        """
        logger.info(
            "[DataQualityGate] run [mode=%s read_only=True no_real_orders=True]",
            self.mode,
        )

        warnings: List[str] = []

        # --- Compute all sub-scores ---
        self._compute_freshness_score(warnings)
        self._compute_coverage_score(warnings)
        self._compute_source_confidence_score(warnings)
        self._compute_timing_quality_score(warnings)
        self._compute_sample_size_score(warnings)
        self._compute_intraday_coverage_score(warnings)
        self._compute_provider_health_score(warnings)
        self._compute_mock_contamination_score(warnings)

        # --- Composite scores ---
        from quality.readiness_score import ReadinessScoreCalculator
        calc = ReadinessScoreCalculator(self._scores)
        prod_score  = calc.production_readiness_score()
        btest_score = calc.backtest_readiness_score()

        # --- Gate decisions ---
        gates = self._evaluate_gates(prod_score, btest_score)

        # Build structured blockers list (v0.3.22)
        blockers = self._build_blockers(prod_score, btest_score, warnings)

        result = {
            "checked_at":                   datetime.now().isoformat(),
            "mode":                         self.mode,
            "scores":                       dict(self._scores),
            "production_readiness_score":   prod_score,
            "backtest_readiness_score":     btest_score,
            "production_classification":    ReadinessScoreCalculator.classify(prod_score),
            "backtest_classification":      ReadinessScoreCalculator.classify(btest_score),
            "gates":                        gates,
            "details":                      dict(self._score_details),
            "production_blocked":           self.PRODUCTION_BLOCKED,
            "real_order_ready":             self.REAL_ORDER_READY,
            "warnings":                     warnings,
            "blockers":                     blockers,
        }
        return result

    # ------------------------------------------------------------------
    # Structured blockers (v0.3.22)
    # ------------------------------------------------------------------

    def _build_blockers(
        self,
        prod_score:  float,
        btest_score: float,
        warnings:    list,
    ) -> list:
        """
        Build a list of structured blocker dicts.

        Each blocker has:
          blocker_name           : short identifier
          severity               : INFO / WARNING / ERROR / FATAL
          reason                 : human-readable explanation
          next_step              : actionable fix
          can_continue_research  : True if research can proceed despite this blocker
        """
        blockers: list = []
        cov_score  = self._scores.get("coverage_score",          0.0)
        mock_score = self._scores.get("mock_contamination_score", 0.0)
        fresh_score = self._scores.get("freshness_score",         0.0)
        sample_score = self._scores.get("sample_size_score",      0.0)

        # Always-present production blocker
        blockers.append({
            "blocker_name":          "PRODUCTION_BLOCKED",
            "severity":              "FATAL",
            "reason":                "Production trading is always blocked in this system. "
                                     "No real orders will ever be placed.",
            "next_step":             "This is intentional. The system is for research only.",
            "can_continue_research": True,
        })

        # Low coverage
        if cov_score < 70.0:
            blockers.append({
                "blocker_name":          "LOW_COVERAGE",
                "severity":              "ERROR",
                "reason":                f"Data coverage score is {cov_score:.1f} (threshold: 70). "
                                         "Insufficient data may produce unreliable backtest results.",
                "next_step":             "Import more CSV data or run: python main.py provider-auto-fetch",
                "can_continue_research": cov_score >= 40.0,
            })

        # Mock contamination
        if mock_score < 90.0:
            blockers.append({
                "blocker_name":          "MOCK_CONTAMINATION",
                "severity":              "ERROR" if mock_score < 60.0 else "WARNING",
                "reason":                f"Mock contamination score is {mock_score:.1f} (threshold: 90). "
                                         "Backtest results may be inflated by mock data.",
                "next_step":             "Review data/import/ files for mock markers. "
                                         "Run: python main.py data-quality-gate --check-mock",
                "can_continue_research": mock_score >= 60.0,
            })

        # Low freshness
        if fresh_score < 50.0:
            blockers.append({
                "blocker_name":          "STALE_DATA",
                "severity":              "WARNING",
                "reason":                f"Data freshness score is {fresh_score:.1f}. "
                                         "Some datasets may be outdated.",
                "next_step":             "Run: python main.py update-data to refresh all data sources.",
                "can_continue_research": True,
            })

        # Low sample size
        if sample_score < 40.0:
            blockers.append({
                "blocker_name":          "INSUFFICIENT_SAMPLE",
                "severity":              "WARNING",
                "reason":                f"Sample size score is {sample_score:.1f}. "
                                         "Statistical confidence is insufficient for reliable backtesting.",
                "next_step":             "Import more historical data covering at least 2+ years.",
                "can_continue_research": True,
            })

        return blockers

    # ------------------------------------------------------------------
    # Gate evaluation
    # ------------------------------------------------------------------

    def _evaluate_gates(self, prod_score: float, btest_score: float) -> dict:
        """
        Evaluate all 8 gate decisions.

        Gates:
          RESEARCH_ONLY       : always True
          BACKTEST_READY      : prod>=70 AND coverage>=70 AND mock_contamination>=90
          PAPER_TRADING_READY : prod>=80 AND btest>=75 (no_real_orders=True)
          PRODUCTION_BLOCKED  : ALWAYS True in v1
          API_READY_READONLY  : provider_health>=60
          INTRADAY_READY      : intraday_coverage>=70
          LONG_TERM_READY     : long-term coverage>=70
          PORTFOLIO_READY     : portfolio sim data exists AND prod>=70
        """
        cov_score         = self._scores.get("coverage_score", 0.0)
        mock_score        = self._scores.get("mock_contamination_score", 0.0)
        provider_score    = self._scores.get("provider_health_score", 0.0)
        intraday_score    = self._scores.get("intraday_coverage_score", 0.0)

        backtest_ready = (
            prod_score  >= 70.0
            and cov_score   >= 70.0
            and mock_score  >= 90.0
        )

        paper_trading_ready = (
            prod_score  >= 80.0
            and btest_score >= 75.0
        )

        portfolio_sim_exists = self._portfolio_sim_exists()

        # Approximate long-term coverage from sample_size_score
        long_term_cov = self._scores.get("sample_size_score", 0.0)

        return {
            "RESEARCH_ONLY":        True,
            "BACKTEST_READY":       backtest_ready,
            "PAPER_TRADING_READY":  paper_trading_ready,
            "PRODUCTION_BLOCKED":   True,          # always True in v1
            "API_READY_READONLY":   provider_score >= 60.0,
            "INTRADAY_READY":       intraday_score >= 70.0,
            "LONG_TERM_READY":      long_term_cov  >= 70.0,
            "PORTFOLIO_READY":      portfolio_sim_exists and prod_score >= 70.0,
            # Safety invariant — never allowed
            "REAL_ORDER_READY":     False,
            # Note fields
            "_note_production_blocked": "PRODUCTION_BLOCKED is always True in v0.3 (v1). Real trading is not supported.",
            "_note_real_order_ready":   "REAL_ORDER_READY is never allowed in this system.",
        }

    # ------------------------------------------------------------------
    # Sub-score: freshness
    # ------------------------------------------------------------------

    def _compute_freshness_score(self, warnings: List[str]) -> None:
        """
        Score based on how many datasets are FRESH.

        FRESH=100, PARTIAL/STALE=60, OLD=30, MISSING=0
        """
        try:
            freshness = self._get_freshness()
            datasets  = freshness.get("datasets", {})

            _status_scores = {
                "FRESH":                100.0,
                "HISTORICAL_INTRADAY":  80.0,
                "PARTIAL":              60.0,
                "STALE":                60.0,
                "OLD":                  30.0,
                "MISSING":              0.0,
                "UNKNOWN":              50.0,
            }

            scored = [
                _status_scores.get(info.get("status", "UNKNOWN"), 50.0)
                for info in datasets.values()
            ]
            score = round(sum(scored) / len(scored), 2) if scored else 0.0

            self._scores["freshness_score"] = score
            self._score_details["freshness_score"] = {
                "score":    score,
                "datasets": {ds: info.get("status", "UNKNOWN") for ds, info in datasets.items()},
            }
        except Exception as exc:
            warnings.append(f"freshness_score: {exc}")
            self._scores["freshness_score"] = 0.0
            self._score_details["freshness_score"] = {"error": str(exc)}

    # ------------------------------------------------------------------
    # Sub-score: coverage
    # ------------------------------------------------------------------

    def _compute_coverage_score(self, warnings: List[str]) -> None:
        """
        Score based on fraction of standard datasets present and non-empty.
        """
        try:
            import pandas as _pd
        except ImportError:
            warnings.append("coverage_score: pandas not available")
            self._scores["coverage_score"] = 0.0
            self._score_details["coverage_score"] = {"error": "pandas not available"}
            return

        _FILES = {
            "daily_price":     "daily/daily_k.csv",
            "monthly_revenue": "monthly_revenue/monthly_revenue.csv",
            "institutional":   "institutional/institutional.csv",
            "margin":          "margin/margin.csv",
            "fundamental":     "fundamental/fundamental.csv",
        }

        details = {}
        ok = 0
        total = len(_FILES)
        for ds, rel in _FILES.items():
            full = os.path.join(self.import_root, rel)
            if not os.path.exists(full):
                details[ds] = "MISSING"
                continue
            try:
                df = _pd.read_csv(full, nrows=5)
                if df.empty:
                    details[ds] = "EMPTY"
                else:
                    details[ds] = "PRESENT"
                    ok += 1
            except Exception:
                details[ds] = "READ_ERROR"

        score = round(100.0 * ok / total, 2) if total else 0.0
        self._scores["coverage_score"] = score
        self._score_details["coverage_score"] = {"score": score, "datasets": details}

    # ------------------------------------------------------------------
    # Sub-score: source confidence
    # ------------------------------------------------------------------

    def _compute_source_confidence_score(self, warnings: List[str]) -> None:
        """
        Score based on provider health: more OK providers → higher confidence.

        provider_health_score is shared/reused here as a proxy.
        """
        try:
            health = self._get_health()
            summary = health.get("summary", {})
            ok      = summary.get("OK", 0)
            partial = summary.get("PARTIAL", 0)
            total_checked = sum(
                summary.get(s, 0)
                for s in ("OK", "PARTIAL", "NOT_CONFIGURED", "FAILED")
            ) or 1

            score = round(100.0 * (ok + 0.5 * partial) / total_checked, 2)
            self._scores["source_confidence_score"] = score
            self._score_details["source_confidence_score"] = {
                "score":   score,
                "summary": summary,
            }
        except Exception as exc:
            warnings.append(f"source_confidence_score: {exc}")
            self._scores["source_confidence_score"] = 50.0
            self._score_details["source_confidence_score"] = {"error": str(exc)}

    # ------------------------------------------------------------------
    # Sub-score: timing quality
    # ------------------------------------------------------------------

    def _compute_timing_quality_score(self, warnings: List[str]) -> None:
        """
        Score based on whether key datasets have recent-enough data for timing.

        daily_price must be within 3 days; monthly_revenue within 45 days.
        """
        try:
            freshness = self._get_freshness()
            datasets  = freshness.get("datasets", {})
            today     = datetime.now().date()

            _weights = {
                "daily_price":     (3,  0.50),   # (max_days_old, weight)
                "monthly_revenue": (45, 0.30),
                "institutional":   (3,  0.10),
                "margin":          (3,  0.10),
            }

            total_score = 0.0
            total_weight = 0.0
            details = {}

            for ds, (max_days, w) in _weights.items():
                info = datasets.get(ds, {})
                ld   = info.get("latest_date", "")
                if ld:
                    try:
                        ld_date = datetime.strptime(ld, "%Y-%m-%d").date()
                        age = (today - ld_date).days
                        if age <= max_days:
                            ds_score = 100.0
                        elif age <= max_days * 3:
                            ds_score = 60.0
                        else:
                            ds_score = max(0.0, 100.0 - (age / max_days) * 20.0)
                        details[ds] = {"age_days": age, "score": ds_score}
                    except ValueError:
                        ds_score = 50.0
                        details[ds] = {"latest_date": ld, "score": ds_score}
                else:
                    ds_score = 0.0
                    details[ds] = {"latest_date": None, "score": ds_score}

                total_score  += ds_score * w
                total_weight += w

            score = round(total_score / total_weight, 2) if total_weight else 0.0
            self._scores["timing_quality_score"] = score
            self._score_details["timing_quality_score"] = {
                "score":   score,
                "details": details,
            }
        except Exception as exc:
            warnings.append(f"timing_quality_score: {exc}")
            self._scores["timing_quality_score"] = 0.0
            self._score_details["timing_quality_score"] = {"error": str(exc)}

    # ------------------------------------------------------------------
    # Sub-score: sample size
    # ------------------------------------------------------------------

    def _compute_sample_size_score(self, warnings: List[str]) -> None:
        """
        Score based on total rows available in key datasets.

        daily_price: >50000 rows → 100; >10000 → 70; >1000 → 40; else 0
        monthly_revenue: >5000 rows → 100; >1000 → 70; else 40
        """
        try:
            import pandas as _pd
        except ImportError:
            warnings.append("sample_size_score: pandas not available")
            self._scores["sample_size_score"] = 0.0
            self._score_details["sample_size_score"] = {"error": "pandas not available"}
            return

        _FILE_THRESHOLDS = {
            "daily/daily_k.csv": [
                (50_000, 100.0),
                (10_000, 70.0),
                (1_000,  40.0),
                (0,       0.0),
            ],
            "monthly_revenue/monthly_revenue.csv": [
                (5_000,  100.0),
                (1_000,   70.0),
                (0,       40.0),
            ],
            "institutional/institutional.csv": [
                (10_000, 100.0),
                (2_000,   70.0),
                (0,       40.0),
            ],
        }

        scores_per_file = []
        details = {}

        for rel_path, thresholds in _FILE_THRESHOLDS.items():
            full = os.path.join(self.import_root, rel_path)
            if not os.path.exists(full):
                details[rel_path] = {"rows": 0, "score": 0.0, "status": "MISSING"}
                scores_per_file.append(0.0)
                continue
            try:
                n_rows = sum(1 for _ in open(full, encoding="utf-8", errors="replace")) - 1
                file_score = 0.0
                for threshold, s in thresholds:
                    if n_rows >= threshold:
                        file_score = s
                        break
                details[rel_path] = {"rows": n_rows, "score": file_score}
                scores_per_file.append(file_score)
            except Exception as exc:
                details[rel_path] = {"error": str(exc), "score": 0.0}
                scores_per_file.append(0.0)

        score = round(sum(scores_per_file) / len(scores_per_file), 2) if scores_per_file else 0.0
        self._scores["sample_size_score"] = score
        self._score_details["sample_size_score"] = {"score": score, "files": details}

    # ------------------------------------------------------------------
    # Sub-score: intraday coverage
    # ------------------------------------------------------------------

    def _compute_intraday_coverage_score(self, warnings: List[str]) -> None:
        """
        Score based on whether intraday data files exist.

        Has any .csv in data/import/intraday/ → 100; MISSING → 0
        """
        try:
            import glob as _glob
            intraday_dir = os.path.join(self.import_root, "intraday")
            csv_files = _glob.glob(os.path.join(intraday_dir, "*.csv"))
            if csv_files:
                score = 100.0
                details = {"files_found": len(csv_files), "status": "PRESENT"}
            else:
                score = 0.0
                details = {"files_found": 0, "status": "MISSING"}

            self._scores["intraday_coverage_score"] = score
            self._score_details["intraday_coverage_score"] = {"score": score, **details}
        except Exception as exc:
            warnings.append(f"intraday_coverage_score: {exc}")
            self._scores["intraday_coverage_score"] = 0.0
            self._score_details["intraday_coverage_score"] = {"error": str(exc)}

    # ------------------------------------------------------------------
    # Sub-score: provider health
    # ------------------------------------------------------------------

    def _compute_provider_health_score(self, warnings: List[str]) -> None:
        """
        Score based on proportion of providers that are OK or PARTIAL.
        """
        try:
            health  = self._get_health()
            summary = health.get("summary", {})
            ok      = summary.get("OK", 0)
            partial = summary.get("PARTIAL", 0)
            total   = sum(summary.values()) or 1

            score = round(100.0 * (ok + 0.5 * partial) / total, 2)
            self._scores["provider_health_score"] = score
            self._score_details["provider_health_score"] = {
                "score":   score,
                "summary": summary,
            }
        except Exception as exc:
            warnings.append(f"provider_health_score: {exc}")
            self._scores["provider_health_score"] = 50.0
            self._score_details["provider_health_score"] = {"error": str(exc)}

    # ------------------------------------------------------------------
    # Sub-score: mock contamination
    # ------------------------------------------------------------------

    def _compute_mock_contamination_score(self, warnings: List[str]) -> None:
        """
        Score from MockContaminationChecker (0-100; 100=clean).
        """
        try:
            from quality.mock_contamination_checker import MockContaminationChecker
            checker = MockContaminationChecker(
                import_root=self.import_root,
                results_dir=self.results_dir,
                reports_dir=self.reports_dir,
                mode=self.mode,
            )
            result = checker.run()
            score  = result.score

            self._scores["mock_contamination_score"] = score
            self._score_details["mock_contamination_score"] = result.to_dict()
        except Exception as exc:
            warnings.append(f"mock_contamination_score: {exc}")
            self._scores["mock_contamination_score"] = 100.0  # assume clean on error
            self._score_details["mock_contamination_score"] = {"error": str(exc)}

    # ------------------------------------------------------------------
    # Lazy loaders for freshness and health
    # ------------------------------------------------------------------

    def _get_freshness(self) -> dict:
        if self._freshness_result is not None:
            return self._freshness_result
        try:
            from data.providers.data_freshness import DataFreshnessChecker
            fc = DataFreshnessChecker(import_root=self.import_root)
            self._freshness_result = fc.run_all()
        except Exception as exc:
            logger.warning("DataFreshnessChecker failed: %s", exc)
            self._freshness_result = {"datasets": {}, "summary": {}}
        return self._freshness_result

    def _get_health(self) -> dict:
        if self._health_result is not None:
            return self._health_result
        try:
            from data.providers.provider_health import ProviderHealthChecker
            hc = ProviderHealthChecker()
            self._health_result = hc.run_all()
        except Exception as exc:
            logger.warning("ProviderHealthChecker failed: %s", exc)
            self._health_result = {"summary": {}, "providers": {}}
        return self._health_result

    # ------------------------------------------------------------------
    # Portfolio sim existence check
    # ------------------------------------------------------------------

    def _portfolio_sim_exists(self) -> bool:
        import glob as _glob
        pattern = os.path.join(self.portfolio_results_dir, "portfolio_*.csv")
        return bool(_glob.glob(pattern))
