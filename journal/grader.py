"""
Zar X journal compartment — the Grader (part 2 of the black box).
ROADMAP queue item #2, first half.

Reads every claim the instruments recorded in the black box, waits until
enough market has passed (24h = six 4h candles), then fetches what price
ACTUALLY did and scores the claim. Cold arithmetic, no feelings. Runs
daily inside the 09:05 ritual so the system checks itself.

v2 upgrades (architect review, recorded 2026-07-20):
- Reads ALL notebooks (legacy snapshots.csv + snapshots_local.csv +
  snapshots_cloud.csv) and merges them.
- CANDLE-IDENTITY RULE: asset + timeframe + candle-open-time = ONE claim.
  Manual test-fires and laptop/cloud double coverage no longer inflate
  the report card; extra rows for the same candle are discarded.
- ALWAYS-UP PARROT baseline: a parrot that says UP every time scores
  55-60% in an up-drifting market with zero skill. The system's verdict
  is now "beats the parrot", never "beats a coin flip".

v1 grading rule unchanged: 'UP' is correct if the close 6 candles later
is higher than at claim time; 'DOWN' if lower. 'MIXED' rows carry no
directional claim and are recorded but not scored (the parrot still
takes those exams — it always has an answer).

Honest by design: rows younger than the grading horizon are reported as
"not yet gradable" — never guessed. Fail-safe like every part.
"""
import sys
import os
import csv
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_FILES = ['snapshots.csv', 'snapshots_local.csv', 'snapshots_cloud.csv']
HORIZON_CANDLES = 6  # 6 x 4h = 24 hours of market before a claim is graded


def _load_claims():
    """All rows from every notebook, de-duplicated by candle identity.

    Candle identity: asset + timeframe + the open-time of the candle the
    snapshot was taken in (utc_time floored to the timeframe grid). The
    earliest row for an identity wins; later duplicates are discarded.
    """
    rows = []
    for name in SNAPSHOT_FILES:
        path = os.path.join(_JOURNAL_DIR, name)
        if not os.path.exists(path):
            continue
        with open(path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                row['_source'] = name
                rows.append(row)

    total = len(rows)
    claims = {}
    for row in rows:
        try:
            t = datetime.strptime(row['utc_time'], '%Y-%m-%d %H:%M')
            tf_hours = int(row.get('timeframe', '4h').rstrip('h'))
        except (ValueError, KeyError):
            continue  # malformed row: not evidence, not counted
        candle_open = t.replace(minute=0, second=0,
                                hour=(t.hour // tf_hours) * tf_hours)
        identity = (row['asset'], row.get('timeframe', '4h'), candle_open)
        if identity not in claims or t < claims[identity][0]:
            claims[identity] = (t, row)

    kept = [(identity[2], row) for identity, (t, row) in
            sorted(claims.items(), key=lambda kv: (kv[1][0], kv[0]))]
    return kept, total


def grade():
    from data.market_data import MarketData

    claims, raw_total = _load_claims()
    if not claims:
        print("📓 No snapshots recorded yet.")
        return

    md = MarketData()
    history = {}
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    horizon = timedelta(hours=4 * HORIZON_CANDLES)

    graded, correct, too_young, unscored = 0, 0, 0, 0
    parrot_exams, parrot_correct = 0, 0
    per_asset = {}

    for candle_open, row in claims:
        t = datetime.strptime(row['utc_time'], '%Y-%m-%d %H:%M')
        asset, trend = row['asset'], row['trend']
        if now - t < horizon:
            too_young += 1
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

        # The parrot sits the same exam on every gradable candle: "UP".
        parrot_exams += 1
        parrot_correct += int(went_up)

        if trend == 'MIXED':
            unscored += 1
            continue
        is_correct = (trend == 'UP' and went_up) or (trend == 'DOWN' and not went_up)

        graded += 1
        correct += int(is_correct)
        a = per_asset.setdefault(asset, {'graded': 0, 'correct': 0})
        a['graded'] += 1
        a['correct'] += int(is_correct)

    dupes = raw_total - len(claims)
    print("=" * 56)
    print("  ZAR X GRADER — trend-claim report card (v2)")
    print("=" * 56)
    print(f"  Rows in all notebooks: {raw_total} "
          f"({dupes} duplicate candle-claims discarded)")
    print(f"  Unique claims        : {len(claims)}")
    print(f"  Not yet gradable     : {too_young} (younger than 24h of market)")
    print(f"  No directional claim : {unscored} (MIXED)")
    print(f"  GRADED               : {graded}")
    if graded:
        acc = correct / graded * 100
        print(f"  CORRECT              : {correct}  ({acc:.1f}%)")
        for asset, a in sorted(per_asset.items()):
            print(f"    {asset}: {a['correct']}/{a['graded']} "
                  f"({a['correct'] / a['graded'] * 100:.0f}%)")
        if parrot_exams:
            pacc = parrot_correct / parrot_exams * 100
            print(f"  ALWAYS-UP PARROT     : {parrot_correct}/{parrot_exams} "
                  f"({pacc:.1f}%)  <- the bar to beat")
            verdict = ("BEATS the parrot" if acc > pacc else
                       "does NOT beat the parrot")
            print(f"  Verdict              : system {verdict} "
                  f"({acc:.1f}% vs {pacc:.1f}%)")
            print("  (In an up-drifting market the parrot scores high with")
            print("   zero skill. Beating the COIN means nothing; beating")
            print("   the PARROT is the honest bar. Small samples lie.)")
        print("  (Reading law: accuracy alone is not edge — payoff and")
        print("   costs decide money. This grades honesty, not profit.)")
    else:
        print("  Verdict: come back after the market has had 24h to answer.")
    print("=" * 56)


if __name__ == '__main__':
    grade()
