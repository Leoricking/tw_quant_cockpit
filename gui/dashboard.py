"""
gui/dashboard.py - TW Quant Cockpit v0.2 Main Dashboard (PySide6).

Launch via:
    python main.py cockpit [--mode mock|real]

Features:
  - 上方工具列   ControlPanel (mode switch, refresh, import, report)
  - 大盤狀態區   MarketStatusBar
  - 左側列表    CandidatesPanel (clickable stock list)
  - 中間詳情    StockDetailPanel + DataStatusPanel (tabbed)
  - 右側策略    StrategyPanel (4 timeframes)
  - 下方面板    ReportPanel | LogPanel (tabbed)
  - 個股五檔    OrderBookPanel
  - 分析評分    ScorePanel
  - 模擬持倉    PositionsPanel

All data comes from MockBroker / screener_pipeline in mock mode.
Real-order execution is NOT implemented and is explicitly blocked.
"""

import sys
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PySide6 availability guard
# ---------------------------------------------------------------------------
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QSplitter, QLabel, QTableWidget, QTableWidgetItem, QTextEdit,
        QGroupBox, QPushButton, QHeaderView, QSizePolicy, QStatusBar,
        QTabWidget, QFrame,
    )
    from PySide6.QtCore import Qt, QTimer, Signal, QThread
    from PySide6.QtGui import QColor, QFont, QPalette
    _PYSIDE6_AVAILABLE = True
except ImportError:
    _PYSIDE6_AVAILABLE = False
    logger.error("PySide6 not installed. Run: pip install PySide6")

# ---------------------------------------------------------------------------
# Phase 5 panel imports (all guarded — panels self-degrade if PySide6 missing)
# ---------------------------------------------------------------------------
try:
    from gui.gui_state import GUIState
    from gui.control_panel import ControlPanel
    from gui.stock_detail_panel import StockDetailPanel
    from gui.data_status_panel import DataStatusPanel
    from gui.strategy_panel import StrategyPanel
    from gui.import_panel import ImportPanel
    from gui.report_panel import ReportPanel
    _PHASE5_PANELS = True
except Exception as _p5_exc:
    logger.warning("Phase 5 panels unavailable: %s", _p5_exc)
    _PHASE5_PANELS = False

# ---------------------------------------------------------------------------
# v0.3.13 Portfolio Cockpit panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.portfolio_cockpit_panel import PortfolioCockpitPanel
    _PORTFOLIO_COCKPIT_AVAILABLE = True
except Exception as _pc_exc:
    logger.warning("PortfolioCockpitPanel unavailable: %s", _pc_exc)
    _PORTFOLIO_COCKPIT_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.14 Signal Quality panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.signal_quality_panel import SignalQualityPanel
    _SIGNAL_QUALITY_AVAILABLE = True
except Exception as _sq_exc:
    logger.warning("SignalQualityPanel unavailable: %s", _sq_exc)
    _SIGNAL_QUALITY_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.15 Rule Weight Tuning panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.rule_weight_tuning_panel import RuleWeightTuningPanel
    _RULE_WEIGHT_TUNING_AVAILABLE = True
except Exception as _rwt_exc:
    logger.warning("RuleWeightTuningPanel unavailable: %s", _rwt_exc)
    _RULE_WEIGHT_TUNING_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.16 Auto Report Center panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.auto_report_center_panel import AutoReportCenterPanel
    _AUTO_REPORT_CENTER_AVAILABLE = True
except Exception as _arc_exc:
    logger.warning("AutoReportCenterPanel unavailable: %s", _arc_exc)
    _AUTO_REPORT_CENTER_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.17 Automation Scheduler panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.automation_scheduler_panel import AutomationSchedulerPanel
    _AUTOMATION_SCHEDULER_AVAILABLE = True
except Exception as _as_exc:
    logger.warning("AutomationSchedulerPanel unavailable: %s", _as_exc)
    _AUTOMATION_SCHEDULER_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.18 Provider Health panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.provider_health_panel import ProviderHealthPanel
    _PROVIDER_HEALTH_AVAILABLE = True
except Exception as _ph_exc:
    logger.warning("ProviderHealthPanel unavailable: %s", _ph_exc)
    _PROVIDER_HEALTH_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.19 Data Provider Fetch panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.data_provider_fetch_panel import DataProviderFetchPanel
    _DATA_PROVIDER_FETCH_AVAILABLE = True
except Exception as _dpf_exc:
    logger.warning("DataProviderFetchPanel unavailable: %s", _dpf_exc)
    _DATA_PROVIDER_FETCH_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.20 Data Quality Gate panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.data_quality_gate_panel import DataQualityGatePanel
    _DATA_QUALITY_GATE_AVAILABLE = True
except Exception as _dqg_exc:
    logger.warning("DataQualityGatePanel unavailable: %s", _dqg_exc)
    _DATA_QUALITY_GATE_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.21 Daily Workflow panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.daily_workflow_panel import DailyWorkflowPanel
    _DAILY_WORKFLOW_AVAILABLE = True
except Exception as _dw_exc:
    logger.warning("DailyWorkflowPanel unavailable: %s", _dw_exc)
    _DAILY_WORKFLOW_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.22 Usability QA panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.usability_qa_panel import UsabilityQAPanel
    _USABILITY_QA_AVAILABLE = True
except Exception as _uqa_exc:
    logger.warning("UsabilityQAPanel unavailable: %s", _uqa_exc)
    _USABILITY_QA_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.24 Provider Reliability panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.provider_reliability_panel import ProviderReliabilityPanel
    _PROVIDER_RELIABILITY_AVAILABLE = True
except Exception as _prel_exc:
    logger.warning("ProviderReliabilityPanel unavailable: %s", _prel_exc)
    _PROVIDER_RELIABILITY_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.25 Universe Manager panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.universe_manager_panel import UniverseManagerPanel
    _UNIVERSE_MANAGER_AVAILABLE = True
except Exception as _umgr_exc:
    logger.warning("UniverseManagerPanel unavailable: %s", _umgr_exc)
    _UNIVERSE_MANAGER_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.26 Hardened Backtest panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.hardened_backtest_panel import HardenedBacktestPanel
    _HARDENED_BACKTEST_AVAILABLE = True
except Exception as _hb_exc:
    logger.warning("HardenedBacktestPanel unavailable: %s", _hb_exc)
    _HARDENED_BACKTEST_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.27 Intraday Pipeline panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.intraday_pipeline_panel import IntradayPipelinePanel
    _INTRADAY_PIPELINE_AVAILABLE = True
except Exception as _ip_exc:
    logger.warning("IntradayPipelinePanel unavailable: %s", _ip_exc)
    _INTRADAY_PIPELINE_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.28 Rule Governance panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.rule_governance_panel import RuleGovernancePanel
    _RULE_GOVERNANCE_AVAILABLE = True
except Exception as _rg_exc:
    logger.warning("RuleGovernancePanel unavailable: %s", _rg_exc)
    _RULE_GOVERNANCE_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.3.29 Experiment Registry panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.experiment_registry_panel import ExperimentRegistryPanel
    _EXPERIMENT_REGISTRY_AVAILABLE = True
except Exception as _er_exc:
    logger.warning("ExperimentRegistryPanel unavailable: %s", _er_exc)
    _EXPERIMENT_REGISTRY_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.4.0 Release Status panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.release_status_panel import ReleaseStatusPanel
    _RELEASE_STATUS_AVAILABLE = True
except Exception as _rs_exc:
    logger.warning("ReleaseStatusPanel unavailable: %s", _rs_exc)
    _RELEASE_STATUS_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.4.1 API Fetch Status panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.api_fetch_status_panel import APIFetchStatusPanel
    _API_FETCH_STATUS_AVAILABLE = True
except Exception as _afs_exc:
    logger.warning("APIFetchStatusPanel unavailable: %s", _afs_exc)
    _API_FETCH_STATUS_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.4.2 ML Feature Store panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.ml_feature_store_panel import MLFeatureStorePanel
    _ML_FEATURE_STORE_AVAILABLE = True
except Exception as _mfs_exc:
    logger.warning("MLFeatureStorePanel unavailable: %s", _mfs_exc)
    _ML_FEATURE_STORE_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.4.3 Model Monitoring panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.model_monitoring_panel import ModelMonitoringPanel
    _MODEL_MONITORING_AVAILABLE = True
except Exception as _mm_exc:
    logger.warning("ModelMonitoringPanel unavailable: %s", _mm_exc)
    _MODEL_MONITORING_AVAILABLE = False


# ---------------------------------------------------------------------------
# v0.4.4 Intraday Replay panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.intraday_replay_panel import IntradayReplayPanel
    _INTRADAY_REPLAY_AVAILABLE = True
except Exception as _irrp_exc:
    logger.warning("IntradayReplayPanel unavailable: %s", _irrp_exc)
    _INTRADAY_REPLAY_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.5.6 Replay Training panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.replay_training_panel import ReplayTrainingPanel
    _REPLAY_TRAINING_AVAILABLE = True
except Exception as _rtp_exc:
    logger.warning("ReplayTrainingPanel unavailable: %s", _rtp_exc)
    _REPLAY_TRAINING_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.6.0 Stable Release panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.stable_release_panel import StableReleasePanel
    _STABLE_RELEASE_AVAILABLE = True
except Exception as _srp_exc:
    logger.warning("StableReleasePanel unavailable: %s", _srp_exc)
    _STABLE_RELEASE_AVAILABLE = False


# ---------------------------------------------------------------------------
# v0.4.1.1 Strategy Knowledge Ingestion panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.strategy_knowledge_ingestion_panel import StrategyKnowledgeIngestionPanel
    _STRATEGY_KNOWLEDGE_INGESTION_AVAILABLE = True
