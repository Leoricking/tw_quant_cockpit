"""
gui/charts.py - Plotly chart builders for TW Quant Cockpit.

All functions return plotly Figure objects or None on error.
"""

import logging

logger = logging.getLogger(__name__)

try:
    import plotly.graph_objects as go
    _PLOTLY_AVAILABLE = True
except ImportError:
    _PLOTLY_AVAILABLE = False
    logger.warning("plotly not installed. Chart functions will return None.")


def create_price_chart(price_data, symbol=''):
    """
    Create a candlestick price chart.

    Parameters
    ----------
    price_data : list of dicts
        Each dict has: date, open, high, low, close (and optionally volume).
    symbol : str
        Stock symbol for chart title.

    Returns
    -------
    plotly.graph_objects.Figure or None
    """
    if not _PLOTLY_AVAILABLE:
        return None

    if not price_data:
        logger.warning("create_price_chart: no price_data provided.")
        return None

    try:
        dates = []
        opens = []
        highs = []
        lows = []
        closes = []

        for p in price_data:
            if isinstance(p, dict):
                dates.append(p.get('date', ''))
                opens.append(float(p.get('open', p.get('Open', 0)) or 0))
                highs.append(float(p.get('high', p.get('High', 0)) or 0))
                lows.append(float(p.get('low', p.get('Low', 0)) or 0))
                closes.append(float(p.get('close', p.get('Close', 0)) or 0))

        if not closes:
            return None

        fig = go.Figure(data=[
            go.Candlestick(
                x=dates,
                open=opens,
                high=highs,
                low=lows,
                close=closes,
                name=symbol,
                increasing_line_color='red',
                decreasing_line_color='green',
            )
        ])

        # Add MA lines
        if len(closes) >= 5:
            ma5 = [sum(closes[max(0,i-4):i+1]) / min(5, i+1) for i in range(len(closes))]
            fig.add_trace(go.Scatter(x=dates, y=ma5, name='MA5', line=dict(color='orange', width=1)))
        if len(closes) >= 20:
            ma20 = [sum(closes[max(0,i-19):i+1]) / min(20, i+1) for i in range(len(closes))]
            fig.add_trace(go.Scatter(x=dates, y=ma20, name='MA20', line=dict(color='blue', width=1)))

        fig.update_layout(
            title=f'{symbol} 日K線',
            xaxis_title='Date',
            yaxis_title='Price (NTD)',
            template='plotly_dark',
            height=400,
            showlegend=True,
        )
        return fig

    except Exception as exc:
        logger.error("create_price_chart error: %s", exc)
        return None


def create_volume_chart(price_data):
    """
    Create a volume bar chart.

    Parameters
    ----------
    price_data : list of dicts with date, volume, close

    Returns
    -------
    plotly.graph_objects.Figure or None
    """
    if not _PLOTLY_AVAILABLE:
        return None

    if not price_data:
        return None

    try:
        dates = []
        volumes = []
        colors = []

        prev_close = None
        for p in price_data:
            if isinstance(p, dict):
                d = p.get('date', '')
                v = float(p.get('volume', p.get('Volume', 0)) or 0)
                c = float(p.get('close', p.get('Close', 0)) or 0)
                dates.append(d)
                volumes.append(v)
                color = 'red' if (prev_close is None or c >= prev_close) else 'green'
                colors.append(color)
                prev_close = c

        fig = go.Figure(data=[
            go.Bar(x=dates, y=volumes, marker_color=colors, name='Volume')
        ])
        fig.update_layout(
            title='Volume',
            xaxis_title='Date',
            yaxis_title='Volume',
            template='plotly_dark',
            height=200,
            showlegend=False,
        )
        return fig

    except Exception as exc:
        logger.error("create_volume_chart error: %s", exc)
        return None


def create_score_gauge(score, title='Score'):
    """
    Create a gauge chart for a 0-100 score.

    Parameters
    ----------
    score : float (0-100)
    title : str

    Returns
    -------
    plotly.graph_objects.Figure or None
    """
    if not _PLOTLY_AVAILABLE:
        return None

    try:
        score = max(0, min(100, float(score or 0)))

        if score >= 80:
            color = 'red'
        elif score >= 65:
            color = 'orange'
        elif score >= 50:
            color = 'yellow'
        else:
            color = 'gray'

        fig = go.Figure(go.Indicator(
            mode='gauge+number',
            value=score,
            title={'text': title},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 50], 'color': 'lightgray'},
                    {'range': [50, 65], 'color': 'lightyellow'},
                    {'range': [65, 80], 'color': 'lightorange'},
                    {'range': [80, 100], 'color': 'lightcoral'},
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 4},
                    'thickness': 0.75,
                    'value': 80,
                },
            }
        ))
        fig.update_layout(height=250, template='plotly_dark')
        return fig

    except Exception as exc:
        logger.error("create_score_gauge error: %s", exc)
        return None


def create_bidask_chart(bidask_data):
    """
    Create a 5-level bid/ask order book visualization.

    Parameters
    ----------
    bidask_data : dict
        Standard bid_price_1..5, bid_volume_1..5, ask_price_1..5, ask_volume_1..5

    Returns
    -------
    plotly.graph_objects.Figure or None
    """
    if not _PLOTLY_AVAILABLE:
        return None

    if not bidask_data:
        return None

    try:
        bid_prices = [bidask_data.get(f'bid_price_{i}', 0) for i in range(1, 6)]
        bid_vols = [bidask_data.get(f'bid_volume_{i}', 0) for i in range(1, 6)]
        ask_prices = [bidask_data.get(f'ask_price_{i}', 0) for i in range(1, 6)]
        ask_vols = [bidask_data.get(f'ask_volume_{i}', 0) for i in range(1, 6)]

        bid_labels = [f'Bid {p:.1f}' for p in bid_prices]
        ask_labels = [f'Ask {p:.1f}' for p in ask_prices]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Bid', x=bid_labels, y=bid_vols,
            marker_color='red', orientation='v',
        ))
        fig.add_trace(go.Bar(
            name='Ask', x=ask_labels, y=ask_vols,
            marker_color='green', orientation='v',
        ))

        fig.update_layout(
            title='5-Level Order Book',
            barmode='group',
            template='plotly_dark',
            height=300,
        )
        return fig

    except Exception as exc:
        logger.error("create_bidask_chart error: %s", exc)
        return None
