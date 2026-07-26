"""
Zar X Lab — Step 2.4, LIE DETECTOR #1: THE WALK-FORWARD (lucky-month catcher).

WHAT IT IS FOR
One number for a whole hold-out window hides the most common way a backtest
lies to its owner: the strategy did nothing for months and then caught ONE
enormous move. The average looks like an edge. It is a lottery ticket, and it
will not be there next year. The +20% February that flipped sign when the
window moved is the reason this file exists.

So the hold-out is cut into 6 consecutive windows and each one is scored on
its own. Two questions are then asked, and the verdict is the AND of both:

  1. CONSISTENCY  — was it profitable in at least 60% of the windows?
  2. CONCENTRATION— did any single window supply more than 50% of the profit?
                    If yes, the "edge" is one lucky stretch wearing a costume.

THE EDGE CASE, DEFINED BEFORE THE CODE WAS WRITTEN
Question 2 only MEANS anything when there is profit to divide. If the total is
zero or negative, "this window is 300% of the profit" is arithmetic noise, and
dividing by a zero or negative total prints nonsense that a reader could
mistake for a finding. So:

    total profit <= 0  ->  the concentration test DOES NOT RUN. It is reported
                           as "does not apply", in words, and the verdict is
                           already INCONSISTENT — because a strategy that lost
                           money over the hold-out is not consistent at
                           anything except losing.

The MA-cross dummy of Gate 2.3 IS a loser (net -4.88%), so this path is the
one the gate walks. That is deliberate: the edge case is tested, not imagined.

WINDOWS WITH NO TRADES are printed as "no trades" and counted as windows. They
are never silently dropped. A quiet window is information — a strategy that
sits out a third of the year is a different animal from one that trades
throughout — and dropping it would quietly improve the consistency score.

WHY THE WINDOWS DO NOT OVERLAP
"Rolling" here means the window rolls forward through time, not that the
windows share trades. Each trade is counted in exactly ONE window; otherwise
the windows' shares of the profit would add up to more than the profit and
the 50% rule would be meaningless.

WHAT IT MEASURES PROFIT IN
`return_pct` — each trade's net result as a fraction of the equity it started
with. Never raw dollars: a window's dollars carry the account history of every
trade BEFORE the window, which has nothing to do with the window.
Two totals are shown per window and they are different on purpose:
  SUM  the arithmetic sum of the trades' percentages. Parts of a sum add up to
       the whole, so this is what "share of total profit" is computed from.
  NET  the same trades compounded, in order. This is what the account did.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\walk_forward.py
"""
import os
import sys

import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)
sys.path.insert(0, os.path.dirname(LAB_DIR))

from trade_stats import summarise, pf_text                       # noqa: E402

N_WINDOWS = 6
MIN_PROFITABLE_SHARE = 0.60      # at least 60% of windows must make money
MAX_WINDOW_SHARE = 50.0          # no window may supply more than 50% of profit


# --------------------------------------------------------------------------
# Cutting the hold-out into windows
# --------------------------------------------------------------------------

def _boundaries_from_index(index, n_windows):
    """Equal numbers of CANDLES per window (the honest cut when we have the
    candle grid: every window is the same amount of market)."""
    n = len(index)
    if n < n_windows:
        raise ValueError(f'cannot cut {n} candles into {n_windows} windows')
    edges = []
    for k in range(n_windows):
        a = (k * n) // n_windows
        b = ((k + 1) * n) // n_windows - 1
        edges.append((index[a], index[b], b - a + 1))
    return edges


def _boundaries_from_times(times, n_windows):
    """Equal amounts of TIME per window (used when there is no candle grid —
    e.g. a synthetic trade sequence built in memory by a gate script)."""
    t0, t1 = pd.Timestamp(min(times)), pd.Timestamp(max(times))
    if t1 <= t0:
        raise ValueError('the trades do not span any time')
    step = (t1 - t0) / n_windows
    edges = []
    for k in range(n_windows):
        a = t0 + k * step
        b = (t0 + (k + 1) * step) if k < n_windows - 1 else t1
        edges.append((a, b, None))
    return edges


# --------------------------------------------------------------------------
# The report
# --------------------------------------------------------------------------

