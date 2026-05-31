"""
experiments/experiment_comparator.py — ExperimentComparator: compare research runs (v0.3.29).
[!] Research Only. No Real Orders. Production Trading: BLOCKED.
"""

import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Comparison result labels
IMPROVED = "IMPROVED"
WORSENED = "WORSENED"
UNCHANGED = "UNCHANGED"
INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

_DISCLAIMER = "IMPROVED does not imply readiness for real trading. No real orders."


class ExperimentComparator:
    """
    Compare two or more experiment runs across snapshots.
    [!] Research Only. No Real Orders. Production Trading: BLOCKED.
    """

    read_only: bool = True
    no_real_orders: bool = True
    production_blocked: bool = True

    def __init__(self, registry_root: str = "experiments"):
        self._registry_root = os.path.join(BASE_DIR, registry_root)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compare(self, experiment_ids: list) -> dict:
        """
        Compare a list of experiments sequentially (adjacent pairs).
        Returns {pairs, summary, disclaimer}.
        """
        try:
            if not experiment_ids or len(experiment_ids) < 2:
                return {
                    "pairs": [],
                    "summary": {
                        "best_experiment_id": experiment_ids[0] if experiment_ids else "",
                        "recommendation": "Not enough experiments to compare.",
                    },
                    "disclaimer": _DISCLAIMER,
                    "no_real_orders": True,
                    "production_blocked": True,
                }

            pairs = []
            for i in range(len(experiment_ids) - 1):
                left_id = experiment_ids[i]
                right_id = experiment_ids[i + 1]
                try:
                    pair_result = self.compare_two(left_id, right_id)
                    pairs.append(pair_result)
                except Exception:
                    logger.exception("compare pair %s vs %s failed", left_id, right_id)
                    pairs.append({
                        "left_id": left_id,
                        "right_id": right_id,
                        "error": "comparison failed",
                        "no_real_orders": True,
                        "production_blocked": True,
                    })

            # Determine best: count improvement votes for each right_id
            best_id = experiment_ids[-1]
            best_score = -1
            vote_tally: dict = {eid: 0 for eid in experiment_ids}
            for pair in pairs:
                direction = pair.get("overall_direction", UNCHANGED)
                right = pair.get("right_id", "")
                left = pair.get("left_id", "")
                if direction == IMPROVED:
                    vote_tally[right] = vote_tally.get(right, 0) + 1
                elif direction == WORSENED:
                    vote_tally[left] = vote_tally.get(left, 0) + 1

            if vote_tally:
                best_id = max(vote_tally, key=lambda k: vote_tally[k])

            return {
                "pairs": pairs,
                "summary": {
                    "best_experiment_id": best_id,
                    "recommendation": (
                        f"Experiment {best_id} shows the most improvement signals. "
                        f"{_DISCLAIMER}"
                    ),
                },
                "disclaimer": _DISCLAIMER,
                "no_real_orders": True,
                "production_blocked": True,
            }

        except Exception:
            logger.exception("compare failed")
            return {
                "pairs": [],
                "summary": {"best_experiment_id": "", "recommendation": "Comparison failed."},
                "disclaimer": _DISCLAIMER,
                "no_real_orders": True,
                "production_blocked": True,
            }

    def compare_two(self, left_id: str, right_id: str) -> dict:
        """
        Full comparison between two experiments.
        Returns {left_id, right_id, scores, backtest, data_quality, rules, universe,
                 overall_direction, recommendation, no_real_orders, production_blocked}.
        """
        try:
            from experiments.experiment_registry import ExperimentRegistry
            reg = ExperimentRegistry(registry_root=os.path.relpath(self._registry_root, BASE_DIR))

            left_meta = reg.get_experiment(left_id)
            right_meta = reg.get_experiment(right_id)

            left_snaps = left_meta.snapshots if left_meta else {}
            right_snaps = right_meta.snapshots if right_meta else {}

            scores = self.compare_scores(left_snaps, right_snaps)
            backtest = self.compare_backtest_metrics(left_snaps, right_snaps)
            data_quality = self.compare_data_quality(left_snaps, right_snaps)
            rules = self.compare_rule_snapshots(left_snaps, right_snaps)
            universe = self.compare_universe(left_snaps, right_snaps)

            # Overall direction: majority vote among top fields
            all_directions = [
                scores.get("production_readiness_score", {}).get("direction", INSUFFICIENT_DATA),
                scores.get("backtest_readiness_score", {}).get("direction", INSUFFICIENT_DATA),
                backtest.get("hardened_sharpe", {}).get("direction", INSUFFICIENT_DATA),
                data_quality.get("production_readiness_score", {}).get("direction", INSUFFICIENT_DATA),
            ]
            improved_count = all_directions.count(IMPROVED)
            worsened_count = all_directions.count(WORSENED)

            if improved_count > worsened_count:
                overall_direction = IMPROVED
            elif worsened_count > improved_count:
                overall_direction = WORSENED
            elif improved_count == 0 and worsened_count == 0:
                overall_direction = INSUFFICIENT_DATA
            else:
                overall_direction = UNCHANGED

            recommendation = (
                f"Compared {left_id} → {right_id}: overall direction is {overall_direction}. "
                f"{_DISCLAIMER}"
            )

            return {
                "left_id": left_id,
                "right_id": right_id,
                "scores": scores,
                "backtest": backtest,
                "data_quality": data_quality,
                "rules": rules,
                "universe": universe,
                "overall_direction": overall_direction,
                "recommendation": recommendation,
                "no_real_orders": True,
                "production_blocked": True,
                "disclaimer": _DISCLAIMER,
            }

        except Exception:
            logger.exception("compare_two failed for %s vs %s", left_id, right_id)
            return {
                "left_id": left_id,
                "right_id": right_id,
                "error": "compare_two raised an exception",
                "overall_direction": INSUFFICIENT_DATA,
                "recommendation": _DISCLAIMER,
                "no_real_orders": True,
                "production_blocked": True,
            }

    def compare_scores(self, left_snaps: dict, right_snaps: dict) -> dict:
        """
        Compare high-level quality scores across snapshot sets.
        """
        try:
            def _get_dq(snaps: dict) -> dict:
                return snaps.get("data_quality", {}).get("summary", {})

            def _get_pr(snaps: dict) -> dict:
                return snaps.get("provider_reliability", {}).get("summary", {})

            left_dq = _get_dq(left_snaps)
            right_dq = _get_dq(right_snaps)
            left_pr = _get_pr(left_snaps)
            right_pr = _get_pr(right_snaps)

            prod_left = self._safe_float(left_dq.get("production_readiness_score"))
            prod_right = self._safe_float(right_dq.get("production_readiness_score"))
            bt_left = self._safe_float(left_dq.get("backtest_readiness_score"))
            bt_right = self._safe_float(right_dq.get("backtest_readiness_score"))
            rel_left = self._safe_float(left_pr.get("provider_reliability_score"))
            rel_right = self._safe_float(right_pr.get("provider_reliability_score"))

            return {
                "production_readiness_score": {
                    "left_value": prod_left,
                    "right_value": prod_right,
                    "direction": self._direction(prod_left, prod_right),
                    "change": _delta(prod_left, prod_right),
                },
                "backtest_readiness_score": {
                    "left_value": bt_left,
                    "right_value": bt_right,
                    "direction": self._direction(bt_left, bt_right),
                    "change": _delta(bt_left, bt_right),
                },
                "provider_reliability_score": {
                    "left_value": rel_left,
                    "right_value": rel_right,
                    "direction": self._direction(rel_left, rel_right),
                    "change": _delta(rel_left, rel_right),
                },
            }

        except Exception:
            logger.exception("compare_scores failed")
            return {}

    def compare_backtest_metrics(self, left_snaps: dict, right_snaps: dict) -> dict:
        """Compare hardened backtest and portfolio metrics."""
        try:
            def _bt(snaps):
                return snaps.get("backtest", {}).get("summary", {}).get("hardened_backtest") or {}

            def _port(snaps):
                return snaps.get("backtest", {}).get("summary", {}).get("portfolio") or {}

            l_bt = _bt(left_snaps)
            r_bt = _bt(right_snaps)
            l_pt = _port(left_snaps)
            r_pt = _port(right_snaps)

            return {
                "hardened_net_return": self._compare_field(l_bt, r_bt, "net_return"),
                "hardened_sharpe": self._compare_field(l_bt, r_bt, "sharpe"),
                "hardened_max_drawdown": self._compare_field(
                    l_bt, r_bt, "max_drawdown", higher_is_better=False
                ),
                "portfolio_sharpe": self._compare_field(l_pt, r_pt, "sharpe"),
                "portfolio_max_drawdown": self._compare_field(
                    l_pt, r_pt, "max_drawdown", higher_is_better=False
                ),
                "portfolio_trade_count": self._compare_field(l_pt, r_pt, "trade_count"),
            }

        except Exception:
            logger.exception("compare_backtest_metrics failed")
            return {}

    def compare_data_quality(self, left_snaps: dict, right_snaps: dict) -> dict:
        """Compare data quality fields."""
        try:
            def _dq(snaps):
                return snaps.get("data_quality", {}).get("summary", {})

            l = _dq(left_snaps)
            r = _dq(right_snaps)

            return {
                "production_readiness_score": self._compare_field(l, r, "production_readiness_score"),
                "backtest_readiness_score": self._compare_field(l, r, "backtest_readiness_score"),
                "missing_data_count": self._compare_field(
                    l, r, "missing_data_count", higher_is_better=False
                ),
            }

        except Exception:
            logger.exception("compare_data_quality failed")
            return {}

    def compare_rule_snapshots(self, left_snaps: dict, right_snaps: dict) -> dict:
        """Compare rule governance fields."""
        try:
            def _rg(snaps):
                return snaps.get("rule_governance", {}).get("summary", {})

            l = _rg(left_snaps)
            r = _rg(right_snaps)

            return {
                "rule_count": self._compare_field(l, r, "total_rules"),
                "experimental_rule_count": self._compare_field(l, r, "experimental"),
            }

        except Exception:
            logger.exception("compare_rule_snapshots failed")
            return {}

    def compare_universe(self, left_snaps: dict, right_snaps: dict) -> dict:
        """Compare universe size."""
        try:
            def _uv(snaps):
                return snaps.get("universe", {}).get("summary", {})

            l = _uv(left_snaps)
            r = _uv(right_snaps)

            return {
                "universe_size": self._compare_field(l, r, "universe_size"),
            }

        except Exception:
            logger.exception("compare_universe failed")
            return {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _safe_float(val) -> float | None:
        """Return float or None."""
        if val is None:
            return None
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _direction(left, right, higher_is_better: bool = True) -> str:
        """Return IMPROVED / WORSENED / UNCHANGED / INSUFFICIENT_DATA."""
        if left is None or right is None:
            return INSUFFICIENT_DATA
        try:
            lv = float(left)
            rv = float(right)
            if rv == lv:
                return UNCHANGED
            if higher_is_better:
                return IMPROVED if rv > lv else WORSENED
            else:
                return IMPROVED if rv < lv else WORSENED
        except (TypeError, ValueError):
            return INSUFFICIENT_DATA

    def _compare_field(
        self, left_dict: dict, right_dict: dict, key: str, higher_is_better: bool = True
    ) -> dict:
        """Build a comparison entry for a single field."""
        lv = self._safe_float(left_dict.get(key))
        rv = self._safe_float(right_dict.get(key))
        return {
            "left_value": lv,
            "right_value": rv,
            "direction": self._direction(lv, rv, higher_is_better=higher_is_better),
            "change": _delta(lv, rv),
        }


def _delta(left, right) -> float | None:
    """Return right - left, or None if either is None."""
    if left is None or right is None:
        return None
    try:
        return round(float(right) - float(left), 6)
    except (TypeError, ValueError):
        return None
