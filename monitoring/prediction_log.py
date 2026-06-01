"""
monitoring/prediction_log.py — Prediction Log for v0.4.3 Model Monitoring.

[!] Monitoring Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading.
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class PredictionRecord:
    """A single logged prediction/signal record."""

    # Identity
    prediction_id:       str
    model_id:            str
    signal_id:           str
    rule_id:             str
    symbol:              str
    date:                str
    prediction_time:     str

    # Type & source
    prediction_type:     str   # "classification" / "regression" / "rule_signal" / "signal_quality" / "portfolio_candidate"
    predicted_label:     str
    predicted_score:     float
    predicted_return:    float
    confidence:          float
    horizon:             int
    source:              str   # "ml_prediction" / "rule_signal" / "signal_quality" / "portfolio_candidate" / "backtest_signal"

    # Lineage
    feature_snapshot_id: str
    experiment_id:       str

    # Actuals (filled in later)
    actual_return:       Optional[float] = None
    actual_label:        Optional[str]   = None
    hit:                 Optional[bool]  = None
    reviewed:            bool            = False
    notes:               str             = ""

    def to_dict(self) -> dict:
        return {
            "prediction_id":       self.prediction_id,
            "model_id":            self.model_id,
            "signal_id":           self.signal_id,
            "rule_id":             self.rule_id,
            "symbol":              self.symbol,
            "date":                self.date,
            "prediction_time":     self.prediction_time,
            "prediction_type":     self.prediction_type,
            "predicted_label":     self.predicted_label,
            "predicted_score":     self.predicted_score,
            "predicted_return":    self.predicted_return,
            "confidence":          self.confidence,
            "horizon":             self.horizon,
            "source":              self.source,
            "feature_snapshot_id": self.feature_snapshot_id,
            "experiment_id":       self.experiment_id,
            "actual_return":       self.actual_return,
            "actual_label":        self.actual_label,
            "hit":                 self.hit,
            "reviewed":            self.reviewed,
            "notes":               self.notes,
        }


class PredictionLog:
    """
    Append-only JSONL log of prediction records.

    [!] Monitoring Only. Read Only. No Real Orders.
    Runtime outputs → model_monitoring/predictions/ (not committed).
    """

    read_only      = True
    no_real_orders = True

    _SAFETY = {
        "monitoring_only":    True,
        "read_only":          True,
        "no_real_orders":     True,
        "production_blocked": True,
        "real_order_ready":   False,
    }

    def __init__(self, log_root: str = "model_monitoring/predictions"):
        if os.path.isabs(log_root):
            self._root = log_root
        else:
            self._root = os.path.join(_BASE_DIR, log_root)
        os.makedirs(self._root, exist_ok=True)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _daily_file(self, date_str: str = None) -> str:
        if date_str is None:
            date_str = datetime.now().strftime("%Y%m%d")
        else:
            date_str = date_str.replace("-", "")
        return os.path.join(self._root, f"predictions_{date_str}.jsonl")

    def _all_jsonl_files(self) -> list:
        try:
            files = [
                os.path.join(self._root, f)
                for f in os.listdir(self._root)
                if f.startswith("predictions_") and f.endswith(".jsonl")
            ]
            files.sort()
            return files
        except Exception:
            return []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def append(self, record: PredictionRecord) -> dict:
        """Append record to today's JSONL file."""
        path = self._daily_file()
        try:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
            return {"ok": True, "prediction_id": record.prediction_id, **self._SAFETY}
        except Exception as exc:
            logger.error("PredictionLog.append: %s", exc)
            return {"ok": False, "error": str(exc), **self._SAFETY}

    def load(
        self,
        model_id:   Optional[str] = None,
        symbol:     Optional[str] = None,
        start_date: Optional[str] = None,
        end_date:   Optional[str] = None,
    ) -> list:
        """Load all JSONL files and filter by params."""
        records = []
        for fpath in self._all_jsonl_files():
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                            records.append(rec)
                        except Exception:
                            pass
            except Exception as exc:
                logger.warning("PredictionLog.load file %s: %s", fpath, exc)

        # Filter
        if model_id:
            records = [r for r in records if r.get("model_id") == model_id]
        if symbol:
            records = [r for r in records if r.get("symbol") == symbol]
        if start_date:
            records = [r for r in records if r.get("date", "") >= start_date]
        if end_date:
            records = [r for r in records if r.get("date", "") <= end_date]
        return records

    def update_actuals(self, price_data) -> dict:
        """
        Given price_data dict/df of {symbol: {date: actual_return}},
        update hit/actual_return for matching records; re-save.
        """
        updated = 0
        errors  = 0

        # Normalize price_data to nested dict
        pd_dict: dict = {}
        try:
            if hasattr(price_data, "to_dict"):
                pd_dict = price_data.to_dict()
            elif isinstance(price_data, dict):
                pd_dict = price_data
        except Exception:
            pass

        for fpath in self._all_jsonl_files():
            new_lines = []
            changed   = False
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    lines = fh.readlines()
            except Exception as exc:
                logger.warning("PredictionLog.update_actuals read %s: %s", fpath, exc)
                errors += 1
                continue

            for line in lines:
                line = line.strip()
                if not line:
                    new_lines.append("")
                    continue
                try:
                    rec = json.loads(line)
                    sym = rec.get("symbol", "")
                    dt  = rec.get("date", "")
                    if sym in pd_dict and dt in pd_dict.get(sym, {}):
                        actual_ret = pd_dict[sym][dt]
                        rec["actual_return"] = actual_ret
                        rec["reviewed"]      = True
                        predicted_ret = rec.get("predicted_return", 0) or 0
                        rec["hit"] = bool(actual_ret > 0 and predicted_ret > 0) or \
                                     bool(actual_ret < 0 and predicted_ret < 0)
                        changed = True
                        updated += 1
                    new_lines.append(json.dumps(rec, ensure_ascii=False))
                except Exception:
                    new_lines.append(line)

            if changed:
                try:
                    with open(fpath, "w", encoding="utf-8") as fh:
                        fh.write("\n".join(new_lines) + "\n")
                except Exception as exc:
                    logger.error("PredictionLog.update_actuals write %s: %s", fpath, exc)
                    errors += 1

        return {"ok": errors == 0, "updated": updated, "errors": errors, **self._SAFETY}

    def summarize(self) -> dict:
        """Return log summary statistics."""
        records = self.load()
        sources:  dict = {}
        horizons: dict = {}
        dates:    list = []
        reviewed  = 0
        for r in records:
            s = r.get("source", "unknown")
            sources[s]  = sources.get(s, 0) + 1
            h = r.get("horizon", 0)
            horizons[str(h)] = horizons.get(str(h), 0) + 1
            d = r.get("date", "")
            if d:
                dates.append(d)
            if r.get("reviewed"):
                reviewed += 1

        dates.sort()
        return {
            "total_predictions": len(records),
            "reviewed_count":    reviewed,
            "sources":           sources,
            "horizons":          horizons,
            "date_range":        {"min": dates[0] if dates else "", "max": dates[-1] if dates else ""},
            **self._SAFETY,
        }
