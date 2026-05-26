"""
main.py - CLI entry point for the Taiwan Quantitative Trading Platform.

Commands
--------
download      : Download all stock price data from FinMind
features      : Compute technical features for all stocks
train         : Train the ML ensemble model
backtest      : Run a backtest for a given strategy
pipeline      : Run the full daily pipeline (update → features → predict → report)
report        : Generate / display the latest daily report
ui            : Launch the Streamlit dashboard

TW Quant Cockpit v1 commands
------------------------------
screener      : Run 4-layer Taiwan stock screener, output top 3-8 candidates
cockpit       : Launch TW Quant Cockpit GUI (PySide6)
paper         : Show paper trading positions and P&L
stock-report  : Generate multi-timeframe analysis report for a single stock
mock-realtime : Run mock real-time market data simulation (no Shioaji required)

TW Quant Cockpit v0.2 Phase 4 commands
----------------------------------------
import-csv    : Import XQ/Excel/manual CSV into standard data/import/ structure
data-check    : Check data completeness for a stock or the full universe

Usage examples
--------------
    python main.py download
    python main.py features
    python main.py train
    python main.py backtest --strategy momentum
    python main.py backtest --strategy mean_reversion --start 2022-01-01
    python main.py pipeline
    python main.py report
    python main.py ui
    python main.py screener
    python main.py cockpit
    python main.py paper
    python main.py stock-report --stock 2330
    python main.py mock-realtime
"""

import argparse
import logging
import os
import sys
from datetime import date, datetime

# Force UTF-8 output on Windows so Chinese characters display correctly
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ---- Setup path so all sub-packages resolve correctly -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config

# ---- Logging setup -------------------------------------------------------