class WalkForwardReport:

    def __init__(self, label, source, windows, n_windows, total_profit,
                 concentration_applies, worst_window, verdict, reasons):
        self.label = label
        self.source = source
        self.windows = windows                  # list of dicts, one per window
        self.n_windows = n_windows
        self.total_profit = total_profit        # arithmetic sum, in %
        self.concentration_applies = concentration_applies
        self.worst_window = worst_window        # the biggest contributor, or None
        self.verdict = verdict                  # 'CONSISTENT' | 'INCONSISTENT'
        self.reasons = reasons

    # -- the two flags a caller (or a gate) can test ----------------------
    @property
    def profitable_windows(self):
        return sum(1 for w in self.windows if w['stats']['net_return'] > 0)

    @property
    def consistency_ok(self):
        return (self.profitable_windows / self.n_windows) >= MIN_PROFITABLE_SHARE

    @property
    def lucky_window_flag(self):
        """TRUE when one window carried more than half the profit. This is the
        alarm the detector exists to raise. It can only be raised when there
        IS profit — see the edge case in the module docstring."""
        return bool(self.concentration_applies
                    and self.worst_window is not None
                    and self.worst_window['share'] > MAX_WINDOW_SHARE)

    def text(self):
        L = []
        L.append('=' * 78)
        L.append(f'WALK-FORWARD — {self.label}')
        L.append('=' * 78)
        L.append(f'  {self.source}')
        L.append(f'  The hold-out is cut into {self.n_windows} consecutive '
                 f'windows. Each is scored alone.')
        L.append('')
        L.append('  #  from         to           candles  trades  win%     PF   '
                 '  SUM%     NET%   maxDD%   share of profit')
        L.append('  ' + '-' * 74)
        for w in self.windows:
            s = w['stats']
            when = (f'{str(w["start"])[:10]}   {str(w["end"])[:10]}')
            candles = f'{w["candles"]:7,}' if w['candles'] else '      -'
            if s['no_trades']:
                L.append(f'  {w["n"]}  {when}  {candles}       0   '
                         f'  no trades in this window (counted, never skipped)')
                continue
            share = ('     -    ' if not self.concentration_applies
                     else f'{w["share"]:8.1f}% ')
            L.append(f'  {w["n"]}  {when}  {candles}  {s["trades"]:6}  '
                     f'{s["win_pct"]:5.1f}  {pf_text(s["profit_factor"])}  '
                     f'{s["sum_return"]:+7.2f}  {s["net_return"]:+7.2f}  '
                     f'{s["max_drawdown"]:6.2f}   {share}')
        L.append('  ' + '-' * 74)
        L.append(f'  TOTAL (arithmetic sum of every trade\'s percent result): '
                 f'{self.total_profit:+.2f}%')
        L.append('')

        # -- test 1 ------------------------------------------------------
        traded = sum(1 for w in self.windows if not w['stats']['no_trades'])
        L.append(f'  TEST 1 — CONSISTENCY: profitable in {self.profitable_windows} '
                 f'of {self.n_windows} windows '
                 f'({100.0 * self.profitable_windows / self.n_windows:.0f}%), '
                 f'needs {MIN_PROFITABLE_SHARE:.0%}.')
        L.append(f'           -> {"PASS" if self.consistency_ok else "FAIL"}'
                 f'   ({traded} of {self.n_windows} windows contained any '
                 f'trades at all; a window that')
        L.append(f'              made no money is not counted as profitable, '
                 f'whatever the reason.)')

        # -- test 2, or the honest refusal to run it ---------------------
        L.append('')
        if not self.concentration_applies:
            L.append(f'  TEST 2 — CONCENTRATION: DOES NOT APPLY. The strategy '
                     f'finished the hold-out at')
            L.append(f'           {self.total_profit:+.2f}% — there is no profit '
                     f'to divide into shares, so asking')
            L.append('           "which window carried the profit?" would be '
                     'arithmetic on nothing.')
            L.append('           No number is printed here because any number '
                     'printed here would be')
            L.append('           misleading. The verdict does not need it: a '
                     'losing strategy is already')
            L.append('           INCONSISTENT.')
        else:
            w = self.worst_window
            L.append(f'  TEST 2 — CONCENTRATION: the biggest single contributor '
                     f'is window {w["n"]} '
                     f'({str(w["start"])[:10]} -> {str(w["end"])[:10]}),')
            L.append(f'           which supplied {w["share"]:.1f}% of the total '
                     f'profit. The limit is {MAX_WINDOW_SHARE:.0f}%.')
            L.append(f'           -> {"FAIL — LUCKY-WINDOW FLAG RAISED" if self.lucky_window_flag else "PASS"}')
            if self.lucky_window_flag:
                L.append('           One stretch of time is carrying this '
                         'strategy. Remove that window and')
                L.append(f'           the rest of the hold-out made '
                         f'{self.total_profit - w["sum_return"]:+.2f}%. That is '
                         f'the strategy without its lucky')
                L.append('           month — treat THAT as the honest '
                         'expectation.')

        L.append('')
        L.append(f'  VERDICT: {self.verdict}')
        for r in self.reasons:
            L.append(f'    - {r}')
        L.append('=' * 78)
        return '\n'.join(L)


# --------------------------------------------------------------------------
# The instrument
# --------------------------------------------------------------------------

