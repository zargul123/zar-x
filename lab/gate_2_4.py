"""
Zar X Lab — GATE 2.4: THE LIE DETECTORS (their own exam).

Step 2.3 built an engine that cannot flatter a strategy. Step 2.4 bolts three
instruments onto it, and this file is the exam that earns them the right to be
believed. An instrument that has never been caught working is decoration.

WHAT THIS GATE PROVES, IN ORDER
  0. NOTHING MOVED. The MA-cross dummy's hold-out card must reproduce Gate 2.3
     EXACTLY — 37 trades, PF 0.63, net -4.88%. If it does not, the ground under
     Step 2.4 shifted and everything below is measuring the wrong thing.
  1. All three instruments run on that dummy and print readable reports.
  2. THE EDGE CASE. The MA-cross dummy LOSES money, so the walk-forward's
     "no window may hold more than 50% of the profit" rule has no profit to
     divide. It must say so in plain words and must never divide by a zero or
     negative total. This is the path the gate deliberately walks.
  3. THE DETECTOR MUST DETECT. A SYNTHETIC per-trade sequence is built in
     memory — clearly labelled, never written to the vault or to results — in
     which one window carries nearly all the profit. Walk-forward must raise
     the lucky-window flag on it. And a CONTROL sequence, profitable but
     evenly spread, must NOT be flagged: a detector that flags everything is
     as useless as one that flags nothing.
  4. REPRODUCIBILITY. The Monte Carlo, run twice with the recorded seed, must
     produce identical numbers. A Monte Carlo that cannot reproduce itself is
     not evidence.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\gate_2_4.py
"""
import os
import sys

import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)
sys.path.insert(0, os.path.dirname(LAB_DIR))

from engine import load_vault, run_backtest                    # noqa: E402
from dummies import MACross                                    # noqa: E402
from walk_forward import walk_forward, walk_forward_trades     # noqa: E402
from monte_carlo import monte_carlo_result, SEED               # noqa: E402
from regime_report import regime_report                        # noqa: E402

ASSET = 'BTC-USD'
TIMEFRAME = '4h'
TRAIN_END = '2025-10-01'        # the SAME hold-out line as Gate 2.3

# The Gate 2.3 hold-out card, copied from PROGRESS_LOG, each number with the
# number of decimals the log actually recorded it to. Comparing to more
# decimals than were written down would fail an honest reproduction on the
# log's rounding rather than on the engine's arithmetic (win rate was recorded
# as 37.8%, and 37.84 IS that number).
GATE_2_3 = {'trades': (37, 0), 'wins': (14, 0), 'losses': (23, 0),
            'win_pct': (37.8, 1), 'profit_factor': (0.63, 2),
            'net_return': (-4.88, 2), 'max_drawdown': (7.98, 2)}

results = {}          # name -> True/False, filled as the gate walks


def check(name, ok, detail=''):
    # two checks sharing a name would mean the second silently overwrites the
    # first in the tally — a failure could disappear behind a pass
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


# --------------------------------------------------------------------------
# STEP 0 — the ground has not moved
# --------------------------------------------------------------------------

def step_0_reproduce(data):
    banner('STEP 0 — THE SAME DUMMY, THE SAME LINE, THE SAME NUMBERS')
    print('Step 2.4 measures the Gate 2.3 result. So the first thing to prove '
          'is that\nthe Gate 2.3 result is still exactly what the log says it '
          'is. Same dummy\n(MA-cross 20/50), same market (BTC-USD 4h), same '
          f'hold-out line ({TRAIN_END}).\n')

    strat = MACross(20, 50)
    res = run_backtest(data, strat, strategy_name=strat.name,
                       params=strat.params, train_end=TRAIN_END,
                       regime=True, verbose=False)
    card = res.card('holdout')
    path = res.save_csv()
    print(f'  evidence written: {os.path.relpath(path, os.path.dirname(LAB_DIR))}')
    print()
    print(card.text())
    print()

    for key, (expected, decimals) in GATE_2_3.items():
        got = round(float(card[key]), decimals)
        same = got == round(float(expected), decimals)
        check(f'reproduces Gate 2.3 {key}',
              same, f'expected {expected}, got {got}')
    check('the engine logged 0 look-ahead violations',
          res.meta['audit_violations'] == 0)
    if card['profit_factor'] > 2 or card['win_pct'] > 70:
        print('\n  !! STANDING LAW: PF > 2 or win rate > 70% — assume a leak '
              'and hunt it.')
    return res, card


