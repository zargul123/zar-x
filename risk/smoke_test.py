"""Risk compartment smoke test — the gate:
a live BTC long plan must have SL < entry < TP, risk == 1% of capital
(unless capped), and the configured reward:risk ratio."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from data.market_data import MarketData
    from risk.calculator import RiskCalculator
    from config import RISK_CONFIG

    df = MarketData().get_candles('BTC-USD', timeframe='4h', limit=100)
    if df is None or df.empty:
        sys.exit("GATE FAILED: no candles.")

    entry = float(df['close'].iloc[-1])
    capital = 1000.0
    plan = RiskCalculator().plan_trade(capital=capital, entry_price=entry,
                                       direction='long', df=df)
    if plan is None:
        sys.exit("GATE FAILED: plan_trade returned None.")

    if not (plan['stop_loss'] < entry < plan['take_profit']):
        sys.exit(f"GATE FAILED: level ordering wrong: {plan}")

    expected_rr = RISK_CONFIG['default_tp_atr'] / RISK_CONFIG['default_sl_atr']
    if abs(plan['reward_risk_ratio'] - expected_rr) > 0.01:
        sys.exit(f"GATE FAILED: RR {plan['reward_risk_ratio']:.3f} != {expected_rr:.3f}")

    if not plan['position_capped'] and abs(plan['risk_money'] - capital * RISK_CONFIG['risk_per_trade']) > 0.01:
        sys.exit(f"GATE FAILED: risk money {plan['risk_money']:.2f} != 1% of capital")

    print(f"✅ Live BTC long plan on ${capital:.0f} capital @ ${entry:,.2f}:")
    print(f"   SL ${plan['stop_loss']:,.2f} | TP ${plan['take_profit']:,.2f} | ATR ${plan['atr']:,.2f}")
    print(f"   Size {plan['size_units']:.6f} BTC (${plan['position_value']:,.2f}"
          f"{' — CAPPED' if plan['position_capped'] else ''})")
    print(f"   Risk ${plan['risk_money']:,.2f} → Reward ${plan['reward_money']:,.2f} "
          f"(R:R {plan['reward_risk_ratio']:.2f})")
    print("\n🎯 RISK GATE PASSED.")