except Exception as _ski_exc:
    logger.warning("StrategyKnowledgeIngestionPanel unavailable: %s", _ski_exc)
    _STRATEGY_KNOWLEDGE_INGESTION_AVAILABLE = False


# ---------------------------------------------------------------------------
# v0.4.2.1 ML Knowledge Integration panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.ml_knowledge_integration_panel import MLKnowledgeIntegrationPanel
    _ML_KNOWLEDGE_INTEGRATION_AVAILABLE = True
except Exception as _mki_exc:
    logger.warning("MLKnowledgeIntegrationPanel unavailable: %s", _mki_exc)
    _ML_KNOWLEDGE_INTEGRATION_AVAILABLE = False


# ---------------------------------------------------------------------------
# v0.4.5 Notification Center panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.notification_center_panel import NotificationCenterPanel
    _NOTIFICATION_CENTER_AVAILABLE = True
except Exception as _nc_exc:
    logger.warning("NotificationCenterPanel unavailable: %s", _nc_exc)
    _NOTIFICATION_CENTER_AVAILABLE = False


# ---------------------------------------------------------------------------
# v0.4.6 Portfolio Journal panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.portfolio_journal_panel import PortfolioJournalPanel
    _PORTFOLIO_JOURNAL_AVAILABLE = True
except Exception as _pj_exc:
    logger.warning("PortfolioJournalPanel unavailable: %s", _pj_exc)
    _PORTFOLIO_JOURNAL_AVAILABLE = False


# ---------------------------------------------------------------------------
# v0.4.7 Research Review Dashboard panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.research_review_dashboard_panel import ResearchReviewDashboardPanel
    _RESEARCH_REVIEW_AVAILABLE = True
except Exception as _rr_exc:
    logger.warning("ResearchReviewDashboardPanel unavailable: %s", _rr_exc)
    _RESEARCH_REVIEW_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.4.8 Research Assistant / Coach panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.research_assistant_panel import ResearchAssistantPanel
    _RESEARCH_COACH_AVAILABLE = True
except Exception as _rc_exc:
    logger.warning("ResearchAssistantPanel unavailable: %s", _rc_exc)
    _RESEARCH_COACH_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.4.9 Research Workflow Automation panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.research_workflow_panel import ResearchWorkflowPanel
    _RESEARCH_WORKFLOW_AVAILABLE = True
except Exception as _rw_exc:
    logger.warning("ResearchWorkflowPanel unavailable: %s", _rw_exc)
    _RESEARCH_WORKFLOW_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.5.0 Research OS Planning panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.research_os_planning_panel import ResearchOSPlanningPanel
    _RESEARCH_OS_PLANNING_AVAILABLE = True
except Exception as _ros_exc:
    logger.warning("ResearchOSPlanningPanel unavailable: %s", _ros_exc)
    _RESEARCH_OS_PLANNING_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.5.1 CLI UX panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.cli_ux_panel import CLIUXPanel
    _CLI_UX_AVAILABLE = True
except Exception as _cux_exc:
    logger.warning("CLIUXPanel unavailable: %s", _cux_exc)
    _CLI_UX_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.5.2 GUI Navigation panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.gui_navigation_panel import GUINavigationPanel
    _GUI_NAVIGATION_AVAILABLE = True
except Exception as _gn_exc:
    logger.warning("GUINavigationPanel unavailable: %s", _gn_exc)
    _GUI_NAVIGATION_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.5.3 Regression Suite panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.regression_suite_panel import RegressionSuitePanel
    _REGRESSION_SUITE_AVAILABLE = True
except Exception as _rs_exc:
    logger.warning("RegressionSuitePanel unavailable: %s", _rs_exc)
    _REGRESSION_SUITE_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.5.4 Report Pack panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.report_pack_panel import ReportPackPanel
    _REPORT_PACK_AVAILABLE = True
except Exception as _rp_exc:
    logger.warning("ReportPackPanel unavailable: %s", _rp_exc)
    _REPORT_PACK_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.5.5 Data Stabilization panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.data_stabilization_panel import DataStabilizationPanel, _DATA_STAB_PANEL_AVAILABLE
except Exception as _ds_exc:
    logger.warning("DataStabilizationPanel unavailable: %s", _ds_exc)
    _DATA_STAB_PANEL_AVAILABLE = False
    DataStabilizationPanel = None

# ---------------------------------------------------------------------------
# v0.6.2 Data Coverage Expansion panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.data_coverage_panel import DataCoveragePanel
    _DATA_COVERAGE_AVAILABLE = True
except Exception as _dc_exc:
    logger.warning("DataCoveragePanel unavailable: %s", _dc_exc)
    _DATA_COVERAGE_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.7.0 Research Intelligence panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.research_intelligence_panel import ResearchIntelligencePanel
    _RESEARCH_INTELLIGENCE_AVAILABLE = True
except Exception as _ri_exc:
    logger.warning("ResearchIntelligencePanel unavailable: %s", _ri_exc)
    _RESEARCH_INTELLIGENCE_AVAILABLE = False

# ---------------------------------------------------------------------------
# v0.7.2 Strategy Research Memory panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.strategy_memory_panel import StrategyMemoryPanel
    _STRATEGY_MEMORY_AVAILABLE = True
except Exception as _sm_exc:
    logger.warning("StrategyMemoryPanel unavailable: %s", _sm_exc)
    _STRATEGY_MEMORY_AVAILABLE = False

# v0.7.3 Backtest-to-Coach Loop panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.backtest_coach_panel import BacktestCoachPanel
    _BACKTEST_COACH_AVAILABLE = True
except Exception as _bc_exc:
    logger.warning("BacktestCoachPanel unavailable: %s", _bc_exc)
    _BACKTEST_COACH_AVAILABLE = False

# v0.8.0 Research Intelligence Stable panel import (guarded)
# ---------------------------------------------------------------------------
try:
    from gui.intelligence_stable_panel import IntelligenceStablePanel
    _INTELLIGENCE_STABLE_AVAILABLE = True
except Exception as _is_exc:
    logger.warning("IntelligenceStablePanel unavailable: %s", _is_exc)
    _INTELLIGENCE_STABLE_AVAILABLE = False

# v0.8.2 Training Metrics panel
# ---------------------------------------------------------------------------
try:
    from gui.training_metrics_panel import TrainingMetricsPanel
    _TRAINING_METRICS_AVAILABLE = True
except Exception as _tm_exc:
    logger.warning("TrainingMetricsPanel unavailable: %s", _tm_exc)
    _TRAINING_METRICS_AVAILABLE = False

# v0.8.3 Evidence Graph panel
# ---------------------------------------------------------------------------
try:
    from gui.evidence_graph_panel import EvidenceGraphPanel
    _EVIDENCE_GRAPH_AVAILABLE = True
except Exception as _eg_exc:
    logger.warning("EvidenceGraphPanel unavailable: %s", _eg_exc)
    _EVIDENCE_GRAPH_AVAILABLE = False

# v0.9.0 Strategy Lab Stable panel
# ---------------------------------------------------------------------------
try:
    from gui.strategy_lab_panel import StrategyLabPanel
    _STRATEGY_LAB_AVAILABLE = True
except Exception as _sl_exc:
    logger.warning("StrategyLabPanel unavailable: %s", _sl_exc)
    _STRATEGY_LAB_AVAILABLE = False

# v0.9.0.1 Crash Reversal
# ---------------------------------------------------------------------------
_CRASH_REVERSAL_AVAILABLE = False
try:
    from gui.crash_reversal_panel import CrashReversalPanel
    _CRASH_REVERSAL_AVAILABLE = True
except ImportError:
    pass

# v0.9.2 Strategy Validation
_STRATEGY_VALIDATION_AVAILABLE = False
try:
    from gui.strategy_validation_panel import StrategyValidationPanel
    _STRATEGY_VALIDATION_AVAILABLE = True
except ImportError:
    pass

# v0.9.3 Strategy Lab Dashboard
_STRATEGY_LAB_DASHBOARD_AVAILABLE = False
try:
    from gui.strategy_lab_dashboard_panel import StrategyLabDashboardPanel
    _STRATEGY_LAB_DASHBOARD_AVAILABLE = True
except ImportError:
    pass

# v1.0.2 Data & Report Hygiene
_DATA_REPORT_HYGIENE_AVAILABLE = False
try:
    from gui.data_report_hygiene_panel import DataReportHygienePanel
    _DATA_REPORT_HYGIENE_AVAILABLE = True
except ImportError:
    pass

# v1.0.7 Knowledge Base Search Panel
_KNOWLEDGE_BASE_SEARCH_AVAILABLE = False
try:
    from gui.knowledge_base_search_panel import KnowledgeBaseSearchPanel
    _KNOWLEDGE_BASE_SEARCH_AVAILABLE = True
except Exception:
    pass

# v1.0.8 Local Research Assistant Panel
_LOCAL_RESEARCH_ASSISTANT_AVAILABLE = False
try:
    from gui.local_research_assistant_panel import LocalResearchAssistantPanel
    _LOCAL_RESEARCH_ASSISTANT_AVAILABLE = True
except Exception:
    pass

# v1.0.9 Final Maintenance Rollup Panel
_FINAL_ROLLUP_AVAILABLE = False
try:
    from gui.final_rollup_panel import FinalRollupPanel
    _FINAL_ROLLUP_AVAILABLE = True
except Exception:
    pass

