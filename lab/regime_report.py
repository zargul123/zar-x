"""
Zar X Lab — Step 2.4, LIE DETECTOR #3: THE REGIME BREAKDOWN.

WHAT IT IS FOR
A single stat card averages together weather that has nothing in common. A
trend-following strategy can look mediocre overall while being genuinely good
in Trending markets and catastrophic in Chaotic ones — and the average hides
both facts. Every per-trade row already carries `regime_at_entry`, stamped by
the live Regime Vane using ONLY candles that had closed before the entry. This
instrument simply groups by it and prints the truth per weather.

WHAT IT IS NOT — READ THIS BEFORE USING ANY NUMBER BELOW
It is INFORMATION FOR THE VERDICT, NEVER AN AUTO-FILTER. It is not an
instruction to "only trade the good regime". Deleting the losing regimes from
a result is the oldest form of curve-fitting there is: with three buckets and
a coin, one bucket always looks brilliant. If a regime filter is ever added to
a strategy it becomes a NEW strategy with a NEW fingerprint, and it goes back
through the whole Lab from the start, on the hold-out it has never seen. This
file changes no strategy and filters nothing. It only tells you where the
money came from and where it went.

SMALL SAMPLES ARE MARKED, NOT SILENTLY PRINTED
A regime holding 4 trades has no statistics in it. Any bucket under 10 trades
is printed with a warning, and under 30 it is marked "thin". The numbers are
still shown — hiding them would be its own kind of lie — but they are never
allowed to look like evidence.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\regime_report.py
"""
import os
import sys

import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)
sys.path.insert(0, os.path.dirname(LAB_DIR))

from trade_stats import summarise, pf_text                      # noqa: E402

THIN_SAMPLE = 30         # below this, a bucket is "thin"
MEANINGLESS_SAMPLE = 10  # below this, it means nothing at all


class RegimeReport:

    def __init__(self, label, source, buckets, overall):
        self.label = label
        self.source = source
        self.buckets = buckets          # list of (regime, stats), biggest first
        self.overall = overall

    @property
    def regimes(self):
        return [name for name, _ in self.buckets]

    def text(self):
        L = []
        L.append('=' * 78)
        L.append(f'REGIME BREAKDOWN — {self.label}')
        L.append('=' * 78)
        L.append(f'  {self.source}')
        L.append('  The weather at each entry was read by the live Regime Vane '
                 'from candles that')
        L.append('  had ALREADY CLOSED before that entry. Nothing here was '
                 'chosen after the fact.')
        L.append('')
        L.append('  regime        trades  share   win%     PF    avg win   '
                 'avg loss     SUM%     NET%   maxDD%')
        L.append('  ' + '-' * 74)
        total = self.overall['trades']
        for name, s in self.buckets:
            share = 100.0 * s['trades'] / total if total else 0.0
            aw = f'{s["avg_win"]:+7.2f}' if s['avg_win'] is not None else '      -'
            al = f'{s["avg_loss"]:+8.2f}' if s['avg_loss'] is not None else '       -'
            L.append(f'  {name:<12} {s["trades"]:6}  {share:5.1f}%  '
                     f'{s["win_pct"]:5.1f}  {pf_text(s["profit_factor"])}  '
                     f'{aw}   {al}  {s["sum_return"]:+7.2f}  '
                     f'{s["net_return"]:+7.2f}  {s["max_drawdown"]:6.2f}')
        L.append('  ' + '-' * 74)
        o = self.overall
        oaw = f'{o["avg_win"]:+7.2f}' if o['avg_win'] is not None else '      -'
        oal = f'{o["avg_loss"]:+8.2f}' if o['avg_loss'] is not None else '       -'
        L.append(f'  {"ALL":<12} {o["trades"]:6}  100.0%  {o["win_pct"]:5.1f}  '
                 f'{pf_text(o["profit_factor"])}  {oaw}   {oal}  '
                 f'{o["sum_return"]:+7.2f}  {o["net_return"]:+7.2f}  '
                 f'{o["max_drawdown"]:6.2f}')
        L.append('')
        L.append('  IN PLAIN WORDS:')
        for name, s in self.buckets:
            verdict = ('made money' if s['sum_return'] > 0
                       else 'lost money' if s['sum_return'] < 0
                       else 'broke even')
            note = ''
            if s['trades'] < MEANINGLESS_SAMPLE:
                note = ('  <- ONLY %d trades. This is an anecdote, not a '
                        'statistic.' % s['trades'])
            elif s['trades'] < THIN_SAMPLE:
                note = ('  <- thin sample (%d trades); treat as a hint at most.'
                        % s['trades'])
            L.append(f'    {name}: {s["trades"]} trades, {verdict} '
                     f'({s["sum_return"]:+.2f}% summed, win rate '
                     f'{s["win_pct"]:.1f}%).{note}')
        L.append('')
        L.append('  THIS IS INFORMATION, NOT A FILTER. Nothing above was used '
                 'to remove a single')
        L.append('  trade from any stat card. Keeping only the flattering '
                 'regime is curve-fitting:')
        L.append('  with three buckets, one of them always looks good. If the '
                 'Commander ever decides')
        L.append('  a regime filter belongs in a strategy, that is a NEW '
                 'strategy with a NEW')
        L.append('  fingerprint and it starts the Lab again from the door.')
        L.append('=' * 78)
        return '\n'.join(L)


def regime_report_trades(trades, label='regime breakdown',
                         source='(trades supplied directly)'):
    if trades is None or len(trades) == 0:
        raise ValueError(
            'no trades to break down by regime. A regime report on zero '
            'trades would be six empty rows pretending to be analysis.')
    if 'regime_at_entry' not in trades.columns:
        raise ValueError(
            'these trades carry no regime_at_entry column. The engine stamps '
            'it on every row; a file without it did not come from the engine.')

    col = trades['regime_at_entry'].fillna('Unrecorded').astype(str)
    buckets = []
    for name in col.value_counts().index:            # biggest bucket first
        buckets.append((name, summarise(trades[col == name])))

    counted = sum(s['trades'] for _, s in buckets)
    if counted != len(trades):
        raise RuntimeError(
            f'{counted} of {len(trades)} trades landed in a regime bucket. '
            f'Every trade belongs to exactly one weather; refusing to report.')

    return RegimeReport(label, source, buckets, summarise(trades))


def regime_report(result, window='holdout'):
    """Run the instrument on a BacktestResult straight from the engine."""
    trades = result.window_trades(window)
    m = result.meta
    source = (f'{m["strategy"]} [{m["fingerprint"]} @ {m["commit"]}] on '
              f'{m["asset"]} {m["timeframe"]}, {window} window '
              f'(train_end {m["train_end"]}), {len(trades)} trades')
    return regime_report_trades(
        trades, label=f'{m["strategy"]} — {window.upper()}', source=source)


if __name__ == '__main__':
    from engine import load_vault, run_backtest        # noqa: E402
    from dummies import MACross                        # noqa: E402

    strat = MACross(20, 50)
    data = load_vault('BTC-USD', '4h')
    res = run_backtest(data, strat, strategy_name=strat.name,
                       params=strat.params, train_end='2025-10-01',
                       verbose=False)
    print(regime_report(res).text())
