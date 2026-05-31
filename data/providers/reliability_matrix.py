"""
data/providers/reliability_matrix.py - Provider Reliability Matrix engine (v0.3.24).

Builds a provider reliability matrix, dataset fallback chains, and dataset
confidence scores from provider health logs and fetch reports.

[!] Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No token written. No mock fallback in real mode.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dataset fallback chains — mock fallback DISABLED
_DATASET_FALLBACK_CHAINS: Dict[str, List[str]] = {
    "daily_price":     ["finmind", "twse", "tpex", "csv", "xq_export"],
    "monthly_revenue": ["finmind", "twse", "mops", "csv", "xq_export"],
    "institutional":   ["finmind", "twse", "tpex", "csv", "xq_export"],
    "margin":          ["finmind", "twse", "tpex", "csv", "xq_export"],
    "fundamental":     ["finmind", "mops", "csv", "xq_export"],
    "intraday":        ["csv", "xq_export", "planned_tick_provider"],
    "tick":            ["planned_tick_provider"],
    "bidask":          ["planned_bidask_provider"],
}

_LOCAL_FALLBACK_PROVIDERS = {"csv", "xq_export"}
_PLANNED_PROVIDERS = {"twse", "tpex", "mops", "mega_readonly_planned", "planned_tick_provider", "planned_bidask_provider"}

# Fallback reasons
_FALLBACK_REASONS = {
    "token_missing":          "API token not configured",
    "network_failure":        "Network/connection failure",
    "provider_unsupported":   "Provider not yet implemented",
    "schema_partial":         "Incomplete schema from provider",
    "stale_data":             "Data too stale for this provider",
    "local_csv_fallback":     "Falling back to local CSV",
    "xq_fallback":            "Falling back to XQ export",
}


class ProviderReliabilityMatrix:
    """
    Provider Reliability & Fallback Matrix engine.

    Parameters
    ----------
    results_dir : data/backtest_results path
    import_root : data/import path root
    report_dir  : reports path
    mode        : 'real' or 'mock'
    """

    read_only         = True
    no_real_orders    = True
    production_blocked = True

    def __init__(
        self,
        results_dir: str = "data/backtest_results",
        import_root: str = "data/import",
        report_dir:  str = "reports",
        mode:        str = "real",
    ):
        self.mode         = mode
        self._results_dir = os.path.join(_BASE_DIR, results_dir) if not os.path.isabs(results_dir) else results_dir
        self._import_root = os.path.join(_BASE_DIR, import_root) if not os.path.isabs(import_root) else import_root
        self._report_dir  = os.path.join(_BASE_DIR, report_dir)  if not os.path.isabs(report_dir)  else report_dir

        self._metrics: dict = {}
        self._freshness: dict = {}
        self._health: dict = {}

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """Run the full reliability matrix and return result dict."""
        generated_at = datetime.now().isoformat()

        # Collect metrics
        try:
            from data.providers.provider_metrics import ProviderMetricsCollector
            collector = ProviderMetricsCollector(
                results_dir=self._results_dir,
                logs_dir=os.path.join(_BASE_DIR, "logs"),
                reports_dir=self._report_dir,
            )
            self._metrics = collector.collect()
        except Exception as exc:
            logger.warning("ProviderMetricsCollector: %s", exc)
            self._metrics = {}

        # Collect freshness data
        try:
            from data.providers.data_freshness import DataFreshnessChecker
            fc = DataFreshnessChecker(import_root=_BASE_DIR)
            self._freshness = fc.run_all().get("datasets", {})
        except Exception as exc:
            logger.warning("DataFreshnessChecker: %s", exc)
            self._freshness = {}

        # Collect health data
        try:
            from data.providers.provider_health import ProviderHealthChecker
            hc = ProviderHealthChecker()
            hr = hc.run_all()
            self._health = {p["provider_name"]: p for p in hr.get("providers", [])}
        except Exception as exc:
            logger.warning("ProviderHealthChecker: %s", exc)
            self._health = {}

        # Build matrices
        provider_summary     = self.build_provider_summary()
        dataset_matrix       = self.build_dataset_provider_matrix()
        fallback_matrix      = self.build_fallback_matrix()
        reliability_scores   = self.calculate_provider_success_rate()
        confidence_scores    = self.calculate_dataset_confidence_score()
        reliability_summary  = self.build_reliability_summary(
            provider_summary, dataset_matrix, fallback_matrix, confidence_scores
        )

        warnings = self._collect_warnings(provider_summary, confidence_scores)
        recommendations = self._collect_recommendations(provider_summary, confidence_scores)

        return {
            "mode":                    self.mode,
            "generated_at":            generated_at,
            "read_only":               True,
            "no_real_orders":          True,
            "production_blocked":      True,
            "mock_fallback_disabled":  True,
            "provider_summary":        provider_summary,
            "dataset_matrix":          dataset_matrix,
            "fallback_matrix":         fallback_matrix,
            "reliability_scores":      reliability_scores,
            "dataset_confidence_scores": confidence_scores,
            "reliability_summary":     reliability_summary,
            "warnings":                warnings,
            "recommendations":         recommendations,
        }

    # ------------------------------------------------------------------
    # Provider summary
    # ------------------------------------------------------------------

    def build_provider_summary(self) -> List[dict]:
        """Build per-provider reliability summary."""
        summaries = []
        all_providers = list(set(
            list(_PLANNED_PROVIDERS) + list(_LOCAL_FALLBACK_PROVIDERS) +
            ["finmind", "csv", "xq_export"]
        ))

        for pname in sorted(all_providers):
            metrics = self._metrics.get("providers", {}).get(pname, {})
            health  = self._health.get(pname, {})
            is_planned = pname in _PLANNED_PROVIDERS
            is_local   = pname in _LOCAL_FALLBACK_PROVIDERS

            success_rate     = metrics.get("success_rate", None)
            failure_rate     = metrics.get("failure_rate", None)
            latency_score    = metrics.get("latency_score", None)
            row_coverage     = metrics.get("row_coverage_score", None)
            freshness_score  = metrics.get("freshness_score", None)

            if success_rate is not None and failure_rate is None:
                failure_rate = 1.0 - success_rate

            # Compute reliability_score
            if success_rate is not None:
                rs_components = [
                    success_rate * 0.40,
                    (latency_score or 0.5) * 0.20,
                    (row_coverage or 0.5) * 0.20,
                    (freshness_score or 0.5) * 0.20,
                ]
                reliability_score = round(sum(rs_components) * 100, 1)
            else:
                reliability_score = None

            status = health.get("status", "PLANNED" if is_planned else "UNKNOWN")
            token_configured = health.get("token_configured", False)

            summaries.append({
                "provider_name":      pname,
                "status":             status,
                "read_only":          True,
                "token_configured":   token_configured,
                "supports_real_orders": False,
                "is_local_provider":  is_local,
                "is_planned":         is_planned,
                "success_rate":       success_rate,
                "failure_rate":       failure_rate,
                "latency_score":      latency_score,
                "row_coverage_score": row_coverage,
                "freshness_score":    freshness_score,
                "reliability_score":  reliability_score,
                "last_success_at":    metrics.get("last_success_at", ""),
                "last_failure_at":    metrics.get("last_failure_at", ""),
                "recommended_usage":  self._get_recommended_usage(pname, status, is_local, is_planned),
            })
        return summaries

    def _get_recommended_usage(self, pname, status, is_local, is_planned) -> str:
        if is_planned:
            return "Planned for v0.4+ — not yet available"
        if is_local:
            return "Local fallback — use when API providers unavailable"
        if pname == "finmind":
            return "Primary provider for most datasets — set FINMIND_TOKEN for full access"
        return "Available as fallback"

    # ------------------------------------------------------------------
    # Dataset matrix
    # ------------------------------------------------------------------

    def build_dataset_provider_matrix(self) -> List[dict]:
        """Build per-dataset fallback matrix."""
        rows = []
        for dataset, chain in _DATASET_FALLBACK_CHAINS.items():
            primary  = chain[0] if chain else ""
            fb1      = chain[1] if len(chain) > 1 else ""
            fb2      = chain[2] if len(chain) > 2 else ""
            local_fb = next((p for p in chain if p in _LOCAL_FALLBACK_PROVIDERS), "")

            freshness_info = self._freshness.get(dataset) or self._freshness.get(dataset.replace("daily_price", "daily_k"), {})
            freshness_status = freshness_info.get("status", "UNKNOWN") if freshness_info else "UNKNOWN"
            coverage_ratio   = freshness_info.get("coverage_ratio", 0.0) if freshness_info else 0.0
            missing_symbols  = freshness_info.get("missing_symbols", []) if freshness_info else []

            # Confidence score
            confidence_scores = self.calculate_dataset_confidence_score()
            conf_entry = confidence_scores.get(dataset, {})
            confidence_score = conf_entry.get("score", 0.0)
            confidence_level = conf_entry.get("level", "UNKNOWN")

            # Provider used last run (from metrics)
            provider_used_last = self._metrics.get("dataset_last_provider", {}).get(dataset, "")

            recommendation = self._dataset_recommendation(dataset, confidence_level, freshness_status)

            rows.append({
                "dataset":               dataset,
                "primary_provider":      primary,
                "fallback_1":            fb1,
                "fallback_2":            fb2,
                "local_fallback":        local_fb,
                "provider_used_last_run": provider_used_last,
                "confidence_score":      confidence_score,
                "confidence_level":      confidence_level,
                "freshness_status":      freshness_status,
                "coverage_ratio":        coverage_ratio,
                "missing_symbols":       missing_symbols[:10],
                "recommendation":        recommendation,
            })
        return rows

    def _dataset_recommendation(self, dataset, confidence_level, freshness_status) -> str:
        if freshness_status in ("MISSING",):
            return f"No data found — run: python main.py provider-auto-fetch --dataset {dataset}"
        if freshness_status in ("OLD",):
            return f"Data is stale — run: python main.py provider-auto-fetch --dataset {dataset}"
        if confidence_level in ("LOW", "WEAK"):
            return "Low confidence — check provider token and data quality"
        if dataset in ("tick", "bidask"):
            return "Planned provider — not yet available"
        if dataset == "intraday":
            return "Use XQ export or CSV import for intraday data"
        return "OK"

    # ------------------------------------------------------------------
    # Fallback matrix
    # ------------------------------------------------------------------

    def build_fallback_matrix(self) -> List[dict]:
        """Build explicit fallback chain per dataset."""
        rows = []
        for dataset, chain in _DATASET_FALLBACK_CHAINS.items():
            rows.append({
                "dataset":         dataset,
                "provider_order":  chain,
                "fallback_reason": {
                    p: ("LOCAL_FALLBACK" if p in _LOCAL_FALLBACK_PROVIDERS
                        else "PLANNED_NOT_AVAILABLE" if p in _PLANNED_PROVIDERS
                        else "API_FALLBACK")
                    for p in chain
                },
                "terminal_fallback": chain[-1] if chain else "",
                "no_mock_fallback":  True,
                "status":            "configured",
            })
        return rows

    # ------------------------------------------------------------------
    # Score calculations
    # ------------------------------------------------------------------

    def calculate_provider_success_rate(self) -> Dict[str, dict]:
        """Return success rate per provider."""
        rates = {}
        for pname, metrics in self._metrics.get("providers", {}).items():
            sr = metrics.get("success_rate")
            rates[pname] = {
                "success_rate":  sr if sr is not None else "UNKNOWN",
                "failure_rate":  (1.0 - sr) if sr is not None else "UNKNOWN",
                "sample_count":  metrics.get("sample_count", 0),
            }
        return rates

    def calculate_provider_latency_score(self) -> Dict[str, float]:
        """Return latency score per provider (0-1)."""
        return {
            pname: metrics.get("latency_score", 0.5)
            for pname, metrics in self._metrics.get("providers", {}).items()
        }

    def calculate_provider_row_coverage_score(self) -> Dict[str, float]:
        """Return row coverage score per provider (0-1)."""
        return {
            pname: metrics.get("row_coverage_score", 0.5)
            for pname, metrics in self._metrics.get("providers", {}).items()
        }

    def calculate_dataset_confidence_score(self) -> Dict[str, dict]:
        """Compute dataset confidence scores using DatasetConfidenceScorer."""
        try:
            from data.providers.dataset_confidence import DatasetConfidenceScorer
            scorer = DatasetConfidenceScorer(
                freshness_data=self._freshness,
                provider_metrics=self._metrics,
                health_data=self._health,
                mode=self.mode,
            )
            return scorer.score_all()
        except Exception as exc:
            logger.warning("DatasetConfidenceScorer: %s", exc)
            return {ds: {"score": 0.0, "level": "UNKNOWN"} for ds in _DATASET_FALLBACK_CHAINS}

    def determine_best_provider_for_dataset(self, dataset_name: str) -> Optional[str]:
        """Return the best available provider for a dataset."""
        chain = _DATASET_FALLBACK_CHAINS.get(dataset_name, [])
        for pname in chain:
            if pname in _PLANNED_PROVIDERS:
                continue
            h = self._health.get(pname, {})
            if h.get("status", "") in ("OK", "PARTIAL", ""):
                return pname
        return chain[0] if chain else None

    def determine_fallback_chain(self, dataset_name: str) -> List[str]:
        """Return the full fallback chain for a dataset."""
        return list(_DATASET_FALLBACK_CHAINS.get(dataset_name, []))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def build_reliability_summary(
        self,
        provider_summary: List[dict],
        dataset_matrix: List[dict],
        fallback_matrix: List[dict],
        confidence_scores: Dict[str, dict],
    ) -> dict:
        """Build overall reliability summary."""
        scores = [
            p["reliability_score"]
            for p in provider_summary
            if p["reliability_score"] is not None and not p["is_planned"]
        ]
        overall_reliability = round(sum(scores) / len(scores), 1) if scores else None

        confidence_vals = [
            v["score"] for v in confidence_scores.values()
            if isinstance(v.get("score"), (int, float))
        ]
        overall_confidence = round(sum(confidence_vals) / len(confidence_vals), 1) if confidence_vals else None

        high_confidence = [
            ds for ds, v in confidence_scores.items()
            if v.get("level") in ("HIGH", "GOOD")
        ]
        weak_datasets = [
            ds for ds, v in confidence_scores.items()
            if v.get("level") in ("WEAK", "LOW")
        ]
        failed_providers = [
            p["provider_name"] for p in provider_summary
            if p["status"] in ("FAILED", "ERROR") and not p["is_planned"]
        ]
        local_fallback_count = sum(
            1 for row in dataset_matrix
            if row.get("provider_used_last_run") in _LOCAL_FALLBACK_PROVIDERS
        )

        return {
            "overall_reliability_score":  overall_reliability,
            "overall_dataset_confidence": overall_confidence,
            "high_confidence_datasets":   high_confidence,
            "weak_datasets":              weak_datasets,
            "failed_providers":           failed_providers,
            "local_fallback_count":       local_fallback_count,
            "mock_fallback_count":        0,
            "providers_checked":          len([p for p in provider_summary if not p["is_planned"]]),
            "datasets_covered":           len(dataset_matrix),
            "read_only":                  True,
            "no_real_orders":             True,
            "production_blocked":         True,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _collect_warnings(self, provider_summary, confidence_scores) -> List[str]:
        warnings = []
        fm = next((p for p in provider_summary if p["provider_name"] == "finmind"), None)
        if fm and not fm.get("token_configured", False):
            warnings.append("FINMIND_TOKEN not configured — FinMind data fetch limited. Set in .env for full access.")
        for ds, v in confidence_scores.items():
            if v.get("level") in ("LOW", "WEAK"):
                warnings.append(f"Dataset '{ds}': confidence {v.get('level')} (score={v.get('score', '?')})")
        return warnings

    def _collect_recommendations(self, provider_summary, confidence_scores) -> List[str]:
        recs = []
        fm = next((p for p in provider_summary if p["provider_name"] == "finmind"), None)
        if fm and not fm.get("token_configured", False):
            recs.append("Set FINMIND_TOKEN in .env to enable FinMind API access")
        for ds, v in confidence_scores.items():
            if v.get("level") in ("LOW",):
                recs.append(f"Run: python main.py provider-auto-fetch --dataset {ds}")
        recs.append("XQ export / CSV local fallback is available for intraday and daily_price")
        recs.append("Production trading remains BLOCKED until REAL_ORDER_READY=True is set")
        return recs