# v0.5.1.1 Strategy Filter panel — inline (no separate panel file required)
# ---------------------------------------------------------------------------
_STRATEGY_FILTER_AVAILABLE = False
try:
    from strategy_filters.strategy_filter_pack import StrategyFilterPack as _SFPack
    _STRATEGY_FILTER_AVAILABLE = True
except Exception as _sf_exc:
    logger.warning("StrategyFilterPack unavailable: %s", _sf_exc)


# ---------------------------------------------------------------------------
# Colour helpers (Taiwan convention: red = up, green = down)
# ---------------------------------------------------------------------------

def _change_color(pct: float) -> str:
    if pct > 0:
        return "#FF4444"   # red = up
    if pct < 0:
        return "#33CC66"   # green = down
    return "#AAAAAA"


def _score_color(score: float) -> str:
    if score >= 80:
        return "#FF4444"
    if score >= 65:
        return "#FF8800"
    if score >= 50:
        return "#CCCC00"
    return "#888888"


# ---------------------------------------------------------------------------
# Data refresh worker (runs in background thread)
# ---------------------------------------------------------------------------

class DataWorker(QThread if _PYSIDE6_AVAILABLE else object):
    """Background thread that fetches mock market data every N seconds."""

    if _PYSIDE6_AVAILABLE:
        data_ready = Signal(dict)

    def __init__(self, broker, screener_pipeline, paper_trader, interval=3):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self.broker = broker
        self.screener_pipeline = screener_pipeline
        self.paper_trader = paper_trader
        self.interval = interval
        self._running = False

    def run(self):
        import time
        self._running = True
        while self._running:
            try:
                payload = self._fetch()
                if _PYSIDE6_AVAILABLE:
                    self.data_ready.emit(payload)
            except Exception as exc:
                logger.error("DataWorker error: %s", exc)
            # Sleep in short chunks so stop() takes effect quickly
            elapsed = 0.0
            while self._running and elapsed < self.interval:
                time.sleep(0.2)
                elapsed += 0.2

    def stop(self):
        self._running = False

    def _fetch(self) -> dict:
        """Collect all data needed by the dashboard."""
        # Market snapshot from mock broker
        market = self.broker.get_market_snapshot() if self.broker else {}

        # Screener top candidates
        try:
            candidates = self.screener_pipeline.run() if self.screener_pipeline else []
        except Exception:
            candidates = []

        # Paper trader summary
        try:
            positions = self.paper_trader.get_positions() if self.paper_trader else []
            pnl_summary = self.paper_trader.get_pnl_summary() if self.paper_trader else {}
        except Exception:
            positions = []
            pnl_summary = {}

        # Per-symbol tick data
        ticks = {}
        if self.broker:
            for sym in self.broker.get_symbols():
                try:
                    ticks[sym] = self.broker.get_tick(sym)
                except Exception:
                    pass

        return {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'market': market,
            'candidates': candidates,
            'positions': positions,
            'pnl_summary': pnl_summary,
            'ticks': ticks,
        }


# ---------------------------------------------------------------------------
# Helper: styled QLabel
# ---------------------------------------------------------------------------

def _label(text, bold=False, color=None, size=None):
    lbl = QLabel(text)
    style_parts = []
    if bold:
        style_parts.append("font-weight:bold")
    if color:
        style_parts.append(f"color:{color}")
    if size:
        style_parts.append(f"font-size:{size}px")
    if style_parts:
        lbl.setStyleSheet(";".join(style_parts))
    return lbl


# ---------------------------------------------------------------------------
# Market Status Bar widget
# ---------------------------------------------------------------------------

