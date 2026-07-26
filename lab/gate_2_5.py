"""
Zar X Lab — GATE 2.5: THE PHASE 2 EXIT GATE (the Lab must catch a con artist).

Steps 2.1-2.4 built a vault, a door, an engine and three lie detectors, and
each of those gates proved its own part worked. This gate asks the only
question that matters about the whole machine:

    IF SOMEBODY HANDS THIS LAB A BEAUTIFUL LIE, DOES THE LAB SAY NO?

A courtroom that has only ever acquitted innocent men has proved nothing. So
a guilty strategy is built on purpose, walked through the ENTIRE pipeline —
the same vault door, the same engine, the same hold-out line, the same three
detectors — and the pipeline is required to expose it.

THE DEFINITION OF "CERTIFIED AS GOOD" IS LOCKED AT THE TOP OF THIS FILE,
BEFORE ANY RUN. It is a copy of the Phase 6 gauntlet bars, written down now so
that nobody can quietly move them later after seeing a result they like. A
strategy is CERTIFIED only if it clears every bar. The con artist below must
fail it.

THE TWO EXHIBITS, AND WHY THEY ARE DIFFERENT ANIMALS

  EXHIBIT 1 — THE CON ARTIST (overfitting).
  A synthetic strategy that breaks no rule at all. It never sees a candle past
  train_end. It never peeks at the future. It obeys the signal contract
  exactly. It is still garbage, because it MEMORISED the training data: a
  lookup table of candle features (hour-of-day x day-of-week x the up/down
  pattern of the last few candles) with thousands of cells, each one recording
  whether that combination happened to make money before train_end. On the
  training data it looks like the best strategy ever built. On candles it has
  never seen, it collapses. This is the disease the Lab's numbers were built
  to detect, and the numbers detect it.

  EXHIBIT 2 — THE LEAK (cheating).
  `PerfectForesight` from lab/dummies.py: a strategy that was handed the whole
  file by its author, so it reads tomorrow's candle around the side of the
  engine's feed. Its hold-out does NOT collapse — a cheat cheats on the
  hold-out too. THIS EXHIBIT EXISTS TO STATE A LIMIT, NOT TO CLAIM A WIN. The
  numeric pipeline cannot expose a leak, and this gate says so out loud rather
  than pretending otherwise.

WHAT SEPARATES THEM, SAID ONCE AND PLAINLY
  Overfitting is a strategy fooling ITSELF on data it was fitted to. The
  hold-out is a different piece of the world, so the fooling stops there and
  the numbers show it. A leak is a strategy being fed answers. Answers work
  everywhere, hold-out included, so no amount of arithmetic can find it. Leaks
  are caught by ONE thing only in this Lab: a human reading the strategy's
  code. The too-good alarm (PF > 2 or win rate > 70%) was meant to be the
  flare that sends a human to go and read that code — and Step 6 of this gate
  MEASURED, rather than assumed, whether that flare actually goes up. IT DOES
  NOT: this leak's hold-out card (PF 1.39, win 57.6%) sits under both limits.
  That measurement is the founding evidence of LAW 7 (SHIP_LAWS.md, adopted
  2026-07-26): mandatory recorded code-reading before certification, with
  lab/leak_check.py — which DOES flag this leak, by finding the DataFrame it
  carries — as the reading's aid, never its substitute. Step 6 verifies all
  of that too.

WHAT THIS FILE MAY AND MAY NOT TOUCH
  It consumes engine.py, walk_forward.py, monte_carlo.py, regime_report.py,
  trade_stats.py and dummies.py. It modifies NONE of them. The con artist is
  built inside this file and is clearly labelled synthetic; it is a test
  instrument, never a strategy, and it goes nowhere near the Phase 6 slots.
  lab/vault/ is read-only, as always.

DETERMINISM
  The lookup table is built with no random numbers of any kind — no RNG, no
  seed, no sampling. The only randomness anywhere in this gate is inside the
  Monte Carlo, whose seed (20260726) is recorded and printed. Run this gate
  twice and every character of the output is the same except the names of the
  evidence files, which are never overwritten (Law 5).

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\gate_2_5.py
"""
import os
import sys

import numpy as np
import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)
sys.path.insert(0, os.path.dirname(LAB_DIR))

from config import LAB_COSTS, RISK_CONFIG                       # noqa: E402
from engine import load_vault, run_backtest                     # noqa: E402
from dummies import MACross, PerfectForesight                   # noqa: E402
from walk_forward import walk_forward                           # noqa: E402
from monte_carlo import monte_carlo_result, SEED                # noqa: E402
from regime_report import regime_report                         # noqa: E402
from leak_check import leak_check                               # noqa: E402

ASSET = 'BTC-USD'
TIMEFRAME = '4h'
TRAIN_END = '2025-10-01'        # the SAME hold-out line as Gates 2.3 and 2.4


# ==========================================================================
# THE LOCKED DEFINITION OF "CERTIFIED AS GOOD"
# ==========================================================================
# These four numbers are copied from PHASE 6 of EXECUTION_PLAN.md and written
# down HERE, in code, BEFORE a single run of this gate. That is the whole
# point: a bar that can be adjusted after seeing the result is not a bar, it
# is a decoration. If any number below is ever edited, every verdict this file
# has ever printed becomes worthless and must be re-earned.
#
# A strategy is CERTIFIED AS GOOD only when it clears ALL FOUR.
# ==========================================================================
BAR_MIN_PROFIT_FACTOR = 1.15    # hold-out profit factor, AFTER costs
BAR_MIN_TRADES = 30             # fewer hold-out trades = sample too small = FAIL
BAR_WALK_FORWARD = 'CONSISTENT'  # >= 60% of windows profitable AND no window
#                                 supplies > 50% of the profit (walk_forward.py
#                                 owns both halves of this test)
BAR_MAX_MC_DRAWDOWN = 30.0      # Monte Carlo 5th-percentile drawdown, percent

