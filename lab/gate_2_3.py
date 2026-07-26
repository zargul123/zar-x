"""
Zar X Lab — GATE 2.3: THE THREE DUMMIES (the backtest engine's own exam).

This is the whole point of Phase 2. A backtest engine cannot be trusted
because its code looks careful; it can only be trusted because it was caught
trying and failing to lie. So we hand it three instruments:

  DUMMY 1  a strategy that never trades       -> must report EXACTLY 0 trades
                                                 and EXACTLY 0 P&L.
  DUMMY 2  an ordinary 20/50 MA cross         -> must produce a full stat card
                                                 on the HOLD-OUT window, with
                                                 trades > 0 and the costs
                                                 visibly subtracted (the same
                                                 run's gross vs net, side by
                                                 side, so the drag is
                                                 undeniable).
  DUMMY 3  a planted cheat that reads          -> profitable when the future is
           tomorrow's close                       handed to it; IMPOSSIBLE
                                                  through the engine's feed.

HOW THE ENGINE STRUCTURALLY PREVENTS THE CHEAT (the part that matters)
----------------------------------------------------------------------
The engine walks the candles in order. At candle i it calls the strategy with

        signal(df.iloc[:i + 1].copy())

Three separate properties make the peek impossible, and this gate measures
all three rather than trusting any of them:

  1. LENGTH. The object handed over has exactly i+1 rows. Candle i+1 is not
     the last row, not a hidden row, not a row of NaNs — it is absent. Asking
     for it (`df['close'].iloc[len(df)]`) raises IndexError. There is no
     value to read, so there is no cheat to perform.
  2. ITS OWN MEMORY. `.copy()` means the strategy does not receive a view onto
     the full price array. It cannot reach the rest of the file by walking
     back through the buffer the slice was cut from.
  3. AUDITED, NOT ASSUMED. The engine checks, at every single call, that the
     last timestamp it is about to hand over is exactly the candle it is
     standing on, and refuses to produce a number at all if that is ever
     untrue. This gate re-checks it independently with a spy that compares
     every delivery against the vault file itself.

And the two rules that stop the cheat from sneaking in through the trade
mechanics instead: entries happen at the NEXT candle's OPEN (never at the
signal candle's close), and if a candle touches both the stop and the target
the LOSS is counted, because we cannot know which came first.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\gate_2_3.py
"""
import os
import sys

import numpy as np
import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)
sys.path.insert(0, os.path.dirname(LAB_DIR))

from engine import load_vault, run_backtest, RESULTS_DIR      # noqa: E402
from dummies import (always_flat, MACross, peek_at_tomorrow,   # noqa: E402
                     PerfectForesight, peek_or_guess)

ASSET = 'BTC-USD'
TIMEFRAME = '4h'
TRAIN_END = '2025-10-01'      # RECORDED: the hold-out line for every gate run
                              # below. ~10 months of untouched candles after it.

saved_files = []


def _save(result, label):
    path = result.save_csv()
    saved_files.append(path)
    print(f'  evidence written: {os.path.relpath(path, os.path.dirname(LAB_DIR))}'
          f'   [{label}]')
    return path


class FeedSpy:
    """An independent witness sitting between the engine and the strategy.

    It does not trust the engine's own audit. For every delivery it records
    what it was given and compares it against the real vault file: how many
    rows, whose timestamp came last, and whether one single candle from the
    future was ever present. It also tries the peek itself, every time.
    """

    def __init__(self, inner, full_index):
        self.inner = inner
        self.full_index = full_index
        self.calls = 0
        self.peek_attempts = 0
        self.peek_refused = 0          # IndexError — the future was not there
        self.future_rows_delivered = 0  # rows dated after "now" — must stay 0
        self.wrong_length = 0           # got more (or fewer) rows than the past
        self.last_time = None
        self.out_of_order = 0

    def __call__(self, df):
        self.calls += 1
        now = df.index[-1]

        # (1) was even one candle from the future inside the delivery?
        if (df.index > now).any():
            self.future_rows_delivered += int((df.index > now).sum())

        # (2) did the delivery contain exactly the past, no more, no less?
        true_position = self.full_index.get_loc(now)
        if len(df) != true_position + 1:
            self.wrong_length += 1

        # (3) is the walk actually chronological?
        if self.last_time is not None and now <= self.last_time:
            self.out_of_order += 1
        self.last_time = now

        # (4) try the cheat ourselves, on every single delivery
        self.peek_attempts += 1
        try:
            df['close'].iloc[len(df)]
        except IndexError:
            self.peek_refused += 1

        return self.inner(df)

    def report(self):
        return [
            f'strategy calls audited            : {self.calls:,}',
            f'candles from the future delivered : {self.future_rows_delivered}'
            f'   (must be 0)',
            f'deliveries with the wrong length  : {self.wrong_length}'
            f'   (must be 0 — each one is exactly "everything up to now")',
            f'out-of-order deliveries           : {self.out_of_order}'
            f'   (must be 0 — the walk is chronological)',
            f'peek attempts refused by IndexError: {self.peek_refused:,} of '
            f'{self.peek_attempts:,}   (must be all of them)',
        ]

    @property
    def clean(self):
        return (self.future_rows_delivered == 0 and self.wrong_length == 0
                and self.out_of_order == 0
                and self.peek_refused == self.peek_attempts
                and self.calls > 0)