# --------------------------------------------------------------------------
# STEP 1 — walk-forward on the real (losing) dummy: THE EDGE CASE
# --------------------------------------------------------------------------

def step_1_walk_forward(res, card):
    banner('STEP 1 — WALK-FORWARD ON THE LOSING DUMMY (the edge case)')
    print('The MA-cross dummy lost 4.88% over the hold-out. The concentration '
          'rule\n("no window may hold more than half the profit") therefore '
          'has NOTHING to\ndivide. The instrument must say that in words and '
          'must never divide by a\nzero or negative total. Watch TEST 2.\n')

    wf = walk_forward(res)
    print(wf.text())
    print()

    traded = sum(w['stats']['trades'] for w in wf.windows)
    shares_printed = [w['share'] for w in wf.windows if w['share'] is not None]

    check('the window table printed with 6 windows', len(wf.windows) == 6)
    check('every hold-out trade landed in exactly one window',
          traded == card['trades'], f'{traded} of {card["trades"]}')
    check('the losing strategy is called INCONSISTENT',
          wf.verdict == 'INCONSISTENT')
    check('the concentration test refused to run on a non-positive total',
          wf.concentration_applies is False,
          f'hold-out total {wf.total_profit:+.2f}%')
    check('no share-of-profit number was invented for a loser',
          len(shares_printed) == 0 and wf.worst_window is None)
    check('the refusal is written in plain words, not left blank',
          'DOES NOT APPLY' in wf.text())
    check('no lucky-window flag was raised on a strategy with no profit',
          wf.lucky_window_flag is False)
    check('the consistency test still ran and failed honestly',
          wf.consistency_ok is False,
          f'profitable in {wf.profitable_windows} of 6 windows')
    return wf


# --------------------------------------------------------------------------
# STEP 2 — THE DETECTOR MUST DETECT (synthetic sequences, built in memory)
# --------------------------------------------------------------------------

def _synthetic_trades(spec, start='2025-10-01'):
    """Build a fake per-trade sequence in memory. SYNTHETIC — it never touches
    the vault, never becomes a results CSV, and no number from it may ever be
    quoted as a market result. It exists only to hand the detector a known
    disease and see whether the detector names it.

    `spec` is six lists of per-trade results in PERCENT, one list per window.
    Each window's trades are spaced two days apart inside a 30-day slot, so
    which window a trade belongs to is obvious by eye.
    """
    t0 = pd.Timestamp(start)
    rows = []
    for k, window_returns in enumerate(spec):
        for j, pct in enumerate(window_returns):
            rows.append({
                'entry_time': t0 + pd.Timedelta(days=30 * k + 2 * j),
                'direction': 'long' if j % 2 == 0 else 'short',
                'return_pct': pct / 100.0,      # the column the Lab compounds
                'regime_at_entry': 'Synthetic',
            })
    return pd.DataFrame(rows)


# five ordinary windows, and ONE that carries almost everything
LUCKY_SPEC = [
    [0.4] * 6 + [-0.3] * 4,        # window 1  -> +1.2%
    [0.4] * 6 + [-0.3] * 4,        # window 2  -> +1.2%
    [0.4] * 6 + [-0.3] * 4,        # window 3  -> +1.2%
    [5.2] * 8 + [-0.8] * 2,        # window 4  -> +40.0%   <- THE LUCKY MONTH
    [0.4] * 6 + [-0.3] * 4,        # window 5  -> +1.2%
    [0.4] * 6 + [-0.3] * 4,        # window 6  -> +1.2%
]

# profitable and evenly spread — the control the detector must NOT flag
CONTROL_SPEC = [
    [0.5] * 6 + [-0.3] * 4,        # +1.80%
    [0.4] * 5 + [-0.35] * 5,       # +0.25%
    [0.6] * 6 + [-0.5] * 4,        # +1.60%
    [0.45] * 7 + [-0.4] * 3,       # +1.95%
    [0.3] * 6 + [-0.2] * 4,        # +1.00%
    [0.5] * 5 + [-0.3] * 5,        # +1.00%
]


