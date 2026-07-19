"""Indicators compartment smoke test — the gate:
live BTC candles gain the full CORE_COLUMNS set with sane values."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from data.market_data import MarketData
    from indicators.technical import add_indicators, CORE_COLUMNS

    df = MarketData().get_candles('BTC-USD', timeframe='4h', limit=300)
    if df is None or df.empty:
        sys.exit("GATE FAILED: no candles from data compartment.")

    enriched = add_indicators(df)
    missing = [c for c in CORE_COLUMNS if c not in enriched.columns]
    if missing:
        sys.exit(f"GATE FAILED: missing columns {missing}")

    last = enriched.iloc[-1]
    if not (0 <= last['rsi'] <= 100):
        sys.exit(f"GATE FAILED: RSI out of range ({last['rsi']})")
    if last['atr'] <= 0:
        sys.exit(f"GATE FAILED: ATR not positive ({last['atr']})")

    print(f"✅ {len(enriched)} candles enriched with {len(CORE_COLUMNS)} core indicators")
    print(f"   RSI {last['rsi']:.1f} | ADX {last['adx']:.1f} | ATR ${last['atr']:.2f} "
          f"| EMA200 ${last['ema_200']:.2f} | close ${last['close']:.2f}")
    trend = "ABOVE" if last['close'] > last['ema_200'] else "BELOW"
    print(f"   Trend check: price {trend} EMA-200")
    print("\n🎯 INDICATORS GATE PASSED.")
