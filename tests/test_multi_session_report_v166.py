"""
test_multi_session_report_v166.py — Report tests for Multi-session Coordination v1.6.6.
[!] Research Only. Paper Only. No Real Orders. No Broker.
"""
import pytest
import json


class TestCoordinationReport:
    def test_set_section_and_to_dict(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        r.set_section("sessions", [{"id": "s1"}])
        d = r.to_dict()
        assert "sessions" in d
        assert d["sessions"] == [{"id": "s1"}]

    def test_to_dict_returns_dict(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        assert isinstance(r.to_dict(), dict)

    def test_to_json_returns_string(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        r.set_section("overview", {"status": "ok"})
        json_str = r.to_json()
        assert isinstance(json_str, str)

    def test_to_json_is_valid_json(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        r.set_section("sessions", [1, 2, 3])
        json_str = r.to_json()
        parsed = json.loads(json_str)
        assert isinstance(parsed, dict)

    def test_to_markdown_returns_string(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        md = r.to_markdown()
        assert isinstance(md, str)

    def test_safety_disclaimer_in_markdown(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        md = r.to_markdown()
        assert "Research Only" in md or "No Real Orders" in md

    def test_to_csv_summary_returns_string(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        csv_str = r.to_csv_summary()
        assert isinstance(csv_str, str)

    def test_to_html_returns_string(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        html = r.to_html()
        assert isinstance(html, str)

    def test_to_html_contains_html_tags(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        html = r.to_html()
        assert "<html>" in html
        assert "</html>" in html

    def test_section_count_zero_initially(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        assert r.section_count() == 0

    def test_section_count_increments(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport, REPORT_SECTIONS
        r = CoordinationReport()
        r.set_section(REPORT_SECTIONS[0], "data1")
        r.set_section(REPORT_SECTIONS[1], "data2")
        assert r.section_count() == 2

    def test_section_count_correct_after_all_set(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport, REPORT_SECTIONS
        r = CoordinationReport()
        for sec in REPORT_SECTIONS:
            r.set_section(sec, f"data_{sec}")
        assert r.section_count() == len(REPORT_SECTIONS)

    def test_to_markdown_has_section_headers(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport, REPORT_SECTIONS
        r = CoordinationReport()
        r.set_section(REPORT_SECTIONS[0], "test")
        md = r.to_markdown()
        assert "##" in md

    def test_to_csv_has_header_row(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        csv_str = r.to_csv_summary()
        assert "section" in csv_str

    def test_multiple_sections_in_json(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        r.set_section("sessions", [])
        r.set_section("conflicts", [])
        json_str = r.to_json()
        d = json.loads(json_str)
        assert "sessions" in d
        assert "conflicts" in d

    def test_no_production_control_in_output_flag(self):
        import paper_trading.multi_session.report_v166 as m
        assert m.NO_PRODUCTION_CONTROL_IN_OUTPUT is True

    def test_to_html_has_safety_disclaimer(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        html = r.to_html()
        assert "Research Only" in html or "No Real Orders" in html

    def test_report_sections_list_exists(self):
        from paper_trading.multi_session.report_v166 import REPORT_SECTIONS
        assert isinstance(REPORT_SECTIONS, list)

    def test_report_sections_has_at_least_30(self):
        from paper_trading.multi_session.report_v166 import REPORT_SECTIONS
        assert len(REPORT_SECTIONS) >= 30

    def test_report_sections_contains_executive_summary(self):
        from paper_trading.multi_session.report_v166 import REPORT_SECTIONS
        assert "executive_summary" in REPORT_SECTIONS

    def test_report_sections_contains_scorecard(self):
        from paper_trading.multi_session.report_v166 import REPORT_SECTIONS
        assert "scorecard" in REPORT_SECTIONS

    def test_report_sections_contains_safety(self):
        from paper_trading.multi_session.report_v166 import REPORT_SECTIONS
        assert "safety" in REPORT_SECTIONS

    def test_report_sections_contains_lineage(self):
        from paper_trading.multi_session.report_v166 import REPORT_SECTIONS
        assert "lineage" in REPORT_SECTIONS

    def test_to_csv_has_true_false_values(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport, REPORT_SECTIONS
        r = CoordinationReport()
        r.set_section(REPORT_SECTIONS[0], "some data")
        csv_str = r.to_csv_summary()
        assert "True" in csv_str

    def test_set_section_overwrites(self):
        from paper_trading.multi_session.report_v166 import CoordinationReport
        r = CoordinationReport()
        r.set_section("sessions", "first")
        r.set_section("sessions", "second")
        d = r.to_dict()
        assert d["sessions"] == "second"