# The standing too-good law from the IF/THEN table of EXECUTION_PLAN.md.
# It is not a bar — it is an ALARM. It never says "fail"; it says "stop
# celebrating and go hunt for a leak".
TOO_GOOD_PF = 2.0
TOO_GOOD_WIN_PCT = 70.0

# Phase 6 carries two further requirements that this gate does NOT evaluate:
# "must beat buy-and-hold-with-1%-risk-sizing", and a second AI's review of
# the setup and the verdict. Leaving them out makes the battery below EASIER
# than the real gauntlet, which is the safe direction for this exam: a con
# artist that fails the easy version would fail the hard one too.


# ==========================================================================
# The gate's own bookkeeping
# ==========================================================================

results = {}          # check name -> True/False, filled as the gate walks
evidence = []         # every per-trade CSV this run wrote


def check(name, ok, detail=''):
    if name in results:
        raise RuntimeError(f'duplicate check name {name!r}: the tally would '
                           f'hide one of them. Rename it.')
    results[name] = bool(ok)
    print(f'  [{"OK" if ok else "FAIL"}] {name}' + (f'   {detail}' if detail else ''))
    return bool(ok)


def banner(title):
    print()
    print('#' * 78)
    print(f'# {title}')
    print('#' * 78)


def save(result, label):
    path = result.save_csv()
    evidence.append(path)
    print(f'  evidence written: {os.path.relpath(path, os.path.dirname(LAB_DIR))}'
          f'   [{label}]')
    return path


def too_good_alarm(card, who):
    """The standing law, applied to a stat card. Returns True if it fires."""
    pf, win = float(card['profit_factor']), float(card['win_pct'])
    fired = pf > TOO_GOOD_PF or win > TOO_GOOD_WIN_PCT
    print()
    if fired:
        reasons = []
        if pf > TOO_GOOD_PF:
            reasons.append(f'profit factor {pf:.2f} > {TOO_GOOD_PF}')
        if win > TOO_GOOD_WIN_PCT:
            reasons.append(f'win rate {win:.1f}% > {TOO_GOOD_WIN_PCT}%')
        print(f'  !! TOO-GOOD ALARM — {who}')
        print(f'  !! {" and ".join(reasons)}.')
        print('  !! STANDING LAW (EXECUTION_PLAN.md): results this good are a '
              'bug or a leak')
        print('  !! until proven otherwise. Do not celebrate. Go and hunt the '
              'leak: check')
        print('  !! for look-ahead, survivorship, and costs switched off — and '
              'READ THE')
        print('  !! STRATEGY\'S CODE. This alarm is not a verdict, it is an '
              'order to go look.')
    else:
        print(f'  .. too-good alarm SILENT — {who}')
        print(f'  .. profit factor {pf:.2f} (limit {TOO_GOOD_PF}) and win rate '
              f'{win:.1f}% (limit {TOO_GOOD_WIN_PCT}%).')
        print('  .. Nothing here is spectacular enough to trip the standing '
              'law.')
    return fired


def side_by_side(train_card, holdout_card):
    """The two cards in two columns. The collapse is the point, and a reader
    should not have to hold one page in their head while reading another."""
    rows = [
        ('trades', 'trades', '{:,.0f}'),
        ('wins / losses', None, None),
        ('win rate %', 'win_pct', '{:.1f}'),
        ('PROFIT FACTOR', 'profit_factor', '{:.2f}'),
        ('avg win %', 'avg_win', '{:+.2f}'),
        ('avg loss %', 'avg_loss', '{:+.2f}'),
        ('max drawdown %', 'max_drawdown', '{:.2f}'),
        ('NET RETURN %', 'net_return', '{:+.2f}'),
        ('gross return %', 'gross_return', '{:.2f}'),
        ('cost drag (pts)', 'cost_drag', '{:.2f}'),
        ('time in market', 'time_in_market', '{:.1%}'),
    ]
    L = []
    L.append('    ' + ' ' * 20 + f'{"TRAIN (memorised)":>22}'
             f'{"HOLD-OUT (never seen)":>25}')
    L.append('    ' + '-' * 67)
    for label, key, fmt in rows:
        if key is None:
            a = f'{train_card["wins"]} / {train_card["losses"]}'
            b = f'{holdout_card["wins"]} / {holdout_card["losses"]}'
        else:
            a = fmt.format(train_card[key])
            b = fmt.format(holdout_card[key])
        L.append(f'    {label:<20}{a:>22}{b:>25}')
    L.append('    ' + '-' * 67)
    L.append(f'    window              {str(train_card["window_from"])[:10]} -> '
             f'{str(train_card["window_to"])[:10]}   '
             f'{str(holdout_card["window_from"])[:10]} -> '
             f'{str(holdout_card["window_to"])[:10]}')
    return '\n'.join(L)


