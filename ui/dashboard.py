"""
ui/dashboard.py - Streamlit dashboard for the Taiwan Quant Trading Platform.

Pages
-----
1. Daily Picks  – Table of today's recommended stocks with scores.
2. Backtest     – Run a backtest and display equity curve + KPI metrics.
3. Strategy Performance – Compare strategies side-by-side.

Run with:
    streamlit run ui/dashboard.py
or via the CLI:
    python main.py ui
"""

import os
import sys
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

# Ensure the project root is in sys.path regardless of cwd
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st

import config
from data.database import (
    initialize_db,
    load_prices,
    load_features,
    load_predictions,
    load_report,
    list_report_dates,
)
from reports.generator import generate_daily_report


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Taiwan Quant Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

st.sidebar.title("Taiwan Quant Platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Daily Picks", "Volume Profile", "Opening Strength", "Backtest", "Strategy Performance"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption(f"DB: `{os.path.basename(config.DB_PATH)}`")
st.sidebar.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')}")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

@st.cache_data(ttl=300)
def _load_predictions_cached(target_date: str) -> pd.DataFrame:
    """Load predictions for a given date with caching."""
    initialize_db()
    return load_predictions(date=target_date)


@st.cache_data(ttl=300)
def _load_features_cached(target_date: str) -> pd.DataFrame:
    """Load feature snapshot for a given date with caching."""
    initialize_db()
    df = load_features(start_date=target_date, end_date=target_date)
    return df


@st.cache_data(ttl=600)
def _load_price_history(stock_id: str, days: int = 252) -> pd.DataFrame:
    """Load recent price history for a stock."""
    start = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    return load_prices(stock_ids=[stock_id], start_date=start)


def _kpi_card(label: str, value: str, delta: str = "", good_color: bool = True):
    """Render a KPI metric card."""
    st.metric(label=label, value=value, delta=delta)


def _regime_badge(regime: str) -> str:
    """Return a coloured emoji badge for the regime."""
    badges = {"bull": "🟢 BULL", "bear": "🔴 BEAR", "sideways": "🟡 SIDEWAYS"}
    return badges.get(regime.lower(), f"⚪ {regime.upper()}")


# ---------------------------------------------------------------------------
# Page: Daily Picks
# ---------------------------------------------------------------------------

def page_daily_picks():
    """Render the Daily Picks page."""
    st.title("📋 Daily Stock Picks")

    # Date selector
    col1, col2 = st.columns([2, 4])
    with col1:
        report_dates = list_report_dates()
        if report_dates:
            selected_date = st.selectbox("Select date", report_dates, index=0)
        else:
            selected_date = date.today().strftime("%Y-%m-%d")
            st.info("No reports in database yet. Run `python main.py pipeline` to generate picks.")

    with col2:
        st.markdown(f"**Selected Date:** {selected_date}")

    st.markdown("---")

    # Load data
    preds = _load_predictions_cached(selected_date)
    features = _load_features_cached(selected_date)

    # Merge predictions with feature data
    if not preds.empty and not features.empty:
        merged = pd.merge(
            features[
                [c for c in features.columns if c in [
                    "stock_id", "date", "close", "rsi_14", "momentum_score",
                    "regime", "vol_regime", "atr_pct", "bb_position",
                    "ret_1d", "ret_5d", "ret_20d",
                    "vol_short", "predicted_return", "up_probability",
                ]]
            ],
            preds[["stock_id", "predicted_return", "up_probability", "predicted_volatility"]],
            on="stock_id",
            how="inner",
            suffixes=("", "_pred"),
        )

        # Use prediction columns where available
        for col in ["predicted_return", "up_probability", "predicted_volatility"]:
            pred_col = col + "_pred"
            if pred_col in merged.columns:
                merged[col] = merged[pred_col].fillna(merged.get(col, pd.Series(dtype=float)))
                merged.drop(columns=[pred_col], inplace=True, errors="ignore")
    elif not preds.empty:
        merged = preds.copy()
    elif not features.empty:
        merged = features.copy()
        merged["predicted_return"] = merged.get("momentum_score", 0)
        merged["up_probability"] = 0.5
    else:
        merged = pd.DataFrame()

    if merged.empty:
        st.warning("No data available for this date. Check that data has been downloaded and features computed.")
        return

    # Compute composite score
    score = pd.Series(0.0, index=merged.index)
    if "predicted_return" in merged.columns:
        score += 0.4 * merged["predicted_return"].fillna(0)
    if "up_probability" in merged.columns:
        score += 0.3 * (merged["up_probability"].fillna(0.5) - 0.5)
    if "momentum_score" in merged.columns:
        score += 0.3 * merged["momentum_score"].fillna(0)
    merged["composite_score"] = score
    merged = merged.sort_values("composite_score", ascending=False)

    # ---- Regime KPI cards -----------------------------------------------
    regime_val = merged["regime"].mode()[0] if "regime" in merged.columns else "unknown"
    vol_regime_val = merged["vol_regime"].mode()[0] if "vol_regime" in merged.columns else "low"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Market Regime", _regime_badge(regime_val))
    with c2:
        st.metric("Volatility Regime", vol_regime_val.upper())
    with c3:
        avg_up_prob = merged["up_probability"].mean() if "up_probability" in merged.columns else float("nan")
        st.metric("Avg Up Probability", f"{avg_up_prob:.1%}" if not np.isnan(avg_up_prob) else "N/A")
    with c4:
        n_bullish = (merged.get("regime", pd.Series(dtype=str)) == "bull").sum()
        st.metric("Bullish Stocks", f"{n_bullish} / {len(merged)}")

    st.markdown("---")

    # ---- Hot stocks / Today's top movers --------------------------------
    st.subheader("Today's Hot Stocks (熱門標的)")
    if not merged.empty:
        hot_cols = [c for c in ["stock_id", "composite_score", "predicted_return",
                                "up_probability", "close", "volume_spike",
                                "microstructure_score", "ret_1d"] if c in merged.columns]
        hot_df = merged.head(10)[hot_cols].copy()
        rename_map = {
            "stock_id": "Stock", "composite_score": "Score",
            "predicted_return": "Pred Ret", "up_probability": "Up Prob",
            "close": "Close", "volume_spike": "Vol Spike",
            "microstructure_score": "MS Score", "ret_1d": "1d Ret",
        }
        hot_df.rename(columns={k: v for k, v in rename_map.items() if k in hot_df.columns}, inplace=True)
        for col in ["Pred Ret", "1d Ret"]:
            if col in hot_df.columns:
                hot_df[col] = hot_df[col].apply(lambda x: f"{x:+.2%}" if pd.notna(x) else "N/A")
        for col in ["Up Prob"]:
            if col in hot_df.columns:
                hot_df[col] = hot_df[col].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
        for col in ["Score", "MS Score", "Vol Spike"]:
            if col in hot_df.columns:
                hot_df[col] = hot_df[col].apply(lambda x: f"{x:.3f}" if pd.notna(x) else "N/A")
        st.dataframe(hot_df, use_container_width=True, height=320)
    st.markdown("---")

    # ---- Top picks table ------------------------------------------------
    st.subheader("Top 15 Recommended Stocks")

    display_cols = {
        "stock_id": "Stock ID",
        "composite_score": "Score",
        "predicted_return": "Pred Return",
        "up_probability": "Up Prob",
        "close": "Close Price",
        "rsi_14": "RSI(14)",
        "momentum_score": "Momentum",
        "regime": "Regime",
        "microstructure_score": "MS Score",
        "no_chase_reason": "No-Chase Warning",
        "fake_breakout_risk": "Fake BK Risk",
    }
    avail_cols = [c for c in display_cols if c in merged.columns]
    top15 = merged.head(15)[avail_cols].copy()
    top15.columns = [display_cols[c] for c in avail_cols]

    # Format numeric columns
    if "Pred Return" in top15.columns:
        top15["Pred Return"] = top15["Pred Return"].apply(
            lambda x: f"{x:+.2%}" if pd.notna(x) else "N/A"
        )
    if "Up Prob" in top15.columns:
        top15["Up Prob"] = top15["Up Prob"].apply(
            lambda x: f"{x:.1%}" if pd.notna(x) else "N/A"
        )
    if "Score" in top15.columns:
        top15["Score"] = top15["Score"].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "N/A")
    if "RSI(14)" in top15.columns:
        top15["RSI(14)"] = top15["RSI(14)"].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
    if "Close Price" in top15.columns:
        top15["Close Price"] = top15["Close Price"].apply(
            lambda x: f"{x:.2f}" if pd.notna(x) else "N/A"
        )

    st.dataframe(top15, use_container_width=True, height=500)

    # ---- Report text -----------------------------------------------------
    with st.expander("View Full Text Report"):
        report_text = load_report(selected_date)
        if report_text:
            st.text(report_text)
        else:
            st.info("No text report saved for this date.")


