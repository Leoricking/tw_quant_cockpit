"""
analysis/timeframe_requirements.py - Data requirements for each analysis timeframe.

Defines what data is needed for each timeframe and checks completeness.
"""

DATA_INSUFFICIENT_WARNING = "資料不足，只能做盤中初估，不能當正式短中長線操作依據"

DAYTRADE_REQUIREMENTS = {
    'name': 'daytrade',
    'required': ['price_1min', 'bidask_realtime', 'tick_stream'],
    'optional': ['price_daily_20d', 'chip_3d'],
    'min_completeness_for_report': 40,
    'description': '當沖策略需要即時盤口與分鐘K資料',
}

SHORT_TERM_REQUIREMENTS = {
    'name': 'short_term',
    'required': ['price_daily_20d', 'price_daily_60d'],
    'optional': ['chip_5d', 'chip_10d', 'fundamental_monthly'],
    'min_completeness_for_report': 50,
    'description': '短線策略需要日K與籌碼資料',
}

MID_TERM_REQUIREMENTS = {
    'name': 'mid_term',
    'required': ['price_daily_60d', 'price_weekly_12w'],
    'optional': ['chip_10d', 'chip_20d', 'fundamental_quarterly'],
    'min_completeness_for_report': 50,
    'description': '中線策略需要週K與季報資料',
}

LONG_TERM_REQUIREMENTS = {
    'name': 'long_term',
    'required': ['price_daily_240d', 'price_monthly_12m'],
    'optional': ['fundamental_annual', 'fundamental_quarterly_4q'],
    'min_completeness_for_report': 60,
    'description': '長線策略需要月K與年報資料',
}

_ALL_REQUIREMENTS = {
    'daytrade': DAYTRADE_REQUIREMENTS,
    'short_term': SHORT_TERM_REQUIREMENTS,
    'mid_term': MID_TERM_REQUIREMENTS,
    'long_term': LONG_TERM_REQUIREMENTS,
}


def check_data_completeness(timeframe, available_data):
    """
    Check data completeness for a given timeframe.

    Parameters
    ----------
    timeframe : str
        One of 'daytrade', 'short_term', 'mid_term', 'long_term'.
    available_data : dict or set
        Keys/items representing available data types.

    Returns
    -------
    tuple: (completeness_pct: float, missing_items: list, can_generate_report: bool)
    """
    req = _ALL_REQUIREMENTS.get(timeframe)
    if req is None:
        return (0.0, ['unknown timeframe'], False)

    all_items = req['required'] + req['optional']
    if not all_items:
        return (100.0, [], True)

    available_set = set(available_data) if not isinstance(available_data, dict) else set(available_data.keys())
    missing_required = [item for item in req['required'] if item not in available_set]
    missing_optional = [item for item in req['optional'] if item not in available_set]
    missing_all = missing_required + missing_optional

    present_count = len(all_items) - len(missing_all)
    completeness_pct = (present_count / len(all_items)) * 100.0

    min_comp = req.get('min_completeness_for_report', 50)
    can_report = (completeness_pct >= min_comp) and (len(missing_required) == 0)

    return (round(completeness_pct, 1), missing_all, can_report)