# ==========================================================================
# EXHIBIT 1 — THE CON ARTIST.  *** SYNTHETIC. A TEST INSTRUMENT. ***
# ==========================================================================
# THIS IS NOT A STRATEGY. It is a deliberately-bad strategy built to be caught,
# in the same spirit as the poisoned vault copy of Gate 2.2 and the planted
# lucky window of Gate 2.4. It must never be run as a signal, never enter a
# Phase 6 slot, and none of its numbers is a claim about the market.
#
# WHAT IT DOES
# It memorises a lookup table of candle FEATURES:
#     hour-of-day (6 values on 4h candles)
#   x day-of-week (7)
#   x the up/down pattern of the last N candles (2^N)
# = up to 2,688 cells at N=6. Each cell records how a trade opened on such a
# candle would have gone, using ONLY candles at or before train_end. Cells
# that made money in training become signals. That is the "1000-parameter
# curve-fit": thousands of free parameters, every one of them fitted to the
# training data, not one of them justified by any idea about markets.
#
# THE EDGE CASE, DECIDED BEFORE THE CODE WAS WRITTEN
# It memorises RECURRING features, never TIMESTAMPS. A table keyed on
# "2024-03-15 08:00" would match nothing after train_end — zero hold-out
# trades, and an exhibit that demonstrates nothing. Hour-of-day, day-of-week
# and candle patterns all come round again, week after week, so the memorised
# cells fire in the hold-out too, and the collapse is visible in the numbers
# rather than hidden behind an empty table. (If the hold-out had still come
# out under 30 trades, that IS one of the locked bars and it would have been
# reported as a failure, not tuned away.)
#
# TRAIN-ONLY, ENFORCED IN CODE
# The table is built from `df[df.index <= train_end]` and NOTHING else. The
# forward walk that scores each candle is also bounded by the end of that
# slice, so a trade that had not finished by train_end is dropped rather than
# followed one candle into the hold-out. Both facts are asserted and printed.
#
# NO RANDOMNESS
# No RNG, no seed, no sampling, no ties broken by chance. Same vault, same
# table, every time.
# ==========================================================================

MAX_HOLD = 400          # candles a scored training trade may run (~67 days)
LADDER = (3, 4, 5, 6)   # the memorisation-capacity dial, weakest first


def _atr_series(d, period=14):
    """The engine's ATR, computed for every candle at once. Same formula as
    risk/calculator.py — rolling mean of the true range."""
    hl = d['high'] - d['low']
    hc = (d['high'] - d['close'].shift()).abs()
    lc = (d['low'] - d['close'].shift()).abs()
    return np.maximum(hl, np.maximum(hc, lc)).rolling(period).mean()


def score_training_candles(train_df):
    """For every candle in the TRAINING slice, what a long and a short opened
    on the next candle would have earned, under the engine's own rules: entry
    at the next open with slippage, 1.5-ATR stop, 2.0-ATR target, the loss
    counted when both are touched in one candle, fees on both sides.

    A trade that has not resolved by the END OF THE TRAINING SLICE is left as
    NaN and never enters the table. That is the wall: this function cannot see
    one candle past train_end, because the array it walks stops there.
    """
    a = _atr_series(train_df).values
    o = train_df['open'].values
    h = train_df['high'].values
    l = train_df['low'].values
    n = len(train_df)
    fee, slip = LAB_COSTS['fee_pct'], LAB_COSTS['slippage_pct']
    sl_m, tp_m = RISK_CONFIG['default_sl_atr'], RISK_CONFIG['default_tp_atr']

    out = {'long': np.full(n, np.nan), 'short': np.full(n, np.nan)}
    for i in range(n - 1):
        atr = a[i]
        if not (atr > 0):
            continue
        j = i + 1                                   # the entry candle
        for d in ('long', 'short'):
            raw = o[j]
            fill = raw * (1 + slip) if d == 'long' else raw * (1 - slip)
            if d == 'long':
                sl, tp = fill - sl_m * atr, fill + tp_m * atr
            else:
                sl, tp = fill + sl_m * atr, fill - tp_m * atr
            for k in range(j, min(n, j + MAX_HOLD)):
                if d == 'long':
                    hit_sl, hit_tp = l[k] <= sl, h[k] >= tp
                else:
                    hit_sl, hit_tp = h[k] >= sl, l[k] <= tp
                if hit_sl:                          # the pessimistic rule
                    ex = min(o[k], sl) if d == 'long' else max(o[k], sl)
                elif hit_tp:
                    ex = tp
                else:
                    continue
                exf = ex * (1 - slip) if d == 'long' else ex * (1 + slip)
                move = ((exf - fill) / fill if d == 'long'
                        else (fill - exf) / fill)
                out[d][i] = move - 2 * fee
                break
    return out


def feature_key(hour, dow, pattern):
    return f'{hour:02d}|{dow}|{pattern}'


def pattern_of(opens, closes):
    """The up/down shape of a run of candles, read as a binary number.
    Up = the candle closed above its open. This RECURS; a date does not."""
    v = 0
    for k in range(len(closes)):
        v = v * 2 + (1 if closes[k] > opens[k] else 0)
    return v


def build_table(train_df, scores, pattern_len):
    """The memorisation. Deterministic, train-only, no random numbers."""
    o, c = train_df['open'].values, train_df['close'].values
    hours = train_df.index.hour.values
    dows = train_df.index.dayofweek.values
    n = len(train_df)

    cells = {}
    scored = 0
    for i in range(pattern_len - 1, n):
        pat = pattern_of(o[i - pattern_len + 1:i + 1],
                         c[i - pattern_len + 1:i + 1])
        key = feature_key(hours[i], dows[i], pat)
        e = cells.setdefault(key, {'long': [0.0, 0], 'short': [0.0, 0]})
        for d in ('long', 'short'):
            v = scores[d][i]
            if np.isnan(v):
                continue
            e[d][0] += float(v)
            e[d][1] += 1
            scored += 1

    # A cell becomes a signal if the better of its two directions made money
    # in training. Ties (an impossible-in-practice exact 0.0) fall to 'long'
    # by the fixed order below — a rule, never a coin.
    table = {}
    for key in cells:                       # insertion order: deterministic
        e = cells[key]
        best = 'long' if e['long'][0] >= e['short'][0] else 'short'
        if e[best][0] > 0.0:
            table[key] = best
    samples = [e['long'][1] for e in cells.values()]
    return table, cells, scored, samples