def _setup_logging(level: str = "INFO") -> None:
    """Configure root logger with a consistent format."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_download(args: argparse.Namespace) -> None:
    """Download stock price data from FinMind."""
    from data.downloader import download_all_stocks
    from data.database import initialize_db

    initialize_db()
    logger = logging.getLogger("main.download")
    logger.info("Starting full data download.")

    stocks = args.stocks if hasattr(args, "stocks") and args.stocks else config.STOCK_UNIVERSE
    start = args.start if hasattr(args, "start") and args.start else config.DEFAULT_START_DATE
    end = args.end if hasattr(args, "end") and args.end else date.today().strftime("%Y-%m-%d")

    logger.info("Stocks: %d | Start: %s | End: %s", len(stocks), start, end)

    rows = download_all_stocks(
        stock_ids=stocks,
        start_date=start,
        end_date=end,
    )
    logger.info("Download complete. %d rows saved.", rows)


def cmd_features(args: argparse.Namespace) -> None:
    """Compute and persist all technical features."""
    from pipeline.daily import compute_all_features

    logger = logging.getLogger("main.features")
    logger.info("Computing features.")

    start = args.start if hasattr(args, "start") and args.start else config.DEFAULT_START_DATE
    end = args.end if hasattr(args, "end") and args.end else date.today().strftime("%Y-%m-%d")

    df = compute_all_features(start_date=start, end_date=end, save_to_db=True)

    if df.empty:
        logger.error("Feature computation returned empty DataFrame. Check that price data exists.")
        sys.exit(1)

    logger.info("Features computed for %d stock-days.", len(df))


def cmd_train(args: argparse.Namespace) -> None:
    """Train the ML ensemble model."""
    from models.trainer import run_training

    logger = logging.getLogger("main.train")
    logger.info("Starting model training.")

    start = args.start if hasattr(args, "start") and args.start else config.DEFAULT_START_DATE
    end = args.end if hasattr(args, "end") and args.end else date.today().strftime("%Y-%m-%d")

    summary = run_training(
        start_date=start,
        end_date=end,
        validate=True,
        save_model=True,
    )

    if summary.get("status") == "failed":
        logger.error("Training failed: %s", summary.get("reason"))
        sys.exit(1)

    logger.info("Training complete. Summary:")
    for k, v in summary.items():
        if k != "metrics":
            logger.info("  %s: %s", k, v)
    if "metrics" in summary:
        logger.info("  Metrics: %s", summary["metrics"])


def cmd_backtest(args: argparse.Namespace) -> None:
    """Run a backtest for the specified strategy."""
    from backtest.engine import BacktestEngine
    from data.database import initialize_db
    from features.indicators import compute_indicators
    from features.volatility import compute_volatility
    from features.momentum import compute_momentum
    from features.regime import detect_regime
    from data.database import load_features, load_prices

    logger = logging.getLogger("main.backtest")
    initialize_db()

    strategy_name = getattr(args, "strategy", "momentum")
    start = getattr(args, "start", None) or config.DEFAULT_START_DATE
    end = getattr(args, "end", None) or date.today().strftime("%Y-%m-%d")
    walk_fwd = getattr(args, "walk_forward", False)

    logger.info("Backtesting strategy: %s | %s → %s", strategy_name, start, end)

    # Load feature data
    feature_df = load_features(start_date=start, end_date=end)

    if feature_df.empty:
        logger.warning("No features in DB. Trying to compute from prices.")
        from pipeline.daily import compute_all_features
        feature_df = compute_all_features(start_date=start, end_date=end, save_to_db=False)

    if feature_df.empty:
        logger.error(
            "No data available. Run 'python main.py download' and "
            "'python main.py features' first."
        )
        sys.exit(1)

    # Build strategy instance
    if strategy_name == "momentum":
        from strategies.momentum import MomentumStrategy
        strategy = MomentumStrategy()
    elif strategy_name == "mean_reversion":
        from strategies.mean_reversion import MeanReversionStrategy
        strategy = MeanReversionStrategy()
    elif strategy_name == "breakout":
        from strategies.breakout import BreakoutStrategy
        strategy = BreakoutStrategy()
    else:
        logger.error("Unknown strategy: %s. Choose: momentum, mean_reversion, breakout", strategy_name)
        sys.exit(1)

    if walk_fwd:
        # Walk-forward validation
        from backtest.walk_forward import run_walk_forward, summarise_walk_forward

        logger.info("Running walk-forward validation.")
        wf_results = run_walk_forward(
            feature_df=feature_df,
            strategy_factory=lambda: type(strategy)(),
        )
        summary_text = summarise_walk_forward(wf_results)
        print(summary_text)
    else:
        # Single backtest
        engine = BacktestEngine(strategy=strategy, initial_capital=config.INITIAL_CAPITAL)
        results = engine.run(feature_df)

        print("\n" + "=" * 55)
        print(f"  Backtest Results: {strategy_name.replace('_', ' ').title()}")
        print("=" * 55)
        for k, v in results.items():
            if k in ("trades", "portfolio_history"):
                continue
            if isinstance(v, float):
                if k in ("total_return", "annualised_return", "max_drawdown", "win_rate"):
                    print(f"  {k:<25}: {v:+.2%}")
                elif k in ("sharpe_ratio", "profit_factor"):
                    print(f"  {k:<25}: {v:.4f}")
                else:
                    print(f"  {k:<25}: {v:.4f}")
            else:
                print(f"  {k:<25}: {v}")

        # KPI check
        kpi_check = engine.meets_kpi_targets(results)
        print("\n  KPI Target Assessment:")
        for kpi, info in kpi_check.items():
            status = "PASS" if info["passed"] else "FAIL"
            print(f"  [{status}] {kpi}: {info['value']:.4f} (target {info['target']})")


def cmd_pipeline(args: argparse.Namespace) -> None:
    """Run the full daily pipeline."""
    from pipeline.daily import run_daily_pipeline

    logger = logging.getLogger("main.pipeline")
    logger.info("Running daily pipeline.")

    target_date = getattr(args, "date", None) or date.today().strftime("%Y-%m-%d")
    update = not getattr(args, "no_update", False)

    result = run_daily_pipeline(target_date=target_date, update_data=update)

    print("\n" + "=" * 55)
    print("  Daily Pipeline Result")
    print("=" * 55)
    print(f"  Date     : {result.get('date')}")
    print(f"  Status   : {result.get('status')}")
    print(f"  Regime   : {result.get('regime')} / {result.get('vol_regime')}")
    print(f"  Strategy : {result.get('selected_strategy')}")

    picks = result.get("picks", None)
    if picks is not None and not picks.empty:
        print(f"\n  Top {min(10, len(picks))} Picks:")
        print(f"  {'StockID':>10} {'Score':>8} {'PredRet':>10} {'UpProb':>7}")
        for _, row in picks.head(10).iterrows():
            sid = row.get("stock_id", "N/A")
            score = row.get("composite_score", float("nan"))
            pred_ret = row.get("predicted_return", float("nan"))
            up_prob = row.get("up_probability", float("nan"))
            score_s = f"{score:.4f}" if not pd.isna(score) else "   N/A"
            ret_s = f"{pred_ret:+.2%}" if not pd.isna(pred_ret) else "    N/A"
            prob_s = f"{up_prob:.1%}" if not pd.isna(up_prob) else "  N/A"
            print(f"  {sid:>10} {score_s:>8} {ret_s:>10} {prob_s:>7}")

    if result.get("errors"):
        print(f"\n  Errors: {result['errors']}")

    # Print report to console
    report = result.get("report")
    if report:
        print("\n" + report)


def cmd_report(args: argparse.Namespace) -> None:
    """Display the latest saved report."""
    from data.database import load_report, list_report_dates, initialize_db

    initialize_db()
    logger = logging.getLogger("main.report")

    target_date = getattr(args, "date", None)
    if not target_date:
        dates = list_report_dates()
        if not dates:
            logger.error("No reports found. Run 'python main.py pipeline' first.")
            sys.exit(1)
        target_date = dates[0]
        logger.info("Loading latest report for %s.", target_date)

    text = load_report(target_date)
    if text:
        print(text)
    else:
        logger.error("No report found for date %s.", target_date)

        # Try to generate one on the fly
        from reports.generator import generate_daily_report
        from data.database import load_predictions, save_report

        preds = load_predictions(date=target_date)
        report = generate_daily_report(
            date=target_date,
            regime="unknown",
            vol_regime="low",
            strategy_name="momentum",
            picks=preds,
        )
        print(report)
        save_report(target_date, report)


def cmd_ui(_args: argparse.Namespace) -> None:
    """Launch the Streamlit dashboard."""
    import subprocess

    dashboard_path = os.path.join(BASE_DIR, "ui", "dashboard.py")
    logger = logging.getLogger("main.ui")
    logger.info("Launching Streamlit dashboard at %s.", dashboard_path)

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", dashboard_path],
        check=True,
    )


# ---------------------------------------------------------------------------
# TW Quant Cockpit v1 command handlers
# ---------------------------------------------------------------------------

def cmd_screener(args: argparse.Namespace) -> None:
    """Run the 4-layer Taiwan stock screener and print top candidates."""
    from screener.screener_pipeline import ScreenerPipeline

    logger = logging.getLogger("main.screener")
    mode = getattr(args, 'mode', 'mock')
    logger.info("Running Taiwan stock screener... [mode=%s]", mode)

    top_n = getattr(args, "top", 8)
    pipeline = ScreenerPipeline()
    pipeline.run(mode=mode)
    result = pipeline.get_top_candidates(n=top_n)

    # get_top_candidates may return a DataFrame or a list of dicts
    import pandas as pd
    if isinstance(result, pd.DataFrame):
        if result.empty:
            candidates = []
        else:
            candidates = result.to_dict(orient='records')
    else:
        candidates = list(result) if result is not None else []

    if not candidates:
        print("No candidates found. Check theme pool CSV files in config/theme_pools/")
        return

    mode_label = '🟡 MOCK' if mode == 'mock' else '🟢 REAL'
    print("\n" + "=" * 70)
    print(f"  TW Quant Cockpit v1 — 飆股候選篩選結果 (Top {len(candidates)}) [{mode_label}]")
    print("=" * 70)
    print(f"  {'代號':>6}  {'名稱':<8}  {'分數':>6}  {'主題':<20}  建議")
    print("-" * 70)

    for c in candidates:
        sym    = str(c.get('symbol', ''))
        name   = str(c.get('name', ''))
        score  = float(c.get('bull_stock_score', 0))
        themes_raw = c.get('theme_tags', [])
        if isinstance(themes_raw, str):
            themes = themes_raw
        elif themes_raw:
            themes = ','.join(themes_raw)
        else:
            themes = '-'
        decision = str(c.get('decision', '-'))
        print(f"  {sym:>6}  {name:<8}  {score:>6.1f}  {themes:<20}  {decision}")

    print("=" * 70)
    print("\n[Score] 80+ Bull candidate | 65-79 Strong watch | 50-64 Wait | <50 Avoid")
    print("[!] For research and simulation only. Not investment advice.")


def cmd_cockpit(args: argparse.Namespace) -> None:
    """Launch the TW Quant Cockpit PySide6 GUI."""
    logger = logging.getLogger("main.cockpit")
    mode = getattr(args, 'mode', 'mock')
    logger.info("Launching TW Quant Cockpit GUI [mode=%s]...", mode)

    try:
        from gui.dashboard import launch
        launch(mode=mode)
    except ImportError as exc:
        logger.error("Failed to import gui.dashboard: %s", exc)
        print("ERROR: PySide6 may not be installed. Run: pip install PySide6")
        sys.exit(1)


def cmd_paper(args: argparse.Namespace) -> None:
    """Show paper trading positions and performance summary."""
    logger = logging.getLogger("main.paper")
    logger.info("Paper trading summary.")

    try:
        from sim.simulator import PaperTrader
        trader = PaperTrader(initial_capital=1_000_000)

        # Try to load persisted state if available
        state_path = os.path.join(BASE_DIR, "data", "paper_state.json")
        if os.path.isfile(state_path):
            try:
                import json
                with open(state_path) as f:
                    state = json.load(f)
                logger.info("Loaded paper state from %s", state_path)
            except Exception as exc:
                logger.warning("Could not load paper state: %s", exc)
                state = {}
        else:
            logger.info("No saved paper state found at %s — showing empty portfolio.", state_path)
            state = {}

        print("\n" + "=" * 60)
        print("  TW Quant Cockpit v1 — 模擬持倉 & 績效")
        print("=" * 60)
        print("  初始資金: NTD 1,000,000")

        positions = []
        if hasattr(trader, 'get_positions'):
            positions = trader.get_positions()

        if not positions:
            print("  目前無持倉。使用 `python main.py cockpit` 開啟 GUI 操作模擬單。")
        else:
            print(f"\n  {'代號':>6}  {'均成本':>8}  {'持倉':>6}  {'浮動損益':>10}")
            print("-" * 45)
            for p in positions:
                sym   = str(p.get('symbol', ''))
                cost  = float(p.get('avg_cost', 0))
                qty   = int(p.get('quantity', 0))
                upnl  = float(p.get('unrealized_pnl', 0))
                print(f"  {sym:>6}  {cost:>8.1f}  {qty:>6}  {upnl:>+10,.0f}")

        pnl = {}
        if hasattr(trader, 'get_pnl_summary'):
            pnl = trader.get_pnl_summary()

        total_pnl = pnl.get('realized_pnl', 0) + pnl.get('unrealized_pnl', 0)
        print(f"\n  已實現損益: NTD {pnl.get('realized_pnl', 0):+,.0f}")
        print(f"  未實現損益: NTD {pnl.get('unrealized_pnl', 0):+,.0f}")
        print(f"  合計損益:   NTD {total_pnl:+,.0f}")
        print("=" * 60)
        print("[!] v1: No real order execution. For research and simulation only.")

    except Exception as exc:
        logger.error("Paper trading command failed: %s", exc)
        print(f"ERROR: {exc}")
        sys.exit(1)


def cmd_stock_report(args: argparse.Namespace) -> None:
    """Generate a multi-timeframe analysis report for a single stock."""
    from analysis.stock_report_builder import StockReportBuilder

    logger = logging.getLogger("main.stock_report")

    stock = getattr(args, 'stock', None)
    if not stock:
        logger.error("--stock is required. Example: python main.py stock-report --stock 2330")
        sys.exit(1)

    mode = getattr(args, 'mode', 'mock')
    logger.info("Building stock report for: %s [mode=%s]", stock, mode)

    try:
        sym = str(stock)

        # Load all real data via RealDataLoader (real mode) or DataSourceRouter (mock mode)
        from data.data_source_router import DataSourceRouter
        router = DataSourceRouter(mode=mode)

        stock_name = None
        price_data = None
        chip_data = None
        fundamental_data = None
        data_sources = None

        if mode == 'real':
            from data.real_data_loader import RealDataLoader
            loader = RealDataLoader()
            all_data = loader.load_all(sym)
            data_sources = all_data.get('_sources')
            profile = all_data.get('profile')
            if profile:
                stock_name = profile.get('name')
            _dk = all_data.get('daily_k')               # dict with 'bars' key, or None
            price_data = _dk.get('bars') if _dk else None
            chip_data = all_data.get('institutional')   # dict or None
            fundamental_data = all_data.get('monthly_revenue')  # dict or None
            logger.info("Real data loaded for %s: price=%s bars, chip=%s, fundamental=%s",
                        sym,
                        len(price_data) if price_data else 0,
                        'yes' if chip_data else 'no',
                        'yes' if fundamental_data else 'no')
        else:
            price_data = router.get_price_data(sym, n_bars=60)
            chip_data = router.get_chip_data(sym)

        # Resolve stock name: profile CSV → _STOCK_NAMES fallback
        if not stock_name:
            from screener.screener_pipeline import _STOCK_NAMES
            stock_name = _STOCK_NAMES.get(sym, sym)

        from analysis.daytrade_analyzer import DaytradeAnalyzer
        from analysis.short_term_analyzer import ShortTermAnalyzer
        from analysis.mid_term_analyzer import MidTermAnalyzer
        from analysis.long_term_analyzer import LongTermAnalyzer

        daytrade_result = None
        short_result = None
        mid_result = None
        long_result = None

        try:
            daytrade_result = DaytradeAnalyzer().analyze(
                symbol=sym, price_data=price_data, mode=mode)
        except Exception as exc:
            logger.warning("DaytradeAnalyzer failed: %s", exc)

        try:
            short_result = ShortTermAnalyzer().analyze(
                symbol=sym, price_data=price_data, chip_data=chip_data, mode=mode)
        except Exception as exc:
            logger.warning("ShortTermAnalyzer failed: %s", exc)

        try:
            mid_result = MidTermAnalyzer().analyze(
                symbol=sym, price_data=price_data, chip_data=chip_data,
                fundamental_data=fundamental_data, mode=mode)
        except Exception as exc:
            logger.warning("MidTermAnalyzer failed: %s", exc)

        try:
            long_result = LongTermAnalyzer().analyze(
                symbol=sym, price_data=price_data,
                fundamental_data=fundamental_data, mode=mode)
        except Exception as exc:
            logger.warning("LongTermAnalyzer failed: %s", exc)

        builder = StockReportBuilder()
        report = builder.build(
            symbol=sym,
            name=stock_name,
            mode=mode,
            daytrade_result=daytrade_result,
            short_result=short_result,
            mid_result=mid_result,
            long_result=long_result,
            data_sources=data_sources,
        )

        # Print to console
        print(report)

        # Optionally save to file
        out_dir = os.path.join(BASE_DIR, "data", "reports")
        os.makedirs(out_dir, exist_ok=True)
        from datetime import date as _date
        filename = f"report_{stock}_{_date.today()}.md"
        out_path = os.path.join(out_dir, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info("Report saved to: %s", out_path)
        print(f"\n[報告已儲存至 {out_path}]")

    except Exception as exc:
        logger.error("stock-report failed: %s", exc)
        print(f"ERROR: {exc}")
        sys.exit(1)


def cmd_import_csv(args: argparse.Namespace) -> None:
    """Import a CSV file into the standard data/import/ structure."""
    from data.csv_importer import CSVImporter

    logger = logging.getLogger("main.import_csv")

    data_type = getattr(args, 'type', None)
    file_path = getattr(args, 'file', None)
    replace = getattr(args, 'replace', False)

    if not data_type:
        logger.error("--type is required.")
        sys.exit(1)
    if not file_path:
        logger.error("--file is required.")
        sys.exit(1)

    append = not replace
    importer = CSVImporter()
    result = importer.import_csv(data_type=data_type, file_path=file_path, append=append)

    print("\n" + "=" * 55)
    print("  TW Quant Cockpit — CSV 匯入")
    print("=" * 55)
    print(f"  匯入類型：{result['data_type']}")
    print(f"  輸入檔案：{result['input_file']}")
    print(f"  輸出檔案：{result['output_file']}")
    print(f"  匯入筆數：{result['rows_imported']}")
    print(f"  總筆數：  {result['rows_total']}")
    missing = result.get('missing_columns', [])
    print(f"  缺少欄位：{missing if missing else '無'}")
    warnings = result.get('warnings', [])
    if warnings:
        for w in warnings:
            print(f"  警告：{w}")
    else:
        print("  警告：無")
    status = "✅ 成功" if result['success'] else "❌ 失敗"
    print(f"  狀態：{status}")
    print("=" * 55)

    if not result['success']:
        sys.exit(1)


def cmd_data_check(args: argparse.Namespace) -> None:
    """Check data completeness for a stock or the entire universe."""
    from data.data_quality_checker import DataQualityChecker

    logger = logging.getLogger("main.data_check")

    stock = getattr(args, 'stock', None)
    check_all = getattr(args, 'all', False)

    checker = DataQualityChecker()

    if stock:
        result = checker.check_stock(str(stock))

        print("\n" + "=" * 55)
        print("  TW Quant Cockpit Data Check")
        print("=" * 55)
        print(f"\n  股票：{result['symbol']} {result['name']}\n")

        def _ok(val, threshold):
            return "OK" if val >= threshold else f"不足（需 {threshold} 筆）"

        profile_status = "OK" if result['profile_ok'] else "缺少"
        print(f"  Profile:          {profile_status}")
        print(f"  Daily K:          {result['daily_rows']} rows  {_ok(result['daily_rows'], 20)}")
        print(f"  Institutional:    {result['institutional_rows']} rows  {_ok(result['institutional_rows'], 5)}")
        print(f"  Margin:           {result['margin_rows']} rows  {_ok(result['margin_rows'], 5)}")
        print(f"  Monthly Revenue:  {result['monthly_revenue_rows']} rows  {_ok(result['monthly_revenue_rows'], 6)}")
        print(f"  Holder:           {result['holder_rows']} rows  {_ok(result['holder_rows'], 2)}")
        print(f"  Trust Cost:       {result['trust_cost_rows']} rows  {_ok(result['trust_cost_rows'], 3)}")

        print("\n  正式判斷允許：")
        dt_note = "否，缺 intraday / bidask" if not result['daytrade_allowed'] else "是"
        print(f"  當沖：{dt_note}")
        print(f"  短線：{'是' if result['short_allowed'] else '否'}")
        print(f"  中線：{'是' if result['mid_allowed'] else '否'}")
        print(f"  長線：{'是' if result['long_allowed'] else '否'}")

        missing = [m for m in result['missing'] if m not in ('intraday', 'bidask')]
        if missing:
            print("\n  缺失資料：")
            for m in missing:
                print(f"  - {m}")

        recs = result.get('recommendations', [])
        if recs:
            print("\n  建議：")
            for r in recs:
                print(f"  - {r}")

        print("=" * 55)

    elif check_all:
        logger.info("Checking full universe...")
        df = checker.check_universe()

        if df is None or (hasattr(df, 'empty') and df.empty):
            print("No stocks found in profile CSV. Run import-csv --type profile first.")
            return

        print("\n" + "=" * 90)
        print("  TW Quant Cockpit Data Check — Universe")
        print("=" * 90)
        print(f"  {'代號':>6}  {'名稱':<8}  {'日K':>5}  {'法人':>5}  {'融資':>5}  "
              f"{'月收':>5}  {'大戶':>5}  {'投信成':>6}  短 中 長")
        print("  " + "-" * 80)

        for _, row in df.iterrows():
            sym = str(row.get('symbol', ''))
            name = str(row.get('name', ''))[:8]
            daily = int(row.get('daily_rows', 0))
            inst = int(row.get('institutional_rows', 0))
            margin = int(row.get('margin_rows', 0))
            rev = int(row.get('monthly_revenue_rows', 0))
            holder = int(row.get('holder_rows', 0))
            tc = int(row.get('trust_cost_rows', 0))
            s = '✓' if row.get('short_allowed') else '✗'
            m = '✓' if row.get('mid_allowed') else '✗'
            l = '✓' if row.get('long_allowed') else '✗'
            print(f"  {sym:>6}  {name:<8}  {daily:>5}  {inst:>5}  {margin:>5}  "
                  f"{rev:>5}  {holder:>5}  {tc:>6}  {s} {m} {l}")

        print("=" * 90)
        print(f"  共 {len(df)} 檔 | ✓=正式判斷允許 ✗=資料不足")
        print("=" * 90)

    else:
        print("請指定 --stock <代號> 或 --all")
        sys.exit(1)


def cmd_mock_realtime(args: argparse.Namespace) -> None:
    """Run mock real-time market data simulation (no Shioaji account required)."""
    import time

    logger = logging.getLogger("main.mock_realtime")

    try:
        from broker.mock_broker import MockBroker

        wl = os.path.join(BASE_DIR, "config", "watchlist.csv")
        broker = MockBroker(watchlist_path=wl)

        symbols = broker._symbols[:10]   # cap at 10 for console demo
        duration = getattr(args, 'duration', 60)
        interval = getattr(args, 'interval', 2)

        print("\n" + "=" * 70)
        print("  TW Quant Cockpit v1 — Mock Realtime 模擬行情 (無需 Shioaji)")
        print(f"  監控 {len(symbols)} 檔 | 更新間隔 {interval}s | 執行 {duration}s | Ctrl+C 停止")
        print("=" * 70)

        start_time = time.time()
        tick_num = 0

        while time.time() - start_time < duration:
            tick_num += 1
            elapsed = time.time() - start_time
            remaining = duration - elapsed

            print(f"\n  --- 更新 #{tick_num}  {datetime.now().strftime('%H:%M:%S')}  "
                  f"(剩餘 {remaining:.0f}s) ---")
            print(f"  {'代號':>6}  {'名稱':<8}  {'價格':>8}  {'漲跌%':>8}  "
                  f"{'委買1':>8}  {'委賣1':>8}  {'成交量':>10}")
            print("  " + "-" * 65)

            for sym in symbols:
                try:
                    snap = broker.get_snapshot(sym)
                    name  = snap.get('name', sym)
                    price = snap.get('price', 0)
                    chg   = snap.get('change_pct', 0)
                    bid1  = snap.get('bid_1', snap.get('bid_price_1', 0))
                    ask1  = snap.get('ask_1', snap.get('ask_price_1', 0))
                    vol   = snap.get('volume', 0)
                    arrow = '▲' if chg > 0 else ('▼' if chg < 0 else ' ')
                    print(f"  {sym:>6}  {name:<8}  {price:>8.1f}  "
                          f"{arrow}{abs(chg):>6.2f}%  {bid1:>8.1f}  {ask1:>8.1f}  {vol:>10,}")
                except Exception as exc:
                    logger.debug("Snapshot error for %s: %s", sym, exc)

            try:
                time.sleep(interval)
            except KeyboardInterrupt:
                break

        print("\n[Mock Realtime 結束]")
        print("[!] For research and simulation only. Not investment advice.")

    except Exception as exc:
        logger.error("mock-realtime failed: %s", exc)
        print(f"ERROR: {exc}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Taiwan Quantitative Trading Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- download ---
    p_dl = subparsers.add_parser("download", help="Download stock price data from FinMind")
    p_dl.add_argument("--start", default=None, help="Start date YYYY-MM-DD")
    p_dl.add_argument("--end", default=None, help="End date YYYY-MM-DD")

    # --- features ---
    p_feat = subparsers.add_parser("features", help="Compute and store technical features")
    p_feat.add_argument("--start", default=None, help="Start date YYYY-MM-DD")
    p_feat.add_argument("--end", default=None, help="End date YYYY-MM-DD")

    # --- train ---
    p_train = subparsers.add_parser("train", help="Train the ML ensemble model")
    p_train.add_argument("--start", default=None, help="Start date for training data")
    p_train.add_argument("--end", default=None, help="End date for training data")

    # --- backtest ---
    p_bt = subparsers.add_parser("backtest", help="Run a backtest")
    p_bt.add_argument(
        "--strategy",
        default="momentum",
        choices=["momentum", "mean_reversion", "breakout"],
        help="Strategy to backtest (default: momentum)",
    )
    p_bt.add_argument("--start", default=None, help="Start date YYYY-MM-DD")
    p_bt.add_argument("--end", default=None, help="End date YYYY-MM-DD")
    p_bt.add_argument(
        "--walk-forward",
        action="store_true",
        help="Run walk-forward validation instead of a single backtest",
    )

    # --- pipeline ---
    p_pipe = subparsers.add_parser("pipeline", help="Run the full daily pipeline")
    p_pipe.add_argument("--date", default=None, help="Target date YYYY-MM-DD (default: today)")
    p_pipe.add_argument(
        "--no-update",
        action="store_true",
        help="Skip the data update step",
    )

    # --- report ---
    p_rep = subparsers.add_parser("report", help="Display the daily report")
    p_rep.add_argument("--date", default=None, help="Report date YYYY-MM-DD (default: latest)")

    # --- ui ---
    subparsers.add_parser("ui", help="Launch the Streamlit dashboard")

    # ---- TW Quant Cockpit v1 commands ----

    # --- screener ---
    p_scr = subparsers.add_parser("screener", help="Run Taiwan stock screener (4-layer)")
    p_scr.add_argument("--top", type=int, default=8, help="Max candidates to output (default: 8)")
    p_scr.add_argument("--mode", default="mock", choices=["mock", "real"],
                       help="Data mode: mock (demo) or real (DB/FinMind). Default: mock")

    # --- cockpit ---
    p_cockpit = subparsers.add_parser("cockpit", help="Launch TW Quant Cockpit GUI (PySide6)")
    p_cockpit.add_argument("--mode", default="mock", choices=["mock", "real"],
                           help="Data mode: mock (demo) or real (CSV). Default: mock")

    # --- paper ---
    subparsers.add_parser("paper", help="Show paper trading positions and P&L")

    # --- stock-report ---
    p_sr = subparsers.add_parser("stock-report", help="Generate multi-timeframe analysis report")
    p_sr.add_argument("--stock", required=True, help="Stock symbol, e.g. 2330")
    p_sr.add_argument("--mode", default="mock", choices=["mock", "real"],
                      help="Data mode: mock (demo) or real (DB/FinMind). Default: mock")

    # --- mock-realtime ---
    p_mr = subparsers.add_parser("mock-realtime", help="Run mock real-time market data simulation")
    p_mr.add_argument("--duration", type=int, default=60, help="Simulation duration in seconds (default: 60)")
    p_mr.add_argument("--interval", type=int, default=2, help="Tick interval in seconds (default: 2)")

    # --- import-csv ---
    p_ic = subparsers.add_parser(
        "import-csv",
        help="Import XQ/Excel/manual CSV into standard data/import/ structure",
    )
    p_ic.add_argument(
        "--type", required=True,
        choices=["profile", "daily", "institutional", "margin",
                 "monthly_revenue", "holder", "trust_cost"],
        help="Data type to import",
    )
    p_ic.add_argument("--file", required=True, help="Path to input CSV file")
    p_ic.add_argument(
        "--replace", action="store_true",
        help="Replace existing standard CSV (default: append and deduplicate)",
    )

    # --- data-check ---
    p_dc = subparsers.add_parser(
        "data-check",
        help="Check data completeness for a stock or the full universe",
    )
    grp = p_dc.add_mutually_exclusive_group(required=True)
    grp.add_argument("--stock", default=None, help="Stock symbol, e.g. 2383")
    grp.add_argument("--all", action="store_true", help="Check all stocks in profile universe")

    return parser


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    """Main entrypoint."""
    import pandas as pd  # imported here to avoid shadowing at module level

    # Make pd available in cmd_pipeline (used in the print loop)
    globals()["pd"] = pd

    parser = _build_parser()
    args = parser.parse_args()

    _setup_logging(getattr(args, "log_level", "INFO"))

    command_map = {
        "download": cmd_download,
        "features": cmd_features,
        "train": cmd_train,
        "backtest": cmd_backtest,
        "pipeline": cmd_pipeline,
        "report": cmd_report,
        "ui": cmd_ui,
        # TW Quant Cockpit v1
        "screener":     cmd_screener,
        "cockpit":      cmd_cockpit,
        "paper":        cmd_paper,
        "stock-report": cmd_stock_report,
        "mock-realtime": cmd_mock_realtime,
        # TW Quant Cockpit v0.2 Phase 4
        "import-csv":   cmd_import_csv,
        "data-check":   cmd_data_check,
    }

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    handler = command_map.get(args.command)
    if handler is None:
        parser.print_help()
        sys.exit(1)

    handler(args)


if __name__ == "__main__":
    main()
