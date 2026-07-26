"""
Zar X Lab — Step 2.4, LIE DETECTOR #2: MONTE CARLO (the luck-of-the-order test).

WHAT IT IS FOR
A backtest hands you ONE ordering of trades — the one history happened to
deal. Deal the same trades in a different order and the ride changes
completely: five losses in a row early on can end an account that the original
ordering carried comfortably. The question this instrument answers is not
"what did it make?" but "how bad could the ride have been with the SAME
trades?" — because it is the ride, not the average, that stops a human from
following a strategy.

WHAT IT DOES
Reshuffles the sequence of per-trade percentage results 10,000 times,
compounds each shuffled path, and reports:
  - the max-drawdown distribution across all 10,000 shuffles
  - the 5th-percentile path: only 5 shuffles in 100 had a rougher ride
THE RULE (locked in the Execution Plan, Step 2.4 / Phase 6):
    5th-percentile max drawdown > 30%  ->  the strategy is a coin with good
    luck, whatever its average says. That is the verdict regardless of profit.

A TRUTH THIS INSTRUMENT MUST NOT HIDE
Reshuffling the SAME trades cannot change where the account ends up:
multiplying the same numbers in a different order gives the same product.
So there is no "distribution of final returns" from a reshuffle — there is one
final number and ten thousand different roads to it. Any tool that prints a
spread of final outcomes from a pure reshuffle is printing rounding dust and
calling it risk. This one prints the spread it measured (it should be ~0) and
says so.

To answer the different question — "what if the same edge had dealt a
different HAND?" — a second, clearly separated exhibit resamples the trades
WITH REPLACEMENT. That one does move the finish line, because it is a
different set of trades drawn from the same behaviour. It is shown as
information; the VERDICT above is judged on the reshuffle, as specified.

REPRODUCIBILITY
A Monte Carlo that cannot reproduce itself is not evidence. The random seed is
fixed, printed in the report, and recorded in the log. Two runs with the same
seed produce byte-identical reports.

WHAT IT COMPOUNDS
`return_pct` — each trade's net result as a fraction of the equity it started
with. A reshuffled sequence has no dollar history, so dollars would be
meaningless here; percentages of own equity are the only honest unit.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\monte_carlo.py
"""
import os
import sys

import numpy as np
import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)
sys.path.insert(0, os.path.dirname(LAB_DIR))

from engine import _max_drawdown as max_drawdown_of        # noqa: E402

N_PATHS = 10_000
SEED = 20260726          # RECORDED. Printed in every report. Never randomised.
RUIN_DRAWDOWN = 30.0     # percent — the line from the Execution Plan
CHECKPOINTS = 10         # how many stops along the 5th-percentile road we print


def _paths_and_drawdowns(returns, order):
    """Compound every path and measure how deep each one fell.

    `order` is a matrix of indices, one row per path. Drawdown is measured
    from the starting equity onwards — an account that never recovers its
    opening balance is in drawdown from candle one, which is exactly how it
    feels."""
    paths = returns[order]
    equity = np.cumprod(1.0 + paths, axis=1)
    peak = np.maximum(np.maximum.accumulate(equity, axis=1), 1.0)
    drawdown = (peak - equity) / peak
    return equity, drawdown.max(axis=1)