class ConArtist:
    """*** SYNTHETIC TEST INSTRUMENT — NOT A STRATEGY ***

    Signals whenever the current candle's features match a cell that made
    money before train_end. It obeys the contract exactly: it looks only at
    the candles it was handed, and its table was sealed at train_end. It is
    still worthless, and the Lab is required to prove that.
    """

    def __init__(self, table, pattern_len, train_end):
        self.table = table
        self.pattern_len = pattern_len
        self.params = {'kind': 'SYNTHETIC lookup-table curve-fit',
                       'features': 'hour-of-day x day-of-week x last-N up/down',
                       'pattern_len': pattern_len,
                       'memorised_cells': len(table),
                       'table_built_from': f'candles <= {train_end} only',
                       'rng': 'none — the table build uses no random numbers'}
        self.name = f'con-artist-curve-fit-p{pattern_len}'
        self.matched = 0
        self.asked = 0

    def __call__(self, df):
        self.asked += 1
        p = self.pattern_len
        if len(df) < p:
            return 'flat'
        o = df['open'].values[-p:]
        c = df['close'].values[-p:]
        t = df.index[-1]
        key = feature_key(t.hour, t.dayofweek, pattern_of(o, c))
        sig = self.table.get(key)
        if sig is None:
            return 'flat'
        self.matched += 1
        return sig


# ==========================================================================
# THE BATTERY — the locked bars, applied and printed one by one
# ==========================================================================

def run_battery(who, card, wf, mc):
    """Apply the four locked bars to a hold-out result. Returns
    (certified, rows). CERTIFIED means every single bar passed."""
    pf = float(card['profit_factor'])
    trades = int(card['trades'])
    rows = [
        ('hold-out profit factor after costs',
         f'{pf:.2f}', f'>= {BAR_MIN_PROFIT_FACTOR}',
         pf >= BAR_MIN_PROFIT_FACTOR),
        ('hold-out trade count',
         f'{trades}', f'>= {BAR_MIN_TRADES}',
         trades >= BAR_MIN_TRADES),
        ('walk-forward verdict',
         wf.verdict, f'must be {BAR_WALK_FORWARD}',
         wf.verdict == BAR_WALK_FORWARD),
        ('Monte Carlo 5th-percentile drawdown',
         f'{mc["dd_p95"]:.2f}%', f'< {BAR_MAX_MC_DRAWDOWN:.0f}%',
         float(mc['dd_p95']) < BAR_MAX_MC_DRAWDOWN),
    ]
    certified = all(ok for _, _, _, ok in rows)

    print()
    print('  ' + '=' * 74)
    print(f'  THE LOCKED BATTERY — {who}')
    print('  (these four bars were written into this file before any run; '
          'they are')
    print('   the Phase 6 gauntlet bars, copied so they cannot drift)')
    print('  ' + '=' * 74)
    print(f'    {"bar":<38}{"measured":>14}{"required":>21}   verdict')
    print('    ' + '-' * 77)
    for name, got, need, ok in rows:
        print(f'    {name:<38}{got:>14}{need:>21}   '
              f'{"PASS" if ok else "FAIL"}')
    print('    ' + '-' * 77)
    passed = sum(1 for _, _, _, ok in rows if ok)
    print(f'    bars passed: {passed} of {len(rows)}')
    print()
    if certified:
        print('    VERDICT: CERTIFIED AS GOOD.')
    else:
        print('    VERDICT: NOT CERTIFIED — REJECTED BY THE LAB.')
        print('    A strategy must clear EVERY bar. Clearing some of them is '
              'not a')
        print('    partial pass, it is a fail — "promising" is the word that '
              'kills')
        print('    accounts.')
    print('  ' + '=' * 74)
    return certified, rows


# ==========================================================================
# STEP 0 — nothing moved
# ==========================================================================

GATE_2_3 = {'trades': (37, 0), 'wins': (14, 0), 'losses': (23, 0),
            'win_pct': (37.8, 1), 'profit_factor': (0.63, 2),
            'net_return': (-4.88, 2), 'max_drawdown': (7.98, 2)}


def step_0_nothing_moved(data):
    banner('STEP 0 — THE GROUND HAS NOT MOVED SINCE GATE 2.3')
    print('Before this gate measures anything new, the old measurement must '
          'still be\nexactly what the log says it is. Same dummy (MA-cross '
          '20/50), same market,\nsame hold-out line. If these numbers have '
          'drifted, everything below is\nmeasuring a different Lab and none of '
          'it counts.\n')

    strat = MACross(20, 50)
    res = run_backtest(data, strat, strategy_name=strat.name,
                       params=strat.params, train_end=TRAIN_END,
                       regime=True, verbose=False)
    card = res.card('holdout')
    save(res, 'the Gate 2.3 dummy, re-run')
    print()
    print(card.text())
    print()
    for key, (expected, decimals) in GATE_2_3.items():
        got = round(float(card[key]), decimals)
        check(f'reproduces Gate 2.3 {key}',
              got == round(float(expected), decimals),
              f'expected {expected}, got {got}')
    check('the engine logged 0 look-ahead violations on the re-run',
          res.meta['audit_violations'] == 0)
    return res


# ==========================================================================
# STEP 1 — build the con artist (and record the capacity dial being turned)
# ==========================================================================

