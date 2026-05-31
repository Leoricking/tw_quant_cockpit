"""
data/providers/auto_fetcher.py - Provider Auto Fetch engine (v0.3.19).

Fetches daily price, monthly revenue, institutional, margin, and fundamental
data from the best available provider and writes to standard CSV paths.

Provider priority: FinMind → TWSE/TPEx/MOPS → CSV existing → XQ existing
Never falls back to mock. Never places real orders.

[!] Read Only. No Real Orders. No Token Logged.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Standard output paths (relative to project root)
_DATASET_PATHS = {
    "daily_price":     "data/import/daily/daily_k.csv",
    "monthly_revenue": "data/import/monthly_revenue/monthly_revenue.csv",
    "institutional":   "data/import/institutional/institutional.csv",
    "margin":          "data/import/margin/margin.csv",
    "fundamental":     "data/import/fundamental/fundamental.csv",
}

# Standard output schemas (column order)
_SCHEMAS = {
    "daily_price": [
        "date", "symbol", "name", "open", "high", "low", "close", "volume",
        "source", "fetched_at",
    ],
    "monthly_revenue": [
        "date", "symbol", "name", "revenue", "revenue_mom", "revenue_yoy",
        "cumulative_revenue", "cumulative_yoy", "source", "fetched_at",
    ],
    "institutional": [
        "date", "symbol", "foreign_net_buy", "trust_net_buy", "dealer_net_buy",
        "total_net_buy", "source", "fetched_at",
    ],
    "margin": [
        "date", "symbol", "margin_balance", "margin_change",
        "short_balance", "short_change", "source", "fetched_at",
    ],
    "fundamental": [
        "date", "symbol", "eps", "gross_margin", "operating_margin", "net_income",
        "announcement_date", "announcement_date_source", "announcement_date_is_estimated",
        "source", "fetched_at",
    ],
}

# Provider priority order per dataset
_PROVIDER_PRIORITY = {
    "daily_price":     ["finmind", "twse", "csv", "xq_export"],
    "monthly_revenue": ["finmind", "twse", "csv", "xq_export"],
    "institutional":   ["finmind", "twse", "csv", "xq_export"],
    "margin":          ["finmind", "twse", "csv", "xq_export"],
    "fundamental":     ["finmind", "mops", "csv", "xq_export"],
}


class DataProviderAutoFetcher:
    """
    Fetches data from the best available provider and writes to standard CSV paths.

    Parameters
    ----------
    mode           : "real" or "mock"
    universe       : List of symbol strings (None = load from universe manifest)
    provider_order : Override provider priority list
    output_root    : Root for data/import/ (default: project root)
    results_dir    : Backtest results dir (unused in v0.3.19)
    report_dir     : Report output dir
    max_symbols    : Limit number of symbols (None = all)
    months         : Lookback months for time-series data (default 24)
    dry_run        : If True, fetch but do not write files
    replace        : If True, replace existing CSV; otherwise merge (append+dedup)
    """

    # Safety invariants
    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        mode:           str = "real",
        universe:       Optional[List[str]] = None,
        provider_order: Optional[Dict[str, List[str]]] = None,
        output_root:    Optional[str] = None,
        results_dir:    Optional[str] = None,
        report_dir:     Optional[str] = None,
        max_symbols:    Optional[int] = None,
        months:         int = 24,
        dry_run:        bool = False,
        replace:        bool = False,
    ):
        self.mode           = mode
        self._universe      = universe
        self._provider_order = provider_order or _PROVIDER_PRIORITY
        self._output_root   = output_root or _BASE_DIR
        self._report_dir    = report_dir or os.path.join(_BASE_DIR, "reports")
        self._max_symbols   = max_symbols
        self.months         = months
        self.dry_run        = dry_run
        self.replace        = replace

        # Runtime state
        self._health: dict = {}
        self._datasets_requested: List[str] = list(_DATASET_PATHS.keys())
        self._fetch_results: Dict[str, dict] = {}

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def run(self, datasets: Optional[List[str]] = None) -> dict:
        """
        Run the full auto-fetch pipeline.
        Returns a summary dict with status, datasets, providers_used, etc.
        """
        started = datetime.now()

        if datasets:
            self._datasets_requested = [d for d in datasets if d in _DATASET_PATHS]
        else:
            self._datasets_requested = list(_DATASET_PATHS.keys())

        # Safety check
        self._check_no_real_orders()

        # Load universe
        symbols = self._load_universe()
        if not symbols:
            return self._make_summary(started, warnings=["No symbols in universe — skipping all fetches"])

        # Run provider health check (lightweight)
        self._run_health_check()

        # Fetch each dataset
        providers_used: List[str] = []
        for ds in self._datasets_requested:
            result = self._fetch_dataset(ds, symbols)
            self._fetch_results[ds] = result
            if result.get("provider_used") and result["provider_used"] not in providers_used:
                providers_used.append(result["provider_used"])

        # Freshness check after fetch
        freshness = self._run_freshness()

        return self._make_summary(started, providers_used=providers_used, freshness=freshness)

    # ------------------------------------------------------------------
    # Individual dataset fetchers
    # ------------------------------------------------------------------

    def fetch_daily_price(self, symbols: List[str]) -> dict:
        """Fetch daily OHLCV price data."""
        import pandas as pd
        fetched_at = datetime.utcnow().isoformat()
        rows: list = []
        provider_used = ""
        warnings: list = []
        errors: list   = []

        for pname in self._get_provider_order("daily_price"):
            if not self._provider_ok(pname):
                continue
            try:
                instance = self._get_provider(pname)
                if instance is None:
                    continue
                fn = getattr(instance, "get_daily_price", None) or getattr(instance, "get_daily", None)
                if fn is None:
                    continue

                for sym in symbols[:self._effective_max()]:
                    try:
                        df = fn(sym)
                        if df is not None and not df.empty:
                            df = df.copy()
                            df["symbol"]     = str(sym)
                            df["name"]       = df.get("name", "")
                            df["source"]     = pname
                            df["fetched_at"] = fetched_at
                            rows.append(df)
                    except Exception as exc:
                        warnings.append(f"daily_price/{sym}/{pname}: {exc}")

                if rows:
                    provider_used = pname
                    break
            except Exception as exc:
                warnings.append(f"daily_price/{pname}: {exc}")

        return self._build_result("daily_price", rows, provider_used, warnings, errors, fetched_at)

    def fetch_monthly_revenue(self, symbols: List[str]) -> dict:
        """Fetch monthly revenue data."""
        import pandas as pd
        fetched_at = datetime.utcnow().isoformat()
        rows: list = []
        provider_used = ""
        warnings: list = []
        errors: list   = []

        for pname in self._get_provider_order("monthly_revenue"):
            if not self._provider_ok(pname):
                continue
            try:
                instance = self._get_provider(pname)
                if instance is None:
                    continue
                fn = getattr(instance, "get_monthly_revenue", None)
                if fn is None:
                    continue

                for sym in symbols[:self._effective_max()]:
                    try:
                        df = fn(sym, months=self.months)
                        if df is not None and not df.empty:
                            df = df.copy()
                            df["symbol"]     = str(sym)
                            df["source"]     = pname
                            df["fetched_at"] = fetched_at
                            # Standardise column names
                            rename = {
                                "revenue_growth_m/m": "revenue_mom",
                                "revenue_growth_y/y": "revenue_yoy",
                                "accumulated_revenue": "cumulative_revenue",
                                "accumulated_yoy":     "cumulative_yoy",
                                "month":               "date",
                            }
                            df = df.rename(columns=rename)
                            rows.append(df)
                    except Exception as exc:
                        warnings.append(f"monthly_revenue/{sym}/{pname}: {exc}")

                if rows:
                    provider_used = pname
                    break
            except Exception as exc:
                warnings.append(f"monthly_revenue/{pname}: {exc}")

        return self._build_result("monthly_revenue", rows, provider_used, warnings, errors, fetched_at)

    def fetch_institutional(self, symbols: List[str]) -> dict:
        """Fetch institutional net-buy data."""
        fetched_at = datetime.utcnow().isoformat()
        rows: list = []
        provider_used = ""
        warnings: list = []
        errors: list   = []

        for pname in self._get_provider_order("institutional"):
            if not self._provider_ok(pname):
                continue
            try:
                instance = self._get_provider(pname)
                if instance is None:
                    continue
                fn = getattr(instance, "get_institutional", None)
                if fn is None:
                    continue

                for sym in symbols[:self._effective_max()]:
                    try:
                        df = fn(sym)
                        if df is not None and not df.empty:
                            df = df.copy()
                            df["symbol"]     = str(sym)
                            df["source"]     = pname
                            df["fetched_at"] = fetched_at
                            # Compute total_net_buy if missing
                            if "total_net_buy" not in df.columns:
                                cols = ["foreign_net_buy", "trust_net_buy", "dealer_net_buy"]
                                present = [c for c in cols if c in df.columns]
                                if present:
                                    df["total_net_buy"] = df[present].sum(axis=1)
                                else:
                                    df["total_net_buy"] = 0
                            rows.append(df)
                    except Exception as exc:
                        warnings.append(f"institutional/{sym}/{pname}: {exc}")

                if rows:
                    provider_used = pname
                    break
            except Exception as exc:
                warnings.append(f"institutional/{pname}: {exc}")

        return self._build_result("institutional", rows, provider_used, warnings, errors, fetched_at)

    def fetch_margin(self, symbols: List[str]) -> dict:
        """Fetch margin/short-sell balance data."""
        fetched_at = datetime.utcnow().isoformat()
        rows: list = []
        provider_used = ""
        warnings: list = []
        errors: list   = []

        for pname in self._get_provider_order("margin"):
            if not self._provider_ok(pname):
                continue
            try:
                instance = self._get_provider(pname)
                if instance is None:
                    continue
                fn = (getattr(instance, "get_margin", None) or
                      getattr(instance, "get_margin_short", None))
                if fn is None:
                    continue

                for sym in symbols[:self._effective_max()]:
                    try:
                        df = fn(sym)
                        if df is not None and not df.empty:
                            df = df.copy()
                            df["symbol"]     = str(sym)
                            df["source"]     = pname
                            df["fetched_at"] = fetched_at
                            rows.append(df)
                    except Exception as exc:
                        warnings.append(f"margin/{sym}/{pname}: {exc}")

                if rows:
                    provider_used = pname
                    break
            except Exception as exc:
                warnings.append(f"margin/{pname}: {exc}")

        return self._build_result("margin", rows, provider_used, warnings, errors, fetched_at)

    def fetch_fundamental(self, symbols: List[str]) -> dict:
        """Fetch fundamental (EPS, margins) data."""
        fetched_at = datetime.utcnow().isoformat()
        rows: list = []
        provider_used = ""
        warnings: list = []
        errors: list   = []

        for pname in self._get_provider_order("fundamental"):
            if not self._provider_ok(pname):
                continue
            try:
                instance = self._get_provider(pname)
                if instance is None:
                    continue
                fn = (getattr(instance, "get_fundamental", None) or
                      getattr(instance, "get_financial_statement", None))
                if fn is None:
                    continue

                for sym in symbols[:self._effective_max()]:
                    try:
                        df = fn(sym)
                        if df is not None and not df.empty:
                            df = df.copy()
                            df["symbol"]     = str(sym)
                            df["source"]     = pname
                            df["fetched_at"] = fetched_at
                            # Estimated announcement dates if not present
                            if "announcement_date" not in df.columns:
                                df["announcement_date"] = None
                            if "announcement_date_source" not in df.columns:
                                df["announcement_date_source"] = "estimated"
                            if "announcement_date_is_estimated" not in df.columns:
                                df["announcement_date_is_estimated"] = True
                            # Date column from year/quarter if missing
                            if "date" not in df.columns:
                                if "year" in df.columns and "quarter" in df.columns:
                                    _qmap = {"Q1": "03", "Q2": "06", "Q3": "09", "Q4": "12"}
                                    df["date"] = df.apply(
                                        lambda r: f"{r['year']}-{_qmap.get(str(r.get('quarter','')), '12')}-01",
                                        axis=1,
                                    )
                            rows.append(df)
                    except Exception as exc:
                        warnings.append(f"fundamental/{sym}/{pname}: {exc}")

                if rows:
                    provider_used = pname
                    break
            except Exception as exc:
                warnings.append(f"fundamental/{pname}: {exc}")

        return self._build_result("fundamental", rows, provider_used, warnings, errors, fetched_at)

    # ------------------------------------------------------------------
    # Internal: dataset dispatch
    # ------------------------------------------------------------------

    def _fetch_dataset(self, dataset_name: str, symbols: List[str]) -> dict:
        _dispatch = {
            "daily_price":     self.fetch_daily_price,
            "monthly_revenue": self.fetch_monthly_revenue,
            "institutional":   self.fetch_institutional,
            "margin":          self.fetch_margin,
            "fundamental":     self.fetch_fundamental,
        }
        fn = _dispatch.get(dataset_name)
        if fn is None:
            return {"status": "SKIPPED", "dataset": dataset_name,
                    "provider_used": "", "rows_fetched": 0, "rows_written": 0,
                    "warnings": [f"Unknown dataset: {dataset_name}"], "errors": []}
        try:
            return fn(symbols)
        except Exception as exc:
            return {"status": "FAILED", "dataset": dataset_name,
                    "provider_used": "", "rows_fetched": 0, "rows_written": 0,
                    "warnings": [], "errors": [str(exc)]}

    # ------------------------------------------------------------------
    # Provider selection
    # ------------------------------------------------------------------

    def select_provider(self, dataset_name: str) -> Optional[str]:
        """Return the name of the best available provider for the dataset."""
        # v0.3.24: try to use fallback chain from registry first
        try:
            from data.providers.provider_registry import ProviderRegistry
            reg = ProviderRegistry()
            chain = reg.get_provider_fallback_chain(dataset_name)
            if chain:
                for pname in chain:
                    if self._provider_ok(pname):
                        return pname
        except Exception:
            pass
        for pname in self._get_provider_order(dataset_name):
            if self._provider_ok(pname):
                return pname
        return None

    def _get_provider_order(self, dataset_name: str) -> List[str]:
        return self._provider_order.get(dataset_name, list(_PROVIDER_PRIORITY.get(dataset_name, [])))

    def _provider_ok(self, pname: str) -> bool:
        """Return True if the provider is reachable/configured based on health check."""
        if not self._health:
            return True  # no health data yet — optimistic
        for p in self._health.get("providers", []):
            if p.get("provider_name") == pname:
                status = p.get("status", "")
                # Only use providers that are OK or PARTIAL
                return status in ("OK", "PARTIAL")
        return True  # unknown = optimistic

    def _get_provider(self, pname: str) -> Any:
        try:
            from data.providers.provider_registry import ProviderRegistry
            reg = ProviderRegistry()
            return reg.get_provider_instance(pname)
        except Exception as exc:
            logger.debug("_get_provider %s: %s", pname, exc)
            return None

    # ------------------------------------------------------------------
    # CSV output
    # ------------------------------------------------------------------

    def write_standard_csv(self, dataset_name: str, df) -> dict:
        """Write df to the standard CSV path. Returns {"path", "rows_written", "error"}."""
        import pandas as pd

        rel_path = _DATASET_PATHS.get(dataset_name)
        if rel_path is None:
            return {"path": None, "rows_written": 0, "error": f"Unknown dataset: {dataset_name}"}

        abs_path = os.path.join(self._output_root, rel_path)
        schema   = _SCHEMAS.get(dataset_name, [])

        if self.dry_run:
            return {"path": abs_path, "rows_written": len(df), "error": None, "dry_run": True}

        # Normalise columns — add missing with NaN, drop extra
        for col in schema:
            if col not in df.columns:
                df[col] = None
        df = df[[c for c in schema if c in df.columns]]

        merged = self.merge_with_existing(dataset_name, df)
        valid  = self.validate_output(dataset_name, merged)
        if not valid.get("ok", True):
            return {"path": abs_path, "rows_written": 0, "error": valid.get("error", "validation failed")}

        try:
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            merged.to_csv(abs_path, index=False)
            return {"path": abs_path, "rows_written": len(merged), "error": None}
        except Exception as exc:
            return {"path": abs_path, "rows_written": 0, "error": str(exc)}

    def merge_with_existing(self, dataset_name: str, new_df):
        """Merge new_df with existing CSV (append + dedup on date+symbol)."""
        import pandas as pd

        if self.replace:
            return new_df

        rel_path = _DATASET_PATHS.get(dataset_name, "")
        abs_path = os.path.join(self._output_root, rel_path)

        if not os.path.isfile(abs_path):
            return new_df

        try:
            existing = pd.read_csv(abs_path, low_memory=False)
            combined = pd.concat([existing, new_df], ignore_index=True)
            # Dedup: keep last (newest fetch) per date+symbol
            key_cols = ["date", "symbol"]
            key_cols = [c for c in key_cols if c in combined.columns]
            if key_cols:
                combined = combined.drop_duplicates(subset=key_cols, keep="last")
            combined = combined.sort_values(key_cols).reset_index(drop=True) if key_cols else combined
            return combined
        except Exception as exc:
            logger.warning("merge_with_existing %s: %s — using new data only", dataset_name, exc)
            return new_df

    def validate_output(self, dataset_name: str, df) -> dict:
        """Basic validation: non-empty, required columns present."""
        schema = _SCHEMAS.get(dataset_name, [])
        required = ["date", "symbol"]
        for col in required:
            if col not in df.columns:
                return {"ok": False, "error": f"Missing required column '{col}' in {dataset_name}"}
        if df.empty:
            return {"ok": False, "error": f"Empty DataFrame for {dataset_name}"}
        return {"ok": True}

    # ------------------------------------------------------------------
    # Build result / summary
    # ------------------------------------------------------------------

    def _build_result(
        self,
        dataset_name:  str,
        rows:          list,
        provider_used: str,
        warnings:      list,
        errors:        list,
        fetched_at:    str,
    ) -> dict:
        import pandas as pd

        if not rows:
            status = "FAILED" if not warnings else "PARTIAL"
            return {
                "dataset":       dataset_name,
                "status":        status,
                "provider_used": provider_used,
                "rows_fetched":  0,
                "rows_written":  0,
                "output_file":   _DATASET_PATHS.get(dataset_name, ""),
                "warnings":      warnings,
                "errors":        errors,
            }

        try:
            df = pd.concat(rows, ignore_index=True)
        except Exception as exc:
            return {
                "dataset":       dataset_name,
                "status":        "FAILED",
                "provider_used": provider_used,
                "rows_fetched":  0,
                "rows_written":  0,
                "output_file":   _DATASET_PATHS.get(dataset_name, ""),
                "warnings":      warnings,
                "errors":        errors + [str(exc)],
            }

        rows_fetched = len(df)
        write_result = self.write_standard_csv(dataset_name, df)
        rows_written = write_result.get("rows_written", 0)
        if write_result.get("error"):
            errors.append(f"write: {write_result['error']}")

        status = "OK" if not errors else ("PARTIAL" if rows_written > 0 else "FAILED")

        # v0.3.24: classify local fallback and record fallback_reason
        _LOCAL_PROVIDERS = {"csv", "xq_export"}
        is_local_fallback = provider_used in _LOCAL_PROVIDERS
        fallback_reason = ""
        if is_local_fallback:
            fallback_reason = "LOCAL_FALLBACK"
        elif provider_used and provider_used not in ("finmind",):
            fallback_reason = "API_FALLBACK"

        return {
            "dataset":          dataset_name,
            "status":           status,
            "provider_used":    provider_used,
            "primary_provider": self._get_provider_order(dataset_name)[0] if self._get_provider_order(dataset_name) else "",
            "fallback_provider": provider_used if fallback_reason else "",
            "fallback_reason":  fallback_reason,
            "is_local_fallback": is_local_fallback,
            "rows_fetched":     rows_fetched,
            "rows_written":     rows_written,
            "output_file":      write_result.get("path", ""),
            "warnings":         warnings,
            "errors":           errors,
            "dry_run":          self.dry_run,
        }

    def build_fetch_summary(self) -> dict:
        """Return aggregated fetch summary from self._fetch_results."""
        total_rows_fetched  = sum(r.get("rows_fetched", 0) for r in self._fetch_results.values())
        total_rows_written  = sum(r.get("rows_written", 0) for r in self._fetch_results.values())
        all_warnings = []
        all_errors   = []
        for r in self._fetch_results.values():
            all_warnings.extend(r.get("warnings", []))
            all_errors.extend(r.get("errors", []))
        return {
            "datasets":     self._fetch_results,
            "rows_fetched": total_rows_fetched,
            "rows_written": total_rows_written,
            "warnings":     all_warnings,
            "errors":       all_errors,
        }

    def _make_summary(
        self,
        started,
        providers_used: Optional[List[str]] = None,
        freshness:      Optional[dict] = None,
        warnings:       Optional[list] = None,
    ) -> dict:
        fetch_summary = self.build_fetch_summary()
        all_warnings  = (warnings or []) + fetch_summary.get("warnings", [])
        all_errors    = fetch_summary.get("errors", [])
        status = "OK" if not all_errors and not all_warnings else \
                 ("PARTIAL" if not all_errors else "FAILED")

        # Build structured warning details (v0.3.22)
        warning_details = []
        for w in all_warnings:
            w_str = str(w)
            if "token" in w_str.lower() or "422" in w_str or "401" in w_str or "403" in w_str:
                warning_details.append({
                    "message":    w_str,
                    "cause":      "API token not configured or request rejected by provider",
                    "next_step":  "Set FINMIND_TOKEN in .env or run: python main.py provider-health --create-env-example",
                    "can_ignore": True,
                })
            elif "timeout" in w_str.lower() or "connection" in w_str.lower():
                warning_details.append({
                    "message":    w_str,
                    "cause":      "Network timeout or connection failure",
                    "next_step":  "Check internet connection and retry",
                    "can_ignore": True,
                })
            else:
                warning_details.append({
                    "message":    w_str,
                    "cause":      "Data fetch warning",
                    "next_step":  "Check logs for details",
                    "can_ignore": True,
                })

        return {
            "status":            status,
            "mode":              self.mode,
            "read_only":         True,
            "no_real_orders":    True,
            "dry_run":           self.dry_run,
            "started_at":        started.isoformat(),
            "finished_at":       datetime.now().isoformat(),
            "datasets_requested": self._datasets_requested,
            "datasets":          fetch_summary.get("datasets", {}),
            "providers_used":    providers_used or [],
            "rows_fetched":      fetch_summary.get("rows_fetched", 0),
            "rows_written":      fetch_summary.get("rows_written", 0),
            "warnings":          all_warnings,
            "warning_details":   warning_details,
            "errors":            all_errors,
            "output_files":      {
                k: v.get("output_file", "") for k, v in fetch_summary.get("datasets", {}).items()
            },
            "freshness_summary": freshness or {},
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_universe(self) -> List[str]:
        """Load universe symbol list."""
        if self._universe:
            syms = list(self._universe)
            if self._max_symbols:
                syms = syms[:self._max_symbols]
            return syms
        # Try universe manifest
        try:
            import pandas as pd
            manifest_path = os.path.join(_BASE_DIR, "data", "universe", "universe_manifest.csv")
            if os.path.isfile(manifest_path):
                df = pd.read_csv(manifest_path, low_memory=False)
                col = next((c for c in ["symbol", "code", "ticker"] if c in df.columns), None)
                if col:
                    syms = df[col].dropna().astype(str).unique().tolist()
                    if self._max_symbols:
                        syms = syms[:self._max_symbols]
                    logger.info("Loaded %d symbols from universe manifest", len(syms))
                    return syms
        except Exception as exc:
            logger.debug("_load_universe from manifest: %s", exc)
        # Fallback: load from daily CSV
        try:
            import pandas as pd
            daily_path = os.path.join(_BASE_DIR, "data", "import", "daily", "daily_k.csv")
            if os.path.isfile(daily_path):
                df = pd.read_csv(daily_path, low_memory=False, usecols=["symbol"])
                syms = df["symbol"].dropna().astype(str).unique().tolist()
                if self._max_symbols:
                    syms = syms[:self._max_symbols]
                logger.info("Loaded %d symbols from daily_k.csv", len(syms))
                return syms
        except Exception as exc:
            logger.debug("_load_universe from daily_k: %s", exc)
        logger.warning("No universe found — auto fetch will be skipped")
        return []

    def _run_health_check(self) -> None:
        """Run provider health check and store results."""
        try:
            from data.providers.provider_health import ProviderHealthChecker
            checker    = ProviderHealthChecker()
            self._health = checker.run_all()
        except Exception as exc:
            logger.debug("_run_health_check: %s", exc)
            self._health = {}

    def _run_freshness(self) -> dict:
        """Run freshness check after fetching."""
        try:
            from data.providers.data_freshness import DataFreshnessChecker
            checker = DataFreshnessChecker(import_root=self._output_root)
            result  = checker.run_all()
            return {
                name: {
                    "status":      info.get("status", ""),
                    "latest_date": info.get("latest_date", ""),
                    "rows":        info.get("rows", 0),
                }
                for name, info in result.get("datasets", {}).items()
            }
        except Exception as exc:
            logger.debug("_run_freshness: %s", exc)
            return {}

    def _effective_max(self) -> int:
        """Effective max symbols per dataset."""
        return self._max_symbols if self._max_symbols else 9999

    def _check_no_real_orders(self) -> None:
        """Safety: verify no provider supports real orders."""
        try:
            from data.providers.provider_registry import ProviderRegistry
            reg = ProviderRegistry()
            reg.assert_no_real_orders()
        except AssertionError as exc:
            raise RuntimeError(f"[SAFETY] {exc}") from exc
        except Exception:
            pass