class MonteCarloReport(dict):

    def text(self):
        s = self
        L = []
        L.append('=' * 78)
        L.append(f'MONTE CARLO — {s["label"]}')
        L.append('=' * 78)
        L.append(f'  {s["source"]}')
        L.append(f'  {s["trades"]} trades reshuffled {s["paths"]:,} times.   '
                 f'RANDOM SEED: {s["seed"]}  <- recorded;')
        L.append('  the same seed reproduces these numbers exactly. A Monte '
                 'Carlo that cannot')
        L.append('  reproduce itself is not evidence.')
        L.append('')
        L.append('  THE TRADES AS HISTORY DEALT THEM (the original order):')
        L.append(f'    net return    : {s["actual_return"]:+.2f}%')
        L.append(f'    max drawdown  : {s["actual_drawdown"]:.2f}%')
        L.append('')
        L.append('  WHERE EVERY SHUFFLE ENDS UP:')
        L.append(f'    final return, best shuffle  : {s["final_best"]:+.4f}%')
        L.append(f'    final return, worst shuffle : {s["final_worst"]:+.4f}%')
        L.append(f'    the spread between them     : {s["final_spread"]:.6f} '
                 f'percentage points')
        L.append('    -> All shuffles finish in the same place, as they must: '
                 'the same numbers')
        L.append('       multiplied in a different order give the same '
                 'product. What changes is')
        L.append('       the ROAD, and the road is what this instrument '
                 'measures.')
        L.append('')
        L.append(f'  THE MAX-DRAWDOWN DISTRIBUTION over {s["paths"]:,} '
                 f'reshuffles:')
        L.append(f'    the gentlest ride (best of all)      : '
                 f'{s["dd_min"]:6.2f}%')
        L.append(f'    typical ride (median)                : '
                 f'{s["dd_median"]:6.2f}%')
        L.append(f'    a rough ride  (75th percentile)      : '
                 f'{s["dd_p75"]:6.2f}%')
        L.append(f'    a bad ride    (90th percentile)      : '
                 f'{s["dd_p90"]:6.2f}%')
        L.append(f'    THE 5th-PERCENTILE RIDE (95th pct)   : '
                 f'{s["dd_p95"]:6.2f}%   <- the number the rule judges')
        L.append(f'    the worst shuffle of all             : '
                 f'{s["dd_max"]:6.2f}%')
        L.append('    ("5th-percentile ride" = only 5 shuffles in 100 were '
                 'rougher than this.')
        L.append('     It is a bad-luck case that is entirely plausible, not '
                 'a doomsday case.)')
        L.append('')
        L.append('  THE 5th-PERCENTILE EQUITY PATH (an account of 100 units '
                 'walking that road):')
        L.append('    after trade:  ' + '  '.join(
            f'{n:>7}' for n in s['checkpoint_trades']))
        L.append('    equity     :  ' + '  '.join(
            f'{v:7.2f}' for v in s['checkpoint_equity']))
        L.append(f'    deepest point on that path: {s["p95_path_drawdown"]:.2f}% '
                 f'below its own peak')
        L.append('')
        L.append('  VERDICT ON THE RULE (5th-percentile drawdown must stay '
                 f'under {RUIN_DRAWDOWN:.0f}%):')
        if s['ruin_flag']:
            L.append(f'    {s["dd_p95"]:.2f}% > {RUIN_DRAWDOWN:.0f}%  ->  '
                     f'RUIN FLAG RAISED.')
            L.append('    This strategy is a coin with good luck. Its average '
                     'is not the point:')
            L.append('    one plausible reordering of its OWN trades takes a '
                     'ruinous bite out of')
            L.append('    the account, and no human keeps following a system '
                     'through that.')
        else:
            L.append(f'    {s["dd_p95"]:.2f}% <= {RUIN_DRAWDOWN:.0f}%  ->  '
                     f'passes the reshuffle test.')
            L.append('    This says the ride is survivable, NOT that the '
                     'strategy makes money.')
            L.append('    A losing strategy can pass this test comfortably by '
                     'losing smoothly.')
        L.append('')
        L.append('  SECOND EXHIBIT — a different HAND, not just a different '
                 'order')
        L.append('  (the same trades drawn WITH REPLACEMENT: this one can '
                 'move the finish line,')
        L.append('   and it is information only — the rule above is judged on '
                 'the reshuffle):')
        L.append(f'    final return, 5th percentile  : '
                 f'{s["boot_return_p05"]:+.2f}%')
        L.append(f'    final return, median          : '
                 f'{s["boot_return_p50"]:+.2f}%')
        L.append(f'    final return, 95th percentile : '
                 f'{s["boot_return_p95"]:+.2f}%')
        L.append(f'    share of hands that lost money: '
                 f'{s["boot_share_losing"]:.1f}%')
        L.append(f'    5th-percentile drawdown       : '
                 f'{s["boot_dd_p95"]:.2f}%')
        L.append('=' * 78)
        return '\n'.join(L)

    def numbers(self):
        """Just the figures, for a reproducibility check that does not depend
        on how the text happens to be formatted."""
        return {k: v for k, v in self.items()
                if isinstance(v, (int, float, str))}