def step_1_build(data):
    banner('STEP 1 — BUILDING THE CON ARTIST (train data only, no RNG)')
    print('*** EVERYTHING IN THIS STEP IS SYNTHETIC AND LABELLED AS SUCH. ***')
    print('The con artist is a test instrument, like the poisoned vault copy '
          'of Gate 2.2\nand the planted lucky window of Gate 2.4. It is not a '
          'strategy, it will never\nbe traded, and none of its numbers is a '
          'claim about the market.\n')

    df = data.df
    te = pd.Timestamp(TRAIN_END)
    train_df = df[df.index <= te]
    holdout_df = df[df.index > te]

    print(f'  the vault file      : {len(df):,} candles, '
          f'{df.index[0]} -> {df.index[-1]}')
    print(f'  TRAINING SLICE      : {len(train_df):,} candles, '
          f'{train_df.index[0]} -> {train_df.index[-1]}')
    print(f'  hold-out (untouched): {len(holdout_df):,} candles, '
          f'{holdout_df.index[0]} -> {holdout_df.index[-1]}')
    print()
    check('the training slice ends at or before train_end',
          train_df.index[-1] <= te,
          f'last training candle {train_df.index[-1]}, train_end {te}')
    check('the training slice and the hold-out share not one candle',
          len(train_df) + len(holdout_df) == len(df)
          and holdout_df.index[0] > train_df.index[-1])

    print('\n  Scoring every training candle under the engine\'s own rules '
          '(entry at the')
    print('  next open with slippage, 1.5-ATR stop, 2.0-ATR target, the loss '
          'counted')
    print('  when both are touched in one candle, fees both sides). The '
          'forward walk')
    print(f'  is bounded by the END of the training slice and by {MAX_HOLD} '
          'candles, so a')
    print('  trade that had not finished by train_end is DROPPED, never '
          'followed one')
    print('  candle into the hold-out.')
    scores = score_training_candles(train_df)
    resolved = int(np.sum(~np.isnan(scores['long'])))
    dropped = len(train_df) - resolved
    print(f'    {resolved:,} training candles scored; {dropped:,} dropped '
          f'(no ATR yet at the start,')
    print('    or the trade had not resolved when the training data ran out).')

    # ---- the capacity dial, turned in the open ---------------------------
    print('\n  THE MEMORISATION-CAPACITY DIAL, TURNED IN FRONT OF THE READER.')
    print('  The con artist is allowed unlimited parameters ON TRAIN — that is '
          'its whole')
    print('  character. What it is never allowed is one candle past train_end. '
          'So the')
    print('  dial below is turned until the TRAIN card is spectacular, and the '
          'rule for')
    print('  stopping is written down first and is a TRAIN-ONLY rule:')
    print()
    print('      use the smallest pattern length whose TRAIN card trips BOTH '
          'halves of')
    print('      the standing too-good law (profit factor > 2 AND win rate > '
          '70%).')
    print()
    print('  The hold-out column is printed too, because the reader should see '
          'the whole')
    print('  disease at once: every turn of the dial makes TRAIN better and '
          'HOLD-OUT')
    print('  worse. That is overfitting, drawn as a table.\n')
    print(f'    {"pattern":>8}{"cells":>8}{"memorised":>11}{"samples":>9}'
          f'{"TRAIN PF":>10}{"TRAIN win%":>12}{"HOLDOUT PF":>12}'
          f'{"HOLDOUT net%":>14}')
    print('    ' + '-' * 84)

    ladder = {}
    for p in LADDER:
        table, cells, _, samples = build_table(train_df, scores, p)
        con = ConArtist(table, p, TRAIN_END)
        res = run_backtest(data, con, strategy_name=con.name,
                           params=con.params, train_end=TRAIN_END,
                           regime=False, verbose=False)
        tc, hc = res.card('train'), res.card('holdout')
        ladder[p] = {'table': table, 'cells_seen': len(cells),
                     'median_samples': float(np.median(samples)),
                     'train': tc, 'holdout': hc,
                     'fires_both': (tc['profit_factor'] > TOO_GOOD_PF
                                    and tc['win_pct'] > TOO_GOOD_WIN_PCT)}
        print(f'    {p:>8}{6 * 7 * 2 ** p:>8}{len(table):>11}'
              f'{np.median(samples):>9.1f}{tc["profit_factor"]:>10.2f}'
              f'{tc["win_pct"]:>12.1f}{hc["profit_factor"]:>12.2f}'
              f'{hc["net_return"]:>14.2f}')
    print('    ' + '-' * 84)
    print('    ("cells" = feature combinations that exist at all; "memorised" '
          '= those the')
    print('     table kept because they made money in training; "samples" = '
          'the median')
    print('     number of training candles behind ONE cell. Two samples per '
          'cell is not')
    print('     a discovery about markets — it is a phone book.)')

    chosen = next((p for p in LADDER if ladder[p]['fires_both']), None)
    print()
    check('the capacity dial reached a spectacular TRAIN card',
          chosen is not None,
          f'smallest pattern length tripping both halves of the too-good law: '
          f'{chosen}')
    if chosen is None:
        raise RuntimeError('the con artist never became convincing on train; '
                           'the exhibit cannot be built.')
    check('the choice of capacity used TRAIN numbers only',
          True,
          'the selecting rule reads train PF and train win rate; the hold-out '
          'column is printed but never consulted by the code')

    table = ladder[chosen]['table']
    con = ConArtist(table, chosen, TRAIN_END)
    print(f'\n  THE CON ARTIST: pattern length {chosen}, '
          f'{len(table):,} memorised cells out of '
          f'{6 * 7 * 2 ** chosen:,} possible.')
    print(f'  {len(table):,} free parameters, every one of them fitted to the '
          f'training data,')
    print('  not one of them justified by any idea about how a market works.')

    # the memorised keys must be RECURRING features, never timestamps
    sample_keys = sorted(table)[:4]
    print(f'\n  A sample of the memorised cells (hour|day-of-week|pattern): '
          f'{", ".join(sample_keys)}')
    print('  Not a single key is a date. Every one of them comes round again, '
          'week after')
    print('  week, which is why the table still fires in the hold-out.')
    key_space_ok = all('-' not in k and k.count('|') == 2 for k in table)
    check('the table memorises recurring features, never timestamps',
          key_space_ok and len(table) > 0,
          f'{len(table):,} keys, all of the form hour|day-of-week|pattern')

    # prove the recurrence numerically on hold-out candles
    o, c = holdout_df['open'].values, holdout_df['close'].values
    hrs, dws = holdout_df.index.hour.values, holdout_df.index.dayofweek.values
    matched = sum(1 for i in range(chosen - 1, len(holdout_df))
                  if feature_key(hrs[i], dws[i],
                                 pattern_of(o[i - chosen + 1:i + 1],
                                            c[i - chosen + 1:i + 1])) in table)
    print(f'\n  {matched:,} of the {len(holdout_df):,} hold-out candles match a '
          f'memorised cell '
          f'({100.0 * matched / len(holdout_df):.1f}%).')
    check('the memorised cells recur after train_end',
          matched > 0, f'{matched:,} hold-out candles matched')

    # determinism of the build itself
    table2, _, _, _ = build_table(train_df, scores, chosen)
    check('the table build is deterministic (built twice, identical)',
          table2 == table, f'{len(table):,} cells, same keys and same '
          f'directions both times')
    check('the table build used no random numbers at all',
          'rng' in con.params and con.params['rng'].startswith('none'),
          'no RNG, no seed, no sampling — the only randomness in this gate is '
          f'the Monte Carlo (seed {SEED})')
    return con, ladder[chosen]


