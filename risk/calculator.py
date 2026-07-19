"""
Zar X risk compartment — the Discipline Engine (Edge Stack Layer 1).

Given "I want to long/short X here", this part answers: where is the stop,
where is the target, and exactly how much to buy so that a losing trade
costs only the chosen fraction of capital. This is the math that makes a
~40%-wrong signal stream survivable.

Ported from Zargul 2.0's proven RiskManager: ATR calculation and ATR-based
SL/TP levels (kept faithful). Position sizing upgraded to the standard
stop-distance formula (size = risk money / stop distance). Deliberately
NOT ported: trailing stop (our own 2026 data showed it cut winners and
kept losers) and the AI-prediction gate (dead pipeline).

Fail-safe: on any error returns None and reports "RISK INSTRUMENT OFFLINE".
"""
import sys
import os

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RISK_CONFIG


class RiskCalculator:

    def atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """Average True Range — ported verbatim from the proven engine."""
        if df is None or df.empty or len(df) < period:
            return 0.0
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        return float(true_range.rolling(period).mean().iloc[-1])

    def levels(self, entry_price: float, direction: str, atr: float,
               sl_atr_mult: float = None, tp_atr_mult: float = None) -> dict:
        """ATR-based stop-loss / take-profit prices (proven logic)."""
        sl_mult = sl_atr_mult if sl_atr_mult is not None else RISK_CONFIG['default_sl_atr']
        tp_mult = tp_atr_mult if tp_atr_mult is not None else RISK_CONFIG['default_tp_atr']
        sl_dist = atr * sl_mult
        tp_dist = atr * tp_mult
        if direction == 'long':
            return {'stop_loss': entry_price - sl_dist,
                    'take_profit': entry_price + tp_dist}
        return {'stop_loss': entry_price + sl_dist,
                'take_profit': entry_price - tp_dist}

    def plan_trade(self, capital: float, entry_price: float, direction: str,
                   df: pd.DataFrame = None, atr: float = None,
                   risk_pct: float = None, sl_atr_mult: float = None,
                   tp_atr_mult: float = None) -> dict | None:
        """
        The cockpit's trade calculator. Returns the full plan:
        SL/TP prices, position size (units and $), money at risk, potential
        reward, and reward:risk ratio — or None if the instrument fails.
        """
        try:
            if direction not in ('long', 'short'):
                raise ValueError(f"direction must be 'long'/'short', got {direction!r}")
            if atr is None:
                atr = self.atr(df)
            if not atr or atr <= 0 or entry_price <= 0 or capital <= 0:
                raise ValueError("need positive capital, entry price and ATR")

            risk_fraction = risk_pct if risk_pct is not None else RISK_CONFIG['risk_per_trade']
            lv = self.levels(entry_price, direction, atr, sl_atr_mult, tp_atr_mult)

            stop_distance = abs(entry_price - lv['stop_loss'])
            risk_money = capital * risk_fraction

            # Core discipline formula: lose exactly risk_money if the stop hits
            size_units = risk_money / stop_distance
            position_value = size_units * entry_price

            # Safety cap: never concentrate more than the configured fraction
            max_value = capital * RISK_CONFIG['max_position_fraction']
            capped = position_value > max_value
            if capped:
                size_units = max_value / entry_price
                position_value = max_value
                risk_money = size_units * stop_distance

            reward_money = size_units * abs(lv['take_profit'] - entry_price)

            return {
                'direction': direction,
                'entry_price': entry_price,
                'stop_loss': lv['stop_loss'],
                'take_profit': lv['take_profit'],
                'atr': atr,
                'size_units': size_units,
                'position_value': position_value,
                'risk_money': risk_money,
                'reward_money': reward_money,
                'reward_risk_ratio': reward_money / risk_money if risk_money else 0.0,
                'position_capped': capped,
            }
        except Exception as e:
            print(f"🔌 RISK INSTRUMENT OFFLINE: {e}")
            return None