def step_2_the_detector_must_detect():
    banner('STEP 2 — THE DETECTOR MUST DETECT (planted lucky window)')
    print('EVERYTHING IN THIS STEP IS SYNTHETIC — trade sequences built in '
          'memory for\nthis test alone, like the poisoned copy in Gate 2.2. '
          'None of it is a market\nresult and no number from it may ever be '
          'quoted as one.\n')

    # ---- EXHIBIT A: the disease ------------------------------------------
    print('EXHIBIT A — the lucky-window disease.')
    print('  Sixty fabricated trades. Five windows make an unremarkable +1.2% '
          'each.\n  Window 4 makes +40% on its own. A single stat card for '
          'all sixty would\n  show +46% and look like an edge. It is one '
          'lucky month wearing a costume.\n')
    lucky = _synthetic_trades(LUCKY_SPEC)
    wf_lucky = walk_forward_trades(
        lucky, label='SYNTHETIC — one window carries the profit',
        source='SYNTHETIC sequence built in memory by gate_2_4.py — NOT a '
               'market result')
    print(wf_lucky.text())
    print()

    w4 = wf_lucky.worst_window
    check('the lucky-window FLAG WAS RAISED', wf_lucky.lucky_window_flag,
          f'window {w4["n"]} held {w4["share"]:.1f}% of the profit'
          if w4 else '')
    check('it named the right window (4)', w4 is not None and w4['n'] == 4)
    check('the verdict is INCONSISTENT', wf_lucky.verdict == 'INCONSISTENT')
    check('the flag came from CONCENTRATION alone, not from a weak '
          'consistency score', wf_lucky.consistency_ok is True,
          f'profitable in {wf_lucky.profitable_windows} of 6 windows — this '
          f'strategy passes test 1 and is caught only by test 2')
    check('it showed what is left without the lucky window',
          'without its lucky' in wf_lucky.text(),
          f'the other five windows made '
          f'{wf_lucky.total_profit - w4["sum_return"]:+.2f}% between them'
          if w4 else '')
    print()

    # ---- EXHIBIT B: the control ------------------------------------------
    print('EXHIBIT B — the control. A detector that flags everything is not a '
          'detector.')
    print('  The same kind of fabricated sequence, profitable in all six '
          'windows, with\n  the profit spread evenly. This one must come back '
          'CLEAN.\n')
    control = _synthetic_trades(CONTROL_SPEC)
    wf_control = walk_forward_trades(
        control, label='SYNTHETIC — profit spread evenly (control)',
        source='SYNTHETIC sequence built in memory by gate_2_4.py — NOT a '
               'market result')
    print(wf_control.text())
    print()
    check('the control was NOT flagged', wf_control.lucky_window_flag is False,
          f'biggest window held '
          f'{wf_control.worst_window["share"]:.1f}% of the profit')
    check('the control is called CONSISTENT', wf_control.verdict == 'CONSISTENT')
    print()

    # ---- EXHIBIT C: the quiet window -------------------------------------
    print('EXHIBIT C — the quiet window. The control with window 3 removed '
          'entirely.')
    print('  A window with no trades must be PRINTED as "no trades" and must '
          'still be\n  counted in the denominator. Silently dropping it would '
          'quietly improve\n  the consistency score of every strategy that '
          'sits out a bad stretch.\n')
    quiet = control[(control['entry_time'] < pd.Timestamp('2025-10-01')
                     + pd.Timedelta(days=60))
                    | (control['entry_time'] >= pd.Timestamp('2025-10-01')
                       + pd.Timedelta(days=90))]
    wf_quiet = walk_forward_trades(
        quiet, label='SYNTHETIC — one window with no trades',
        source='SYNTHETIC sequence built in memory by gate_2_4.py — NOT a '
               'market result')
    print(wf_quiet.text())
    print()
    empty = [w for w in wf_quiet.windows if w['stats']['no_trades']]
    check('the empty window was reported, not skipped',
          len(empty) == 1 and 'no trades in this window' in wf_quiet.text(),
          f'window {empty[0]["n"]} printed as "no trades"' if empty else '')
    check('the empty window still counts in the denominator (6 windows, not 5)',
          wf_quiet.n_windows == 6 and len(wf_quiet.windows) == 6,
          f'profitable in {wf_quiet.profitable_windows} of 6')
    return wf_lucky, wf_control, wf_quiet


# --------------------------------------------------------------------------
# STEP 3 — Monte Carlo, and the same seed twice
# --------------------------------------------------------------------------