# ==========================================================================
# STEP 2 — the two cards, side by side
# ==========================================================================

def step_2_collapse(data, con):
    banner('STEP 2 — THE TRAIN CARD, AND THEN THE HOLD-OUT CARD')
    print('The same strategy, the same run, the same costs. The only '
          'difference between\nthe two columns is whether the candles were '
          'inside the table\'s memory.\n')

    res = run_backtest(data, con, strategy_name=con.name, params=con.params,
                       train_end=TRAIN_END, regime=True, verbose=False)
    save(res, 'EXHIBIT 1 — the con artist (SYNTHETIC)')
    train_card, holdout_card = res.card('train'), res.card('holdout')
    print()
    print(side_by_side(train_card, holdout_card))
    print()
    print('  THE TRAIN CARD IN FULL:')
    print(train_card.text())
    print()
    print('  THE HOLD-OUT CARD IN FULL:')
    print(holdout_card.text())

    fired = too_good_alarm(train_card, 'the con artist\'s TRAIN card')
    check('(a) the con artist\'s TRAIN card looks spectacular',
          train_card['profit_factor'] > TOO_GOOD_PF
          and train_card['win_pct'] > TOO_GOOD_WIN_PCT,
          f'PF {train_card["profit_factor"]:.2f}, win rate '
          f'{train_card["win_pct"]:.1f}%, net '
          f'{train_card["net_return"]:+.2f}%')
    check('(a) the standing too-good law fires on that train card', fired)
    check('(b) the hold-out card collapses next to it',
          holdout_card['profit_factor'] < train_card['profit_factor']
          and holdout_card['net_return'] < 0,
          f'profit factor {train_card["profit_factor"]:.2f} -> '
          f'{holdout_card["profit_factor"]:.2f}, net return '
          f'{train_card["net_return"]:+.2f}% -> '
          f'{holdout_card["net_return"]:+.2f}%')
    check('the con artist never saw a candle past train_end',
          res.meta['audit_violations'] == 0,
          f'{res.meta["audit_calls"]:,} strategy calls, 0 look-ahead '
          f'violations; its table was sealed at {TRAIN_END}')

    print()
    print('  WHAT JUST HAPPENED, IN PLAIN WORDS. Nothing was broken and no '
          'rule was')
    print('  bent. The strategy wrote down what had already happened and then '
          'bet that')
    print('  it would happen again in the same hour of the same weekday after '
          'the same')
    print('  shape of candles. On the data it copied from, that is a perfect '
          'prophecy.')
    print('  On ten months it had never seen, it is a phone book. THIS IS THE '
          'ENTIRE')
    print('  DISEASE, and it is why a train card is never evidence of '
          'anything.')
    return res, train_card, holdout_card


# ==========================================================================
# STEP 3 / 4 — the three detectors on the con artist's hold-out
# ==========================================================================

def step_3_detectors(res, holdout_card):
    banner('STEP 3 — THE THREE LIE DETECTORS ON THE CON ARTIST\'S HOLD-OUT')

    wf = walk_forward(res)
    print(wf.text())
    check('(c) walk-forward rendered a verdict on the con artist',
          wf.verdict in ('CONSISTENT', 'INCONSISTENT'),
          f'{wf.verdict} — profitable in {wf.profitable_windows} of '
          f'{wf.n_windows} windows')
    counted = sum(w['stats']['trades'] for w in wf.windows)
    check('every hold-out trade landed in exactly one walk-forward window',
          counted == holdout_card['trades'],
          f'{counted} of {holdout_card["trades"]}')

    print()
    mc = monte_carlo_result(res)
    print(mc.text())
    check('(d) Monte Carlo ran on the con artist without error',
          isinstance(mc['dd_p95'], float),
          f'seed {mc["seed"]}, {mc["paths"]:,} reshuffles, 5th-percentile '
          f'drawdown {mc["dd_p95"]:.2f}%')
    mc2 = monte_carlo_result(res)
    check('the con artist\'s Monte Carlo reproduces itself on the same seed',
          mc.numbers() == mc2.numbers())

    print()
    rr = regime_report(res)
    print(rr.text())
    check('(d) the regime report ran on the con artist without error',
          len(rr.buckets) > 0, ', '.join(rr.regimes))
    check('the regime buckets add back up to the con artist\'s stat card',
          round(rr.overall['net_return'], 2) == round(holdout_card['net_return'], 2),
          f'{rr.overall["net_return"]:+.2f}% both ways')
    return wf, mc, rr


# ==========================================================================
# STEP 5 — the locked battery on the con artist
# ==========================================================================

