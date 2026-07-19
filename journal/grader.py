"""
Zar X journal compartment — the Grader (part 2 of the black box).
ROADMAP queue item #2, first half.

Reads every claim the instruments recorded in snapshots.csv, waits until
enough market has passed (24h = six 4h candles), then fetches what price
ACTUALLY did and scores the claim. Cold arithmetic, no feelings. Runs
daily inside the 09:05 ritual so the system checks itself.

v1 grades the TREND claim: 'UP' is correct if the close 6 candles later
is higher than at claim time; 'DOWN' if lower. 'MIXED' rows carry no
directional claim and are recorded but not scored.

Honest by design: rows younger than the grading horizon are reported as
"not yet gradable" — never guessed. Fail-safe like every part.
"""
import sys
import os
import csv
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SNAPSHOT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'snapshots.csv')
HORIZON_CANDLES = 6  # 6 x 4h = 24 hours of market before a claim is graded


def grade():
    from data.market_data import MarketData

    if not os.path.exists(SNAPSHOT_FILE):
        print("📓 No snapshots recorded yet.")
        return
    with open(SNAPSHOT_FILE, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("📓 Snapshot file is empty.")
        return

    md = MarketData()
    history = {}
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    horizon = timedelta(hours=4 * HORIZON_CANDLES)

    graded, correct, too_young, unscored = 0, 0, 0, 0
    per_asset = {}

    for row in rows:
        t = datetime.strptime(row['utc_time'], '%Y-%m-%d %H:%M')
        asset, trend = row['asset'], row['trend']
        if now - t < horizon:
            too_young += 1
            continue
        if trend == 'MIXED':
            unscored += 1
            continue
        if asset not in history:
            df = md.get_candles(asset, timeframe='4h', limit=500)
            history[asset] = df if (df is not None and not df.empty) else None
            if history[asset] is None:
                print(f"🔌 {asset}: data offline — its rows skipped this run")
        df = history[asset]
        if df is None:
            continue

        idx = df.index.searchsorted(t, side='right') - 1
        if idx < 0 or idx + HORIZON_CANDLES >= len(df):
            too_young += 1
            continue
        p0 = float(df['close'].iloc[idx])
        p1 = float(df['close'].iloc[idx + HORIZON_CANDLES])
        went_up = p1 > p0
        is_correct = (trend == 'UP' and went_up) or (trend == 'DOWN' and not went_up)

        graded += 1
        correct += int(is_correct)
        a = per_asset.setdefault(asset, {'graded': 0, 'correct': 0})
        a['graded'] += 1
        a['correct'] += int(is_correct)

    print("=" * 56)
    print("  ZAR X GRADER — trend-claim report card")
    print("=" * 56)
    print(f"  Claims on file      : {len(rows)}")
    print(f"  Not yet gradable    : {too_young} (younger than 24h of market)")
    print(f"  No directional claim: {unscored} (MIXED)")
    print(f"  GRADED              : {graded}")
    if graded:
        print(f"  CORRECT             : {correct}  ({correct / graded * 100:.1f}%)")
        for asset, a in sorted(per_asset.items()):
            print(f"    {asset}: {a['correct']}/{a['graded']} "
                  f"({a['correct'] / a['graded'] * 100:.0f}%)")
        print("  (Reading law: accuracy alone is not edge — payoff and")
        print("   costs decide money. This grades honesty, not profit.)")
    else:
        print("  Verdict: come back after the market has had 24h to answer.")
    print("=" * 56)


if __name__ == '__main__':
    grade()
