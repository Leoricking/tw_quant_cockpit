"""
ml/feature_snapshot.py — ML Feature Snapshot Builder (v0.4.2).

Builds a feature matrix from available data sources.
Does NOT use future data for features.
Output: data/ml_features/feature_snapshot_YYYYMMDD_HHMMSS.csv (not committed).

[!] ML Research Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No data leakage. Features use only data known at feature date.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FeatureSnapshotBuilder:
    """
    Builds feature snapshots from available data sources.

    Parameters
    ----------
    mode        : "real" or "mock"
    universe    : Optional universe name filter
    import_root : Root directory for imported data
    results_dir : Root directory for backtest results
    output_root : Root directory for ML feature outputs
    """

    read_only      = True
    no_real_orders = True

    def __init__(
        self,
        mode:        str = "real",
        universe:    Optional[str] = None,
        import_root: str = "data/import",
        results_dir: str = "data/backtest_results",
        output_root: str = "data/ml_features",
    ):
        self.mode        = mode
        self.universe    = universe
        self.import_root = os.path.join(_BASE_DIR, import_root) if not os.path.isabs(import_root) else import_root
        self.results_dir = os.path.join(_BASE_DIR, results_dir) if not os.path.isabs(results_dir) else results_dir
        self.output_root = os.path.join(_BASE_DIR, output_root) if not os.path.isabs(output_root) else output_root
        os.makedirs(self.output_root, exist_ok=True)

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------

    def build(
        self,
        symbols:    Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date:   Optional[str] = None,
    ) -> Tuple[object, dict]:
        """
        Build feature snapshot for given symbols and date range.

        Returns (feature_df, summary)
        """
        try:
            import pandas as pd

            logger.info("FeatureSnapshotBuilder.build: mode=%s symbols=%s", self.mode, symbols)

            # 1. Load available symbols
            if symbols is None:
                symbols = self._load_available_symbols()
            if not symbols:
                logger.warning("FeatureSnapshotBuilder: no symbols available")
                return pd.DataFrame(), {"status": "NO_DATA", "warnings": ["No symbols available"]}

            # 2. Build per-symbol feature frames
            frames = []
            warnings = []
            for sym in symbols[:50]:  # cap at 50 symbols for v1
                try:
                    daily_f = self.build_daily_features(sym, start_date=start_date, end_date=end_date)
                    if daily_f is not None and not daily_f.empty:
                        frames.append(daily_f)
                except Exception as exc:
                    warnings.append(f"{sym}: {exc}")

            if not frames:
                return pd.DataFrame(), {"status": "NO_DATA", "warnings": warnings}

            # 3. Merge
            df = pd.concat(frames, ignore_index=True)
            df = self.merge_features([df])

            # 4. Write
            path, summary_path = self.write_snapshot(df)

            summary = {
                "status":        "OK",
                "feature_count": len([c for c in df.columns if c not in ("symbol", "date")]),
                "row_count":     len(df),
                "symbol_count":  df["symbol"].nunique() if "symbol" in df.columns else 0,
                "date_range":    (
                    str(df["date"].min()) if "date" in df.columns and not df["date"].empty else "",
                    str(df["date"].max()) if "date" in df.columns and not df["date"].empty else "",
                ),
                "output_path":   path,
                "summary_path":  summary_path,
                "warnings":      warnings,
            }
            return df, summary

        except Exception as exc:
            logger.warning("FeatureSnapshotBuilder.build: %s", exc)
            try:
                import pandas as pd
                return pd.DataFrame(), {"status": "ERROR", "error": str(exc)}
            except Exception:
                return None, {"status": "ERROR", "error": str(exc)}

    # ------------------------------------------------------------------
    # Feature builders
    # ------------------------------------------------------------------

    def build_daily_features(
        self,
        symbol:     str,
        start_date: Optional[str] = None,
        end_date:   Optional[str] = None,
    ):
        """Build daily price/technical/volume features for one symbol."""
        try:
            import pandas as pd
            import numpy as np

            # Load daily price data
            df = self._load_daily_price(symbol)
            if df is None or df.empty:
                return None

            df = df.sort_values("date").reset_index(drop=True)
            if start_date:
                df = df[df["date"] >= start_date]
            if end_date:
                df = df[df["date"] <= end_date]
            if df.empty:
                return None

            close = df["close"].astype(float)
            vol   = df["volume"].astype(float) if "volume" in df.columns else pd.Series([float("nan")] * len(df))
            high  = df["high"].astype(float) if "high" in df.columns else close
            low   = df["low"].astype(float) if "low" in df.columns else close

            # Price returns (no future data)
            df["price.close_return_1d"]  = close.pct_change(1)
            df["price.close_return_5d"]  = close.pct_change(5)
            df["price.close_return_20d"] = close.pct_change(20)
            df["price.volatility_20d"]   = close.pct_change().rolling(20).std()
            df["price.high_low_range_pct"] = (high - low) / close.where(close != 0, other=float("nan"))

            # Moving average gaps (no future data)
            for w in (5, 10, 20, 60):
                ma = close.rolling(w).mean()
                df[f"tech.ma{w}_gap"] = (close - ma) / ma.where(ma != 0, other=float("nan"))

            # MACD
            ema12 = close.ewm(span=12, adjust=False).mean()
            ema26 = close.ewm(span=26, adjust=False).mean()
            dif   = ema12 - ema26
            signal = dif.ewm(span=9, adjust=False).mean()
            df["tech.macd_dif"]    = dif
            df["tech.macd_signal"] = signal
            df["tech.macd_osc"]    = dif - signal

            # RSI
            for period in (6, 12):
                delta = close.diff()
                gain  = delta.clip(lower=0).rolling(period).mean()
                loss  = (-delta.clip(upper=0)).rolling(period).mean()
                rs    = gain / loss.where(loss != 0, other=float("nan"))
                df[f"tech.rsi{period}"] = 100 - (100 / (1 + rs))

            # KD
            low_min  = low.rolling(9).min()
            high_max = high.rolling(9).max()
            rsv = (close - low_min) / (high_max - low_min).where((high_max - low_min) != 0, other=float("nan")) * 100
            k = rsv.ewm(com=2, adjust=False).mean()
            d = k.ewm(com=2, adjust=False).mean()
            df["tech.kd_k"] = k
            df["tech.kd_d"] = d

            # Volume features (no future data)
            if not vol.isna().all():
                df["vol.volume_ratio_5d"]     = vol / vol.rolling(5).mean()
                df["vol.volume_ratio_20d"]     = vol / vol.rolling(20).mean()
                df["vol.turnover_value"]       = close * vol
                df["vol.volume_breakout_flag"] = (vol > vol.rolling(20).mean() * 2).astype(float)
            else:
                for c in ("vol.volume_ratio_5d", "vol.volume_ratio_20d", "vol.turnover_value", "vol.volume_breakout_flag"):
                    df[c] = float("nan")

            df["symbol"] = symbol
            return df

        except Exception as exc:
            logger.warning("FeatureSnapshotBuilder.build_daily_features %s: %s", symbol, exc)
            return None

    def build_fundamental_features(self, symbol: str):
        """Build fundamental features (EPS, margins, timing quality)."""
        try:
            import pandas as pd
            fin_path = os.path.join(self.import_root, "fundamental", "fundamental.csv")
            if not os.path.exists(fin_path):
                return None
            df = pd.read_csv(fin_path)
            if "symbol" in df.columns or "代號" in df.columns:
                sym_col = "symbol" if "symbol" in df.columns else "代號"
                df = df[df[sym_col].astype(str) == str(symbol)]
            if df.empty:
                return None
            # Rename known columns
            aliases = {"eps": ["eps", "EPS", "每股盈餘"],
                       "gross_margin": ["gross_margin", "毛利率"],
                       "operating_margin": ["operating_margin", "營業利益率"]}
            for std, opts in aliases.items():
                for opt in opts:
                    if opt in df.columns and std not in df.columns:
                        df = df.rename(columns={opt: std})
                        break
            df["symbol"] = symbol
            return df
        except Exception as exc:
            logger.debug("build_fundamental_features %s: %s", symbol, exc)
            return None

    def build_chip_features(self, symbol: str):
        """Build chip / institutional features."""
        try:
            import pandas as pd
            inst_path = os.path.join(self.import_root, "institutional", "institutional.csv")
            if not os.path.exists(inst_path):
                return None
            df = pd.read_csv(inst_path)
            if "symbol" in df.columns:
                df = df[df["symbol"].astype(str) == str(symbol)]
            if df.empty:
                return None

            aliases = {
                "chip.foreign_net_buy":           ["foreign_net_buy", "外資買賣超"],
                "chip.trust_net_buy":             ["trust_net_buy", "投信買賣超"],
                "chip.dealer_net_buy":            ["dealer_net_buy", "自營商買賣超"],
                "chip.institutional_total_net_buy": ["institutional_total_net_buy"],
            }
            for std, opts in aliases.items():
                for opt in opts:
                    if opt in df.columns and std not in df.columns:
                        df = df.rename(columns={opt: std})
                        break

            df["symbol"] = symbol
            return df
        except Exception as exc:
            logger.debug("build_chip_features %s: %s", symbol, exc)
            return None

    def build_intraday_features(self, symbol: str):
        """Build intraday features (returns None if no intraday data)."""
        try:
            import pandas as pd
            intra_base = os.path.join(_BASE_DIR, "data", "import", "intraday_standard", "1min")
            if not os.path.isdir(intra_base):
                return None
            sym_path = os.path.join(intra_base, f"{symbol}_1min.csv")
            if not os.path.exists(sym_path):
                return None
            df = pd.read_csv(sym_path)
            df["symbol"] = symbol
            return df
        except Exception as exc:
            logger.debug("build_intraday_features %s: %s", symbol, exc)
            return None

    def build_quality_features(self, symbol: str):
        """Build data quality metadata features (non-predictive metadata)."""
        return None

    # ------------------------------------------------------------------
    # Merge
    # ------------------------------------------------------------------

    def merge_features(self, feature_frames: list):
        """
        Merge multiple feature DataFrames on [symbol, date].
        Missing values filled with NaN (not filled with 0 to avoid false data).
        """
        try:
            import pandas as pd

            frames = [f for f in feature_frames if f is not None and not (hasattr(f, "empty") and f.empty)]
            if not frames:
                return pd.DataFrame()
            if len(frames) == 1:
                return frames[0]

            base = frames[0]
            for other in frames[1:]:
                if "symbol" in other.columns and "date" in other.columns:
                    try:
                        base = base.merge(other, on=["symbol", "date"], how="left", suffixes=("", "_dup"))
                        # Drop duplicate columns
                        dup_cols = [c for c in base.columns if c.endswith("_dup")]
                        base = base.drop(columns=dup_cols)
                    except Exception as exc:
                        logger.debug("merge_features: %s", exc)
            return base
        except Exception as exc:
            logger.warning("merge_features: %s", exc)
            return feature_frames[0] if feature_frames else None

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def write_snapshot(self, df, name: Optional[str] = None) -> Tuple[str, str]:
        """Write snapshot CSV and summary JSON. Returns (csv_path, summary_path)."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = name or "feature_snapshot"
        csv_path  = os.path.join(self.output_root, f"{prefix}_{ts}.csv")
        json_path = os.path.join(self.output_root, f"{prefix}_summary_{ts}.json")
        try:
            if df is not None and not (hasattr(df, "empty") and df.empty):
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            summary = {
                "snapshot_name": prefix,
                "generated_at":  datetime.now().isoformat(),
                "mode":          self.mode,
                "output_path":   csv_path,
                "row_count":     len(df) if df is not None else 0,
                "feature_count": len(df.columns) - 2 if df is not None else 0,
                "research_only": True,
                "no_real_orders": True,
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            logger.warning("FeatureSnapshotBuilder.write_snapshot: %s", exc)
        return csv_path, json_path

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_available_symbols(self) -> List[str]:
        """Load available symbols from data/import."""
        try:
            import pandas as pd
            # Try profile CSV
            profile_path = os.path.join(self.import_root, "profile", "stock_profile.csv")
            if os.path.exists(profile_path):
                df = pd.read_csv(profile_path)
                sym_col = next((c for c in df.columns if c.lower() in ("symbol", "代號", "stock_id")), None)
                if sym_col:
                    return df[sym_col].astype(str).dropna().tolist()[:50]

            # Try daily price CSV
            daily_path = os.path.join(self.import_root, "daily", "daily_k.csv")
            if os.path.exists(daily_path):
                df = pd.read_csv(daily_path, usecols=[0])
                return df.iloc[:, 0].astype(str).unique()[:20].tolist()

            return []
        except Exception as exc:
            logger.debug("_load_available_symbols: %s", exc)
            return []

    def _load_daily_price(self, symbol: str):
        """Load daily price data for one symbol."""
        try:
            import pandas as pd
            daily_path = os.path.join(self.import_root, "daily", "daily_k.csv")
            if not os.path.exists(daily_path):
                return None
            df = pd.read_csv(daily_path)
            sym_col  = next((c for c in df.columns if c.lower() in ("symbol", "代號", "stock_id")), None)
            date_col = next((c for c in df.columns if c.lower() in ("date", "日期")), None)
            if not sym_col or not date_col:
                return None
            df = df[df[sym_col].astype(str) == str(symbol)].copy()
            if date_col != "date":
                df = df.rename(columns={date_col: "date"})
            if sym_col != "symbol":
                df = df.rename(columns={sym_col: "symbol"})
            # Normalize close
            close_col = next((c for c in df.columns if c.lower() in ("close", "收盤價")), None)
            if close_col and close_col != "close":
                df = df.rename(columns={close_col: "close"})
            return df if not df.empty else None
        except Exception as exc:
            logger.debug("_load_daily_price %s: %s", symbol, exc)
            return None
