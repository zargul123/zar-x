"""
Zar X cockpit — the Morning Brief.

One command: a plain-words briefing for every watched asset — price, trend
state, momentum, volatility, and the weather report — plus a ready example
risk plan so the pilot always sees what a disciplined trade would look like.

Assembled ONLY from the sealed compartments' doorways (data, indicators,
regime, risk). Facts and instrument readings — never advice, never a
promise. Any offline instrument reports itself; the Brief continues.
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ASSETS, RISK_CONFIG
from data.market_data import MarketData
from indicators.technical import add_indicators
from regime.vane import RegimeVane
from risk.calculator import RiskCalculator

TIMEFRAME = '4h'
CANDLES = 300
BRIEF_CAPITAL = 1000.0  # example capital for the illustrative risk plan


def _trend_words(last) -> str:
    above50 = last['close'] > last['ema_50']
    above200 = last['close'] > last['ema_200']
    if above50 and above200:
        return "UP (price above EMA-50 and EMA-200)"
    if not above50 and not above200:
        return "DOWN (price below EMA-50 and EMA-200)"
    return "MIXED (between EMA-50 and EMA-200)"


def _rsi_words(rsi: float) -> str:
    if rsi >= 70: return f"{rsi:.0f} — overbought territory"
    if rsi <= 30: return f"{rsi:.0f} — oversold territory"
    return f"{rsi:.0f} — neutral"


def asset_brief(md, vane, risk, asset: str) -> bool:
    print(f"\n{'─' * 62}")
    print(f"  {asset}")
    print(f"{'─' * 62}")
    df = md.get_candles(asset, timeframe=TIMEFRAME, limit=CANDLES)
    if df is None or df.empty:
        print("  🔌 data instrument offline — no briefing for this asset")
        return False
    df = add_indicators(df)
    last = df.iloc[-1]
    prev_day = df.iloc[-7] if len(df) > 7 else df.iloc[0]  # ~24h ago on 4h
    change_24h = (last['close'] / prev_day['close'] - 1) * 100

    print(f"  Price     : ${last['close']:,.2f}  ({change_24h:+.2f}% vs ~24h ago)")
    print(f"  Trend     : {_trend_words(last)}")
    print(f"  Momentum  : RSI {_rsi_words(last['rsi'])}")
    print(f"  Volatility: ATR ${last['atr']:,.2f} ({last['atr'] / last['close'] * 100:.2f}% of price)")

    weather = vane.read(df, timeframe=TIMEFRAME)
    tag = "" if weather['calibrated'] else " (uncalibrated)"
    print(f"  Weather   : {weather['regime']}{tag}"
          + (f"  [entropy {weather['entropy']:.3f} | ADX {weather['adx']:.1f}]"
             if weather['entropy'] is not None else ""))

    plan = risk.plan_trade(capital=BRIEF_CAPITAL, entry_price=float(last['close']),
                           direction='long', atr=float(last['atr']))
    if plan:
        print(f"  Example   : long ${BRIEF_CAPITAL:,.0f} acct → "
              f"SL ${plan['stop_loss']:,.2f} · TP ${plan['take_profit']:,.2f} · "
              f"size ${plan['position_value']:,.0f} · risk ${plan['risk_money']:,.2f}")
    return True


def run_brief() -> int:
    print("=" * 62)
    print(f"  ZAR X — MORNING BRIEF   {datetime.now():%Y-%m-%d %H:%M}   [{TIMEFRAME}]")
    print("=" * 62)
    md, vane, risk = MarketData(), RegimeVane(), RiskCalculator()
    ok = sum(asset_brief(md, vane, risk, a) for a in ASSETS)
    print(f"\n{'=' * 62}")
    print(f"  {ok}/{len(ASSETS)} instruments reporting. "
          f"Facts, not advice — the pilot decides.")
    print("=" * 62)
    return ok


if __name__ == '__main__':
    if run_brief() == 0:
        sys.exit("BRIEF FAILED: no assets reporting.")