class MarketStatusBar(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows TAIEX index, date/time, and market session state."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)

        self._lbl_title = _label("TW Quant Cockpit v1", bold=True, size=16)
        self._lbl_time = _label("--:--:--", color="#AAAAAA")
        self._lbl_taiex = _label("加權指數: ---", bold=True, color="#FF8800", size=13)
        self._lbl_mode = _label("[MOCK MODE]", bold=True, color="#33CCFF")
        self._lbl_session = _label("盤前", color="#AAAAAA")

        layout.addWidget(self._lbl_title)
        layout.addSpacing(20)
        layout.addWidget(self._lbl_taiex)
        layout.addSpacing(10)
        layout.addWidget(self._lbl_session)
        layout.addStretch()
        layout.addWidget(self._lbl_mode)
        layout.addSpacing(10)
        layout.addWidget(self._lbl_time)

        self.setStyleSheet("background:#1E1E2E; border-radius:4px; padding:2px")

    def update(self, market: dict, timestamp: str):
        if not _PYSIDE6_AVAILABLE:
            return
        self._lbl_time.setText(timestamp)
        taiex = market.get('taiex', 0)
        taiex_chg = market.get('taiex_change_pct', 0)
        color = _change_color(taiex_chg)
        self._lbl_taiex.setText(f"加權指數: {taiex:,.0f}  ({taiex_chg:+.2f}%)")
        self._lbl_taiex.setStyleSheet(f"font-weight:bold;color:{color};font-size:13px")
        session = market.get('session', '盤前')
        self._lbl_session.setText(session)


# ---------------------------------------------------------------------------
# Input normalizer — converts DataFrame / dict / list[str] / None to list[dict]
# ---------------------------------------------------------------------------

def normalize_records(obj):
    """Normalize DataFrame / dict / list[dict] / list[str] / None into list[dict]."""
    if obj is None:
        return []

    try:
        import pandas as pd
        if isinstance(obj, pd.DataFrame):
            if obj.empty:
                return []
            return obj.to_dict(orient="records")
    except Exception:
        pass

    if isinstance(obj, dict):
        if "symbol" in obj:
            return [obj]
        rows = []
        for k, v in obj.items():
            if isinstance(v, dict):
                row = dict(v)
                row.setdefault("symbol", str(k))
                rows.append(row)
            else:
                rows.append({"symbol": str(k), "value": v})
        return rows

    if isinstance(obj, (list, tuple)):
        rows = []
        for item in obj:
            if isinstance(item, dict):
                rows.append(item)
            else:
                rows.append({"symbol": str(item)})
        return rows

    return []


# ---------------------------------------------------------------------------
# Stock Monitoring Table
# ---------------------------------------------------------------------------

_TABLE_COLS = [
    'symbol', 'name', 'price', 'change_pct',
    'bull_score', 'daytrade_score', 'swing_score', 'risk_score',
    'orderbook_state', 'decision', 'position', 'pnl',
    'buy_point_grade', 'buy_point_type', 'support_price', 'confirm_price', 'invalid_price',
]
_TABLE_HEADERS = [
    '代號', '名稱', '價格', '漲跌%',
    '飆股分', '當沖分', '波段分', '風險分',
    '五檔狀態', '建議', '持倉', '損益',
    '買點等級', '買點型態', '支撐價', '確認價', '失效價',
]


class StockTable(QWidget if _PYSIDE6_AVAILABLE else object):
    """Main stock monitoring table."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()
        self._rows = {}   # symbol -> row_index

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = _label("股票監控表", bold=True, size=12)
        layout.addWidget(header)

        self._table = QTableWidget()
        self._table.setColumnCount(len(_TABLE_COLS))
        self._table.setHorizontalHeaderLabels(_TABLE_HEADERS)
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setStyleSheet("""
            QTableWidget { background:#12121E; color:#EEEEEE; gridline-color:#333355; }
            QTableWidget::item:alternate { background:#1A1A2E; }
            QHeaderView::section { background:#252540; color:#AAAAFF; font-weight:bold; }
        """)
        layout.addWidget(self._table)

    def update(self, ticks: dict, candidates: list, positions: list):
        if not _PYSIDE6_AVAILABLE:
            return

        # Normalize all inputs; ticks stays a dict for symbol-keyed lookups
        candidates = normalize_records(candidates)
        positions = normalize_records(positions)
        if not isinstance(ticks, dict):
            ticks = {
                str(t.get('symbol', '')): t
                for t in normalize_records(ticks)
                if isinstance(t, dict) and t.get('symbol')
            }

        # Build defensive lookups
        cand_map = {}
        for c in candidates:
            if not isinstance(c, dict):
                continue
            sym = str(c.get('symbol', '')).strip()
            if sym:
                cand_map[sym] = c

        pos_map = {}
        for p in positions:
            if not isinstance(p, dict):
                continue
            sym = str(p.get('symbol', '')).strip()
            if sym:
                pos_map[sym] = p

        # Merge symbols from ticks + candidates + positions
        all_syms = list(dict.fromkeys(
            list(ticks.keys()) +
            [str(c.get('symbol', '')) for c in candidates if isinstance(c, dict)] +
            list(pos_map.keys())
        ))

        self._table.setRowCount(len(all_syms))

        for row, sym in enumerate(all_syms):
            tick = ticks.get(sym, {})
            cand = cand_map.get(sym, {})
            pos = pos_map.get(sym, {})

            price = tick.get('price', cand.get('price', 0)) or 0
            change_pct = tick.get('change_pct', 0) or 0
            name = tick.get('name', cand.get('name', sym))
            bull_score = cand.get('bull_stock_score', 0)
            daytrade_score = cand.get('daytrade_score', 0)
            swing_score = cand.get('swing_score', 0)
            risk_score = cand.get('risk_score', 0)
            ob_state = cand.get('orderbook_state', '-')
            decision = cand.get('decision', '-')
            position = pos.get('quantity', 0)
            pnl = pos.get('unrealized_pnl', 0)

            def _cell(text, color=None):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                if color:
                    item.setForeground(QColor(color))
                return item

            chg_color = _change_color(change_pct)

            self._table.setItem(row, 0, _cell(sym))
            self._table.setItem(row, 1, _cell(name))
            self._table.setItem(row, 2, _cell(f"{price:.1f}" if price else '-'))
            self._table.setItem(row, 3, _cell(f"{change_pct:+.2f}%" if change_pct else '-', color=chg_color))
            self._table.setItem(row, 4, _cell(f"{bull_score:.0f}" if bull_score else '-', color=_score_color(bull_score)))
            self._table.setItem(row, 5, _cell(f"{daytrade_score:.0f}" if daytrade_score else '-'))
            self._table.setItem(row, 6, _cell(f"{swing_score:.0f}" if swing_score else '-'))
            self._table.setItem(row, 7, _cell(f"{risk_score:.0f}" if risk_score else '-'))
            self._table.setItem(row, 8, _cell(ob_state))
            self._table.setItem(row, 9, _cell(decision))
            self._table.setItem(row, 10, _cell(str(position) if position else '-'))
            pnl_color = _change_color(pnl)
            self._table.setItem(row, 11, _cell(f"{pnl:+,.0f}" if pnl else '-', color=pnl_color))

            # Buy point columns
            bp_grade = cand.get('buy_point_grade', '-') or '-'
            bp_type = cand.get('buy_point_type', '-') or '-'
            bp_support = cand.get('support_price')
            bp_confirm = cand.get('confirm_price')
            bp_invalid = cand.get('invalid_price')
            grade_color = {'A': '#FF4444', 'B': '#FF8800', 'C': '#CCCC00'}.get(bp_grade)
            self._table.setItem(row, 12, _cell(bp_grade, color=grade_color))
            self._table.setItem(row, 13, _cell(bp_type))
            self._table.setItem(row, 14, _cell(f"{bp_support:.1f}" if bp_support else '-'))
            self._table.setItem(row, 15, _cell(f"{bp_confirm:.1f}" if bp_confirm else '-'))
            self._table.setItem(row, 16, _cell(f"{bp_invalid:.1f}" if bp_invalid else '-'))


# ---------------------------------------------------------------------------
# Bull Candidates Panel
# ---------------------------------------------------------------------------

class CandidatesPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows top 3-8 bull candidates with scores."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("飆股候選 Top 3~8", bold=True, size=12, color="#FF8800")
        layout.addWidget(header)

        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(['代號', '名稱', '綜合分', '主題', '建議'])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setMaximumHeight(260)
        self._table.setStyleSheet("""
            QTableWidget { background:#0E1520; color:#EEEEEE; }
            QHeaderView::section { background:#252540; color:#FFAA44; font-weight:bold; }
        """)
        layout.addWidget(self._table)
        layout.addStretch()

    def update(self, candidates: list):
        if not _PYSIDE6_AVAILABLE:
            return
        candidates = normalize_records(candidates)
        top = candidates[:8]
        self._table.setRowCount(len(top))
        for row, c in enumerate(top):
            if not isinstance(c, dict):
                continue
            sym = str(c.get('symbol', '') or '').strip()
            name = str(c.get('name', sym) or sym)
            score = float(c.get('bull_stock_score', c.get('score', 0)) or 0)
            themes = ','.join(c.get('theme_tags', [])) if c.get('theme_tags') else '-'
            decision = str(c.get('decision', '-') or '-')

            def _cell(text, color=None):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                if color:
                    item.setForeground(QColor(color))
                return item

            self._table.setItem(row, 0, _cell(sym))
            self._table.setItem(row, 1, _cell(name))
            self._table.setItem(row, 2, _cell(f"{score:.0f}", color=_score_color(score)))
            self._table.setItem(row, 3, _cell(themes))
            self._table.setItem(row, 4, _cell(decision))


# ---------------------------------------------------------------------------
# Order Book Panel
# ---------------------------------------------------------------------------

class OrderBookPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows 5-level bid/ask for a selected symbol."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("五檔委買委賣", bold=True, size=12)
        layout.addWidget(header)

        self._sym_label = _label("---", color="#AAAAFF", size=11)
        layout.addWidget(self._sym_label)

        # Bid table (委買)
        layout.addWidget(_label("委買", color="#FF5555"))
        self._bid_table = self._make_table()
        layout.addWidget(self._bid_table)

        # Ask table (委賣)
        layout.addWidget(_label("委賣", color="#55CC55"))
        self._ask_table = self._make_table()
        layout.addWidget(self._ask_table)

        layout.addStretch()

    def _make_table(self):
        t = QTableWidget(5, 2)
        t.setHorizontalHeaderLabels(['價格', '數量'])
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.setMaximumHeight(160)
        t.setEditTriggers(QTableWidget.NoEditTriggers)
        t.setStyleSheet("QTableWidget { background:#0E1520; color:#EEEEEE; } QHeaderView::section { background:#252540; }")
        return t

    def update(self, symbol: str, bidask: dict):
        if not _PYSIDE6_AVAILABLE:
            return
        self._sym_label.setText(f"代號：{symbol}")

        for i in range(1, 6):
            row = i - 1
            bp = bidask.get(f'bid_price_{i}', '-')
            bv = bidask.get(f'bid_volume_{i}', '-')
            ap = bidask.get(f'ask_price_{i}', '-')
            av = bidask.get(f'ask_volume_{i}', '-')

            self._bid_table.setItem(row, 0, QTableWidgetItem(str(bp)))
            self._bid_table.setItem(row, 1, QTableWidgetItem(str(bv)))
            self._ask_table.setItem(row, 0, QTableWidgetItem(str(ap)))
            self._ask_table.setItem(row, 1, QTableWidgetItem(str(av)))


# ---------------------------------------------------------------------------
# Score / Decision Panel
# ---------------------------------------------------------------------------

class ScorePanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows scores and AI decision for a selected stock."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("評分 & 建議", bold=True, size=12)
        layout.addWidget(header)

        self._sym_label = _label("---", color="#AAAAFF", size=11)
        layout.addWidget(self._sym_label)

        rows_data = [
            ('飆股分', '_lbl_bull'),
            ('當沖分', '_lbl_daytrade'),
            ('波段分', '_lbl_swing'),
            ('風險分', '_lbl_risk'),
            ('建議',   '_lbl_decision'),
            ('KD訊號',  '_lbl_kd_signal'),
            ('融券訊號', '_lbl_short_interest'),
            ('破底翻',  '_lbl_bottom_reversal'),
            ('族群訊號', '_lbl_sector_signal'),
            ('基本面品質', '_lbl_fq_score'),
        ]
        for label_text, attr in rows_data:
            row = QHBoxLayout()
            row.addWidget(_label(f"{label_text}：", bold=True))
            lbl = _label('---')
            setattr(self, attr, lbl)
            row.addWidget(lbl)
            row.addStretch()
            layout.addLayout(row)

        layout.addSpacing(8)
        layout.addWidget(_label("判斷依據：", bold=True))
        self._txt_reasoning = QTextEdit()
        self._txt_reasoning.setReadOnly(True)
        self._txt_reasoning.setMaximumHeight(100)
        self._txt_reasoning.setStyleSheet("background:#0E1520; color:#CCCCCC; font-size:11px")
        layout.addWidget(self._txt_reasoning)

        layout.addWidget(_label("── Phase 2 Strategy Signals ──", bold=True, color="#AAAAFF"))
        layout.addStretch()

    def update(self, symbol: str, candidate: dict):
        if not _PYSIDE6_AVAILABLE:
            return
        self._sym_label.setText(f"代號：{symbol}")

        bull = candidate.get('bull_stock_score', 0)
        dt = candidate.get('daytrade_score', 0)
        sw = candidate.get('swing_score', 0)
        risk = candidate.get('risk_score', 0)
        decision = candidate.get('decision', '---')
        reasoning = candidate.get('reason_summary', candidate.get('reasoning', '資料不足，只能做盤中初估，不能當正式短中長線操作依據'))

        def _set_score(lbl, val):
            lbl.setText(f"{val:.0f}" if val else '---')
            lbl.setStyleSheet(f"color:{_score_color(float(val or 0))};font-weight:bold")

        _set_score(self._lbl_bull, bull)
        _set_score(self._lbl_daytrade, dt)
        _set_score(self._lbl_swing, sw)
        _set_score(self._lbl_risk, risk)
        self._lbl_decision.setText(str(decision))
        self._txt_reasoning.setPlainText(str(reasoning))

        # Phase 2 signals
        def _p2_lbl(lbl_attr, val, warn_color='#FF8888', ok_color='#44CC88', neutral_color='#CCCCCC'):
            lbl = getattr(self, lbl_attr, None)
            if lbl is None:
                return
            if val is None or val == '' or (isinstance(val, float) and val != val):
                lbl.setText('unavailable')
                lbl.setStyleSheet(f'color:#888888')
            else:
                lbl.setText(str(val))
                _v = str(val).upper()
                if any(w in _v for w in ('SELL', 'DEATH', 'WEAK', 'WARNING', 'RISK', 'LOW')):
                    lbl.setStyleSheet(f'color:{warn_color}')
                elif any(w in _v for w in ('BUY', 'GOLDEN', 'SQUEEZE', 'LAGGARD', 'STRONG')):
                    lbl.setStyleSheet(f'color:{ok_color}')
                else:
                    lbl.setStyleSheet(f'color:{neutral_color}')

        _p2 = candidate.get('phase2_signals', {})
        _kd_adv = _p2.get('kd_advanced', {}) if isinstance(_p2, dict) else {}
        _si_adv = _p2.get('short_interest', {}) if isinstance(_p2, dict) else {}
        _br_adv = _p2.get('bottom_reversal', {}) if isinstance(_p2, dict) else {}
        _sr_adv = _p2.get('sector_rotation', {}) if isinstance(_p2, dict) else {}
        _fq_adv = _p2.get('fundamental_quality', {}) if isinstance(_p2, dict) else {}

        _kd_txt = _kd_adv.get('kd_signal') or candidate.get('kd_signal')
        _si_txt = _si_adv.get('short_interest_signal') or candidate.get('short_interest_signal')
        _br_txt = _br_adv.get('bottom_signal') or candidate.get('bottom_signal')
        _sr_txt = _sr_adv.get('sector_signal') or candidate.get('sector_signal')
        _fq_txt = _fq_adv.get('fundamental_quality_score')
        if _fq_txt is None:
            _fq_txt = candidate.get('fundamental_quality_score')

        _p2_lbl('_lbl_kd_signal', _kd_txt)
        _p2_lbl('_lbl_short_interest', _si_txt)
        _p2_lbl('_lbl_bottom_reversal', _br_txt)
        _p2_lbl('_lbl_sector_signal', _sr_txt)
        _p2_lbl('_lbl_fq_score',
                 f"{_fq_txt:.2f}" if isinstance(_fq_txt, float) else _fq_txt)


# ---------------------------------------------------------------------------
# Paper Positions Panel
# ---------------------------------------------------------------------------

class PositionsPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Shows current paper trading positions and P&L."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("模擬持倉", bold=True, size=12)
        layout.addWidget(header)

        self._pnl_label = _label("今日損益: ---", bold=True, size=13, color="#FFAA44")
        layout.addWidget(self._pnl_label)

        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels(['代號', '名稱', '均成本', '現價', '持倉', '浮動損益'])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setMaximumHeight(200)
        self._table.setStyleSheet("""
            QTableWidget { background:#0E1520; color:#EEEEEE; }
            QHeaderView::section { background:#252540; color:#AAAAFF; font-weight:bold; }
        """)
        layout.addWidget(self._table)
        layout.addStretch()

    def update(self, positions: list, pnl_summary: dict):
        if not _PYSIDE6_AVAILABLE:
            return

        today_pnl = pnl_summary.get('realized_pnl', 0) + pnl_summary.get('unrealized_pnl', 0)
        pnl_color = _change_color(today_pnl)
        self._pnl_label.setText(f"今日損益: {today_pnl:+,.0f} NTD")
        self._pnl_label.setStyleSheet(f"font-weight:bold;font-size:13px;color:{pnl_color}")

        self._table.setRowCount(len(positions))
        for row, pos in enumerate(positions):
            sym = str(pos.get('symbol', ''))
            name = str(pos.get('name', sym))
            cost = float(pos.get('avg_cost', 0) or 0)
            price = float(pos.get('current_price', 0) or 0)
            qty = int(pos.get('quantity', 0) or 0)
            upnl = float(pos.get('unrealized_pnl', 0) or 0)

            def _cell(text, color=None):
                item = QTableWidgetItem(str(text))
                item.setTextAlignment(Qt.AlignCenter)
                if color:
                    item.setForeground(QColor(color))
                return item

            self._table.setItem(row, 0, _cell(sym))
            self._table.setItem(row, 1, _cell(name))
            self._table.setItem(row, 2, _cell(f"{cost:.1f}"))
            self._table.setItem(row, 3, _cell(f"{price:.1f}"))
            self._table.setItem(row, 4, _cell(str(qty)))
            self._table.setItem(row, 5, _cell(f"{upnl:+,.0f}", color=_change_color(upnl)))


# ---------------------------------------------------------------------------
# Log Window
# ---------------------------------------------------------------------------

class LogPanel(QWidget if _PYSIDE6_AVAILABLE else object):
    """Scrollable log output panel."""

    def __init__(self):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
            self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        header = _label("系統 Log", bold=True)
        layout.addWidget(header)

        self._text = QTextEdit()
        self._text.setReadOnly(True)
        self._text.setMaximumHeight(130)
        self._text.setStyleSheet(
            "background:#0A0A14; color:#88FF88; font-family:monospace; font-size:11px"
        )
        layout.addWidget(self._text)

    def append(self, msg: str):
        if not _PYSIDE6_AVAILABLE:
            return
        ts = datetime.now().strftime('%H:%M:%S')
        self._text.append(f"[{ts}] {msg}")
        # Auto-scroll
        sb = self._text.verticalScrollBar()
        sb.setValue(sb.maximum())


# ---------------------------------------------------------------------------
# Qt Log Handler
# ---------------------------------------------------------------------------

class _QLogHandler(logging.Handler if _PYSIDE6_AVAILABLE else object):
    """Redirect Python logging to the LogPanel."""

    def __init__(self, log_panel):
        if _PYSIDE6_AVAILABLE:
            super().__init__()
        self.log_panel = log_panel

    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_panel.append(msg)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Main Window
# ---------------------------------------------------------------------------

class CockpitWindow(QMainWindow if _PYSIDE6_AVAILABLE else object):
    """TW Quant Cockpit v0.2 Main Window."""

    def __init__(self, mode: str = 'mock'):
        if _PYSIDE6_AVAILABLE:
            super().__init__()

        # Shared GUI state
        self._gui_state = GUIState() if _PHASE5_PANELS else None
        if self._gui_state:
            self._gui_state.set_mode(mode)

        self._broker = None
        self._screener = None
        self._paper_trader = None
        self._worker = None
        self._candidates = []
        self._ticks = {}
        self._selected_symbol = None
        self._mode = mode
        self._portfolio_panel = None
        self._signal_quality_panel = None
        self._rule_weight_panel = None
        self._auto_report_panel = None
        self._automation_panel = None
        self._provider_health_panel = None
        self._data_provider_fetch_panel = None
        self._data_quality_gate_panel = None
        self._daily_workflow_panel = None
        self._usability_qa_panel = None
        self._provider_reliability_panel = None
        self._universe_manager_panel = None
        self._hardened_backtest_panel = None

        self._init_backends()
        if _PYSIDE6_AVAILABLE:
            self._build_ui()
            self._start_worker()

    # ---- Backend init ----

    def _init_backends(self):
        """Initialize mock broker, screener, and paper trader."""
        try:
            from broker.mock_broker import MockBroker
            import os
            wl = os.path.join(os.path.dirname(__file__), '..', 'config', 'watchlist.csv')
            self._broker = MockBroker(watchlist_path=wl)
            logger.info("MockBroker initialized.")
        except Exception as exc:
            logger.warning("MockBroker init failed: %s", exc)

        try:
            from screener.screener_pipeline import ScreenerPipeline
            self._screener = ScreenerPipeline()
        except Exception as exc:
            logger.warning("Screener init failed: %s", exc)

        try:
            from sim.simulator import PaperTrader
            self._paper_trader = PaperTrader(initial_capital=1_000_000)
            logger.info("PaperTrader initialized.")
        except Exception as exc:
            logger.warning("PaperTrader init failed: %s", exc)

    # ---- UI Build ----

    def _build_ui(self):
        mode_label = "REAL MODE" if self._mode == 'real' else "MOCK MODE"
        self.setWindowTitle(f"TW Quant Cockpit v0.2  [{mode_label} — 禁止實盤下單]")
        self.resize(1600, 950)
        self.setStyleSheet("background:#12121E; color:#DDDDDD;")

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(4)
        root.setContentsMargins(6, 6, 6, 6)

        # ---- Top: ControlPanel ----
        if _PHASE5_PANELS:
            self._ctrl_panel = ControlPanel(gui_state=self._gui_state)
            self._ctrl_panel.mode_changed.connect(self._on_mode_changed)
            self._ctrl_panel.refresh_screener_requested.connect(self._on_refresh_screener)
            self._ctrl_panel.data_check_requested.connect(self._on_data_check)
            self._ctrl_panel.report_requested.connect(self._on_generate_report)
            self._ctrl_panel.import_requested.connect(self._on_import_csv)
            root.addWidget(self._ctrl_panel)
        else:
            self._ctrl_panel = None

        # ---- Market status bar ----
        self._market_bar = MarketStatusBar()
        root.addWidget(self._market_bar)

        # ---- Main content splitter ----
        h_split = QSplitter(Qt.Horizontal)

        # LEFT: candidates list
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self._stock_table = StockTable()
        left_layout.addWidget(self._stock_table, stretch=3)

        self._candidates_panel = CandidatesPanel()
        # Wire row-click to stock selection
        self._candidates_panel._table.cellClicked.connect(self._on_candidate_clicked)
        left_layout.addWidget(self._candidates_panel, stretch=2)

        h_split.addWidget(left)

        # MIDDLE: detail tabs (詳情 + 策略 + 五檔 + 評分 + 持倉)
        mid_tabs = QTabWidget()
        _tab_style = (
            "QTabBar::tab { background:#252540; color:#AAAAFF; padding:4px 10px; } "
            "QTabBar::tab:selected { background:#3344AA; color:#FFFFFF; }"
        )
        mid_tabs.setStyleSheet(_tab_style)

        # 詳情 tab: StockDetailPanel + DataStatusPanel stacked vertically
        if _PHASE5_PANELS:
            detail_widget = QWidget()
            detail_layout = QVBoxLayout(detail_widget)
            detail_layout.setContentsMargins(0, 0, 0, 0)
            detail_layout.setSpacing(4)
            self._detail_panel = StockDetailPanel()
            self._data_status_panel = DataStatusPanel()
            detail_layout.addWidget(self._detail_panel, stretch=2)
            detail_layout.addWidget(self._data_status_panel, stretch=3)
            mid_tabs.addTab(detail_widget, "詳情")

            self._strategy_panel = StrategyPanel()
            mid_tabs.addTab(self._strategy_panel, "策略")
        else:
            self._detail_panel = None
            self._data_status_panel = None
            self._strategy_panel = None

        self._ob_panel = OrderBookPanel()
        mid_tabs.addTab(self._ob_panel, "五檔")

        self._score_panel = ScorePanel()
        mid_tabs.addTab(self._score_panel, "評分")

        self._pos_panel = PositionsPanel()
        mid_tabs.addTab(self._pos_panel, "持倉")

        # v0.3.13 Portfolio Cockpit tab
        if _PORTFOLIO_COCKPIT_AVAILABLE:
            self._portfolio_panel = PortfolioCockpitPanel(mode=self._mode)
            mid_tabs.addTab(self._portfolio_panel, "Portfolio Cockpit")
        else:
            self._portfolio_panel = None

        # v0.3.14 Signal Quality tab
        if _SIGNAL_QUALITY_AVAILABLE:
            self._signal_quality_panel = SignalQualityPanel(mode=self._mode)
            mid_tabs.addTab(self._signal_quality_panel, "Signal Quality")
        else:
            self._signal_quality_panel = None

        # v0.3.15 Rule Weight Tuning tab
        if _RULE_WEIGHT_TUNING_AVAILABLE:
            self._rule_weight_panel = RuleWeightTuningPanel(mode=self._mode)
            mid_tabs.addTab(self._rule_weight_panel, "Rule Weight Tuning")
        else:
            self._rule_weight_panel = None

        # v0.3.16 Auto Report Center tab
        if _AUTO_REPORT_CENTER_AVAILABLE:
            self._auto_report_panel = AutoReportCenterPanel(mode=self._mode)
            mid_tabs.addTab(self._auto_report_panel, "Auto Report Center")
        else:
            self._auto_report_panel = None

        # v0.3.17 Automation Scheduler tab
        if _AUTOMATION_SCHEDULER_AVAILABLE:
            self._automation_panel = AutomationSchedulerPanel(mode=self._mode)
            mid_tabs.addTab(self._automation_panel, "Automation Scheduler")
        else:
            self._automation_panel = None

        # v0.3.18 Provider Health tab
        if _PROVIDER_HEALTH_AVAILABLE:
            self._provider_health_panel = ProviderHealthPanel()
            mid_tabs.addTab(self._provider_health_panel, "Provider Health")
        else:
            self._provider_health_panel = None

        # v0.3.19 Data Provider Fetch tab
        if _DATA_PROVIDER_FETCH_AVAILABLE:
            self._data_provider_fetch_panel = DataProviderFetchPanel()
            mid_tabs.addTab(self._data_provider_fetch_panel, "Data Provider Fetch")
        else:
            self._data_provider_fetch_panel = None

        # v0.3.20 Data Quality Gate tab
        if _DATA_QUALITY_GATE_AVAILABLE:
            self._data_quality_gate_panel = DataQualityGatePanel()
            mid_tabs.addTab(self._data_quality_gate_panel, "Data Quality Gate")
        else:
            self._data_quality_gate_panel = None

        # v0.3.21 Daily Workflow tab
        if _DAILY_WORKFLOW_AVAILABLE:
            self._daily_workflow_panel = DailyWorkflowPanel()
            mid_tabs.addTab(self._daily_workflow_panel, "Daily Workflow")
        else:
            self._daily_workflow_panel = None

        # v0.3.22 Usability QA tab
        if _USABILITY_QA_AVAILABLE:
            self._usability_qa_panel = UsabilityQAPanel()
            mid_tabs.addTab(self._usability_qa_panel, "Usability QA")
        else:
            self._usability_qa_panel = None

        # v0.3.24 Provider Reliability tab
        if _PROVIDER_RELIABILITY_AVAILABLE:
            self._provider_reliability_panel = ProviderReliabilityPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._provider_reliability_panel, "Provider Reliability")
        else:
            self._provider_reliability_panel = None

        # v0.3.25 Universe Manager tab
        if _UNIVERSE_MANAGER_AVAILABLE:
            self._universe_manager_panel = UniverseManagerPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._universe_manager_panel, "Universe Manager")
        else:
            self._universe_manager_panel = None

        # v0.3.26 Hardened Backtest tab
        if _HARDENED_BACKTEST_AVAILABLE:
            self._hardened_backtest_panel = HardenedBacktestPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._hardened_backtest_panel, "Hardened Backtest")
        else:
            self._hardened_backtest_panel = None

        # v0.3.27 Intraday Pipeline tab
        if _INTRADAY_PIPELINE_AVAILABLE:
            self._intraday_pipeline_panel = IntradayPipelinePanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._intraday_pipeline_panel, "Intraday Pipeline")
        else:
            self._intraday_pipeline_panel = None

        # v0.3.28 Rule Governance tab
        if _RULE_GOVERNANCE_AVAILABLE:
            self._rule_governance_panel = RuleGovernancePanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._rule_governance_panel, "Rule Governance")
        else:
            self._rule_governance_panel = None

        # v0.3.29 Experiment Registry tab
        if _EXPERIMENT_REGISTRY_AVAILABLE:
            self._experiment_registry_panel = ExperimentRegistryPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._experiment_registry_panel, "Experiment Registry")
        else:
            self._experiment_registry_panel = None

        # v0.4.0 Release Status tab
        if _RELEASE_STATUS_AVAILABLE:
            self._release_status_panel = ReleaseStatusPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._release_status_panel, "Release Status")
        else:
            self._release_status_panel = None

        # v0.4.1 API Fetch Status tab
        if _API_FETCH_STATUS_AVAILABLE:
            self._api_fetch_status_panel = APIFetchStatusPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._api_fetch_status_panel, "API Fetch Status")
        else:
            self._api_fetch_status_panel = None

        # v0.4.2 ML Feature Store tab
        if _ML_FEATURE_STORE_AVAILABLE:
            self._ml_feature_store_panel = MLFeatureStorePanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._ml_feature_store_panel, "ML Feature Store")
        else:
            self._ml_feature_store_panel = None

        # v0.4.3 Model Monitoring tab
        if _MODEL_MONITORING_AVAILABLE:
            self._model_monitoring_panel = ModelMonitoringPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._model_monitoring_panel, "Model Monitoring")
        else:
            self._model_monitoring_panel = None

        # v0.4.4 Intraday Replay tab
        if _INTRADAY_REPLAY_AVAILABLE:
            self._intraday_replay_panel = IntradayReplayPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._intraday_replay_panel, "Intraday Replay")
        else:
            self._intraday_replay_panel = None

        # v0.5.6 Replay Training tab
        if _REPLAY_TRAINING_AVAILABLE:
            self._replay_training_panel = ReplayTrainingPanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._replay_training_panel, "Replay Training")
        else:
            self._replay_training_panel = None

        # v0.6.0 Stable Release tab
        if _STABLE_RELEASE_AVAILABLE:
            self._stable_release_panel = StableReleasePanel(mode=self._mode if hasattr(self, "_mode") else "real")
            mid_tabs.addTab(self._stable_release_panel, "Stable Release")
        else:
            self._stable_release_panel = None

        # v0.6.2 Data Coverage Expansion tab
        if _DATA_COVERAGE_AVAILABLE:
            self._data_coverage_panel = DataCoveragePanel()
            mid_tabs.addTab(self._data_coverage_panel, "Data Coverage")
        else:
            self._data_coverage_panel = None

        # v0.7.0 Research Intelligence tab
        if _RESEARCH_INTELLIGENCE_AVAILABLE:
            self._research_intelligence_panel = ResearchIntelligencePanel()
            mid_tabs.addTab(self._research_intelligence_panel, "Research Intelligence")
        else:
            self._research_intelligence_panel = None

        # v0.7.2 Strategy Research Memory tab
        if _STRATEGY_MEMORY_AVAILABLE:
            self._strategy_memory_panel = StrategyMemoryPanel()
            mid_tabs.addTab(self._strategy_memory_panel, "Strategy Memory")
        else:
            self._strategy_memory_panel = None

        # v0.7.3 Backtest-to-Coach Loop tab
        if _BACKTEST_COACH_AVAILABLE:
            self._backtest_coach_panel = BacktestCoachPanel()
            mid_tabs.addTab(self._backtest_coach_panel, "Backtest Coach")
        else:
            self._backtest_coach_panel = None

        # v0.8.0 Research Intelligence Stable tab
        if _INTELLIGENCE_STABLE_AVAILABLE:
            self._intelligence_stable_panel = IntelligenceStablePanel()
            mid_tabs.addTab(self._intelligence_stable_panel, "Intelligence Stable")
        else:
            self._intelligence_stable_panel = None

        # v0.8.2 Training Metrics tab
        if _TRAINING_METRICS_AVAILABLE:
            self._training_metrics_panel = TrainingMetricsPanel()
            mid_tabs.addTab(self._training_metrics_panel, "Training Metrics")
        else:
            self._training_metrics_panel = None

        # v0.8.3 Evidence Graph tab
        if _EVIDENCE_GRAPH_AVAILABLE:
            self._evidence_graph_panel = EvidenceGraphPanel()
            mid_tabs.addTab(self._evidence_graph_panel, "Evidence Graph")
        else:
            self._evidence_graph_panel = None

        # v0.9.0 Strategy Lab Stable tab
        if _STRATEGY_LAB_AVAILABLE:
            self._strategy_lab_panel = StrategyLabPanel()
            mid_tabs.addTab(self._strategy_lab_panel, "Strategy Lab")
        else:
            self._strategy_lab_panel = None

        # v0.9.0.1 Crash Reversal
        if _CRASH_REVERSAL_AVAILABLE:
            self._crash_reversal_panel = CrashReversalPanel(mode=getattr(self, '_mode', 'real'))
            mid_tabs.addTab(self._crash_reversal_panel, "Crash Reversal")
        else:
            self._crash_reversal_panel = None

        # v0.9.2 Strategy Validation
        if _STRATEGY_VALIDATION_AVAILABLE:
            self.tab_widget.addTab(StrategyValidationPanel(mode=getattr(self, '_mode', 'real')), "Strategy Validation")

        # v0.9.3 Strategy Lab Dashboard
        if _STRATEGY_LAB_DASHBOARD_AVAILABLE:
            self._strategy_lab_dashboard_panel = StrategyLabDashboardPanel(mode=getattr(self, '_mode', 'real'))
            self.tab_widget.addTab(self._strategy_lab_dashboard_panel, "Strategy Lab Dashboard")
        else:
            self._strategy_lab_dashboard_panel = None

        # v1.0.2 Data & Report Hygiene
        if _DATA_REPORT_HYGIENE_AVAILABLE:
            self._data_report_hygiene_panel = DataReportHygienePanel(mode=getattr(self, '_mode', 'real'))
            self.tab_widget.addTab(self._data_report_hygiene_panel, "Data & Report Hygiene")
        else:
            self._data_report_hygiene_panel = None

        # v0.4.1.1 Strategy Knowledge tab
        if _STRATEGY_KNOWLEDGE_INGESTION_AVAILABLE:
            self._strategy_knowledge_panel = StrategyKnowledgeIngestionPanel(
                mode=self._mode if hasattr(self, "_mode") else "real"
            )
            mid_tabs.addTab(self._strategy_knowledge_panel, "Strategy Knowledge")
        else:
            self._strategy_knowledge_panel = None

        # v0.4.2.1 ML Knowledge Integration tab
        if _ML_KNOWLEDGE_INTEGRATION_AVAILABLE:
            self._ml_knowledge_panel = MLKnowledgeIntegrationPanel(
                mode=self._mode if hasattr(self, "_mode") else "real"
            )
            mid_tabs.addTab(self._ml_knowledge_panel, "ML Knowledge Integration")
        else:
            self._ml_knowledge_panel = None

        # v0.4.5 Notification Center tab
        if _NOTIFICATION_CENTER_AVAILABLE:
            self._notification_center_panel = NotificationCenterPanel(
                mode=self._mode if hasattr(self, "_mode") else "real"
            )
            mid_tabs.addTab(self._notification_center_panel, "Notification Center")
        else:
            self._notification_center_panel = None

        # v0.4.6 Portfolio Journal tab
        if _PORTFOLIO_JOURNAL_AVAILABLE:
            self._portfolio_journal_panel = PortfolioJournalPanel(
                mode=self._mode if hasattr(self, "_mode") else "real"
            )
            mid_tabs.addTab(self._portfolio_journal_panel, "Portfolio Journal")
        else:
            self._portfolio_journal_panel = None

        # v0.4.7 Research Review Dashboard tab
        if _RESEARCH_REVIEW_AVAILABLE:
            self._research_review_panel = ResearchReviewDashboardPanel(
                mode=self._mode if hasattr(self, "_mode") else "real"
            )
            mid_tabs.addTab(self._research_review_panel, "Research Review")
        else:
            self._research_review_panel = None

        # v0.4.8 Research Assistant / Coach tab
        if _RESEARCH_COACH_AVAILABLE:
            self._research_assistant_panel = ResearchAssistantPanel()
            mid_tabs.addTab(self._research_assistant_panel, "Research Coach")
        else:
            self._research_assistant_panel = None

        # v0.4.9 Research Workflow Automation tab
        if _RESEARCH_WORKFLOW_AVAILABLE:
            self._research_workflow_panel = ResearchWorkflowPanel()
            mid_tabs.addTab(self._research_workflow_panel, "Research Workflow")
        else:
            self._research_workflow_panel = None

        # v0.5.0 Research OS Planning tab
        if _RESEARCH_OS_PLANNING_AVAILABLE:
            self._research_os_planning_panel = ResearchOSPlanningPanel()
            mid_tabs.addTab(self._research_os_planning_panel, "Research OS Planning")
        else:
            self._research_os_planning_panel = None

        # v0.5.1 CLI UX tab
        if _CLI_UX_AVAILABLE:
            self._cli_ux_panel = CLIUXPanel()
            mid_tabs.addTab(self._cli_ux_panel, "CLI UX")
        else:
            self._cli_ux_panel = None

        # v0.5.2 GUI Navigation tab
        if _GUI_NAVIGATION_AVAILABLE:
            self._gui_navigation_panel = GUINavigationPanel()
            mid_tabs.addTab(self._gui_navigation_panel, "GUI Navigation")
        else:
            self._gui_navigation_panel = None

        # v0.5.3 Regression Suite tab
        if _REGRESSION_SUITE_AVAILABLE:
            self._regression_suite_panel = RegressionSuitePanel()
            mid_tabs.addTab(self._regression_suite_panel, "Regression Suite")
        else:
            self._regression_suite_panel = None

        # v0.5.4 Report Pack tab
        if _REPORT_PACK_AVAILABLE:
            self._report_pack_panel = ReportPackPanel()
            mid_tabs.addTab(self._report_pack_panel, "Report Pack")
        else:
            self._report_pack_panel = None

        # v0.5.5 Data Stabilization tab
        if _DATA_STAB_PANEL_AVAILABLE and DataStabilizationPanel is not None:
            self._data_stabilization_panel = DataStabilizationPanel()
            mid_tabs.addTab(self._data_stabilization_panel, "Data Stabilization")
        else:
            self._data_stabilization_panel = None

        # v0.5.1.1 Strategy Filter tab (inline — no separate panel file)
        if _STRATEGY_FILTER_AVAILABLE and _PYSIDE6_AVAILABLE:
            _sf_widget = QWidget()
            _sf_layout = QVBoxLayout(_sf_widget)
            _sf_label = QLabel(
                "<b>Strategy Filter Pack — Financial Turnaround &amp; Trend Discipline</b><br>"
                "[!] Research Only. Strategy Filter Only. No Real Orders. "
                "Production Trading: BLOCKED.<br>"
                "Use CLI: <code>python main.py strategy-filter --stock 2454 --mode real</code>"
            )
            _sf_label.setWordWrap(True)
            _sf_layout.addWidget(_sf_label)
            _sf_layout.addStretch()
            mid_tabs.addTab(_sf_widget, "Strategy Filter")

        h_split.addWidget(mid_tabs)
        h_split.setStretchFactor(0, 3)
        h_split.setStretchFactor(1, 2)

        root.addWidget(h_split, stretch=5)

        # ---- Bottom: Report | Log tabs ----
        bottom_tabs = QTabWidget()
        bottom_tabs.setMaximumHeight(200)
        bottom_tabs.setStyleSheet(_tab_style)

        if _PHASE5_PANELS:
            self._report_panel = ReportPanel(gui_state=self._gui_state)
            self._report_panel.report_requested.connect(self._on_generate_report)
            bottom_tabs.addTab(self._report_panel, "Report")
        else:
            self._report_panel = None

        self._log_panel = LogPanel()
        bottom_tabs.addTab(self._log_panel, "Log")

        root.addWidget(bottom_tabs, stretch=1)

        # ---- Status bar ----
        sb = QStatusBar()
        sb.showMessage("⚠ 禁止實盤自動下單。本系統僅供研究、模擬交易與決策輔助，不構成投資建議。")
        sb.setStyleSheet("color:#FF8888; background:#1A0A0A")
        self.setStatusBar(sb)

        # ---- Attach log handler ----
        handler = _QLogHandler(self._log_panel)
        handler.setFormatter(logging.Formatter('%(levelname)s | %(name)s | %(message)s'))
        logging.getLogger().addHandler(handler)

        self._log_panel.append(f"TW Quant Cockpit v0.2 啟動 [{mode_label}]")
        self._log_panel.append("⚠ 禁止實盤自動下單")

    # ---- Mode / UI event handlers ----

    def _on_mode_changed(self, new_mode: str):
        self._mode = new_mode
        if self._gui_state:
            self._gui_state.set_mode(new_mode)
        logger.info("Mode switched to: %s", new_mode)
        # Restart worker with new mode
        if self._worker:
            self._worker.stop()
            self._worker.quit()
            self._worker.wait(3000)
            self._worker = None
        self._start_worker()
        # Sync Portfolio Cockpit panel mode
        if self._portfolio_panel is not None:
            self._portfolio_panel.set_mode(new_mode)
        # Sync Signal Quality panel mode
        if self._signal_quality_panel is not None:
            self._signal_quality_panel.set_mode(new_mode)
        # Sync Rule Weight Tuning panel mode
        if self._rule_weight_panel is not None:
            self._rule_weight_panel.set_mode(new_mode)
        # Sync Auto Report Center panel mode
        if self._auto_report_panel is not None:
            self._auto_report_panel.set_mode(new_mode)
        # Sync Automation Scheduler panel mode
        if self._automation_panel is not None:
            self._automation_panel.set_mode(new_mode)

    def _on_candidate_clicked(self, row: int, col: int):
        """Called when user clicks a row in the candidates table."""
        try:
            item = self._candidates_panel._table.item(row, 0)
            if item:
                sym = item.text().strip()
                if sym:
                    self._on_stock_selected(sym)
        except Exception as exc:
            logger.warning("Candidate click error: %s", exc)

    def _on_stock_selected(self, symbol: str):
        """Central handler when a stock is selected."""
        self._selected_symbol = symbol
        if self._gui_state:
            self._gui_state.set_symbol(symbol)

        # Update detail panel
        cand = next(
            (c for c in self._candidates if str(c.get('symbol', '')) == symbol),
            {}
        )
        tick = self._ticks.get(symbol, {})

        if self._detail_panel:
            self._detail_panel.update(cand, tick=tick)

        # Order book
        bidask = tick.get('bidask', {})
        self._ob_panel.update(symbol, bidask)

        # Scores
        self._score_panel.update(symbol, cand)

        # Strategy + data check
        self._update_strategy_for_symbol(symbol, cand)

    def _update_strategy_for_symbol(self, symbol: str, candidate: dict = None):
        """Run data-check and strategy analysis for the selected symbol, update panels."""
        if not _PHASE5_PANELS:
            return
        try:
            mode = self._mode
            data_sources = None

            # Attempt to load real data sources info
            if mode == 'real':
                try:
                    from data.real_data_loader import RealDataLoader
                    loader = RealDataLoader()
                    all_data = loader.load_all(symbol)
                    data_sources = all_data.get('_sources')
                    if self._detail_panel:
                        self._detail_panel.update(
                            candidate or {}, tick=self._ticks.get(symbol, {}),
                            data_sources=data_sources
                        )
                except Exception as exc:
                    logger.warning("RealDataLoader for %s: %s", symbol, exc)

            # Data quality check
            try:
                from data.data_quality_checker import DataQualityChecker
                checker = DataQualityChecker()
                dq_result = checker.check_stock(symbol)
                if self._gui_state:
                    self._gui_state.cache_data_check(symbol, dq_result)
                if self._data_status_panel:
                    self._data_status_panel.update(dq_result)
            except Exception as exc:
                logger.warning("DataQualityChecker for %s: %s", symbol, exc)

            # Strategy analysis
            if self._strategy_panel:
                try:
                    from analysis.strategy_analyzer import StrategyAnalyzer
                    analyzer = StrategyAnalyzer(mode=mode)
                    daytrade = analyzer.analyze(symbol, timeframe='daytrade')
                    short_r  = analyzer.analyze(symbol, timeframe='short')
                    mid_r    = analyzer.analyze(symbol, timeframe='mid')
                    long_r   = analyzer.analyze(symbol, timeframe='long')
                    self._strategy_panel.update(
                        daytrade=daytrade, short=short_r,
                        mid=mid_r, long_=long_r, mode=mode
                    )
                except Exception as exc:
                    logger.warning("StrategyAnalyzer for %s: %s", symbol, exc)
                    self._strategy_panel.clear()

        except Exception as exc:
            logger.error("_update_strategy_for_symbol error: %s", exc)

    def _on_refresh_screener(self):
        """Manual refresh: restart the worker immediately."""
        if self._worker:
            self._worker.stop()
            self._worker.quit()
            self._worker.wait(3000)
            self._worker = None
        self._start_worker()
        self._log_panel.append("手動刷新篩選…")

    def _on_data_check(self):
        """Run data-check for selected symbol and show in DataStatusPanel."""
        sym = self._selected_symbol
        if not sym:
            self._log_panel.append("請先選擇一支股票再執行 Data Check。")
            return
        self._update_strategy_for_symbol(sym, next(
            (c for c in self._candidates if str(c.get('symbol', '')) == sym), {}
        ))
        self._log_panel.append(f"Data Check 完成：{sym}")

    def _on_generate_report(self, symbol: str = None):
        """Generate stock report for the given or currently selected symbol."""
        sym = symbol or self._selected_symbol
        if not sym:
            if self._report_panel:
                self._report_panel.show_status("請先選擇一支股票再產生報告。")
            return
        if self._report_panel:
            self._report_panel.show_status(f"正在產生 {sym} 報告…")
        try:
            import os
            mode = self._mode
            from analysis.stock_report_builder import StockReportBuilder
            builder = StockReportBuilder()

            cand = next(
                (c for c in self._candidates if str(c.get('symbol', '')) == sym), {}
            )
            bull_score_data = {
                'score': cand.get('bull_stock_score'),
                'deduction_reasons': cand.get('deduction_reasons', []),
            }

            data_sources = None
            if mode == 'real':
                try:
                    from data.real_data_loader import RealDataLoader
                    all_data = RealDataLoader().load_all(sym)
                    data_sources = all_data.get('_sources')
                except Exception:
                    pass

            report_text = builder.build(
                symbol=sym,
                name=cand.get('name', sym),
                bull_score_data=bull_score_data,
                mode=mode,
                data_sources=data_sources,
            )

            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(base, 'data', 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            out_path = os.path.join(reports_dir, f"{sym}_report_{ts}.txt")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(report_text)

            if self._report_panel:
                self._report_panel.show_report(report_text, file_path=out_path, symbol=sym)
            if self._gui_state:
                self._gui_state.last_report_path = out_path
            self._log_panel.append(f"報告已產生：{out_path}")

        except Exception as exc:
            msg = f"報告產生失敗：{exc}"
            logger.error(msg)
            if self._report_panel:
                self._report_panel.show_status(msg)

    def _on_import_csv(self):
        """Open the ImportPanel modal dialog."""
        if not _PHASE5_PANELS:
            return
        try:
            dlg = ImportPanel(parent=self)
            dlg.exec()
        except Exception as exc:
            logger.error("ImportPanel error: %s", exc)

    # ---- Worker ----

    def _start_worker(self):
        if not _PYSIDE6_AVAILABLE:
            return

        mode = self._mode

        class _ScreenerWrapper:
            def __init__(self, m):
                self._mode = m

            def run(self):
                try:
                    from screener.screener_pipeline import ScreenerPipeline
                    p = ScreenerPipeline()
                    use_mock = (self._mode != 'real')
                    p.run(mock_data=use_mock)
                    return p.get_top_candidates(n=8)
                except Exception:
                    return []

        class _BrokerWrapper:
            def __init__(self, broker):
                self._b = broker

            def get_market_snapshot(self):
                if self._b and hasattr(self._b, 'get_market_snapshot'):
                    return self._b.get_market_snapshot()
                import random
                return {
                    'taiex': 21500 + random.randint(-200, 200),
                    'taiex_change_pct': random.uniform(-1.5, 1.5),
                    'session': '盤中',
                }

            def get_symbols(self):
                if self._b and hasattr(self._b, 'get_symbols'):
                    return self._b.get_symbols()
                return []

            def get_tick(self, sym):
                if self._b and hasattr(self._b, 'get_tick'):
                    return self._b.get_tick(sym)
                return {}

        class _PaperWrapper:
            def __init__(self, pt):
                self._pt = pt

            def get_positions(self):
                if self._pt and hasattr(self._pt, 'get_positions'):
                    return self._pt.get_positions()
                return []

            def get_pnl_summary(self):
                if self._pt and hasattr(self._pt, 'get_pnl_summary'):
                    return self._pt.get_pnl_summary()
                return {}

        self._worker = DataWorker(
            broker=_BrokerWrapper(self._broker),
            screener_pipeline=_ScreenerWrapper(mode),
            paper_trader=_PaperWrapper(self._paper_trader),
            interval=5,
        )
        self._worker.data_ready.connect(self._on_data)
        self._worker.start()

    def _on_data(self, payload: dict):
        """Called from worker thread with fresh data."""
        try:
            ts = payload.get('timestamp', '')
            market = payload.get('market', {})
            candidates = normalize_records(payload.get('candidates', []))
            ticks = payload.get('ticks', {})
            positions = payload.get('positions', [])
            pnl_summary = payload.get('pnl_summary', {})

            self._candidates = candidates
            self._ticks = ticks

            if self._gui_state:
                self._gui_state.last_candidates = candidates
                self._gui_state.update_refresh_time()

            self._market_bar.update(market, ts)
            self._stock_table.update(ticks, candidates, positions)
            self._candidates_panel.update(candidates)
            self._pos_panel.update(positions, pnl_summary)

            # Update detail panels for selected symbol (or first candidate)
            sym = self._selected_symbol
            if not sym and candidates:
                sym = str(candidates[0].get('symbol', ''))
            if sym:
                cand = next((c for c in candidates if str(c.get('symbol', '')) == sym), {})
                tick = ticks.get(sym, {})
                bidask = tick.get('bidask', {})
                self._ob_panel.update(sym, bidask)
                self._score_panel.update(sym, cand)
                if self._detail_panel:
                    self._detail_panel.update(cand, tick=tick)

            # Refresh ControlPanel status if available
            if self._ctrl_panel:
                try:
                    self._ctrl_panel.set_refresh_time(ts)
                except Exception:
                    pass

        except Exception as exc:
            logger.error("Dashboard update error: %s\n%s", exc, traceback.format_exc())

    def closeEvent(self, event):
        if self._worker:
            self._worker.stop()
            self._worker.quit()
            self._worker.wait(3000)
        if _PYSIDE6_AVAILABLE:
            super().closeEvent(event)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def launch(mode: str = 'mock'):
    """Launch the Cockpit GUI. Called by main.py cockpit command."""
    if not _PYSIDE6_AVAILABLE:
        print("ERROR: PySide6 is required to run the Cockpit GUI.")
        print("Install with: pip install PySide6")
        return

    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#12121E"))
    palette.setColor(QPalette.WindowText, QColor("#DDDDDD"))
    palette.setColor(QPalette.Base, QColor("#0E1520"))
    palette.setColor(QPalette.AlternateBase, QColor("#1A1A2E"))
    palette.setColor(QPalette.Text, QColor("#EEEEEE"))
    palette.setColor(QPalette.Button, QColor("#252540"))
    palette.setColor(QPalette.ButtonText, QColor("#EEEEEE"))
    palette.setColor(QPalette.Highlight, QColor("#3344AA"))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(palette)

    window = CockpitWindow(mode=mode)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    launch()