def monte_carlo(returns, n_paths=N_PATHS, seed=SEED, label='monte carlo',
                source='(returns supplied directly)'):
    """returns: a sequence of per-trade results as FRACTIONS of the equity each
    trade started with (the `return_pct` column). Never dollars."""
    r = np.asarray(pd.Series(list(returns)).astype(float).values)
    n = len(r)
    if n < 2:
        raise ValueError(
            f'a Monte Carlo on {n} trade(s) is theatre, not evidence. '
            f'Reshuffling needs a sequence to reshuffle.')

    rng = np.random.default_rng(seed)

    # independent uniform permutations, one per row, from one seeded stream
    order = np.argsort(rng.random((n_paths, n)), axis=1)
    equity, maxdd = _paths_and_drawdowns(r, order)
    finals = 100.0 * (equity[:, -1] - 1.0)

    # the honest self-check: our vectorised drawdown must agree with the
    # engine's own definition on the one path history actually dealt
    actual_dd = 100.0 * max_drawdown_of(r)
    _, dd_check = _paths_and_drawdowns(r, np.arange(n)[None, :])
    if abs(100.0 * dd_check[0] - actual_dd) > 1e-9:
        raise RuntimeError(
            'the Monte Carlo measures drawdown differently from the engine. '
            'One definition or the other is wrong; refusing to report.')

    dd_p95 = float(np.percentile(maxdd, 95))
    # the path that actually walked the 5th-percentile road (a real path, not
    # an interpolated one — we print an equity curve, so it must be genuine)
    p95_i = int(np.argmin(np.abs(maxdd - dd_p95)))
    path = equity[p95_i]
    stops = np.unique(np.linspace(1, n, min(CHECKPOINTS, n)).astype(int))

    # second exhibit: resample WITH replacement (a different hand)
    boot_order = rng.integers(0, n, size=(n_paths, n))
    boot_equity, boot_dd = _paths_and_drawdowns(r, boot_order)
    boot_finals = 100.0 * (boot_equity[:, -1] - 1.0)

    return MonteCarloReport({
        'label': label,
        'source': source,
        'seed': int(seed),
        'paths': int(n_paths),
        'trades': int(n),
        'actual_return': 100.0 * (float(np.prod(1.0 + r)) - 1.0),
        'actual_drawdown': actual_dd,
        'final_best': float(finals.max()),
        'final_worst': float(finals.min()),
        'final_spread': float(finals.max() - finals.min()),
        'dd_min': float(maxdd.min()) * 100.0,
        'dd_median': float(np.percentile(maxdd, 50)) * 100.0,
        'dd_p75': float(np.percentile(maxdd, 75)) * 100.0,
        'dd_p90': float(np.percentile(maxdd, 90)) * 100.0,
        'dd_p95': dd_p95 * 100.0,
        'dd_max': float(maxdd.max()) * 100.0,
        'ruin_flag': bool(dd_p95 * 100.0 > RUIN_DRAWDOWN),
        'checkpoint_trades': [int(x) for x in stops],
        'checkpoint_equity': [round(100.0 * float(path[x - 1]), 2) for x in stops],
        'p95_path_drawdown': float(maxdd[p95_i]) * 100.0,
        'boot_return_p05': float(np.percentile(boot_finals, 5)),
        'boot_return_p50': float(np.percentile(boot_finals, 50)),
        'boot_return_p95': float(np.percentile(boot_finals, 95)),
        'boot_share_losing': 100.0 * float((boot_finals < 0).mean()),
        'boot_dd_p95': float(np.percentile(boot_dd, 95)) * 100.0,
    })


def monte_carlo_result(result, window='holdout', n_paths=N_PATHS, seed=SEED):
    """Run the instrument on a BacktestResult straight from the engine."""
    trades = result.window_trades(window)
    m = result.meta
    source = (f'{m["strategy"]} [{m["fingerprint"]} @ {m["commit"]}] on '
              f'{m["asset"]} {m["timeframe"]}, {window} window '
              f'(train_end {m["train_end"]})')
    return monte_carlo(trades['return_pct'].values, n_paths=n_paths, seed=seed,
                       label=f'{m["strategy"]} — {window.upper()}',
                       source=source)


if __name__ == '__main__':
    from engine import load_vault, run_backtest        # noqa: E402
    from dummies import MACross                        # noqa: E402

    strat = MACross(20, 50)
    data = load_vault('BTC-USD', '4h')
    res = run_backtest(data, strat, strategy_name=strat.name,
                       params=strat.params, train_end='2025-10-01',
                       verbose=False)
    print(monte_carlo_result(res).text())