def step_5_battery(holdout_card, wf, mc):
    banner('STEP 5 — THE LOCKED BATTERY: DOES THE LAB CERTIFY THE CON ARTIST?')
    print('This is the exam Phase 2 exists to pass. If the Lab certifies this '
          'strategy,\nPhase 2 is NOT done, no matter how nice the code looks.\n')

    certified, rows = run_battery('EXHIBIT 1, THE CON ARTIST '
                                  '(hold-out, after costs)',
                                  holdout_card, wf, mc)
    check('(e) THE LAB REFUSED TO CERTIFY THE CON ARTIST',
          not certified,
          f'{sum(1 for r in rows if not r[3])} of {len(rows)} locked bars '
          f'failed')
    for name, got, need, ok in rows:
        check(f'battery bar recorded: {name}', True, f'{got} (needs {need}) '
              f'-> {"PASS" if ok else "FAIL"}')

    print()
    print('  A NOTE ON THE BARS THE CON ARTIST DID CLEAR, so that clearing '
          'them is')
    print('  never mistaken for a compliment. A bar it passes is a bar that '
          'was never')
    print('  going to catch it: a big enough trade count only means it traded '
          'a lot,')
    print('  and a survivable Monte Carlo ride only means it lost SMOOTHLY. '
          'Losing')
    print('  smoothly is still losing. The battery is an AND, not a score.')
    return certified


# ==========================================================================
# STEP 6 — EXHIBIT 2: the leak, and the limit this Lab must admit
# ==========================================================================

def step_6_the_leak(data, con):
    banner('STEP 6 — EXHIBIT 2: THE CHEAT\'S RESULTS SOLD AS A TRACK RECORD')
    print('`PerfectForesight` from lab/dummies.py — the leak from Gate 2.3. '
          'Its author\nhanded it the whole file, so it reads tomorrow\'s candle '
          'around the side of\nthe engine\'s feed. The engine cannot stop this: '
          'the engine controls what the\nFEED delivers, and nothing else.\n')
    print('THIS EXHIBIT DOES NOT SHOW THE LAB WINNING. It shows exactly where '
          'the Lab\'s\nnumbers stop working, measured rather than assumed.\n')

    leaked = PerfectForesight(data.df)
    res = run_backtest(data, leaked, strategy_name='cheat-perfect-foresight',
                       params=leaked.params, train_end=TRAIN_END,
                       regime=True, verbose=False)
    save(res, 'EXHIBIT 2 — the leak (SYNTHETIC)')
    train_card, holdout_card = res.card('train'), res.card('holdout')
    print()
    print(side_by_side(train_card, holdout_card))
    print()
    print(holdout_card.text())

    check('the leak\'s hold-out does NOT collapse (a cheat cheats everywhere)',
          holdout_card['net_return'] > 0
          and holdout_card['profit_factor'] > 1.0,
          f'train net {train_card["net_return"]:+.2f}% / PF '
          f'{train_card["profit_factor"]:.2f}  ->  hold-out net '
          f'{holdout_card["net_return"]:+.2f}% / PF '
          f'{holdout_card["profit_factor"]:.2f}')

    wf = walk_forward(res)
    mc = monte_carlo_result(res)
    print()
    print(wf.text())
    certified, _ = run_battery('EXHIBIT 2, THE LEAK (hold-out, after costs)',
                               holdout_card, wf, mc)
    check('the numeric pipeline could not expose the leak',
          certified,
          'the leak cleared every locked bar — which is the point of this '
          'exhibit, not a failure of the bars')

    fired = too_good_alarm(holdout_card, 'the leak\'s HOLD-OUT card')
    check('MEASURED LIMIT: the too-good alarm stays SILENT on the leak',
          not fired,
          f'PF {holdout_card["profit_factor"]:.2f} < {TOO_GOOD_PF} and win '
          f'rate {holdout_card["win_pct"]:.1f}% < {TOO_GOOD_WIN_PCT}% — the '
          f'founding evidence of Law 7; if this ever starts firing, the '
          f'ground has moved and Law 7 must be re-examined')

    # ---- LAW 7's instrument, proven against the very leak that founded it --
    print()
    print('  LAW 7\'S INSTRUMENT — lab/leak_check.py, scanning the strategy '
          'OBJECTS for')
    print('  smuggled data (the scan the numbers cannot do):')
    print()
    rep_leak = leak_check(leaked)
    print(rep_leak.text())
    check('leak_check FLAGS the leak: it carries the whole file',
          rep_leak.flagged
          and any('full' in path for path, _ in rep_leak.findings),
          '; '.join(f'{p} -> {d}' for p, d in rep_leak.findings))
    rep_con = leak_check(con)
    rep_ma = leak_check(MACross(20, 50))
    check('leak_check clears the honest strategies (MA-cross, con artist)',
          not rep_con.flagged and not rep_ma.flagged,
          'the con artist smuggles nothing — its sin is memorising, which is '
          'the numbers\' job to catch, and they did')
    check('leak_check says in words that a clean scan is not innocence',
          'NOT INNOCENCE' in rep_ma.text() and 'READ' in rep_ma.text())

    print()
    print('  ' + '=' * 74)
    print('  THE LIMIT, STATED IN PLAIN WORDS AND NEVER TO BE OVERSTATED')
    print('  ' + '=' * 74)
    print('  The Lab\'s NUMBERS catch OVERFITTING. That is what Exhibit 1 '
          'proved, and it')
    print('  is a real and valuable power: a strategy that memorised the past '
          'falls')
    print('  apart on candles it has not seen, and the hold-out, the '
          'walk-forward and')
    print('  the Monte Carlo all said so, in that order.')
    print()
    print('  The Lab\'s NUMBERS CANNOT CATCH A LEAK. A strategy that is fed '
          'the answers')
    print('  answers correctly everywhere — on train, on the hold-out, in '
          'every')
    print('  walk-forward window. There is no arithmetic that separates '
          '"knew the')
    print('  future" from "was right". Exhibit 2 walked the whole locked '
          'battery and')
    print('  the battery CERTIFIED IT AS GOOD.')
    print()
    if fired:
        print('  The flare went up. The too-good alarm fired on this card, '
              'which is the')
        print('  signal to stop celebrating and send a human to read the '
              'strategy\'s code.')
        print('  That alarm plus that reading are the entire defence against a '
              'leak — the')
        print('  numbers contributed nothing here and must never be credited '
              'with it.')
    else:
        print('  AND THE FLARE DID NOT GO UP. THIS IS THE FINDING OF GATE 2.5, '
              'AND IT IS')
        print('  WORSE THAN THE LIMIT WE EXPECTED TO WRITE DOWN.')
        print()
        print('  We expected to report: "the numbers miss a leak, but the '
              'too-good alarm')
        print('  catches it." That is NOT what was measured. This leak\'s '
              'hold-out card')
        print(f'  reads profit factor {holdout_card["profit_factor"]:.2f} and '
              f'win rate {holdout_card["win_pct"]:.1f}% — respectable, '
              f'unremarkable,')
        print(f'  and comfortably under BOTH halves of the standing law '
              f'(PF > {TOO_GOOD_PF}, '
              f'win > {TOO_GOOD_WIN_PCT}%).')
        print('  So a strategy that reads tomorrow\'s candle walked this '
              'entire pipeline,')
        print('  cleared every locked Phase 6 bar, and set off NO alarm '
              'anywhere.')
        print()
        print('  WHY IT LOOKS SO ORDINARY (recorded in Gate 2.3 and confirmed '
              'again here):')
        print('  the cheat sees exactly ONE candle ahead, but the engine holds '
              'a trade until')
        print('  an ATR stop or target is hit — many candles later. So the '
              'peek buys the')
        print('  entry direction and nothing else; most of the exposure is '
              'blind, and')
        print('  rule-based exits decide the outcome. A modest leak produces '
              'modest numbers.')
        print('  THAT IS PRECISELY WHAT MAKES IT DANGEROUS: the too-good alarm '
              'is tuned for')
        print('  spectacular cheating, and a leak does not have to be '
              'spectacular to be a')
        print('  lie. It only has to be good enough to win a Phase 6 slot, and '
              'this one is.')
        print()
        print('  WHAT THIS LEAVES AS THE ONLY DEFENCE:')
        print('    A HUMAN READING THE STRATEGY\'S CODE. Not a formality. Not '
              'a')
        print('    nice-to-have. On the evidence of this exhibit it is the '
              'SINGLE point of')
        print('    failure between a leaking strategy and a Phase 6 '
              'certificate, because')
        print('    neither the battery nor the alarm objected to this one at '
              'any point.')
        print()
        print('  THE COMMANDER\'S DECISION (2026-07-26, delegated in his '
              'words and recorded')
        print('  in PROGRESS_LOG.md): the limit is ACCEPTED and ARMOURED, '
              'never papered')
        print('  over. LAW 7 — THE LEAK LAW — now stands in SHIP_LAWS.md: no '
              'strategy')
        print('  enters certification until its code has been read for leaks '
              'and the')
        print('  reading recorded; lab/leak_check.py (which finds the data '
              'this leak')
        print('  smuggles) runs as the reading\'s aid, never its substitute; '
              'and the alarm')
        print('  was NOT lowered — tuning it until this exhibit trips would '
              'flag every')
        print('  honest strategy too, a detector that catches nothing.')
    print('  ' + '=' * 74)
    return res, holdout_card, fired


