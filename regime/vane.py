"""
Zar X regime compartment — the weather vane (Edge Stack Layer 2).

Classifies market character as Trending / Ranging / Chaotic using ADX
(trend strength) and smoothed Shannon entropy of returns (randomness).
Ported from Zargul 2.0's MarketRegimeFilter with three lessons applied:

1. PER-TIMEFRAME thresholds (the 1h-tuned dial saturated on 4h candles and
   stamped ~92% of history "Chaotic" — root cause found 2026-07-19).
2. Fail-honest: a timeframe without a calibrated threshold returns
   "Uncalibrated" instead of a confident guess.
3. Stateless readings: the museum filter kept one EMA state shared across
   ALL assets (cross-contamination bug). Here every reading is replayed
   fresh from the supplied candles — deterministic, isolated.

HONEST STATUS (recorded per Ship Law 1): in the 2026 full-year hold-out
study the vane improved a 6-month window but FAILED fresh-year validation
as a P&L rescue. It is a CONTEXT instrument — weather information for the
pilot — not proven alpha.

Fail-safe: on error returns "Offline" and never raises into the ship.
"""
import sys
import os

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import REGIME_CONFIG


class RegimeVane:

    def _entropy_series_last(self, returns: np.ndarray) -> float:
        """Replay smoothed entropy over the return series; return final EMA.
        Math identical to the proven filter (4 buckets at ±edge, EMA alpha)."""
        window = REGIME_CONFIG['entropy_window']
        alpha = REGIME_CONFIG['entropy_smoothing_alpha']
        edge = REGIME_CONFIG['entropy_bin_edge']
        ema = 1.0
        for i in range(window + 1, len(returns) + 1):
            win = returns[i - window:i]
            bins = np.digitize(win, [-edge, 0.0, edge])
            counts = np.bincount(bins, minlength=4)
            p = counts / len(win)
            p = p[p > 0]
            raw = -np.sum(p * np.log2(p))
            ema = alpha * raw + (1 - alpha) * ema
        return float(ema)

    def read(self, df: pd.DataFrame, timeframe: str) -> dict:
        """
        Weather reading for the supplied candles.
        Returns {'regime', 'entropy', 'adx', 'calibrated'} — regime is one of
        Trending / Ranging / Chaotic / Uncalibrated / Offline.
        """
        try:
            threshold = REGIME_CONFIG['entropy_chaotic_thresholds'].get(timeframe)
            adx = float(df['adx'].iloc[-1]) if 'adx' in df.columns else None
            returns = df['close'].pct_change().dropna().values
            if len(returns) < REGIME_CONFIG['entropy_window'] + 1:
                raise ValueError("not enough candles for an entropy reading")
            entropy = self._entropy_series_last(returns)

            if threshold is None:
                return {'regime': 'Uncalibrated', 'entropy': entropy,
                        'adx': adx, 'calibrated': False}

            if entropy > threshold:
                regime = 'Chaotic'
            elif adx is not None and adx > REGIME_CONFIG['adx_trending_threshold']:
                regime = 'Trending'
            else:
                regime = 'Ranging'
            return {'regime': regime, 'entropy': entropy,
                    'adx': adx, 'calibrated': True}

        except Exception as e:
            print(f"🔌 REGIME INSTRUMENT OFFLINE: {e}")
            return {'regime': 'Offline', 'entropy': None,
                    'adx': None, 'calibrated': False}
