"""
Zar X journal compartment — the ship's black box (part 1: daily snapshots).

Each run appends one row per asset to journal/snapshots.csv recording what
the instruments said at that moment: price, trend state, RSI, ATR, weather.
Later runs can then be scored against reality ("Brief said UP on the 15th —
what actually happened?"). Records are evidence; evidence beats memory.

Fail-safe: an asset whose instruments are offline is skipped and reported;
the snapshot continues for the rest.
"""
import sys
import os
import csv
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ASSETS

SNAPSHOT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'snapshots.csv')
FIELDS = ['utc_time', 'asset', 'timeframe', 'close', 'trend', 'rsi',
          'atr', 'atr_pct', 'regime', 'entropy', 'adx']


def take_snapshot(timeframe='4h', candles=300) -> int:
    from data.market_data import MarketData
    from indicators.technical import add_indicators
    from regime.vane import RegimeVane

    md, vane = MarketData(), RegimeVane()
    new_file = not os.path.exists(SNAPSHOT_FILE)
    written = 0

    with open(SNAPSHOT_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')

        for asset in ASSETS:
            df = md.get_candles(asset, timeframe=timeframe, limit=candles)
            if df is None or df.empty:
                print(f"🔌 {asset}: offline — skipped in snapshot")
                continue
            df = add_indicators(df)
            last = df.iloc[-1]
            above50 = last['close'] > last['ema_50']
            above200 = last['close'] > last['ema_200']
            trend = 'UP' if (above50 and above200) else (
                    'DOWN' if (not above50 and not above200) else 'MIXED')
            weather = vane.read(df, timeframe=timeframe)
            writer.writerow({
                'utc_time': now, 'asset': asset, 'timeframe': timeframe,
                'close': f"{last['close']:.2f}", 'trend': trend,
                'rsi': f"{last['rsi']:.1f}", 'atr': f"{last['atr']:.2f}",
                'atr_pct': f"{last['atr'] / last['close'] * 100:.2f}",
                'regime': weather['regime'],
                'entropy': (f"{weather['entropy']:.3f}"
                            if weather['entropy'] is not None else ''),
                'adx': (f"{weather['adx']:.1f}"
                        if weather['adx'] is not None else ''),
            })
            written += 1
            print(f"📓 {asset}: recorded — ${last['close']:,.2f}, "
                  f"{trend}, {weather['regime']}")
    print(f"\n🗃️ {written} row(s) appended to {os.path.basename(SNAPSHOT_FILE)}")
    return written


if __name__ == '__main__':
    if take_snapshot() == 0:
        sys.exit("SNAPSHOT FAILED: nothing recorded.")
