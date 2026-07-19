"""
Zar X cockpit — the Trade Planner.

The pilot says the trade; Zar X answers with the disciplined plan:
exact stop-loss, take-profit, position size, and money at risk — computed
from live market data by the Risk compartment. Facts and math, not advice.

Usage:
  python cockpit/plan.py --asset BTC-USD --direction long --capital 500
  python cockpit/plan.py --asset ETH-USD --direction short --capital 1000 --risk 2
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from config import ASSETS
    from data.market_data import MarketData
    from indicators.technical import add_indicators
    from regime.vane import RegimeVane
    from risk.calculator import RiskCalculator

    p = argparse.ArgumentParser(description="Plan a trade with discipline math.")
    p.add_argument('--asset', required=True, choices=ASSETS)
    p.add_argument('--direction', required=True, choices=['long', 'short'])
    p.add_argument('--capital', type=float, required=True,
                   help="Your account size in USD")
    p.add_argument('--risk', type=float, default=1.0,
                   help="Percent of capital to risk on this trade (default 1)")
    p.add_argument('--entry', type=float, default=None,
                   help="Planned entry price (default: current market price)")
    a = p.parse_args()

    df = MarketData().get_candles(a.asset, timeframe='4h', limit=300)
    if df is None or df.empty:
        sys.exit("🔌 Data instrument offline — cannot plan.")
    df = add_indicators(df)
    last = df.iloc[-1]
    entry = a.entry if a.entry else float(last['close'])

    weather = RegimeVane().read(df, timeframe='4h')
    plan = RiskCalculator().plan_trade(
        capital=a.capital, entry_price=entry, direction=a.direction,
        atr=float(last['atr']), risk_pct=a.risk / 100.0)
    if plan is None:
        sys.exit("🔌 Risk instrument offline — cannot plan.")

    print("=" * 56)
    print(f"  ZAR X TRADE PLAN — {a.direction.upper()} {a.asset}")
    print("=" * 56)
    print(f"  Market now : ${float(last['close']):,.2f} | weather: {weather['regime']}")
    print(f"  Entry      : ${entry:,.2f}"
          + ("  (your price)" if a.entry else "  (current market)"))
    print(f"  STOP-LOSS  : ${plan['stop_loss']:,.2f}   ← exit here if wrong")
    print(f"  TAKE-PROFIT: ${plan['take_profit']:,.2f}   ← target if right")
    print(f"  Buy/sell   : {plan['size_units']:.6f} units "
          f"(${plan['position_value']:,.2f} of your ${a.capital:,.0f})"
          + ("  [CAPPED at 25% of capital]" if plan['position_capped'] else ""))
    print(f"  If WRONG   : you lose ${plan['risk_money']:,.2f} "
          f"({plan['risk_money'] / a.capital * 100:.2f}% of capital)")
    print(f"  If RIGHT   : you gain ${plan['reward_money']:,.2f} "
          f"(reward:risk {plan['reward_risk_ratio']:.2f})")
    print("-" * 56)
    print("  Math, not advice. The pilot decides. Log what you do.")
    print("=" * 56)