def walk_forward_trades(trades, n_windows=N_WINDOWS, index=None,
                        label='walk-forward', source='(trades supplied directly)'):
    """The core. Scores a set of trades window by window.

    trades  : DataFrame with at least `entry_time` and `return_pct`
    index   : the candle index of the window being cut, when it is known.
              With it, every window holds the same number of candles. Without
              it (a synthetic sequence), the windows hold equal amounts of
              time instead, cut from the first and last entry.
    """
    trades = trades.copy()
    # a strategy that never traded still gets a real window table — six windows
    # of "no trades" is a finding, not an error
    has_trades = len(trades) > 0 and 'entry_time' in trades.columns
    if has_trades:
        trades['entry_time'] = pd.to_datetime(trades['entry_time'])

    if index is not None and len(index):
        edges = _boundaries_from_index(pd.DatetimeIndex(index), n_windows)
    elif has_trades:
        edges = _boundaries_from_times(trades['entry_time'], n_windows)
    else:
        raise ValueError('nothing to cut: no candle index and no trades')

    windows = []
    for k, (start, end, candles) in enumerate(edges, start=1):
        if not has_trades:
            sub = trades
        else:
            if k < n_windows:
                nxt = edges[k][0]
                sel = ((trades['entry_time'] >= start)
                       & (trades['entry_time'] < nxt))
            else:                          # the last window keeps its own end
                sel = ((trades['entry_time'] >= start)
                       & (trades['entry_time'] <= end))
            sub = trades[sel]
        windows.append({'n': k, 'start': start, 'end': end,
                        'candles': candles, 'stats': summarise(sub),
                        'trades_df': sub, 'share': None})

    counted = sum(w['stats']['trades'] for w in windows)
    if has_trades and counted != len(trades):
        raise RuntimeError(
            f'window cut lost trades: {counted} of {len(trades)} landed in a '
            f'window. Every trade must be counted exactly once or the shares '
            f'of profit are fiction.')

    total = sum(w['stats']['sum_return'] for w in windows)

    # ---- THE EDGE CASE, handled once, here --------------------------------
    concentration_applies = total > 0.0
    worst = None
    if concentration_applies:
        for w in windows:
            w['share'] = 100.0 * w['stats']['sum_return'] / total
        worst = max(windows, key=lambda w: w['share'])
        worst = {'n': worst['n'], 'start': worst['start'], 'end': worst['end'],
                 'share': worst['share'],
                 'sum_return': worst['stats']['sum_return']}

    report = WalkForwardReport(label, source, windows, n_windows, total,
                               concentration_applies, worst, 'PENDING', [])

    reasons = []
    if not report.consistency_ok:
        reasons.append(
            f'profitable in only {report.profitable_windows} of {n_windows} '
            f'windows (needs {int(MIN_PROFITABLE_SHARE * n_windows + 0.999)}).')
    if not concentration_applies:
        reasons.append(
            f'the hold-out total is {total:+.2f}% — the strategy lost money '
            f'overall, so it is inconsistent by definition and the '
            f'"one lucky window" test was not run (it needs a positive total '
            f'to mean anything).')
    elif report.lucky_window_flag:
        reasons.append(
            f'window {worst["n"]} alone supplied {worst["share"]:.1f}% of the '
            f'profit — more than half. This is the lucky-window pattern the '
            f'detector exists to catch.')
    if not reasons:
        reasons.append(
            f'profitable in {report.profitable_windows} of {n_windows} windows '
            f'and no single window supplied more than {MAX_WINDOW_SHARE:.0f}% '
            f'of the profit (biggest was {worst["share"]:.1f}%). '
            f'Consistent is not the same as good — it means the result is '
            f'spread out, not that the edge is real.')
        report.verdict = 'CONSISTENT'
    else:
        report.verdict = 'INCONSISTENT'
    report.reasons = reasons
    return report


def walk_forward(result, window='holdout', n_windows=N_WINDOWS, label=None):
    """Run the detector on a BacktestResult straight from the engine."""
    idx = result.index
    te = result.meta['train_end']
    if te is not None and window == 'holdout':
        idx = idx[idx > te]
    elif te is not None and window == 'train':
        idx = idx[idx <= te]
    trades = result.window_trades(window)
    m = result.meta
    source = (f'{m["strategy"]} [{m["fingerprint"]} @ {m["commit"]}] on '
              f'{m["asset"]} {m["timeframe"]}, {window} window '
              f'(train_end {m["train_end"]}), {len(idx):,} candles, '
              f'{len(trades)} trades')
    return walk_forward_trades(
        trades, n_windows=n_windows, index=idx,
        label=label or f'{m["strategy"]} — {window.upper()}', source=source)


if __name__ == '__main__':
    from engine import load_vault, run_backtest       # noqa: E402
    from dummies import MACross                       # noqa: E402

    strat = MACross(20, 50)
    data = load_vault('BTC-USD', '4h')
    res = run_backtest(data, strat, strategy_name=strat.name,
                       params=strat.params, train_end='2025-10-01',
                       verbose=False)
    print(walk_forward(res).text())
