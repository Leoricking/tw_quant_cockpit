"""reports/intraday_replay_report.py — Intraday Replay Report builder (v0.4.4).
[!] Replay Training Only. Read Only. No Real Orders. Production Trading: BLOCKED.
[!] No live prediction. No auto-trading. Not investment advice."""
from __future__ import annotations

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class IntradayReplayReportBuilder:
    """Generates Markdown reports for intraday replay training sessions.

    Research Only / Replay Training Only / No Real Orders / Production Trading BLOCKED.
    """

    VERSION = "v0.4.4"

    _SAFETY_FLAGS = {
        "research_only": True,
        "replay_training_only": True,
        "no_real_orders": True,
        "production_blocked": True,
        "no_live_prediction": True,
        "not_investment_advice": True,
    }

    read_only = True
    no_real_orders = True

    def __init__(self, report_dir: str = "reports", mode: str = "real"):
        self._report_dir = os.path.join(BASE_DIR, report_dir)
        self._mode = mode
        os.makedirs(self._report_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _safe(self, d: dict, key: str, default="N/A"):
        if d is None:
            return default
        v = d.get(key, default)
        return v if v is not None else default

    def _section_overview(self, session_summary, now_str: str) -> str:
        ss = session_summary or {}
        lines = [
            "## 一、總覽 (Overview)",
            "",
            f"- **Report Version**: {self.VERSION}",
            f"- **Generated**: {now_str}",
            f"- **Mode**: {self._mode}",
            f"- **Research Only**: {self._SAFETY_FLAGS['research_only']}",
            f"- **Replay Training Only**: {self._SAFETY_FLAGS['replay_training_only']}",
            f"- **No Real Orders**: {self._SAFETY_FLAGS['no_real_orders']}",
            f"- **Production Trading**: BLOCKED",
            "",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Symbol | {self._safe(ss, 'symbol')} |",
            f"| Date | {self._safe(ss, 'date')} |",
            f"| Freq | {self._safe(ss, 'freq')} |",
            f"| Session ID | {self._safe(ss, 'session_id')} |",
            f"| Session Name | {self._safe(ss, 'session_name')} |",
            f"| Total Bars | {self._safe(ss, 'total_bars')} |",
            f"| Bars Replayed | {self._safe(ss, 'bars_replayed', self._safe(ss, 'current_index'))} |",
            f"| Status | {self._safe(ss, 'status')} |",
            f"| Training Mode | {self._safe(ss, 'training_mode')} |",
            "",
        ]
        return "\n".join(lines)

    def _section_replay_events(self, events_summary) -> str:
        es = events_summary or {}
        lines = [
            "## 二、Replay Events",
            "",
            f"| Event Type | Count |",
            f"|------------|-------|",
            f"| Opening Range Events | {self._safe(es, 'opening_range_count', 0)} |",
            f"| VWAP Events | {self._safe(es, 'vwap_count', 0)} |",
            f"| Fake Breakout Warnings | {self._safe(es, 'fake_breakout_count', 0)} |",
            f"| Volume Spikes | {self._safe(es, 'volume_spike_count', 0)} |",
            f"| POC Touches | {self._safe(es, 'poc_touch_count', 0)} |",
            f"| Signal Triggers | {self._safe(es, 'signal_trigger_count', 0)} |",
            f"| Total Events | {self._safe(es, 'total', 0)} |",
            "",
        ]
        event_list = es.get("events", [])
        if event_list:
            lines += ["### Event Log", "", "| # | Bar | Time | Type | Severity | Title |", "|---|-----|------|------|----------|-------|"]
            for i, evt in enumerate(event_list[:20], 1):
                if isinstance(evt, dict):
                    lines.append(
                        f"| {i} | {evt.get('bar_index', '')} | {evt.get('time', '')} | "
                        f"{evt.get('event_type', '')} | {evt.get('severity', '')} | {evt.get('title', '')} |"
                    )
            lines.append("")
        return "\n".join(lines)

    def _section_opening_range(self, opening_range_summary) -> str:
        ors = opening_range_summary or {}
        lines = [
            "## 三、Opening Range Replay",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Opening High | {self._safe(ors, 'opening_high')} |",
            f"| Opening Low | {self._safe(ors, 'opening_low')} |",
            f"| Opening Range % | {self._safe(ors, 'opening_range_pct')} |",
            f"| Range Break Status | {self._safe(ors, 'range_break_status')} |",
            f"| Current Position in Range | {self._safe(ors, 'current_position_in_range')} |",
            f"| Opening Strength | {self._safe(ors, 'opening_strength_so_far')} |",
            f"| Bars in Range | {self._safe(ors, 'bars_in_range')} |",
            f"| Opening Bars Count | {self._safe(ors, 'opening_bars_count')} |",
            "",
        ]
        return "\n".join(lines)

    def _section_vwap(self, vwap_summary) -> str:
        vs = vwap_summary or {}
        lines = [
            "## 四、VWAP Replay",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Current VWAP | {self._safe(vs, 'current_vwap')} |",
            f"| Price vs VWAP % | {self._safe(vs, 'price_vs_vwap_pct')} |",
            f"| VWAP State | {self._safe(vs, 'vwap_state')} |",
            f"| Above VWAP | {self._safe(vs, 'above_vwap')} |",
            f"| Above VWAP Ratio | {self._safe(vs, 'above_vwap_ratio_so_far')} |",
            f"| VWAP Reclaim | {self._safe(vs, 'vwap_reclaim')} |",
            f"| VWAP Lost | {self._safe(vs, 'vwap_lost')} |",
            "",
        ]
        return "\n".join(lines)

    def _section_fake_breakout(self, fake_breakout_summary) -> str:
        fb = fake_breakout_summary or {}
        lines = [
            "## 五、Fake Breakout Replay",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Breakout Attempt | {self._safe(fb, 'breakout_attempt')} |",
            f"| Breakout Confirmed | {self._safe(fb, 'breakout_confirmed')} |",
            f"| Breakout Failed | {self._safe(fb, 'breakout_failed_so_far', self._safe(fb, 'breakout_failed'))} |",
            f"| Fake Breakout Risk | {self._safe(fb, 'fake_breakout_risk_so_far', self._safe(fb, 'risk_level'))} |",
            f"| Chase Risk Score | {self._safe(fb, 'chase_risk_score_so_far', self._safe(fb, 'chase_risk_score'))} |",
            f"| Warning | {self._safe(fb, 'warning_message', self._safe(fb, 'description'))} |",
            "",
        ]
        return "\n".join(lines)

    def _section_volume_profile(self, volume_profile_summary) -> str:
        vp = volume_profile_summary or {}
        lines = [
            "## 六、Volume Profile Replay",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| POC Price (so far) | {self._safe(vp, 'poc_price_so_far')} |",
            f"| Value Area High | {self._safe(vp, 'value_area_high_so_far')} |",
            f"| Value Area Low | {self._safe(vp, 'value_area_low_so_far')} |",
            f"| Price vs POC % | {self._safe(vp, 'price_vs_poc_pct')} |",
            f"| Volume Cluster Strength | {self._safe(vp, 'volume_cluster_strength')} |",
            f"| Support/Pressure State | {self._safe(vp, 'support_pressure_state')} |",
            "",
        ]
        bins = vp.get("price_bins", {})
        if bins:
            lines += ["### Price → Volume Distribution (top 10 bins)", ""]
            sorted_bins = sorted(bins.items(), key=lambda x: float(x[1]), reverse=True)[:10]
            lines += ["| Price | Volume |", "|-------|--------|"]
            for price, vol in sorted_bins:
                lines.append(f"| {price} | {vol} |")
            lines.append("")
        return "\n".join(lines)

    def _section_training(self, training_summary) -> str:
        ts = training_summary or {}
        lines = [
            "## 七、Training Mode",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Questions | {self._safe(ts, 'total_questions')} |",
            f"| Answered | {self._safe(ts, 'answered')} |",
            f"| Correct | {self._safe(ts, 'correct')} |",
            f"| Quiz Accuracy | {self._safe(ts, 'accuracy', self._safe(ts, 'quiz_accuracy'))} |",
            f"| Training Score | {self._safe(ts, 'training_score')} |",
            f"| Grade | {self._safe(ts, 'grade')} |",
            "",
            "> Training scores are for self-assessment only.",
            "> They are NOT trading performance metrics and NOT investment advice.",
            "",
        ]
        return "\n".join(lines)

    def _section_safety(self) -> str:
        lines = [
            "## 八、安全聲明 (Safety Declaration)",
            "",
            "| Flag | Value |",
            "|------|-------|",
            "| Research Only | TRUE |",
            "| Replay Training Only | TRUE |",
            "| No Live Prediction | TRUE |",
            "| No Real Orders | TRUE |",
            "| Production Trading | BLOCKED |",
            "| Not Investment Advice | TRUE |",
            "| Read Only | TRUE |",
            "",
            "---",
            "",
            "> **[!] WARNING**: This report is for research and training purposes only.",
            "> It does NOT constitute investment advice, trading signals, or order instructions.",
            "> No real orders have been or will be generated by this system.",
            "> Production trading is permanently blocked in all replay components.",
            "> Past intraday patterns do not guarantee future results.",
            "",
            f"*Generated by TW Quant Cockpit {self.VERSION} — Intraday Replay Training Module*",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def build(
        self,
        session_summary=None,
        events_summary=None,
        opening_range_summary=None,
        vwap_summary=None,
        fake_breakout_summary=None,
        volume_profile_summary=None,
        training_summary=None,
        metrics=None,
    ) -> str:
        """Build and save the intraday replay report. Returns file path."""
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")

        # Merge metrics into session_summary if provided
        combined_session = dict(session_summary or {})
        if metrics:
            combined_session.update(metrics)

        sections = [
            f"# TW Quant Cockpit — Intraday Replay Report {self.VERSION}",
            "",
            f"> **[!] Replay Training Only | Research Only | No Real Orders | Production Trading: BLOCKED**",
            "",
            "---",
            "",
            self._section_overview(combined_session, now_str),
            self._section_replay_events(events_summary),
            self._section_opening_range(opening_range_summary),
            self._section_vwap(vwap_summary),
            self._section_fake_breakout(fake_breakout_summary),
            self._section_volume_profile(volume_profile_summary),
            self._section_training(training_summary or metrics),
            self._section_safety(),
        ]

        content = "\n".join(sections)
        filename = f"intraday_replay_report_{date_str}.md"
        out_path = os.path.join(self._report_dir, filename)

        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("[IntradayReplayReportBuilder] saved: %s", out_path)
        except Exception as exc:
            logger.error("[IntradayReplayReportBuilder] save error: %s", exc)

        return out_path
