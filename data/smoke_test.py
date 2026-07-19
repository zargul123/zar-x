"""Data compartment smoke test — Phase 0 gate:
'one command prints live BTC/ETH/SOL candles'. Exit code 0 = gate passed."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from data.market_data import MarketData
    from config import ASSETS

    md = MarketData()
    failures = 0
    for asset in ASSETS:
        df = md.get_candles(asset, timeframe='4h', limit=3)
        if df is None or df.empty:
            print(f"❌ {asset}: no data")
            failures += 1
            continue
        last = df.iloc[-1]
        print(f"✅ {asset}: {len(df)} candles | latest {df.index[-1]} "
              f"close ${last['close']:.2f}")
    if failures:
        sys.exit(f"GATE FAILED: {failures} asset(s) offline.")
    print("\n🎯 PHASE 0 GATE PASSED: data compartment alive for all assets.")