# ---------------------------------------------------------------------------
# Page: Volume Profile
# ---------------------------------------------------------------------------

def page_volume_profile():
    """Render the Volume Profile (分價量) support/resistance page."""
    st.title("📊 Volume Profile – Support & Pressure (分價量支撐壓力)")

    col1, col2 = st.columns([2, 4])
    with col1:
        report_dates = list_report_dates()
        if report_dates:
            selected_date = st.selectbox("Select date", report_dates, index=0, key="vp_date")
        else:
            selected_date = date.today().strftime("%Y-%m-%d")
            st.info("No data yet. Run `python main.py pipeline` first.")

    features = _load_features_cached(selected_date)

    vp_cols = [
        "stock_id", "close",
        "vp_peak_price", "vp_distance_to_peak",
        "vp_cluster_strength",
        "vp_support_score", "vp_pressure_score", "support_pressure_score",
        "vp_value_area_high", "vp_value_area_low", "vp_price_in_value_area",
    ]
    avail_vp = [c for c in vp_cols if c in features.columns]

    if not avail_vp or "vp_support_score" not in features.columns:
        st.warning(
            "Volume Profile columns not found.  "
            "Re-run `python main.py features` to compute them."
        )
        return

    vp_df = features[avail_vp].copy().sort_values("support_pressure_score", ascending=False)

    st.markdown("**Net score = Support − Pressure** (positive = more support below price)")

    rename_vp = {
        "stock_id": "Stock", "close": "Close",
        "vp_peak_price": "Peak Price", "vp_distance_to_peak": "Dist to Peak",
        "vp_cluster_strength": "Cluster Strength",
        "vp_support_score": "Support Score", "vp_pressure_score": "Pressure Score",
        "support_pressure_score": "Net Score",
        "vp_value_area_high": "VA High", "vp_value_area_low": "VA Low",
        "vp_price_in_value_area": "In VA",
    }
    vp_display = vp_df.rename(columns={k: v for k, v in rename_vp.items() if k in vp_df.columns})

    # Format
    for col in ["Dist to Peak"]:
        if col in vp_display.columns:
            vp_display[col] = vp_display[col].apply(lambda x: f"{x:+.2%}" if pd.notna(x) else "N/A")
    for col in ["Support Score", "Pressure Score", "Net Score", "Cluster Strength"]:
        if col in vp_display.columns:
            vp_display[col] = vp_display[col].apply(lambda x: f"{x:.3f}" if pd.notna(x) else "N/A")
    if "In VA" in vp_display.columns:
        vp_display["In VA"] = vp_display["In VA"].apply(
            lambda x: "Yes" if x == 1.0 else ("No" if x == 0.0 else "N/A")
        )

    st.dataframe(vp_display, use_container_width=True, height=500)

    # ---- Pressure / Support chart for a selected stock ------------------
    st.markdown("---")
    st.subheader("Stock Detail – Volume Profile Chart")
    all_stocks = features["stock_id"].unique().tolist() if "stock_id" in features.columns else []
    if all_stocks:
        sel_stock = st.selectbox("Choose a stock", sorted(all_stocks))
        days_back = st.slider("Lookback days", 20, 252, 60)

        price_hist = _load_price_history(sel_stock, days=days_back + 10)
        if not price_hist.empty and "close" in price_hist.columns:
            import matplotlib.pyplot as plt

            price_hist = price_hist.sort_values("date").tail(days_back)
            closes = price_hist["close"].values
            highs = price_hist["high"].values if "high" in price_hist.columns else closes
            lows = price_hist["low"].values if "low" in price_hist.columns else closes
            volumes = price_hist["volume"].values if "volume" in price_hist.columns else np.ones(len(closes))

            # Build simple volume profile histogram
            n_bins = 20
            price_min, price_max = np.nanmin(lows), np.nanmax(highs)
            bin_edges = np.linspace(price_min, price_max, n_bins + 1)
            bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
            bin_vols = np.zeros(n_bins)
            for i in range(len(closes)):
                bar_rng = highs[i] - lows[i]
                for k in range(n_bins):
                    ovl_lo = max(bin_edges[k], lows[i])
                    ovl_hi = min(bin_edges[k + 1], highs[i])
                    if ovl_hi > ovl_lo:
                        frac = (ovl_hi - ovl_lo) / bar_rng if bar_rng > 1e-9 else 1.0
                        bin_vols[k] += volumes[i] * frac

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={"width_ratios": [3, 1]})
            fig.patch.set_facecolor("#0e1117")
            for ax in [ax1, ax2]:
                ax.set_facecolor("#0e1117")
                ax.tick_params(colors="white")
                for sp in ax.spines.values():
                    sp.set_color("#333")

            dates_plot = pd.to_datetime(price_hist["date"])
            ax1.plot(dates_plot, closes, color="#00d4ff", linewidth=1.5, label=sel_stock)
            ax1.set_title(f"{sel_stock} Price ({days_back}d)", color="white")
            ax1.set_ylabel("Price", color="white")
            ax1.legend(facecolor="#1a1a2e", labelcolor="white")

            peak_idx = int(np.argmax(bin_vols))
            colors_vp = ["#ff6b6b" if i == peak_idx else "#4fc3f7" for i in range(n_bins)]
            ax2.barh(bin_centers, bin_vols, height=(bin_edges[1] - bin_edges[0]) * 0.85,
                     color=colors_vp, alpha=0.8)
            ax2.axhline(y=float(closes[-1]), color="yellow", linestyle="--", linewidth=1.2, label="Current")
            ax2.set_title("Volume Profile", color="white")
            ax2.set_xlabel("Volume", color="white")
            ax2.legend(facecolor="#1a1a2e", labelcolor="white")

            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("No price history available for this stock.")


