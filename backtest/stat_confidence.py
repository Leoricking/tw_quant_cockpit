"""
backtest/stat_confidence.py - Statistical confidence evaluation for backtests.

Classifies sample adequacy into three tiers:
  INSUFFICIENT   - too few samples; only confirms the code runs
  OBSERVATIONAL  - initial patterns visible; needs more data
  RELIABLE       - sufficient for strategy-adjustment reference (still not
                   investment advice)

Thresholds
----------
Universe:
  < 10  symbols  -> INSUFFICIENT
  < 50  symbols  -> OBSERVATIONAL
  >= 50 symbols  -> RELIABLE

Signal:
  < 30  signals  -> INSUFFICIENT
  < 200 signals  -> OBSERVATIONAL
  >= 200 signals -> RELIABLE

Bucket sample:
  < 30  rows     -> INSUFFICIENT
  < 100 rows     -> OBSERVATIONAL
  >= 100 rows    -> RELIABLE

Trading days:
  < 60  days     -> INSUFFICIENT
  < 120 days     -> OBSERVATIONAL
  >= 120 days    -> RELIABLE

Usage:
    from backtest.stat_confidence import StatConfidence
    sc = StatConfidence()
    r  = sc.evaluate(symbol_count=50, signal_count=300, trading_days=200)
    print(r['overall'])   # 'RELIABLE'
    print(r['reasons'])   # []

    b = sc.evaluate_bucket(sample_count=11)
    print(b['level'])     # 'INSUFFICIENT'
"""


