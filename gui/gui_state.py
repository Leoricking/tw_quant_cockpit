"""
gui/gui_state.py - Shared GUI state for TW Quant Cockpit.
"""
from datetime import datetime


class GUIState:
    """
    Shared state container for all GUI panels.

    All panels read from and write to this shared instance so that
    mode switches, symbol selection, and refresh events propagate
    consistently without tight coupling between panels.
    """

    def __init__(self):
        self.selected_symbol: str = None
        self.current_mode: str = 'mock'          # 'mock' or 'real'
        self.watchlist_source: str = 'screener'  # 'watchlist', 'profile', 'screener'
        self.last_candidates: list = []
        self.last_data_check: dict = {}           # symbol -> check_stock() result
        self.last_report_path: str = None
        self.last_refresh_time: str = None
        self.last_warning: str = ''

    def update_refresh_time(self):
        self.last_refresh_time = datetime.now().strftime('%H:%M:%S')

    def set_mode(self, mode: str):
        if mode in ('mock', 'real'):
            self.current_mode = mode

    def set_symbol(self, symbol: str):
        self.selected_symbol = str(symbol) if symbol else None

    def cache_data_check(self, symbol: str, result: dict):
        self.last_data_check[str(symbol)] = result

    def get_data_check(self, symbol: str):
        return self.last_data_check.get(str(symbol) if symbol else '')
