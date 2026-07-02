"""
tests/test_paper_attribution_store_query_v167.py
Tests for paper attribution store and query API v1.6.7.
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest
from paper_trading.performance_attribution.attribution_store_v167 import AttributionStore
from paper_trading.performance_attribution.attribution_query_v167 import AttributionQueryAPI


def _run(run_id="run_001", **extra):
    base = {
        "paper_only": True,
        "research_only": True,
        "portfolio_id": "P1",
        "status": "COMPLETE",
    }
    base.update(extra)
    return run_id, base


class TestAttributionStoreSave:
    def setup_method(self):
        self.store = AttributionStore()

    def test_save_valid_run(self):
        rid, data = _run()
        r = self.store.save_run(rid, data)
        assert r["saved"] is True

    def test_save_sets_run_id(self):
        rid, data = _run("r1")
        self.store.save_run(rid, data)
        loaded = self.store.load_run("r1")
        assert loaded["run_id"] == "r1"

    def test_save_blocks_missing_paper_only(self):
        r = self.store.save_run("bad", {"research_only": True})
        assert r["saved"] is False

    def test_save_blocks_missing_research_only(self):
        r = self.store.save_run("bad", {"paper_only": True})
        assert r["saved"] is False

    def test_save_blocks_broker_session(self):
        r = self.store.save_run("bad", {
            "paper_only": True, "research_only": True,
            "broker_session": "live",
        })
        assert r["saved"] is False

    def test_save_blocks_real_account_token(self):
        r = self.store.save_run("bad", {
            "paper_only": True, "research_only": True,
            "real_account_token": "tok",
        })
        assert r["saved"] is False

    def test_save_blocks_api_secret(self):
        r = self.store.save_run("bad", {
            "paper_only": True, "research_only": True,
            "api_secret": "key",
        })
        assert r["saved"] is False

    def test_save_blocks_empty_run_id(self):
        r = self.store.save_run("", {"paper_only": True, "research_only": True})
        assert r["saved"] is False

    def test_save_schema_version_added(self):
        rid, data = _run()
        self.store.save_run(rid, data)
        loaded = self.store.load_run(rid)
        assert "schema_version" in loaded

    def test_save_policy_version_added(self):
        rid, data = _run()
        self.store.save_run(rid, data)
        loaded = self.store.load_run(rid)
        assert "policy_version" in loaded


class TestAttributionStoreLoad:
    def setup_method(self):
        self.store = AttributionStore()

    def test_load_existing_run(self):
        rid, data = _run("r2")
        self.store.save_run(rid, data)
        loaded = self.store.load_run("r2")
        assert loaded is not None
        assert loaded["portfolio_id"] == "P1"

    def test_load_nonexistent_returns_none(self):
        loaded = self.store.load_run("does_not_exist")
        assert loaded is None

    def test_load_preserves_data(self):
        rid, data = _run("r3", period_start="2024-01-01", period_end="2024-01-31")
        self.store.save_run(rid, data)
        loaded = self.store.load_run("r3")
        assert loaded["period_start"] == "2024-01-01"


class TestAttributionStoreList:
    def setup_method(self):
        self.store = AttributionStore()

    def test_list_empty_store(self):
        assert self.store.list_runs() == []

    def test_list_returns_sorted(self):
        for rid in ("zrun", "arun", "mrun"):
            self.store.save_run(rid, {"paper_only": True, "research_only": True})
        runs = self.store.list_runs()
        assert runs == sorted(runs)

    def test_list_contains_saved_runs(self):
        self.store.save_run("r10", {"paper_only": True, "research_only": True})
        assert "r10" in self.store.list_runs()


class TestAttributionStoreDelete:
    def setup_method(self):
        self.store = AttributionStore()

    def test_delete_existing(self):
        rid, data = _run("del_run")
        self.store.save_run(rid, data)
        r = self.store.delete_test_run("del_run")
        assert r["deleted"] is True

    def test_delete_removes_run(self):
        rid, data = _run("del_run2")
        self.store.save_run(rid, data)
        self.store.delete_test_run("del_run2")
        assert self.store.load_run("del_run2") is None

    def test_delete_nonexistent_not_deleted(self):
        r = self.store.delete_test_run("no_such_run")
        assert r["deleted"] is False


class TestAttributionStoreSummarize:
    def setup_method(self):
        self.store = AttributionStore()

    def test_empty_store_zero_total(self):
        s = self.store.summarize()
        assert s["total_runs"] == 0

    def test_after_save_total_increases(self):
        self.store.save_run("r1", {"paper_only": True, "research_only": True, "status": "COMPLETE"})
        s = self.store.summarize()
        assert s["total_runs"] == 1

    def test_paper_only_in_summary(self):
        s = self.store.summarize()
        assert s["paper_only"] is True


class TestAttributionStoreExport:
    def setup_method(self):
        self.store = AttributionStore()
        self.store.save_run("exp1", {
            "paper_only": True, "research_only": True,
            "portfolio_id": "EXP_P1", "status": "COMPLETE",
        })

    def test_export_json_contains_key(self):
        j = self.store.export_json("exp1")
        assert "portfolio_id" in j

    def test_export_json_all_runs(self):
        j = self.store.export_json()
        assert "exp1" in j

    def test_export_csv_has_header(self):
        csv = self.store.export_csv()
        assert "run_id" in csv

    def test_export_csv_has_run_data(self):
        csv = self.store.export_csv("exp1")
        assert "exp1" in csv

    def test_export_markdown_has_header(self):
        md = self.store.export_markdown()
        assert "#" in md

    def test_export_markdown_no_runs(self):
        empty_store = AttributionStore()
        md = empty_store.export_markdown()
        assert "No runs" in md


class TestAttributionQueryPortfolio:
    def setup_method(self):
        self.store = AttributionStore()
        self.store.save_run("qa_run", {
            "paper_only": True,
            "research_only": True,
            "portfolio_id": "QA_P1",
            "status": "COMPLETE",
            "portfolio_attribution": {
                "active_return": 0.05,
                "gross_return": 0.07,
                "net_return": 0.065,
                "reconciled": True,
                "confidence": "HIGH",
            },
        })
        self.q = AttributionQueryAPI(self.store)

    def test_get_portfolio_attribution(self):
        r = self.q.get_portfolio_attribution("qa_run")
        assert r["active_return"] == 0.05

    def test_get_portfolio_not_found(self):
        r = self.q.get_portfolio_attribution("no_run")
        assert "error" in r

    def test_summarize_attribution(self):
        r = self.q.summarize_attribution("qa_run")
        assert r["portfolio_id"] == "QA_P1"
        assert r["paper_only"] is True
        assert r["research_only"] is True

    def test_summarize_not_found(self):
        r = self.q.summarize_attribution("no_run")
        assert "error" in r


class TestAttributionQueryStrategy:
    def setup_method(self):
        self.store = AttributionStore()
        self.store.save_run("strat_run", {
            "paper_only": True, "research_only": True,
            "strategy_attribution": {
                "s1": {"return": 0.03},
                "s2": {"return": 0.02},
            },
        })
        self.q = AttributionQueryAPI(self.store)

    def test_get_all_strategies(self):
        r = self.q.get_strategy_attribution("strat_run")
        assert "s1" in r
        assert "s2" in r

    def test_get_specific_strategy(self):
        r = self.q.get_strategy_attribution("strat_run", strategy_id="s1")
        assert r["return"] == 0.03

    def test_strategy_not_found(self):
        r = self.q.get_strategy_attribution("strat_run", strategy_id="s_none")
        assert "error" in r

    def test_compare_strategies(self):
        r = self.q.compare_strategies("strat_run", strategy_ids=["s1", "s2"])
        assert "strategies" in r
        assert r["paper_only"] is True


class TestAttributionQueryTopBottom:
    def setup_method(self):
        self.store = AttributionStore()
        self.store.save_run("contrib_run", {
            "paper_only": True, "research_only": True,
            "symbol_attribution": {
                "AAPL": {"return": 0.10},
                "MSFT": {"return": 0.05},
                "GOOG": {"return": 0.08},
                "TSLA": {"return": -0.05},
                "META": {"return": 0.03},
                "AMZN": {"return": 0.02},
            },
        })
        self.q = AttributionQueryAPI(self.store)

    def test_top_contributors_returns_n(self):
        r = self.q.get_top_contributors("contrib_run", level="symbol", n=3)
        assert len(r["top_contributors"]) == 3

    def test_bottom_contributors_returns_n(self):
        r = self.q.get_bottom_contributors("contrib_run", level="symbol", n=3)
        assert len(r["bottom_contributors"]) == 3

    def test_top_contributor_first_is_highest(self):
        r = self.q.get_top_contributors("contrib_run", level="symbol", n=1)
        top = r["top_contributors"][0]
        assert top[0] == "AAPL"

    def test_bottom_contributor_first_is_lowest(self):
        r = self.q.get_bottom_contributors("contrib_run", level="symbol", n=1)
        bot = r["bottom_contributors"][0]
        assert bot[0] == "TSLA"


class TestAttributionQueryComparePeriods:
    def setup_method(self):
        self.store = AttributionStore()
        for i, ar in enumerate([0.03, 0.05]):
            self.store.save_run(f"period_{i}", {
                "paper_only": True, "research_only": True,
                "portfolio_attribution": {"active_return": ar},
            })
        self.q = AttributionQueryAPI(self.store)

    def test_compare_periods_returns_dict(self):
        r = self.q.compare_periods(["period_0", "period_1"])
        assert "comparison" in r

    def test_compare_periods_has_both_runs(self):
        r = self.q.compare_periods(["period_0", "period_1"])
        assert "period_0" in r["comparison"]
        assert "period_1" in r["comparison"]

    def test_compare_empty_run_ids_error(self):
        r = self.q.compare_periods([])
        assert "error" in r

    def test_compare_paper_only(self):
        r = self.q.compare_periods(["period_0"])
        assert r["paper_only"] is True