def big_pct(x):
    """Print a percentage a human can read, however absurd it gets."""
    if abs(x) >= 1e6:
        return f'{x:+,.0f}%  (that is {x / 100:,.0f}x the account)'
    return f'{x:+,.2f}%'


# --------------------------------------------------------------------------
# DUMMY 1
# --------------------------------------------------------------------------

def dummy_1_always_flat(data):
    print('=' * 70)
    print('DUMMY 1 — THE STRATEGY THAT NEVER TRADES')
    print('=' * 70)
    print('If the engine reports a single trade or a single cent of profit '
          'here,\nit is inventing trades. Expected: 0 and 0.\n')

    res = run_backtest(data, always_flat, strategy_name='always-flat',
                       params={}, train_end=TRAIN_END, regime=True)
    _save(res, 'dummy 1')

    full = res.card('full')
    hold = res.card('holdout')
    checks = {
        'exactly 0 trades (full history)': full['trades'] == 0,
        'exactly 0 trades (hold-out)': hold['trades'] == 0,
        'exactly 0 net P&L': full['net_pnl'] == 0.0,
        'exactly 0 net return': full['net_return'] == 0.0,
        'exactly 0% time in market': full['time_in_market'] == 0.0,
        'the per-trade CSV is empty (no phantom rows)': len(res.trades) == 0,
        'the engine still walked every candle': full['candles'] == len(data.df),
    }
    print()
    for label, ok in checks.items():
        print(f'  [{"OK" if ok else "FAIL"}] {label}')
    ok = all(checks.values())
    print(f'\nDUMMY 1: {"PASSED" if ok else "FAILED"}\n')
    return ok


# --------------------------------------------------------------------------
# DUMMY 2
# --------------------------------------------------------------------------

def dummy_2_ma_cross(data):
    print('=' * 70)
    print('DUMMY 2 — AN ORDINARY 20/50 MOVING-AVERAGE CROSS')
    print('=' * 70)
    print(f'An unremarkable strategy nobody is claiming is good. It is here to '
          f'prove\nthe engine can produce a COMPLETE stat card on the hold-out '
          f'window\n(everything after {TRAIN_END}) with the costs visibly '
          f'taken out.\n')

    strat = MACross(20, 50)
    spy = FeedSpy(strat, data.df.index)
    res = run_backtest(data, spy, strategy_name=strat.name,
                       params=strat.params, train_end=TRAIN_END, regime=True)
    _save(res, 'dummy 2')

    hold = res.card('holdout')
    full = res.card('full')

    print('\n  THE COST DRAG, SAME RUN, SIDE BY SIDE (hold-out window):')
    print(f'    gross return, costs switched OFF : '
          f'{hold["gross_return"]:+.2f}%   <- the fantasy')
    print(f'    net return, every cost paid      : '
          f'{hold["net_return"]:+.2f}%   <- the truth')
    print(f'    the difference                   : '
          f'{hold["cost_drag"]:.2f} percentage points, '
          f'${hold["costs_paid"]:,.2f} handed to the exchange over '
          f'{hold["trades"]} trades')
    if hold['trades']:
        print(f'    average cost per round trip      : '
              f'${hold["costs_paid"] / hold["trades"]:,.2f}')

    print('\n  THE FEED SPY (an independent witness, not the engine\'s own audit):')
    for line in spy.report():
        print(f'    {line}')

    regimes = res.window_trades('holdout')['regime_at_entry'].value_counts() \
        if hold['trades'] else pd.Series(dtype=int)
    print('\n  REGIME AT ENTRY (computed only from candles before each entry):')
    for k, v in regimes.items():
        print(f'    {k}: {v}')

    checks = {
        'the hold-out produced trades (trades > 0)': hold['trades'] > 0,
        'the hold-out window is real (candles > 0)': hold['candles'] > 0,
        'the stat card is complete (no missing field)': all(
            k in hold for k in ('win_pct', 'profit_factor', 'avg_win',
                                'avg_loss', 'max_drawdown', 'net_return',
                                'time_in_market')),
        'costs were actually charged (> $0)': hold['costs_paid'] > 0,
        'net return is BELOW gross return (costs subtracted, not ignored)':
            hold['net_return'] < hold['gross_return'],
        'every trade paid a cost (no free trade)': bool(
            (res.window_trades('holdout')['costs_paid'] > 0).all()),
        'time in market is a real fraction (0 < x <= 1)':
            0 < hold['time_in_market'] <= 1,
        'trades exist outside the hold-out too (the walk covered everything)':
            full['trades'] > hold['trades'],
        'the feed spy found no leak': spy.clean,
        'the engine logged 0 look-ahead violations':
            res.meta['audit_violations'] == 0,
        'every trade has a regime stamped at entry': bool(
            res.window_trades('holdout')['regime_at_entry'].notna().all()),
    }
    print()
    for label, ok in checks.items():
        print(f'  [{"OK" if ok else "FAIL"}] {label}')

    if hold['profit_factor'] > 2 or hold['win_pct'] > 70:
        print('\n  !! STANDING LAW TRIGGERED: profit factor > 2 or win rate > '
              '70%.\n     Assume a leak and hunt it before believing this '
              'number.')
    else:
        print(f'\n  Sanity: PF {hold["profit_factor"]:.2f}, win rate '
              f'{hold["win_pct"]:.1f}% — ordinary numbers for an ordinary '
              f'strategy.\n  Nothing here is being claimed as an edge.')

    ok = all(checks.values())
    print(f'\nDUMMY 2: {"PASSED" if ok else "FAILED"}\n')
    return ok, hold