# ---------------------------------------------------------------------------
# Page: Opening 15-min Strength
# ---------------------------------------------------------------------------

def page_opening_strength():
    """Render the Opening 15-min Microstructure Strength ranking page."""
    st.title("⚡ Opening 15-min Strength Ranking (開盤 15 分鐘強弱榜)")

    col1, _ = st.columns([2, 4])
    with col1:
        report_dates = list_report_dates()
        if report_dates:
            selected_date = st.selectbox("Select date", report_dates, index=0, key="ms_date")
        else:
            selected_date = date.today().strftime("%Y-%m-%d")
            st.info("No data yet. Run `python main.py pipeline` first.")

    features = _load_features_cached(selected_date)

    ms_cols = [
        "stock_id", "close",
        "microstructure_score", "buy_sell_pressure",
        "opening_return_15m", "opening_volume_ratio",
        "opening_high_break", "opening_low_break",
        "ms_fake_breakout_risk", "ms_no_chase_flag",
    ]
    avail_ms = [c for c in ms_cols if c in features.columns]

    if "microstructure_score" not in features.columns:
        st.warning(
            "Microstructure columns not found.  "
            "Re-run `python main.py features` to compute them."
        )
        return

    ms_df = features[avail_ms].copy().sort_values("microstructure_score", ascending=False)

    # ---- Summary KPIs ---------------------------------------------------
    avg_ms = ms_df["microstructure_score"].mean()
    n_strong = (ms_df["microstructure_score"] > 0.6).sum()
    n_weak = (ms_df["microstructure_score"] < 0.4).sum()
    n_fake = ms_df.get("ms_fake_breakout_risk", pd.Series(dtype=float)).sum() if "ms_fake_breakout_risk" in ms_df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Avg MS Score", f"{avg_ms:.3f}" if pd.notna(avg_ms) else "N/A")
    with c2:
        st.metric("Strong Stocks (>0.6)", int(n_strong))
    with c3:
        st.metric("Weak Stocks (<0.4)", int(n_weak))
    with c4:
        st.metric("Fake Breakout Risk", int(n_fake))

    st.markdown("---")

    # ---- Ranking table --------------------------------------------------
    rename_ms = {
        "stock_id": "Stock", "close": "Close",
        "microstructure_score": "MS Score", "buy_sell_pressure": "Buy/Sell Pressure",
        "opening_return_15m": "Open 15m Ret", "opening_volume_ratio": "Open Vol Ratio",
        "opening_high_break": "Hi Break", "opening_low_break": "Lo Break",
        "ms_fake_breakout_risk": "Fake BK Risk", "ms_no_chase_flag": "No Chase",
    }
    ms_display = ms_df.rename(columns={k: v for k, v in rename_ms.items() if k in ms_df.columns})

    for col in ["Open 15m Ret"]:
        if col in ms_display.columns:
            ms_display[col] = ms_display[col].apply(lambda x: f"{x:+.2%}" if pd.notna(x) else "N/A")
    for col in ["MS Score", "Buy/Sell Pressure", "Open Vol Ratio"]:
        if col in ms_display.columns:
            ms_display[col] = ms_display[col].apply(lambda x: f"{x:.3f}" if pd.notna(x) else "N/A")
    for col in ["Hi Break", "Lo Break", "Fake BK Risk", "No Chase"]:
        if col in ms_display.columns:
            ms_display[col] = ms_display[col].apply(
                lambda x: "Yes" if x == 1.0 else ("No" if x == 0.0 else "N/A")
            )

    st.subheader("All Stocks – Microstructure Ranking")
    st.dataframe(ms_display, use_container_width=True, height=500)

    # ---- No-chase & fake-breakout alerts --------------------------------
    if "ms_no_chase_flag" in features.columns:
        no_chase_stocks = ms_df[ms_df["ms_no_chase_flag"] == 1.0]["stock_id"].tolist()
        if no_chase_stocks:
            st.warning(f"不建議追價 (No-Chase): {', '.join(str(s) for s in no_chase_stocks)}")

    if "ms_fake_breakout_risk" in features.columns:
        fake_stocks = ms_df[ms_df["ms_fake_breakout_risk"] == 1.0]["stock_id"].tolist()
        if fake_stocks:
            st.error(f"假突破風險警告 (Fake Breakout Risk): {', '.join(str(s) for s in fake_stocks)}")


