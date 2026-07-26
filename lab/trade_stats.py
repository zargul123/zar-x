"""
Zar X Lab — Step 2.4 plumbing: the stat card for ANY subset of trades.

WHY THIS SMALL FILE EXISTS
The engine's own `BacktestResult.card()` can only score three fixed windows
(full / train / hold-out). The three lie detectors all need the same
arithmetic on ARBITRARY subsets — a walk-forward window, one regime's trades,
a reshuffled sequence. Rather than write the same profit-factor and drawdown
formulas three times (three places to be subtly wrong, and no way to notice),
they are written once, here, and imported by all three.

THE ONE RULE THAT MATTERS — WHY EVERYTHING IS `return_pct`
Every trade carries `return_pct`: its net result as a fraction of the equity
it STARTED with. That number is self-contained. Raw dollars are not: a trade's
$-P&L depends on how big the account had grown by then, which depends on every
trade before it — including trades that are not in the subset we are scoring.
Compound a window's dollars and you are secretly reporting the history of
trades outside that window. So: percentages of own equity, always.

The max-drawdown formula is imported from engine.py rather than rewritten, so
the Lab has exactly ONE definition of "drawdown" and it cannot drift.
"""
import os
import sys

import numpy as np
import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)
sys.path.insert(0, os.path.dirname(LAB_DIR))

from engine import _max_drawdown as max_drawdown_of   # noqa: E402  (ONE definition)


def summarise(trades):
    """Score any set of trades. `trades` is a DataFrame with `return_pct`.

    Returns a plain dict. An empty set is NOT an error and NOT a zero-return
    strategy — it is 'no trades', and the caller must say so in words.

    Percentage conventions in the returned dict:
      *_pct fields are already multiplied by 100 (so -4.88 means -4.88%).
      `sum_return`   the arithmetic sum of the trades' percent results. This is
                     the ONLY honest way to ask "what share of the profit came
                     from this window?", because compounded percentages do not
                     add up to the whole — products do not split into parts.
      `net_return`   the compounded result of the same trades, in order. This
                     is what the account actually did.
    """
    if trades is None or len(trades) == 0:
        return {'trades': 0, 'no_trades': True, 'wins': 0, 'losses': 0,
                'win_pct': None, 'profit_factor': None, 'avg_win': None,
                'avg_loss': None, 'sum_return': 0.0, 'net_return': 0.0,
                'max_drawdown': 0.0, 'best': None, 'worst': None,
                'longs': 0, 'shorts': 0}

    r = np.asarray(pd.Series(trades['return_pct']).astype(float).values)
    wins, losses = r[r > 0], r[r <= 0]
    gross_win = float(wins.sum())
    gross_loss = float(-losses.sum())
    equity = float(np.prod(1.0 + r))

    direction = (trades['direction'] if 'direction' in trades
                 else pd.Series([], dtype=object))

    return {
        'trades': int(len(r)),
        'no_trades': False,
        'wins': int(len(wins)),
        'losses': int(len(losses)),
        'win_pct': 100.0 * len(wins) / len(r),
        # a set with no losing trade has no denominator: infinity, said plainly
        'profit_factor': (gross_win / gross_loss) if gross_loss > 0 else float('inf'),
        'avg_win': 100.0 * float(wins.mean()) if len(wins) else None,
        'avg_loss': 100.0 * float(losses.mean()) if len(losses) else None,
        'sum_return': 100.0 * float(r.sum()),
        'net_return': 100.0 * (equity - 1.0),
        'max_drawdown': 100.0 * max_drawdown_of(r),
        'best': 100.0 * float(r.max()),
        'worst': 100.0 * float(r.min()),
        'longs': int((direction == 'long').sum()) if len(direction) else 0,
        'shorts': int((direction == 'short').sum()) if len(direction) else 0,
    }


def pf_text(pf):
    """Profit factor as a human reads it, including the awkward cases."""
    if pf is None:
        return '   -  '
    if pf == float('inf'):
        return '  inf '      # not one losing trade in the set
    return f'{pf:6.2f}'


def pct_text(x, width=7):
    return f'{x:+{width}.2f}' if x is not None else ' ' * (width - 1) + '-'


if __name__ == '__main__':
    print(__doc__)