# --------------------------------------------------------------------------
# DUMMY 3 — THE CHEAT
# --------------------------------------------------------------------------

def dummy_3_the_cheat(data, ma_card):
    print('=' * 70)
    print('DUMMY 3 — THE CHEAT (a planted look-ahead strategy)')
    print('=' * 70)
    print('The cheat is one line: look at TOMORROW\'S close, buy if it is '
          'higher.\nRun two ways — fed the future, and through the engine\'s '
          'own feed.\n')

    df = data.df
    holdout = df[df.index > pd.Timestamp(TRAIN_END)]

    # ---- (a) FED THE FUTURE, OUTSIDE THE ENGINE ------------------------
    print('-' * 70)
    print('(a) THE CHEAT FED THE FUTURE DIRECTLY — computed outside the engine')
    print('-' * 70)
    close = holdout['close'].values
    moves = np.diff(close) / close[:-1]
    # perfect direction every single candle: every move is a winning move
    perfect = float(np.prod(1.0 + np.abs(moves))) - 1.0
    buy_hold = float(close[-1] / close[0]) - 1.0
    print(f'  window        : {holdout.index[0]} -> {holdout.index[-1]}  '
          f'({len(holdout):,} candles)')
    print(f'  the cheat, no costs, full stake, correct every single candle:')
    print(f'      {big_pct(perfect * 100)}')
    print(f'  buy and hold over the same window : {buy_hold * 100:+.2f}%')
    print(f'  the honest MA cross (dummy 2)     : '
          f'{ma_card["net_return"]:+.2f}%')
    print('  This is what a leak is worth. Any strategy that returns numbers '
          'in\n  this neighbourhood is not a strategy, it is a bug.')
    cheat_works = perfect > 100 * max(abs(buy_hold), 0.01)

    # ---- (a2) THE FUTURE HANDED AROUND THE ENGINE ----------------------
    print()
    print('-' * 70)
    print('(a2) THE SAME CHEAT THROUGH THE ENGINE — but holding its own copy')
    print('     of the whole file, so the future reaches it AROUND the feed.')
    print('     (Same costs, same 1% sizing, same stops. Only the future '
          'differs.)')
    print('-' * 70)
    leaked = PerfectForesight(df)
    res_leak = run_backtest(data, leaked, strategy_name='cheat-leaked-future',
                            params=leaked.params, train_end=TRAIN_END,
                            regime=False, verbose=False)
    leak_card = res_leak.card('holdout')
    print(leak_card.text())
    _save(res_leak, 'dummy 3a2 — the leak succeeding')
    leak_trades = res_leak.window_trades('holdout')
    held = leak_trades['bars_held']
    print('\n  Read that as a warning, not a result: this is what the stat '
          'card of a\n  leaking strategy looks like from the inside. The '
          'engine cannot save a\n  strategy whose AUTHOR hands it the future — '
          'the engine only controls\n  what the FEED delivers. That is why '
          'strategy code gets read, and why\n  Step 2.4\'s lie detectors '
          'exist.')
    print('\n  WHY THIS IS "ONLY" A GOOD RETURN AND NOT A BILLION PERCENT '
          '(recorded so\n  nobody mistakes it for the engine half-containing '
          'the leak):')
    print(f'    The cheat sees exactly ONE candle ahead. But the engine holds '
          f'a trade\n    until an ATR stop or target is hit — a median of '
          f'{held.median():.0f} candles here, mean\n    {held.mean():.1f}, max '
          f'{held.max()}. Only {int((held == 1).sum())} of {len(held)} trades '
          f'lasted a single candle.')
    print('    So the peek buys the ENTRY direction and nothing else; the '
          'other ~5/6\n    of the exposure is blind, and rule-based exits '
          'decide the outcome.')
    print('    It also enters at the NEXT candle\'s OPEN while the peek is '
          'about that\n    candle\'s CLOSE — so the cheat is not even perfect '
          'on the one candle it\n    can see. Compare (a), where the cheat '
          'compounds close-to-close with no\n    holding period and no costs: '
          'THAT is the unbounded version.')
    print('\n    The leak\'s fingerprint is the SWING, not the size — see the '
          'comparison\n    against (b2) in the table at the end of this dummy.')

    # What this exhibit must prove: that the leak is WORTH something inside
    # the engine — it turns a loser into a winner. NOT that it prints an
    # absurd number: the engine's own discipline (next-open entry, ATR exits)
    # caps what one candle of foresight can buy. Demanding an absurd number
    # here would be demanding the wrong thing.
    leak_profitable = (leak_card['trades'] > 0
                       and leak_card['net_return'] > 0
                       and leak_card['profit_factor'] > 1.0
                       and leak_card['net_return'] > ma_card['net_return'])

    # ---- (b1) THROUGH THE ENGINE'S FEED: THE PEEK IS IMPOSSIBLE --------
    print()
    print('-' * 70)
    print('(b1) THE CHEAT THROUGH THE ENGINE\'S PROPER FEED')
    print('-' * 70)
    print('  Identical peek — `df[\'close\'].iloc[len(df)]`, one row past the '
          'end.\n  The engine hands over candles 0..i as their own copy. Row '
          'i+1 does not\n  exist, the lookup raises IndexError, and the cheat '
          'has nothing to read.\n')
    spy = FeedSpy(peek_at_tomorrow, df.index)
    res_blind = run_backtest(data, spy, strategy_name='cheat-through-the-feed',
                             params=peek_at_tomorrow.params,
                             train_end=TRAIN_END, regime=False, verbose=False)
    blind_card = res_blind.card('holdout')
    print(blind_card.text())
    _save(res_blind, 'dummy 3b1 — the cheat blinded')
    print('\n  THE STRUCTURAL PROOF (measured, not asserted):')
    for line in spy.report():
        print(f'    {line}')
    print(f'    engine\'s own look-ahead violations : '
          f'{res_blind.meta["audit_violations"]}   (must be 0)')

    # ---- (b2) WHAT THE CHEAT DEGRADES TO -------------------------------
    print()
    print('-' * 70)
    print('(b2) THE SAME CHEAT, BUT IT REFUSES TO GO FLAT')
    print('     When the peek fails it guesses "the last move continues".')
    print('     This is what the cheat IS once the future is taken away.')
    print('-' * 70)
    res_garbage = run_backtest(data, peek_or_guess,
                               strategy_name='cheat-degraded-to-a-guess',
                               params=peek_or_guess.params,
                               train_end=TRAIN_END, regime=False, verbose=False)
    garbage_card = res_garbage.card('holdout')
    print(garbage_card.text())
    _save(res_garbage, 'dummy 3b2 — the cheat degraded')

    print()
    print('  THE VERDICT OF DUMMY 3, IN ONE TABLE (hold-out window, '
          'same costs):')
    print(f'    cheat holding the future itself : '
          f'{leak_card["net_return"]:+12.2f}%   '
          f'({leak_card["trades"]} trades, win rate {leak_card["win_pct"]:.1f}%, '
          f'PF {leak_card["profit_factor"]:.2f})')
    print(f'    cheat through the engine\'s feed : '
          f'{blind_card["net_return"]:+12.2f}%   '
          f'({blind_card["trades"]} trades — it never got a number to cheat '
          f'with)')
    print(f'    cheat degraded to a guess       : '
          f'{garbage_card["net_return"]:+12.2f}%   '
          f'({garbage_card["trades"]} trades, win rate '
          f'{garbage_card["win_pct"]:.1f}%, PF '
          f'{garbage_card["profit_factor"]:.2f})')

    print('\n  THE LEAK\'S FINGERPRINT IS THE SWING, NOT THE SIZE. The leaked '
          'run and the\n  degraded run share the same entry cadence, the same '
          'ATR exits and the\n  same costs. The ONLY difference between them '
          'is one candle of future:')
    print(f'      win rate    {garbage_card["win_pct"]:.1f}%  ->  '
          f'{leak_card["win_pct"]:.1f}%')
    print(f'      profit fact {garbage_card["profit_factor"]:.2f}  ->  '
          f'{leak_card["profit_factor"]:.2f}')
    print(f'      net return  {garbage_card["net_return"]:+.2f}%  ->  '
          f'{leak_card["net_return"]:+.2f}%')
    print('  A losing strategy turned into a winning one by a single candle of '
          'future.\n  That is how much damage a leak does, and exactly why the '
          'feed is built\n  the way it is.')

    checks = {
        '(a) the cheat prints money when fed the future': cheat_works,
        '(a2) holding the future itself, the cheat turns a loser into a winner':
            leak_profitable,
        '(b1) through the feed: EVERY peek was refused by IndexError':
            spy.peek_refused == spy.peek_attempts and spy.peek_attempts > 0,
        '(b1) through the feed: not one future candle was ever delivered':
            spy.future_rows_delivered == 0,
        '(b1) through the feed: every delivery was exactly "up to now"':
            spy.wrong_length == 0,
        '(b1) through the feed: the blinded cheat took 0 trades':
            blind_card['trades'] == 0,
        '(b1) through the feed: the blinded cheat made 0 P&L':
            blind_card['net_return'] == 0.0,
        '(b1) the engine logged 0 look-ahead violations':
            res_blind.meta['audit_violations'] == 0,
        '(b2) degraded to a guess, the cheat is NOT profitable':
            garbage_card['net_return'] < 0,
        '(b2) degraded to a guess, its profit factor is under 1':
            garbage_card['profit_factor'] < 1.0,
        '(b2) the degraded cheat is nowhere near the leaked one':
            garbage_card['net_return'] < leak_card['net_return'],
    }
    print()
    for label, ok in checks.items():
        print(f'  [{"OK" if ok else "FAIL"}] {label}')
    ok = all(checks.values())
    print(f'\nDUMMY 3: {"PASSED" if ok else "FAILED"}')
    if not ok:
        print('  IF THE CHEAT SURVIVED THE FEED, THE LAB IS LYING. No real '
              'strategy\n  may be tested until this is fixed.')
    print()
    return ok