class StatConfidence:
    """Evaluates statistical confidence of backtest / validation results."""

    # --- thresholds ---
    _T_SYM_INSUF    = 10
    _T_SYM_OBS      = 50
    _T_SIG_INSUF    = 30
    _T_SIG_OBS      = 200
    _T_BUCKET_INSUF = 30
    _T_BUCKET_OBS   = 100
    _T_DAYS_INSUF   = 60
    _T_DAYS_OBS     = 120

    # --- internal helpers ---

    def _level(self, value, t_insuf: int, t_obs: int) -> str:
        if value is None or value < t_insuf:
            return 'INSUFFICIENT'
        if value < t_obs:
            return 'OBSERVATIONAL'
        return 'RELIABLE'

    @staticmethod
    def _worst(*levels: str) -> str:
        order = ['INSUFFICIENT', 'OBSERVATIONAL', 'RELIABLE']
        for lvl in order:
            if lvl in levels:
                return lvl
        return 'INSUFFICIENT'

    # --- public API ---

    def evaluate(
        self,
        symbol_count: int,
        signal_count: int,
        trading_days: int = None,
    ) -> dict:
        """Evaluate overall confidence from universe + signal counts.

        Parameters
        ----------
        symbol_count  : number of distinct symbols in the universe
        signal_count  : total number of trading signals detected
        trading_days  : number of trading days covered (optional)

        Returns
        -------
        dict with keys:
          universe, signal, [trading_days], overall, reasons
        """
        sym_lvl = self._level(symbol_count, self._T_SYM_INSUF, self._T_SYM_OBS)
        sig_lvl = self._level(signal_count, self._T_SIG_INSUF, self._T_SIG_OBS)
        day_lvl = (
            self._level(trading_days, self._T_DAYS_INSUF, self._T_DAYS_OBS)
            if trading_days is not None
            else None
        )

        levels = [sym_lvl, sig_lvl]
        if day_lvl:
            levels.append(day_lvl)
        overall = self._worst(*levels)

        reasons = []
        if symbol_count < self._T_SYM_INSUF:
            reasons.append(
                f'symbol_count {symbol_count} < {self._T_SYM_INSUF} -> INSUFFICIENT'
            )
        elif symbol_count < self._T_SYM_OBS:
            reasons.append(
                f'symbol_count {symbol_count} < {self._T_SYM_OBS} -> OBSERVATIONAL'
            )
        if signal_count < self._T_SIG_INSUF:
            reasons.append(
                f'signal_count {signal_count} < {self._T_SIG_INSUF} -> INSUFFICIENT'
            )
        elif signal_count < self._T_SIG_OBS:
            reasons.append(
                f'signal_count {signal_count} < {self._T_SIG_OBS} -> OBSERVATIONAL'
            )
        if trading_days is not None:
            if trading_days < self._T_DAYS_INSUF:
                reasons.append(
                    f'trading_days {trading_days} < {self._T_DAYS_INSUF} -> INSUFFICIENT'
                )
            elif trading_days < self._T_DAYS_OBS:
                reasons.append(
                    f'trading_days {trading_days} < {self._T_DAYS_OBS} -> not yet RELIABLE'
                )

        result = {
            'universe': sym_lvl,
            'signal':   sig_lvl,
            'overall':  overall,
            'reasons':  reasons,
        }
        if day_lvl is not None:
            result['trading_days_level'] = day_lvl
        return result

    def evaluate_bucket(self, sample_count: int) -> dict:
        """Evaluate confidence for a single score-bucket row.

        Returns
        -------
        dict with keys: level, note
        """
        level = self._level(sample_count, self._T_BUCKET_INSUF, self._T_BUCKET_OBS)
        notes = {
            'INSUFFICIENT':  (
                f'sample {sample_count} < {self._T_BUCKET_INSUF}'
                ' — do not draw conclusions'
            ),
            'OBSERVATIONAL': (
                f'sample {sample_count} < {self._T_BUCKET_OBS}'
                ' — observational only'
            ),
            'RELIABLE': (
                f'sample {sample_count} >= {self._T_BUCKET_OBS}'
                ' — usable as reference'
            ),
        }
        return {'level': level, 'note': notes[level]}

    def evaluate_universe(self, symbol_count: int) -> dict:
        """Return a stage description for the current universe size.

        Returns
        -------
        dict with keys: level, stage, note
        """
        if symbol_count < 10:
            stage = 'FUNCTIONAL_TEST'
            note  = (
                f'{symbol_count} symbols — functional test only, '
                'no strategy conclusions possible'
            )
            level = 'INSUFFICIENT'
        elif symbol_count < 50:
            stage = 'SMALL_SAMPLE'
            note  = f'{symbol_count} symbols — small sample, observational only'
            level = 'INSUFFICIENT'
        elif symbol_count < 100:
            stage = 'BASIC_VALIDATION'
            note  = f'{symbol_count} symbols — basic validation possible'
            level = 'OBSERVATIONAL'
        elif symbol_count < 200:
            stage = 'BETTER_VALIDATION'
            note  = f'{symbol_count} symbols — better validation quality'
            level = 'RELIABLE'
        else:
            stage = 'PRODUCTION_LEVEL'
            note  = f'{symbol_count} symbols — production-level sample'
            level = 'RELIABLE'

        return {'level': level, 'stage': stage, 'note': note}

    def label(self, level: str) -> str:
        """Return the canonical plain-text label for a confidence level."""
        lvl = (level or '').strip().upper()
        if lvl == 'RELIABLE':
            return 'RELIABLE'
        if lvl == 'OBSERVATIONAL':
            return 'OBSERVATIONAL'
        return 'INSUFFICIENT'

    @staticmethod
    def for_universe(
        symbol_count: int,
        trading_days: int = None,
        signal_count: int = None,
    ) -> dict:
        """
        Evaluate confidence for a universe-level backtest.

        Rules (v0.3.8):
          symbol_count < 10                                  → INSUFFICIENT
          10 <= symbol_count < 30                            → OBSERVATIONAL
          symbol_count >= 30 and trading_days >= 120
            (and signal_count >= 200 if provided)            → RELIABLE

        Parameters
        ----------
        symbol_count  : number of symbols with sufficient data
        trading_days  : trading days covered (optional)
        signal_count  : total signals detected (optional)

        Returns
        -------
        dict with keys: overall, universe, reasons
        """
        if symbol_count < 10:
            uni_lvl = 'INSUFFICIENT'
        elif symbol_count < 30:
            uni_lvl = 'OBSERVATIONAL'
        else:
            uni_lvl = 'RELIABLE'

        levels = [uni_lvl]
        if trading_days is not None and trading_days < 120:
            levels.append('OBSERVATIONAL')
        if signal_count is not None and signal_count < 200:
            levels.append('OBSERVATIONAL' if signal_count >= 30 else 'INSUFFICIENT')

        order = ['INSUFFICIENT', 'OBSERVATIONAL', 'RELIABLE']
        overall = 'RELIABLE'
        for lvl in order:
            if lvl in levels:
                overall = lvl
                break

        reasons = []
        if symbol_count < 10:
            reasons.append(f'symbol_count {symbol_count} < 10 -> INSUFFICIENT')
        elif symbol_count < 30:
            reasons.append(f'symbol_count {symbol_count} < 30 -> OBSERVATIONAL')
        if trading_days is not None and trading_days < 120:
            reasons.append(f'trading_days {trading_days} < 120 -> not RELIABLE')
        if signal_count is not None and signal_count < 200:
            reasons.append(f'signal_count {signal_count} < 200 -> not RELIABLE')

        return {'overall': overall, 'universe': uni_lvl, 'reasons': reasons}

    @staticmethod
    def for_strategy_module(
        symbol_count: int,
        signal_count: int,
        trading_days: int = None,
        module_name: str = '',
    ) -> dict:
        """
        Evaluate confidence for a strategy knowledge module backtest.

        Rules (v0.3.7):
          symbol_count < 10                             → INSUFFICIENT
          signal_count < 30                             → INSUFFICIENT
          signal_count 30–199                           → OBSERVATIONAL
          trading_days < 120                            → not RELIABLE
          symbol_count >= 30 and signal_count >= 200
            and trading_days >= 120 (or None)           → RELIABLE

        Parameters
        ----------
        symbol_count  : distinct symbols in the backtest universe
        signal_count  : total signals of the module detected
        trading_days  : number of trading days covered
        module_name   : optional label for display

        Returns
        -------
        dict with keys: overall, universe, signal, trading_days_level, reasons
        """
        # Universe
        if symbol_count < 10:
            uni_lvl = 'INSUFFICIENT'
        elif symbol_count < 30:
            uni_lvl = 'OBSERVATIONAL'
        else:
            uni_lvl = 'RELIABLE'

        # Signal count
        if signal_count < 30:
            sig_lvl = 'INSUFFICIENT'
        elif signal_count < 200:
            sig_lvl = 'OBSERVATIONAL'
        else:
            sig_lvl = 'RELIABLE'

        # Trading days
        if trading_days is None:
            day_lvl = None
        elif trading_days < 120:
            day_lvl = 'OBSERVATIONAL'
        else:
            day_lvl = 'RELIABLE'

        levels = [uni_lvl, sig_lvl]
        if day_lvl is not None:
            levels.append(day_lvl)

        # Worst level wins
        order = ['INSUFFICIENT', 'OBSERVATIONAL', 'RELIABLE']
        overall = 'RELIABLE'
        for lvl in order:
            if lvl in levels:
                overall = lvl
                break

        reasons = []
        if symbol_count < 10:
            reasons.append(
                f'symbol_count {symbol_count} < 10 -> INSUFFICIENT'
            )
        elif symbol_count < 30:
            reasons.append(
                f'symbol_count {symbol_count} < 30 -> OBSERVATIONAL'
            )
        if signal_count < 30:
            reasons.append(
                f'signal_count {signal_count} < 30 -> INSUFFICIENT'
            )
        elif signal_count < 200:
            reasons.append(
                f'signal_count {signal_count} < 200 -> OBSERVATIONAL'
            )
        if trading_days is not None and trading_days < 120:
            reasons.append(
                f'trading_days {trading_days} < 120 -> not RELIABLE'
            )

        result = {
            'overall':   overall,
            'universe':  uni_lvl,
            'signal':    sig_lvl,
            'reasons':   reasons,
        }
        if module_name:
            result['module_name'] = module_name
        if day_lvl is not None:
            result['trading_days_level'] = day_lvl
        return result
