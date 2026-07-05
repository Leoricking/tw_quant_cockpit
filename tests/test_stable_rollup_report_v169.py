"""
tests/test_stable_rollup_report_v169.py
Tests for stable_report_v169 module.
"""
import pytest
from paper_trading.stable_rollup.stable_report_v169 import StableReport, generate_report
from paper_trading.stable_rollup.models_v169 import StableRollupReport
from paper_trading.stable_rollup.enums_v169 import RollupStatus


def test_report_instantiable():
    r = StableReport()
    assert r is not None


def test_generate_returns_report():
    r = StableReport()
    report = r.generate()
    assert isinstance(report, StableRollupReport)


def test_generate_report_id_nonempty():
    r = StableReport()
    report = r.generate()
    assert report.report_id


def test_generate_paper_only():
    r = StableReport()
    report = r.generate()
    assert report.paper_only is True


def test_generate_no_real_orders():
    r = StableReport()
    report = r.generate()
    assert report.no_real_orders is True


def test_generate_not_for_production():
    r = StableReport()
    report = r.generate()
    assert report.not_for_production is True


def test_generate_release_version():
    r = StableReport()
    report = r.generate()
    assert report.release_version == "1.6.9"


def test_generate_release_name():
    r = StableReport()
    report = r.generate()
    assert report.release_name == "Live Paper Trading Stable Rollup"


def test_to_dict_returns_dict():
    r = StableReport()
    report = r.generate()
    d = r.to_dict(report)
    assert isinstance(d, dict)


def test_to_dict_has_report_id():
    r = StableReport()
    report = r.generate()
    d = r.to_dict(report)
    assert "report_id" in d


def test_to_dict_has_rollup_status():
    r = StableReport()
    report = r.generate()
    d = r.to_dict(report)
    assert "rollup_status" in d


def test_to_dict_paper_only():
    r = StableReport()
    report = r.generate()
    d = r.to_dict(report)
    assert d["paper_only"] is True


def test_summary_returns_string():
    r = StableReport()
    report = r.generate()
    s = r.summary(report)
    assert isinstance(s, str)
    assert "1.6.9" in s


def test_generate_report_function():
    report = generate_report()
    assert isinstance(report, StableRollupReport)
    assert report.release_version == "1.6.9"


def test_generate_report_ids_unique():
    r = StableReport()
    r1 = r.generate()
    r2 = r.generate()
    assert r1.report_id != r2.report_id