def main():
    print('=' * 70)
    print('ZAR X LAB — GATE 2.3: THE HONEST BACKTEST ENGINE')
    print('=' * 70)
    print(f'  market    : {ASSET} {TIMEFRAME}  (frozen vault only)')
    print(f'  train_end : {TRAIN_END}   <- RECORDED. Everything after this '
          f'date is\n              the hold-out; it is the only window whose '
          f'numbers count.')
    print()

    data = load_vault(ASSET, TIMEFRAME)
    print(f'  THE DOOR: {data.report.name} inspected at load -> '
          f'{data.verdict}')
    print(f'  {len(data.df):,} candles, {data.df.index[0]} -> '
          f'{data.df.index[-1]}')
    print('  (a FAIL verdict here would refuse the backtest outright)\n')

    d1 = dummy_1_always_flat(data)
    d2, ma_card = dummy_2_ma_cross(data)
    d3 = dummy_3_the_cheat(data, ma_card)

    print('=' * 70)
    print(f'  DUMMY 1 (always flat)   : {"PASSED" if d1 else "FAILED"}')
    print(f'  DUMMY 2 (MA cross 20/50): {"PASSED" if d2 else "FAILED"}')
    print(f'  DUMMY 3 (the cheat)     : {"PASSED" if d3 else "FAILED"}')
    print('-' * 70)
    ok = d1 and d2 and d3
    print(f'GATE 2.3: {"PASSED" if ok else "FAILED"}')
    print('=' * 70)
    print('\nEvidence written this run:')
    for p in saved_files:
        print(f'  {os.path.relpath(p, os.path.dirname(LAB_DIR))}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
