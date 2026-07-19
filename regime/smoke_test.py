"""Regime compartment smoke test — the gate:
live 4h reading returns a calibrated regime; an uncalibrated timeframe
answers 'Uncalibrated' (fail-honest) instead of guessing."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    from data.market_data import MarketData
    from indicators.technical import add_indicators
    from regime.vane import RegimeVane

    df = MarketData().get_candles('BTC-USD', timeframe='4h', limit=300)
    if df is None or df.empty:
        sys.exit("GATE FAILED: no candles.")
    df = add_indicators(df)

    vane = RegimeVane()
    reading = vane.read(df, timeframe='4h')
    if reading['regime'] not in ('Trending', 'Ranging', 'Chaotic'):
        sys.exit(f"GATE FAILED: 4h reading invalid: {reading}")
    if not reading['calibrated']:
        sys.exit("GATE FAILED: 4h should be calibrated.")

    uncal = vane.read(df, timeframe='1d')
    if uncal['regime'] != 'Uncalibrated':
        sys.exit(f"GATE FAILED: 1d should report Uncalibrated, got {uncal}")

    print(f"✅ 4h weather: {reading['regime']} "
          f"(entropy {reading['entropy']:.3f} vs dial 1.96 | ADX {reading['adx']:.1f})")
    print(f"✅ 1d honesty: {uncal['regime']} (no calibrated dial → no guessing)")
    print("\n🎯 REGIME GATE PASSED.")