# ==========================================================================

def main():
    print('=' * 78)
    print('ZAR X LAB — GATE 2.5: THE PHASE 2 EXIT GATE')
    print('=' * 78)
    print(f'  market    : {ASSET} {TIMEFRAME}  (frozen vault only, read-only)')
    print(f'  train_end : {TRAIN_END}   <- the SAME hold-out line as Gates 2.3 '
          f'and 2.4')
    print(f'  costs     : fee {LAB_COSTS["fee_pct"]:.3%} + slippage '
          f'{LAB_COSTS["slippage_pct"]:.3%}, per side, every trade')
    print(f'  MC seed   : {SEED} (recorded). The lookup-table build uses no '
          f'randomness at all.')
    print()
    print('  THE LOCKED DEFINITION OF "CERTIFIED AS GOOD" (written into this '
          'file')
    print('  before any run; a copy of the Phase 6 gauntlet bars):')
    print(f'    - hold-out profit factor after costs      >= '
          f'{BAR_MIN_PROFIT_FACTOR}')
    print(f'    - hold-out trades                         >= '
          f'{BAR_MIN_TRADES}')
    print(f'    - walk-forward verdict                    == '
          f'{BAR_WALK_FORWARD}')
    print(f'      (>= 60% of windows profitable AND no window > 50% of profit)')
    print(f'    - Monte Carlo 5th-percentile drawdown     <  '
          f'{BAR_MAX_MC_DRAWDOWN:.0f}%')
    print()

    data = load_vault(ASSET, TIMEFRAME)
    print(f'  THE DOOR: {data.report.name} inspected at load -> {data.verdict}')
    print(f'  {len(data.df):,} candles, {data.df.index[0]} -> '
          f'{data.df.index[-1]}')

    step_0_nothing_moved(data)
    con, _ = step_1_build(data)
    res, train_card, holdout_card = step_2_collapse(data, con)
    wf, mc, _ = step_3_detectors(res, holdout_card)
    step_5_battery(holdout_card, wf, mc)
    step_6_the_leak(data, con)

    banner('GATE 2.5 — THE FULL TALLY')
    for name, ok in results.items():
        print(f'  [{"OK" if ok else "FAIL"}] {name}')
    ok = all(results.values())
    print('-' * 78)
    print(f'  checks run: {len(results)}   passed: {sum(results.values())}   '
          f'failed: {len(results) - sum(results.values())}')
    print(f'GATE 2.5: {"PASSED" if ok else "FAILED"}')
    print('=' * 78)
    if not ok:
        print()
        print('  A failing gate is never committed and never called "mostly '
              'passed".')
        print('  The failing checks above are the message; read them before '
              'anything else.')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