def step_3_monte_carlo(res):
    banner('STEP 3 — MONTE CARLO (and the proof it reproduces itself)')
    print('The same 37 hold-out trades, dealt in 10,000 different orders. The '
          'question\nis not what it made — that cannot change — but how rough '
          'the ride could\nhave been. Then the whole thing is run a SECOND '
          f'time with the same recorded\nseed ({SEED}), and the two reports '
          'are compared character by character.\n')

    mc1 = monte_carlo_result(res)
    print(mc1.text())
    print()

    mc2 = monte_carlo_result(res)
    same_text = mc1.text() == mc2.text()
    same_numbers = mc1.numbers() == mc2.numbers()
    diffs = [k for k in mc1.numbers()
             if mc1.numbers()[k] != mc2.numbers().get(k)]

    check('the seed is recorded in the report itself', str(SEED) in mc1.text(),
          f'seed {SEED}')
    check('run twice with the same seed -> identical numbers', same_numbers,
          'every figure matches' if same_numbers else f'differences: {diffs}')
    check('run twice with the same seed -> identical report text', same_text)
    check('the reshuffle changed the road, not the destination',
          mc1['final_spread'] < 1e-6,
          f'spread between best and worst final return: '
          f'{mc1["final_spread"]:.9f} percentage points')
    check('the 5th-percentile drawdown was measured and judged',
          isinstance(mc1['dd_p95'], float),
          f'{mc1["dd_p95"]:.2f}% vs the 30% ruin line -> '
          f'{"RUIN FLAG" if mc1["ruin_flag"] else "survivable"}')
    return mc1


# --------------------------------------------------------------------------
# STEP 4 — the regime breakdown
# --------------------------------------------------------------------------

def step_4_regime(res, card):
    banner('STEP 4 — THE REGIME BREAKDOWN (information, never a filter)')
    print('Where did the money come from, and in what weather? The regime was '
          'stamped\nat entry by the live Regime Vane, from candles that had '
          'already closed.\n')

    rr = regime_report(res)
    print(rr.text())
    print()

    counted = sum(s['trades'] for _, s in rr.buckets)
    check('every hold-out trade landed in exactly one regime bucket',
          counted == card['trades'], f'{counted} of {card["trades"]}')
    check('the buckets add back up to the engine\'s own stat card',
          round(rr.overall['net_return'], 2) == round(card['net_return'], 2)
          and round(rr.overall['profit_factor'], 2) == round(card['profit_factor'], 2),
          f'net {rr.overall["net_return"]:+.2f}% and PF '
          f'{rr.overall["profit_factor"]:.2f}, same as the card')
    check('no trade is missing its weather',
          all(name and name != 'Unrecorded' for name in rr.regimes),
          ', '.join(rr.regimes))
    check('thin samples are marked, not quietly presented as evidence',
          'anecdote, not a statistic' in rr.text() or
          'thin sample' in rr.text())
    check('the report states in words that it is not a filter',
          'INFORMATION, NOT A FILTER' in rr.text())
    return rr


# --------------------------------------------------------------------------

def main():
    print('=' * 78)
    print('ZAR X LAB — GATE 2.4: THE LIE DETECTORS')
    print('=' * 78)
    print(f'  market    : {ASSET} {TIMEFRAME}  (frozen vault only)')
    print(f'  dummy     : MA-cross 20/50 — the same unimpressive loser as '
          f'Gate 2.3')
    print(f'  train_end : {TRAIN_END}   <- the SAME hold-out line. If this '
          f'ever changes,\n              every number in the log changes with '
          f'it and must be re-stated.')
    print()

    data = load_vault(ASSET, TIMEFRAME)
    print(f'  THE DOOR: {data.report.name} inspected at load -> {data.verdict}')
    print(f'  {len(data.df):,} candles, {data.df.index[0]} -> '
          f'{data.df.index[-1]}')
    print()

    res, card = step_0_reproduce(data)
    step_1_walk_forward(res, card)
    step_2_the_detector_must_detect()
    step_3_monte_carlo(res)
    step_4_regime(res, card)

    banner('GATE 2.4 — THE FULL TALLY')
    for name, ok in results.items():
        print(f'  [{"OK" if ok else "FAIL"}] {name}')
    ok = all(results.values())
    print('-' * 78)
    print(f'  checks run: {len(results)}   passed: {sum(results.values())}   '
          f'failed: {len(results) - sum(results.values())}')
    print(f'GATE 2.4: {"PASSED" if ok else "FAILED"}')
    print('=' * 78)
    if not ok:
        print('\n  A failing gate is never committed and never called '
              '"mostly passed".')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
