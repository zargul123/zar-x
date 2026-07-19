"""
Zar X indicators compartment — chart math only.

Takes clean OHLC candles (from data/) and returns them enriched with the
proven 'Elite' indicator set ported from Zargul 2.0, plus the long EMAs the
Morning Brief needs for trend state. No fetching, no signals, no risk math —
those live in their own compartments.

Fail-safe: on any error returns the original candles untouched and reports
"INDICATORS INSTRUMENT OFFLINE" — never raises into the rest of the ship.
"""
import sys
import os

import pandas as pd
import pandas_ta as ta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Enrich candles with the Elite indicator set. Returns a new DataFrame."""
    if df is None or df.empty:
        return df
    try:
        out = df.copy()
        out = out.loc[:, ~out.columns.duplicated()]

        # pandas-ta needs a volume column even when the source has none
        if 'volume' not in out.columns:
            out['volume'] = 0

        strategy = ta.Strategy(
            name="ZarXElite",
            description="Proven Elite indicator set ported from Zargul 2.0.",
            ta=[
                {"kind": "rsi"},
                {"kind": "macd"},
                {"kind": "bbands", "length": 20, "std": 2},
                {"kind": "adx"},
                {"kind": "mfi", "length": 14},
                {"kind": "atr"},
                {"kind": "ema", "length": 20},
                {"kind": "ema", "length": 50},
                {"kind": "ema", "length": 200},
            ],
        )
        # In-process computation: the default multiprocessing Pool exhausts
        # RAM on Windows (each worker re-imports the full stack) — proven
        # failure mode in Zargul 2.0, fixed with cores=0.
        out.ta.cores = 0
        out.ta.strategy(strategy)

        out.rename(columns={
            'RSI_14': 'rsi',
            'MACD_12_26_9': 'macd',
            'MACDs_12_26_9': 'macd_signal',
            'ADX_14': 'adx',
            'MFI_14': 'mfi_14',
            'ATRr_14': 'atr',
            'BBB_20_2.0': 'bollinger_width',
            'BBU_20_2.0': 'bollinger_upper',
            'BBL_20_2.0': 'bollinger_lower',
            'EMA_20': 'ema_20',
            'EMA_50': 'ema_50',
            'EMA_200': 'ema_200',
        }, inplace=True)

        # Time features (kept from the proven pipeline)
        out['hour_of_day'] = out.index.hour
        out['day_of_week'] = out.index.dayofweek

        # Final cleanup, same order as the proven code
        out = out.loc[:, ~out.columns.duplicated()]
        out.ffill(inplace=True)
        out.bfill(inplace=True)
        out.fillna(0, inplace=True)
        return out

    except Exception as e:
        print(f"🔌 INDICATORS INSTRUMENT OFFLINE: {e}")
        return df


# Columns every consumer may rely on after add_indicators succeeds
CORE_COLUMNS = [
    'rsi', 'macd', 'macd_signal', 'adx', 'mfi_14', 'atr',
    'bollinger_width', 'bollinger_upper', 'bollinger_lower',
    'ema_20', 'ema_50', 'ema_200',
]
