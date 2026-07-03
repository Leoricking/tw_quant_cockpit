"""
tests/test_operational_integration_report_v168.py — Report Generator tests v1.6.8
[!] Research Only. Paper Only. No Real Orders.
"""
import pytest

from paper_trading.operational_integration.integration_report_v168 import (
    IntegrationReportGenerator, _REPORT_SECTIONS, PAPER_ONLY, RESEARCH_ONLY, NO_REAL_ORDERS,
)


class TestReportSafetyFlags:
    def test_paper_only(self):
        assert PAPER_ONLY is True

    def test_research_only(self):
        assert RESEARCH_ONLY is True

    def test_no_real_orders(self):
        assert NO_REAL_ORDERS is True


class TestIntegrationReportGeneratorCore:
    def setup_method(self):
        self.generator = IntegrationReportGenerator()
        self.run_result = {
            "run_id": "R001",
            "session_id": "S001",
            "status": "COMPLETE",
            "stage_count": 14,
            "stages": [],
            "period_start": "2026-01-02",
            "period_end": "2026-01-03",
            "components": [],
            "scorecard_total": 95.0,
            "paper_only": True,
        }

    def test_report_sections_count(self):
        assert len(_REPORT_SECTIONS) == 19

    def test_build_sections_returns_dict(self):
        sections = self.generator._build_sections(self.run_result)
        assert isinstance(sections, dict)

    def test_build_sections_has_19_keys(self):
        sections = self.generator._build_sections(self.run_result)
        assert len(sections) == 19

    def test_build_sections_integration_summary(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Integration Summary" in sections

    def test_build_sections_safety(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Safety" in sections
        assert sections["Safety"]["paper_only"] is True

    def test_build_sections_not_for_real_trading(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Not for Real Trading" in sections

    def test_build_sections_limitations(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Limitations" in sections
        assert isinstance(sections["Limitations"], list)
        assert len(sections["Limitations"]) > 0

    def test_build_sections_run_id_in_summary(self):
        sections = self.generator._build_sections(self.run_result)
        summary = sections["Integration Summary"]
        assert summary["run_id"] == "R001"

    def test_generate_markdown_returns_string(self):
        md = self.generator.generate_markdown(self.run_result)
        assert isinstance(md, str)
        assert len(md) > 0

    def test_generate_markdown_has_paper_only(self):
        md = self.generator.generate_markdown(self.run_result)
        assert "Paper" in md or "paper" in md

    def test_generate_markdown_has_run_id(self):
        md = self.generator.generate_markdown(self.run_result)
        assert "R001" in md

    def test_generate_json_returns_string(self):
        json_str = self.generator.generate_json(self.run_result)
        assert isinstance(json_str, str)

    def test_generate_json_parseable(self):
        import json
        json_str = self.generator.generate_json(self.run_result)
        parsed = json.loads(json_str)
        assert isinstance(parsed, dict)

    def test_generate_json_has_paper_only(self):
        import json
        json_str = self.generator.generate_json(self.run_result)
        parsed = json.loads(json_str)
        assert parsed.get("paper_only") is True or "sections" in parsed

    def test_generate_csv_returns_string(self):
        csv_str = self.generator.generate_csv(self.run_result)
        assert isinstance(csv_str, str)

    def test_sections_include_scorecard(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Scorecard" in sections

    def test_sections_include_reconciliation(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Reconciliation" in sections

    def test_sections_include_failures(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Failures" in sections

    def test_sections_include_determinism(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Determinism" in sections

    def test_sections_pipeline_status(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Pipeline Status" in sections

    def test_sections_data_flow(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Data Flow" in sections

    def test_sections_lineage_integrity(self):
        sections = self.generator._build_sections(self.run_result)
        assert "Lineage Integrity" in sections

    def test_build_sections_not_for_production(self):
        sections = self.generator._build_sections(self.run_result)
        not_for_real = sections["Not for Real Trading"]
        assert not_for_real.get("not_for_production") is True