# ---------------------------------------------------------------------------
# Page: Backtest
# ---------------------------------------------------------------------------

def page_backtest():
    """Render the Backtest page."""
    st.title("📊 Backtesting Engine")

    # Controls
    col1, col2, col3 = st.columns(3)
    with col1:
        strategy_name = st.selectbox(
            "Strategy",
            ["momentum", "mean_reversion", "breakout"],
            index=0,
        )
    with col2:
        start_date = st.date_input(
            "Start Date",
            value=date(2022, 1, 1),
            min_value=date(2019, 1, 1),
        )
    with col3:
        end_date = st.date_input(
            "End Date",
            value=date.today(),
            min_value=date(2019, 1, 1),
        )

    initial_capital = st.number_input(
        "Initial Capital (NTD)",
        min_value=100_000,
        max_value=100_000_000,
        value=config.INITIAL_CAPITAL,
        step=100_000,
    )

    run_backtest = st.button("Run Backtest", type="primary")

    if not run_backtest:
        st.info("Configure backtest parameters above and click 'Run Backtest'.")
        return

    with st.spinner("Running backtest..."):
        try:
            # Load feature data
            initialize_db()
            feature_df = load_features(
                start_date=str(start_date),
                end_date=str(end_date),
            )

            if feature_df.empty:
                st.error(
                    "No feature data found. Please run:\n"
                    "```\npython main.py download\npython main.py features\n```"
                )
                return

            # Import strategy
            if strategy_name == "momentum":
                from strategies.momentum import MomentumStrategy
                strategy = MomentumStrategy()
            elif strategy_name == "mean_reversion":
                from strategies.mean_reversion import MeanReversionStrategy
                strategy = MeanReversionStrategy()
            else:
                from strategies.breakout import BreakoutStrategy
                strategy = BreakoutStrategy()

            # Run backtest
            from backtest.engine import BacktestEngine
            engine = BacktestEngine(strategy=strategy, initial_capital=initial_capital)
            results = engine.run(feature_df)

        except Exception as exc:
            st.error(f"Backtest failed: {exc}")
            import traceback
            st.code(traceback.format_exc())
            return

    hist = results.get("portfolio_history", pd.DataFrame())
    if hist.empty:
        st.warning("Backtest produced no results.")
        return

    st.success("Backtest complete!")
    st.markdown("---")

    # ---- KPI cards -------------------------------------------------------
    st.subheader("Performance KPIs")
    kpi_cols = st.columns(5)

    kpis = [
        ("Total Return", results.get("total_return"), "+.2%", 0),
        ("Sharpe Ratio", results.get("sharpe_ratio"), ".3f", 1.5),
        ("Max Drawdown", results.get("max_drawdown"), ".2%", None),
        ("Profit Factor", results.get("profit_factor"), ".3f", 1.5),
        ("Win Rate", results.get("win_rate"), ".1%", 0.5),
    ]

    for i, (label, val, fmt, target) in enumerate(kpis):
        with kpi_cols[i]:
            if val is not None and not (isinstance(val, float) and np.isnan(val)):
                formatted = format(val, fmt)
                if target is not None:
                    if label == "Max Drawdown":
                        delta_color = "inverse" if val > 0.20 else "normal"
                    else:
                        delta_color = "normal" if val >= target else "inverse"
                    st.metric(label, formatted)
                else:
                    st.metric(label, formatted)
            else:
                st.metric(label, "N/A")

    # KPI target check
    kpi_check = engine.meets_kpi_targets(results)
    all_pass = all(v["passed"] for v in kpi_check.values())
    if all_pass:
        st.success("All KPI targets met!")
    else:
        failed = [k for k, v in kpi_check.items() if not v["passed"]]
        st.warning(f"KPI targets not met: {', '.join(failed)}")

    st.markdown("---")

    # ---- Equity curve ---------------------------------------------------
    st.subheader("Equity Curve")

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    hist["date"] = pd.to_datetime(hist["date"])
    hist = hist.sort_values("date")

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.patch.set_facecolor("#0e1117")
    for ax in axes:
        ax.set_facecolor("#0e1117")
        ax.tick_params(colors="white")
        ax.spines["bottom"].set_color("#333")
        ax.spines["top"].set_color("#333")
        ax.spines["left"].set_color("#333")
        ax.spines["right"].set_color("#333")

    # Portfolio value
    axes[0].plot(hist["date"], hist["portfolio_value"], color="#00d4ff", linewidth=1.5)
    axes[0].axhline(y=initial_capital, color="#666", linestyle="--", linewidth=0.8)
    axes[0].set_ylabel("Portfolio Value (NTD)", color="white")
    axes[0].yaxis.label.set_color("white")
    axes[0].set_title(
        f"Backtest: {strategy_name.replace('_', ' ').title()} Strategy", color="white", fontsize=13
    )

    # Drawdown
    axes[1].fill_between(
        hist["date"], hist["drawdown"] * 100, 0, alpha=0.7, color="#ff4b4b"
    )
    axes[1].axhline(y=config.MAX_DRAWDOWN_HALT * 100, color="orange", linestyle="--", linewidth=1, label=f"Halt level ({config.MAX_DRAWDOWN_HALT:.0%})")
    axes[1].set_ylabel("Drawdown (%)", color="white")
    axes[1].yaxis.label.set_color("white")
    axes[1].legend(facecolor="#1a1a2e", labelcolor="white")
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=30, color="white")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # ---- Trade table ---------------------------------------------------
    st.subheader("Trade History")
    trades_df = engine.get_trades()
    if not trades_df.empty:
        trades_display = trades_df.copy()
        trades_display["pnl_pct"] = trades_display["pnl_pct"].apply(
            lambda x: f"{x:+.2%}" if pd.notna(x) else "N/A"
        )
        trades_display["pnl"] = trades_display["pnl"].apply(
            lambda x: f"{x:+.0f}" if pd.notna(x) else "N/A"
        )
        st.dataframe(trades_display, use_container_width=True, height=300)
    else:
        st.info("No completed trades in this period.")

    # ---- Additional stats -----------------------------------------------
    with st.expander("Additional Statistics"):
        stats_data = {
            "Metric": [
                "Initial Capital", "Final Value", "Annualised Return",
                "N Trading Days", "N Trades", "Avg Win %", "Avg Loss %"
            ],
            "Value": [
                f"NTD {results.get('initial_value', 0):,.0f}",
                f"NTD {results.get('final_value', 0):,.0f}",
                f"{results.get('annualised_return', 0):+.2%}",
                str(results.get("n_trading_days", 0)),
                str(results.get("n_trades", 0)),
                f"{results.get('avg_win_pct', 0):+.2%}",
                f"{results.get('avg_loss_pct', 0):+.2%}",
            ],
        }
        st.dataframe(pd.DataFrame(stats_data), use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Page: Strategy Performance
# ---------------------------------------------------------------------------

def page_strategy_performance():
    """Render the Strategy Performance comparison page."""
    st.title("🔬 Strategy Performance Comparison")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=date(2022, 1, 1),
            key="strat_start",
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=date.today(),
            key="strat_end",
        )

    run_comparison = st.button("Compare Strategies", type="primary")

    if not run_comparison:
        st.info("Click 'Compare Strategies' to run backtests for all three strategies.")
        return

    initialize_db()
    feature_df = load_features(start_date=str(start_date), end_date=str(end_date))

    if feature_df.empty:
        st.error("No feature data. Run `python main.py download && python main.py features` first.")
        return

    from strategies.momentum import MomentumStrategy
    from strategies.mean_reversion import MeanReversionStrategy
    from strategies.breakout import BreakoutStrategy
    from backtest.engine import BacktestEngine

    strategy_map = {
        "Momentum": MomentumStrategy,
        "Mean Reversion": MeanReversionStrategy,
        "Breakout": BreakoutStrategy,
    }

    results = {}
    equity_curves = {}

    progress = st.progress(0)
    for i, (name, cls) in enumerate(strategy_map.items()):
        with st.spinner(f"Running {name} backtest..."):
            engine = BacktestEngine(strategy=cls(), initial_capital=config.INITIAL_CAPITAL)
            try:
                res = engine.run(feature_df)
                results[name] = res
                hist = res.get("portfolio_history", pd.DataFrame())
                if not hist.empty:
                    equity_curves[name] = hist
            except Exception as exc:
                st.error(f"{name} backtest failed: {exc}")
        progress.progress((i + 1) / len(strategy_map))

    if not results:
        st.error("All backtests failed.")
        return

    st.success("All backtests complete!")
    st.markdown("---")

    # ---- Comparison table -----------------------------------------------
    st.subheader("Performance Comparison")

    comparison_rows = []
    for name, res in results.items():
        comparison_rows.append(
            {
                "Strategy": name,
                "Total Return": f"{res.get('total_return', 0):+.2%}",
                "Sharpe Ratio": f"{res.get('sharpe_ratio', float('nan')):.3f}",
                "Max Drawdown": f"{res.get('max_drawdown', 0):.2%}",
                "Profit Factor": f"{res.get('profit_factor', float('nan')):.3f}",
                "Win Rate": f"{res.get('win_rate', float('nan')):.1%}",
                "N Trades": str(res.get("n_trades", 0)),
            }
        )

    comp_df = pd.DataFrame(comparison_rows)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    # ---- Equity curves chart -------------------------------------------
    if equity_curves:
        st.subheader("Equity Curves Comparison")

        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates

        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("#333")

        colours = {"Momentum": "#00d4ff", "Mean Reversion": "#00ff88", "Breakout": "#ff6b6b"}

        for name, hist in equity_curves.items():
            hist_sorted = hist.sort_values("date")
            dates = pd.to_datetime(hist_sorted["date"])
            vals = hist_sorted["portfolio_value"]
            normalised = vals / vals.iloc[0] * 100  # index to 100
            ax.plot(dates, normalised, label=name, color=colours.get(name, None), linewidth=1.5)

        ax.axhline(y=100, color="#666", linestyle="--", linewidth=0.8, label="Baseline")
        ax.set_ylabel("Portfolio Value (indexed to 100)", color="white")
        ax.set_title("Strategy Comparison – Normalised Equity Curves", color="white", fontsize=13)
        ax.legend(facecolor="#1a1a2e", labelcolor="white")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.xticks(rotation=30, color="white")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ---- Regime breakdown -----------------------------------------------
    st.subheader("Strategy Recommendation by Regime")

    regime_recs = [
        {"Regime": "Bull + Low Vol", "Recommended": "Momentum", "Reason": "Trend following works best in sustained bull runs"},
        {"Regime": "Bull + High Vol", "Recommended": "Breakout", "Reason": "Volatility creates breakout opportunities"},
        {"Regime": "Bear", "Recommended": "Mean Reversion", "Reason": "Oversold bounces in downtrends"},
        {"Regime": "Sideways", "Recommended": "Mean Reversion", "Reason": "Range-bound price action suits reversion"},
    ]
    st.dataframe(pd.DataFrame(regime_recs), use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

if page == "Daily Picks":
    page_daily_picks()
elif page == "Volume Profile":
    page_volume_profile()
elif page == "Opening Strength":
    page_opening_strength()
elif page == "Backtest":
    page_backtest()
elif page == "Strategy Performance":
    page_strategy_performance()
